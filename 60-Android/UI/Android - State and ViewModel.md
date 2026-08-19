---
title: State and ViewModel
domain: android
section: "69"
category: ui
difficulty: intermediate
danger: medium
tags:
  - android/ui
  - android/state
commands: []
endpoints: []
dashboard_relevant: true
mobile_relevant: true
related:
  - "[[Android - Jetpack Compose]]"
  - "[[Android - Coroutines and Flow]]"
  - "[[Android - App Lifecycle]]"
  - "[[Android - Layered Architecture]]"
sources:
  - https://developer.android.com/topic/libraries/architecture/viewmodel
  - https://developer.android.com/topic/architecture/ui-layer/state-production
  - https://developer.android.com/develop/ui/compose/state
updated: 2026-08-18
---

# State and ViewModel

A ViewModel exists to outlive the UI. It survives configuration changes, holds
the state a screen is built from, and is the boundary where data-layer results
become something renderable. For a polling client there is a second, less
obvious job: it is the place that decides **when observation stops**, and
getting that wrong means firing requests at a screen nobody is looking at.

## State hoisting

State moves up, events move down.

```kotlin
// Stateless: fully controlled by its caller, trivially previewable and testable.
@Composable
fun SearchField(query: String, onQueryChange: (String) -> Unit) {
    TextField(value = query, onValueChange = onQueryChange)
}
```

The rule of thumb: hoist state to the lowest common ancestor that needs it. If
only one composable reads and writes it, `remember` is correct; if the data
layer or another screen cares, it belongs in the ViewModel.

## Modelling the whole screen as one type

```kotlin
sealed interface PullsUiState {
    data object Loading : PullsUiState
    data class Success(
        val pulls: List<PullRequest>,
        val lastSyncedAt: Instant?,
        val refreshing: Boolean,
    ) : PullsUiState
    data class Error(val message: String, val cached: List<PullRequest>) : PullsUiState
}
```

A sealed hierarchy makes illegal combinations unrepresentable. Three independent
booleans — `isLoading`, `hasError`, `isEmpty` — permit eight states of which
most are nonsense, and the UI ends up with defensive branches for combinations
that should never occur.

Note that `Error` carries `cached`. In an offline-first app a failed refresh is
not an empty screen: the database still has the last good data, so the honest
rendering is stale content plus an error banner — see
[[Android - Offline First and Room]].

## Producing state

```kotlin
class PullsViewModel(
    private val repository: PullRepository,
    savedState: SavedStateHandle,
) : ViewModel() {

    private val repoId: String = checkNotNull(savedState["repoId"])
    private val refreshing = MutableStateFlow(false)

    val uiState: StateFlow<PullsUiState> =
        combine(
            repository.observePulls(RepoId(repoId)),
            refreshing,
        ) { pulls, isRefreshing ->
            PullsUiState.Success(pulls, repository.lastSyncedAt(), isRefreshing)
        }.stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5_000),
            initialValue = PullsUiState.Loading,
        )

    fun refresh() {
        viewModelScope.launch {
            refreshing.value = true
            repository.refresh(RepoId(repoId))
            refreshing.value = false
        }
    }
}
```

Two details carry most of the weight.

`viewModelScope` is cancelled when the ViewModel is cleared, so nothing outlives
the screen. `SharingStarted.WhileSubscribed` stops the upstream flow when the
last collector goes away, with a grace period so that a rotation does not tear
down and rebuild the pipeline. Using `SharingStarted.Eagerly` here would keep
the database query — and anything chained to it — running forever.

## Collecting with lifecycle awareness

```kotlin
@Composable
fun PullsScreen(viewModel: PullsViewModel) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()

    when (state) {
        is PullsUiState.Loading -> LoadingIndicator()
        is PullsUiState.Success -> PullList(state.pulls)
        is PullsUiState.Error -> PullList(state.cached, banner = state.message)
    }
}
```

`collectAsStateWithLifecycle` stops collecting when the UI stops and resumes on
return. Plain `collectAsState` does not: it keeps collecting while the app is in
the background. The artifact that provides the lifecycle-aware variant is
`<verify current>`.

## One-time events

Navigation, snackbars and "copied to clipboard" are events, not state. Putting
them in a `StateFlow` replays them: rotate the device and the snackbar appears
again.

| Approach | Behaviour |
|---|---|
| `StateFlow` | Replays on every new collector. Wrong for events |
| `Channel` as `receiveAsFlow` | Delivered once, to one collector |
| Event in state plus explicit `onConsumed` | Verbose, but survives process death |

## ⚠️ Gotchas

- ⚠️ **`collectAsState` without lifecycle awareness keeps collecting in the
  background.** For this dashboard that means a database subscription, and
  anything upstream of it, running while the app is not visible — battery and
  rate-limit budget spent on a screen the user cannot see.
- ⚠️ **`SharingStarted.Eagerly` never stops.** It is the same leak one layer
  down, and it looks deliberate in review. Prefer `WhileSubscribed`.
- ⚠️ **Events modelled as state replay on rotation.** A navigation event stored
  in a `StateFlow` re-navigates every time a new collector subscribes.
- ⚠️ **Never hold a `Context`, an Activity or a View in a ViewModel.** It
  outlives them by design, so the reference leaks exactly the object it was
  meant to survive.
- **Do not put the whole DTO in the UI state.** Map to a domain model at the
  repository boundary — see [[Android - Layered Architecture]].
- **`SavedStateHandle` is for identity, not payloads.** The repo id belongs
  there; the pull request list does not — see [[Android - App Lifecycle]].
- **Show the last successful sync time in the UI.** Background work is
  best-effort, so the user needs to see staleness rather than guess at it — see
  [[Android - Background Limits and Doze]].

---

## Related

- [[Android - Jetpack Compose]]
- [[Android - Coroutines and Flow]]
- [[Android - App Lifecycle]]
- [[Android - Layered Architecture]]

## Sources

- <https://developer.android.com/topic/libraries/architecture/viewmodel>
- <https://developer.android.com/topic/architecture/ui-layer/state-production>
- <https://developer.android.com/develop/ui/compose/state>
