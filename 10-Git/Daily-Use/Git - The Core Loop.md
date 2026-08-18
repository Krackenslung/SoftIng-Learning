---
title: The Core Loop
domain: git
section: 05
category: daily-use
difficulty: beginner
danger: low
tags:
  - git/daily
commands:
  - git add
  - git commit
  - git status
  - git diff
  - git log
  - git restore
related:
  - "[[Git - Mental Model]]"
  - "[[Git - Commit Conventions]]"
  - "[[Git - Reset Revert Restore]]"
sources:
  - https://git-scm.com/docs/git-add
  - https://git-scm.com/docs/git-commit
  - https://git-scm.com/docs/git-diff
  - https://git-scm.com/docs/git-log
  - https://git-scm.com/docs/git-restore
  - https://git-scm.com/docs/git-switch
  - https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository
  - https://github.blog/open-source/git/highlights-from-git-2-23/
updated: 2026-08-14
---

# The Core Loop


```
edit  →  git add  →  git commit  →  (git push)
  ▲                                     │
  └─────────────────────────────────────┘
```

## `git status`

```bash
git status
git status -s          # short format
git status -sb         # short + branch line
git status --ignored   # include ignored files
```

Short-format columns: left char = index state, right char = working tree state.
`M ` = staged modification. ` M` = unstaged modification. `MM` = both. `??` =
untracked.

## `git add`

```bash
git add file.txt
git add src/               # directory, recursively
git add .                  # everything under current dir
git add -A                 # all changes in the whole repo, incl. deletions
git add -u                 # only already-tracked files
git add -p                 # INTERACTIVE: stage hunk by hunk
git add -N file            # "intent to add" — makes an untracked file diffable
```

`git add -p` is the highest-leverage command in this document. It forces you to
read your own diff before committing and makes atomic commits practical. Keys:
`y` stage, `n` skip, `s` split hunk, `e` edit hunk manually, `q` quit.

## `git commit`

```bash
git commit                        # open editor
git commit -m "Short summary"
git commit -am "msg"              # stage tracked-file changes AND commit
git commit --amend                # replace the last commit
git commit --amend --no-edit      # amend, keep the message
git commit --allow-empty -m "trigger CI"
git commit --fixup=abc123         # marked for autosquash during rebase
```

⚠️ `--amend` creates a **new commit object** with a new hash. Never amend a
commit that others have already pulled (see §9.3).

## `git diff`

```bash
git diff                    # working dir vs. index (unstaged changes)
git diff --staged           # index vs. HEAD (what you're about to commit)
git diff HEAD               # working dir vs. HEAD (everything)
git diff main..feature      # tip-to-tip
git diff main...feature     # feature since it diverged from main ← usually this
git diff --stat             # summary only
git diff --word-diff        # word-level, good for prose
git diff -- path/to/file    # limit to a path
git diff --check            # find whitespace errors
```

## `git log`

```bash
git log --oneline --graph --decorate --all     # the one to alias
git log -5                                     # last 5
git log -p                                     # with patches
git log --stat                                 # with file change summary
git log --author="Jane"
git log --since="2 weeks ago" --until="yesterday"
git log --grep="fix.*login" -i
git log -- path/to/file                        # history of one path
git log --follow -- file                       # ...across renames
git log --first-parent                         # skip inside merged branches
git log main..feature                          # what feature adds
git log --format="%h %an %ar %s"               # custom formatting
```

## `git show`

```bash
git show                  # HEAD, full patch
git show abc123
git show HEAD~3:src/app.js    # a FILE as it was at that commit
git show v1.0.0               # a tag and what it points at
git show --stat HEAD
```

## Removing, moving, restoring

```bash
git rm file.txt                 # delete from disk AND stage the deletion
git rm --cached secrets.env     # UNTRACK but keep on disk
git rm -r --cached .            # untrack everything (after fixing .gitignore)
git mv old.txt new.txt          # = mv + git rm + git add

git restore file.txt            # discard unstaged changes ⚠️ destructive
git restore --staged file.txt   # unstage, keep working-dir changes
git restore --source=HEAD~2 file.txt   # pull an old version into working dir
git restore .                   # discard ALL unstaged changes ⚠️
```

Git does not track renames explicitly — it detects them by content similarity at
diff time. `git mv` is a convenience, not a metadata operation.

## Modern vs. legacy commands

`git checkout` was overloaded (switch branches *and* restore files). Git 2.23
split it into `git switch` and `git restore`. They are no longer experimental and
are the recommended commands.

| Legacy | Modern |
|---|---|
| `git checkout main` | `git switch main` |
| `git checkout -b feat` | `git switch -c feat` |
| `git checkout -- file` | `git restore file` |
| `git checkout HEAD~2 -- file` | `git restore --source=HEAD~2 file` |

`git checkout` isn't going away; you'll see it everywhere in older material.

---

## Related

- [[Git - Mental Model]]
- [[Git - Commit Conventions]]
- [[Git - Reset Revert Restore]]

## Sources

- <https://git-scm.com/docs/git-add>
- <https://git-scm.com/docs/git-commit>
- <https://git-scm.com/docs/git-diff>
- <https://git-scm.com/docs/git-log>
- <https://git-scm.com/docs/git-restore>
- <https://git-scm.com/docs/git-switch>
- <https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository>
- <https://github.blog/open-source/git/highlights-from-git-2-23/>
