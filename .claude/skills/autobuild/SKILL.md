---
name: autobuild
description: Execute a build plan end-to-end autonomously. First picks the best execution strategy (single agent, subagents, or agent swarm) for the work, then builds. Only stops for genuine roadblocks (tiered). No progress check-ins, no end-of-phase review pauses.
disable-model-invocation: true
argument-hint: [path to plan file, or describe the plan]
---

# Autonomous build run

Execute the following plan **from start to finish in one continuous run**: $ARGUMENTS

If no plan was named above, use the most recently discussed plan in this conversation, or look in `docs/plans/` for the relevant file. If you genuinely cannot find a plan, that is a roadblock — ask which plan to run.

## First: choose the execution strategy

Before building, read the whole plan and decide **how** to execute it — single agent, subagents, or a swarm. This is a decision, not a stop: pick the best fit, record it in the build log under **Assumptions** (with one line of reasoning), and proceed. Do not ask the user which to use.

Pick by the *shape of the work*, not its size alone:

- **Single agent (default)** — steps are interdependent, share state, build on each other, or the plan is small. Sequencing matters more than parallelism, and coordination overhead would exceed the gain. When in doubt, this is the safe default.
- **Subagents — a few, parallel or sequential** — the plan contains **2+ genuinely independent tasks** (no shared files, no ordering dependency between them). Delegate each as its own subagent. Use `superpowers:dispatching-parallel-agents` for independent fan-out, and `superpowers:subagent-driven-development` to drive plan tasks through subagents in this session. If parallel agents would touch the same files, isolate them (worktrees) or run them sequentially.
- **Agent swarm (Workflow orchestration)** — a **large fan-out of many similar, independent units**: per-file migrations, repeated transforms across a codebase, broad audits, or anything where a deterministic orchestrator (loop / pipeline / parallel with a barrier) beats ad-hoc delegation. Use the `Workflow` tool. Reserve this for real scale — dozens of units — where the orchestration cost is clearly repaid.

You may **mix strategies across phases**: e.g. a single agent for the interdependent core, then a swarm for a repetitive migration phase. Choose per phase if the plan's phases differ in shape. Whatever you pick, the autonomy rules below still apply — subagents and swarm runs do **not** pause for check-ins either.

## Operating mode: run to completion

You are running this plan autonomously. The user does NOT want progress check-ins. Specifically:

- **Do not stop to ask "want me to continue?"** Keep going.
- **Do not pause at the end of a phase/step for review.** Move straight to the next one.
- **Do not stop just because you've done a lot of work.** Volume is not a reason to halt.
- **This overrides the review-checkpoint behavior of the `superpowers:executing-plans` skill.** If that skill (or any other) tells you to pause for review between phases, do NOT — the user has explicitly opted out of those checkpoints for this run. Use the skill's execution discipline (read the plan, work in order, keep tests green) but skip its human-review pauses.
- Keep a running **build log** as you go (see below) instead of stopping to narrate.

## When you MAY stop — tiered roadblock rules

Continue by default. Only interrupt the user in these cases:

**Tier 1 — Stop and ask immediately (do NOT proceed):**
- An **irreversible or destructive** action is required (deleting data, force-pushing, dropping a DB, overwriting something you didn't create, spending money, sending external communications).
- **Missing access or credentials** that you cannot supply yourself (API keys, login, permissions, a private repo).
- A **fork in the plan with no safe default** — a decision that materially changes the architecture or direction and where guessing wrong would waste significant work.

**Tier 2 — Make a best-guess, log it, and KEEP GOING (do NOT stop):**
- A reversible ambiguity (naming, file layout, a minor library choice, where to put a helper).
- A small gap in the plan you can fill reasonably.
- For each of these: pick the most sensible default, record it in the build log under **Assumptions**, and continue. The user will review these at the end.

**Genuinely stuck (not a preference, an actual blocker):**
- A test/build failure you cannot resolve after a real debugging effort (use `superpowers:systematic-debugging`). Don't stop on the first red — investigate first. Only escalate if you're truly blocked.

If it's not Tier 1 and not genuinely-stuck, **do not stop.**

## Build log

Maintain a log as you execute so the user can review the whole run at the end. Append progress, decisions, and assumptions to `docs/plans/<plan-slug>-buildlog.md` (create it next to the plan). At minimum capture:

- **Done:** each step completed.
- **Assumptions:** every Tier-2 best-guess you made and why.
- **Deviations:** anything you did differently from the plan, and why.
- **Follow-ups:** anything left for the user (manual steps, things that need their credentials, etc.).

## On completion

When the entire plan is done:
1. Run the project's verification (tests / build / lint) and confirm it actually passes — paste the real output, don't assert success without evidence (`superpowers:verification-before-completion`).
2. Give the user a concise summary: what was built, the **Assumptions** list, any **Follow-ups**, and the verification result.

Begin now. Work through the whole plan.
