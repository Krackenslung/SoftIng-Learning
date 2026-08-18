---
title: Branching
domain: git
section: 07
category: daily-use
difficulty: beginner
danger: medium
tags:
  - git/branching
commands:
  - git branch
  - git switch
related:
  - "[[Git - Merging]]"
  - "[[Git - Rebase]]"
  - "[[Git - Remotes]]"
  - "[[GitHub - Branch Protection and Rulesets]]"
sources:
  - https://git-scm.com/docs/git-branch
  - https://git-scm.com/docs/git-switch
  - https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell
  - https://git-scm.com/book/en/v2/Git-Branching-Remote-Branches
  - https://git-scm.com/book/en/v2/Git-Tools-Revision-Selection
updated: 2026-08-14
---

# Branching


A branch is a movable pointer to a commit. Creating one writes a single small
file. This cheapness is the design principle behind every Git workflow.

## Creating and switching

```bash
git branch                       # list local
git branch -a                    # + remote-tracking
git branch -vv                   # + upstream + last commit
git branch feature-x             # create, don't switch
git switch feature-x             # switch
git switch -c feature-x          # create + switch
git switch -c hotfix main        # branch from a specific base
git switch -                     # previous branch (like `cd -`)
git switch --detach abc123       # deliberately detach
```

## Deleting and renaming

```bash
git branch -d feature-x          # safe: refuses if unmerged
git branch -D feature-x          # force ⚠️
git push origin --delete feature-x   # delete on the remote
git branch -m old new            # rename
git branch -m new                # rename current branch

git branch --merged main         # branches fully merged into main
git branch --no-merged main      # branches with unmerged work
```

Cleanup one-liner for merged local branches:

```bash
git branch --merged main | grep -v '^\*\|main' | xargs -r git branch -d
```

## Tracking branches

A **remote-tracking branch** (`origin/main`) is a local, read-only cache of where
that branch was on the remote *the last time you fetched*. It does not update
itself.

A **tracking branch** is a local branch configured with an upstream:

```bash
git switch -c feature origin/feature      # auto-sets upstream
git branch -u origin/feature              # set upstream on existing branch
git push -u origin feature                # push + set upstream
git branch --unset-upstream
```

With an upstream set, bare `git pull`, `git push`, and `git status`'s
ahead/behind counts all work.

## Detached HEAD

HEAD points directly at a commit instead of a branch. You get here from
`git checkout <hash>`, `git switch --detach`, checking out a tag, or during a
rebase/bisect.

You can look around and even commit — but new commits belong to no branch and
become unreachable once you switch away. Git warns you and prints the hash.

To keep the work:

```bash
git switch -c new-branch          # from within detached HEAD
```

To recover after you already left:

```bash
git reflog                        # find the hash
git switch -c rescue abc123
```

---

## Related

- [[Git - Merging]]
- [[Git - Rebase]]
- [[Git - Remotes]]
- [[GitHub - Branch Protection and Rulesets]]

## Sources

- <https://git-scm.com/docs/git-branch>
- <https://git-scm.com/docs/git-switch>
- <https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell>
- <https://git-scm.com/book/en/v2/Git-Branching-Remote-Branches>
- <https://git-scm.com/book/en/v2/Git-Tools-Revision-Selection>
