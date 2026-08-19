---
title: Background Limits and Doze
domain: android
section: "75"
category: background
difficulty: advanced
danger: medium
tags:
  - android/background
  - android/battery
commands: []
endpoints: []
dashboard_relevant: true
mobile_relevant: true
related:
  - "[[Android - WorkManager]]"
  - "[[API - Client-Only vs Backend Architectures]]"
  - "[[API - Webhooks vs Polling]]"
  - "[[Android - App Lifecycle]]"
sources:
  - https://developer.android.com/training/monitoring-device-state/doze-standby
  - https://developer.android.com/topic/performance/appstandby
  - https://developer.android.com/develop/background-work/services/fgs
updated: 2026-08-18
---

# Background Limits and Doze

Android does not let apps decide how often they run. The system does, based on
how much the user actually uses the app and how the device is being treated —
and it has grown steadily stricter with every release. This is the note that
explains why "refresh every five minutes" is not a thing you can build, and why
the dashboard's honest promise is *live while open, best-effort otherwise*.

Specific thresholds, bucket names and per-release behaviour are
`<verify current>`: this area changes more than any other in the platform, and
OEM battery managers layer additional restrictions on top that Google does not
document.

## The layers of restriction

They stack. Passing one does not exempt you from the next.

| Layer | Triggered by | Effect on background work |
|---|---|---|
| Doze | Device idle, screen off, unplugged | Work batched into maintenance windows; network suspended between them |
| App Standby buckets | How recently and often the user opens your app | Progressively longer minimum gaps between jobs |
| Background execution limits | App not in the foreground | Background services largely unavailable |
| Battery optimisation | System or user setting | Further deferral |
| OEM battery managers | Vendor-specific, often aggressive | Can stop background work entirely |

## Doze

When a device sits unused with the screen off, it enters Doze. Deferred work
does not run continuously; it is collected and released in **maintenance
windows**, which grow further apart the longer the device stays idle.

```text
screen off ──► idle ──► [ maintenance ] ─── longer idle ─── [ maintenance ] ...
                            ▲                                     ▲
                     deferred work runs                  and again, less often
```

The practical consequence for a polling client: a phone left on a desk overnight
does not sync every fifteen minutes. It syncs a handful of times, in bursts.
The `WorkManager` interval is a floor on *how often you may ask*, not a promise
of how often you run — see [[Android - WorkManager]].

## App Standby buckets

The system sorts apps by usage into buckets, from actively used down to rarely
used, and applies increasingly long minimum intervals between their jobs. An app
the user opens daily gets treated well; one opened weekly does not.

This produces a feedback loop worth naming: an app that is not opened syncs less,
so it is more stale when opened, so it feels less useful. A dashboard has to be
worth opening — the background path cannot carry it alone.

## What this means for the design

| Assumption | Reality |
|---|---|
| "Refresh every 5 minutes" | Clamped to 15, then deferred further |
| "Always current when opened" | It is current as of the last window that ran |
| "Background sync is enough" | It is not. Foreground refresh is the primary path |
| "The badge count is live" | It is as live as the last successful sync |

Three consequences follow, and all three belong in the app:

1. **Pull-to-refresh is not a nicety.** It is the only mechanism the user
   controls, and the only one with predictable latency.
2. **Refresh on foreground.** Opening the app is the strongest possible signal
   that data is about to be read.
3. **Show the last successful sync time.** Staleness the user can see is a
   different product from staleness they discover — see
   [[Android - State and ViewModel]].

## Foreground services are not the loophole

A foreground service runs with a persistent notification and is exempt from most
of this. It is the right tool for navigation, media playback or an active
upload — work the user has explicitly started and can see.

Using one to poll an API in the background is an abuse: it drains battery, shows
a permanent notification the user did not ask for, requires a declared type that
must match a legitimate use case, and is a plausible route to store rejection.
Requirements and permitted types are `<verify current>`.

For genuine low-latency push, the mechanism is a server sending FCM — which
means a backend, which is [[API - Client-Only vs Backend Architectures|Option
B]]. That is the real trade: latency costs a server.

## Testing it

The emulator does not reproduce Doze faithfully, and OEM managers not at all.
Force the states with `adb`:

```bash
adb shell dumpsys deviceidle force-idle    # enter Doze
adb shell dumpsys deviceidle unforce       # leave it
adb shell am set-standby-bucket <package> rare
```

Then leave a real device unplugged and idle overnight and check whether sync
actually happened. Exact command syntax is `<verify current>`.

## ⚠️ Gotchas

- ⚠️ **Background sync can simply not run for hours**, with no error and no
  callback. The app looks broken to the user and healthy in your logs. Design
  every screen to show its own freshness rather than implying it is current.
- ⚠️ **Testing only in the foreground or on an emulator proves nothing.** These
  restrictions are absent in exactly the conditions you develop under.
- ⚠️ **OEM battery managers can kill background work entirely**, and are not
  documented by Google. On affected devices the fix is a user-granted exemption,
  which you must ask for honestly rather than nag for.
- ⚠️ **Do not use a foreground service to poll.** It is visible, expensive,
  requires a matching service type, and is not what the mechanism is for.
- **Asking to disable battery optimisation is a last resort**, restricted by
  policy, and users refuse it — reasonably.
- **Constraints compound with Doze.** `requiresCharging` plus Doze plus a rare
  bucket can mean never.
- **A `304`-heavy poller is cheap on quota but not free on battery.** Each wake
  still costs a radio activation — see [[API - Caching and ETags]].

---

## Related

- [[Android - WorkManager]]
- [[API - Client-Only vs Backend Architectures]]
- [[API - Webhooks vs Polling]]
- [[Android - App Lifecycle]]

## Sources

- <https://developer.android.com/training/monitoring-device-state/doze-standby>
- <https://developer.android.com/topic/performance/appstandby>
- <https://developer.android.com/develop/background-work/services/fgs>
