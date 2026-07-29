---
name: verify-it-actually-ran
description: Use before saying a deploy, send, post, schedule, job run, or write succeeded. Turns "the command exited 0" into evidence that the effect actually reached the world. Invoke when you are about to report something as done, shipped, sent, posted, scheduled, or saved.
---

You are about to tell someone something happened. Before you do, prove the *effect* occurred — not that the *attempt* did.

Almost every expensive miss in this class shares one shape: a check that passed while the thing it was checking did not happen. The build was Ready and served nobody. The script exited 0 and sent nothing. The task ran and wrote no file. The reply said "marked done" and the register was untouched.

**The attempt and the effect are different facts. Verify the second one.**

## The rule per class of action

### Deploys — assert the SERVING artifact, never the build status

"Ready" is a build outcome. "Serving" is an alias fact. A platform will happily report `target: production, status: Ready` for a deployment that no user can reach, because the production alias is still pinned to an older one.

Resolve the alias and see which deployment it lands on. Then, if the change must be *in* that deployment, probe a **runtime marker** — a string the live response contains only if your code is really there. Deploy timestamps false-positive on deploy-then-commit; source-line coverage false-positives on `as const`, imports, and type-stripping. A runtime marker survives transpilation or it doesn't.

In this workspace: `python scripts/verify_deploy.py --alias <alias> [--expect-deployment <id>] [--marker-path /x --marker '<string>']`. Exit 0 verified, 1 not serving what you expect, 2 **unverifiable** — and unverifiable is never success.

### Sends — assert the returned message id, never "the script ran"

A send is proven by an identifier the receiving system gave back: a Slack `ts`, a message id, a provider event with status `delivered`. Not a 200. Not "no exception was raised". Not "I called the function".

If the API returned an id, quote it. If it didn't return one, you have not verified a send — say that instead of implying it.

### Scheduled jobs — assert last-run-in-window **and** a side-effect artifact

Exit code 0 means the process ended cleanly. It does not mean the process did its job: a weekly report task returned `0x0` for weeks while never sending anything.

Check both: did it run inside the window it was supposed to, *and* is there a fresh artifact it can only have produced by doing the work — a written log, a posted message, a modified file? Two independent facts, because either alone lies.

### Writes and state changes — assert the row, the file, the diff

"Saved" means a store now contains something it didn't. Read it back, or name the file and line you wrote. Chat text is not memory; the next session sees only what was persisted.

This is the one with the worst history, and the reason is subtle: a turn can do a great deal of real work and still not perform the *one* write it claims. Doing ten things is not evidence you did the eleventh. Tie each claim to its own receipt.

## The structural rule

**A watcher must not share the failure domain of the thing it watches.**

On 2026-07-22 a scheduled drop was missed because the machine was asleep — and the sweep whose job was to detect the miss was on the same machine, so it was asleep too. The watcher died in the same event as the watched, and the failure was found by a human noticing an absent post.

Ask: *what single event takes out both my job and my check?* If there is one, the check is decorative. Move the watcher to a different machine, a different runtime, or a different trigger.

The same logic applies to two actors guarding one side effect: if both read-then-act at the same instant, neither sees the other, and both act.

## Before you report

- [ ] Named the *effect*, not the attempt — an alias resolution, a returned id, a fresh artifact, a row read back.
- [ ] Distinguished **failed** from **unverifiable**. A check that could not reach its subject proves nothing and must never be reported as a pass.
- [ ] Each separate claim has its own receipt. One verified action does not vouch for the others in the same turn.
- [ ] The watcher doesn't share a failure domain with the watched.
- [ ] If you could not verify: **say so plainly.** "I can't confirm that landed" beats a confident false "done" — and per CLAUDE.md, claiming completion you didn't perform is the one hard never-rule.
