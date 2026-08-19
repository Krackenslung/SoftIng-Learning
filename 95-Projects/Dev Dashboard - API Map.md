---
title: Dev Dashboard — API Map
domain: project
type: spec
tags:
  - project/dashboard
related:
  - "[[GitHub - REST API]]"
  - "[[GitHub - GraphQL API]]"
  - "[[GitHub - Authentication]]"
  - "[[API - Caching and ETags]]"
  - "[[API - Pagination Patterns]]"
  - "[[Bridge - GitHub API Conventions]]"
  - "[[API - Client-Only vs Backend Architectures]]"
  - "[[Android - Networking]]"
  - "[[Android - Keystore and Secure Storage]]"
  - "[[Bridge - GitHub API on Android]]"
updated: 2026-08-14
---

# Dev Dashboard — API Map

Which endpoint feeds which view, and what it costs.

## Per sub-tab

| Sub-tab | Call | Cost / cycle |
|---|---|---|
| Repositories | `GET /user/repos?per_page=100` | 1 per 100 repos |
| Pull Requests | `GET /repos/{o}/{r}/pulls?state=open` | 1 per repo ⚠️ |
| PR review state | GraphQL `reviewDecision` | folded into 1 query |
| PR checks | `GET /commits/{sha}/check-runs` | 1 per PR ⚠️⚠️ |
| Issues | `GET /repos/{o}/{r}/issues?state=open` | 1 per repo |
| Actions | `GET /actions/runs?per_page=10` | 1 per repo |
| Notifications | `GET /notifications?participating=true` | 1 total ✅ |
| Budget check | `GET /rate_limit` | free |

The ⚠️ rows scale with repo and PR count. At 40 repos with 5 open PRs each,
naive REST costs ~240 requests per cycle. At 12 cycles/hour that's 2,880 of a
5,000 budget — before anything else.

## Therefore: one GraphQL query replaces most of it

```graphql
query {
  rateLimit { cost remaining }
  search(query: "is:pr is:open involves:@me", type: ISSUE, first: 50) {
    nodes { ... on PullRequest {
      number title url isDraft createdAt updatedAt
      repository { nameWithOwner }
      author { login }
      reviewDecision
      mergeable
      reviewRequests(first: 10) { nodes { requestedReviewer {
        ... on User { login } } } }
      commits(last: 1) { nodes { commit {
        statusCheckRollup { state } } } }
    }}
  }
}
```

One call. `reviewDecision` and `statusCheckRollup` are the two fields that
collapse the ⚠️⚠️ rows above. See [[GitHub - GraphQL API]].

## Auth

Fine-grained PAT, read-only. Required permissions — see
[[GitHub - Authentication]]:

```
Metadata: read          (mandatory)
Contents: read
Pull requests: read
Issues: read
Actions: read
Checks: read
Projects: read          (only if surfacing project fields)
```

User-level: `Notifications: read`.

Ship as a GitHub App if this ever goes multi-user — installation tokens get
higher, scaling limits and per-repo install scoping.

## Caching rules

Nothing here is invalidated by a push. With no backend there is no webhook to
receive, so every entry is revalidated by a poll — see
[[API - Client-Only vs Backend Architectures]].

| Data | Revalidate after, in foreground | Refreshed by |
|---|---|---|
| Repo list | 1 h | Manual refresh |
| PR list | 60 s | App opened, pull-to-refresh, background sync |
| Checks | 30 s | App opened, pull-to-refresh, background sync |
| Notifications | `X-Poll-Interval` | `PATCH` mark-read, pull-to-refresh |
| Issues | 5 min | App opened, pull-to-refresh, background sync |

⚠️ Those intervals apply while the app is open. Background sync cannot beat the
`WorkManager` floor of 15 minutes, and Doze pushes it further out — see
[[Android - WorkManager]] and [[Android - Background Limits and Doze]].

Always send stored `ETag`s — a `304` is free. On Android, OkHttp resolves it
into a cached `200`, so quota must be measured from `networkResponse` rather
than `response.code` — see [[Bridge - GitHub API on Android]] and
[[GitHub - REST API]].
