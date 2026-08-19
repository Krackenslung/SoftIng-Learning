---
title: Dependency Injection
domain: android
section: "67"
category: architecture
difficulty: intermediate
danger: low
tags:
  - android/architecture
  - android/di
commands: []
endpoints: []
dashboard_relevant: true
mobile_relevant: true
related:
  - "[[Android - Layered Architecture]]"
  - "[[Android - WorkManager]]"
  - "[[Android - State and ViewModel]]"
  - "[[Android - Networking]]"
sources:
  - https://developer.android.com/training/dependency-injection
  - https://developer.android.com/training/dependency-injection/hilt-android
  - https://developer.android.com/training/dependency-injection/manual
updated: 2026-08-18
---

# Dependency Injection

Dependency injection is one idea: a class receives what it needs instead of
constructing it. Everything else — containers, annotations, scopes — is
machinery for doing that at scale. The reason it matters here is narrow and
concrete: the `OkHttpClient` carrying the auth interceptor and the connection
pool must be **one instance shared across the whole app**, and the repository
must be swappable for a fake in tests without an emulator.

## The idea, without a framework

```kotlin
// Not injected: the class decides, and nothing can change it.
class PullRepository {
    private val api = Retrofit.Builder().build().create(GitHubApi::class.java)
}

// Injected: the caller decides, so a test can pass a fake.
class PullRepository(private val api: GitHubApi, private val dao: PullDao)
```

That is the whole concept. A framework only answers "who calls the
constructor?" once the graph gets deep.

## Choosing

| Approach | Fits when | Cost |
|---|---|---|
| Manual container | Small app, shallow graph, one module | You write and maintain the wiring |
| Hilt | Android-first, needs ViewModel and Worker integration | Annotation processing, build time |
| Koin | You want runtime resolution, no processor | Failures appear at runtime, not compile time |

Hilt is the option Google documents for Android and the only one with
first-class hooks for the two integration points that actually hurt —
ViewModels and `WorkManager`. Its artifacts, plugin and processor setup are
`<verify current>`.

For a single-module dashboard, a hand-written container is genuinely viable:

```kotlin
class AppContainer(context: Context) {
    private val tokenStore = KeystoreTokenStore(context)

    val okHttp: OkHttpClient by lazy {          // one instance, app-wide
        OkHttpClient.Builder()
            .addInterceptor(AuthInterceptor(tokenStore))
            .build()
    }

    val pullRepository: PullRepository by lazy {
        DefaultPullRepository(GitHubApi.create(okHttp), database.pullDao())
    }
}
```

The `by lazy` is doing the scoping: created once, on first use, shared
thereafter.

## Scopes

A scope answers *how long does this instance live*.

| Scope | Lives as long as | Right for |
|---|---|---|
| Singleton / app | The process | `OkHttpClient`, the database, repositories |
| ViewModel | The ViewModel | Per-screen state holders |
| Activity | The Activity | Rarely needed |
| Unscoped | Created per request | Mappers, plain value objects |

Getting this wrong in the direction of *too narrow* is the expensive mistake: a
new `OkHttpClient` per screen means a new connection pool and a new cache each
time, which quietly discards every conditional-request saving described in
[[API - Caching and ETags]].

## The two integration points

**ViewModels** need construction by the framework, so they cannot simply take
constructor arguments — the platform creates them. Both Hilt and a manual
factory solve this; the manual version is a `ViewModelProvider.Factory`.

**Workers** are worse, and this is the gotcha the spec calls out.
`WorkManager` instantiates Workers itself, by reflection, so a Worker with
constructor dependencies will fail at runtime unless you install a custom
`WorkerFactory` and disable the default initializer.

```kotlin
class SyncWorkerFactory(private val repository: PullRepository) : WorkerFactory() {
    override fun createWorker(
        appContext: Context,
        workerClassName: String,
        params: WorkerParameters,
    ): ListenableWorker? = when (workerClassName) {
        SyncWorker::class.java.name -> SyncWorker(appContext, params, repository)
        else -> null                 // null lets the default factory try
    }
}
```

Registering it requires opting out of the automatic `WorkManager`
initialisation and providing a `Configuration`; the exact manifest provider name
and API for this are `<verify current>`. See [[Android - WorkManager]].

## ⚠️ Gotchas

- ⚠️ **A Worker with constructor dependencies crashes at runtime, not compile
  time.** The default factory cannot construct it, and the failure surfaces as a
  background job that silently never succeeds — the worst possible place for it,
  because nothing is on screen to show the error.
- ⚠️ **Creating `OkHttpClient` more than once throws away caching and pooling.**
  Every instance has its own connection pool, cache and interceptors. Share one.
- ⚠️ **Runtime-resolution containers fail in production paths you never
  exercised.** A missing binding on a rarely visited screen compiles fine and
  crashes for the user. Compile-time graphs turn that into a build error.
- **Do not inject `Context` where `Application` will do.** Holding an Activity
  `Context` in a singleton leaks the entire Activity.
- **Annotation processing costs build time.** In a one-module app, weigh that
  against wiring you could write in twenty lines — see
  [[Android - Gradle and AGP]].
- **Interfaces at the repository boundary are what make DI worth it.** Injecting
  a concrete class buys almost nothing; injecting
  `PullRepository` is what lets tests run on the JVM — see
  [[Android - Layered Architecture]].

---

## Related

- [[Android - Layered Architecture]]
- [[Android - WorkManager]]
- [[Android - State and ViewModel]]
- [[Android - Networking]]

## Sources

- <https://developer.android.com/training/dependency-injection>
- <https://developer.android.com/training/dependency-injection/hilt-android>
- <https://developer.android.com/training/dependency-injection/manual>
