---
name: quickpush-branch
description: Commit work on a branch and open a pull request for review — the team-default way to ship. Never pushes main, never deploys.
disable-model-invocation: true
argument-hint: [commit message]
---

Ship the current changes as a **reviewable pull request** — never a direct push to main, never a deploy. (Deploying is a separate, deliberate step: the person who MERGES the PR runs `quickpush-deploy` after merging. Merge ≠ ship.)

1. Run `git status` (never use -uall), `git diff --staged`, and `git diff` to see all changes.
2. Check the current branch with `git branch --show-current`:
   - If on `main` (or `master`): create a working branch first. Derive a short kebab-case name from the change (e.g. `fix-invoice-email`, `add-paid-tab`) and run `git switch -c <branch-name>`.
   - If already on a working branch: stay on it.
   Never commit directly on main.
3. Run `git log --oneline -5` to match the repo's commit style.
4. If a commit message was provided use it: $ARGUMENTS
   If no message was provided, analyze the changes and generate a concise commit message in the repo's existing style. Focus on the "why" not the "what".
5. Stage the relevant changed files **by name** (prefer specific files over `git add -A` — never stage `.env` or credential files).
6. Create the commit. Always append this co-author trailer, using a HEREDOC:
   ```
   git commit -m "$(cat <<'EOF'
   Your message here.

   Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
   EOF
   )"
   ```
7. Push the branch: `git push -u origin HEAD`.
8. Open a pull request:
   - If the `gh` CLI is available and authenticated: `gh pr create --fill` (edit the title/body to describe what the change does and why, and what a reviewer should check).
   - Otherwise: the push output printed a `https://github.com/.../compare/...` link — give the user that link and tell them to open the PR in the browser with a clear title and description.
9. Report: branch name, commit hash, and the PR URL (or compare link). Remind the user: **the PR ships only when a teammate reviews and merges it — and the merger then runs `quickpush-deploy`.** Do NOT push Supabase migrations or deploy edge functions from this skill.
