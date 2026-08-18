---
title: Rate Limits
domain: github
section: 20
category: api
difficulty: intermediate
danger: high
tags:
  - github/api
  - github/limits
commands: []
endpoints:
  - GET /rate_limit
dashboard_relevant: true
related:
  - "[[GitHub - REST API]]"
  - "[[GitHub - GraphQL API]]"
  - "[[GitHub - Webhooks]]"
  - "[[GitHub - Authentication]]"
  - "[[API - Rate Limiting Strategies]]"
  - "[[API - Caching and ETags]]"
  - "[[API - Pagination Patterns]]"
sources:
  - https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api
  - https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/rate-limits-for-github-apps
  - https://docs.github.com/en/graphql/overview/resource-limitations
updated: 2026-08-14
---

# Rate Limits

The constraint that shapes every GitHub integration's architecture.

## Primary limits (REST)

| Auth method | Requests / hour |
|---|---|
| Unauthenticated (by IP) | **60** |
| Personal access token | **5,000** |
| OAuth app | 5,000 per app |
| GitHub App installation | **5,000 minimum**, scaling with install size |
| GitHub App on Enterprise Cloud org | 15,000 |
| `GITHUB_TOKEN` in Actions | **1,000 per repository** |

GitHub App installations scale up: larger installations earn additional quota
per user and per repository beyond a threshold, up to a ceiling well above the
5,000 baseline. This is a concrete reason to ship a GitHub App rather than
distribute a PAT-based tool.

## Separate buckets

These do **not** share the core quota:

| Bucket | Limit |
|---|---|
| Search API | 30/min authenticated, 10/min unauthenticated |
| GraphQL | 5,000 **points**/hour |
| Git LFS | 300/min unauth, 3,000/min auth |

## Secondary rate limits

Undocumented-by-design behavioural limits, independent of the primary budget:

- Too many **concurrent** requests (keep it ≲ 100 concurrent, realistically far fewer)
- Too many requests per minute to a single endpoint
- Excessive content-creating requests (comments, issues)
- Too much CPU consumed by expensive queries

Signalled by `403` or `429` **with a `retry-after` header**. Honour it exactly.

## Checking your budget

```http
GET /rate_limit      ← does not itself consume quota
```

Returns per-bucket `limit`, `remaining`, `reset`, `used` for `core`, `search`,
`graphql`, `integration_manifest`, `code_search`, and more.

## Response headers

```
x-ratelimit-limit: 5000
x-ratelimit-remaining: 4987
x-ratelimit-used: 13
x-ratelimit-reset: 1755180000     ← UTC epoch seconds
x-ratelimit-resource: core
```

## Survival strategy, in priority order

1. **Webhooks over polling** — zero quota ([[GitHub - Webhooks]])
2. **ETags / conditional requests** — a `304` is free ([[GitHub - REST API]])
3. **GraphQL** to collapse N calls into 1 ([[GitHub - GraphQL API]])
4. **`per_page=100`** — never paginate in 30s
5. **Cache aggressively**; treat GitHub as the source of truth, not the datastore
6. **Back off on 403/429** with `retry-after`, then exponential + jitter
7. **Never retry in a tight loop** — that is how you earn a longer block
8. **Ship as a GitHub App** for higher, scaling limits

## Budget sketch

A 5,000/hr budget, polling every 5 minutes = 12 cycles/hr = **~416 requests per
cycle**. That sounds generous until you do one request per PR per repo across 40
repos. Conditional requests and GraphQL are not optimizations here — they are the
design.

---

## Related

- [[GitHub - REST API]]
- [[GitHub - GraphQL API]]
- [[GitHub - Webhooks]]
- [[GitHub - Authentication]]
- [[API - Rate Limiting Strategies]]
- [[API - Caching and ETags]]
- [[API - Pagination Patterns]]

## Sources

- <https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api>
- <https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/rate-limits-for-github-apps>
- <https://docs.github.com/en/graphql/overview/resource-limitations>
