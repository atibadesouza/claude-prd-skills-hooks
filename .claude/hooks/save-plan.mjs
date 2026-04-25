#!/usr/bin/env node
// PostToolUse hook: every time Claude exits plan mode, persist the plan
// as a markdown file under docs/plans/.
//
// Wiring: triggered by .claude/settings.json `PostToolUse` matcher: "ExitPlanMode".
// The plan body is read from tool_input.plan in the hook event JSON.

import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

let stdin = '';
process.stdin.on('data', (chunk) => { stdin += chunk; });
process.stdin.on('end', () => {
  try {
    const event = JSON.parse(stdin || '{}');
    const plan = event?.tool_input?.plan;
    if (!plan || typeof plan !== 'string' || !plan.trim()) return;

    const root = process.env.CLAUDE_PROJECT_DIR || process.cwd();
    const plansDir = join(root, 'docs', 'plans');
    mkdirSync(plansDir, { recursive: true });

    const now = new Date();
    const ts = now.toISOString().replace(/[:.]/g, '-').slice(0, 19);

    const firstLine = plan.split('\n').find((l) => l.trim()) || 'plan';
    const slug = firstLine
      .replace(/^[#\s*\-]+/, '')
      .replace(/[^a-zA-Z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '')
      .toLowerCase()
      .slice(0, 60) || 'plan';

    const filename = `${ts}-${slug}.md`;
    const filePath = join(plansDir, filename);

    if (existsSync(filePath)) return;

    const sessionId = event?.session_id || 'unknown';
    const body = `---
created: ${now.toISOString()}
session_id: ${sessionId}
status: proposed
---

${plan}
`;
    writeFileSync(filePath, body);

    process.stdout.write(JSON.stringify({
      hookSpecificOutput: {
        hookEventName: 'PostToolUse',
        additionalContext: `PLAN_SAVED: docs/plans/${filename}`,
      },
    }));
  } catch {
    // Silent — never break the user's session.
  }
});
