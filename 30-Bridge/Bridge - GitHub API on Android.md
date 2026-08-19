---
title: GitHub API on Android
domain: bridge
section: B8
category: bridge
difficulty: intermediate
danger: medium
tags:
  - bridge
  - android/networking
  - github/api
commands: []
endpoints: []
dashboard_relevant: true
mobile_relevant: true
related:
  - "[[API - Client-Only vs Backend Architectures]]"
  - "[[Android - Networking]]"
  - "[[Android - WorkManager]]"
  - "[[Android - Keystore and Secure Storage]]"
  - "[[GitHub - REST API]]"
sources:
  - https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api
  - https://developer.android.com/topic/libraries/architecture/workmanager
  - https://github.com/Kotlin/kotlinx.serialization/blob/master/docs/json.md
updated: 2026-08-18
---

# GitHub API on Android

> **The general pattern is X. On Android it becomes Y.**

[[Web-APIs]] describes how to consume an HTTP API, and
[[Bridge - GitHub API Conventions]] describes where GitHub deviates from that.
This note is the third layer: where the advice in both changes shape because the
client is a phone with no server behind it. Every row below is a place where
doing the textbook thing produces the wrong result here.

## At a glance

| The general pattern | On Android it becomes |
|---|---|
| Webhooks for change detection | **Polling** — a phone has no inbound endpoint |
| Poll as often as the quota allows | A **15-minute floor**, then Doze defers further |
| `304` means the cache is valid | Your code sees **`200`** — OkHttp resolved it already |
| OAuth redirects to your server | Redirects to a **verified App Link**, via Custom Tabs |
| Token lives in a server session | Token lives in the **Keystore**, on one device |
| Server-side cache warms all users | **Room**, per device, warmed by nobody |
| Unknown JSON fields are the server's problem | `ignoreUnknownKeys`, or the app **crashes** |

## Polling replaces webhooks, and the floor is the platform's

Webhooks are unavailable — not discouraged, unavailable — because delivery
requires a public address the device does not have. That reasoning is in
[[API - Client-Only vs Backend Architectures]].

What is specific to Android is the *floor*. Even having accepted polling, you do
not choose the interval: periodic work has a documented minimum of 15 minutes
(`<verify current>`), and Doze and App Standby defer it further on an idle
device. So the real design is:

| Path | Latency | Reliability |
|---|---|---|
| App in foreground | Seconds | You control it |
| Pull-to-refresh | Immediate | The only predictable path |
| Background periodic | 15 minutes at best, hours at worst | Best-effort |

Anything the UI implies about freshness must be earned by a visible "last
synced" timestamp — see [[Android - WorkManager]] and
[[Android - Background Limits and Doze]].

## The `304` you never see

`GitHub - REST API` says a `304` costs no rate-limit quota, and
[[API - Caching and ETags]] explains why. Both are true, and on Android neither
is directly observable, because OkHttp handles validators internally and hands
your code a `200` served from disk.

```kotlin
// response.code is 200 even when the network returned 304.
val cameFromNetwork = response.networkResponse != null
val quotaSpent = response.networkResponse?.code !in setOf(null, 304)
```

This is the single most consequential difference in the whole note: an
integration that measures quota by `response.code` reports every cache hit as a
full-price request, so the saving that makes client-only polling viable becomes
invisible and unverifiable. Read `networkResponse` — see
[[Android - Networking]].

## OAuth without a redirect you control

The textbook flow redirects to a URL on your server. There is no server, so the
redirect target is the app itself, and *how* the app claims it is a security
decision rather than a configuration detail.

| | Server redirect | Custom scheme | Verified App Link |
|---|---|---|---|
| Claimed by | Your domain | Any app declaring it | Only the verified app |
| Interceptable | No | **Yes** | No |

Use Custom Tabs, never a WebView, and pair verified App Links with PKCE so that
an intercepted code cannot be redeemed anyway. See [[Android - Navigation]] and
[[API - OAuth 2.0 Flows]].

## The token has no session to hide in

A backend keeps the token in a server session the user never touches. Here it
sits on the device, so the protections are different in kind: Keystore-wrapped
ciphertext, backup exclusion, redacted logging, and a working "sign out" that
clears both the blob and the key.

The compensating advantage is real and worth stating: a breach costs one device,
not every user's token at once — see
[[API - Token Storage on Public Clients]] and
[[Android - Keystore and Secure Storage]].

## Room is the cache, and nobody warms it

A server-side cache is populated by whoever arrives first and serves everyone
after. Per-device, every install pays its own cold start, so the local database
is not an optimisation — it is the only cache in the system, and the UI reads
from it rather than from the network. See
[[Android - Offline First and Room]].

## Unknown fields are your problem now

GitHub adds fields to responses without notice. A strict Kotlin parser treats an
unrecognised key as a hard error, which turns a routine, backwards-compatible
API change into a crash on every device at once — the worst failure mode
available to a client you cannot hotfix.

```kotlin
val json = Json {
    ignoreUnknownKeys = true      // non-negotiable against a live API
    explicitNulls = false
    coerceInputValues = true
}
```

The same lenience does **not** apply to fields you depend on: model those as
non-nullable and let deserialisation fail loudly in tests rather than silently
in production.

## ⚠️ Gotchas

- ⚠️ **Measuring quota by `response.code` counts every cache hit as a paid
  request.** The number is wrong in the conservative direction, which is why
  nobody notices — and it hides whether conditional requests work at all.
- ⚠️ **Missing `ignoreUnknownKeys` turns a GitHub field addition into a crash**
  for every installed copy simultaneously, with no server-side fix available.
- ⚠️ **A custom-scheme OAuth redirect can be intercepted by another installed
  app.** Verified App Links plus PKCE, both.
- ⚠️ **`User-Agent` is mandatory on GitHub** and its absence returns 403, which
  reads as an auth failure and sends you debugging the token — see
  [[Bridge - GitHub API Conventions]].
- ⚠️ **Background sync can silently not run for hours.** Never render a count as
  authoritative without showing when it was last refreshed.
- **`GET /issues` includes pull requests**, and `state: "closed"` includes merged
  ones. Fix both once, at the DTO-to-entity boundary — see
  [[Android - Layered Architecture]].
- **A 404 usually means permission, not absence.** Check scope before the path.
- **`304`-heavy polling is cheap on quota but not on battery.** Each wake still
  costs a radio activation.

---

## Related

- [[API - Client-Only vs Backend Architectures]]
- [[Android - Networking]]
- [[Android - WorkManager]]
- [[Android - Keystore and Secure Storage]]
- [[GitHub - REST API]]

## Sources

- <https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api>
- <https://developer.android.com/topic/libraries/architecture/workmanager>
- <https://github.com/Kotlin/kotlinx.serialization/blob/master/docs/json.md>
