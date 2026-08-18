---
title: Stash & Worktrees
domain: git
section: 19
category: advanced
difficulty: intermediate
danger: medium
tags:
  - git/advanced
commands:
  - git stash
  - git worktree
related:
  - "[[Git - Branching]]"
  - "[[Git - The Core Loop]]"
sources:
  - https://git-scm.com/docs/git-stash
  - https://git-scm.com/docs/git-worktree
  - https://git-scm.com/book/en/v2/Git-Tools-Stashing-and-Cleaning
updated: 2026-08-14
---

# Stash & Worktrees


## `git stash`

Park uncommitted work without committing it.

```bash
git stash                              # stash tracked modifications
git stash push -m "WIP: login form"    # with a message
git stash -u                           # include UNTRACKED files
git stash -a                           # include ignored files too
git stash push -- path/to/file         # stash only certain paths
git stash -p                           # interactively choose hunks

git stash list                         # stash@{0}, stash@{1}, ...
git stash show                         # summary of the latest
git stash show -p stash@{1}            # full patch

git stash apply                        # restore, KEEP in stash list
git stash pop                          # restore and DROP from list
git stash apply stash@{2}
git stash branch new-branch stash@{0}  # create a branch from a stash

git stash drop stash@{1}
git stash clear                        # ⚠️ delete all stashes
```

Stashes are stored as commits under `refs/stash` — recoverable via
`git fsck --unreachable` if dropped by accident, but don't rely on it.

**Caution:** the stash is easy to forget. Anything you'd be sad to lose belongs
in a commit on a branch (even a WIP commit you'll later amend), not in a stash.

## `git worktree`

Check out multiple branches **simultaneously** from one repository, in separate
directories, sharing one object store.

```bash
git worktree add ../hotfix hotfix-branch      # existing branch
git worktree add -b new-feature ../feature    # create branch + worktree
git worktree add --detach ../inspect abc123
git worktree list
git worktree remove ../hotfix
git worktree prune                            # clean up stale entries
git worktree lock ../important
```

**Why it beats stashing:** urgent hotfix while mid-feature? Instead of stashing,
switching, fixing, switching back, popping — just spin up a second worktree. Your
build artifacts, `node_modules`, editor state, and running dev server all stay
intact.

Also good for: running long test suites on one branch while developing on
another; reviewing a PR without disturbing your work; comparing two versions
side by side in an editor.

Constraints: the same branch can't be checked out in two worktrees at once;
worktrees live in `.git/worktrees/`, so deleting the directory without
`git worktree remove` leaves stale metadata (fix with `prune`).

---

## Related

- [[Git - Branching]]
- [[Git - The Core Loop]]

## Sources

- <https://git-scm.com/docs/git-stash>
- <https://git-scm.com/docs/git-worktree>
- <https://git-scm.com/book/en/v2/Git-Tools-Stashing-and-Cleaning>
