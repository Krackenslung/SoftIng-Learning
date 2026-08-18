---
title: Repositories
domain: github
section: 03
category: platform
difficulty: beginner
danger: medium
tags:
  - github/platform
  - github/repos
commands: []
endpoints:
  - GET /user/repos
  - GET /orgs/{org}/repos
  - GET /repos/{owner}/{repo}
  - GET /repos/{owner}/{repo}/branches
  - GET /repos/{owner}/{repo}/languages
dashboard_relevant: true
related:
  - "[[GitHub - Branch Protection and Rulesets]]"
  - "[[Git - Starting a Repository]]"
  - "[[GitHub - REST API]]"
sources:
  - https://docs.github.com/en/repositories
  - https://docs.github.com/en/rest/repos/repos
updated: 2026-08-14
---

# Repositories

## Visibility

| Level | Who can see | Notes |
|---|---|---|
| **Public** | Everyone | Actions minutes free; forkable by anyone |
| **Private** | Explicit collaborators | Counts against plan limits |
| **Internal** | All enterprise members | Enterprise only — good default for inner source |

⚠️ Making a private repo public **does not** retroactively hide history. Every
past commit becomes visible. Treat any secret ever committed as compromised —
see [[Git - Undo Cookbook]].

## Key settings worth knowing

- **Default branch** — `main`; changing it does not update open PRs' base
- **Merge methods** — enable/disable merge commit, squash, rebase per repo
- **Auto-delete head branches** — turn this on; it prevents branch sprawl
- **Allow auto-merge** — merge once checks pass
- **Template repository** — makes "Use this template" available
- **Topics** — free-text tags, queryable via `topic:` in search

## Special files

| Path | Effect |
|---|---|
| `README.md` | Rendered on the repo home page |
| `.github/CODEOWNERS` | Auto-request reviewers |
| `.github/ISSUE_TEMPLATE/` | Issue forms and templates |
| `.github/PULL_REQUEST_TEMPLATE.md` | Prefilled PR body |
| `.github/workflows/` | [[GitHub - Actions]] |
| `.github/dependabot.yml` | Dependency update config |
| `CITATION.cff` | Citation metadata |
| `.git-blame-ignore-revs` | Honored by GitHub's blame view |
| `SECURITY.md` | Linked from the Security tab |
| `FUNDING.yml` | Sponsor button |

A repo named the same as your username (or `.github` in an org) becomes a profile
/ org-wide default repository.

## Useful API fields for a dashboard

`full_name`, `private`, `fork`, `archived`, `disabled`, `default_branch`,
`open_issues_count`, `pushed_at`, `stargazers_count`, `language`, `permissions`.

⚠️ `open_issues_count` **includes pull requests**. To get real issue counts you
must subtract PRs or query with a search filter. This trips up almost every
first-pass dashboard.

---

## Related

- [[GitHub - Branch Protection and Rulesets]]
- [[Git - Starting a Repository]]
- [[GitHub - REST API]]

## Sources

- <https://docs.github.com/en/repositories>
- <https://docs.github.com/en/rest/repos/repos>
