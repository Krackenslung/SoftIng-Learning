---
title: Remotes
domain: git
section: 13
category: collaboration
difficulty: intermediate
danger: high
tags:
  - git/remotes
commands:
  - git fetch
  - git pull
  - git push
  - git remote
related:
  - "[[Git - Branching]]"
  - "[[Bridge - Forks and Remotes]]"
  - "[[Git - Workflows]]"
sources:
  - https://git-scm.com/docs/git-fetch
  - https://git-scm.com/docs/git-pull
  - https://git-scm.com/docs/git-push
  - https://git-scm.com/docs/git-remote
  - https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes
  - https://git-scm.com/book/en/v2/Git-Internals-The-Refspec
  - https://github.blog/open-source/git/highlights-from-git-2-27/
updated: 2026-08-14
---

# Remotes


## Fetch vs. pull

```bash
git fetch origin          # download objects, update origin/* — TOUCHES NOTHING LOCAL
git fetch --all --prune
git pull                  # = fetch + merge (or rebase)
```

**`fetch` is always safe.** It never changes your working directory or your local
branches. Get in the habit of `git fetch` + inspect + integrate:

```bash
git fetch origin
git log HEAD..origin/main --oneline    # what's incoming
git diff HEAD origin/main              # what would change
git merge origin/main                  # or rebase
```

## Pull configuration

```bash
git pull --rebase
git pull --ff-only
git config --global pull.rebase true      # rebase by default
git config --global pull.ff only          # or: refuse anything but fast-forward
```

Since Git 2.27, bare `git pull` on diverged branches warns and requires you to
choose. Set one of the above once and stop thinking about it.

## Push

```bash
git push
git push origin main
git push -u origin feature            # set upstream on first push
git push --all
git push --tags
git push origin --delete old-branch
git push --force-with-lease           # safe force
git push --dry-run
```

```bash
git config --global push.default simple            # default; push current branch to its upstream
git config --global push.autoSetupRemote true      # `git push` works on brand-new branches
```

## Refspecs

The full push/fetch syntax is `<src>:<dst>`.

```bash
git push origin main:main
git push origin HEAD:main                  # push current branch as main
git push origin local-name:remote-name     # rename during push
git push origin :old-branch                # delete (empty source)
git fetch origin main:local-copy-of-main
```

The `+` prefix means "allow non-fast-forward". A remote's default fetch refspec
lives in `.git/config`:

```ini
[remote "origin"]
    url = git@github.com:user/repo.git
    fetch = +refs/heads/*:refs/remotes/origin/*
```

## Pruning

```bash
git fetch --prune                       # delete origin/* refs for deleted remote branches
git remote prune origin
git config --global fetch.prune true    # always
```

Note this cleans up *remote-tracking* refs, not your local branches. For those,
see §7.2.

## Multiple remotes (fork workflow)

```bash
git remote add upstream git@github.com:original/repo.git
git fetch upstream
git switch main
git merge upstream/main         # or: git rebase upstream/main
git push origin main
```

---

## Related

- [[Git - Branching]]
- [[Bridge - Forks and Remotes]]
- [[Git - Workflows]]

## Sources

- <https://git-scm.com/docs/git-fetch>
- <https://git-scm.com/docs/git-pull>
- <https://git-scm.com/docs/git-push>
- <https://git-scm.com/docs/git-remote>
- <https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes>
- <https://git-scm.com/book/en/v2/Git-Internals-The-Refspec>
- <https://github.blog/open-source/git/highlights-from-git-2-27/>
