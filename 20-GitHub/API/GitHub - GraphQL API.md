---
title: GraphQL API
domain: github
section: 18
category: api
difficulty: advanced
danger: low
tags:
  - github/api
  - github/graphql
commands: []
endpoints:
  - POST https://api.github.com/graphql
dashboard_relevant: true
related:
  - "[[GitHub - REST API]]"
  - "[[GitHub - Projects]]"
  - "[[GitHub - Rate Limits]]"
  - "[[API - REST vs GraphQL]]"
  - "[[API - Pagination Patterns]]"
  - "[[API - Caching and ETags]]"
sources:
  - https://docs.github.com/en/graphql
  - https://docs.github.com/en/graphql/overview/resource-limitations
  - https://docs.github.com/en/graphql/guides/forming-calls-with-graphql
updated: 2026-08-14
---

# GraphQL API

Single endpoint: `POST https://api.github.com/graphql`. Always authenticated —
there is no anonymous access.

## When GraphQL wins

- One screen needs fields from several REST endpoints (N+1 elimination)
- You need **Projects v2**, **Discussions**, or **sub-issues** — GraphQL only
- You want to fetch exactly 6 fields instead of a 40 KB REST object
- You need review state, checks, and PR metadata together

## When REST wins

- Simple single-resource reads
- Conditional requests / ETags (GraphQL has no `304`)
- Endpoints with no GraphQL equivalent
- Easier debugging and caching

Most real integrations use **both**. That is normal, not a design failure.

## The dashboard query

```graphql
query($login: String!) {
  viewer { login avatarUrl }
  search(query: "is:pr is:open review-requested:@me",
         type: ISSUE, first: 20) {
    nodes {
      ... on PullRequest {
        number title url isDraft createdAt
        repository { nameWithOwner }
        author { login }
        reviewDecision
        mergeable
        commits(last: 1) {
          nodes { commit {
            statusCheckRollup { state }
          }}
        }
      }
    }
  }
}
```

`reviewDecision` and `statusCheckRollup.state` are the two fields that make
GraphQL worth it — each would otherwise cost an extra REST call *per PR*.

## Pagination

```graphql
pullRequests(first: 50, after: $cursor) {
  pageInfo { hasNextPage endCursor }
  nodes { number title }
}
```

Cursor-based only. Loop on `hasNextPage`, pass `endCursor` as `after`.

## Rate limiting is different

GraphQL uses a **point budget: 5,000 points/hour**, not request count. Points
are computed from the number of nodes a query could return, not what it does
return.

```graphql
query { rateLimit { limit cost remaining resetAt } }
```

Include `rateLimit` in every query during development. `first: 100` nested
inside `first: 100` is a 10,000-node query and will be rejected outright —
GraphQL caps a single call at 500,000 nodes.

## Practical notes

- Use the **Explorer** (`/graphql/explorer` on docs) — the schema is huge and
  autocomplete is the only sane way to navigate it
- Node IDs are opaque, globally unique, and stable — good primary keys for a
  local cache
- Mutations require an `input` object and often a node ID you must fetch first
- Errors return **HTTP 200** with an `errors` array. Checking `res.ok` is not
  enough — this catches everyone once.

---

## Related

- [[GitHub - REST API]]
- [[GitHub - Projects]]
- [[GitHub - Rate Limits]]
- [[API - REST vs GraphQL]]
- [[API - Pagination Patterns]]
- [[API - Caching and ETags]]

## Sources

- <https://docs.github.com/en/graphql>
- <https://docs.github.com/en/graphql/overview/resource-limitations>
- <https://docs.github.com/en/graphql/guides/forming-calls-with-graphql>
