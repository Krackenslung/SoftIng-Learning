---
title: GitHub API Conventions
domain: bridge
section: B7
category: bridge
difficulty: intermediate
danger: medium
tags:
  - bridge
  - api/rest
  - github/api
commands: []endpoints: []

dashboard_relevant: true
mobile_relevant: true
related:
  - "[[API - REST vs GraphQL]]"
  - "[[API - Pagination Patterns]]"
  - "[[API - Rate Limiting Strategies]]"
  - "[[GitHub - REST API]]"
  - "[[GitHub - GraphQL API]]"
sources:
  - https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api
  - https://docs.github.com/en/graphql/overview/resource-limitations
  - https://docs.github.com/en/rest/about-the-rest-api/api-versions
updated: 2026-08-18
---

# GitHub API Conventions

> **The general pattern is X. GitHub does Y.**

Everything in [[Web-APIs]] describes how HTTP APIs behave in general. GitHub
follows most of it, and the handful of places where it does not are exactly the
places integrations break — usually silently, because the deviations return
success-shaped responses. This note is the diff.

## At a glance

| Generic behaviour | What GitHub does |
|---|---|
| GraphQL errors are still HTTP errors | **200 OK** with an `errors` array |
| 403 means "not allowed" | **404** for private resources you cannot see |
| One rate-limit bucket | Separate buckets for core, search and GraphQL |
| Rate limits count requests | GraphQL bills **node points**, not requests |
| `User-Agent` is polite | **Mandatory** — 403 without it |
| Versioning via URL or `Accept` | Date-based `X-GitHub-Api-Version` header |
| Paging until you run out | Search stops dead at **1,000 results** |

## GraphQL errors arrive as 200

```json
{
  "data": { "repository": null },
  "errors": [
    { "type": "NOT_FOUND", "message": "Could not resolve to a Repository" }
  ]
}
```

`res.ok` is `true`. Any generic HTTP error handling you own is bypassed, and
`data` can be **partially** populated — some fields resolved, others null beside
a matching entry in `errors`. A client that checks only the status code renders
missing data as legitimately absent.

```kotlin
val body = json.decodeFromString<GraphQlResponse<T>>(
    res.body?.string().orEmpty(),
)
if (!body.errors.isNullOrEmpty()) throw GraphQlException(body.errors)
```

Genuine transport failures still use status codes, and rate limiting in GraphQL
does return 403 or 502 rather than an `errors` entry — so you need both checks.

## 404 where you expect 403

Requesting a private repository you cannot see returns **404, not 403**, so that
the response does not confirm the repository exists. The practical consequence:
a 404 on a resource you are certain exists is almost always an authentication or
authorisation problem.

Work through it in this order:

1. Is the token being sent at all? A dropped `Authorization` header looks
   identical to a missing repository.
2. Does the token have the right scope or fine-grained permission?
3. For a SAML-enforced organisation, has the token been **authorised for that
   org**? An unauthorised token also fails as 404 — see
   [[Bridge - Auth SSH HTTPS and Tokens]].
4. Only then suspect the path.

## Three rate-limit buckets

| Bucket | Limit (authenticated) | Metered in |
|---|---|---|
| Core REST | 5,000/hour | Requests |
| Search | 30/minute | Requests |
| GraphQL | 5,000/hour | **Points** |

Exhausting search leaves core untouched, and vice versa — a "rate limited"
integration is often only limited in one bucket. `GET /rate_limit` reports all
of them and is itself free.

Conditional requests are the main lever: **a 304 costs no core quota**, which is
what makes ETag-aware polling viable at all. See [[API - Caching and ETags]].

## GraphQL bills by node points

A REST request costs one unit regardless of size. A GraphQL query costs a
computed score based on how many nodes it could return, charged whether or not
you read them:

```graphql
repositories(first: 100) { nodes { issues(first: 100) { nodes { title } } } }
```

That is 10,000 potential nodes from a single request. The lesson is the inverse
of the REST one: on REST, fetch bigger pages to make fewer requests; on GraphQL,
**request the smallest `first:` that works**, because size is the cost. See
[[API - REST vs GraphQL]].

## Mandatory `User-Agent`

```http
User-Agent: my-dev-dashboard/1.0 (+https://github.com/octocat/dashboard)
```

A request without it is rejected with 403. GitHub asks for a username or
application name so they can contact you if your client misbehaves — and in
practice, a descriptive one is what stops you being caught by a blanket block
during an incident. See [[API - Headers]].

## Date-based versioning

```http
X-GitHub-Api-Version: 2022-11-28
```

Breaking changes ship as new dated versions; omitting the header pins you to the
oldest supported version, not the newest. Set it explicitly so upgrades are a
deliberate one-line change rather than something that happens to you.

Media types (`Accept: application/vnd.github+json`) are a separate axis and
select the *representation* — raw, rendered, diff — not the API version.

## Search has a hard ceiling

The Search API returns at most **1,000 results**, whatever `page` says, and is
metered separately at 30 requests per minute. Paging past the ceiling returns
422. The fix is never deeper paging — partition the query instead (by date
range, by repository, by author) so no single search exceeds the cap.

Search results are also **eventually consistent**: a just-created issue may not
appear for some seconds. Never use search to confirm a write you just made; read
the resource directly.

## ⚠️ Gotchas

- ⚠️ **`res.ok` is not success for GraphQL.** Check `body.errors` on every
  response, and treat a partially filled `data` as a failure rather than as
  absent data.
- ⚠️ **A 404 usually means auth, not absence.** Chasing it as a wrong URL wastes
  the debugging session; check the token, scope and SAML authorisation first.
- ⚠️ **`GET /repos/{o}/{r}/issues` includes pull requests.** Every PR is an
  issue in GitHub's data model. Filter on the presence of `pull_request` in each
  item or your issue counts are inflated — a classic dashboard defect.
- ⚠️ **Do not page past 1,000 search results.** Partition the query; the
  ceiling is not negotiable.
- ⚠️ **Search is eventually consistent.** Confirming a write via search
  intermittently reports failure for something that succeeded.
- **Some resources are GraphQL-only** (Projects v2) and some are REST-only
  (parts of Actions). Check before committing an integration to one API.
- **`X-GitHub-Request-Id` belongs in every error log.** It is what support asks
  for, and it is unavailable after the fact if you did not record it.
- **Secondary rate limits are separate from the documented ones**, undocumented,
  and triggered by concurrency and rapid content creation rather than volume —
  see [[API - Rate Limiting Strategies]].

---

## Related

- [[API - REST vs GraphQL]]
- [[API - Pagination Patterns]]
- [[API - Rate Limiting Strategies]]
- [[GitHub - REST API]]
- [[GitHub - GraphQL API]]

## Sources

- <https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api>
- <https://docs.github.com/en/graphql/overview/resource-limitations>
- <https://docs.github.com/en/rest/about-the-rest-api/api-versions>
