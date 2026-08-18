---
title: Authentication
domain: github
section: 16
category: api
difficulty: intermediate
danger: high
tags:
  - github/api
  - github/auth
  - github/security
commands: []
endpoints:
  - GET /user
  - GET /rate_limit
dashboard_relevant: true
related:
  - "[[GitHub - Bots and Apps]]"
  - "[[GitHub - Rate Limits]]"
  - "[[Bridge - Auth SSH HTTPS and Tokens]]"
  - "[[API - OAuth 2.0 Flows]]"
  - "[[API - JWT]]"
  - "[[API - Token Storage on Public Clients]]"
sources:
  - https://docs.github.com/en/authentication
  - https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
  - https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api
updated: 2026-08-14
---

# Authentication

## Token types

| Type | Prefix | Life | Scope model |
|---|---|---|---|
| Classic PAT | `ghp_` | Configurable / never | Coarse scopes (`repo`, `admin:org`) |
| Fine-grained PAT | `github_pat_` | Max 1 year | Per-repo + per-permission |
| OAuth token | `gho_` | Long-lived | Scopes |
| App user token | `ghu_` | 8 hours (+ refresh) | App permissions |
| App installation token | `ghs_` | 1 hour | App permissions |
| Actions token | `ghs_` | Job duration | Workflow `permissions:` |

**Prefer fine-grained PATs.** Classic `repo` scope grants full read/write to
*every* repo you can access, including private ones you merely collaborate on —
a wildly over-broad grant for a dashboard that only needs to read PRs.

## Using a token

```http
Authorization: Bearer ghp_xxx
Accept: application/vnd.github+json
X-GitHub-Api-Version: 2022-11-28
User-Agent: my-dashboard/1.0
```

`User-Agent` is **required** — requests without it are rejected. Pin the API
version header; GitHub uses date-based versioning and unpinned clients can break.

## Permission mapping for a dashboard

| To read | Fine-grained permission |
|---|---|
| Repo metadata, branches | Metadata: read |
| Commits, contents | Contents: read |
| Issues | Issues: read |
| Pull requests | Pull requests: read |
| Workflow runs | Actions: read |
| Checks | Checks: read |
| Notifications | *(user-level)* Notifications: read |
| Projects v2 | Projects: read |
| Org members / teams | Members: read |

⚠️ **Metadata: read is mandatory** and implicitly required by most others.

## Handling failures

| Code | Meaning | Response |
|---|---|---|
| 401 | Bad/expired/revoked token | Re-auth; don't retry |
| 403 + `x-ratelimit-remaining: 0` | Primary rate limit | Wait for reset |
| 403 + `retry-after` | Secondary rate limit | Back off |
| 403 (neither) | Insufficient permission | Surface a scope error |
| 404 on a known-existing private repo | Also insufficient permission | GitHub returns 404 not 403 to avoid leaking existence |

That last row matters: **a 404 often means "no permission", not "not found"**.
Distinguish them in your UI or users will chase phantom bugs.

## Storage rules

- Never commit tokens. See [[Git - Undo Cookbook]] if you already did.
- OS keychain for desktop, encrypted at rest server-side
- Set expiry and rotate
- Log the *fact* of a token, never its value

---

## Related

- [[GitHub - Bots and Apps]]
- [[GitHub - Rate Limits]]
- [[Bridge - Auth SSH HTTPS and Tokens]]
- [[API - OAuth 2.0 Flows]]
- [[API - JWT]]
- [[API - Token Storage on Public Clients]]

## Sources

- <https://docs.github.com/en/authentication>
- <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens>
- <https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api>
