---
title: Coroutines and Flow
domain: android
section: "72"
category: data
difficulty: intermediate
danger: medium
tags:
  - android/coroutines
  - android/concurrency
commands: []
endpoints: []
dashboard_relevant: true
mobile_relevant: true
related:
  - "[[API - Idempotency and Retries]]"
  - "[[Android - State and ViewModel]]"
  - "[[Android - WorkManager]]"
  - "[[Android - Networking]]"
sources:
  - https://developer.android.com/kotlin/coroutines
  - https://developer.android.com/kotlin/flow
  - https://kotlinlang.org/docs/coroutines-guide.html
updated: 2026-08-18
---

# Coroutines and Flow

A coroutine is work that can suspend without blocking a thread, and a `Flow` is
a sequence of values produced over time. The idea that makes both safe is
**structured concurrency**: every coroutine belongs to a scope, and cancelling
the scope cancels everything inside it. That is not a convenience — on Android
it is what guarantees a screen's work stops when the screen does, and what stops
a polling client from issuing requests nobody will read.

## `suspend`

```kotlin
suspend fun refresh(repo: RepoId): Result<Unit> {
    val response = api.pulls(repo.owner, repo.name)   // suspends, frees the thread
    dao.upsertAll(response.body().orEmpty().map { it.toEntity(repo) })
    return Result.success(Unit)
}
```

A `suspend` function can only be called from another `suspend` function or from
a coroutine builder. That restriction is the type system enforcing that
long-running work has somewhere to be cancelled from.

## Scopes decide lifetime

| Scope | Cancelled when | Use for |
|---|---|---|
| `viewModelScope` | The ViewModel is cleared | Screen-driven work |
| `lifecycleScope` | The lifecycle owner is destroyed | UI-bound work outside Compose |
| A `CoroutineScope` you own | You cancel it | Application-lifetime components |
| `GlobalScope` | **Never** | Nothing, in an app |

`GlobalScope` is not a shortcut for "runs in the background". It is a scope with
no owner, so nothing cancels it: the work continues after the screen is gone,
holds references that cannot be collected, and — for this dashboard — keeps
spending rate-limit budget on results that will be discarded. Background work
that must outlive the UI belongs to [[Android - WorkManager]], which is
scheduled by the system rather than orphaned by you.

## Dispatchers

| Dispatcher | For |
|---|---|
| `Dispatchers.Main` | UI updates |
| `Dispatchers.IO` | Blocking I/O: files, sockets, non-suspending SQL |
| `Dispatchers.Default` | CPU work: parsing, sorting, diffing |

A well-written suspend API is **main-safe** — it switches internally, so callers
never have to. Retrofit and Room already are, which is why the repository code
in this vault never wraps calls in `withContext(Dispatchers.IO)`. Adding it
"just in case" is noise that hides which functions genuinely block.

## Cancellation is cooperative

```kotlin
suspend fun syncAll(repos: List<RepoId>) {
    repos.forEach { repo ->
        ensureActive()        // throws if the scope was cancelled
        refresh(repo)
    }
}
```

Cancellation throws `CancellationException` at the next suspension point. Code
that never suspends never notices, which is how a long CPU loop keeps running
after the screen closed.

```kotlin
try {
    refresh(repo)
} catch (e: CancellationException) {
    throw e                  // never swallow this
} catch (e: IOException) {
    log(e)
}
```

⚠️ A blanket `catch (e: Exception)` swallows `CancellationException` and breaks
structured concurrency: the parent believes the child finished normally.

## Cold flows and hot flows

| | Cold (`flow { }`, Room queries) | Hot (`StateFlow`, `SharedFlow`) |
|---|---|---|
| Runs when | Someone collects | Always, once created |
| Per collector | A separate execution | Shared |
| Holds a value | No | `StateFlow` does |
| Right for | A request, a database query | Screen state, events |

Converting cold to hot is `stateIn`/`shareIn`, and the `SharingStarted` argument
is where the leak lives — see [[Android - State and ViewModel]].

## Operators worth knowing here

```kotlin
val results = queryFlow
    .debounce(300)                 // wait for typing to settle
    .distinctUntilChanged()        // ignore no-op changes
    .flatMapLatest { query ->      // cancel the previous search
        repository.search(query)
    }
    .catch { emit(SearchState.Error) }   // upstream failures only
```

`flatMapLatest` cancelling the previous request is the single most useful
operator for a search field: without it, every keystroke is a live request
competing for the same quota.

## Retries

`retryWhen` on a `Flow` is the idiomatic place for the backoff policy described
in [[API - Idempotency and Retries]]:

```kotlin
.retryWhen { cause, attempt ->
    if (cause !is IOException || attempt >= 3) return@retryWhen false
    delay(Random.nextLong(minOf(30_000, 500 shl attempt.toInt())))  // full jitter
    true
}
```

Retry only what is safe to repeat, and never a non-idempotent write.

## ⚠️ Gotchas

- ⚠️ **`GlobalScope` leaks work that nothing can cancel.** It survives the
  screen, the ViewModel and often the user's attention, spending battery and
  quota on results that are thrown away. There is no correct use of it in an app.
- ⚠️ **Never catch `CancellationException` without rethrowing.** A broad
  `catch (e: Exception)` does exactly this, and the result is coroutines that
  refuse to stop and a parent scope that thinks they succeeded.
- ⚠️ **`launch` swallows failures into the scope's handler; `async` holds them
  until `await()`.** An `async` whose result is never awaited fails silently —
  the classic way a background sync error disappears.
- ⚠️ **Cancellation needs a suspension point.** A tight CPU loop ignores it.
  Call `ensureActive()` inside long loops.
- **Do not wrap already-main-safe calls in `withContext(Dispatchers.IO)`.** It
  adds a thread switch and obscures which calls actually block.
- **`Dispatchers.IO` is a bounded pool.** Launching hundreds of parallel requests
  exhausts it and trips secondary rate limits anyway — see
  [[API - Rate Limiting Strategies]].
- **`catch` on a `Flow` only sees upstream failures.** An exception thrown inside
  `collect` is not caught by it.

---

## Related

- [[API - Idempotency and Retries]]
- [[Android - State and ViewModel]]
- [[Android - WorkManager]]
- [[Android - Networking]]

## Sources

- <https://developer.android.com/kotlin/coroutines>
- <https://developer.android.com/kotlin/flow>
- <https://kotlinlang.org/docs/coroutines-guide.html>
