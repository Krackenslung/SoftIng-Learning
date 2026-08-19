---
title: Paging
domain: android
section: "73"
category: data
difficulty: advanced
danger: medium
tags:
  - android/data
  - android/paging
commands: []
endpoints: []
dashboard_relevant: true
mobile_relevant: true
related:
  - "[[API - Pagination Patterns]]"
  - "[[Android - Offline First and Room]]"
  - "[[Android - Networking]]"
  - "[[Dev Dashboard - API Map]]"
sources:
  - https://developer.android.com/topic/libraries/architecture/paging/v3-overview
  - https://developer.android.com/topic/libraries/architecture/paging/v3-paged-data
  - https://developer.android.com/topic/libraries/architecture/paging/v3-network-db
updated: 2026-08-18
---

# Paging

Paging solves a UI problem — load a long list incrementally without holding it
all in memory — but the correctness problems it inherits are the ones described
in [[API - Pagination Patterns]]. The library gives you a place to put a key and
a place to fetch the next chunk; it does not decide whether that key is stable
under concurrent writes. That part is still yours.

The Paging artifact version is `<verify current>`.

## Two shapes, and only one is right here

| Setup | Source of truth | Works offline |
|---|---|---|
| `PagingSource` straight from the network | The network | **No** |
| `RemoteMediator` plus Room | The database | Yes |

For a client whose whole design says the database is authoritative, the second
is the only consistent choice — see [[Android - Offline First and Room]]. The
network-only variant refetches on every rotation and shows nothing without a
connection.

## The key type mirrors the API's scheme

This is where [[API - Pagination Patterns]] maps directly onto code:

| API scheme | Paging key | Notes |
|---|---|---|
| `?page=2` offset paging | `Int` | Subject to offset drift |
| `?after=<cursor>` | `String` | Opaque; never construct it |
| `Link` header | `String` — the whole next URL | Follow it, do not rebuild it |

```kotlin
@OptIn(ExperimentalPagingApi::class)
class PullsRemoteMediator(
    private val repoId: RepoId,
    private val api: GitHubApi,
    private val db: AppDatabase,
) : RemoteMediator<Int, PullEntity>() {

    override suspend fun load(
        loadType: LoadType,
        state: PagingState<Int, PullEntity>,
    ): MediatorResult {
        val page = when (loadType) {
            LoadType.REFRESH -> 1
            LoadType.PREPEND ->
                return MediatorResult.Success(endOfPaginationReached = true)
            LoadType.APPEND -> db.keyDao().nextPage(repoId.value)
                ?: return MediatorResult.Success(endOfPaginationReached = true)
        }

        return try {
            val response = api.pulls(repoId.owner, repoId.name, page = page)
            val body = response.body().orEmpty()
            val next = parseLink(response.headers()["link"])?.next   // absent = done

            db.withTransaction {
                if (loadType == LoadType.REFRESH) db.pullDao().clear(repoId.value)
                db.pullDao().upsertAll(body.map { it.toEntity(repoId) })
                db.keyDao().upsert(RemoteKey(repoId.value, nextPage = next?.pageNumber))
            }

            MediatorResult.Success(endOfPaginationReached = next == null)
        } catch (e: IOException) {
            MediatorResult.Error(e)          // Paging surfaces this as LoadState.Error
        }
    }
}
```

Three things in that function decide whether the list is correct.

**Termination is the absence of `rel="next"`**, not a short page. GitHub can
return fewer items than `per_page` mid-result.

**The transaction covers the clear, the rows and the key.** A crash between them
leaves a key pointing at a page whose rows were never written.

**`REFRESH` clears the scope first.** Without it, upsert-only paging accumulates
rows that were deleted upstream — the same leak described in
[[Android - Offline First and Room]].

## Consuming it

```kotlin
val pulls: Flow<PagingData<PullRequest>> = Pager(
    config = PagingConfig(pageSize = 100, enablePlaceholders = false),
    remoteMediator = PullsRemoteMediator(repoId, api, db),
) { db.pullDao().pagingSource(repoId.value) }
    .flow
    .map { paging -> paging.map(PullEntity::toDomain) }
    .cachedIn(viewModelScope)
```

`cachedIn` is not optional: without it the flow restarts on every configuration
change and re-fetches. The `pageSize` should match what you ask the API for —
100 on GitHub, the documented maximum, because fewer requests is the entire
saving here.

## Is paging even needed?

For this dashboard, mostly not. `GET /notifications` returns one page, and the
GraphQL query in [[Dev Dashboard - API Map]] deliberately collapses the PR view
into a single call. Paging earns its complexity on genuinely unbounded lists —
commit history, an org's repository list — and costs a `RemoteMediator`, a key
table and a migration on everything else.

## ⚠️ Gotchas

- ⚠️ **Offset keys drift under concurrent writes.** A PR opened while the user
  scrolls shifts every subsequent page, duplicating one item and — worse —
  skipping another. Prefer cursors or the `Link` header where the endpoint
  offers them; see [[API - Pagination Patterns]].
- ⚠️ **Do not stop on a short page.** Stop when `rel="next"` is absent. Short
  pages occur mid-result after server-side filtering.
- ⚠️ **Write rows and remote keys in one transaction.** Otherwise a crash leaves
  a key that points past data that was never stored, and the list silently ends
  early on the next launch.
- ⚠️ **`REFRESH` without clearing leaves deleted items behind**, inflating every
  count derived from the table.
- ⚠️ **An unbounded pager can burn the whole rate-limit budget.** A malformed
  `next` that never terminates loops at full speed. Cap total pages — see
  [[API - Rate Limiting Strategies]].
- **`cachedIn` or you refetch on rotation.** This is the single most common
  Paging bug.
- **Placeholders need an accurate total count.** Cursor APIs do not provide one,
  so leave them disabled.
- **Do not construct cursors.** They are opaque and their format is unsupported.

---

## Related

- [[API - Pagination Patterns]]
- [[Android - Offline First and Room]]
- [[Android - Networking]]
- [[Dev Dashboard - API Map]]

## Sources

- <https://developer.android.com/topic/libraries/architecture/paging/v3-overview>
- <https://developer.android.com/topic/libraries/architecture/paging/v3-paged-data>
- <https://developer.android.com/topic/libraries/architecture/paging/v3-network-db>
