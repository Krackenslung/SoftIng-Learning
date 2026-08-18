---
title: REST vs GraphQL
domain: api
section: "50"
category: patterns
difficulty: intermediate
danger: none
tags:
  - api/rest
  - api/graphql
commands: []endpoints: []

dashboard_relevant: true
mobile_relevant: true
related:
  - "[[API - Pagination Patterns]]"
  - "[[API - Rate Limiting Strategies]]"
  - "[[Bridge - GitHub API Conventions]]"
  - "[[GitHub - GraphQL API]]"
  - "[[GitHub - REST API]]"
  - "[[API - JSON YAML and TOML]]"
sources:
  - https://graphql.org/learn/
  - https://datatracker.ietf.org/doc/html/rfc9110
  - https://docs.github.com/en/graphql/overview/about-the-graphql-api
updated: 2026-08-18
---

# REST vs GraphQL

REST models an API as a set of **resources** you fetch by URL; GraphQL models it
as a **graph** you query with a shape. The practical difference is who decides
what comes back — the server, once, for every caller, or the client, per
request. That single choice determines how the API is cached, rate limited and
debugged, which is why the trade-off is architectural rather than stylistic.

## Side by side

| | REST | GraphQL |
|---|---|---|
| Endpoints | Many, one per resource | One (`POST /graphql`) |
| Response shape | Fixed by the server | Chosen by the client |
| Over-fetching | Common — you get every field | Eliminated by design |
| Under-fetching | Common — N round trips | One request for a whole tree |
| HTTP caching | Free (`ETag`, `304`) | **Effectively unavailable** |
| Error signalling | Status codes | 200 + an `errors` array |
| Cost model | Requests per hour | Query complexity points |
| Discoverability | Docs, `Link`, OpenAPI | Introspection, typed schema |
| Debugging | `curl`, browser, proxy logs | Needs a client that speaks GraphQL |

## The problem GraphQL solves

Building one dashboard screen from REST often means a request fan-out:

```http
GET /repos/{o}/{r}/pulls?state=open      then, for each PR:
GET /repos/{o}/{r}/pulls/{n}/reviews
GET /repos/{o}/{r}/commits/{sha}/check-runs
```

Twenty open pull requests become 41 requests, and each returns a large object
when you wanted four fields. GraphQL collapses that into one round trip:

```graphql
query($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    pullRequests(first: 20, states: OPEN) {
      nodes {
        number
        title
        reviewDecision
        commits(last: 1) {
          nodes { commit { statusCheckRollup { state } } }
        }
      }
    }
  }
}
```

**If one screen needs five REST endpoints, that is the signal to switch.**

## What you give up

**HTTP caching.** Every GraphQL request is a `POST` to the same URL with a
different body, so `ETag` and `304` do not apply, and none of
[[API - Caching and ETags]] is available to you. Caching moves into the client
(a normalised store keyed by object ID) and into the server. On an API where
304s are free, this can make a polling REST client cheaper than the "more
efficient" GraphQL one — measure before assuming.

**Status codes.** A GraphQL error usually arrives as `200 OK` with an `errors`
array, so `res.ok` tells you nothing and any generic HTTP error handling you own
is bypassed. See [[Bridge - GitHub API Conventions]].

**A simple cost model.** Rate limiting by request count is meaningless when one
request can traverse the entire graph, so GraphQL APIs bill by computed
complexity instead — see [[API - Rate Limiting Strategies]].

## Choosing

| Situation | Pick |
|---|---|
| Fetching one resource by ID | REST |
| Polling for change on a budget | REST — 304s are free |
| Assembling one view from many resources | GraphQL |
| Only some fields, from deeply nested data | GraphQL |
| Uploads, downloads, streaming | REST |
| Public API for unknown clients | REST — cacheable, debuggable |
| Field only exposed on one of them | Whichever has it |

These are not exclusive. A dashboard reasonably uses GraphQL for its main view
and REST for everything else, which is how most GitHub integrations end up.

## ⚠️ Gotchas

- ⚠️ **`res.ok` does not mean the query succeeded.** GraphQL returns 200 with
  `errors` populated, and `data` can be **partially** filled: some fields
  resolved, others null. Code that checks only the status code silently renders
  missing data as absent rather than failed. Always inspect `errors`.
- ⚠️ **A nested query can cost far more than it looks.** `first: 100` inside
  `first: 100` is 10,000 nodes, and the cost is charged whether or not you read
  them. Deeply nested pagination is the usual way an integration exhausts its
  budget in one call.
- **Introspection is a production decision.** It powers tooling, and it also
  publishes your complete schema. Public APIs enable it; internal ones often do
  not.
- **Schema parity is never complete.** GitHub Projects v2 is GraphQL-only, while
  parts of the Actions surface are REST-only. Check before committing to one.
- **A GraphQL `POST` is not idempotent to HTTP**, even for a pure read. Proxies,
  retries and browser caches all treat it as a write — see
  [[API - Idempotency and Retries]].

---

## Related

- [[API - Pagination Patterns]]
- [[API - Rate Limiting Strategies]]
- [[Bridge - GitHub API Conventions]]
- [[GitHub - GraphQL API]]
- [[GitHub - REST API]]
- [[API - JSON YAML and TOML]]

## Sources

- <https://graphql.org/learn/>
- <https://datatracker.ietf.org/doc/html/rfc9110>
- <https://docs.github.com/en/graphql/overview/about-the-graphql-api>
