#!/usr/bin/env node
// SessionStart hook: at the start of each Claude Code session, check whether
// the Supabase CLI is installed on this machine. If the project uses Supabase
// and the CLI is missing, inject an additionalContext reminder so Claude can
// recommend `npm i -g supabase` (or the platform-appropriate install) BEFORE
// the user hits the wall on `supabase db push`, `supabase functions deploy`,
// or `supabase functions serve`.
//
// Behavior:
// 1. Bails silently unless the project actually uses Supabase. We detect this
//    by looking for a `supabase/` directory at the repo root, OR a dependency
//    on `@supabase/supabase-js` / `@supabase/ssr` in package.json. Pure
//    frontend projects without Supabase get no noise.
// 2. Runs `supabase --version` with a 2-second timeout. If the binary is not
//    on PATH (ENOENT) or returns non-zero, emits the reminder.
// 3. If the CLI is present, exits silently with no output.
//
// This mirrors the Vercel plugin's CLI-install reminder pattern. Costs zero
// tokens when the CLI is installed, costs one short additionalContext
// injection when it is not.

import { spawnSync } from 'node:child_process';
import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

let stdin = '';
process.stdin.on('data', (chunk) => { stdin += chunk; });
process.stdin.on('end', () => {
  try {
    // Strip a leading UTF-8 BOM if present (some shells / pipes inject it).
    const cleaned = stdin.replace(/^﻿/, '').trim() || '{}';
    const event = JSON.parse(cleaned);
    const cwd = event?.cwd || process.cwd();

    if (!projectUsesSupabase(cwd)) return;

    const installed = isSupabaseCliInstalled();
    if (installed) return;

    process.stdout.write(JSON.stringify({
      hookSpecificOutput: {
        hookEventName: 'SessionStart',
        additionalContext:
          'IMPORTANT: The Supabase CLI is not installed on this machine, ' +
          'but this project depends on Supabase. Strongly recommend the user ' +
          'install it before attempting any of: `supabase db push`, ' +
          '`supabase functions serve`, `supabase functions deploy`, ' +
          '`supabase secrets set`, `supabase db reset`. ' +
          'Install commands by platform:\n' +
          '  - macOS / Linux (Homebrew):  brew install supabase/tap/supabase\n' +
          '  - npm (any OS):               npm i -g supabase\n' +
          '  - Windows (Scoop):            scoop bucket add supabase https://github.com/supabase/scoop-bucket.git && scoop install supabase\n' +
          'After install, run `supabase --version` to verify, then `supabase login` ' +
          'with the user\'s Personal Access Token.',
      },
    }));
  } catch {
    // Silent — never break the user's session.
  }
});

function projectUsesSupabase(cwd) {
  // Signal 1: a top-level `supabase/` directory (created by `supabase init`).
  if (existsSync(join(cwd, 'supabase'))) return true;

  // Signal 2: a dependency on @supabase/* in package.json.
  const pkgPath = join(cwd, 'package.json');
  if (existsSync(pkgPath)) {
    try {
      const pkg = JSON.parse(readFileSync(pkgPath, 'utf8'));
      const deps = { ...(pkg.dependencies || {}), ...(pkg.devDependencies || {}) };
      if (Object.keys(deps).some((d) => d.startsWith('@supabase/'))) return true;
    } catch {
      // ignore malformed package.json — fall through
    }
  }

  return false;
}

function isSupabaseCliInstalled() {
  try {
    const result = spawnSync('supabase', ['--version'], {
      encoding: 'utf8',
      timeout: 2000,
      windowsHide: true,
    });
    return result.status === 0;
  } catch {
    return false;
  }
}
