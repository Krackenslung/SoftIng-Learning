---
title: Client-Only vs Backend Architectures
domain: api
section: "52a"
category: patterns
difficulty: advanced
danger: medium
tags:
  - api/patterns
  - api/architecture
  - api/mobile
commands: []
endpoints: []
dashboard_relevant: true
mobile_relevant: true
related:
  - "[[API - Webhooks vs Polling]]"
  - "[[API - Rate Limiting Strategies]]"
  - "[[API - Caching and ETags]]"
  - "[[API - Token Storage on Public Clients]]"
  - "[[Dev Dashboard - API Map]]"
sources:
  - https://datatracker.ietf.org/doc/html/rfc8252
  - https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api
  - https://developer.android.com/topic/libraries/architecture/workmanager
updated: 2026-08-18
---

# Client-Only vs Backend Architectures

An app that talks to a third-party API has one structural decision to make
before anything else: does the device call the API directly, or does it call a
server you run, which calls the API? Everything downstream — how you
authenticate, whether webhooks are even possible, whose rate-limit budget you
spend, where the cache lives — is determined by that one choice. This vault
assumes **Option A, client-only**, and this note is the reasoning and the bill.

## The two options

| | A — Client-only | B — Thin backend |
|---|---|---|
| Who calls the API | The device | Your server |
| Token lives | On the device | On the server |
| Client type | **Public** — no secret possible | Confidential |
| OAuth flow | Auth code + PKCE, or device flow | Any, including client credentials |
| Webhooks | **Impossible** — no public endpoint | Natural fit |
| Change detection | Polling only | Push |
| Rate-limit budget | Per user, per device | **Shared across all users** |
| Cache | Per device | Shared, warm for everyone |
| Ops cost | Zero | Hosting, deploys, monitoring, uptime |
| Breach scope | One device | **Every user's token at once** |
| Offline | Local store is the source of truth | Needs a sync design either way |

## What client-only costs

**No webhooks.** A webhook is an inbound HTTP request, and a phone has no
stable public address to receive one. That is not a limitation you can engineer
around on-device; it removes push entirely and makes polling the only mechanism.
Latency goes from seconds to half your poll interval, and correctness now
depends on a reconciliation sweep — see [[API - Webhooks vs Polling]].

**Polling is bounded by the platform, not by you.** Background work on Android
is scheduled, not guaranteed: `WorkManager` periodic work has a documented
minimum interval, and Doze and app standby will delay it further on an idle
device. A "live" dashboard is therefore live when the app is open and
best-effort when it is not.

```kotlin
val request = PeriodicWorkRequestBuilder<SyncWorker>(15, TimeUnit.MINUTES)
    .setConstraints(
        Constraints.Builder()
            .setRequiredNetworkType(NetworkType.CONNECTED)
            .build(),
    )
    .build()

WorkManager.getInstance(context).enqueueUniquePeriodicWork(
    "github-sync",
    ExistingPeriodicWorkPolicy.KEEP,
    request,
)
```

**Every device pays its own fan-out.** There is no shared cache to amortise the
first load, so a cold install spends real budget rebuilding state that a backend
would have served from memory.

## What client-only buys

**No secret to protect, and no shared blast radius.** A backend holding every
user's token is a single target whose compromise is total; a client-only app
loses one device at a time — see [[API - Token Storage on Public Clients]].

**The rate-limit budget is per user.** Each device authenticates as its own
user and gets that user's full hourly quota. A backend that calls the API with
one token pools every user into a single bucket, which is the more common way
integrations hit limits — see [[API - Rate Limiting Strategies]].

**Nothing to run.** No hosting, no deploy pipeline, no uptime obligation, no
privacy question about storing other people's tokens.

## Consequence map

Choosing A is not one decision; it is these, already made:

| Because there is no server | The consequence | Covered in |
|---|---|---|
| No inbound endpoint | Polling replaces push | [[API - Webhooks vs Polling]] |
| Polling costs quota | Conditional requests become critical | [[API - Caching and ETags]] |
| Budget is per device | Pace against `x-ratelimit-*`, do not sprint | [[API - Rate Limiting Strategies]] |
| No client secret | PKCE or device flow, never a secret | [[API - OAuth 2.0 Flows]] |
| Token sits on-device | Keystore, short lifetimes, revocation | [[API - Token Storage on Public Clients]] |
| No shared cache | Local store is authoritative; reconcile | [[Dev Dashboard - Data Model]] |

The `304` is what makes this viable at all: on GitHub a conditional request that
returns "not modified" costs no core quota, so a well-behaved poller can check
far more often than a naive one — see [[Bridge - GitHub API Conventions]].

## When a backend wins

Switch to Option B when any of these is true, and not before:

- **Multiple users must see the same aggregated view.** One server call feeding
  many clients beats N clients each fetching everything.
- **You need webhook latency.** Seconds instead of minutes, reliably.
- **A real secret is required** — a GitHub App's private key, a signing key, or
  any credential that cannot be shipped to a device.
- **Queries are expensive and repeated.** A shared cache amortises a costly
  GraphQL query across users; per-device, every user pays it.
- **You need server-side history** beyond what the API retains.

A hybrid is legitimate: client-only for the common path, with a small server
added later purely to receive webhooks and push notifications. That migration is
much easier than the reverse, which is another reason to start at A.

## ⚠️ Gotchas

- ⚠️ **A backend concentrates every user's token.** Option B is not "more
  secure" by default; it converts many one-device compromises into one total
  compromise. If you build it, that store is the highest-value asset you own.
- ⚠️ **A shared backend token pools every user into one rate-limit bucket.**
  This is the failure that appears only under growth: fine at ten users, throttled
  at a thousand, with no code change in between.
- ⚠️ **Background polling is best-effort, not scheduled.** Treating a periodic
  worker as a guaranteed timer produces a dashboard that is silently hours stale
  on a phone in a pocket. Show the last successful sync time in the UI.
- ⚠️ **Client-only means no reliable "since I last looked".** Without webhooks
  you cannot detect an event that happened and was reverted between two polls.
  If that matters, you need push, which means a server.
- **Do not proxy the API through a backend purely to hide the token.** A proxy
  that forwards a user's own token adds a hop, a cache-correctness problem and a
  liability without changing the client's public-client status.
- **The device flow exists for exactly this case** and avoids redirect-URI
  handling on mobile entirely — worth preferring where the provider supports it.

## To verify

- The current minimum periodic interval for `WorkManager`, and current Doze and
  app-standby behaviour at the target API level — `<verify current>`
- Whether the planned `60-Android` stack pins any library version — none are
  asserted in this note — `<verify current>`

---

## Related

- [[API - Webhooks vs Polling]]
- [[API - Rate Limiting Strategies]]
- [[API - Caching and ETags]]
- [[API - Token Storage on Public Clients]]
- [[Dev Dashboard - API Map]]

## Sources

- <https://datatracker.ietf.org/doc/html/rfc8252>
- <https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api>
- <https://developer.android.com/topic/libraries/architecture/workmanager>
