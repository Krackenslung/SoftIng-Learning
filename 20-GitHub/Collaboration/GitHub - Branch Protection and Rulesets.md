---
title: Branch Protection and Rulesets
domain: github
section: 09
category: collaboration
difficulty: intermediate
danger: high
tags:
  - github/policy
  - github/security
commands: []
endpoints:
  - GET /repos/{owner}/{repo}/branches/{branch}/protection
  - GET /repos/{owner}/{repo}/rulesets
  - GET /orgs/{org}/rulesets
dashboard_relevant: true
related:
  - "[[Bridge - Branch Protection vs Hooks]]"
  - "[[GitHub - Pull Requests]]"
  - "[[GitHub - Actions]]"
sources:
  - https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
  - https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
  - https://docs.github.com/en/rest/repos/rules
updated: 2026-08-14
---

# Branch Protection and Rulesets

Server-side enforcement of what may reach a branch. This is the **only** reliable
place to enforce policy — client hooks can be bypassed with `--no-verify`. See
[[Bridge - Branch Protection vs Hooks]].

## Two systems

| | Branch protection rules | Rulesets |
|---|---|---|
| Scope | One repo, one branch pattern | Repo **or org**-wide |
| Layering | One rule wins | Multiple rulesets **stack** |
| Targets | Branches | Branches **and tags**, incl. push rules |
| Modes | Active only | `disabled` / `evaluate` (dry run) / `active` |
| Visibility | Admin only | Contributors can see what applies |

Rulesets are the newer system and the one to build on. `evaluate` mode lets you
test a policy against real traffic before enforcing — use it.

## Common rules

- Require a pull request before merging (+ N approvals)
- Dismiss stale approvals on new commits
- Require review from **Code Owners**
- Require **status checks** to pass (name them explicitly)
- Require branches to be **up to date** before merging
- Require conversation resolution
- Require signed commits → see [[Git - Commit Conventions]]
- Require linear history (blocks merge commits)
- Require deployment to succeed
- Block force pushes
- Restrict deletions
- Restrict who can push (bypass list)

## ⚠️ Sharp edges

- **"Require branches to be up to date" + a busy repo = merge starvation.** Every
  merge invalidates every other PR. Use a **merge queue** instead.
- **A required status check that never reports blocks the PR forever.** If a
  workflow is skipped by a `paths` filter, its check never arrives. Fix with a
  dummy job that reports success on skip.
- **Renaming a workflow job orphans the required check.** The old name stays
  required and never reports.
- Bypass lists are a genuine hole — audit them; they are visible via the API.

## For a dashboard

`GET /repos/{owner}/{repo}/rules/branches/{branch}` returns the **effective**
rules for a branch, merged across all rulesets. That is far more useful than
reading rulesets individually and re-implementing the merge logic.

---

## Related

- [[Bridge - Branch Protection vs Hooks]]
- [[GitHub - Pull Requests]]
- [[GitHub - Actions]]

## Sources

- <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets>
- <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches>
- <https://docs.github.com/en/rest/repos/rules>
