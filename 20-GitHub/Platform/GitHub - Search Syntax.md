---
title: Search Syntax
domain: github
section: 04
category: platform
difficulty: intermediate
danger: none
tags:
  - github/search
commands: []
endpoints:
  - GET /search/issues
  - GET /search/repositories
  - GET /search/code
dashboard_relevant: true
related:
  - "[[Git - Searching History]]"
  - "[[GitHub - Issues]]"
  - "[[GitHub - Pull Requests]]"
  - "[[API - Pagination Patterns]]"
  - "[[Bridge - GitHub API Conventions]]"
sources:
  - https://docs.github.com/en/search-github/searching-on-github
  - https://docs.github.com/en/rest/search/search
updated: 2026-08-14
---

# Search Syntax

GitHub search qualifiers work identically in the UI and the search API — learning
them once pays off twice.

## Core qualifiers

```
is:pr is:open                      type filter
is:issue is:closed
author:octocat
assignee:@me
mentions:@me
review-requested:@me               ← the "what needs me" query
reviewed-by:octocat
org:my-org  repo:owner/name  user:octocat
label:bug label:"help wanted"
milestone:"v2.0"
state:open
draft:true
merged:>2026-01-01
created:>=2026-06-01
updated:<2026-08-01
closed:2026-01-01..2026-06-30
comments:>10
interactions:>50
no:label  no:assignee  no:milestone
sort:updated-desc
archived:false
```

## Boolean and ranges

- `AND`, `OR`, `NOT` (uppercase) — supported in issue/PR search
- `-` prefix negates: `-label:wontfix`
- Ranges: `>`, `>=`, `<`, `<=`, `n..m`, `*..m`, `n..*`
- Quote multi-word values: `label:"good first issue"`

## Repository search

```
stars:>1000 language:typescript topic:cli
pushed:>2026-01-01 archived:false
size:<10000 license:mit is:public
```

## Code search

The rewritten code search supports regex (`/pattern/`), `path:`, `symbol:`,
`content:`, and `language:` qualifiers. Note it indexes default branches of
non-archived repos, so it is **not** a substitute for [[Git - Searching History]]
when you need historical content.

## Gotchas for integrations

- Search API has its **own rate limit**: 30 req/min authenticated, 10
  unauthenticated — completely separate from the core limit. See
  [[GitHub - Rate Limits]].
- Search results cap at **1,000 items** regardless of pagination.
- Results are eventually consistent — a just-opened PR may not appear instantly.
- For exact, complete, real-time data, prefer the list endpoints or
  [[GitHub - GraphQL API]] over search.

---

## Related

- [[Git - Searching History]]
- [[GitHub - Issues]]
- [[GitHub - Pull Requests]]
- [[API - Pagination Patterns]]
- [[Bridge - GitHub API Conventions]]

## Sources

- <https://docs.github.com/en/search-github/searching-on-github>
- <https://docs.github.com/en/rest/search/search>
