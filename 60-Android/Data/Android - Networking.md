---
title: Networking
domain: android
section: "71"
category: data
difficulty: intermediate
danger: high
tags:
  - android/networking
  - android/http
  - android/security
commands: []
endpoints: []
dashboard_relevant: true
mobile_relevant: true
related:
  - "[[API - Caching and ETags]]"
  - "[[GitHub - REST API]]"
  - "[[API - REST vs GraphQL]]"
  - "[[API - Token Storage on Public Clients]]"
  - "[[Bridge - GitHub API on Android]]"
  - "[[Android - Paging]]"
  - "[[Android - Dependency Injection]]"
sources:
  - https://developer.android.com/develop/connectivity/network-ops/connecting
  - https://square.github.io/okhttp/
  - https://square.github.io/retrofit/
updated: 2026-08-18
---

# Networking

Every HTTP concept in [[Web-APIs]] arrives here as a concrete object: headers
become interceptors, conditional requests become a cache plus an `ETag` store,
status codes become a `Response`. OkHttp is the engine underneath both Retrofit
and Apollo, so it is the layer where authentication, caching and rate-limit
accounting actually happen — and where a single misconfiguration writes your
token into logcat.

## The stack

| Layer | Job |
|---|---|
| OkHttp | Connections, interceptors, cache, retries at transport level |
| Retrofit | Turns a Kotlin interface into REST calls |
| Apollo Kotlin | Turns `.graphql` documents into typed calls |
| Serializer | JSON to data classes |

Retrofit and Apollo both sit on **one shared `OkHttpClient`**. Creating a second
one gives it a separate connection pool and a separate cache, silently
discarding every saving described below — see
[[Android - Dependency Injection]].

Library versions and artifacts are `<verify current>`.

## Interceptors

```kotlin
class AuthInterceptor(private val tokens: TokenStore) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val token = tokens.read() ?: return chain.proceed(chain.request())

        val request = chain.request().newBuilder()
            .header("Authorization", "Bearer $token")
            .header("Accept", "application/vnd.github+json")
            .header("X-GitHub-Api-Version", "<verify current>")
            .header("User-Agent", "dev-dashboard/1.0 (+https://github.com/...)")
            .build()

        return chain.proceed(request)
    }
}
```

Three of those headers are not optional against GitHub: `User-Agent` is
**mandatory** and its absence returns 403, and pinning
`X-GitHub-Api-Version` is what stops a future breaking change arriving
unannounced. See [[Bridge - GitHub API Conventions]] and [[API - Headers]].

Application interceptors run once per call; network interceptors run per actual
network request and can see redirects and cache behaviour. That distinction
matters for the gotcha below.

## Conditional requests, and OkHttp's cache

```kotlin
val client = OkHttpClient.Builder()
    .cache(Cache(File(context.cacheDir, "http"), maxSize = 20L * 1024 * 1024))
    .addInterceptor(AuthInterceptor(tokenStore))
    .build()
```

Given a cache, OkHttp handles validators for you: it stores the `ETag`, sends
`If-None-Match`, and on a `304` serves the cached body.

> [!warning] The 304 you never see
> Your code receives **`200`** with a body, because OkHttp has already resolved
> the `304` into a cache hit. `response.code` will not tell you whether quota was
> spent. Read `response.networkResponse?.code` for what actually crossed the
> wire, and `response.cacheResponse` for what came from disk.

```kotlin
val spentQuota = response.networkResponse?.code !in setOf(null, 304)
```

This matters because on GitHub a `304` costs no core quota — the entire reason
polling is viable for a client-only app. If your accounting reads
`response.code`, every cache hit looks like a full-price request and the budget
logic is wrong in the safe direction, but the *savings* are invisible and
unverifiable. See [[API - Caching and ETags]].

For anything you cache in Room rather than in OkHttp's disk cache, store the
`ETag` yourself, alongside the data, in one transaction — see
[[Android - Offline First and Room]].

## Retrofit

```kotlin
interface GitHubApi {
    @GET("repos/{owner}/{repo}/pulls")
    suspend fun pulls(
        @Path("owner") owner: String,
        @Path("repo") repo: String,
        @Query("state") state: String = "open",
        @Query("per_page") perPage: Int = 100,
    ): Response<List<PullDto>>
}
```

Returning `Response<T>` rather than `T` keeps headers reachable — `Link` for
pagination, `x-ratelimit-*` for budgeting — which a bare `T` throws away. See
[[API - Pagination Patterns]] and [[API - Rate Limiting Strategies]].

## Errors

```kotlin
suspend fun <T> call(block: suspend () -> Response<T>): Result<T> = try {
    val response = block()
    when {
        response.isSuccessful -> Result.success(response.body()!!)
        response.code() == 401 -> Result.failure(Unauthorized)   // discard token
        response.code() == 403 || response.code() == 429 ->
            Result.failure(RateLimited(response.headers()["retry-after"]))
        else -> Result.failure(HttpError(response.code()))
    }
} catch (e: IOException) {
    Result.failure(Offline(e))          // transport only: no response at all
}
```

`IOException` means nothing arrived. A non-2xx means the server answered and
disagreed. Collapsing the two makes "you are offline" and "your token expired"
indistinguishable to the user.

## ⚠️ Gotchas

- ⚠️ **The logging interceptor prints `Authorization` in release builds.** At
  `HEADERS` or `BODY` level it writes the token into logcat and every crash
  report. Add it only on `debugImplementation`, and redact the header explicitly
  even there — see [[API - Token Storage on Public Clients]] and
  [[Android - Gradle and AGP]].
- ⚠️ **`response.code` hides cache hits.** A `304` reaches your code as `200`.
  Rate-limit accounting and any "did caching work?" metric must read
  `networkResponse`, or you are measuring nothing.
- ⚠️ **A missing `User-Agent` fails with 403 on GitHub**, which reads as an
  auth problem and sends you debugging the token instead of the header.
- ⚠️ **Do not build a second `OkHttpClient`.** Separate pools and caches mean
  every conditional-request saving is lost, quietly.
- **Set explicit timeouts.** The defaults are not tuned for a mobile network, and
  a hung call blocks a Worker until the system kills it.
- **`Response<T>` over `T`.** Without it you lose `Link`, `ETag` and every
  rate-limit header.
- **404 usually means permission, not absence** — see
  [[Bridge - GitHub API Conventions]].
- **Do not retry a non-idempotent request on timeout** — see
  [[API - Idempotency and Retries]].

---

## Related

- [[API - Caching and ETags]]
- [[GitHub - REST API]]
- [[API - REST vs GraphQL]]
- [[API - Token Storage on Public Clients]]
- [[Bridge - GitHub API on Android]]
- [[Android - Paging]]
- [[Android - Dependency Injection]]

## Sources

- <https://developer.android.com/develop/connectivity/network-ops/connecting>
- <https://square.github.io/okhttp/>
- <https://square.github.io/retrofit/>
