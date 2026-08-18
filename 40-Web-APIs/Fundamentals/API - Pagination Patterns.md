---
title: Pagination Patterns
domain: api
section: "44"
category: fundamentals
difficulty: intermediate
danger: low
tags:
  - api/http
  - api/pagination
commands: []
dashboard_relevant: true
related:
  - "[[API - Headers]]"
  - "[[API - REST vs GraphQL]]"
  - "[[GitHub - REST API]]"
  - "[[GitHub - GraphQL API]]"
  - "[[Bridge - GitHub API Conventions]]"
sources:
  - https://www.rfc-editor.org/rfc/rfc8288.html
  - https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api
  - https://graphql.org/learn/pagination/
updated: 2026-08-18
---

# Pagination Patterns

No API returns an unbounded collection, so every collection endpoint has a
paging scheme — and the scheme chosen determines whether iterating a list that
is being written to concurrently gives you a correct answer. The three schemes
in common use differ mainly in how badly they behave under concurrent writes.

## The three schemes

| Scheme | Request | Stable under writes | Can jump to page N | Cost at depth |
|---|---|---|---|---|
| Offset / limit | `?page=3&per_page=100` | **no** | yes | grows linearly |
| Cursor / keyset | `?after=Y3Vyc29yOjEwMA` | yes | no | constant |
| `Link` header | follow `rel="next"` | depends on underlying scheme | no | — |

`Link` is not a third algorithm so much as a way of *hiding* which of the other
two is in use, which is exactly why you should follow it rather than construct
URLs.

## Offset and the drift problem

Offset paging asks "skip 100 rows, give me the next 100". If the collection
changes between requests, the window slides underneath you:

```text
Page 1 (offset 0)   [ A B C D E ]
        <- item Z is inserted at the front ->
Page 2 (offset 5)   [ E F G H I ]
                      ^ E returned twice, and nothing was lost
```

An **insert** before your cursor causes duplicates; a **delete** causes items to
be skipped entirely — and a skipped item is invisible. You do not get an error,
you get a quietly incomplete result. For a dashboard that reconciles state, a
silently missing pull request is worse than a crash.

Offset also degrades: `OFFSET 100000` typically makes the database walk and
discard 100,000 rows on every request.

## Cursor paging

The cursor encodes "where I stopped" in terms of the sort key, not a count:

```http
GET /repos/octocat/hello/issues?per_page=100&after=Y3Vyc29yOjEwMA
```

Because the server resumes from a key rather than a position, inserts and
deletes elsewhere in the collection do not shift the window. The trade-off is
that you cannot jump to an arbitrary page, and usually cannot get a total count.

Cursors are **opaque**. They frequently base64-encode an internal key; decoding
one and constructing your own is unsupported and will break.

## Following the `Link` header

```http
Link: <https://api.github.com/user/repos?page=3>; rel="next",
      <https://api.github.com/user/repos?page=9>; rel="last"
```

`rel` values are `next`, `prev`, `first`, `last`. Cursor-based endpoints emit
`next` but no `last`, since the total is unknown.

```js
async function* paginate(url, headers) {
  while (url) {
    const res = await fetch(url, { headers });
    if (!res.ok) throw new HttpError(res.status, await res.text());
    yield* await res.json();
    url = parseLink(res.headers.get("link"))?.next ?? null;
  }
}
```

Terminate on the **absence of `rel="next"`**, never on a short page — some APIs
legitimately return fewer items than `per_page` in the middle of a result set
after post-filtering.

## GraphQL connections

GraphQL standardises cursor paging as the Connection pattern:

```graphql
query {
  repository(owner: "octocat", name: "hello") {
    pullRequests(first: 100, after: $cursor) {
      pageInfo { hasNextPage endCursor }
      nodes { number title }
    }
  }
}
```

`pageInfo.hasNextPage` is the loop condition and `endCursor` feeds the next
`after`. Note that nested connections multiply the cost budget rather than the
request count — see [[API - REST vs GraphQL]] and [[GitHub - GraphQL API]].

## ⚠️ Gotchas

- ⚠️ **Offset paging over a live collection loses items.** If completeness
  matters, use cursors, or sort by an immutable key (`created_at`, `id`) and
  page by that. Sorting by `updated_at` while things are being updated is the
  worst case of all: an item can be pushed ahead of your cursor repeatedly and
  never appear.
- ⚠️ **Do not build page URLs by hand.** Endpoints migrate from offset to cursor
  without notice; a client that increments `?page=` breaks silently on the day
  it happens, usually by looping forever or stopping at page 1.
- ⚠️ **An unbounded pagination loop is a runaway.** Always cap total pages and
  total items. A malformed `next` that points at itself will otherwise burn an
  entire rate-limit budget in seconds — see [[API - Rate Limiting Strategies]].
- **`per_page` caps are per-endpoint.** 100 is a common maximum but not
  universal, and asking for more is usually clamped silently rather than
  rejected.
- **Deep paging is often hard-capped.** GitHub's Search API stops at 1,000
  results no matter what `page` says; narrow the query instead of paging past
  the ceiling.
- **Totals are estimates when they exist at all.** Cursor APIs usually omit
  them, and search totals are frequently approximate.

---

## Related

- [[API - Headers]]
- [[API - REST vs GraphQL]]
- [[GitHub - REST API]]
- [[GitHub - GraphQL API]]
- [[Bridge - GitHub API Conventions]]

## Sources

- <https://www.rfc-editor.org/rfc/rfc8288.html>
- <https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api>
- <https://graphql.org/learn/pagination/>
