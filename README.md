# claude-prd-skills-hooks

Drop-in Claude Code template for new projects. Adds two automatic hooks and one slash command:

| Item | Type | What it does |
|---|---|---|
| `post-commit-pitfalls.mjs` | `PostToolUse` hook on `Bash` | After any `git commit`, spawns a detached headless Claude that scans the last 10 commits and updates `docs/reference/PITFALLS.md` (or `.claude/PITFALLS.md`). Also patches root `CLAUDE.md` to add a pointer if missing. Debounced to 30 minutes. |
| `save-plan.mjs` | `PostToolUse` hook on `ExitPlanMode` | Every plan Claude finalizes is written to `docs/plans/<timestamp>-<slug>.md` with frontmatter. |
| `quickpush` | Skill (`/quickpush`) | Stage, auto-write a commit message in repo style, commit, push. Supabase migration + edge function deploy steps included (skip if not relevant). |

## Why this exists

Claude Code only auto-reads `CLAUDE.md` files. Anything else (PITFALLS, plans, ADRs) has to be referenced from `CLAUDE.md` or it won't surface in future sessions. The pitfalls hook handles both: it writes the file and ensures `CLAUDE.md` points at it.

## Install (per-project)

> These are installed at the **project level** — they live in the target repo's `.claude/` dir. They cannot be installed at the user level (`~/.claude/`) by this repo; do that manually if you want them everywhere.

### Bash / WSL / macOS / Linux

```bash
git clone https://github.com/atibadesouza/claude-prd-skills-hooks.git /tmp/cpsh
/tmp/cpsh/install.sh /path/to/your/project
```

### Windows / PowerShell

```powershell
git clone https://github.com/atibadesouza/claude-prd-skills-hooks.git $env:TEMP\cpsh
& "$env:TEMP\cpsh\install.ps1" -Target C:\path\to\your\project
```

### Manual

Copy `.claude/hooks/`, `.claude/skills/`, and `.claude/settings.json` into the target project's `.claude/` dir. If the target already has a `settings.json`, merge the `hooks.PostToolUse` entries by hand.

## How the hooks work

### Pitfalls hook

1. Fires on every `Bash` tool call.
2. Filters to commands containing `git commit`. Skips amends, merges, reverts, and `docs:` commits.
3. Checks `.claude/.pitfalls-last-run` — bails if a scan ran in the last 30 min.
4. Spawns `claude -p "..."` **detached + unref'd** so the parent session is not blocked.
5. The headless Claude reads `git log -10 -p`, extracts root causes, updates the PITFALLS file by category, and patches `CLAUDE.md` if needed.

The headless Claude inherits whatever auth your `claude` CLI uses. No keys are stored in the repo.

### Plan hook

1. Fires on `ExitPlanMode`.
2. Reads `tool_input.plan` from the hook event JSON.
3. Writes `docs/plans/YYYY-MM-DDTHH-MM-SS-<slug>.md` with frontmatter (`created`, `session_id`, `status: proposed`).
4. Will not overwrite existing files (timestamps make collisions unlikely anyway).

## Notes

- Both hooks fail silently. They will never break your Claude session.
- The pitfalls hook spawns a sub-Claude — it costs tokens. The 30-min debounce keeps that cost bounded.
- Quickpush's Supabase steps are no-ops in projects without `supabase/`. Trim them out if you want a leaner skill.
- Hooks expect Node.js to be on PATH (the scripts are `.mjs`, run via `node`).
