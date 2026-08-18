---
title: Code Review
domain: github
section: 08
category: collaboration
difficulty: intermediate
danger: none
tags:
  - github/pr
  - github/review
commands: []
endpoints:
  - GET /repos/{owner}/{repo}/pulls/{n}/reviews
  - POST /repos/{owner}/{repo}/pulls/{n}/reviews
  - GET /repos/{owner}/{repo}/pulls/{n}/comments
dashboard_relevant: true
related:
  - "[[GitHub - Pull Requests]]"
  - "[[GitHub - Branch Protection and Rulesets]]"
  - "[[GitHub - Accounts Orgs and Teams]]"
sources:
  - https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests
  - https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
  - https://docs.github.com/en/rest/pulls/reviews
updated: 2026-08-14
---

# Code Review

## Three kinds of comment

| Kind | Attached to | API |
|---|---|---|
| **Issue comment** | The PR conversation | `/issues/{n}/comments` |
| **Review comment** | A specific line/diff hunk | `/pulls/{n}/comments` |
| **Review** | A batch of review comments + a verdict | `/pulls/{n}/reviews` |

They live at **different endpoints**. A dashboard showing "all comments" must
query at least two.

## Review states

`COMMENTED` · `APPROVED` · `CHANGES_REQUESTED` · `DISMISSED` · `PENDING`

`PENDING` reviews are drafts visible only to their author — they are returned by
the API only for the authenticated author.

Only the **latest** review per reviewer counts toward branch protection. An
`APPROVED` followed by `COMMENTED` from the same person still counts as approved.

## CODEOWNERS

`.github/CODEOWNERS` (or repo root, or `docs/`):

```
*                      @org/core-team
/src/api/              @org/backend @alice
/src/ui/**/*.tsx       @org/frontend
*.tf                   @org/infra
/docs/                 @tech-writers
```

- Last matching pattern wins — order matters, general to specific
- Gitignore-style syntax
- Owners are auto-requested as reviewers
- Combined with "Require review from Code Owners" in
  [[GitHub - Branch Protection and Rulesets]], it becomes enforcement rather
  than suggestion
- Syntax errors fail **silently** in older setups — check the repo's CODEOWNERS
  validation view

## Suggested changes

````markdown
```suggestion
const timeout = 5000;
```
````

Committable by the author in one click, batchable into a single commit.

## Dismissing and re-requesting

- Stale approvals can be auto-dismissed on new pushes (a protection setting)
- `POST .../reviews/{id}/dismissals` dismisses with a reason
- Re-request review after addressing feedback — this re-triggers the
  `review_requested` notification

---

## Related

- [[GitHub - Pull Requests]]
- [[GitHub - Branch Protection and Rulesets]]
- [[GitHub - Accounts Orgs and Teams]]

## Sources

- <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests>
- <https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners>
- <https://docs.github.com/en/rest/pulls/reviews>
