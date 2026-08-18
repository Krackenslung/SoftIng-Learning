---
title: Command Cheat Sheet
domain: reference
section: 24
category: reference
difficulty: beginner
danger: medium
tags:
  - git/cheatsheet
  - reference
commands: []
related:
  - "[[Git - Undo Cookbook]]"
  - "[[Glossary]]"
sources:
  - https://git-scm.com/docs
  - https://education.github.com/git-cheat-sheet-education.pdf
  - https://git-scm.com/book/en/v2
updated: 2026-08-14
---

# Command Cheat Sheet


## Setup
| Command | Purpose |
|---|---|
| `git config --global user.name "X"` | Set name |
| `git config --list --show-origin` | All settings + source file |
| `git init` | New repo |
| `git clone URL` | Copy a repo |

## Daily
| Command | Purpose |
|---|---|
| `git status -sb` | Compact status |
| `git add -p` | Stage interactively |
| `git commit -m "msg"` | Commit |
| `git commit --amend --no-edit` | Fix last commit |
| `git diff` / `--staged` | Unstaged / staged changes |
| `git log --oneline --graph --all` | Visual history |
| `git show HEAD` | Inspect a commit |

## Branching
| Command | Purpose |
|---|---|
| `git switch -c name` | Create + switch |
| `git switch -` | Previous branch |
| `git branch -vv` | Branches + upstreams |
| `git branch -d name` | Delete (safe) |
| `git merge branch` | Merge in |
| `git rebase main` | Replay onto main |
| `git rebase -i HEAD~5` | Rewrite last 5 |

## Remote
| Command | Purpose |
|---|---|
| `git fetch --all --prune` | Update refs, no changes |
| `git pull --rebase` | Fetch + replay |
| `git push -u origin HEAD` | Push + set upstream |
| `git push --force-with-lease` | Safe force push |
| `git push --follow-tags` | Push + annotated tags |

## Undo
| Command | Purpose |
|---|---|
| `git restore file` | Discard file changes ⚠️ |
| `git restore --staged file` | Unstage |
| `git reset --soft HEAD~1` | Undo commit, keep staged |
| `git reset --hard HEAD~1` | Obliterate ⚠️ |
| `git revert HASH` | Safe undo of a pushed commit |
| `git reflog` | Find anything you lost |

## Investigate
| Command | Purpose |
|---|---|
| `git log -S "text"` | When did this string appear/vanish |
| `git log -L :func:file` | Evolution of a function |
| `git grep -n "text"` | Search tracked files |
| `git blame -w -C file` | Line authorship |
| `git bisect run ./test.sh` | Auto-find the breaking commit |
| `git shortlog -sn` | Commits per author |

## Other
| Command | Purpose |
|---|---|
| `git stash -u` | Park work incl. untracked |
| `git stash pop` | Restore it |
| `git worktree add ../dir branch` | Second checkout |
| `git tag -a v1.0 -m "msg"` | Annotated tag |
| `git describe --tags --dirty` | Version string |
| `git clean -nd` | Dry-run cleanup |

## Danger list ⚠️
`reset --hard` · `clean -fdx` · `push --force` · `branch -D` ·
`stash clear` · `gc --prune=now` · `reflog expire --expire=now` ·
`filter-repo` · any rebase of shared history

---

## Related

- [[Git - Undo Cookbook]]
- [[Glossary]]

## Sources

- <https://git-scm.com/docs>
- <https://education.github.com/git-cheat-sheet-education.pdf>
- <https://git-scm.com/book/en/v2>
