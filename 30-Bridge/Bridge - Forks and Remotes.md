---
title: Forks and Remotes
domain: bridge
section: B1
category: bridge
difficulty: intermediate
danger: medium
tags:
  - bridge
  - git/remotes
  - github/platform
commands:
  - git remote add upstream
  - gh repo fork
related:
  - "[[Git - Remotes]]"
  - "[[GitHub - GitHub vs Git]]"
  - "[[Git - Workflows]]"
sources:
  - https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes
  - https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks
updated: 2026-08-14
---

# Forks and Remotes

> **Git does X. GitHub wraps it as Y.**

## Git's side

Git has **remotes**: named URLs pointing at other repositories. That's it. Any
clone can be a remote of any other. There is no hierarchy, no "original", no
"parent".

```bash
git remote -v
git remote add upstream git@github.com:original/repo.git
```

## GitHub's side

A **fork** is a server-side clone that GitHub *remembers the parent of*. That
memory is the entire added value — it's what enables:

- Cross-repo pull requests (`head: you:feature`, `base: original:main`)
- The "N commits behind" indicator and the Sync fork button
- Shared object storage between fork and parent (forks are cheap to create)
- Fork network graphs

Git knows none of this. Clone a fork and run `git remote -v` — you'll see only
`origin`. The parent relationship lives in GitHub's database, not in `.git/`.

## The standard setup

```bash
gh repo fork original/repo --clone
# or manually:
git clone git@github.com:you/repo.git
git remote add upstream git@github.com:original/repo.git
git fetch upstream
git switch -c feature upstream/main
```

Convention: `origin` = your fork (you push here), `upstream` = the original
(you pull from here).

## Staying current

```bash
git fetch upstream
git switch main
git merge --ff-only upstream/main     # or: git rebase upstream/main
git push origin main
gh repo sync                          # the shortcut
```

## ⚠️ Sharp edges

- **Fork PRs get a restricted `GITHUB_TOKEN`** and no access to secrets — this is
  deliberate, and why `pull_request_target` exists and is dangerous.
- **Deleting the parent repo** breaks the fork network; one fork gets promoted.
- **A private repo's forks inherit its visibility** and stay in its network —
  deleting the parent does not orphan them cleanly.
- Commits pushed to a fork are reachable from the parent's object store via
  direct SHA URLs, **even after the fork is deleted**. Never assume a deleted
  fork's commits are private.

That last point is a real security consideration: pushing a secret to a fork of a
public repo exposes it permanently.

---

## Related

- [[Git - Remotes]]
- [[GitHub - GitHub vs Git]]
- [[Git - Workflows]]

## Sources

- <https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes>
- <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks>
