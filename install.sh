#!/usr/bin/env bash
# Install Claude PRD/skills/hooks template into a target project's .claude/ dir.
# Usage:
#   ./install.sh                # installs into the current directory
#   ./install.sh /path/to/repo  # installs into the given repo

set -euo pipefail

TARGET="${1:-$PWD}"
SRC="$(cd "$(dirname "$0")" && pwd)"

if [ ! -d "$TARGET" ]; then
  echo "ERROR: target directory does not exist: $TARGET" >&2
  exit 1
fi

mkdir -p "$TARGET/.claude/hooks"
mkdir -p "$TARGET/.claude/skills"

cp "$SRC/.claude/hooks/prd-reminder.mjs"         "$TARGET/.claude/hooks/"
cp "$SRC/.claude/hooks/post-commit-pitfalls.mjs" "$TARGET/.claude/hooks/"
cp "$SRC/.claude/hooks/save-plan.mjs"            "$TARGET/.claude/hooks/"

cp -r "$SRC/.claude/skills/quickpush" "$TARGET/.claude/skills/"

SETTINGS="$TARGET/.claude/settings.json"
if [ -f "$SETTINGS" ]; then
  echo "NOTE: $SETTINGS already exists — not overwriting."
  echo "      Merge the PostToolUse entries from $SRC/.claude/settings.json manually."
else
  cp "$SRC/.claude/settings.json" "$SETTINGS"
fi

mkdir -p "$TARGET/docs/plans"

echo "Installed Claude hooks + quickpush skill into $TARGET/.claude/"
echo "Hooks installed:"
echo "  - prd-reminder.mjs          (PostToolUse / Bash → reminds to update PRDs)"
echo "  - post-commit-pitfalls.mjs  (PostToolUse / Bash → updates PITFALLS.md)"
echo "  - save-plan.mjs             (PostToolUse / ExitPlanMode → docs/plans/*.md)"
echo "Skill installed: quickpush"
