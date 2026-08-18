---
title: Web APIs
domain: api
type: hub
tags:
  - hub
  - api
updated: 2026-08-18
cssclasses:
  - hub
---

# Web APIs

The protocol layer underneath [[GitHub]]. These notes cover HTTP and API
mechanics that are true of any provider — status codes, ETags, cursors, OAuth,
JWTs, HMAC — so that the GitHub notes can stop assuming them. Where GitHub
deviates from the generic behaviour described here, that divergence lives in
[[Bridge - GitHub API Conventions]].

> [!tip] Reading order
> Start with **Fundamentals** in section order; they build on each other. Auth,
> Patterns and Data-Formats are lookup material and can be read in any order.

## Fundamentals

- [[API - HTTP Methods and Status Codes]] — safe vs idempotent, the codes worth
  memorising
- [[API - Headers]] — the metadata channel: negotiation, auth, `Link`, `Vary`
- [[API - Caching and ETags]] — freshness vs validation, conditional requests
- [[API - Pagination Patterns]] — offset drift, cursors, following `Link`
- [[API - Idempotency and Retries]] — idempotency keys, backoff with jitter

## Auth

- [[API - OAuth 2.0 Flows]] — authorization code + PKCE, scopes, deprecated
  grants
- [[API - JWT]] — structure, signing, `alg: none`, claim validation
- [[API - HMAC Signatures]] — webhook verification, constant-time comparison
- [[API - OIDC and Federated Identity]] — identity on top of OAuth, keyless CI

## Patterns

- [[API - REST vs GraphQL]] — over-fetching, round trips, cost models
- [[API - Webhooks vs Polling]] — push vs pull, delivery guarantees
- [[API - Rate Limiting Strategies]] — token bucket, leaky bucket, sliding window

## Data formats

- [[API - JSON YAML and TOML]] — where each fits, and YAML's real footguns

## Where this meets GitHub

- [[Bridge - GitHub API Conventions]] — GraphQL 200-with-errors, 404-not-403,
  search ceilings, node points
- [[GitHub - REST API]] · [[GitHub - GraphQL API]] · [[GitHub - Webhooks]] ·
  [[GitHub - Rate Limits]] · [[GitHub - Authentication]]

---

## All Web API notes

```dataview
TABLE category AS Category, difficulty AS Level, danger AS Risk
FROM "40-Web-APIs"
WHERE type != "hub"
SORT section ASC
```

## Dashboard-relevant notes

```dataview
TABLE category AS Category, difficulty AS Level
FROM "40-Web-APIs"
WHERE dashboard_relevant = true
SORT section ASC
```
