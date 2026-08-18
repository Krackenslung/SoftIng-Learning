---
title: GitHub vs Git
domain: github
section: 01
category: platform
difficulty: beginner
danger: none
tags:
  - github/foundations
commands: []
related:
  - "[[Git - What Git Is]]"
  - "[[Bridge - Forks and Remotes]]"
  - "[[GitHub - Repositories]]"
sources:
  - https://docs.github.com/en/get-started/start-your-journey/about-github-and-git
  - https://git-scm.com/about
updated: 2026-08-14
---

# GitHub vs Git

Git is the version control tool. GitHub is a hosting platform built on top of it,
plus a large layer of collaboration features that are **not part of Git at all**.

Confusing the two is the single most common source of mental-model errors.

## What is Git

| Concept | Lives in |
|---|---|
| Commits, trees, blobs | Git |
| Branches, tags, refs | Git |
| Merge, rebase, cherry-pick | Git |
| Remotes, fetch, push | Git |
| Hooks | Git (local) |

## What is GitHub only

| Concept | Exists only on GitHub |
|---|---|
| Pull Requests | ✅ |
| Forks | ✅ (Git has no "fork") |
| Issues, Labels, Milestones | ✅ |
| Code review, CODEOWNERS | ✅ |
| Branch protection, Rulesets | ✅ |
| Actions / CI | ✅ |
| Releases (as distinct from tags) | ✅ |
| Stars, watchers, Discussions | ✅ |
| Notifications | ✅ |

## Why it matters for tooling

If you are building an integration, this line determines **which data source you
query**. Anything in the left column you can read from a local clone with plumbing
commands. Anything in the right column requires the [[GitHub - REST API]] or
[[GitHub - GraphQL API]] — there is no local copy of it.

A dashboard that shows commits can work offline. A dashboard that shows PRs cannot.

## The practical consequence

Git is fully decentralized; GitHub reintroduces a centre. `origin` is technically
just a remote, but every GitHub feature assumes it is *the* authoritative one.

---

## Related

- [[Git - What Git Is]]
- [[Bridge - Forks and Remotes]]
- [[GitHub - Repositories]]

## Sources

- <https://docs.github.com/en/get-started/start-your-journey/about-github-and-git>
- <https://git-scm.com/about>
