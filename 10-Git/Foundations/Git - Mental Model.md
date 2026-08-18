---
title: The Mental Model
domain: git
section: 02
category: foundations
difficulty: beginner
danger: none
tags:
  - git/foundations
  - git/internals
commands:
  - git status
related:
  - "[[Git - The Core Loop]]"
  - "[[Git - Internals]]"
  - "[[Git - Branching]]"
sources:
  - https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F
  - https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell
  - https://git-scm.com/book/en/v2/Git-Tools-Revision-Selection
  - https://git-scm.com/book/en/v2/Git-Tools-Reset-Demystified
  - https://git-scm.com/docs/gitrevisions
  - https://git-scm.com/docs/git-status
updated: 2026-08-14
---

# The Mental Model


Most Git confusion dissolves once these two models are internalized.

## The three trees

```
  working directory        index / staging area          HEAD (repository)
  ─────────────────        ────────────────────          ────────────────
  files you edit    ──►    what goes in next commit ──►  last committed snapshot
                    add                          commit
```

- **Working directory** — the actual files on disk. A checkout of one version.
- **Index (staging area)** — a binary file (`.git/index`) holding the *proposed
  next commit*. Its existence is what lets you commit a subset of your changes.
- **HEAD** — a pointer to the current branch, which points to the current commit.

Nearly every "confusing" Git command is just moving data between these three
trees. `git status` is literally a two-way diff report: working dir vs. index,
and index vs. HEAD.

## Commits as a DAG

A commit object contains:

- a pointer to a **tree** (the snapshot of the directory)
- pointer(s) to **parent** commit(s) — zero for the root, one normally, two or
  more for a merge
- author + committer (name, email, timestamp)
- the commit message

Because commits point *backwards* to parents, history forms a **directed acyclic
graph**. A branch is not a container of commits — it's a **41-byte file
containing a commit hash**. "Creating a branch" writes one file. That's the whole
operation.

```
        A───B───C  (main)
             \
              D───E  (feature)
```

`main` = pointer to C. `feature` = pointer to E. E's history is A→B→D→E.

## Refs and HEAD

- **ref** — a human-readable name pointing to a commit. Stored under `.git/refs/`
  (or in `packed-refs`, or in reftable in newer repos).
  - `refs/heads/main` — local branch
  - `refs/remotes/origin/main` — remote-tracking branch
  - `refs/tags/v1.0` — tag
- **HEAD** — usually a *symbolic ref*: the text `ref: refs/heads/main`. When it
  contains a raw hash instead, you are in **detached HEAD** state.

## Naming any commit

| Syntax | Means |
|---|---|
| `HEAD` | current commit |
| `HEAD~1`, `HEAD~3` | 1st / 3rd **first-parent** ancestor |
| `HEAD^` | first parent (same as `HEAD~1`) |
| `HEAD^2` | *second* parent — only meaningful on merge commits |
| `main@{2}` | where `main` pointed 2 moves ago (reflog) |
| `main@{yesterday}` | where `main` pointed yesterday |
| `abc123` | any unambiguous hash prefix |
| `:/fix login` | most recent commit whose message contains that text |
| `A..B` | commits reachable from B but not A |
| `A...B` | commits reachable from either, but not both |

---

## Related

- [[Git - The Core Loop]]
- [[Git - Internals]]
- [[Git - Branching]]

## Sources

- <https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F>
- <https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell>
- <https://git-scm.com/book/en/v2/Git-Tools-Revision-Selection>
- <https://git-scm.com/book/en/v2/Git-Tools-Reset-Demystified>
- <https://git-scm.com/docs/gitrevisions>
- <https://git-scm.com/docs/git-status>
