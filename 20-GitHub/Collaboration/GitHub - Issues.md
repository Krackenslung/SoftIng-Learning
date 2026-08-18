---
title: Issues
domain: github
section: 06
category: collaboration
difficulty: beginner
danger: none
tags:
  - github/issues
commands: []
endpoints:
  - GET /repos/{owner}/{repo}/issues
  - POST /repos/{owner}/{repo}/issues
  - GET /repos/{owner}/{repo}/labels
  - GET /repos/{owner}/{repo}/milestones
dashboard_relevant: true
related:
  - "[[GitHub - Projects]]"
  - "[[GitHub - Search Syntax]]"
  - "[[GitHub - Pull Requests]]"
sources:
  - https://docs.github.com/en/issues
  - https://docs.github.com/en/rest/issues/issues
  - https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests
updated: 2026-08-14
---

# Issues

## Structure

An issue has: title, body (GFM), state (`open`/`closed`), state reason
(`completed`/`not_planned`/`reopened`/`duplicate`), labels, assignees (max 10),
milestone, and a timeline of events.

## Labels

Free-form `name` + `color` + `description`. Conventions that scale:

```
type:bug  type:feature  type:chore
priority:p0 … priority:p3
area:api  area:ui
status:blocked  status:needs-info
good first issue     ← surfaced specially by GitHub
help wanted          ← same
```

Prefixed labels sort together and read cleanly in filters.

## Milestones

A named bucket with an optional due date. Gives you a completion percentage for
free. Use for releases; use [[GitHub - Projects]] for anything needing custom
fields.

## Issue templates vs. issue forms

- **Templates** — Markdown files in `.github/ISSUE_TEMPLATE/`; a prefilled body
- **Forms** — YAML in the same directory; real input widgets with validation,
  producing structured, parseable bodies

Forms are strictly better if you plan to parse issue content programmatically.
`.github/ISSUE_TEMPLATE/config.yml` controls the chooser and can add external
links and disable blank issues.

## Linking to PRs

A PR body containing `Fixes #123`, `Closes #123`, or `Resolves #123` auto-closes
the issue on merge. Cross-repo works: `Fixes owner/repo#123`. Bare `#123` links
without closing.

## Sub-issues and types

GitHub added native **sub-issues** (parent/child hierarchy) and **issue types**
(org-level classification separate from labels). Both are exposed in GraphQL
before REST — check current API coverage before depending on them.

## ⚠️ The PR-in-issues trap

`GET /repos/{owner}/{repo}/issues` **returns pull requests too**. Every PR is an
issue in GitHub's data model. Filter client-side on the presence of the
`pull_request` key:

```js
const realIssues = items.filter(i => !i.pull_request);
```

This affects `open_issues_count` on the repo object as well.

---

## Related

- [[GitHub - Projects]]
- [[GitHub - Search Syntax]]
- [[GitHub - Pull Requests]]

## Sources

- <https://docs.github.com/en/issues>
- <https://docs.github.com/en/rest/issues/issues>
- <https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests>
