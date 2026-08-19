---
title: Idempotency and Retries
domain: api
section: "45"
category: fundamentals
difficulty: intermediate
danger: high
tags:
  - api/http
  - api/reliability
commands: []endpoints: []

dashboard_relevant: true
mobile_relevant: true
related:
  - "[[API - HTTP Methods and Status Codes]]"
  - "[[API - Rate Limiting Strategies]]"
  - "[[API - Webhooks vs Polling]]"
  - "[[GitHub - REST API]]"
  - "[[Android - WorkManager]]"
  - "[[Android - Coroutines and Flow]]"
sources:
  - https://datatracker.ietf.org/doc/html/rfc9110#section-9.2.2
  - https://developer.mozilla.org/en-US/docs/Glossary/Idempotent
  - https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/
updated: 2026-08-18
---

# Idempotency and Retries

A network timeout tells you nothing about what the server did. The request may
never have arrived, may have been processed and had its response lost, or may
still be running. Retrying is therefore a bet, and idempotency is what decides
whether the bet is free or dangerous — this is the single property that
separates a retry policy from a data-corruption policy.

## What the spec guarantees

| Method | Idempotent by spec | Safe to auto-retry |
|---|---|---|
| `GET`, `HEAD`, `OPTIONS` | yes | yes |
| `PUT` | yes | yes |
| `DELETE` | yes | yes (expect 404 on the second) |
| `POST` | **no** | only with an idempotency key |
| `PATCH` | **no** | only if the patch is absolute, or with a key |

Idempotent means N identical requests leave the same *state* as one. It does not
mean the responses match: a repeated `DELETE` returns 204 then 404, and that is
still idempotent.

## Idempotency keys

For unavoidable `POST` retries, the client supplies a unique key and the server
promises to execute at most once per key:

```http
POST /payments HTTP/1.1
Idempotency-Key: 1f0c3a7e-3f5a-4c1a-9a1c-2b8f5a0d9e77
Content-Type: application/json
```

Rules that make this actually work:

- Generate the key **once per logical operation**, not once per attempt — a new
  UUID on each retry defeats the entire mechanism.
- Keep it stable across process restarts if the operation can outlive one, which
  means persisting it alongside the pending work.
- The server stores key to result and replays the stored response, including the
  original status code.
- Keys expire. A retry a week later is a new operation.

Not every API supports this. Where it is absent, the fallback is a **natural
idempotency key**: a client-chosen identifier the resource itself carries, so a
duplicate create collides on a uniqueness constraint and returns 409 instead of
creating a second row.

## Backoff with jitter

```kotlin
suspend fun <T> withRetry(
    attempts: Int = 5,
    baseMs: Long = 500,
    capMs: Long = 30_000,
    block: suspend () -> T,
): T {
    repeat(attempts - 1) { i ->
        try {
            return block()
        } catch (e: IOException) {
            if (!isRetryable(e)) throw e
            val ceiling = minOf(capMs, baseMs shl i)
            val jittered = Random.nextLong(ceiling)      // full jitter
            delay(retryAfterMs(e) ?: jittered)
        }
    }
    return block()                                       // last attempt
}
```

Exponential backoff alone is not enough. If a shared dependency fails, every
client backs off on the *same* schedule and they all return together, producing
a synchronised thundering herd that re-breaks the service. **Jitter** — randomly
spreading each client's delay — is what actually decorrelates them.

`Retry-After` always wins over your computed delay when the server sends it.

## What to retry

| Signal | Retry | Why |
|---|---|---|
| Connection reset, DNS failure, timeout | yes | Possibly never processed |
| 500, 502, 503, 504 | yes | Transient server fault |
| 429 | yes, after `Retry-After` | You are over budget, not wrong |
| 408 Request Timeout | yes | Server gave up waiting |
| 400, 401, 403, 404, 422 | **no** | Deterministic; the retry fails identically |
| 409 Conflict | only after re-reading state | The precondition changed |

Retrying a 4xx is how a broken token turns into a self-inflicted denial of
service against your own quota.

## Retry budgets and circuit breakers

Per-request retry limits still allow a system-wide amplification of 3–5x
precisely when a dependency is least able to take it. Two controls bound that:

- **Retry budget** — cap retries at a fraction of overall traffic (10% is a
  common figure) and shed the rest rather than queueing them.
- **Circuit breaker** — after a run of failures, fail fast for a cooldown, then
  let a single probe request decide whether to close the circuit.

## ⚠️ Gotchas

- ⚠️ **Retrying a non-idempotent write can duplicate it.** A timeout on
  `POST /issues` that actually succeeded produces two issues on retry. Without
  an idempotency key, the correct response to an ambiguous write failure is to
  *read back* and reconcile, not to resend.
- ⚠️ **A fresh key per attempt is worse than no key**, because the code looks
  correct and reviewers stop asking. Generate it where the operation is created.
- ⚠️ **Retries multiply under nesting.** Three layers each retrying three times
  is 27 requests for one logical call. Retry at exactly one layer — usually the
  outermost one that still knows the operation is safe to repeat.
- ⚠️ **Backoff without jitter synchronises clients.** Every instance recovers at
  the same instant and the outage repeats in waves.
- **`PUT` is idempotent, but read-modify-write is not.** Fetching, mutating and
  putting back is a lost-update race unless you send `If-Match` with the ETag —
  see [[API - Caching and ETags]].
- **Do not retry inside a request handler that already timed out upstream.** The
  caller has gone; the work is pure load.
- **At-least-once delivery makes consumers responsible for deduplication.**
  Webhook receivers must key on the delivery or event ID — see
  [[API - Webhooks vs Polling]].

> [!warning] The ambiguous outcome is the whole problem
> "Did it happen?" is unanswerable from the client side. Every design here
> exists to convert that ambiguity into either a safe repeat or a definite
> answer. If your write path does neither, it is one dropped packet away from
> duplicate data.

---

## Related

- [[API - HTTP Methods and Status Codes]]
- [[API - Rate Limiting Strategies]]
- [[API - Webhooks vs Polling]]
- [[GitHub - REST API]]
- [[Android - WorkManager]]
- [[Android - Coroutines and Flow]]

## Sources

- <https://datatracker.ietf.org/doc/html/rfc9110#section-9.2.2>
- <https://developer.mozilla.org/en-US/docs/Glossary/Idempotent>
- <https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/>
