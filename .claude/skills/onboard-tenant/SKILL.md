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
- **1. Provision infra:** create Supabase schema; run `scripts/sql/connections.sql`, **`scripts/sql/cards.sql`** (PM board + attach the shared `cards_planning_gate` trigger), and **`scripts/sql/tp-events.sql`** (two-agent role substrate: `tp_correction_events`/`tp_patterns`/`tp_pattern_events`/`tp_tension_events` + attach the `cards_correction_log` trigger), and — for the email-ingest lane — the per-schema **`pending_email_intents` + `inbox_signal_state`** tables (`scripts/sql/2026-07-24-pending-email-intents.up.sql` is hardcoded to `['athenaai','truemdai']`, so for a new schema run the same DDL substituted for `<schema>`) plus the materializer grant (`grant select, update on <schema>.pending_email_intents to <schema>_materializer;`, baked into `athena_materializer_role.sql`) — all substitute the schema, validate `^[a-z][a-z0-9_]{2,30}$`; insert `platform.tenants` row; seed `ce_principals`. → `provisioned`.
- **2. Keys:** engine keys → tenant repo `.env`; Athena keys (Anthropic, Whisper-OpenAI) → the secret store (Phase B machinery). Shared (Supabase) reused. Secrets ONLY in gitignored `.env` / the store — never committed/echoed.
- **3. Mirror machinery:** run the Part-1 mirror — create/clone `brain_repo`, **de-Drive its `.git`** (junction to `C:\GitData\<repo>`; adapt `ensure-gitdir.sh`'s `TARGET_POSIX`), copy the **schema-safe set** (engine + usage + athena_db + connections.sql + cards.sql + tp-events.sql + tp.py + tp_pattern_pass.py + render_board + adapted ensure-gitdir + audited new-project skill + the `.claude/agents/{thinking-partner,project-manager}.md` defs), author `.claude/settings.json` (git-sync hooks only; `CE_SCHEMA` + `BOARD_SCHEMA`), scaffold the hub-spoke + `ONBOARDING-SLOT` manifests. **Materialize machinery is NOT copied here** (Phase C). → `mirrored`.
- **4. Author the Brain:** turn the approved intake into `brain.md` + spokes + `themes/` vocabulary + the ToC constraint → `sync-themes` + `ingest-brain` (embed). → `authored`.
- **5. Wire integrations + comms:** `platform.tenants` (schema/repo/comms/bot_name); GHL/Drive; comms branch (Slack wired / WhatsApp manual-relay / other adapter); Athena per-tenant config (send-gate, provider keys, materialize role, **schema in the dynamic allowlist**). → `wired`.
  - **5b. Email ingest (`athena@<domain>` mailbox — the FULL conversational lane, not a scraper).** A standing step so tenant #N inherits email. **Gate:** the mailbox must EXIST — the owner creates `athena@<domain>` on their host and provides creds (Tier-1, owner-supplied; see Gates). Then, by transport fork:
    - **Google-hosted mailbox** → reuse `gmail.ts` with a per-tenant `tenantGoogleRefreshToken` (`google-tokens`), add the schema to `ATHENA_INBOX_SIGNAL_SCHEMAS`, seed the owner allowlist so inbound routes to the read→detect→stage lane (`inbox-signal`).
    - **Custom-domain mailbox** → reuse `truemd-mail.ts` IMAP/SMTP: put `<TENANT>_MAIL_HOST/USER/PASS` + `_IMAP_PORT/_SMTP_PORT` in the secret store, set the owner allowlist (`<TENANT>_OWNER_EMAILS`), and enable the lane flag. This provisions the clarify→reply→board **conversational** lane (never-drop lease), not a one-way scraper.
    - Register the ingest cron scope + verify one round-trip (an owner email → in-thread reply → board reflects it). Confirm any chat-pasted mailbox password was rotated.
    - **Status (2026-07-26):** this generalizes from ONE proven transport — TrueMD custom-domain IMAP (live, verified sweeping). The Google-mailbox fork is built (`gmail.ts`+`tenantGoogleRefreshToken` exist) but UNPROVEN on a real tenant; OpReady will validate it once its mailbox exists (blocked on the domain). Treat the Google path as designed-not-proven until then.
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
