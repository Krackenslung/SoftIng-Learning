---
title: Bots and Apps
domain: github
section: 15
category: automation
difficulty: advanced
danger: medium
tags:
  - github/apps
  - github/automation
commands: []
endpoints:
  - POST /app/installations/{id}/access_tokens
  - GET /app/installations
dashboard_relevant: true
related:
  - "[[GitHub - Authentication]]"
  - "[[GitHub - Webhooks]]"
  - "[[GitHub - Rate Limits]]"
  - "[[API - JWT]]"
  - "[[API - OAuth 2.0 Flows]]"
sources:
  - https://docs.github.com/en/apps
  - https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/authenticating-as-a-github-app-installation
  - https://docs.github.com/en/code-security/dependabot
updated: 2026-08-14
---

# Bots and Apps

## GitHub App vs. OAuth App vs. PAT

| | GitHub App | OAuth App | PAT |
|---|---|---|---|
| Acts as | Itself, or a user | Always a user | A user |
| Permissions | Fine-grained, per-resource | Broad scopes | Scopes |
| Install scope | Chosen repos | Whole account | Whole account |
| Token life | 1 hour (installation) | Long-lived | Long-lived |
| Rate limit | Scales with install size | 5,000/hr | 5,000/hr |
| Webhooks | Built in | Manual | N/A |

**For anything multi-user or production, build a GitHub App.** PATs are fine for
personal scripts and prototypes.

## Installation token flow

```
1. Sign a JWT with your app's private key    (exp ≤ 10 min, iss = app id)
2. GET  /app/installations                    → find the installation id
3. POST /app/installations/{id}/access_tokens → 1-hour installation token
4. Use that token as: Authorization: Bearer <token>
5. Refresh before expiry
```

Cache installation tokens for their full hour. Re-minting on every request is a
fast route to a secondary rate limit.

## Common bots

- **Dependabot** — `.github/dependabot.yml`; version + security updates
- **Renovate** — third party, far more configurable, monorepo-aware
- **Mergify / Kodiak** — merge queue and rule automation

⚠️ Dependabot PRs run with a **restricted** `GITHUB_TOKEN` and cannot see repo
secrets by default. Use `secrets: DEPENDABOT_*` or a `pull_request_target`
workflow written very carefully.

## Identifying bot activity

Bot accounts have `type: "Bot"` on the user object and logins ending in
`[bot]` (e.g. `dependabot[bot]`). A dashboard should let the user filter these
out — otherwise bot PRs drown the signal.

---

## Related

- [[GitHub - Authentication]]
- [[GitHub - Webhooks]]
- [[GitHub - Rate Limits]]
- [[API - JWT]]
- [[API - OAuth 2.0 Flows]]

## Sources

- <https://docs.github.com/en/apps>
- <https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/authenticating-as-a-github-app-installation>
- <https://docs.github.com/en/code-security/dependabot>
