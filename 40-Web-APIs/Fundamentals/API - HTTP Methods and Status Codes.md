---
title: HTTP Methods and Status Codes
domain: api
section: "41"
category: fundamentals
difficulty: beginner
danger: none
tags:
  - api/http
  - api/rest
commands: []
dashboard_relevant: true
related:
  - "[[API - Headers]]"
  - "[[API - Idempotency and Retries]]"
  - "[[API - Rate Limiting Strategies]]"
  - "[[GitHub - REST API]]"
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status
  - https://www.rfc-editor.org/rfc/rfc9110.html
updated: 2026-08-18
---

# HTTP Methods and Status Codes

Every HTTP request is a verb applied to a URL, and every response is a
three-digit number plus a body. Fluency in those two vocabularies is most of
what "knowing an API" means — the rest is that particular API's nouns. Two
properties of the verbs, **safe** and **idempotent**, are what decide whether a
client may retry a failed call automatically.

## Methods

| Method | Purpose | Safe | Idempotent | Request body |
|---|---|---|---|---|
| `GET` | Read a resource | yes | yes | no |
| `HEAD` | Headers only, no body | yes | yes | no |
| `OPTIONS` | Discover allowed methods, CORS preflight | yes | yes | no |
| `POST` | Create, or "run this operation" | no | **no** | yes |
| `PUT` | Replace a resource wholesale | no | yes | yes |
| `PATCH` | Partial update | no | **no** | yes |
| `DELETE` | Remove a resource | no | yes | optional |

**Safe** means no observable state change on the server. **Idempotent** means
N identical requests leave the same state as one — it says nothing about the
*responses* being identical. `DELETE` twice returns 204 then 404, but the end
state is the same either way, so it qualifies.

`PATCH` is not idempotent by spec because a patch document can be relative
("increment by 1"). A JSON Merge Patch that only sets absolute values is
idempotent in practice, but nothing in HTTP guarantees it, so a generic client
must assume it is not. See [[API - Idempotency and Retries]].

## Status codes

| Class | Meaning | What the client should do |
|---|---|---|
| `1xx` | Informational | Rarely surfaced; ignore |
| `2xx` | Success | Proceed |
| `3xx` | Redirect or not-modified | Follow it, or use the cache |
| `4xx` | The request was wrong | Fix it — do not blindly retry |
| `5xx` | The server failed | Retry with backoff |

The individual codes worth memorising:

| Code | Name | Notes |
|---|---|---|
| 200 | OK | Body present |
| 201 | Created | Should carry a `Location` header |
| 202 | Accepted | Queued, not done — poll for the result |
| 204 | No Content | Success, **empty body** |
| 301 / 308 | Moved Permanently | 308 preserves the method, 301 may not |
| 302 / 307 | Found / Temporary Redirect | 307 preserves the method |
| 304 | Not Modified | Cached copy still valid ([[API - Caching and ETags]]) |
| 400 | Bad Request | Malformed syntax or invalid parameters |
| 401 | Unauthorized | Actually *unauthenticated* — missing or bad credentials |
| 403 | Forbidden | Authenticated, but not permitted |
| 404 | Not Found | ...or deliberately hidden. See gotchas |
| 409 | Conflict | Concurrent edit, or a state precondition failed |
| 410 | Gone | Permanently deleted; stop asking |
| 422 | Unprocessable Content | Syntax fine, semantics wrong (validation) |
| 429 | Too Many Requests | Back off, and read `Retry-After` |
| 500 | Internal Server Error | Their bug |
| 502 / 503 / 504 | Bad Gateway / Unavailable / Gateway Timeout | Transient |

## Reading a response correctly

```js
const res = await fetch(url, { headers });

if (res.status === 304) return cached;   // no body at all
if (res.status === 204) return null;     // no body at all
if (!res.ok) throw new HttpError(res.status, await res.text());

return res.json();
```

`fetch` does **not** throw on 4xx or 5xx — only on network failure. `res.ok` is
true only for 200–299.

## ⚠️ Gotchas

- ⚠️ **A non-2xx response is not an exception.** Calling `res.json()` without
  checking `res.ok` silently parses an error page as data, and the bug surfaces
  much later as a missing field. This is the most common defect in hand-rolled
  API clients.
- ⚠️ **401 means unauthenticated, 403 means unauthorized.** The names are
  historically backwards. 401 is "your token is missing, expired or malformed";
  403 is "your token is fine, your permissions are not."
- ⚠️ **Some APIs return 404 where you expect 403**, to avoid confirming that a
  private resource exists. GitHub does exactly this, so a 404 on a repository
  you know exists is usually an auth failure, not a typo — see
  [[Bridge - GitHub API Conventions]].
- ⚠️ **Never retry a `POST` automatically** without an idempotency key. A
  timeout does not tell you whether the server processed the request; retrying
  can double-charge, double-comment or double-create.
- **202 is not success.** It means "accepted, maybe later". You must poll the
  status URL to find out what actually happened.
- **204 and 304 have no body.** Calling `.json()` on either throws a parse
  error that looks like a server fault but is entirely client-side.
- **`GET` with a request body** is not portable and is widely dropped by
  proxies. If a query is too large for a URL, the API has to offer a
  `POST /search` variant.

> [!tip] Method preservation on redirect
> Old 301/302 handling downgraded `POST` to `GET`. 307 and 308 were added
> precisely to forbid that. If a redirect silently turns a write into a read,
> this is why.

---

## Related

- [[API - Headers]]
- [[API - Idempotency and Retries]]
- [[API - Rate Limiting Strategies]]
- [[GitHub - REST API]]

## Sources

- <https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods>
- <https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status>
- <https://www.rfc-editor.org/rfc/rfc9110.html>
