---
title: Maintenance & Internals
domain: git
section: 22
category: advanced
difficulty: advanced
danger: high
tags:
  - git/internals
commands:
  - git cat-file
  - git gc
  - git fsck
  - git maintenance
related:
  - "[[Git - Mental Model]]"
  - "[[Git - Undo Cookbook]]"
sources:
  - https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain
  - https://git-scm.com/book/en/v2/Git-Internals-Git-Objects
  - https://git-scm.com/book/en/v2/Git-Internals-Packfiles
  - https://git-scm.com/docs/git-gc
  - https://git-scm.com/docs/git-maintenance
  - https://git-scm.com/docs/git-cat-file
  - https://git-scm.com/docs/BreakingChanges
  - https://git-scm.com/docs/hash-function-transition
  - https://git-scm.com/docs/reftable
  - https://github.blog/open-source/git/highlights-from-git-2-45/
updated: 2026-08-14
---

# Maintenance & Internals


## The object model

Four object types, all content-addressed:

| Object | Contains |
|---|---|
| **blob** | File contents (no name, no permissions) |
| **tree** | Directory listing: names, modes, → blob/tree hashes |
| **commit** | → tree, → parent(s), author, committer, message |
| **tag** | → object, type, tagger, message (annotated tags only) |

```
commit ──► tree ──► tree (subdir) ──► blob
              └───► blob
```

Identical content anywhere in history = one blob, stored once. That's the
deduplication.

Inspect them:

```bash
git cat-file -t abc123          # type
git cat-file -p abc123          # pretty-print contents
git cat-file -s abc123          # size
git rev-parse HEAD              # resolve a ref to a hash
git ls-tree HEAD                # tree at HEAD
git ls-tree -r HEAD             # recursive
git hash-object file.txt        # what hash WOULD this content get
```

## `.git/` anatomy

```
.git/
├── HEAD              # "ref: refs/heads/main"
├── config            # repo-local config
├── description       # used by gitweb only
├── index             # the staging area (binary)
├── hooks/            # hook scripts
├── info/
│   └── exclude       # local-only ignore rules
├── logs/             # the REFLOG lives here
│   ├── HEAD
│   └── refs/
├── objects/
│   ├── ab/cd1234...  # loose objects (zlib-compressed)
│   ├── pack/         # packfiles (*.pack, *.idx)
│   └── info/
├── refs/
│   ├── heads/        # local branches
│   ├── remotes/      # remote-tracking branches
│   └── tags/
└── packed-refs       # refs compacted into one file
```

## Loose objects vs. packfiles

New objects are written **loose**: one zlib-compressed file each. Periodically
Git packs them into **packfiles**, which use delta compression between similar
objects and are far more space- and network-efficient. Packfiles are what get
transferred over the wire.

## Garbage collection & repo health

```bash
git gc                       # pack loose objects, prune, expire reflogs
git gc --aggressive          # slower, better packing — rarely needed
git gc --prune=now           # ⚠️ removes unreachable objects immediately
git count-objects -vH        # size report
git fsck                     # integrity check
git fsck --lost-found        # write dangling objects out for recovery
git prune                    # remove unreachable objects
git repack -ad               # repack everything
git maintenance start        # register background maintenance (Git 2.30+)
```

Git runs `gc --auto` automatically after some commands, so manual `gc` is
seldom necessary. `git maintenance` is the modern scheduled alternative.

⚠️ `gc --prune=now` can destroy objects your reflog would otherwise have let you
recover. Don't run it while panicking about lost work.

Finding what's making a repo huge:

```bash
git count-objects -vH
git rev-list --objects --all |
  git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' |
  sort -k3 -n -r | head -20
```

## Storage formats in transition

Two defaults change for **newly created** repositories in Git 3.0. Existing
repositories keep working unchanged.

**Object format — SHA-1 → SHA-256.** Motivated by demonstrated SHA-1 collision
attacks. Hashes go from 40 to 64 hex characters, which can break scripts and
tooling that assume 40. Forge support is the gating factor. There is no plan to
deprecate SHA-1.

```bash
git init --object-format=sha256      # opt in today
```

**Ref backend — files → reftable.** The `files` backend stores one file per ref
plus a `packed-refs` file; it struggles with many refs, requires rewriting all of
`packed-refs` to delete one ref, and can't store two refs differing only in case
on case-insensitive filesystems (Windows, macOS). Reftable is a binary, prefix-
compressed format that fixes all of this.

```bash
git init --ref-format=reftable       # opt in today
git config --global init.defaultRefFormat reftable
```

Git 3.0 is also expected to introduce Rust components into the build and remove
some long-deprecated commands (e.g. `git whatchanged`).

---

## Related

- [[Git - Mental Model]]
- [[Git - Undo Cookbook]]

## Sources

- <https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain>
- <https://git-scm.com/book/en/v2/Git-Internals-Git-Objects>
- <https://git-scm.com/book/en/v2/Git-Internals-Packfiles>
- <https://git-scm.com/docs/git-gc>
- <https://git-scm.com/docs/git-maintenance>
- <https://git-scm.com/docs/git-cat-file>
- <https://git-scm.com/docs/BreakingChanges>
- <https://git-scm.com/docs/hash-function-transition>
- <https://git-scm.com/docs/reftable>
- <https://github.blog/open-source/git/highlights-from-git-2-45/>
