---
title: App Lifecycle
domain: android
section: "64"
category: foundations
difficulty: intermediate
danger: medium
tags:
  - android/lifecycle
  - android/state
commands: []
endpoints: []
dashboard_relevant: true
mobile_relevant: true
related:
  - "[[Android - State and ViewModel]]"
  - "[[Android - WorkManager]]"
  - "[[Android - Background Limits and Doze]]"
  - "[[Android - Layered Architecture]]"
sources:
  - https://developer.android.com/guide/components/activities/activity-lifecycle
  - https://developer.android.com/topic/libraries/architecture/saving-states
  - https://developer.android.com/topic/libraries/architecture/coroutines
updated: 2026-08-18
---

# App Lifecycle

On a desktop, a process runs until it exits. On Android it runs until the system
decides it needs the memory, and that decision arrives without warning and
without a callback you can rely on. Every piece of state your app holds is
therefore either persisted or gone — and for a dashboard that syncs in the
background, "gone" means silently refetching data you already had, at the cost
of rate-limit budget.

## The Activity lifecycle

| Callback | Means | Do here |
|---|---|---|
| `onCreate` | Instance created | Wire up, restore state |
| `onStart` | Becoming visible | Start observing |
| `onResume` | Interactive, in foreground | Nothing extra, usually |
| `onPause` | Losing focus, still visible | Stop anything sensitive to being watched |
| `onStop` | No longer visible | Stop observing, release heavy resources |
| `onDestroy` | Being torn down | **May never be called** |

`onDestroy` is not a guarantee. If the system kills the process, none of the
teardown callbacks run. Anything that must survive has to be written down before
that point, not during it.

## Three different kinds of "the app went away"

These are constantly conflated and behave completely differently:

| Event | Process | ViewModel | UI state |
|---|---|---|---|
| Configuration change (rotation, theme, locale) | Survives | **Survives** | Restored from saved state |
| User navigates back / finishes | Survives | Cleared | Gone, intentionally |
| **System process death** | **Killed** | Gone | Only what was persisted |

Process death is the one that gets missed, because it almost never happens
during development — your app is in the foreground with a debugger attached.
It happens constantly in real use, when the user switches away for an hour.

> [!warning] Test it deliberately
> Process death does not reproduce by accident. Background the app and kill the
> process from the IDE, or use the developer option that limits background
> processes. Anything that breaks only after an hour in a pocket is this.

## Surviving each level

```kotlin
class PullsViewModel(
    private val savedState: SavedStateHandle,
    private val repository: PullRepository,
) : ViewModel() {

    // Survives process death: written to the saved-state bundle.
    var selectedRepo: String?
        get() = savedState["selectedRepo"]
        set(value) { savedState["selectedRepo"] = value }

    // Survives rotation only: lives and dies with the ViewModel.
    private val _refreshing = MutableStateFlow(false)
    val refreshing: StateFlow<Boolean> = _refreshing.asStateFlow()
}
```

`SavedStateHandle` is for **small** UI state — a selected tab, a scroll key, a
query string. It is serialised into a system bundle with a hard size limit, and
exceeding it crashes the app rather than truncating.

Anything larger belongs in the database, which is the actual source of truth —
see [[Android - Offline First and Room]] and [[Android - Layered Architecture]].

## Collecting only while visible

A flow collected without regard to lifecycle keeps running after the UI is gone,
which for a polling client means requests fired at a screen nobody is looking at.

```kotlin
// In a Compose UI: stops collecting when the UI stops.
val state by viewModel.uiState.collectAsStateWithLifecycle()
```

```kotlin
// Outside Compose: the same guarantee, explicitly.
lifecycleScope.launch {
    repeatOnLifecycle(Lifecycle.State.STARTED) {
        viewModel.uiState.collect { render(it) }
    }
}
```

`repeatOnLifecycle` cancels the block on `STOP` and restarts it on `START`. The
API level and artifact that provide these are `<verify current>`.

## What this means for sync state

The rule for this dashboard: **the last successful sync timestamp, the stored
`ETag`s and the cached payloads are persisted, never held in memory.** After a
process death the app must be able to resume without refetching, because
refetching costs quota — see [[API - Caching and ETags]].

Background work is separate from all of this. `WorkManager` schedules against
the system, not the Activity, so it survives process death by design — see
[[Android - WorkManager]].

## ⚠️ Gotchas

- ⚠️ **The system can kill the process at any moment with no callback.** State
  held only in memory is lost, and the failure looks like the app "forgetting"
  things intermittently. Persist anything you cannot cheaply rebuild.
- ⚠️ **`onDestroy` is not a save point.** It is skipped on process death, which
  is exactly the case you were trying to protect against.
- ⚠️ **`SavedStateHandle` has a size limit and crashes when exceeded.** Putting
  a list of API responses in it produces a `TransactionTooLargeException` that
  only appears with real data volumes, long after the code was written.
- ⚠️ **`collectAsState` without lifecycle awareness keeps collecting in the
  background.** For a client that polls, this burns battery and rate-limit
  budget for a screen that is not visible. Use
  `collectAsStateWithLifecycle`.
- **Rotation is not process death.** Code that survives rotation can still lose
  everything to a real kill, so testing rotation proves nothing about the
  harder case.
- **Do not fight configuration changes** by locking orientation or handling them
  manually. It breaks multi-window, theme switching and locale changes, and the
  ViewModel already solves the problem.

---

## Related

- [[Android - State and ViewModel]]
- [[Android - WorkManager]]
- [[Android - Background Limits and Doze]]
- [[Android - Layered Architecture]]

## Sources

- <https://developer.android.com/guide/components/activities/activity-lifecycle>
- <https://developer.android.com/topic/libraries/architecture/saving-states>
- <https://developer.android.com/topic/libraries/architecture/coroutines>
