---
title: Submodules, Subtrees, Sparse-checkout, LFS
domain: git
section: 20
category: advanced
difficulty: advanced
danger: medium
tags:
  - git/advanced
  - git/monorepo
commands:
  - git submodule
  - git subtree
  - git sparse-checkout
  - git lfs
related:
  - "[[Git - Starting a Repository]]"
  - "[[Git - Internals]]"
sources:
  - https://git-scm.com/docs/git-submodule
  - https://git-scm.com/docs/git-subtree
  - https://git-scm.com/docs/git-sparse-checkout
  - https://git-scm.com/book/en/v2/Git-Tools-Submodules
  - https://git-lfs.com/
  - https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage
  - https://github.blog/open-source/git/bring-your-monorepo-down-to-size-with-sparse-checkout/
updated: 2026-08-14
---

# Submodules, Subtrees, Sparse-checkout, LFS


## Submodules

A pointer to a specific commit in another repository.

```bash
git submodule add https://github.com/user/lib.git libs/lib
git clone --recurse-submodules URL
git submodule update --init --recursive     # after a normal clone
git submodule update --remote               # pull latest from tracked branch
git submodule foreach 'git pull origin main'
git submodule status
git submodule deinit -f libs/lib && git rm -f libs/lib   # removal
git config --global submodule.recurse true  # auto-recurse on pull/checkout
```

The parent repo records a **commit hash**, not a branch. Updating the submodule
means committing the new pointer in the parent.

- ✅ Clean separation, exact version pinning, independent access control
- ❌ Sharp edges everywhere: detached HEADs inside submodules, easy to forget
  `--init`, easy to commit a pointer to an unpushed commit, painful merges
- Fits: vendored third-party deps, shared internal libraries where the boundary
  is genuinely firm

## Subtrees

Merge another repo's content directly into a subdirectory of yours.

```bash
git subtree add --prefix=libs/lib https://github.com/user/lib.git main --squash
git subtree pull --prefix=libs/lib URL main --squash
git subtree push --prefix=libs/lib URL main
```

- ✅ Invisible to collaborators — normal clone just works, no extra commands
- ❌ Long commands you must remember, repo size grows, less explicit versioning
- Fits: when consumers shouldn't need to know or care

## Sparse-checkout

Work with only part of a large repository's tree.

```bash
git sparse-checkout init --cone
git sparse-checkout set apps/web libs/shared
git sparse-checkout list
git sparse-checkout add tools/
git sparse-checkout disable
```

Cone mode is directory-based and much faster than the legacy pattern mode. Pairs
naturally with partial clone (§4.2) for monorepos:

```bash
git clone --filter=blob:none --sparse URL
```

## Git LFS

Replaces large files with text pointers; actual content lives on an LFS server.

```bash
git lfs install
git lfs track "*.psd"
git lfs track "*.mp4"
git add .gitattributes         # ← the tracking config lives here; must be committed
git lfs ls-files
git lfs migrate import --include="*.psd"   # convert EXISTING history
git lfs pull
```

- ✅ Keeps clone size sane for binary assets
- ❌ Requires server support and quota; every collaborator needs the LFS client;
  migrating existing history rewrites it
- Fits: game assets, design files, media, datasets

## Choosing

| Need | Use |
|---|---|
| Pin an exact external dependency version | Submodule |
| Vendor code so consumers don't notice | Subtree |
| Work on a slice of a monorepo | Sparse-checkout (+ partial clone) |
| Version large binaries | LFS |
| Actual dependency management | Your language's package manager, honestly |

---

## Related

- [[Git - Starting a Repository]]
- [[Git - Internals]]

## Sources

- <https://git-scm.com/docs/git-submodule>
- <https://git-scm.com/docs/git-subtree>
- <https://git-scm.com/docs/git-sparse-checkout>
- <https://git-scm.com/book/en/v2/Git-Tools-Submodules>
- <https://git-lfs.com/>
- <https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage>
- <https://github.blog/open-source/git/bring-your-monorepo-down-to-size-with-sparse-checkout/>
