---
name: answering-how-it-works
description: Use when asked how an existing feature works, where something lives, what the process/steps are for a capability, or to explain or walk through existing behavior in a codebase or product.
---

# Answering How-It-Works Questions

## Overview

When someone asks how a feature works, your answer is only as trustworthy as its grounding. The failure to avoid: jumping straight to code, then presenting what you read as established fact — skipping the docs that may already explain it, and skipping any check that the code you read is actually what runs.

**Core principle: ground every claim, in order, and label how each part is grounded. Code that you read is not the same as behavior you verified.**

## The order: docs → code → verify

Work the layers in this sequence, and report what each one yielded — including when a layer turns up nothing.

1. **Docs first.** Search the docs (`docs/`, PRDs, READMEs, architecture notes, CLAUDE.md, memory/notes). State what you found, or say plainly "this isn't documented" — an undocumented feature is itself a finding worth reporting, not a gap to paper over by going quiet.
2. **Code second.** Trace the real implementation: UI entry point → hook/service → backend (RPC/edge function/table). Cite concrete `file:line`.
3. **Verify last, when it matters.** Confirm the code reflects reality: does the route load, does the RPC/table/function actually exist in the target environment, does live data match the claim? Reach for this whenever deploy-drift, "code ≠ deployed," or stale-doc risk is plausible — and always before stating something works in a specific live environment.

## Label provenance — the output contract

Lead with where the feature lives and the step-by-step process. Then make the grounding of every nontrivial claim unmistakable. Each claim is one of:

- **[documented]** — stated in docs/PRD/spec.
- **[from code]** — read from source; *not* confirmed against a running system.
- **[verified]** — confirmed against the running app / live DB / actual environment.

You don't need a literal tag on every sentence, but the reader must never have to guess. At minimum, say up front which layers you did and didn't do — e.g. "This is from reading the code; I have not run it or confirmed these RPCs exist on prod."

End by naming what's unverified and **offer to verify it** (open the page, confirm the RPC/table exists in the target env, check live data).

## When a layer is missing, say so

- No docs? Report it: "Not in any PRD; found only by reading code." (Then consider whether it's worth documenting.)
- Didn't verify? Report it: "Code-read only, not verified live" — don't let confident prose imply otherwise.
- Silently skipping a layer and presenting the result as settled fact is the core mistake this skill exists to prevent.

## Common mistakes

| Mistake | Fix |
|---|---|
| Straight to grep/code, skip docs | Search docs first; report what's there or that there's nothing |
| "This is how it works" from code alone | Label it [from code]; say it's unverified |
| Treating source as ground truth | Source ≠ deployed. Verify before claiming live behavior |
| Going quiet when undocumented | "Undocumented" is a finding — state it |
| Stopping at the answer | Name what's unverified and offer to verify |
