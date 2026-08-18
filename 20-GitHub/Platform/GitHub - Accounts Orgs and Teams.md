---
title: Accounts, Organizations and Teams
domain: github
section: 02
category: platform
difficulty: beginner
danger: medium
tags:
  - github/platform
  - github/permissions
commands: []
endpoints:
  - GET /orgs/{org}/members
  - GET /orgs/{org}/teams
  - GET /repos/{owner}/{repo}/collaborators
dashboard_relevant: true
related:
  - "[[GitHub - Repositories]]"
  - "[[GitHub - Branch Protection and Rulesets]]"
  - "[[GitHub - Authentication]]"
sources:
  - https://docs.github.com/en/organizations
  - https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization
updated: 2026-08-14
---

# Accounts, Organizations and Teams

## The hierarchy

```
Enterprise
└── Organization
    ├── Teams (nestable)
    │   └── Members
    └── Repositories
```

Personal accounts own repos directly and have no teams — collaborators are added
individually.

## Repository roles

| Role | Can |
|---|---|
| **Read** | Clone, pull, open issues/PRs |
| **Triage** | + manage issues and PRs without write access |
| **Write** | + push, manage some settings |
| **Maintain** | + repo settings, excluding sensitive/destructive ones |
| **Admin** | Everything, including delete and transfer |

Custom repository roles are available on Enterprise plans.

## Precedence

Permissions are **additive and highest-wins**. If someone is a member of two teams
with Read and Write, they get Write. Removing the Write team does not remove
access granted directly as a collaborator — a common audit blind spot.

## Teams

- Nestable; child teams inherit parent permissions
- `@org/team-name` mentions notify all members
- Usable in [[GitHub - Code Review]] via CODEOWNERS
- Can be synced from an IdP group (Enterprise + SAML)

## For a dashboard

Team and permission data is only visible to tokens with sufficient scope. A
fine-grained PAT needs explicit **Members** and **Administration** permissions;
see [[GitHub - Authentication]]. Expect 403s rather than empty lists when scope
is missing — handle them distinctly.

---

## Related

- [[GitHub - Repositories]]
- [[GitHub - Branch Protection and Rulesets]]
- [[GitHub - Authentication]]

## Sources

- <https://docs.github.com/en/organizations>
- <https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization>
