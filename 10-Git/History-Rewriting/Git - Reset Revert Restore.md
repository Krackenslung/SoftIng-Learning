---
title: Reset, Revert, Restore
domain: git
section: 10
category: history-rewriting
difficulty: intermediate
danger: high
tags:
  - git/history
  - git/undo
commands:
  - git reset
  - git revert
  - git restore
related:
  - "[[Git - Undo Cookbook]]"
  - "[[Git - Blame Bisect Reflog]]"
  - "[[Git - Rebase]]"
sources:
  - https://git-scm.com/docs/git-reset
  - https://git-scm.com/docs/git-revert
  - https://git-scm.com/docs/git-restore
  - https://git-scm.com/book/en/v2/Git-Tools-Reset-Demystified
  - https://git-scm.com/docs/howto/revert-a-faulty-merge
updated: 2026-08-14
---

# Reset, Revert, Restore


Three commands that all "undo" — but at different levels.

| Command | Operates on | Rewrites history? | Use when |
|---|---|---|---|
| `git restore` | Files | No | Discard changes to files |
| `git reset` | Branch pointer (+ index/tree) | Yes | Undo local commits |
| `git revert` | Creates a new commit | No | Undo a **published** commit |

## `git reset` — three modes

`git reset` moves the current branch pointer, then optionally updates the index
and working directory.

```bash
git reset --soft HEAD~1
# ✅ moves branch pointer   ❌ index unchanged   ❌ working dir unchanged
# → changes stay STAGED. Use to recommit differently.

git reset --mixed HEAD~1     # this is the DEFAULT
# ✅ moves pointer   ✅ resets index   ❌ working dir unchanged
# → changes become UNSTAGED but present.

git reset --hard HEAD~1
# ✅ moves pointer   ✅ resets index   ✅ resets working dir  ⚠️ DESTRUCTIVE
# → changes are GONE (recoverable via reflog for ~90 days).
```

Memory aid: soft → **commits** undone. mixed → commits + **staging** undone.
hard → commits + staging + **your files** undone.

Path-limited form doesn't move the branch, it just unstages:

```bash
git reset HEAD file.txt        # legacy — prefer:
git restore --staged file.txt
```

## `git revert`

Creates a *new* commit that applies the inverse of a previous one. History is
preserved, so it's safe on shared branches.

```bash
git revert abc123
git revert HEAD
git revert --no-commit abc123      # stage without committing
git revert HEAD~3..HEAD            # revert a range
git revert -m 1 <merge-commit>     # revert a MERGE, keeping parent 1's line
git revert --abort
```

⚠️ **Reverting a merge is a trap.** After `git revert -m 1 <merge>`, re-merging
that branch won't reintroduce the changes, because Git thinks they're already
merged. You must revert the revert, or rebuild the branch.

## Decision table

| Situation | Command |
|---|---|
| Discard unstaged edits to a file | `git restore file` |
| Unstage a file | `git restore --staged file` |
| Fix the last commit's message | `git commit --amend` |
| Undo last commit, keep staged | `git reset --soft HEAD~1` |
| Undo last commit, keep files | `git reset HEAD~1` |
| Obliterate last commit + changes | `git reset --hard HEAD~1` |
| Undo a commit already pushed | `git revert <hash>` |
| Undo a pushed commit on *your* branch | `reset --hard` + `push --force-with-lease` |

---

## Related

- [[Git - Undo Cookbook]]
- [[Git - Blame Bisect Reflog]]
- [[Git - Rebase]]

## Sources

- <https://git-scm.com/docs/git-reset>
- <https://git-scm.com/docs/git-revert>
- <https://git-scm.com/docs/git-restore>
- <https://git-scm.com/book/en/v2/Git-Tools-Reset-Demystified>
- <https://git-scm.com/docs/howto/revert-a-faulty-merge>
