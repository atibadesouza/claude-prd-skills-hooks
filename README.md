# claude-prd-skills-hooks

Drop-in Claude Code template for new projects. Adds three automatic hooks and one slash command:

| Item | Type | What it does |
|---|---|---|
| `prd-reminder.mjs` | `PostToolUse` hook on `Bash` | After any commit / migration / deploy, injects a reminder into Claude's context to check whether `docs/prd/` needs updating. Pure nudge — does not read or edit PRDs itself. |
| `post-commit-pitfalls.mjs` | `PostToolUse` hook on `Bash` | After any `git commit`, spawns a detached headless Claude that scans the last 10 commits and updates `docs/reference/PITFALLS.md` (or `.claude/PITFALLS.md`). Also patches root `CLAUDE.md` to add a pointer if missing. Debounced to 30 minutes. |
| `save-plan.mjs` | `PostToolUse` hook on `ExitPlanMode` | Every plan Claude finalizes is written to `docs/plans/<timestamp>-<slug>.md` with frontmatter. |
| `supabase-cli-check.mjs` | `SessionStart` hook | At session start in any project that uses Supabase (detected via `supabase/` dir or `@supabase/*` in package.json), checks whether the Supabase CLI is on PATH. If missing, injects an `additionalContext` reminder with platform-specific install commands. Silent in non-Supabase projects and when the CLI is already installed. Mirrors the Vercel CLI session-start pattern. |
| `publish-skill.mjs` | `Stop` hook (user-level) | At session end, syncs every folder under `~/.claude/skills/` into this repo and pushes. Detached + debounced. Drop a `.skipsync` file in any skill folder to opt it out. |
| `sound-notify` | `Stop` + `Notification` hooks (user-level, Windows) | Plays a Windows system sound when Claude finishes a turn (Asterisk "ding") or needs your input/permission (Question "bell"). Inline PowerShell, no script file. Distinct sounds so you can tell completion vs. needs-input apart by ear. |
| `quickpush` | Skill (`/quickpush`) | Stage, auto-write a commit message in repo style, commit, push. Supabase migration + edge function deploy steps included (skip if not relevant). |
| `reviewer` | Skill (`/reviewer`) | Senior software architect that reviews another agent's plan. Proves or disproves the plan, surfaces issues, hidden assumptions, wrong patterns, and blindspots; asks clarifying questions; only approves when the plan is genuinely correct. |
| `frontend-design` | Skill (third-party, from [`anthropics/skills`](https://github.com/anthropics/skills)) | Builds distinctive, production-grade frontend interfaces. Triggers on requests to build web components, pages, artifacts, or applications — avoids generic AI aesthetics. |
| `ui-ux-pro-max` | Skill (third-party, from [`nextlevelbuilder/ui-ux-pro-max-skill`](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)) | UI/UX design intelligence: 50+ styles, 161 color palettes, 57 font pairings, 25 chart types across React/Next/Vue/Svelte/SwiftUI/Flutter/Tailwind/shadcn. **Heads-up:** Gen flags this skill High Risk (Snyk: Low; Socket: 0 alerts). Review before running. |
| `pdf` | Skill (third-party, from [`anthropics/skills`](https://github.com/anthropics/skills)) | Read/extract text and tables from PDFs, merge/split, rotate pages, watermark, fill forms, encrypt/decrypt, extract images, OCR scanned PDFs. **Heads-up:** Snyk flags this skill High Risk (Gen: Safe; Socket: 0 alerts) — likely from PDF-parsing dependencies with known CVEs. Review before running. |

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

### PRD reminder hook

1. Fires on every `Bash` tool call.
2. If the command matches `git commit`, `db push`, `functions deploy`, `vercel deploy`, or `npm publish`, emits an `additionalContext` reminder telling Claude to check whether any PRD in `docs/prd/` needs updating.
3. Does NOT read PRDs, does NOT edit anything, does NOT spawn a sub-Claude. The in-session Claude does the thinking once it sees the reminder.

Trim or expand the regex inside `prd-reminder.mjs` to match the deploy/publish commands your project actually uses.

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

### Supabase CLI check hook

1. Fires on every `SessionStart`.
2. Bails silently unless the project actually uses Supabase. Detection:
   - a `supabase/` directory at the repo root, OR
   - a `@supabase/*` dependency in `package.json` (`dependencies` or `devDependencies`).
3. Runs `supabase --version` with a 2-second timeout. If the binary is on PATH and exits 0, the hook exits silently — costs zero tokens.
4. If the CLI is missing or fails, emits a one-shot `additionalContext` reminder with install commands for macOS/Linux (Homebrew), npm (any OS), and Windows (Scoop). Mentions the CLI subcommands the user is most likely to hit first (`db push`, `functions serve`, `functions deploy`, `secrets set`, `db reset`).
5. Pure check + reminder. Does not install anything itself.

This mirrors the Vercel plugin's CLI install reminder so that a Supabase-using project gets the same gentle nudge before the user runs into a `command not found`.

### Skill auto-publish hook (user-level only)

> This hook lives at `~/.claude/hooks/publish-skill.mjs` (a copy is kept in this repo for reference) and is wired in `~/.claude/settings.json` under `hooks.Stop`. It is **not** installed by `install.sh` / `install.ps1` because it pushes to GitHub on your behalf — install it deliberately.

1. Fires on every `Stop` event (end of an assistant turn).
2. Debounced to 1 minute, and only does work when a skill folder's mtime is newer than the last successful sync.
3. Maintains a cached clone at `~/.claude/cache/claude-prd-skills-hooks/`. `git fetch` + hard-reset to `origin/main` before each sync.
4. Copies every directory under `~/.claude/skills/` into `.claude/skills/<name>/`. Drop a `.skipsync` file in any skill folder you don't want published.
5. Stages `.claude/skills/`, commits as `Claude Auto-Publish`, and pushes to `main`. Silent on failure; logs go to `~/.claude/cache/publish-skill.log`.

#### Manual install

```bash
mkdir -p ~/.claude/hooks
curl -fsSL https://raw.githubusercontent.com/atibadesouza/claude-prd-skills-hooks/main/.claude/hooks/publish-skill.mjs \
  -o ~/.claude/hooks/publish-skill.mjs
```

Then merge this into `~/.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "node ~/.claude/hooks/publish-skill.mjs", "timeout": 5 }
        ]
      }
    ]
  }
}
```

Auth is whatever `gh` / `git` already uses on your machine. No tokens are stored in the repo.

### Sound notify hook (user-level only, Windows)

> Inline PowerShell wired in `~/.claude/settings.json` — no script file to install. Plays a Windows system sound on each `Stop` (turn complete) and `Notification` (Claude is waiting on you) event so you can step away from the terminal and still know when to look back.

1. `Stop` fires `[System.Media.SystemSounds]::Asterisk.Play()` — short "ding" indicating the turn finished.
2. `Notification` fires `[System.Media.SystemSounds]::Question.Play()` — distinct "bell" indicating Claude needs input or a permission decision.
3. Both run with `"shell": "powershell"` and `"async": true` so they never block the session. `Play()` itself is non-blocking, and the system sounds respect your Windows sound theme (mute the system to silence them).

Pick a different `.wav` (e.g. `chimes.wav`, `tada.wav`) by swapping the inline command for `(New-Object Media.SoundPlayer 'C:\Windows\Media\chimes.wav').Play()`.

#### Manual install

Merge this into `~/.claude/settings.json` (preserve any existing `Stop`/`Notification` entries — append, don't replace):

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "shell": "powershell",
            "command": "[System.Media.SystemSounds]::Asterisk.Play()",
            "async": true,
            "timeout": 2
          }
        ]
      }
    ],
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "shell": "powershell",
            "command": "[System.Media.SystemSounds]::Question.Play()",
            "async": true,
            "timeout": 2
          }
        ]
      }
    ]
  }
}
```

After saving, open `/hooks` in Claude Code once to force a config reload (the settings watcher may not pick up new hook events mid-session).

## Skills

### `/reviewer`

Senior software architect persona. Pass it a plan path, inline plan text, or nothing (it picks the latest `docs/plans/*.md`). It reads the codebase the plan touches, stress-tests assumptions, surfaces blindspots and wrong patterns, and emits exactly one verdict: **APPROVED**, **CHANGES REQUIRED**, or **NEEDS CLARIFICATION** — with concrete `path:line` evidence. Approval is rare and earned.

### `/quickpush`

Stage + commit (auto-message in repo style if none given) + push. Includes Supabase migration push and edge-function deploy steps that no-op cleanly in projects without `supabase/`.

### `/frontend-design`, `/ui-ux-pro-max`, and `/pdf` (third-party)

Auto-published from `~/.claude/skills/` by the `publish-skill` hook. Originally installed globally with the [`skills`](https://skills.sh) CLI:

```powershell
# Anthropic's frontend-design (Safe / Low Risk)
npx -y skills add anthropics/skills -g --agent claude-code --skill frontend-design -y --copy

# Anthropic's pdf (Snyk flags High Risk — review before use)
npx -y skills add anthropics/skills -g --agent claude-code --skill pdf -y --copy

# nextlevelbuilder's ui-ux-pro-max (Gen flags High Risk — review before use)
npx -y skills add nextlevelbuilder/ui-ux-pro-max-skill -g --agent claude-code --skill ui-ux-pro-max -y --copy
```

Use `--copy` (not symlinks) so the `publish-skill` hook can detect mtime changes and sync them. Drop a `.skipsync` file in either folder to opt it out of auto-publishing.

## Notes

- All hooks fail silently. They will never break your Claude session.
- The pitfalls hook spawns a sub-Claude — it costs tokens. The 30-min debounce keeps that cost bounded.
- The publish-skill hook does network I/O (git push) on each sync. The 1-min debounce + mtime check keep it cheap.
- Quickpush's Supabase steps are no-ops in projects without `supabase/`. Trim them out if you want a leaner skill.
- Hooks expect Node.js to be on PATH (the scripts are `.mjs`, run via `node`).
