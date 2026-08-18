---
title: Workflows
domain: git
section: 14
category: collaboration
difficulty: intermediate
danger: none
tags:
  - git/workflow
commands: []
related:
  - "[[GitHub - Pull Requests]]"
  - "[[Bridge - PRs vs Merge]]"
  - "[[Git - Rebase]]"
sources:
  - https://docs.github.com/en/get-started/using-github/github-flow
  - https://nvie.com/posts/a-successful-git-branching-model/
  - https://www.atlassian.com/git/tutorials/comparing-workflows
  - https://trunkbaseddevelopment.com/
  - https://git-scm.com/book/en/v2/Distributed-Git-Distributed-Workflows
  - https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges
updated: 2026-08-14
---

# Workflows


## Trunk-based development

One long-lived branch (`main`). Very short-lived feature branches (hours to a
couple of days) or direct commits behind feature flags. Continuous integration in
the literal sense.

- ✅ Minimal merge pain, fastest feedback, forces good test discipline
- ❌ Requires strong CI, feature flags, and mature review culture
- Fits: SaaS, continuous deployment, high-trust teams

## GitHub Flow

`main` is always deployable. Branch → commit → open PR → review → merge → deploy.

- ✅ Simple, well-tooled, easy to teach
- ❌ No built-in story for supporting multiple released versions
- Fits: web apps, most teams, open source

## Git Flow

Branches: `main` (releases), `develop` (integration), `feature/*`, `release/*`,
`hotfix/*`.

- ✅ Explicit release management, good for versioned/shipped software
- ❌ Heavy; the original author has since noted it's a poor fit for continuously
  delivered web apps
- Fits: desktop/mobile apps, firmware, anything with maintained release lines

## Fork & pull request

Contributors fork to their own namespace, push branches there, and open PRs
against upstream. Standard for open source, where contributors lack write access.

## Choosing

| Question | If yes → |
|---|---|
| Deploy multiple times per day? | Trunk-based |
| Need to support several released versions? | Git Flow |
| Contributors without write access? | Fork & PR |
| Small team, deploy on merge? | GitHub Flow |

## Merge button semantics

| Option | Result | Trade-off |
|---|---|---|
| Merge commit | Preserves every branch commit + a merge node | Full fidelity, noisier graph |
| Squash and merge | One commit on `main` | Clean trunk, loses granular history |
| Rebase and merge | Commits replayed linearly, no merge node | Linear, but rewrites hashes |

---

## Related

- [[GitHub - Pull Requests]]
- [[Bridge - PRs vs Merge]]
- [[Git - Rebase]]

## Sources

- <https://docs.github.com/en/get-started/using-github/github-flow>
- <https://nvie.com/posts/a-successful-git-branching-model/>
- <https://www.atlassian.com/git/tutorials/comparing-workflows>
- <https://trunkbaseddevelopment.com/>
- <https://git-scm.com/book/en/v2/Distributed-Git-Distributed-Workflows>
- <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges>
