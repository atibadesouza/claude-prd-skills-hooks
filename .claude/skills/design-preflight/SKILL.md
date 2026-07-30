---
name: design-preflight
description: Verify a built page or site against the design rules mechanically, before calling it done. Runs the countable checks from outside the build - banned tells, eyebrow ratio, palette family, and browser checks for sideways scroll, long-word overflow, and fake screenshots. Use after building or changing a landing page, marketing site, or portfolio, when asked to check or review a built page, or before shipping design work.
---

You are about to verify design work that something else built. Your job is to run a check the
builder could not run on itself, then report what it found and — just as importantly — what it
did not look at.

**This skill verifies. It does not decide what to build.** `design-taste-frontend` owns the rules
and the design direction. Nothing here adds a rule, and nothing here overrides one. If you find
yourself reasoning about whether a layout is *good*, you are in the wrong skill.

## Why this exists

The pre-flight checklist in `design-taste-frontend` is 62 boxes, and it used to be ticked
entirely by the agent that wrote the code. Self-attestation fails silently: the box gets ticked,
nothing verified it, and the failure surfaces in front of a client. A subset of those boxes is
countable, and a script now checks that subset from outside the build.

The script is the mechanism. This skill is what makes running it a single step instead of a
command someone has to remember.

## Step 1 — run the static check

```bash
python scripts/design_preflight.py <site-root>
```

The script lives in the **Atiba Projects** workspace repo (`scripts/design_preflight.py`).
`<site-root>` is the site's own folder, which is usually a *different* repo — pass an absolute
path.

**Silence means clean.** It prints nothing when there is nothing to say, so an empty result is
the pass signal, not a missing run. Confirm the exit code if you need certainty:

| Exit | Meaning |
|---|---|
| 0 | ran to completion, with or without findings — never blocks |
| 1 | `--strict` was passed and something hard-failed |
| 2 | **nothing was scanned** — bad path, or no page files found. This is an unknown, never a pass. |
| 3 | `--strict` and the gate itself crashed — results unknown |

If you get exit 2, do not report the site as clean. Fix the path and run it again.

Add `--brief=premium-consumer` when the brand brief genuinely is premium-consumer (cookware,
wellness, artisan, luxury, heritage craft, DTC home goods). The palette check is inert without
it, because a static scan cannot infer a brief from code and firing by default would apply a rule
the skill does not make.

## Step 2 — run the browser checks when you can

```bash
python scripts/design_preflight.py <site-root> --rendered
```

This starts the site's own dev server, drives it with the site's own Playwright at 375 / 768 /
1440 with motion forced to `reduce`, and always shuts the server down afterwards. Roughly
20–30 seconds. Overflow is measured with a 1px tolerance, matching what both real sites'
own test suites allow.

Add `--check-fake-screenshots` to also check for div-based fake product UI — a row of small
circles in a panel's top band above a large blank region, with no real image inside:

```bash
python scripts/design_preflight.py <site-root> --rendered --check-fake-screenshots
```

It is **opt-in on purpose.** Against adversarial fixtures it flags 0 of 5 benign dot patterns
(carousel dots, loading spinner, step tracker, rating row, bullet card) and catches 2 of 2 real
fake-chrome panels. That is enough to show it discriminates, and not enough to make it a blocking
default — so it reports as `justify-or-fix` and asks you to confirm by eye.

**If the site's own Playwright config boots a production server** (`npm run start`) and no
production build exists, the gate measures the dev build instead and prints a note saying so.
Layout on a dev build is not always representative. When you see that note, either run
`npm run build` first or say in your report that the measurement was against dev.

It needs `node_modules` present in the site and `npm` on PATH. When it cannot run it says so
explicitly — **`rendered checks (9, 12, 13) NOT RUN — <reason>`**. That line is not noise. If you
see it, the browser checks did not happen, and you must say so in your report rather than letting
the static result stand in for full coverage.

## Step 3 — report what it found, in plain language

Translate. Do not paste raw output at the reader.

- **hard-fail** — the underlying rule has no override. It is a defect. Say what it is and where.
- **justify-or-fix** — the rule carries an explicit override clause. Report it, and either fix it
  or write down the reason it is acceptable here. An unexplained justify-or-fix is an unmade
  decision, not a pass.

Give the file and line. "Four small uppercase labels above headings on the homepage, against a
limit of two" is a report. "check 10 eyebrow-ratio" is not.

## Step 4 — say what was NOT checked

This is the step that keeps the whole thing honest. The script covers roughly ten of the 62
boxes. The rest are human judgement and were **not** verified by anything.

Always name these two explicitly, because they are the ones most easily assumed covered:

- **Eyebrow adjacency.** The script checks the *ratio* (how many labels per page). It does not
  check the *spacing* rule — if one section has an eyebrow, the next two must not. A page can
  pass the mechanical check and still break this.
- **Everything visual.** Hierarchy, spacing rhythm, whether the type scale works, whether the
  photography is any good, whether the copy is true. None of it is checked.

Never let "the gate passed" stand in for "the page is good." The gate's silence means a specific,
small set of countable mistakes is absent. That is all it means.

## Step 5 — point the fix at the block library

When something needs rebuilding, start from
`~/.claude/skills/design-taste-frontend/blocks/` rather than inventing markup again. Each block
carries a props API, a code sketch, mobile collapse rules, motion bands, dark-mode notes, and the
anti-patterns that block specifically falls into.

Blocks are harvested from shipped, gate-clean pages — never invented, and admitted only where two
real sites solved the same job differently. That difference is the evidence of what is structural
and what is brand.

To check the library itself:

```bash
python scripts/design_preflight.py <blocks-dir> --extract-blocks
```

This validates every block against the section 12 contract and scans each block's code sketch for
the same banned tells. It reads the code sketches only, never the prose — otherwise a block could
not name the mistakes it warns about.

## When the script is not available

If `scripts/design_preflight.py` is not on the machine — the skills repo and the workspace repo
are separate, so this genuinely happens — **say so plainly** and fall back to the human checklist
in `design-taste-frontend` section 14.

Do not tick a box marked `[MECHANICAL]` without having run the mechanism. Reporting an unverified
check as verified is the exact failure this skill was built to remove, and it is worse than
having no gate at all, because it manufactures confidence.
