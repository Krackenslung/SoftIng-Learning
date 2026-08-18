---
title: Webhooks
domain: github
section: 19
category: api
difficulty: advanced
danger: high
tags:
  - github/api
  - github/webhooks
commands: []
endpoints:
  - GET /repos/{owner}/{repo}/hooks
  - POST /repos/{owner}/{repo}/hooks
dashboard_relevant: true
related:
  - "[[GitHub - REST API]]"
  - "[[GitHub - Bots and Apps]]"
  - "[[GitHub - Rate Limits]]"
  - "[[API - HMAC Signatures]]"
  - "[[API - Webhooks vs Polling]]"
  - "[[API - Idempotency and Retries]]"
sources:
  - https://docs.github.com/en/webhooks
  - https://docs.github.com/en/webhooks/webhook-events-and-payloads
  - https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries
updated: 2026-08-14
---

# Webhooks

Push instead of poll. GitHub `POST`s a JSON payload to your endpoint when
something happens. Costs **zero** rate limit quota.

## Setup

Configurable at repo, org, or [[GitHub - Bots and Apps|App]] level. App-level is
best — one config for all installs.

## Signature verification — mandatory

Your endpoint is public. Without verification anyone can forge events.

```js
import crypto from "node:crypto";

function verify(rawBody, signatureHeader, secret) {
  const expected = "sha256=" + crypto
    .createHmac("sha256", secret)
    .update(rawBody)           // ⚠️ RAW bytes, before JSON.parse
    .digest("hex");
  const a = Buffer.from(expected);
  const b = Buffer.from(signatureHeader ?? "");
  return a.length === b.length && crypto.timingSafeEqual(a, b);
}
```

Two things people get wrong: hashing the *re-serialized* body instead of the raw
bytes, and using `===` instead of a timing-safe compare.

## Key headers

| Header | Use |
|---|---|
| `X-GitHub-Event` | Event type — routes your handler |
| `X-GitHub-Delivery` | Unique GUID — **use for idempotency** |
| `X-Hub-Signature-256` | HMAC to verify |
| `X-GitHub-Hook-Installation-Target-ID` | Which repo/org/app |

## Events for a dev dashboard

| Event | Useful `action` values |
|---|---|
| `pull_request` | opened, closed, reopened, synchronize, ready_for_review, review_requested |
| `pull_request_review` | submitted, dismissed |
| `pull_request_review_comment` | created |
| `issues` | opened, closed, assigned, labeled |
| `issue_comment` | created |
| `push` | *(no action field)* |
| `check_run` / `check_suite` | completed |
| `workflow_run` | requested, completed |
| `release` | published |
| `create` / `delete` | branch and tag lifecycle |

`synchronize` means new commits were pushed to the PR — that's your "re-check
this PR" trigger.

## Delivery guarantees

- **At-least-once.** Duplicates happen — dedupe on `X-GitHub-Delivery`.
- **No ordering guarantee.** Compare timestamps; don't assume sequence.
- Respond **2xx within 10 seconds** or the delivery is marked failed.
- So: verify → enqueue → return 200 → process async. Never do work inline.
- Failed deliveries can be redelivered from the UI or API; payloads are retained
  for a limited window.

## Local development

```bash
gh webhook forward --repo owner/repo --events pull_request --url http://localhost:3000/hooks
```

`smee.io` and `ngrok` are the alternatives.

## Hybrid architecture (recommended)

Webhooks for freshness, REST for reconciliation:

```
webhook → verify → enqueue → update cache      (near-real-time)
cron    → full sync every 15 min               (catches missed deliveries)
```

Webhooks alone will drift. Polling alone burns quota. Do both.

---

## Related

- [[GitHub - REST API]]
- [[GitHub - Bots and Apps]]
- [[GitHub - Rate Limits]]
- [[API - HMAC Signatures]]
- [[API - Webhooks vs Polling]]
- [[API - Idempotency and Retries]]

## Sources

- <https://docs.github.com/en/webhooks>
- <https://docs.github.com/en/webhooks/webhook-events-and-payloads>
- <https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries>
