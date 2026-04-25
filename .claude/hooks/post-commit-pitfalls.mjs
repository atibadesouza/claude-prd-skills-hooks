#!/usr/bin/env node
// PostToolUse hook: after a `git commit`, kick off a detached headless
// Claude that scans the last 10 commits and updates the PITFALLS file.
//
// Wiring: triggered by .claude/settings.json `PostToolUse` matcher: "Bash".
// Filters down to actual commits, skips amends/merges/reverts/docs commits,
// and debounces via .claude/.pitfalls-last-run so rapid-fire commits don't
// spawn N background scans.

import { spawn } from 'node:child_process';
import { existsSync, statSync, mkdirSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';

const DEBOUNCE_MS = 30 * 60 * 1000; // 30 minutes

let stdin = '';
process.stdin.on('data', (chunk) => { stdin += chunk; });
process.stdin.on('end', () => {
  try {
    const event = JSON.parse(stdin || '{}');
    const cmd = event?.tool_input?.command || '';

    if (!/\bgit\s+commit\b/.test(cmd)) return;
    if (/--amend\b/.test(cmd)) return;

    const msgMatch =
      cmd.match(/-m\s*"([^"]+)"/) ||
      cmd.match(/-m\s*'([^']+)'/) ||
      cmd.match(/<<\s*'?EOF'?\s*\r?\n([^\r\n]+)/);
    const firstLine = msgMatch ? msgMatch[1] : '';
    if (/^(Merge\b|Revert\b|docs:\s|chore\(docs\))/i.test(firstLine)) return;

    const root = process.env.CLAUDE_PROJECT_DIR || process.cwd();

    const stampPath = join(root, '.claude', '.pitfalls-last-run');
    if (existsSync(stampPath)) {
      const age = Date.now() - statSync(stampPath).mtimeMs;
      if (age < DEBOUNCE_MS) return;
    }
    mkdirSync(dirname(stampPath), { recursive: true });
    writeFileSync(stampPath, new Date().toISOString());

    const hasDocsRef = existsSync(join(root, 'docs', 'reference'));
    const pitfallsRel = hasDocsRef
      ? 'docs/reference/PITFALLS.md'
      : '.claude/PITFALLS.md';

    const prompt = `Update this project's PITFALLS file based on the last 10 commits.

Steps:
1. Run \`git log -10 --oneline\` then \`git log -10 -p --stat\` to inspect recent commits.
2. Identify commits that fix bugs or document a pitfall. Skip pure features, refactors, and docs-only commits.
3. For each, extract the ROOT CAUSE (not the fix). Group by category (Supabase, n8n, React, Deployment, Auth, Build, or whatever fits this project).
4. Update ${pitfallsRel} (create the file and any parent dirs if missing). Each entry: short title, 2-3 sentence root cause, commit hash. Merge with existing entries — never duplicate.
5. Verify CLAUDE.md (root) references ${pitfallsRel}. If it does not, insert a one-line pointer under a "Detailed Reference" / "References" section so future sessions know to read it.

Be terse. Do not ask questions. Do not write a plan. Just edit the files and exit.`;

    const child = spawn('claude', ['-p', prompt], {
      detached: true,
      stdio: 'ignore',
      cwd: root,
      shell: process.platform === 'win32',
    });
    child.unref();

    process.stdout.write(JSON.stringify({
      hookSpecificOutput: {
        hookEventName: 'PostToolUse',
        additionalContext: `PITFALLS_SCAN_LAUNCHED: A background Claude is updating ${pitfallsRel} from the last 10 commits.`,
      },
    }));
  } catch {
    // Silent — never break the user's session.
  }
});
