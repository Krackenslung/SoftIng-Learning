---
title: Notifications and Inbox
domain: github
section: 05
category: platform
difficulty: intermediate
danger: none
tags:
  - github/notifications
commands: []
endpoints:
  - GET /notifications
  - PATCH /notifications
  - GET /repos/{owner}/{repo}/notifications
  - PATCH /notifications/threads/{thread_id}
dashboard_relevant: true
related:
  - "[[GitHub - Pull Requests]]"
  - "[[GitHub - REST API]]"
  - "[[GitHub - Webhooks]]"
sources:
  - https://docs.github.com/en/account-and-profile/managing-subscriptions-and-notifications-on-github
  - https://docs.github.com/en/rest/activity/notifications
updated: 2026-08-14
---

# Notifications and Inbox

## The model

A **notification** belongs to a **thread** (an issue, PR, commit, release, or
discussion). You receive one when you are *subscribed* to that thread.

Subscription happens automatically when you:
- are assigned, mentioned (`@you` or via a team), or requested for review
- comment on the thread
- open it
- watch the repository
- have your team mentioned

## `reason` values

The API returns a `reason` on every notification. This is the most useful field
for triage, and the natural way to segment a dashboard inbox:

| Reason | Meaning |
|---|---|
| `review_requested` | You were asked to review — **highest priority** |
| `assign` | You were assigned |
| `mention` | You were @-mentioned directly |
| `team_mention` | Your team was mentioned |
| `author` | You opened the thread |
| `comment` | You commented on it |
| `state_change` | Thread was opened/closed |
| `subscribed` | You watch the repo |
| `ci_activity` | A workflow run you triggered finished |
| `security_alert` | Dependabot / scanning alert |
| `manual` | You clicked Subscribe |

## API notes

```http
GET /notifications?all=false&participating=true&since=2026-08-01T00:00:00Z
```

- Default returns **unread only**; `all=true` includes read
- `participating=true` filters to threads you're directly involved in
- Supports `If-Modified-Since` → a `304` costs **no rate limit quota**
- Response includes `X-Poll-Interval` — **respect it**; polling faster is a
  secondary-rate-limit violation
- Mark a thread read: `PATCH /notifications/threads/{id}`
- Mark all read: `PATCH /notifications` with `last_read_at`

⚠️ The notifications payload does **not** include the PR/issue state. You get a
`subject.url` you must follow to learn whether the thread is still open. Batch
these or use [[GitHub - GraphQL API]] to avoid an N+1 request explosion.

## Dashboard design note

`review_requested` + `mention` + `assign` is the "needs my action" set. Everything
else is ambient. Badge counts should reflect the former only.

---

## Related

- [[GitHub - Pull Requests]]
- [[GitHub - REST API]]
- [[GitHub - Webhooks]]

## Sources

- <https://docs.github.com/en/account-and-profile/managing-subscriptions-and-notifications-on-github>
- <https://docs.github.com/en/rest/activity/notifications>
