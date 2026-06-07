---
name: onboard-tenant
description: Stand up a complete, isolated AI-partner instance for a new tenant — capture identity (cold-start capable), provision infra + the tenant's own keys, mirror the machinery, author the Brain, wire comms, activate. Use when Atiba says "onboard <tenant>", "spin up a new tenant/clone", "set up <X> as a tenant". Run from the Atiba Projects (factory) repo.
---

# onboard-tenant

Turns a new tenant from nothing → a live, isolated instance: `{ brain_repo + Supabase schema + platform.tenants row + its own keys + comms path + a slice of shared Athena }`. Spec: `docs/plans/2026-06-07-tenant-onboarding.md` (Part 2). Machinery mirror: `docs/plans/2026-06-07-truemd-machinery-mirror.md` (Part 1). Intake form: `docs/onboarding/intake-template.md`.

**Operating order applies:** Discuss → Plan → Confirm → Act. Identity is **authored with the owners, never copied** from another tenant. Track progress in `platform.tenants.onboarding_state` (pending→intake→provisioned→mirrored→authored→wired→live).

## Capture method D (how identity is captured — cold-start capable)
1. **Ingest** whatever materials exist (Drive/site/docs/recordings) → draft Brain.
2. **AI-interview the gaps** against the intake form, over the tenant's own comms medium.
3. **Owners approve** the assembled draft. Nothing is canon until approved.
4. **Author + embed** from the approved record.
> Warm-start (has a Drive, e.g. TrueMD) → step 1 does most of it. Cold-start (nothing) → skip step 1; the interview carries it.

## Phases (checklist — create a TodoWrite item per phase)
- **-1. Bootstrap (cold-start):** first interview round in a Claude session Atiba drives (medium-independent) — capture name, owners, comms medium — enough to provision the channel.
- **0. Intake:** fill `docs/onboarding/intake-template.md` via D → owner-approved. Set `onboarding_state='intake'`.
- **1. Provision infra:** create Supabase schema; run `scripts/sql/connections.sql` (substitute the schema, validate `^[a-z][a-z0-9_]{2,30}$`); insert `platform.tenants` row; seed `ce_principals`. → `provisioned`.
- **2. Keys:** engine keys → tenant repo `.env`; Athena keys (Anthropic, Whisper-OpenAI) → the secret store (Phase B machinery). Shared (Supabase) reused. Secrets ONLY in gitignored `.env` / the store — never committed/echoed.
- **3. Mirror machinery:** run the Part-1 mirror — create/clone `brain_repo`, **de-Drive its `.git`** (junction to `C:\GitData\<repo>`; adapt `ensure-gitdir.sh`'s `TARGET_POSIX`), copy the **schema-safe set** (engine + usage + athena_db + connections.sql + render_board + adapted ensure-gitdir + audited new-project skill), author `.claude/settings.json` (git-sync hooks only; `CE_SCHEMA` + `BOARD_SCHEMA`), scaffold the hub-spoke + `ONBOARDING-SLOT` manifests. **Materialize machinery is NOT copied here** (Phase C). → `mirrored`.
- **4. Author the Brain:** turn the approved intake into `brain.md` + spokes + `themes/` vocabulary + the ToC constraint → `sync-themes` + `ingest-brain` (embed). → `authored`.
- **5. Wire integrations + comms:** `platform.tenants` (schema/repo/comms/bot_name); GHL/Drive; comms branch (Slack wired / WhatsApp manual-relay / other adapter); Athena per-tenant config (send-gate, provider keys, materialize role, **schema in the dynamic allowlist**). → `wired`.
- **6. Activate + verify:** `connengine doctor` (asserts state); `ingest-brain` backfill; board render (schema-correct); Athena routing test; **application-level isolation test** (the resolved tenant context never targets another schema — NOT a DB-credential guarantee); capture round-trip (manual-relay, or — for adapter tenants — once materialize-per-schema exists). → `live`.

## Gates (stop for these — Tier-1)
- **Vercel deploy** of `athena-realtime` for any Athena-side change (send-gate, keys, allowlist, adapters) — Atiba's gate.
- **Tenant keys / creds** you can't supply — Atiba/the tenant provides.
- **Identity authoring** is interactive — the owners' input, not autonomous.

## Machinery dependencies (must exist for a non-1st-2nd tenant)
- **Dynamic schema allowlist** (Phase C): `dm.ts`/`intents.ts`/`usage.ts` derive allowed schemas from `platform.tenants` (helper `listTenantSchemas()` in `tenants.ts`) — else a new schema is rejected/skipped by the shared Athena app.
- **Per-tenant secret store** (Phase B): for tenant-owned Anthropic/Whisper keys (Slack/adapter tenants only; manual-relay tenants run on shared Athena keys).
- **Materialize-per-schema** (Phase C): for Athena captures to land as tenant Brain files.

## Teardown / un-onboard (the reverse SOP)
Drop the schema; delete the `platform.tenants` row; revoke the materializer role; purge the tenant's secrets from the store; archive the repo. Set `onboarding_state='offboarded'`.

## Non-goals
No L3 self-serve yet; no per-tenant Supabase project (schema isolation stands); no speculative comms adapters; never copy another tenant's principles/voice/content.
