---
name: repo-status
description: Use when asked how many uncommitted changes, branches, unpushed/unmerged branches, or open PRs the current repo has — or any "what's the git state / what's outstanding / what's not pushed / do we have open PRs" question for the repo you're in.
argument-hint: (no args — operates on the current repo)
---

Report the full git state of the **current repository** — uncommitted changes, branches, unpushed commits, and open PRs — as a single scannable summary. Read-only: do NOT commit, push, or modify anything.

Run these in the repo root (use the working directory the user is in):

1. **Uncommitted changes** — `git status --short`. Count modified/staged/untracked entries.
2. **Local branches + tracking** — `git branch -vv`. Note the current branch and how many local branches exist.
3. **Remote branches** — `git branch -r`.
4. **Unpushed work** — `git log --branches --not --remotes --oneline`. Any output = commits that exist locally but not on any remote (per branch). Empty = everything is pushed.
5. **Unmerged branches** — `git branch --no-merged main` (swap `main` for the repo's default branch if different). Lists branches with work not yet folded into the mainline.
6. **Open PRs** — `gh pr list --state open`. If `gh` is missing or not authenticated, say so explicitly and report PRs as "unknown" rather than "0".

Then present a **summary table** with counts for: uncommitted changes (files), unpushed branches/commits, unmerged branches, and open PRs. List the specific files/branches/PRs underneath when the count is small (≤ ~10); otherwise give counts only.

Close with a one-line bottom line (e.g. "everything pushed, nothing outstanding" or "3 uncommitted plan docs, no open PRs"). If this repo auto-syncs on session end (check for a `.git-sync.log` or SessionEnd hook), note that loose uncommitted work will be swept up automatically, and offer to commit/push now.

**Never claim "0 open PRs" if `gh` failed** — distinguish "verified none" from "couldn't check."
