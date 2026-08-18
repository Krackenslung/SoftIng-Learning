---
title: Pull Requests
domain: github
section: 07
category: collaboration
difficulty: intermediate
danger: medium
tags:
  - github/pr
  - github/collaboration
commands: []
endpoints:
  - GET /repos/{owner}/{repo}/pulls
  - GET /repos/{owner}/{repo}/pulls/{n}
  - GET /repos/{owner}/{repo}/pulls/{n}/files
  - GET /repos/{owner}/{repo}/pulls/{n}/reviews
  - PUT /repos/{owner}/{repo}/pulls/{n}/merge
  - GET /repos/{owner}/{repo}/commits/{ref}/status
dashboard_relevant: true
related:
  - "[[Bridge - PRs vs Merge]]"
  - "[[GitHub - Code Review]]"
  - "[[GitHub - Branch Protection and Rulesets]]"
  - "[[Git - Workflows]]"
sources:
  - https://docs.github.com/en/pull-requests
  - https://docs.github.com/en/rest/pulls/pulls
  - https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges
updated: 2026-08-14
---

# Pull Requests

A PR is a **request to merge `head` into `base`**, wrapped in review and CI
machinery. Git itself has no such concept — see [[Bridge - PRs vs Merge]].

## Lifecycle

```
draft ──► open ──► review ──┬──► approved ──► merged
                            ├──► changes requested ──► (push more commits)
                            └──► closed (unmerged)
```

## Key state fields

| Field | Values / meaning |
|---|---|
| `state` | `open` \| `closed` — **`merged` is not a state** |
| `merged` | boolean — check this, not `state` |
| `merged_at` | null if closed without merging |
| `draft` | true = not ready for review |
| `mergeable` | `true` / `false` / **`null` = still computing** |
| `mergeable_state` | `clean`, `dirty`, `blocked`, `behind`, `unstable`, `draft`, `unknown` |
| `requested_reviewers` | users still owing a review |
| `head.sha` | the commit to query for check status |

⚠️ **`mergeable` is computed lazily.** The first request after a change returns
`null` and *triggers* the computation. Poll again after a short delay. Dashboards
that read it once report nonsense.

⚠️ **A merged PR has `state: "closed"`.** Filtering on `state=closed` gives you
both abandoned and merged PRs. Always branch on `merged_at !== null`.

## Merge methods

| Method | Result on base | Trade-off |
|---|---|---|
| **Merge commit** | All commits + a merge node | Full fidelity, busier graph |
| **Squash** | One commit | Clean trunk, loses granularity |
| **Rebase** | Commits replayed linearly | Linear, but rewrites SHAs |

Squash uses the PR title as the commit subject by default — which is why
[[Git - Commit Conventions]] should be enforced on PR titles if you squash.

## Useful mechanics

- **Draft PRs** — no review requests sent, cannot merge
- **Auto-merge** — queues the merge for when checks pass
- **Merge queue** — serializes merges and tests each against the real future base;
  the fix for "green PR, red main"
- **Linked issues** — `Fixes #123` in the body
- **Suggested changes** — reviewers propose exact diffs, committable in one click
- `?w=1` on the Files tab hides whitespace-only changes

## Dashboard priority signals

For a "needs my attention" view, rank by:
1. `review_requested` for me and no review submitted yet
2. My PR with `changes_requested`
3. My PR that is `mergeable_state: clean` and approved → ready to merge
4. My PR with failing checks
5. My PR `behind` base

---

## Related

- [[Bridge - PRs vs Merge]]
- [[GitHub - Code Review]]
- [[GitHub - Branch Protection and Rulesets]]
- [[Git - Workflows]]

## Sources

- <https://docs.github.com/en/pull-requests>
- <https://docs.github.com/en/rest/pulls/pulls>
- <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges>
