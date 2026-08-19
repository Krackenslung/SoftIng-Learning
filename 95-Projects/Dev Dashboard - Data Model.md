---
title: Dev Dashboard — Data Model
domain: project
type: spec
tags:
  - project/dashboard
related:
  - "[[GitHub - Pull Requests]]"
  - "[[GitHub - Notifications]]"
  - "[[GitHub - Rate Limits]]"
  - "[[API - Caching and ETags]]"
  - "[[Android - Offline First and Room]]"
  - "[[Android - WorkManager]]"
  - "[[Bridge - GitHub API on Android]]"
updated: 2026-08-14
---

# Dev Dashboard — Data Model

Working spec for the GitHub tab. Concepts link back to the reference notes.

## Tab hierarchy

Ordered by check frequency — PRs and Notifications carry badge counts.

| # | Sub-tab | Badge | Primary source |
|---|---|---|---|
| 1 | **Pull Requests** | ✅ needs-my-action count | [[GitHub - Pull Requests]] |
| 2 | **Notifications** | ✅ unread actionable | [[GitHub - Notifications]] |
| 3 | Issues | — | [[GitHub - Issues]] |
| 4 | Actions / CI | on failure | [[GitHub - Actions]] |
| 5 | Activity / Commits | — | [[Git - Searching History]] |
| 6 | Repositories | — | [[GitHub - Repositories]] |

## Storage format decision

| Data | Format | Why |
|---|---|---|
| Reference docs, notes | `.md` | Human-authored, diffable, this vault |
| Cached API responses | JSON | Programmatic parsing, matches API shape |
| App config, workflows | YAML | Human-editable, comments, hierarchy |
| Local cache index | SQLite | Query across entities, offline |

`.md` supports YAML frontmatter, Mermaid, LaTeX and inline HTML — good for
documentation. It is the wrong shape for anything the app parses on a hot path.

## Entities

```
Repository
├── id, full_name, private, archived, default_branch, pushed_at
├── PullRequest[]
│   ├── number, title, state, merged_at, draft, mergeable_state
│   ├── head.sha  → CheckRun[]
│   ├── Review[]  → state, user, submitted_at
│   └── requested_reviewers[]
├── Issue[]          ⚠️ filter out items with a `pull_request` key
├── WorkflowRun[]    → status + conclusion (both nullable, see note)
└── Branch[]         → protection rules
Notification         → thread, reason, unread, subject.url
```

## Derived: "needs my action"

The badge count. Priority order:

1. PR where I'm in `requested_reviewers` and have no submitted review
2. My PR with `reviewDecision: CHANGES_REQUESTED`
3. My PR approved + `mergeable_state: clean` → ready to merge
4. My PR with a failed check
5. Notification with `reason` in `{review_requested, assign, mention}`

Everything else is ambient and must not inflate the badge.

## ⚠️ Data traps

Each of these has bitten real dashboards — details in the linked notes.

- `state: "closed"` includes merged PRs → branch on `merged_at !== null`
- `issues` endpoint returns PRs → filter on the `pull_request` key
- `open_issues_count` includes PRs
- `mergeable` is `null` on first read → poll again
- `conclusion` is `null` while `status: in_progress` → don't render as failure
- `404` on a private resource often means **missing permission**, not missing
- Projects v2, Discussions and sub-issues are **GraphQL only**
- Search API caps at 1,000 results and has its own 30/min limit

## Sync architecture

There is no backend, so there are no webhooks: a phone has no inbound endpoint
to deliver them to. Change detection is polling, on three paths with very
different latencies — see [[API - Client-Only vs Backend Architectures]].

```
app opened      → refresh, conditional → write Room → UI re-emits
pull-to-refresh → refresh, conditional → write Room → UI re-emits
WorkManager     → periodic, 15 min floor, deferred by Doze → write Room
```

Every read sends its stored `ETag`; a `304` costs no core quota, which is what
makes polling viable at all. Room is the source of truth the UI observes, so a
failed sync writes nothing and the screen keeps the last good data instead of
blanking — see [[Android - Offline First and Room]].

⚠️ Background sync is best-effort, not scheduled. It can be hours stale on an
idle device, so the UI must show the last successful sync time rather than imply
the data is current. See [[Android - WorkManager]] and
[[Android - Background Limits and Doze]].
