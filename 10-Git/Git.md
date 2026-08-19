---
title: Git
domain: git
type: hub
tags:
  - hub
  - git
updated: 2026-08-14
cssclasses:
  - hub
---

# Git

The distributed version control system. Everything here is true regardless of
where your code is hosted — for the platform layer, see [[GitHub]].

> [!tip] New here?
> Follow the **Learning path** below in order. Sections 1–8 build on each other;
> everything after that is lookup material.

## Learning path

1. [[Git - What Git Is]] — distributed VCS, snapshots not diffs
2. [[Git - Mental Model]] — three trees, the DAG, refs and HEAD
3. [[Git - Setup and Config]] — identity, aliases, line endings, auth
4. [[Git - Starting a Repository]] — init, clone, remotes
5. [[Git - The Core Loop]] — add, commit, diff, log, restore
6. [[Git - Ignoring Files]] — gitignore, gitattributes
7. [[Git - Branching]] — branches, tracking, detached HEAD
8. [[Git - Merging]] — fast-forward, three-way, conflicts

## By category

### Rewriting & repair
- [[Git - Rebase]] — replay history, interactive, the golden rule
- [[Git - Reset Revert Restore]] — soft/mixed/hard, when to use which
- [[Git - Cherry-pick]] — porting individual commits

### Collaboration
- [[Git - Remotes]] — fetch vs pull, push, refspecs
- [[Git - Workflows]] — trunk-based, GitHub flow, git-flow, forks
- [[Git - Commit Conventions]] — atomic commits, messages, signing
- [[Git - Tags and Releases]] — annotated tags, describe, semver

### Investigation
- [[Git - Searching History]] — log filters, pickaxe, grep
- [[Git - Blame Bisect Reflog]] — who, when, which commit broke it

### Advanced
- [[Git - Stash and Worktrees]] — parking work, multiple checkouts
- [[Git - Submodules and LFS]] — nested repos, sparse-checkout, large files
- [[Git - Hooks]] — client and server automation
- [[Git - Internals]] — objects, packfiles, gc, `.git/` anatomy

## 🚨 Emergency

> [!warning] Broke something?
> → **[[Git - Undo Cookbook]]** — recipes for the 13 common disasters
> → [[Git - Troubleshooting]] — error messages and fixes
>
> Almost nothing is lost for ~90 days. Start with `git reflog`.

## Reference
- [[Git - Cheat Sheet]]
- [[Glossary]]
- [[Sources]]

## Where Git ends and GitHub begins
- [[Bridge - Forks and Remotes]]
- [[Bridge - PRs vs Merge]]
- [[Bridge - Tags vs Releases]]
- [[Bridge - Branch Protection vs Hooks]]
- [[Bridge - Actions vs Git Hooks]]
- [[Bridge - Auth SSH HTTPS and Tokens]]
- [[Bridge - GitHub API Conventions]]
- [[Bridge - GitHub API on Android]]

---

## All Git notes

```dataview
TABLE category AS Category, difficulty AS Level, danger AS Risk
FROM "10-Git"
WHERE type != "hub"
SORT section ASC
```

## Commands that can lose work

```dataview
TABLE commands AS Commands
FROM "10-Git" OR "90-Reference"
WHERE danger = "high"
SORT section ASC
```
