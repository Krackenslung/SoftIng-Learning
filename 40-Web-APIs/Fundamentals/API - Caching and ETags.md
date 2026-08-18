---
title: Caching and ETags
domain: api
section: "43"
category: fundamentals
difficulty: intermediate
danger: low
tags:
  - api/http
  - api/caching
commands: []
dashboard_relevant: true
related:
  - "[[API - Headers]]"
  - "[[API - HTTP Methods and Status Codes]]"
  - "[[GitHub - REST API]]"
  - "[[GitHub - Rate Limits]]"
  - "[[API - Rate Limiting Strategies]]"
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/ETag
  - https://www.rfc-editor.org/rfc/rfc9111.html
  - https://www.rfc-editor.org/rfc/rfc9110.html#section-13
updated: 2026-08-18
---

# Caching and ETags

An HTTP cache answers two separate questions: *may I reuse this without asking?*
(freshness) and *is the copy I already have still correct?* (validation).
Freshness saves the round trip entirely; validation still costs a round trip but
avoids re-sending the body — and, on APIs that meter by request outcome, often
costs no quota at all. For a polling dashboard, validation is the difference
between viable and not.

## Freshness: `Cache-Control`

```http
Cache-Control: private, max-age=60, must-revalidate
```

| Directive | Meaning |
|---|---|
| `max-age=N` | Fresh for N seconds from generation |
| `s-maxage=N` | As above, but for shared caches only; overrides `max-age` |
| `no-cache` | Store it, but **revalidate every time** before reuse |
| `no-store` | Do not write it to disk or memory at all |
| `private` | Only a single user's cache may store it |
| `public` | Shared caches may store it, even if authenticated |
| `must-revalidate` | Once stale, never serve without revalidating |
| `immutable` | Do not revalidate while fresh, even on reload |

`no-cache` and `no-store` are constantly confused. `no-cache` means "always
check first"; `no-store` means "never keep it". Only `no-store` is a
confidentiality control.

## Validation: strong and weak validators

A validator is an opaque token the server gives you and later recognises.

| Validator | Header | Precision |
|---|---|---|
| ETag, strong | `ETag: "a1b2c3"` | Byte-for-byte identical |
| ETag, weak | `ETag: W/"a1b2c3"` | Semantically equivalent |
| Modification date | `Last-Modified: Wed, 13 Aug 2026 10:00:00 GMT` | **One second** |

Strong ETags are required for range requests and for safe concurrent writes.
Weak ETags (`W/` prefix) say "the meaning is unchanged" and are the right choice
when a timestamp or a rendered footer shifts on every request without the
content really differing.

`Last-Modified` has one-second granularity, so two changes within the same
second are indistinguishable. Prefer an ETag whenever the server offers one.

## Making a conditional request

```http
GET /user/repos HTTP/1.1
If-None-Match: "a1b2c3"
```

```http
HTTP/1.1 304 Not Modified
ETag: "a1b2c3"
```

| Request header | Pairs with | Comparison |
|---|---|---|
| `If-None-Match` | `ETag` | Reads: 304 if unchanged |
| `If-Modified-Since` | `Last-Modified` | Reads: 304 if not newer |
| `If-Match` | `ETag` | Writes: 412 if changed under you |
| `If-Unmodified-Since` | `Last-Modified` | Writes: 412 if changed under you |

The read pair saves bandwidth. The **write** pair is optimistic concurrency
control: send `If-Match` with the ETag you read, and a 412 tells you someone
else edited the resource first, instead of you silently clobbering them.

```js
const res = await fetch(url, {
  headers: { ...auth, "If-None-Match": store.etag ?? "" },
});

if (res.status === 304) return store.body;      // no body, no re-parse

store.etag = res.headers.get("etag");
store.body = await res.json();
return store.body;
```

## Why a 304 is cheap

The response carries headers only — no body to transfer, no JSON to parse. On
GitHub it goes further: **a 304 does not count against the REST rate limit**,
so an ETag-aware poller can check far more often than its quota would otherwise
allow. See [[GitHub - Rate Limits]] and [[GitHub - REST API]].

## ⚠️ Gotchas

- ⚠️ **Key the cache by URL *and* identity.** Two tokens see different results
  from the same endpoint. Storing one ETag per URL, ignoring who asked, will
  serve one account's data to another. Key on URL plus a hash of the token.
- ⚠️ **Honour `Vary`.** If the response says `Vary: Accept, Authorization`,
  those headers are part of the cache key. Ignoring it is the same bug as above,
  one layer down — see [[API - Headers]].
- ⚠️ **A 304 has no body.** Return the stored copy; calling `.json()` on the
  304 response itself throws.
- ⚠️ **Store the ETag with the data it validates, atomically.** If a crash
  persists the new ETag but not the new body, every later request 304s against
  stale content and the cache never self-corrects. This failure is silent and
  can outlive several deploys.
- **Send the ETag back verbatim**, quotes and any `W/` prefix included. Stripping
  the quotes makes the comparison fail, and you get a 200 and full body every
  time while believing caching is on.
- **`ETag` is per-representation.** A gzipped and an identity response are
  different representations and carry different ETags.
- **Compare weak validators weakly.** `If-None-Match` uses weak comparison, so
  `W/"x"` matches `"x"`. `If-Match` uses strong comparison and will not match a
  weak tag at all.

> [!tip] Verify caching actually works
> Log the ratio of 304s to 200s. If it is zero, something in the chain is
> dropping or mangling the ETag, and you are paying full quota while thinking
> you are not.

---

## Related

- [[API - Headers]]
- [[API - HTTP Methods and Status Codes]]
- [[GitHub - REST API]]
- [[GitHub - Rate Limits]]
- [[API - Rate Limiting Strategies]]

## Sources

- <https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/ETag>
- <https://www.rfc-editor.org/rfc/rfc9111.html>
- <https://www.rfc-editor.org/rfc/rfc9110.html#section-13>
