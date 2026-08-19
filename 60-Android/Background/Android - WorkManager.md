---
title: WorkManager
domain: android
section: "74"
category: background
difficulty: intermediate
danger: medium
tags:
  - android/background
  - android/sync
commands: []
endpoints: []
dashboard_relevant: true
mobile_relevant: true
related:
  - "[[API - Webhooks vs Polling]]"
  - "[[API - Client-Only vs Backend Architectures]]"
  - "[[Android - Background Limits and Doze]]"
  - "[[API - Idempotency and Retries]]"
  - "[[Android - Dependency Injection]]"
sources:
  - https://developer.android.com/topic/libraries/architecture/workmanager
  - https://developer.android.com/topic/libraries/architecture/workmanager/how-to/define-work
  - https://developer.android.com/topic/libraries/architecture/workmanager/how-to/managing-work
updated: 2026-08-18
---

# WorkManager

This note is not really about a library. It is about the consequence of a
decision already made: the dashboard has no backend, so it cannot receive
webhooks, so change detection is **polling** — see
[[API - Client-Only vs Backend Architectures]] and
[[API - Webhooks vs Polling]]. `WorkManager` is how a phone polls without
being killed for it, and its constraints are what set the dashboard's real
latency floor.

The library version and artifacts are `<verify current>`.

## What it guarantees, and what it does not

| | Guarantee |
|---|---|
| Survives process death | Yes — the queue is persisted to disk |
| Survives reboot | Yes |
| Runs at a precise time | **No** |
| Runs at the requested interval | **No** — that is a minimum, not a schedule |
| Runs at all, eventually, if constraints are met | Yes |

`WorkManager` is a *deferrable* work scheduler. It trades timing for
reliability, which is the correct trade for sync and the wrong one for anything
the user is waiting on.

## Periodic sync

```kotlin
val sync = PeriodicWorkRequestBuilder<SyncWorker>(15, TimeUnit.MINUTES)
    .setConstraints(
        Constraints.Builder()
            .setRequiredNetworkType(NetworkType.CONNECTED)
            .setRequiresBatteryNotLow(true)
            .build(),
    )
    .setBackoffCriteria(BackoffPolicy.EXPONENTIAL, 30, TimeUnit.SECONDS)
    .build()

WorkManager.getInstance(context).enqueueUniquePeriodicWork(
    "github-sync",
    ExistingPeriodicWorkPolicy.KEEP,     // do not stack duplicates on every launch
    sync,
)
```

> [!warning] The 15-minute floor
> Periodic work has a documented **minimum interval of 15 minutes**. Requesting
> less does not fail — it is silently clamped. This is the architectural
> constraint of the dashboard: background freshness cannot be better than about
> fifteen minutes, and in practice it is worse. Treat this figure as
> `<verify current>` before relying on it, since platform behaviour around
> background work changes between releases.

`ExistingPeriodicWorkPolicy.KEEP` matters more than it looks: enqueueing on every
app launch with `REPLACE` resets the interval each time, so a frequently opened
app never reaches its own schedule.

## The worker

```kotlin
class SyncWorker(
    context: Context,
    params: WorkerParameters,
    private val repository: PullRepository,   // needs a WorkerFactory
) : CoroutineWorker(context, params) {

    override suspend fun doWork(): Result = when (val outcome = repository.syncAll()) {
        is SyncOutcome.Success -> Result.success()
        is SyncOutcome.RateLimited -> Result.retry()     // backoff applies
        is SyncOutcome.Transient -> if (runAttemptCount < 3) Result.retry()
                                    else Result.failure()
        is SyncOutcome.Unauthorized -> Result.failure()  // retrying cannot help
    }
}
```

The mapping from failure to `Result` is the whole design:

| Situation | Return | Why |
|---|---|---|
| Worked | `success()` | — |
| 429 or 403 with quota exhausted | `retry()` | Backoff is exactly right |
| Network error, 5xx | `retry()`, bounded by `runAttemptCount` | Transient |
| 401, bad token | `failure()` | Deterministic; retrying burns battery |
| Nothing changed (all 304) | `success()` | A no-op sync is a success |

`Result.retry()` uses the backoff policy, which is exponential from the value
you set. That is the same policy described in
[[API - Idempotency and Retries]] — but note that `WorkManager` does not add
jitter, so many devices recovering from the same outage return together. For a
client hitting a shared API, spreading the initial enqueue slightly is worth
doing.

Constructor dependencies require a custom `WorkerFactory`, or the worker fails
to instantiate at runtime — see [[Android - Dependency Injection]].

## Expedited and one-off work

Pull-to-refresh should **not** go through `WorkManager`. The user is watching;
run it in `viewModelScope` and show the result. `WorkManager` is for the
unattended path.

One-off work is right for something that must survive process death but is not
periodic — marking notifications read while offline, for example, replayed when
connectivity returns.

## Observing state

```kotlin
val lastSync: Flow<WorkInfo?> = WorkManager.getInstance(context)
    .getWorkInfosForUniqueWorkFlow("github-sync")
    .map { it.firstOrNull() }
```

Surface this. Because scheduling is best-effort, the user needs to see *when the
data is from* rather than assume it is current — see
[[Android - State and ViewModel]].

## ⚠️ Gotchas

- ⚠️ **Requesting an interval below 15 minutes is silently clamped.** No error,
  no warning. A design that assumes five-minute freshness is wrong from the
  first line, and nothing in the API will tell you.
- ⚠️ **A worker with constructor arguments crashes at runtime.** The default
  factory cannot build it, and it fails in the background where nothing is on
  screen to show it. The symptom is sync that simply never happens.
- ⚠️ **`ExistingPeriodicWorkPolicy.REPLACE` on every launch restarts the
  interval**, so an app opened often never completes a background cycle.
- ⚠️ **Unbounded `Result.retry()` is a battery and quota drain.** Always bound it
  with `runAttemptCount`, and never retry a deterministic failure such as 401.
- ⚠️ **`doWork` runs with a time limit and can be stopped mid-flight.** Write
  results transactionally so a stopped worker leaves no half-applied sync — see
  [[Android - Offline First and Room]].
- **The emulator does not model Doze faithfully.** Background sync that works
  there proves little; test on a real device left idle — see
  [[Android - Background Limits and Doze]].
- **Constraints delay work indefinitely if never met.** `setRequiresCharging` on
  a sync job means a phone that is never plugged in never syncs.
- **Do not use it for anything the user is waiting on.** It is deferrable by
  design.

---

## Related

- [[API - Webhooks vs Polling]]
- [[API - Client-Only vs Backend Architectures]]
- [[Android - Background Limits and Doze]]
- [[API - Idempotency and Retries]]
- [[Android - Dependency Injection]]

## Sources

- <https://developer.android.com/topic/libraries/architecture/workmanager>
- <https://developer.android.com/topic/libraries/architecture/workmanager/how-to/define-work>
- <https://developer.android.com/topic/libraries/architecture/workmanager/how-to/managing-work>
