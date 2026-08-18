---
title: Rate Limiting Strategies
domain: api
section: "52"
category: patterns
difficulty: intermediate
danger: medium
tags:
  - api/limits
  - api/patterns
commands: []endpoints: []

dashboard_relevant: true
mobile_relevant: true
related:
  - "[[API - Idempotency and Retries]]"
  - "[[API - Caching and ETags]]"
  - "[[API - Headers]]"
  - "[[GitHub - Rate Limits]]"
  - "[[API - HTTP Methods and Status Codes]]"
  - "[[Bridge - GitHub API Conventions]]"
  - "[[API - Client-Only vs Backend Architectures]]"
sources:
  - https://datatracker.ietf.org/doc/html/rfc6585
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Retry-After
  - https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api
updated: 2026-08-18
---

# Rate Limiting Strategies

A rate limit is a server protecting itself from the sum of its clients. As a
client you need to know which algorithm you are up against, because they fail in
different ways: one lets you burst and then stalls, another smooths you out, a
third makes a limit you have not touched in an hour still reject you. Guessing
wrong produces a client that works in testing and gets throttled in production.

## The algorithms

| Algorithm | Behaviour | Bursts | Typical use |
|---|---|---|---|
| Fixed window | N per calendar hour, resets on the hour | Yes, badly | Simple quotas |
| Sliding window | N in any trailing 60 minutes | Smoothed | Public APIs |
| Token bucket | Bucket of N, refills at R per second | **Yes, up to N** | Most APIs |
| Leaky bucket | Queue drains at a constant rate | No | Traffic shaping |
| Concurrency cap | At most N requests in flight | N/A | Expensive operations |

**Token bucket** is the common one and the most client-friendly: you accumulate
allowance while idle and may spend it in a burst, then you are limited to the
refill rate. **Leaky bucket** is the opposite — a strictly constant output rate,
no bursting at all.

**Fixed window** has a well-known edge defect: N requests at 10:59 and N more at
11:00 is 2N in two minutes, all legal. Servers move to sliding windows precisely
to close that, which is why a limit that "should have reset" sometimes has not.

## Reading your budget

```http
HTTP/1.1 200 OK
x-ratelimit-limit: 5000
x-ratelimit-remaining: 4832
x-ratelimit-used: 168
x-ratelimit-reset: 1755500000      # Unix seconds, not a duration
```

Read these on **every** response, not only after a rejection. A client that
first looks at `remaining` when it sees a 429 has already lost.

```kotlin
data class Budget(
    val remaining: Int,
    val resetAt: Long,
    val safeRatePerSec: Double,
)

fun budget(res: Response): Budget {
    val remaining = res.header("x-ratelimit-remaining")?.toIntOrNull() ?: 0
    val resetAt = (res.header("x-ratelimit-reset")?.toLongOrNull() ?: 0L) * 1000
    val secondsLeft =
        ((resetAt - System.currentTimeMillis()) / 1000).coerceAtLeast(0)

    return Budget(remaining, resetAt, remaining / (secondsLeft + 1.0))
}
```

Pacing against `safeRatePerSec` spreads the budget across the window instead of
sprinting through it and then blocking for fifty minutes.

## Responding to 429

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 60
```

`Retry-After` is either a delay in seconds or an HTTP date, and it **overrides**
any backoff you computed. When it is absent, fall back to exponential backoff
with full jitter — see [[API - Idempotency and Retries]].

| Response | Meaning | Action |
|---|---|---|
| 429 + `Retry-After` | Over the documented limit | Sleep exactly that long |
| 429, no header | Over a secondary or hidden limit | Backoff with jitter |
| 403 + `x-ratelimit-remaining: 0` | Some APIs use 403 for quota | Treat as 429 |
| 5xx under load | Overload, not quota | Backoff, and reduce concurrency |

## Spending less

The cheapest request is the one you do not make.

- **Conditional requests.** On GitHub a 304 costs no quota at all, which makes
  ETags the single largest saving available — see [[API - Caching and ETags]].
- **Webhooks instead of polling**, where you control a server — see
  [[API - Webhooks vs Polling]].
- **Bigger pages.** `per_page=100` fetches the same data in a tenth of the
  requests of `per_page=10`.
- **One GraphQL query instead of a REST fan-out**, when the cost model favours
  it — see [[API - REST vs GraphQL]].

## Server-side, briefly

If you are the one imposing limits: key on identity rather than IP where you
can (NAT and mobile carriers put thousands of users behind one address), always
send `Retry-After`, return 429 rather than dropping connections, and apply a
separate stricter limit to expensive endpoints such as search.

## ⚠️ Gotchas

- ⚠️ **Secondary limits are undocumented and separate.** Concurrent writes to
  the same resource, rapid content creation and long-running queries trip
  abuse-detection limits that no `x-ratelimit-*` header ever showed as
  consumed. Serialise writes to a single resource and keep concurrency modest.
- ⚠️ **The quota is per token, not per process.** Every instance, worker and
  developer laptop sharing one token draws from one bucket. Scaling out
  multiplies consumption while the limit stays fixed — this is the usual cause
  of a limit that appears to have shrunk.
- ⚠️ **Retrying a 429 without honouring `Retry-After` extends the block.** Many
  gateways treat over-limit requests during a cooldown as fresh violations and
  lengthen the penalty.
- ⚠️ **Reset is an absolute timestamp, not a duration.** Reading
  `x-ratelimit-reset` as "seconds from now" produces sleeps of decades and a
  client that appears to hang forever.
- **Different buckets have different limits.** GitHub meters search separately
  from core REST and meters GraphQL in points; exhausting one leaves the others
  untouched. See [[Bridge - GitHub API Conventions]].
- **Unauthenticated limits are dramatically lower** — 60 requests per hour on
  GitHub versus 5,000. A dropped token looks exactly like a sudden rate-limit
  collapse.
- **Checking your budget can be free.** `GET /rate_limit` does not itself count
  against the limit.

---

## Related

- [[API - Idempotency and Retries]]
- [[API - Caching and ETags]]
- [[API - Headers]]
- [[GitHub - Rate Limits]]
- [[API - HTTP Methods and Status Codes]]
- [[Bridge - GitHub API Conventions]]
- [[API - Client-Only vs Backend Architectures]]

## Sources

- <https://datatracker.ietf.org/doc/html/rfc6585>
- <https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Retry-After>
- <https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api>
