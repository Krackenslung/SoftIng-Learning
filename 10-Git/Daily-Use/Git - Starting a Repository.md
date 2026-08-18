---
title: Starting a Repository
domain: git
section: 04
category: daily-use
difficulty: beginner
danger: none
tags:
  - git/setup
commands:
  - git init
  - git clone
  - git remote add
related:
  - "[[Git - Remotes]]"
  - "[[Git - Submodules and LFS]]"
sources:
  - https://git-scm.com/docs/git-init
  - https://git-scm.com/docs/git-clone
  - https://git-scm.com/docs/git-remote
  - https://github.blog/open-source/git/get-up-to-speed-with-partial-clone-and-shallow-clone/
  - https://git-scm.com/docs/partial-clone
updated: 2026-08-14
---

# Starting a Repository


## `git init`

```bash
git init                          # current directory
git init my-project               # create + init
git init --bare repo.git          # server-side repo, no working directory
git init --initial-branch=main
git init --object-format=sha256   # SHA-256 repo (limited forge support today)
git init --ref-format=reftable    # reftable backend (Git 2.45+)
```

## `git clone`

```bash
git clone https://github.com/user/repo.git
git clone git@github.com:user/repo.git my-dir     # custom target dir
git clone --branch develop --single-branch URL    # one branch only
git clone --depth 1 URL                           # shallow: latest commit only
git clone --filter=blob:none URL                  # blobless — fetch blobs lazily
git clone --filter=tree:0 URL                     # treeless — most aggressive
git clone --recurse-submodules URL
```

**Which clone type when:**

| Type | Use for | Cost |
|---|---|---|
| Full | Normal development | Full history download |
| `--depth 1` | CI builds, Dockerfiles | Can't see history, awkward to deepen |
| `--filter=blob:none` | Large repos you still need history for | Lazy fetch needs network |
| `--filter=tree:0` | Massive monorepos, CI | Many local ops trigger fetches |

Partial clone (`--filter`) is generally the better modern choice over shallow
clone for developer machines, because history operations still work.

## Adding remotes

```bash
git remote add origin git@github.com:user/repo.git
git remote -v
git remote rename origin upstream
git remote set-url origin NEW_URL
git remote remove old-remote
```

---

## Related

- [[Git - Remotes]]
- [[Git - Submodules and LFS]]

## Sources

- <https://git-scm.com/docs/git-init>
- <https://git-scm.com/docs/git-clone>
- <https://git-scm.com/docs/git-remote>
- <https://github.blog/open-source/git/get-up-to-speed-with-partial-clone-and-shallow-clone/>
- <https://git-scm.com/docs/partial-clone>
