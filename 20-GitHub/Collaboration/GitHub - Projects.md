---
title: Projects
domain: github
section: 10
category: collaboration
difficulty: intermediate
danger: none
tags:
  - github/projects
  - github/planning
commands: []
endpoints:
  - GraphQL: organization.projectV2
  - GraphQL: projectV2.items
dashboard_relevant: true
related:
  - "[[GitHub - Issues]]"
  - "[[GitHub - GraphQL API]]"
  - "[[GitHub - Bots and Apps]]"
sources:
  - https://docs.github.com/en/issues/planning-and-tracking-with-projects
  - https://docs.github.com/en/graphql/reference/objects#projectv2
updated: 2026-08-14
---

# Projects

Projects (v2) is a flexible spreadsheet/board over issues, PRs, and standalone
draft items.

## Model

```
Project
├── Fields   (Text, Number, Date, Single-select, Iteration)
├── Items    (Issue | PullRequest | DraftIssue)
│   └── FieldValues
└── Views    (Table | Board | Roadmap)
```

Fields are **project-scoped**, not repo-scoped — the same issue can carry
different field values in two projects.

## Built-in automation

- Auto-add items matching a filter
- Auto-archive
- Item closed → set Status to Done
- Custom workflows via [[GitHub - Actions]] and the `actions/add-to-project` action

## ⚠️ REST API does not cover Projects v2

**Projects v2 is GraphQL-only.** The old REST `/projects` endpoints refer to the
deprecated classic Projects. Any integration must use
[[GitHub - GraphQL API]].

Minimal query shape:

```graphql
query($org: String!, $number: Int!) {
  organization(login: $org) {
    projectV2(number: $number) {
      items(first: 50) {
        pageInfo { hasNextPage endCursor }
        nodes {
          content {
            ... on Issue { number title state url }
            ... on PullRequest { number title state isDraft url }
          }
          fieldValues(first: 20) {
            nodes {
              ... on ProjectV2ItemFieldSingleSelectValue {
                name field { ... on ProjectV2SingleSelectField { name } }
              }
            }
          }
        }
      }
    }
  }
}
```

Note the double indirection on field values — this is the part everyone gets
wrong first. Field values are a union type and each variant needs its own
inline fragment.

Token needs the `project` scope (classic PAT) or **Projects: read** permission
(fine-grained).

---

## Related

- [[GitHub - Issues]]
- [[GitHub - GraphQL API]]
- [[GitHub - Bots and Apps]]

## Sources

- <https://docs.github.com/en/issues/planning-and-tracking-with-projects>
- <https://docs.github.com/en/graphql/reference/objects#projectv2>
