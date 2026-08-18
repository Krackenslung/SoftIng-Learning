---
title: Headers
domain: api
section: "42"
category: fundamentals
difficulty: beginner
danger: none
tags:
  - api/http
  - api/headers
commands: []
dashboard_relevant: true
related:
  - "[[API - HTTP Methods and Status Codes]]"
  - "[[API - Caching and ETags]]"
  - "[[API - Pagination Patterns]]"
  - "[[GitHub - REST API]]"
  - "[[API - JSON YAML and TOML]]"
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers
  - https://www.rfc-editor.org/rfc/rfc9110.html
  - https://www.rfc-editor.org/rfc/rfc8288.html
updated: 2026-08-18
---

# Headers

Headers are the metadata channel of HTTP: everything the two sides need to say
to each other that is not the resource itself. Most of the behaviour people
attribute to "the API" — caching, auth, pagination, rate limiting, content
negotiation — is negotiated entirely in headers, which is why an API client
that ignores response headers is throwing away most of the protocol.

## The categories

| Category | Request | Response |
|---|---|---|
| Identity | `Authorization`, `User-Agent` | `WWW-Authenticate` |
| Negotiation | `Accept`, `Accept-Encoding`, `Accept-Language` | `Content-Type`, `Content-Encoding`, `Vary` |
| Caching | `If-None-Match`, `If-Modified-Since`, `Cache-Control` | `ETag`, `Last-Modified`, `Cache-Control`, `Age` |
| Flow control | — | `Retry-After`, `X-RateLimit-*` |
| Navigation | — | `Link`, `Location` |
| Payload | `Content-Type`, `Content-Length` | `Content-Length`, `Content-Disposition` |
| Tracing | `Idempotency-Key`, `traceparent` | `X-Request-Id` |

## Casing and structure

Header **names are case-insensitive**. HTTP/2 and HTTP/3 additionally require
them to be sent lowercase on the wire, which is why response headers usually
appear lowercase in a debugger even when the docs capitalise them.

```js
// Both work — the Headers object normalises case for you.
res.headers.get("ETag");
res.headers.get("etag");
```

Values are ASCII. Non-ASCII needs encoding (RFC 8187), which is why
`Content-Disposition` filenames use the `filename*=UTF-8''...` form.

## Content negotiation

```http
GET /repos/octocat/hello HTTP/1.1
Accept: application/vnd.github+json
Accept-Encoding: gzip
```

The `Accept` header asks for a representation; `Content-Type` on the response
states what was actually sent. Vendor media types (`application/vnd.*`) are how
APIs version or opt into alternate representations — GitHub uses them for raw
vs rendered Markdown, for example.

Never assume the response type. A gateway returning an HTML error page with
`Content-Type: text/html` will make a blind `.json()` call fail confusingly.

## Authorization

```http
Authorization: Bearer ghp_xxx
```

The scheme (`Bearer`, `Basic`, `token`) is part of the value, and APIs are
picky about which they accept. Bearer tokens are defined by RFC 6750 — see
[[API - JWT]] and [[API - OAuth 2.0 Flows]] for what is inside them.

## The `Link` header

Standardised by RFC 8288, this is how a REST API expresses "there is more":

```http
Link: <https://api.github.com/user/repos?page=3>; rel="next",
      <https://api.github.com/user/repos?page=9>; rel="last"
```

Parse it and follow `rel="next"` rather than building page URLs yourself. See
[[API - Pagination Patterns]].

## Custom headers

The `X-` prefix was deprecated by RFC 6648 in 2012, on the grounds that
successful experimental headers get standardised and then have to live with a
misleading name forever. In practice `X-RateLimit-Remaining`,
`X-GitHub-Api-Version` and friends are entrenched, so read them — just do not
mint new `X-` names in your own APIs.

## ⚠️ Gotchas

- ⚠️ **`Vary` is what makes a shared cache correct.** If a response differs by
  `Authorization` or `Accept` and the server does not say `Vary: Authorization`,
  an intermediate cache can serve one user's private response to another. When
  caching client-side, key on the full set of varying headers yourself.
- ⚠️ **Header values are attacker-controlled input.** Reflecting a request
  header into a response, a log line or a shell command without escaping is a
  standing injection risk. Never interpolate one into a database query or a
  command line.
- ⚠️ **Duplicate headers do not always merge.** Most repeated headers combine
  into a comma-separated list, but `Set-Cookie` is exempt. `headers.get()`
  returns a joined string; use `headers.getSetCookie()` for cookies.
- **A missing `User-Agent` is a hard failure on some APIs**, GitHub included,
  which returns 403. Set a descriptive one naming your application.
- **Do not log the `Authorization` header.** It is the most common way a token
  ends up in a log aggregator, a crash report or a CI transcript.
- **CORS only restricts browsers.** `Access-Control-Allow-Origin` is not access
  control; a server-side client ignores it entirely. It is never a substitute
  for real auth.

> [!warning] Reading a header you never sent
> `X-RateLimit-Remaining` is present on nearly every response, and dashboards
> that only read it *after* hitting a 429 have already lost. Budget from every
> response — see [[API - Rate Limiting Strategies]].

---

## Related

- [[API - HTTP Methods and Status Codes]]
- [[API - Caching and ETags]]
- [[API - Pagination Patterns]]
- [[GitHub - REST API]]
- [[API - JSON YAML and TOML]]

## Sources

- <https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers>
- <https://www.rfc-editor.org/rfc/rfc9110.html>
- <https://www.rfc-editor.org/rfc/rfc8288.html>
