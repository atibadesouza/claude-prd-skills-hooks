---
name: quickpush-deploy
description: Deploy the merged state of main — Supabase migrations + edge functions. Run by the person who merges a PR, immediately after merging. Merge ≠ ship; this is the ship step.
disable-model-invocation: true
---

Deploy what was just merged. This is the extracted deploy step of `quickpush` — run it **on main, after a PR is merged**, by the person who merged it.

1. Make sure you are on up-to-date main: `git switch main && git pull`. If the pull brings in nothing new and you expected a merge, stop and check the PR actually merged.
2. Push Supabase DB changes:
   a. Run `source .env && npx supabase migration list --linked` to check for unpushed migrations (local column has value, remote column is empty).
   b. If there are unpushed migrations, run `source .env && npx supabase db push --linked` (add `--include-all` if prompted).
   c. If push fails due to remote-only migrations, repair them with `npx supabase migration repair --status reverted <version> --linked` then retry.
   d. If push fails because a migration was already applied (columns/tables exist), mark it with `npx supabase migration repair --status applied <version> --linked`.
3. Deploy any edge functions modified by the merged PR: `source .env && SUPABASE_ACCESS_TOKEN=$SUPABASE_ACCESS_TOKEN npx supabase functions deploy <function-name> --project-ref $VITE_SUPABASE_PROJECT_ID`.
   (Find which functions changed with `git diff --name-only HEAD@{1} HEAD -- supabase/functions/` after the pull, or from the PR's changed-files list.)
4. If there were no migrations and no changed edge functions, say so — for a frontend-only change on a Vercel-connected repo, the merge itself triggered the deploy and this skill has nothing to do.
5. Report: migration status and any deployed edge functions. Never run this on a branch, and never run it to "ship" work that hasn't been merged through a reviewed PR.
