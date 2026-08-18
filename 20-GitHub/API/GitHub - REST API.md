---
title: REST API
domain: github
section: 17
category: api
difficulty: intermediate
danger: low
tags:
  - github/api
  - github/rest
commands: []
endpoints:
  - GET /user/repos
  - GET /repos/{owner}/{repo}/pulls
  - GET /repos/{owner}/{repo}/issues
  - GET /notifications
dashboard_relevant: true
related:
  - "[[GitHub - GraphQL API]]"
  - "[[GitHub - Rate Limits]]"
  - "[[GitHub - Authentication]]"
  - "[[API - Caching and ETags]]"
  - "[[API - Pagination Patterns]]"
  - "[[API - Idempotency and Retries]]"
sources:
  - https://docs.github.com/en/rest
  - https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api
  - https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api
updated: 2026-08-14
---

# REST API

Base URL: `https://api.github.com`

## Pagination

```http
GET /repos/octocat/hello/pulls?state=open&per_page=100&page=2
```

- `per_page` max is **100** (some endpoints cap lower)
- **Do not construct page URLs yourself** — follow the `Link` header:

```
Link: <https://api.github.com/...?page=3>; rel="next",
      <https://api.github.com/...?page=9>; rel="last"
```

- Some newer endpoints are **cursor-based** (`?after=`) and have no `last`
- Stop when there is no `rel="next"`

```js
async function* paginate(url, headers) {
  while (url) {
    const res = await fetch(url, { headers });
    yield* await res.json();
    url = parseLink(res.headers.get("link"))?.next ?? null;
  }
}
```

## Conditional requests — the most important optimization

```http
If-None-Match: "abc123etag"
If-Modified-Since: Wed, 13 Aug 2026 10:00:00 GMT
```

A **`304 Not Modified` does not count against your rate limit.** For a polling
dashboard this is the difference between viable and not. Store the `ETag` per
endpoint and always send it back.

## Response headers to keep

| Header | Use |
|---|---|
| `etag` | Conditional requests |
| `x-ratelimit-remaining` / `-reset` / `-used` | Budgeting |
| `link` | Pagination |
| `retry-after` | Secondary limit backoff |
| `x-poll-interval` | Minimum poll gap (notifications) |
| `x-github-request-id` | Quote this in support reports |

## Endpoints a dev dashboard actually needs

```http
GET /user                                          identity
GET /user/repos?affiliation=owner,collaborator     repo list
GET /repos/{o}/{r}/pulls?state=open                PRs
GET /repos/{o}/{r}/pulls/{n}/reviews               review state
GET /repos/{o}/{r}/issues?state=open               issues (⚠ includes PRs)
GET /repos/{o}/{r}/commits?sha={branch}            commits
GET /repos/{o}/{r}/commits/{sha}/check-runs        CI status
GET /repos/{o}/{r}/actions/runs?per_page=10        workflow runs
GET /notifications?participating=true              inbox
GET /search/issues?q=review-requested:@me+is:open  my review queue
GET /rate_limit                                    budget (free — no quota cost)
```

## Practices that matter

- Reuse HTTP connections; set a sane timeout
- Retry `5xx` and `429` with exponential backoff + jitter — never a tight loop
- Serialize writes to the same resource; concurrent mutations trip secondary limits
- Prefer webhooks over polling where you control a server
  ([[GitHub - Webhooks]])
- If one screen needs data from 5 endpoints, that is the signal to switch to
  [[GitHub - GraphQL API]]

---

## Related

- [[GitHub - GraphQL API]]
- [[GitHub - Rate Limits]]
- [[GitHub - Authentication]]
- [[API - Caching and ETags]]
- [[API - Pagination Patterns]]
- [[API - Idempotency and Retries]]

## Sources

- <https://docs.github.com/en/rest>
- <https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api>
- <https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api>
