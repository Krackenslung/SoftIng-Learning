---
title: Layered Architecture
domain: android
section: "65"
category: architecture
difficulty: intermediate
danger: low
tags:
  - android/architecture
  - android/patterns
commands: []
endpoints: []
dashboard_relevant: true
mobile_relevant: true
related:
  - "[[API - Client-Only vs Backend Architectures]]"
  - "[[Android - Offline First and Room]]"
  - "[[Android - Dependency Injection]]"
  - "[[Android - Networking]]"
sources:
  - https://developer.android.com/topic/architecture
  - https://developer.android.com/topic/architecture/data-layer
  - https://developer.android.com/topic/architecture/recommendations
updated: 2026-08-18
---

# Layered Architecture

Layering is not decoration: it is the mechanism that keeps a decision reversible.
This dashboard runs without a backend, and that choice is documented and
deliberate — but it is a choice, not a law. Putting the network behind an
interface is precisely what makes moving to
[[API - Client-Only vs Backend Architectures|Option B]] a change in one module
rather than a rewrite.

## The three layers

| Layer | Owns | Knows about |
|---|---|---|
| UI | Screens, state holders | Domain layer only |
| Domain *(optional)* | Business rules, use cases | Data layer only |
| Data | Repositories, network, database | Nothing above it |

Dependencies point **downward only**. The data layer must never reference a
ViewModel, a Composable or an Android `Context` beyond what it needs to open a
database. When that rule holds, the data layer is testable on the JVM without an
emulator, which is most of the practical payoff.

The domain layer is optional. Add it when business rules exist that belong to
neither the UI nor a single repository — the "needs my action" priority ordering
in [[Dev Dashboard - Data Model]] is exactly such a rule.

## The repository is the seam

```kotlin
interface PullRepository {
    fun observePulls(repo: RepoId): Flow<List<PullRequest>>
    suspend fun refresh(repo: RepoId): Result<Unit>
}
```

Everything above this interface is unaware of where pull requests come from. The
client-only implementation talks to GitHub directly and caches in Room; a future
backed implementation would talk to your own server. Same interface, same UI.

```kotlin
class DefaultPullRepository(
    private val api: GitHubApi,        // Retrofit or Apollo
    private val dao: PullDao,          // Room
) : PullRepository {

    // The database is the single source of truth. The UI never sees the network.
    override fun observePulls(repo: RepoId): Flow<List<PullRequest>> =
        dao.observeByRepo(repo.value).map { rows -> rows.map(PullEntity::toDomain) }

    override suspend fun refresh(repo: RepoId): Result<Unit> = runCatching {
        val response = api.pulls(repo.owner, repo.name)
        dao.upsertAll(response.map { it.toEntity(repo) })
    }
}
```

Note what the UI observes: the **database**, not the network call. A refresh
writes to Room and the `Flow` emits; the screen has no idea a request happened.
That is what makes offline work and what makes a failed refresh non-destructive
— see [[Android - Offline First and Room]].

## Three models, on purpose

| Model | Shape decided by | Lives in |
|---|---|---|
| DTO | The API's JSON | Data layer, never leaves it |
| Entity | Your database schema | Data layer, never leaves it |
| Domain model | What the app actually means | Crosses layers freely |

Collapsing these into one class is the most tempting shortcut in the whole
architecture, and it welds three independent rates of change together: GitHub
adds a field, your database needs a migration, and your UI recompiles. Keeping
them separate costs mapping functions and buys the ability to absorb an API
change in one file.

It also removes a class of bug the vault already documents: the `issues`
endpoint returns pull requests, and `state: "closed"` includes merged PRs. Those
are DTO facts. The domain model should expose `isMerged`, computed once at the
boundary, so the mistake cannot propagate — see
[[Bridge - GitHub API Conventions]].

## Where each concern lands

| Concern | Layer | Note |
|---|---|---|
| `ETag` storage and conditional requests | Data | [[API - Caching and ETags]] |
| Rate-limit budgeting | Data | [[API - Rate Limiting Strategies]] |
| Retry and backoff | Data | [[API - Idempotency and Retries]] |
| Token storage | Data | [[API - Token Storage on Public Clients]] |
| Background sync scheduling | Data, triggered by a Worker | [[Android - WorkManager]] |
| Loading and error state | UI | [[Android - State and ViewModel]] |

## ⚠️ Gotchas

- ⚠️ **A repository that returns network results directly defeats the design.**
  If `observePulls` emitted from the API instead of the database, every
  configuration change would refetch, offline would show nothing, and a failed
  request would blank the screen. Read from the database, always.
- ⚠️ **Do not let DTOs reach the UI.** A nullable field from the API becomes a
  nullable field in a Composable, and the API's naming becomes your naming
  forever. The mapping boundary is the only place to fix data traps once.
- ⚠️ **Layer violations compile fine.** Nothing stops a ViewModel importing
  Retrofit; the cost only appears later as untestable code. In a single-module
  project the boundary is a convention, so enforce it in review — or split
  modules and let Gradle enforce it, per
  [[Android - Project Structure]].
- **The domain layer is optional, and premature use cases are noise.** A use
  case that calls one repository method and returns is indirection with no
  benefit.
- **`Result` at the repository boundary beats exceptions crossing layers.** The
  UI needs to render failure, not catch it.

---

## Related

- [[API - Client-Only vs Backend Architectures]]
- [[Android - Offline First and Room]]
- [[Android - Dependency Injection]]
- [[Android - Networking]]

## Sources

- <https://developer.android.com/topic/architecture>
- <https://developer.android.com/topic/architecture/data-layer>
- <https://developer.android.com/topic/architecture/recommendations>
