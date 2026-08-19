---
title: Android
domain: android
type: hub
tags:
  - hub
  - android
updated: 2026-08-18
cssclasses:
  - hub
---

# Android

The client that consumes everything in [[Web-APIs]] and [[GitHub]]. The
dashboard is a native Android app with **no backend** — the architecture
decision, and everything it forces, is in
[[API - Client-Only vs Backend Architectures]]. Read that first: it explains why
this domain is built around polling, a local database and on-device key storage
rather than webhooks and a server session.

> [!warning] Versions in this domain go stale
> The rest of the vault rests on RFCs and `git-scm.com`, stable for years. This
> one does not. Every version number here is written `<verify current>` and
> collected in `00-Meta/specs/spec-02-android-VERSIONS.md` for checking against
> developer.android.com. A note with an invented `targetSdk` is worse than no
> note.

## Foundations

- [[Android - Project Structure]] — modules, source sets, manifest merging, R8
- [[Android - Gradle and AGP]] — version catalog, configurations, signing
- [[Android - Android Studio]] — the three tools with no CLI equivalent
- [[Android - App Lifecycle]] — process death, saved state, lifecycle-aware
  collection

## Architecture

- [[Android - Layered Architecture]] — UI, domain, data; the repository seam
- [[Android - Offline First and Room]] — the local database as source of truth
- [[Android - Dependency Injection]] — scopes, ViewModels, Workers

## UI

- [[Android - Jetpack Compose]] — declarative UI, recomposition
- [[Android - State and ViewModel]] — state hoisting, `StateFlow`, sealed state
- [[Android - Navigation]] — back stack, deep links, the OAuth return path

## Data

- [[Android - Networking]] — OkHttp interceptors, Retrofit, Apollo, ETags
- [[Android - Coroutines and Flow]] — structured concurrency, cold vs hot
- [[Android - Paging]] — `PagingSource`, `RemoteMediator`, cursors vs pages

## Background

- [[Android - WorkManager]] — periodic sync, constraints, backoff
- [[Android - Background Limits and Doze]] — why "every 5 minutes" is not real

## Security

- [[Android - Keystore and Secure Storage]] — the Android implementation of
  [[API - Token Storage on Public Clients]]

## Where this meets the API notes

- [[Bridge - GitHub API on Android]] — polling instead of webhooks, OkHttp's
  cached `304`, Custom Tabs instead of a server redirect
- [[API - Client-Only vs Backend Architectures]] · [[API - Caching and ETags]] ·
  [[API - Pagination Patterns]] · [[API - Token Storage on Public Clients]]
- [[Dev Dashboard - Data Model]] · [[Dev Dashboard - API Map]]

---

## All Android notes

```dataview
TABLE category AS Category, difficulty AS Level, danger AS Risk
FROM "60-Android"
WHERE type != "hub"
SORT section ASC
```

## Dashboard-relevant notes

```dataview
TABLE category AS Category, difficulty AS Level
FROM "60-Android"
WHERE dashboard_relevant = true
SORT section ASC
```
