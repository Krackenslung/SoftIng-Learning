---
title: Jetpack Compose
domain: android
section: "68"
category: ui
difficulty: intermediate
danger: low
tags:
  - android/ui
  - android/compose
commands: []
endpoints: []
dashboard_relevant: false
mobile_relevant: true
related:
  - "[[Android - State and ViewModel]]"
  - "[[Android - Navigation]]"
  - "[[Android - Layered Architecture]]"
sources:
  - https://developer.android.com/develop/ui/compose/mental-model
  - https://developer.android.com/develop/ui/compose/lifecycle
  - https://developer.android.com/develop/ui/compose/performance
updated: 2026-08-18
---

# Jetpack Compose

Compose replaces "find the widget and mutate it" with "describe the UI for this
state". The framework decides what actually changed. That inversion is the whole
mental model, and every Compose problem — stale UI, jank, a list that scrolls
badly — is some version of the framework being unable to tell what changed,
because you did not give it a way to know.

## Declarative versus imperative

| | Views | Compose |
|---|---|---|
| You write | Layout XML plus mutation code | A function of state |
| Updating | `textView.text = title` | Emit again with new state |
| State lives | In the widget | Hoisted, outside the UI |
| Risk | Widget and model drift apart | Recomposing more than necessary |

The Views failure mode is *correctness*: two sources of truth diverge. The
Compose failure mode is *performance*: correctness is structural, but you can
recompose far more than needed.

## Composables and recomposition

```kotlin
@Composable
fun PullRow(pull: PullRequest, onClick: (Int) -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick(pull.number) }
            .padding(horizontal = 16.dp, vertical = 12.dp),
    ) {
        Text(text = pull.title, modifier = Modifier.weight(1f))
        if (pull.isDraft) Text(text = "draft")
    }
}
```

A composable is a function with no return value that *emits* UI. When its inputs
change, Compose calls it again — recomposition — and skips functions whose
inputs are unchanged.

That skipping only works if Compose can compare inputs. A stable, immutable
`data class` compares cheaply; a mutable class, or a lambda that is a new object
every frame, cannot be shown to be unchanged and forces recomposition.

> [!warning] Recomposition is not ordered, timed or guaranteed once
> A composable can run many times per frame, in any order, in parallel, and can
> be abandoned mid-flight. Never put a side effect — a network call, a write, a
> counter increment — directly in the composable body. Use the effect APIs.

## Modifiers

Order matters, and it composes left to right:

```kotlin
Modifier.padding(16.dp).background(Color.Red)   // padding OUTSIDE the red
Modifier.background(Color.Red).padding(16.dp)   // padding INSIDE the red
```

This trips everyone once. The modifier chain is a pipeline, not a property bag.

## `remember` and `rememberSaveable`

```kotlin
// Survives recomposition. Lost on configuration change.
val listState = rememberLazyListState()

// Survives configuration change too: stored in the saved-state bundle.
var query by rememberSaveable { mutableStateOf("") }
```

| API | Survives recomposition | Survives rotation | Survives process death |
|---|---|---|---|
| plain `val` | No | No | No |
| `remember` | Yes | No | No |
| `rememberSaveable` | Yes | Yes | Yes, within bundle limits |
| ViewModel | Yes | Yes | Only via `SavedStateHandle` |

`rememberSaveable` writes into the same size-limited bundle described in
[[Android - App Lifecycle]]. It is for a query string or a selected tab, never
for a list of API responses.

## Lists need keys

```kotlin
LazyColumn {
    items(
        items = pulls,
        key = { pull -> "${pull.repoId}#${pull.number}" },   // stable identity
    ) { pull ->
        PullRow(pull = pull, onClick = onOpen)
    }
}
```

Without a key, Compose identifies items by position. Insert one row at the top
and every row below it is treated as changed: scroll position jumps, animations
run on the wrong items, and the whole visible list recomposes. With a stable key
it moves the existing items instead.

Use a key that is unique and does not change — the API's identifier, not the
index and not a hash of the whole object.

Compose artifacts, the BOM and the compiler plugin setup are `<verify current>`.

## ⚠️ Gotchas

- ⚠️ **Never perform side effects in a composable body.** It may run many times
  per frame and be abandoned, so a request fired there can be issued repeatedly
  and its result discarded — costing rate-limit budget for nothing. Effects go in
  `LaunchedEffect` or, better, in the ViewModel.
- ⚠️ **Unkeyed lists lose scroll position and animate the wrong rows.** For a
  dashboard that refreshes underneath the user, this reads as the list "jumping"
  at random.
- ⚠️ **Unstable parameters silently defeat skipping.** A `List` interface, a
  mutable class or a freshly created lambda make Compose assume "changed", and
  the subtree recomposes on every frame. The symptom is jank with no obvious
  cause.
- **Modifier order is semantic**, not stylistic. Read the chain as a sequence of
  wrappers from the outside in.
- **Do not hoist state into Compose that belongs to the ViewModel.** Screen
  state has a lifecycle longer than the composable — see
  [[Android - State and ViewModel]].
- **Previews are not a test.** They render with fabricated data on your machine;
  they say nothing about recomposition behaviour with real state.

---

## Related

- [[Android - State and ViewModel]]
- [[Android - Navigation]]
- [[Android - Layered Architecture]]

## Sources

- <https://developer.android.com/develop/ui/compose/mental-model>
- <https://developer.android.com/develop/ui/compose/lifecycle>
- <https://developer.android.com/develop/ui/compose/performance>
