---
title: Offline First and Room
domain: android
section: "66"
category: architecture
difficulty: advanced
danger: high
tags:
  - android/data
  - android/room
  - android/cache
commands: []
endpoints: []
dashboard_relevant: true
mobile_relevant: true
related:
  - "[[Dev Dashboard - Data Model]]"
  - "[[API - Caching and ETags]]"
  - "[[Android - Paging]]"
  - "[[Android - Layered Architecture]]"
sources:
  - https://developer.android.com/training/data-storage/room
  - https://developer.android.com/training/data-storage/room/migrating-db-versions
  - https://developer.android.com/topic/architecture/data-layer/offline-first
updated: 2026-08-18
---

# Offline First and Room

"Offline first" is not a feature for aeroplanes. It is the statement that **the
local database, not the network, is what the UI reads** — which makes the app
instant on launch, correct when the connection drops, and cheap against a rate
limit it cannot exceed. For a client with no backend, the local database is the
only cache that exists, so this note and [[API - Caching and ETags]] describe
the same mechanism at two altitudes.

## The shape

```text
UI ──observes──► Room ◄──writes── Repository ──requests──► GitHub
                  ▲                                            │
                  └────────────── 304: nothing to write ────────┘
```

Reads and writes are separate paths. The UI subscribes to the database once and
never waits on a request; a sync writes into the database and the subscription
emits. A failed sync writes nothing, so the screen keeps showing the last known
good state instead of an error.

## Entities, DAO, database

```kotlin
@Entity(tableName = "pull_request", primaryKey = ["repoId", "number"])
data class PullEntity(
    val repoId: String,
    val number: Int,
    val title: String,
    val isDraft: Boolean,
    val mergedAt: Instant?,          // null means not merged. See gotchas
    val updatedAt: Instant,
)
```

```kotlin
@Dao
interface PullDao {
    // Returns a Flow: Room re-emits automatically when the table changes.
    @Query("SELECT * FROM pull_request WHERE repoId = :repoId ORDER BY updatedAt DESC")
    fun observeByRepo(repoId: String): Flow<List<PullEntity>>

    @Upsert
    suspend fun upsertAll(rows: List<PullEntity>)

    @Query("DELETE FROM pull_request WHERE repoId = :repoId AND number NOT IN (:keep)")
    suspend fun deleteMissing(repoId: String, keep: List<Int>)
}
```

A `Flow`-returning query is the whole reason this architecture is pleasant: one
subscription, automatic invalidation, no manual refresh plumbing.

The Room version and its annotation-processor setup are `<verify current>`.

## Storing the validator with the data

This is where Room and [[API - Caching and ETags]] meet, and it is the part
people get wrong.

```kotlin
@Entity(tableName = "sync_state")
data class SyncStateEntity(
    @PrimaryKey val endpoint: String,
    val etag: String?,
    val lastSuccessAt: Instant,
)
```

```kotlin
@Transaction                                  // both, or neither
suspend fun applySync(repoId: String, rows: List<PullEntity>, etag: String?) {
    pullDao.upsertAll(rows)
    syncDao.upsert(SyncStateEntity("pulls/$repoId", etag, Clock.System.now()))
}
```

⚠️ The `@Transaction` is load-bearing. If the process dies between writing the
`ETag` and writing the rows, every later request returns `304` against content
you never stored, and the cache is permanently stale with no error — the exact
silent failure described in [[API - Caching and ETags]].

## Deletions need explicit handling

An upsert-only sync never removes anything. A pull request that was closed
upstream simply stays in your database forever, and the badge count stays wrong.

Two workable strategies:

| Strategy | How | Cost |
|---|---|---|
| Replace-by-scope | In one transaction, upsert the page and delete rows in that scope not returned | Needs a complete listing |
| Tombstone by timestamp | Record `syncedAt` per row, delete rows older than the last full sync | Survives partial pages |

Never `DELETE` then `INSERT` outside a transaction: a reader between the two
sees an empty list and the UI flashes blank.

## Conflict resolution

The dashboard is read-mostly, which makes this simpler than it usually is:
**the server always wins.** GitHub is the source of truth; Room is a cache of it.

Where the app does write — marking a notification read — the honest pattern is
optimistic update plus reconciliation: write locally, mark the row pending, send
the request, and on failure restore from the next successful sync. Do not retry
a non-idempotent write blindly, per
[[API - Idempotency and Retries]].

## Migrations

Changing an entity changes the schema, and Room refuses to open a database whose
version does not match.

```kotlin
val MIGRATION_1_2 = object : Migration(1, 2) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL(
            "ALTER TABLE pull_request " +
                "ADD COLUMN isDraft INTEGER NOT NULL DEFAULT 0",
        )
    }
}
```

Export the schema JSON to the repository and commit it. It is what makes
migrations reviewable in a diff and testable.

## ⚠️ Gotchas

- ⚠️ **`fallbackToDestructiveMigration` deletes the entire database.** It is the
  path of least resistance during development and a data-loss bug in
  production: every cached payload, every stored `ETag` and the whole sync state
  vanish, and the next launch refetches everything at full quota cost. Never
  ship it enabled.
- ⚠️ **Write the `ETag` and the rows in one transaction.** Split writes produce a
  cache that `304`s forever against content it does not have. Silent, and it
  survives reinstalls of your app's *code* because the data outlives them.
- ⚠️ **Upsert-only sync leaks deleted rows.** Closed PRs accumulate and inflate
  every count derived from the table. Decide a deletion strategy before shipping.
- ⚠️ **A migration that is wrong is worse than one that is missing.** A missing
  migration crashes loudly at open; a wrong one silently drops a column's data.
  Test migrations against a real populated database.
- ⚠️ **Do not store the token in Room.** It is a plain SQLite file in the app's
  data directory. Tokens go to the Keystore — see
  [[API - Token Storage on Public Clients]].
- **Room queries on the main thread throw by default**, and that default is
  correct. Make DAO functions `suspend` or return `Flow`.
- **`mergedAt` being null is the only reliable "not merged" signal.** `state`
  reports `closed` for merged PRs, per [[Dev Dashboard - Data Model]]. Compute
  this once when mapping into the entity.
- **Storing timestamps as text sorts wrong.** Use epoch integers, or an ISO-8601
  format that is lexicographically ordered, and be consistent.

---

## Related

- [[Dev Dashboard - Data Model]]
- [[API - Caching and ETags]]
- [[Android - Paging]]
- [[Android - Layered Architecture]]

## Sources

- <https://developer.android.com/training/data-storage/room>
- <https://developer.android.com/training/data-storage/room/migrating-db-versions>
- <https://developer.android.com/topic/architecture/data-layer/offline-first>
