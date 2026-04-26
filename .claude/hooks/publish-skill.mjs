#!/usr/bin/env node
// Stop hook: at the end of every Claude session, sync any new or modified
// skill folders under ~/.claude/skills/ to the
// atibadesouza/claude-prd-skills-hooks GitHub repo.
//
// Wiring: ~/.claude/settings.json → hooks.Stop → this script.
// All work runs in a detached child process so the user's session never blocks.
// Failures are silent — never break Claude.
//
// Opt-out per skill: drop a `.skipsync` file in the skill's folder.

import { spawn } from 'node:child_process';
import { existsSync, mkdirSync, statSync, writeFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { homedir } from 'node:os';

const REPO = 'atibadesouza/claude-prd-skills-hooks';
const HOME = homedir();
const SKILLS_DIR = join(HOME, '.claude', 'skills');
const CACHE_DIR = join(HOME, '.claude', 'cache', 'claude-prd-skills-hooks');
const STAMP = join(HOME, '.claude', 'cache', '.publish-skill-last-run');
const LOG = join(HOME, '.claude', 'cache', 'publish-skill.log');
const DEBOUNCE_MS = 60 * 1000; // 1 minute — Stop fires often

let stdin = '';
process.stdin.on('data', (c) => { stdin += c; });
process.stdin.on('end', () => {
  try {
    if (!existsSync(SKILLS_DIR)) return;

    // Debounce: Stop fires at every turn end; we only need occasional sync.
    if (existsSync(STAMP)) {
      const age = Date.now() - statSync(STAMP).mtimeMs;
      if (age < DEBOUNCE_MS) return;
    }

    // Quick check: any skill folder mtime newer than the last successful sync?
    const lastSync = existsSync(STAMP) ? statSync(STAMP).mtimeMs : 0;
    const skillDirs = readdirSync(SKILLS_DIR, { withFileTypes: true })
      .filter((d) => d.isDirectory())
      .map((d) => join(SKILLS_DIR, d.name));
    if (skillDirs.length === 0) return;

    const anyChanged = skillDirs.some((dir) => {
      try {
        // Use directory mtime as a fast proxy; a fresh skill or any file
        // change inside should bump the parent's mtime on most filesystems.
        return statSync(dir).mtimeMs > lastSync;
      } catch {
        return false;
      }
    });
    if (!anyChanged && existsSync(STAMP)) return;

    mkdirSync(join(HOME, '.claude', 'cache'), { recursive: true });
    writeFileSync(STAMP, new Date().toISOString());

    // Build a portable shell script that does the actual sync. Detached so
    // the hook returns immediately. All output is appended to the log.
    const script = `
set -e
exec >>"${LOG}" 2>&1
echo "--- $(date -Iseconds) publish-skill run ---"

REPO_DIR="${CACHE_DIR}"
if [ ! -d "$REPO_DIR/.git" ]; then
  mkdir -p "$(dirname "$REPO_DIR")"
  gh repo clone ${REPO} "$REPO_DIR" || git clone "https://github.com/${REPO}.git" "$REPO_DIR"
fi

cd "$REPO_DIR"
git fetch origin main --quiet || true
git checkout main --quiet || git checkout -B main
git reset --hard origin/main --quiet || true

mkdir -p .claude/skills

CHANGED=0
for SRC in "${SKILLS_DIR}"/*/; do
  [ -d "$SRC" ] || continue
  NAME="$(basename "$SRC")"
  if [ -f "$SRC/.skipsync" ]; then
    echo "skip: $NAME (.skipsync present)"
    continue
  fi
  DEST=".claude/skills/$NAME"
  rm -rf "$DEST"
  mkdir -p "$DEST"
  # Copy the skill folder, excluding .skipsync, .DS_Store, and node_modules.
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --delete \\
      --exclude='.skipsync' --exclude='.DS_Store' --exclude='node_modules' \\
      "$SRC" "$DEST/"
  else
    cp -R "$SRC". "$DEST/"
    rm -f "$DEST/.skipsync" "$DEST/.DS_Store" 2>/dev/null || true
    rm -rf "$DEST/node_modules" 2>/dev/null || true
  fi
  echo "synced: $NAME"
  CHANGED=1
done

if [ "$CHANGED" = "0" ]; then
  echo "no skill folders found to sync"
fi

# Stage everything under .claude/skills/ so deletions are picked up too.
git add .claude/skills

if git diff --cached --quiet; then
  echo "no changes to commit"
  exit 0
fi

# Detect skills present in the commit by inspecting staged changes.
SKILL_LIST="$(git diff --cached --name-only | awk -F/ '/^\\.claude\\/skills\\//{print $3}' | sort -u | tr '\\n' ',' | sed 's/,$//')"

git -c user.name='Claude Auto-Publish' -c user.email='noreply@anthropic.com' \\
  commit -m "auto: sync skills (\${SKILL_LIST})

Auto-published from ~/.claude/skills/ by the publish-skill hook.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>" --quiet

git push origin main --quiet
echo "pushed"
`;

    const child = spawn('bash', ['-c', script], {
      detached: true,
      stdio: ['ignore', 'ignore', 'ignore'],
    });
    child.unref();
  } catch {
    // Silent — never break the user's session.
  }
});
