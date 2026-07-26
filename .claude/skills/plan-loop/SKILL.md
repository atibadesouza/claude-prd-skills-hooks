---
name: plan-loop
description: Orchestrate the plan ↔ reviewer loop in a single chat. Spawns the `reviewer` skill as a subagent, parses its verdict, revises the plan in place, and re-spawns until APPROVED or the round cap is hit. Defaults to pausing each round for human approval; pass `--auto` for autonomous revision. Hard cap forces human checkpoint after 4 rounds regardless of mode.
argument-hint: [plan path | empty for latest docs/plans/*.md] [--auto] [--max=N]
---

You are orchestrating an automated plan-review loop. The planner is **you** (in this main chat); the reviewer is a subagent spawned via the Agent tool, running the `reviewer` skill against the same plan file.

Your job is to drive rounds of review → revise → re-review until the reviewer issues `APPROVED`, or until you hit a stopping condition that requires human input.

## The most important rule: push back

**You wrote the plan. You are not subordinate to the reviewer.** The reviewer is a senior architect offering a second opinion — they are frequently right, and sometimes wrong. Your job in this loop is *not* to placate the reviewer until they approve. Your job is to converge on the **correct** plan.

That means:
- When the reviewer is right, accept the correction cleanly and update the plan.
- When the reviewer is wrong, partially wrong, or missing context you have, **push back in writing** in the Review log. Do not silently change the plan to match. Do not soften your position to avoid another round.
- When you are unsure, say so — in the Review log, mark the point as "open" and let the next round resolve it (or kick to the human).

A loop where the planner caves on every point converges fast but produces a plan shaped by the reviewer's biases, not the truth. A loop where the planner pushes back honestly takes more rounds but produces a defensible plan. Optimize for the latter.

The Review log's `**Contested:**` section is where pushback lives. Use it. If a round goes by and "Contested" is empty when you genuinely disagreed with something, you failed.

## Inputs

`$ARGUMENTS` may contain, in any order:
- **A plan path** — e.g. `docs/plans/2026-05-10-foo.md`.
- **`--auto`** — autonomous mode. Revise + re-spawn reviewer without pausing between rounds.
- **`--max=N`** — override the default round cap of **4**. The cap applies in both modes.

If no flag is passed, mode is **pause** (default).

### Resolving the plan path when none is given

When the user does not pass a path, resolve in this order — **do not skip ahead**:

1. **Plan from this conversation.** If you (the planner) wrote or edited a plan file in `docs/plans/` earlier in this same chat, use that path. This is the common case: the user just asked you to plan something, you saved it to `docs/plans/YYYY-MM-DD-<slug>.md` per their global instructions, and now they want to review *that* plan — not whatever else is sitting in the folder. Look back through the conversation for a plan you authored or revised; if there's exactly one, use it. If there are multiple, ask the user which one (don't guess by recency).

2. **Latest in `docs/plans/`.** Only if no plan from this conversation exists, fall back to the most recent file in `docs/plans/` (sorted by name, which is timestamped). Before spawning the reviewer, tell the user which plan you resolved to and confirm it's the right one — the latest file might not be what they meant.

3. **Empty / no `docs/plans/` directory.** Ask the user for a path. Do not invent one.

Always echo the resolved path back to the user at loop start so they can catch a wrong resolution before any rounds run.

## The hard rule

**After 4 rounds without convergence, you MUST stop and ask the human**, regardless of mode. The user explicitly required this. If `--max` is set higher than 4, you still pause at round 4 and ask whether to continue — only proceed past round 4 if the user explicitly says to.

In pause mode this is naturally satisfied (you pause every round). In auto mode, treat round 4 as a forced checkpoint even if no other condition fires.

## Round 0 — planner self-audit (before the first reviewer spawn)

Before spawning round 1 (in **both** modes), run this fast checklist against your own plan and fix what it surfaces. It is a self-check, not a gate — its output is edits to the plan, then round 1 proceeds. It catches the cheap, high-frequency errors that otherwise each cost a full review round (the five most common historical misses):

1. **Refs grounded** — you opened every file / table / column / function / API field the plan cites and confirmed it exists and behaves as claimed.
2. **Reuse verified** — every "reuse / extend / inherit / already-wired existing X" claim is checked by reading X, and you are not reinventing something that already exists.
3. **Write paths idempotent** — every write / mutation / send path names its atomic claim / dedup key and its cron-retry / concurrency behavior.
4. **Internally consistent** — no section of the plan contradicts another.
5. **Falsifiable success** — acceptance criteria are a test that can actually fail.
6. **Owner-gate declared** — if the plan schedules a dated downstream auto-fire (a `schtasks`/cron/`.cmd` drop, a scheduled send, an auto-post) gated on an owner review, it declares a matching `owner_gates:` frontmatter entry so the surfacing gate can nudge before it fires. Run the deterministic check in the project (fail-silent if the script isn't present): `python scripts/owner_gate_check.py --check-plan <this-plan.md>` — a non-zero exit means the plan names a scheduling artifact but declares no `owner_gates` block; resolve it (add the block, or set `owner_gates_na: true` if it genuinely isn't owner-gated). (2026-07: the Dojo Kata Card-3 review gated a Wed auto-drop and nothing surfaced it.)
7. **Scope baseline captured** — write the `## Scope Baseline` section into the plan (see "Scope-delta tracking" below) **before** round 1. Without it there is nothing to diff the loop's revisions against, and drift becomes invisible.

This is fast and round-saving. **Auto mode does NOT skip it.** Do not spawn the reviewer until you've run it and applied the fixes.

## Scope-delta tracking — new/changed functionality (non-negotiable)

The loop's known failure mode is **silent scope drift**: a review round adds functionality nobody asked for, it lands in the plan body under the banner of "the reviewer required it," and it gets built. (Precedent: an RXGH product-listing plan came out of the loop carrying a prescription vs. non-prescription split that was never in the ask.) Defects are already reported every round. **Additions are not — this section fixes that.**

### A. Scope Baseline (written at Round 0, then frozen)

Before round 1, add this section to the plan, immediately below the plan's goal/overview:

```markdown
## Scope Baseline
_Frozen at Round 0 — the functionality committed before any review round. Do not edit after round 1; changes are tracked in "New & Changed Functionality" instead._

**In scope (functionality this plan commits to):**
- <one line per user-visible capability / behavior / surface the plan delivers>

**Explicitly out of scope:**
- <anything deliberately excluded — say it, so a later round can't quietly re-include it>
```

Derive "in scope" from the plan as it stands *and* from what the human actually asked for. If the plan already exceeds the ask at Round 0, that is drift too — flag it before round 1 rather than laundering it through the loop.

If the plan already has a frozen `## Scope Baseline` (a resumed loop), do not rewrite it.

### B. Per-round classification (every round, both modes)

When you apply a round's revisions, classify **each** change against the Scope Baseline:

| Class | Meaning |
|---|---|
| `FIX` | Corrects a defect in already-committed functionality. Adds no capability. **Not drift.** |
| `NEW` | Adds a capability, surface, field, mode, or branch not in the Baseline. **Drift.** |
| `CHANGED` | Alters committed behavior, a contract, or a user-visible outcome. **Drift.** |
| `CUT` | Removes or defers something the Baseline committed to. **Drift.** |

**Noise floor — these are NOT deltas**, and logging them buries the real ones: wording/formatting edits, added evidence or `path:line` citations, tightened acceptance criteria for already-committed behavior, added tests, added rollback/observability for committed behavior, filling in an implementation detail the Baseline already implied.

**When in doubt, classify as drift.** A false `NEW` costs one line of review; a missed one ships a feature nobody approved.

Each round's `## Review log` entry carries a `**Functionality delta:**` block (format in step 5). Every drift row names its **origin** — `reviewer:<issue title>`, `planner`, or `human` — because reviewer-originated additions are the highest-risk class: they arrive wearing the authority of a defect report. A reviewer issue tagged `SCOPE-ADD` in its review is a *proposal*, not a defect; you may decline it and record that under **Contested**.

### C. Consolidated section (refreshed at loop end)

At loop end — on **every** terminal verdict, `APPROVED` included — write or refresh this section, placed immediately **above** `## Review log`:

```markdown
## New & Changed Functionality
_What this plan gained, lost, or altered across N review rounds, vs. the Scope Baseline._

| # | Item | Class | Origin | Round | Justification | Status |
|---|------|-------|--------|-------|---------------|--------|
| 1 | <capability in one line> | NEW | reviewer:<issue> | 2 | <why it was added> | PENDING |

**Fixes (no scope change):** <count> — <one line summarising them; do not table them individually>
```

`Status` is `PENDING` (awaiting the human's keep/cut), `KEEP` (human approved it into scope), or `CUT` (removed from the plan body). Set the plan frontmatter `scope_delta: none | pending | resolved` to match — `none` when the loop produced zero drift rows.

If there is genuinely no drift, still write the section with the single line `No functionality added, changed, or cut — all revisions were FIX-class.` Silence is indistinguishable from "nobody checked."

### D. The end-of-loop gate

**The loop is not complete while any drift row is `PENDING`.** On the final report:

- Lead with the drift rows — before the verdict summary, before next steps. They are the part a human cannot recover later.
- Ask for an explicit **keep or cut per row**. This is one of the few decisions the loop may not make for the human, in either mode — `--auto` authorises autonomous *revision*, not autonomous *scope expansion*.
- Do not report the plan as approved-and-ready while `scope_delta: pending`. Say "approved, N scope items awaiting your keep/cut."
- On the human's answer: apply CUTs to the plan body in the same turn, flip the surviving rows to `KEEP`, set `scope_delta: resolved`, and say what you removed.

## Per-round flow

For each round (1, 2, 3, ...):

### 1. Spawn the reviewer subagent

Use the Agent tool. Pass the plan path as the prompt argument so the reviewer skill can resolve it. Brief the agent to invoke the `reviewer` skill:

```
Skill({ skill: "reviewer", args: "<absolute-or-repo-relative plan path>" })
```

But you cannot directly invoke another instance's skill. Instead, spawn a general-purpose subagent and instruct it to run the reviewer skill itself. Example prompt:

> "Run the `reviewer` skill against the plan at `<path>`. Produce the full review (Verdict, Issues, Hidden assumptions, Blindspots, Recommended course of action) and write it to `<path with _review suffix>` per the reviewer skill's contract. Report back with: (1) the verdict line verbatim, (2) the path you wrote the review to. Do not edit any other file."

Use `subagent_type: "general-purpose"` so the subagent has access to file write tools (the `reviewer` skill writes the `_review.md` companion file).

### 2. Read the review file

After the subagent returns, read `<plan>_review.md` directly. Don't trust the subagent's summary — read the file the reviewer wrote. The file path follows the reviewer skill's rule: strip the last extension, append `_review`, re-add the extension. So `docs/plans/foo.md` → `docs/plans/foo_review.md`.

### 3. Parse the verdict

Look for the `**Verdict:**` line near the top. It will contain one of:
- `APPROVED`
- `CHANGES REQUIRED`
- `NEEDS CLARIFICATION`

### 4. Branch on verdict

**APPROVED:**
- Loop is done. Append a final entry to the plan's `## Review log` noting the round number and "Approved by reviewer". Refresh the `## New & Changed Functionality` section (section C above) — an APPROVED verdict does **not** exempt the loop from reporting drift; a reviewer approves correctness, not scope. Report to the user with the plan path, round count, and the drift rows first. Stop.

**NEEDS CLARIFICATION:**
- The reviewer is asking the *human*, not you. Stop the loop regardless of mode. Show the user the reviewer's questions verbatim and wait for their answers. Do not attempt to answer the questions yourself — the reviewer already determined they require human input.

**CHANGES REQUIRED:**
- Read the full review (Issues, Hidden assumptions, Blindspots, Recommended course of action).
- For each issue, decide: do you agree, partially agree, or disagree? Be honest. The reviewer is not always right.
- Draft your revisions to the plan body. For points you accept, update the plan. For points you contest, leave the plan unchanged on that point but record your reasoning in the Review log.
- Now check the round number against the cap (see "Stopping conditions" below) before proceeding to step 5.

### 5. Apply revisions (or pause first)

**Pause mode (default):**
- Show the user a concise summary: reviewer's verdict, the issues raised, which you intend to accept, which you intend to push back on, and your proposed plan edits.
- Wait for user approval before writing anything to disk. The user may amend your interpretation, add new constraints, or tell you to skip a round.
- Once approved, edit the plan file in place per the global plan-revision rules (overwrite, never create a `-v2` file).

**Auto mode (`--auto`):**
- Edit the plan file in place immediately. No user prompt.
- BUT: if this completes round 4 (or `--max` if lower), stop after the edits and surface to the user before spawning round 5. See "Stopping conditions".

In **both** modes, every round appends a structured entry to the plan's `## Review log` section at the bottom of the plan file. Format:

```markdown
## Review log

### Round N — <YYYY-MM-DD>

**Reviewer verdict:** CHANGES REQUIRED

**Reviewer summary:**
- <one-line per issue the reviewer raised>

**Accepted:**
- <issue title> — <one line on what changed in the plan body>

**Contested:**
- <issue title> — <reasoning for pushing back; reviewer should reconsider in the next round>

**Functionality delta:**
- `NEW` <capability> — origin: reviewer:<issue title> — <why>
- `CHANGED` <committed behavior → new behavior> — origin: planner — <why>
- `CUT` <dropped capability> — origin: <origin> — <why>
- `FIX` ×N — <one line covering all defect-only corrections; do not itemise>
_(or: `none beyond FIX` when the round added, altered, and cut nothing.)_

**Plan body changes:** <one-line description of the diff to the plan body, or "none — only contested points">
```

Create the `## Review log` section if it doesn't exist yet (place it at the very bottom of the plan file).

### 6. Loop or stop

If verdict was `CHANGES REQUIRED` and no stopping condition is hit, increment the round counter and go back to step 1.

## Stopping conditions

The loop stops when **any** of these is true:
1. **APPROVED** verdict received.
2. **NEEDS CLARIFICATION** verdict received.
3. **Round count reached the cap** (default 4, or `--max=N` if set). Pause and ask the user whether to continue, abandon, or take over manually. Only proceed past the cap if they explicitly say to.
4. **Round 4 reached in auto mode regardless of `--max`** — the hard rule. Even if `--max=10`, you stop at round 4 to give the human a checkpoint.
5. **The reviewer is repeating itself** — if round N's review is substantively the same as round N-1's, the loop is thrashing. Stop and surface this to the user.
6. **The user interrupts** (in pause mode, by saying "stop" / "don't apply" / etc.).

## Output to the user

**At loop start:** one short line — "Starting plan-loop in <pause|auto> mode, max <N> rounds, plan: <path>".

**Per round (pause mode):** show the reviewer's verdict + the structured summary described in step 5, then wait.

**Per round (auto mode):** one line — "Round <N>: <verdict>. <one-line summary of action taken>". Don't dump the full review on every round.

**At loop end:** a final report, **in this order**:
- **New & changed functionality** — every drift row (`NEW` / `CHANGED` / `CUT`) with its origin and round, and an explicit ask for keep-or-cut on each. If there were none, say so in one line: "No functionality added, changed, or cut." Never omit this block.
- Plan path
- Final verdict (and, if drift is pending, "approved — N scope items awaiting your keep/cut", not a bare "approved")
- Round count
- Path to the review file (`<plan>_review.md` — overwritten each round, only the last review survives)
- One-sentence next-step suggestion

## Pushback discipline

You are not a yes-man. The reviewer is a senior architect, not the final authority. When you disagree:
- Say so, in the Review log under "Contested", with concrete reasoning.
- Don't silently capitulate just to converge faster.
- Don't pick fights for sport either — if the reviewer is right, accept cleanly.

Auto mode without honest pushback collapses into the planner agreeing with everything the reviewer says, which defeats the point of having two roles. Stay rigorous.

## What you do NOT do

- Do not edit any file other than the plan file and (transitively, via the subagent) the `_review.md` file.
- Do not write code based on the plan. This skill orchestrates planning, not implementation.
- Do not skip the round-4 human checkpoint.
- Do not claim the loop is complete unless a stopping condition was actually hit.
- Do not let functionality into the plan without a `NEW`/`CHANGED` row — not even when the reviewer demanded it, and not in `--auto`. Autonomous revision is authorised; autonomous scope expansion is not.
- Do not edit the `## Scope Baseline` after round 1. It is the anchor the diff is measured from; editing it to match the revised plan erases the drift it exists to expose.
- Do not invent or guess at the reviewer's verdict — read the file.
