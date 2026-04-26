#!/usr/bin/env node
// PostToolUse hook: after a significant change (commit, migration, deploy),
// inject an additionalContext reminder so Claude pauses to check whether
// any PRD in docs/prd/ needs updating.
//
// This is a NUDGE only — it does not read PRDs, does not edit anything,
// and does not spawn a background Claude. The in-session Claude does the
// thinking once it sees the reminder.

let stdin = '';
process.stdin.on('data', (chunk) => { stdin += chunk; });
process.stdin.on('end', () => {
  try {
    const event = JSON.parse(stdin || '{}');
    const cmd = event?.tool_input?.command || '';

    // Trigger on: git commit, supabase db push, supabase functions deploy,
    // vercel deploy / --prod, npm publish. Add or trim patterns for your project.
    if (!/(git\s+commit|db\s+push|functions\s+deploy|vercel\s+(deploy|--prod)|npm\s+publish)/.test(cmd)) return;

    process.stdout.write(JSON.stringify({
      hookSpecificOutput: {
        hookEventName: 'PostToolUse',
        additionalContext:
          'PRD_MAINTENANCE_REMINDER: A significant change was just made (deploy, migration, or commit). ' +
          'Check if any PRDs in docs/prd/ need updating to reflect this change, or if a new PRD should be ' +
          'created for new functionality areas. Review the affected area and offer to update relevant PRDs. ' +
          'Command: ' + cmd.substring(0, 200),
      },
    }));
  } catch {
    // Silent — never break the user's session.
  }
});
