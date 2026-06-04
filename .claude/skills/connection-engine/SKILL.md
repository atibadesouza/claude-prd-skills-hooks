---
name: connection-engine
description: Surface, judge, and learn connections across the Brain — theme-anchored (curated + semantic via pgvector), Theory-of-Constraints-filtered. Use when Atiba asks "what connects to X?", wants reuse/links surfaced across companies/projects/clients/staff/captures, wants to record a verdict on a surfaced connection, or wants the connections digest. Backed by Supabase (athenaai schema) + scripts/connengine.py.
---

# Connection Engine

Surfaces non-obvious connections across everything in the Brain, anchored on **themes** (`themes/*.md`, mirrored to `athenaai.ce_themes` with embeddings) and filtered by the current **binding constraint**. Spec: `docs/plans/2026-06-04-brain-connection-engine-design.md`. Core: `scripts/connengine.py` (reuses `scripts/athena_db.py` for the Supabase Management-API transport).

## ToC gate (do this FIRST — non-negotiable)
Before surfacing or ranking connections, **state the active environment's binding constraint** (read it: `python scripts/connengine.py` → or query `athenaai.ce_constraint_state`). Connections that move the constraint lead; off-constraint ones are demoted/labeled, not hidden. This is the forcing function — never skip it.

## Checklist
1. **State the binding constraint** (ToC gate above).
2. **Run the relevant command** (below).
3. **For surfaced connections:** present top candidates (inline: cap to top 1–3 by score); for each, let Atiba react 👍/👎/"refine: …"; **record the verdict** so the engine learns.
4. **If results look stale or empty:** run `embed-scan` (the markdown↔DB embedding mirror may have drifted) and note any stale count to Atiba.

## Commands
```bash
python scripts/connengine.py doctor            # health check: pgvector, OpenAI embed round-trip, stale count
python scripts/connengine.py sync-themes       # themes/*.md  -> athenaai.ce_themes (run after editing a theme doc)
python scripts/connengine.py embed-scan        # re-embed only drifted rows (text_sha != embedded_sha); OFF the hot path
python scripts/connengine.py ingest-inbox      # read scratchpad/inbox/*.md -> artifacts + themes + triggers + connections
python scripts/connengine.py digest            # constraint (+staleness) · due date-triggers · watched conditions · new connections · cost
python scripts/connengine.py propose <ref>     # surface connections for an artifact ref (direct + semantic + 2-hop)
python scripts/connengine.py verdict <conn_id> <confirmed|rejected|refined|void|tombstone> <actor> "<reason>"
python scripts/connengine.py cost            # OpenAI spend to date: total + by op + by day (per environment)
```

## Captures & time-triggers (Phase 2)
Loose captures live in `scratchpad/inbox/*.md` (front-matter + body; see that folder's README). `ingest-inbox` turns each into a `ce_artifacts` row, attaches explicit (front-matter) + semantic themes, stores its `trigger` in `ce_triggers`, and logs candidate connections. **Date triggers** fire in the `digest` once due; **condition triggers** are listed as "watching" and surface naturally via semantic `propose` (the capture body is embedded). Run `ingest-inbox` after dropping captures (off the hot path), then `digest`.

## Cost tracking (workspace-wide)
Every paid call by **any** tool records to the shared per-environment ledger `<env>.api_usage` via `scripts/usage.py` → `usage.record(source, provider, model, op, tokens_in, tokens_out)`. The engine records its OpenAI embeds (`source='connection-engine'`); **Athena should record its LLM calls the same way** (write to `athenaai.api_usage` via its pooler — see `scripts/sql/connections.sql` for the columns; not yet wired, separate repo). Prices live in `usage.PRICES` (per-token input/output; stored rows keep the cost at call time). `cost` / `python scripts/usage.py` aggregate by source + day. Per-environment by construction → doubles as per-partner billing. Embedding spend is tiny ($0.02/1M tokens); tokens are the real signal until a full-Brain backfill.

## How it works (so you can explain/operate it)
- **Themes are M:N.** An artifact carries many themes (the reuse mechanism); a theme has many artifacts (the cluster). Membership = `ce_artifact_themes` (explicit tag or semantic match).
- **`propose` retrieves three ways:** *direct* (shared theme), *semantic* (pgvector artifact↔artifact similarity, no shared tag, zero hops), *indirect* (bounded 2-hop via a multi-theme hub — lower confidence, a candidate to judge, never asserted; hard 2-hop bound).
- **Learning loop:** verdicts are append-only events (`ce_connection_events`); `read-first` suppresses any connection whose latest verdict is `rejected`/`tombstone` (keyed on the stable connection id = `hash(source,target,coalesce(theme,via))`). A `void` un-rejects; `confirmed` keeps an indirect connection as `kind='indirect'` (provenance) at full confidence. A wrong *semantic theme tag* is killed at source via `ce_artifact_themes.status='rejected'`.
- **Isolation:** one schema per environment (`athenaai` = Atiba's Projects). Zero cross-environment relationships. Other environments (e.g. TrueMD) are the same schema template deployed separately — see the spec.

## Posture
- **Fail-silent.** If creds/extension are absent, commands print a note and exit 0 — never wedge a session.
- **Observability.** Runs log to `ce_engine_runs` (proposed/suppressed/off_constraint/embedded/stale/embed_failed).
- **Embedding is off the SessionStart hot path** — `embed-scan` is manual/backgrounded, never the blocking hook.
- Adding/editing a theme = edit `themes/<slug>.md`, then `sync-themes && embed-scan`. Slugs are immutable once curated (rename via `aliases`).
