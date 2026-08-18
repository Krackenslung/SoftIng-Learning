---
title: What Git Is
domain: git
section: 01
category: foundations
difficulty: beginner
danger: none
tags:
  - git/foundations
commands: []
related:
  - "[[Git - Mental Model]]"
  - "[[GitHub - GitHub vs Git]]"
sources:
  - https://git-scm.com/about
  - https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control
  - https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F
  - https://git-scm.com/docs/BreakingChanges
updated: 2026-08-14
---

# What Git Is


Git is a **distributed version control system**. Created by Linus Torvalds in
2005 for Linux kernel development, it is now used by the overwhelming majority
of professional developers.

## Distributed, not centralized

In Subversion or CVS, there is one authoritative server; your local copy is a
thin working checkout. In Git, `git clone` gives you the **entire repository** —
all commits, all branches, all history. Consequences:

- Nearly every operation is local, and therefore fast (no network round-trip for
  `log`, `diff`, `blame`, `commit`, branch switching).
- You can work fully offline and sync later.
- Every clone is a complete backup.
- There is no technically-privileged "central" repo. `origin` is central only by
  team convention.

## Snapshots, not diffs

This is the single most important conceptual difference from older VCSs.

Most systems store a file list plus the per-file changes over time (delta-based).
Git instead stores a **snapshot of the entire tree** at each commit. Files that
didn't change aren't re-stored — Git stores a reference to the identical previous
blob. Diffs are *computed* on demand, not stored.

This is why branching is cheap, merging is reliable, and history is hard to
corrupt silently.

## Integrity by hashing

Everything in Git is content-addressed by a cryptographic hash. You cannot change
a file, a commit, or a directory tree without the hash changing. History is a
hash chain: each commit references its parent's hash, so altering an old commit
invalidates every commit after it.

Git has historically used SHA-1 (40 hex chars). Because of demonstrated SHA-1
collision attacks, Git moved to a hardened SHA-1 implementation, and SHA-256
support was added as an alternative object format. Git 3.0 will make SHA-256 the
default for new repositories (64 hex chars). There is no plan to remove SHA-1
support.

## The three states

Every file in a Git working directory is in one of three states:

| State | Meaning |
|---|---|
| **Modified** | Changed on disk, not yet marked for commit |
| **Staged** | Marked in its current version to go into the next commit |
| **Committed** | Safely stored in the local database |

---

## Related

- [[Git - Mental Model]]
- [[GitHub - GitHub vs Git]]

## Sources

- <https://git-scm.com/about>
- <https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control>
- <https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F>
- <https://git-scm.com/docs/BreakingChanges>
