---
title: Rebase
domain: git
section: 09
category: history-rewriting
difficulty: intermediate
danger: high
tags:
  - git/history
  - git/rebase
commands:
  - git rebase
  - git rebase -i
  - git push --force-with-lease
related:
  - "[[Git - Merging]]"
  - "[[Git - Reset Revert Restore]]"
  - "[[Git - Undo Cookbook]]"
sources:
  - https://git-scm.com/docs/git-rebase
  - https://git-scm.com/book/en/v2/Git-Branching-Rebasing
  - https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History
  - https://git-scm.com/docs/git-push
  - https://github.blog/open-source/git/highlights-from-git-2-30/
updated: 2026-08-14
---

# Rebase


Rebase replays your commits on top of a different base, producing a linear
history. It **rewrites commits** — the replayed commits have new hashes.

## Standard rebase

```bash
git switch feature
git rebase main
```

```
before:  A───B───E  (main)      after:  A───B───E  (main)
              \                                  \
               C───D  (feature)                   C'──D'  (feature)
```

C' and D' contain the same changes as C and D but are different objects.

```bash
git rebase --continue     # after resolving a conflict
git rebase --skip         # drop the current commit
git rebase --abort        # restore pre-rebase state
```

## Interactive rebase

```bash
git rebase -i HEAD~5           # last 5 commits
git rebase -i main             # everything since diverging from main
git rebase -i --root           # entire history
```

The editor lists commits **oldest first**. Change the verb on each line:

| Verb | Short | Effect |
|---|---|---|
| `pick` | `p` | keep as is |
| `reword` | `r` | keep changes, edit the message |
| `edit` | `e` | pause here so you can amend |
| `squash` | `s` | fold into previous, combine messages |
| `fixup` | `f` | fold into previous, **discard** this message |
| `drop` | `d` | delete the commit |
| `exec` | `x` | run a shell command (e.g. tests) at that point |
| `break` | `b` | stop for manual inspection |

Reordering the lines reorders the commits. Deleting a line drops that commit.

**Autosquash workflow** — the clean way to fix up review feedback:

```bash
git commit --fixup=abc123           # or --squash=abc123
git rebase -i --autosquash abc123~1 # lines are pre-arranged for you
git config --global rebase.autosquash true   # make it the default
```

**Run tests on every commit:**

```bash
git rebase -i --exec "npm test" main
```

## The golden rule

> **Do not rebase commits that exist outside your repository.**

Rewriting shared history forces everyone else into a painful reconciliation. The
practical version: rebase freely on your own unpushed or personal-branch work;
never rebase `main` or any branch others build on.

If you must force-push a rebased personal branch:

```bash
git push --force-with-lease        # ✅ refuses if the remote moved unexpectedly
git push --force                   # ❌ clobbers whatever is there
```

`--force-with-lease` is a safety interlock. Prefer it always. Add
`--force-if-includes` (Git 2.30+) for extra protection against a fetch-without-
integrate race.

## `--onto`

Transplant a range of commits onto a new base. Used when you branched off the
wrong branch.

```bash
# feature branched off wrongbase; move it onto main
git rebase --onto main wrongbase feature
```

Read as: take commits in `wrongbase..feature`, replay them onto `main`.

## Rebase vs. merge

| | Merge | Rebase |
|---|---|---|
| History | True, non-linear | Linear, tidy |
| Preserves original hashes | Yes | No |
| Safe on shared branches | Yes | No |
| Conflict resolution | Once | Potentially once *per commit* |
| Bisect quality | Noisier | Cleaner |
| Audit trail | Complete | Idealized |

Common team policy: rebase your feature branch onto `main` before opening a PR;
merge the PR with a merge commit or a squash.

---

## Related

- [[Git - Merging]]
- [[Git - Reset Revert Restore]]
- [[Git - Undo Cookbook]]

## Sources

- <https://git-scm.com/docs/git-rebase>
- <https://git-scm.com/book/en/v2/Git-Branching-Rebasing>
- <https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History>
- <https://git-scm.com/docs/git-push>
- <https://github.blog/open-source/git/highlights-from-git-2-30/>
