---
name: fork-session
description: Split the current conversation into self-contained handoff briefs you launch in separate, fresh Claude instances (NOT subagents) for context relief. Classifies the conversation into workstreams, lets you pick which to fork (1 or N), writes each to docs/plans/forks/<date>/<slug>.md, and manages their lifecycle. Subcommands - `list` shows active forks, `clean` archives completed and flags stale (>14d) ones.
argument-hint: [empty to fork | list | clean]
---

You turn the **current conversation** into one or more self-contained handoff briefs that the user
launches in **separate, fresh Claude instances** — real new sessions, not subagents. Subagents return
their output into this context and would defeat the purpose; this skill only writes files and prints
launch instructions.

You operate on the conversation already in your context. You do not need any special tool to "read"
it — reflect on what has been discussed and cluster it.

## Modes

- No argument → **fork flow** (classify → select → write briefs → report).
- `list` → list active forks with status and age.
- `clean` → archive completed forks and flag stale ones.

Dispatch on `$ARGUMENTS`: if it contains `list`, run List mode; if `clean`, run Clean mode;
otherwise run Fork mode.

Note: deliberately **no** `disable-model-invocation` flag — this is a user-triggered utility, so it
must stay model-invocable as `/fork-session` (matching `plan-loop`, unlike `reviewer` which disables
it). Omitting the flag is the correct choice; do not add it.

---

## Fork mode

### 1. Classify

Read back over the entire current conversation. Cluster it into **distinct, separable workstreams** —
threads of work that could each continue independently in their own session. For each workstream
produce:

- a short **title**,
- a **one-line summary** of what it covers,
- its rough **state** (e.g. "spec drafted", "half-implemented", "blocked on X").

Rules:
- If there are **no** forkable workstreams (trivial, empty, or purely conversational session), say so
  plainly and stop. Do not invent work.
- If there is exactly **one** coherent workstream, present it and offer to fork just that one.
- Keep clusters genuinely separable. Do not split one tightly-coupled task into fake sub-forks.

### 2. Select

Pick the presentation by workstream count (the `AskUserQuestion` tool caps a single question at
**4 options**, so it cannot list more than 4 at once):

- **1 workstream:** just confirm "Fork this one topic?" — no multi-select needed.
- **2–4 workstreams:** one `AskUserQuestion` with `multiSelect: true`, one option per workstream.
  Label = the title (keep it short; option labels truncate), description = one-line summary + state.
- **5+ workstreams:** do NOT try to cram them into `AskUserQuestion`. Print a numbered plain-text
  list (number · title · one-line summary · state) and ask the user to reply with the numbers they
  want to fork (e.g. "1,3,4"). Parse the reply leniently (commas/spaces/ranges); if any number is
  out of range or the reply is unparseable, show what you understood, list the valid options again,
  and re-ask rather than guessing.

In all cases, if the user selects none, stop without writing anything.

### 3. Write briefs

For each **selected** workstream:

1. Derive a kebab-case `<slug>` from the title (short, ≤ 5 words).
2. Determine today's date as `<YYYY-MM-DD>` by reading the real clock once:
   PowerShell `Get-Date -Format yyyy-MM-dd` (this is a win32 environment). Reuse the value for all
   briefs in this run; do not rely on a possibly-stale in-context date.
3. Target path: `docs/plans/forks/<YYYY-MM-DD>/<slug>.md`. Resolve collisions against **both** the
   active path and the archive path `docs/plans/forks/_archive/<YYYY-MM-DD>/<slug>.md`: if either
   exists, append `-2`, `-3`, … until the slug is free in both trees. (Checking the archive too
   prevents a later `clean` from colliding with an already-archived brief of the same date+slug.)
4. Write the file using this exact template, populated from the conversation:

```markdown
---
name: <slug>
status: active
created: <YYYY-MM-DD>
forked-from: <one-line description of this originating session>
---

## Goal
<the objective, stated so a session with zero prior context understands it>

## Background
<the relevant slice of decisions and context already made here — enough to continue without this chat>

## Relevant files
<paths and artifacts the new session should look at; "none yet" if greenfield>

## Constraints
<invariants, user preferences, things not to break>

## Next steps
<concrete, ordered actions to pick the work back up>

## Completion protocol
When this work is finished:
1. Set `status: done` in the frontmatter above.
2. Move this file to `docs/plans/forks/_archive/<YYYY-MM-DD>/<slug>.md`
   (same date, under `_archive/`).
This keeps the active forks folder showing only live work.
```

The brief must stand alone — assume the launching session has **none** of this conversation. Pull in
the actual decisions, paths, and constraints; do not write "see previous discussion".

If there is no project root / no obvious place for `docs/`, ask the user where to write the briefs
(mirroring the global plan-saving rule) rather than guessing.

### 4. Report

After writing all briefs, output:

- For each brief, its path and a ready-to-paste launch instruction that also carries the completion
  protocol so the new session knows to self-archive:
  > Open a new terminal → run `claude` → say:
  > *"Read `docs/plans/forks/<date>/<slug>.md` and continue. When the work is done, follow the
  > brief's Completion protocol (set status: done and move it under `_archive/`)."*
- A caution: **review each brief for completeness before you `/clear`.** Once this session is
  cleared, the brief is the only surviving record — there is no lossy summary to fall back on.
- A closing line: this session can now be `/clear`'d to reclaim context if you're done with the
  remaining topics here.

Do **not** run `/clear` yourself (you cannot) and do **not** delete or modify any other files.

---

## List mode

1. Read today's date once: PowerShell `Get-Date -Format yyyy-MM-dd`.
2. Find active briefs: glob `docs/plans/forks/**/*.md` but **exclude** any path under
   `docs/plans/forks/_archive/`. (The glob is deliberately scoped to `forks/**`, not all of
   `docs/plans/` — the user's global plan rule writes ordinary plans one level up in `docs/plans/`,
   and those are not forks. Do not broaden this glob.)
3. If none (or the directory does not exist), report "No active forks." and stop.
4. For each, read the frontmatter `status` and `created` date. If the frontmatter is missing or
   malformed, treat the brief as `status: active` with unknown age (never crash the loop) and note
   it as "(unparseable frontmatter)". Otherwise compute age in days from `created` to today.
5. Print a table: path · status · age (days). Mark any with age > 14 as **STALE**.

This mode is read-only — never move or delete files.

---

## Clean mode

Self-archiving via each brief's Completion protocol is **best-effort** — a fresh session may never
re-read the brief to honor it. So in practice this `clean` mode is the de-facto primary lifecycle
mechanism, not a rarely-used backstop. Treat it as the reliable path.

1. Read today's date once: PowerShell `Get-Date -Format yyyy-MM-dd`.
2. Glob active briefs (exclude `_archive/`, as in List mode). If a brief's frontmatter is missing or
   malformed, treat it as `active`/unknown age and skip the archive step for it (never crash); note
   it in the summary.
3. **Archive done:** for each brief whose frontmatter `status` is `done`, move it from
   `docs/plans/forks/<date>/<slug>.md` to `docs/plans/forks/_archive/<date>/<slug>.md` using
   PowerShell `Move-Item` (create the archive date folder first with `New-Item -ItemType Directory
   -Force`). If the destination already exists, suffix the archived name `-2`, `-3`, … until free
   (mirrors the create-side collision rule, so no archived brief is overwritten). Report each move.
4. **Flag stale:** for each remaining `active` brief with age > 14 days, list it as a stale
   candidate. **Do not delete it.** Tell the user they can delete it manually if it is no longer
   needed.
5. Summary: N archived, M flagged stale, plus any unparseable briefs noted.

Never auto-delete. Archiving only ever moves; deletion is always a manual user action.
