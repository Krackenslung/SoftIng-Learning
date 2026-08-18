---
title: PRs vs Merge
domain: bridge
section: B2
category: bridge
difficulty: intermediate
danger: medium
tags:
  - bridge
  - git/merging
  - github/pr
commands:
  - git merge
  - git merge --squash
related:
  - "[[Git - Merging]]"
  - "[[GitHub - Pull Requests]]"
  - "[[Git - Workflows]]"
  - "[[Git - Rebase]]"
sources:
  - https://git-scm.com/docs/git-merge
  - https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges
updated: 2026-08-14
---

# PRs vs Merge

> **Git does X. GitHub wraps it as Y.**

## Git's side

`git merge` combines two branches. It is instantaneous, local, and unaccountable
— no record of who approved it, whether tests passed, or why.

## GitHub's side

A **pull request** is a durable object wrapping a *proposed* merge:

| PR component | Git equivalent |
|---|---|
| `head` / `base` branches | Two refs |
| The diff | `git diff base...head` (three-dot) |
| Commits tab | `git log base..head` |
| **Review, approval** | ❌ none |
| **Required checks** | ❌ none |
| **Discussion thread** | ❌ none |
| **Merge button** | `git merge` / `git rebase` / squash |

Note the diff uses **three dots** — changes since divergence, not tip-to-tip.
That's why a PR diff doesn't show unrelated changes made to `main` after you
branched. See [[Git - Searching History]].

## What each merge button really runs

| Button | Roughly equivalent to |
|---|---|
| Create a merge commit | `git merge --no-ff head` |
| Squash and merge | `git merge --squash head` + `git commit` |
| Rebase and merge | `git rebase base head` + fast-forward |

⚠️ **Squash and rebase both rewrite SHAs.** After a squash merge, the commits on
your branch no longer exist on `main` under those hashes. If you keep working on
that branch afterwards, Git can't tell it was merged — you'll get phantom
conflicts. Always delete and re-branch after a squash merge.

## Doing it without GitHub

Nothing stops you:

```bash
git fetch origin pull/123/head:pr-123     # fetch any PR as a local branch
git switch main
git merge --no-ff pr-123
git push origin main
```

GitHub notices the merge and marks the PR merged, provided the commits match.

## Why the PR wrapper matters anyway

The merge is trivial. The *record* is not. A PR is where the reasoning, the
review, and the CI evidence live — and that's the part you can't reconstruct from
the Git history six months later.

---

## Related

- [[Git - Merging]]
- [[GitHub - Pull Requests]]
- [[Git - Workflows]]
- [[Git - Rebase]]

## Sources

- <https://git-scm.com/docs/git-merge>
- <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges>
