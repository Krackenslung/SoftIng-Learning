---
title: GitHub
domain: github
type: hub
tags:
  - hub
  - github
updated: 2026-08-14
cssclasses:
  - hub
---

# GitHub

The platform layer on top of [[Git]]. Start with [[GitHub - GitHub vs Git]] —
knowing which side of that line a concept sits on determines whether you can read
it from a local clone or must call the API.

## Platform
- [[GitHub - GitHub vs Git]] — what the platform actually adds
- [[GitHub - Accounts Orgs and Teams]] — permission model
- [[GitHub - Repositories]] — settings, visibility, special files
- [[GitHub - Search Syntax]] — qualifiers, used by UI and API alike
- [[GitHub - Notifications]] — subscriptions, reasons, the inbox API

## Collaboration
- [[GitHub - Issues]] — labels, milestones, forms
- [[GitHub - Pull Requests]] — lifecycle, state fields, merge methods
- [[GitHub - Code Review]] — reviews, comments, CODEOWNERS
- [[GitHub - Branch Protection and Rulesets]] — server-side enforcement
- [[GitHub - Projects]] — boards, custom fields (GraphQL only)
- [[GitHub - Discussions and Wikis]]

## Automation
- [[GitHub - Actions]] — workflows, triggers, status vs conclusion
- [[GitHub - Actions Advanced]] — matrices, reusables, caching, OIDC
- [[GitHub - Releases and Packages]]
- [[GitHub - Bots and Apps]] — Apps vs OAuth vs PAT, Dependabot

## 🔌 API — build against this
- [[GitHub - Authentication]] — token types and permission mapping
- [[GitHub - REST API]] — pagination, ETags, endpoint list
- [[GitHub - GraphQL API]] — when it beats REST, point budget
- [[GitHub - Webhooks]] — signature verification, delivery guarantees
- [[GitHub - Rate Limits]] — the constraint that shapes the architecture
- [[Web-APIs]] — the generic HTTP layer: ETags, cursors, OAuth, JWT, HMAC
- [[Bridge - GitHub API Conventions]] — where GitHub deviates from generic REST
- [[Bridge - GitHub API on Android]] — and how it changes again on a phone
- [[Android]] — the client that consumes all of it

## Security
- [[GitHub - Code and Secret Scanning]]
- [[GitHub - Advisories and Supply Chain]]

## Extras
- [[GitHub - CLI]] — `gh`, including `gh api`
- [[GitHub - Flavored Markdown]] — GFM vs Obsidian differences
- [[GitHub - Gists Pages and Codespaces]]

---

## Dashboard-relevant notes

```dataview
TABLE category AS Area, endpoints AS Endpoints
FROM "20-GitHub"
WHERE dashboard_relevant = true
SORT section ASC
```

## All GitHub notes

```dataview
TABLE category AS Category, difficulty AS Level
FROM "20-GitHub"
WHERE type != "hub"
SORT section ASC
```
