---
name: gate-authoring
description: Use when writing or modifying any automated check — a git/session hook, watcher, validator, linter, nudge, scheduled job, drift detector, or CI gate. Enforces the checklist that stops a gate from crying wolf, going silently blind, corrupting the tree it guards, or dying on re-clone. Invoke BEFORE writing the gate, not after.
---

You are about to write a mechanism that watches something and speaks up when it's wrong. Gates are high-leverage and quietly dangerous: a gate that fires falsely gets ignored within a week, and an ignored gate is worse than no gate — it consumes attention and certifies safety it isn't providing.

Work the eight rules below in order. Each exists because a real gate failed in exactly that way.

## The checklist

### 1. Measure the noise floor on the live corpus before wiring it in

Run the check against the real data **before** it is installed anywhere. Count the lines it emits. Open them and confirm each one is a true finding. Record the number.

If the floor isn't zero (or a small, enumerated, understood set), the gate is not ready. Do not install it and plan to "tune it later" — nobody tunes it later; they mute it.

> *Origin: a session-start validator shipped without a live-corpus count and emitted 37 false lines on its first run. It was backed out the same day.*

### 2. Existence oracle before declaring absence

Only report "missing", "orphaned", "dangling", or "unknown" against an oracle that could actually **see** the thing if it were there.

A scanner that enumerates a narrow universe (say, `lib/*.ts` and `scripts/*.py`) and then flags anything outside it as missing is not detecting absence — it's reporting the edge of its own vision. Before emitting a negative finding, ask: *what is the widest source of truth for this thing, and did I check that one?* For files, that's the filesystem (`os.path.exists`, a glob, a directory test). For people, the roster. For scheduled jobs, the scheduler's own report.

Two-step it: `elif not real_existence_oracle(x): flag(x)`. A thing outside the narrow universe but present in reality is neither claimed nor missing — it's simply not this scanner's business.

**Absence in a tool's output is not absence in reality.**

> *Origin: a catalog scanner flagged three real, tracked, on-disk files as dangling because they weren't the file types it enumerated — the "cosmetic fix" of deleting those references would have destroyed correct documentation. Separately, a generated roster silently listed most of the staff as unknown because the generator's input was truncated.*

### 3. No open-ended text ranges, no unquoted expansions

Parsing tool output is where gates corrupt the thing they guard.

- **Never** a `sed` range that has no guaranteed terminator (`/^START/,/^END/p` where `END` may not appear — it swallows the rest of the file). Use a section-scoped `awk` state machine that toggles **off at the next header of any kind**, or parse in a real language.
- **Never** two ranges over the same start marker. The second one re-reads and merges sections that were meant to stay separate.
- **Never** `for f in $VAR`. Unquoted expansion word-splits prose into garbage tokens. Use `while IFS= read -r line`.
- Any string that may contain `&`, `$`, `%`, quotes, backticks, or spaces gets **a script file**, not an inline one-liner. Shells and command-line parsers eat these silently and the truncation looks like a legitimate short value.
- **Keep `.ps1` files pure ASCII.** PowerShell reads a BOM-less UTF-8 script as cp1252, so an em-dash (`—` = `E2 80 94`) decodes to bytes including `0x94` — a Unicode right-double-quote, which PowerShell honours as a *string delimiter*. One em-dash in a comment closes a string early and produces a cascade of "missing closing `}`" errors pointing dozens of lines away from the real cause. Same trap for smart quotes and arrows. Write `-`, `->`, `"`.

> *Origin: an open-ended range plus an unquoted `for` loop turned a hook's prose output into 14 junk artifacts, each of which the next run then read as input — a self-feeding corruption loop.*

### 4. Fail-silent on the happy path, loud on the finding

- Clean state emits **nothing**. A gate that prints "✅ all good" on every run trains people to skim past the one run that doesn't.
- The gate must **never wedge** the thing it hooks into. Wrap it so a crash, a missing dependency, or a slow network degrades to silence, not to a blocked session/commit/deploy. Exit `0` unless blocking is the deliberate, documented point of the gate.
- **Know which stream you're writing to.** If the harness discards `stderr` (or the hook is invoked with `2>/dev/null`), a diagnostic printed to `stderr` is a gate that looks wired and does nothing. Check the actual invocation, then match it.
- Budget the runtime. A session-start gate above a few hundred milliseconds gets noticed and eventually removed. If a validator is slow because of a per-item subprocess, return **before** the expensive stage when running in nudge mode.

### 5. Tracked source + install step

A gate that lives only in `.git/hooks/`, only in a scheduler's registry, or only in one machine's config **does not exist**. It dies at the next clone, re-image, or machine change, and its absence is silent.

Every gate needs: a tracked source file in the repo, an install/registration step that is itself scripted and tracked, and a single writer. Two scripts registering the same job is a merge conflict with no merge tool.

### 6. A test file, including a live-corpus zero-noise regression

Tests must include both directions:
- **Positive** — a synthetic broken input the gate must catch.
- **Negative** — the **real, current corpus**, asserting zero output. This is the regression that stops a future "improvement" from reintroducing the noise floor from rule 1.

If the gate silences something that used to be flagged, prove the silencing is *accuracy*, not suppression: the fabricated-missing case must still flag.

### 7. Self-check the check

Before reporting a gate's output as fact — in a plan, in a commit message, to a human — confirm the oracle isn't producing false positives. Take the two or three most alarming rows and verify them independently, by a different method than the gate used.

A gate's output is a hypothesis about reality. Publishing it unverified is how a false alarm becomes a "finding" and then a root cause in a document.

> *Origin: a scheduled-task sweep reported six executables as missing by testing each raw command string as a path. Those strings carried embedded quotes, which the scheduler handles correctly; all six had in fact last exited `0`. The correct oracle was the scheduler's own last-result code.*

### 8. Two guards on one side effect need a shared lock or a deliberate time offset

When **two independent actors** can produce the same side effect (a cloud cron and a local fallback; two workers; a retry and its original), read-then-act guards do **not** deduplicate them.

If both actors read shared state, see nothing, and then both act, both guards pass and the effect happens twice. This is guaranteed — not unlikely — when the two are scheduled at the **same instant**, which is easy to do accidentally when they're expressed in different timezones and nobody converts them.

You need one of:
- **A shared atomic claim** both actors write to (a unique-indexed `(job_key, period_key)` row, a lock, a compare-and-set) — and *both* actors must actually touch it. A claim only one participant writes protects nothing.
- **A deliberate time offset**, with the fallback running late enough that its read genuinely observes the primary's effect.

Convert every schedule to a single timezone (UTC) and compare the actual instants before asserting that a fallback is deduped. And note: a "prove they can't double-fire" task dated the same day as the fire is an *observation*, not a gate.

> *Origin: a cloud cron at `0 1 * * 3` (Wed 01:00 UTC) and its local fallback at Tue 18:00 PDT were the same instant. Both had channel-history guards; neither could have seen the other's post. Caught three days early by converting both to UTC.*

## When you move content out into a reference file, leave a stub that makes the load necessary

Skills and gates grow, and the fix is usually to move the detail into a reference file. That move
quietly breaks things, because what gets left behind is a pointer — *"see `references/foo.md` for
the details"* — and an agent that believes it already knows the details will skip it. The load
becomes advisory, and the reference stops being read at exactly the moment it starts mattering.

**The stub names two things and withholds a third:**

1. **What the reference contains** — enough to know whether it is relevant now.
2. **What breaks if you skip it** — the concrete failure, not "for more detail".
3. **No detail an agent could improvise from.** This is the part that does the work. If the stub
   summarises the rules, a confident agent reconstructs them from the summary and never opens the
   file — and reconstructs them slightly wrong, which is worse than not having them.

> **Weak:** "See `references/adjudication.md` for how to handle flagged findings."
> **Strong:** "Read `references/adjudication.md` before judging a single flag. It holds the rule for
> which flags are questions and which are failures — getting that backwards means auto-fixing a
> finding that was correct, and the fix is silent. Nothing here summarises it: the file is the only
> copy."

The test: **could someone act plausibly without opening the file?** If yes, the stub is too
generous. A load-bearing reference deserves a stub that makes skipping it obviously reckless.

## Before you finish

Confirm, explicitly:

- [ ] Noise floor measured on the live corpus, counted, inspected, **recorded in the plan**.
- [ ] Every negative finding backed by a real existence oracle.
- [ ] No open-ended ranges, no unquoted expansions; hostile strings in a script file.
- [ ] Silent when clean; can't wedge its host; writing to a stream the host actually reads; runtime budgeted.
- [ ] Source tracked, install scripted, exactly one writer.
- [ ] Tests cover synthetic-broken **and** live-corpus-zero.
- [ ] Alarming rows independently re-verified before being reported as fact.
- [ ] If a second actor can cause the same effect: shared atomic claim, or a real time offset proven in UTC.
- [ ] Any reference file this splits out has a stub naming what it holds and what breaks without it — and summarising none of it.

## Related

- The **`reviewer`** skill hard-checks that a plan introducing a gate cites its **measured noise floor** (§4). Writing the number down at authoring time is what makes that check passable.
- Prefer a gate to a promise. A behavior that must reliably happen should be enforced by a mechanism, not by remembering — trusted discipline fails silently, gates fail loudly. Where a gate is genuinely infeasible, **say so explicitly** and name the residual risk rather than implying coverage.
