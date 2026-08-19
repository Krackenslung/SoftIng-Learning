---
title: Webhooks vs Polling
domain: api
section: "51"
category: patterns
difficulty: intermediate
danger: low
tags:
  - api/webhooks
  - api/patterns
commands: []endpoints: []

dashboard_relevant: true
mobile_relevant: true
related:
  - "[[API - HMAC Signatures]]"
  - "[[API - Idempotency and Retries]]"
  - "[[API - Caching and ETags]]"
  - "[[GitHub - Webhooks]]"
  - "[[API - Client-Only vs Backend Architectures]]"
  - "[[Android - WorkManager]]"
  - "[[Android - Background Limits and Doze]]"
sources:
  - https://docs.github.com/en/webhooks/about-webhooks
  - https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api
  - https://datatracker.ietf.org/doc/html/rfc9110
updated: 2026-08-18
---

# Webhooks vs Polling

Two ways to learn that something changed: ask repeatedly, or be told. Polling is
trivial to build and wastes almost every request; webhooks are efficient and
push a distributed-systems problem — delivery, ordering, duplication, security —
onto you. The choice is mostly decided by one question: **do you control a
publicly reachable server?** If not, the decision is already made.

## Comparison

| | Polling | Webhooks |
|---|---|---|
| Direction | You pull | They push |
| Latency | Half the poll interval, on average | Seconds |
| Cost when idle | Full — every poll is a request | Zero |
| Needs a public endpoint | No | **Yes** |
| Works behind a firewall | Yes | No, without a tunnel |
| Missed events | Impossible — you re-read state | Possible, must reconcile |
| Duplicates | No | **Yes — at-least-once** |
| Ordering | You read current state | **Not guaranteed** |
| Security burden | Guard your token | Verify every request |
| Failure mode | Stale data | Silent divergence |

## Making polling cheap

Polling is not automatically wasteful. Conditional requests turn "nothing
changed" into a nearly free answer:

```kotlin
val request = Request.Builder()
    .url(url)
    .apply { store.etag?.let { header("If-None-Match", it) } }
    .build()

client.newCall(request).execute().use { res ->
    // 304 means no body, and on GitHub it costs no core quota.
    if (res.code == 304) return store.data
    store.etag = res.header("ETag")
    store.data = json.decodeFromString(res.body?.string().orEmpty())
    return store.data
}
```

Three rules make a poller well-behaved:

- Send the stored `ETag` every time — see [[API - Caching and ETags]].
- Honour `X-Poll-Interval` where the API sends one; it is a floor, not a hint.
- Add jitter to the interval so restarts do not synchronise every instance into
  a burst — see [[API - Rate Limiting Strategies]].

## What webhooks do not guarantee

A webhook is an HTTP request from someone else's queue, with all that implies.

**At-least-once delivery.** Retries mean the same event can arrive twice.
Deduplicate on the delivery ID, and make the handler idempotent — see
[[API - Idempotency and Retries]].

**No ordering.** Concurrent deliveries mean a `closed` event can arrive before
the `opened` event for the same pull request. Never build state by applying
events in arrival order; carry a version or timestamp and drop anything older
than what you already have.

**Delivery can fail entirely.** Your endpoint is down, a deploy drops in-flight
requests, the provider disables the hook after repeated failures. Any of these
means permanent divergence unless you reconcile.

**The payload can be stale.** By the time you process it, the resource may have
changed again. Treat the payload as a *notification that something happened*,
and re-read authoritative state when correctness matters.

## The handler shape that works

```js
app.post("/hooks", async (req, res) => {
  if (!verify(req.rawBody, req.get("x-hub-signature-256"), SECRET)) {
    return res.sendStatus(401);          // verify before anything else
  }
  const id = req.get("x-github-delivery");
  if (await seen(id)) return res.sendStatus(200);   // dedupe

  await queue.push({ id, event: req.get("x-github-event"), body: req.rawBody });
  res.sendStatus(202);                   // ack fast, process out of band
});
```

Acknowledge within a couple of seconds. Providers time out aggressively, and
slow processing inside the request turns into retries, which turn into
duplicates, which turn into more load.

## Use both

The production pattern is webhooks for latency plus a periodic reconciliation
sweep for correctness: hourly or daily, list the resources you track and repair
anything the event stream missed. Webhooks keep the dashboard live; the sweep
keeps it true.

## ⚠️ Gotchas

- ⚠️ **Every webhook endpoint is a public, unauthenticated URL until you verify
  the signature.** Anyone can POST to it. Verification is not optional — see
  [[API - HMAC Signatures]].
- ⚠️ **Without reconciliation, a missed delivery is permanent.** There is no
  error and no gap in your logs; the data is simply wrong from that moment on.
  This is the failure mode that makes webhook-only designs quietly unreliable.
- ⚠️ **Do not apply events in arrival order.** Out-of-order delivery will
  reopen closed issues and resurrect deleted rows. Compare versions before
  writing.
- ⚠️ **Slow handlers cause duplicate deliveries.** A timeout is a failure to the
  provider, which retries — while your first invocation is still running.
  Acknowledge immediately and queue the work.
- **Redeliveries are also a debugging tool.** GitHub keeps recent deliveries and
  lets you replay them, which beats reproducing an event by hand.
- **Local development needs a tunnel** (`gh webhook forward`, ngrok, smee).
  Nothing reaches `localhost` from a provider's queue.
- **Polling frequency is not free even with ETags.** The request still costs a
  connection and a secondary-limit slot, so respect the documented floor.

---

## Related

- [[API - HMAC Signatures]]
- [[API - Idempotency and Retries]]
- [[API - Caching and ETags]]
- [[GitHub - Webhooks]]
- [[API - Client-Only vs Backend Architectures]]
- [[Android - WorkManager]]
- [[Android - Background Limits and Doze]]

## Sources

- <https://docs.github.com/en/webhooks/about-webhooks>
- <https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api>
- <https://datatracker.ietf.org/doc/html/rfc9110>
