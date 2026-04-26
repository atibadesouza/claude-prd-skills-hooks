---
name: quickpush
description: Stage, commit, and push changes. Auto-generates commit message if none provided.
disable-model-invocation: true
argument-hint: [commit message]
---

Perform a quick commit and push with these steps:

1. Run `git status` (never use -uall) and `git diff --staged` and `git diff` to see all changes.
2. Run `git log --oneline -5` to see recent commit style.
3. If a commit message was provided use it: $ARGUMENTS
   If no message was provided (empty $ARGUMENTS), analyze the changes and generate a concise commit message that follows the repo's existing style. Focus on the "why" not the "what".
4. Stage all relevant changed files by name (prefer specific files over `git add -A` — never stage .env or credential files).
5. Create the commit. Always append this co-author trailer:

   Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

   Use a HEREDOC for the message:
   ```
   git commit -m "$(cat <<'EOF'
   Your message here.

   Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
   EOF
   )"
   ```
6. Push to the current branch with `git push`. If there is no upstream, use `git push -u origin HEAD`.
7. Push Supabase DB changes:
   a. Run `source .env && npx supabase migration list --linked` to check for unpushed migrations (local column has value, remote column is empty).
   b. If there are unpushed migrations, run `source .env && npx supabase db push --linked` (add `--include-all` if prompted).
   c. If push fails due to remote-only migrations, repair them with `npx supabase migration repair --status reverted <version> --linked` then retry.
   d. If push fails because migration was already applied (columns/tables exist), mark it with `npx supabase migration repair --status applied <version> --linked`.
   e. Deploy any modified edge functions: `source .env && SUPABASE_ACCESS_TOKEN=$SUPABASE_ACCESS_TOKEN npx supabase functions deploy <function-name> --project-ref $VITE_SUPABASE_PROJECT_ID`.
8. Report the commit hash, branch name, migration status, and any deployed edge functions when done.
