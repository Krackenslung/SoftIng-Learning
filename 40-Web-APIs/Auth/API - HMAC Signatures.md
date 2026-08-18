---
title: HMAC Signatures
domain: api
section: "48"
category: auth
difficulty: advanced
danger: high
tags:
  - api/auth
  - api/webhooks
  - api/security
commands: []
dashboard_relevant: true
related:
  - "[[API - JWT]]"
  - "[[API - Webhooks vs Polling]]"
  - "[[API - Headers]]"
  - "[[GitHub - Webhooks]]"
sources:
  - https://www.rfc-editor.org/rfc/rfc2104.html
  - https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries
  - https://nodejs.org/api/crypto.html#cryptotimingsafeequala-b
updated: 2026-08-18
---

# HMAC Signatures

An HMAC proves that whoever produced a message held a shared secret, and that
the message has not been altered since. It is the standard way an incoming
webhook proves it came from the provider and not from anyone who guessed your
public URL — and unlike a bearer token, the proof is bound to the specific
payload rather than replayable against any request.

## The construction

```text
HMAC(K, m) = H( (K ⊕ opad) || H( (K ⊕ ipad) || m ) )
```

The nested hash in RFC 2104 exists to defeat **length-extension** attacks, which
is why a plain `SHA256(secret || body)` is not a safe substitute even though it
looks equivalent. Use a real HMAC implementation.

The sender computes the HMAC over the request body and sends it in a header; the
receiver recomputes it and compares.

```http
POST /hooks/github HTTP/1.1
Content-Type: application/json
X-Hub-Signature-256: sha256=7d38cdd689735b008b3c702edd92eea23791c5f6
X-GitHub-Delivery: 72d3162e-cc78-11e3-81ab-4c9367dc0958
```

## Verifying correctly

```js
import crypto from "node:crypto";

// rawBody is a Buffer — captured BEFORE any JSON parsing.
export function verify(rawBody, headerValue, secret) {
  const expected =
    "sha256=" + crypto.createHmac("sha256", secret).update(rawBody).digest("hex");

  const a = Buffer.from(expected, "utf8");
  const b = Buffer.from(headerValue ?? "", "utf8");

  // timingSafeEqual throws on length mismatch, so guard first.
  return a.length === b.length && crypto.timingSafeEqual(a, b);
}
```

Three things in that function are load-bearing, and each is a real CVE class.

### 1. Hash the raw bytes

The signature covers the exact byte sequence transmitted. Parsing to JSON and
re-serialising changes key order, whitespace, Unicode escaping and number
formatting — the recomputed HMAC then never matches, or worse, a middleware that
normalises the body lets a modified payload verify against a signature computed
over something else. Capture the raw buffer before any body parser touches it:

```js
app.use(express.json({ verify: (req, _res, buf) => { req.rawBody = buf; } }));
```

### 2. Compare in constant time

`===` and `Buffer.compare` return as soon as they hit a differing byte. That
makes execution time a function of how many leading bytes matched, and an
attacker who can send many requests recovers the expected signature one byte at
a time. `crypto.timingSafeEqual` always reads both buffers fully.

The timing difference is microseconds and absolutely is exploitable across a
network with enough samples — this is not a theoretical concern.

### 3. Reject before doing anything else

Verify before parsing, before logging the payload, before touching a queue. An
unverified webhook body is entirely attacker-controlled.

## Replay protection

A valid signature stays valid forever, so an intercepted delivery can be resent.
Providers that care include a timestamp **inside the signed material**:

```text
signature_base = f"{timestamp}.{raw_body}"
```

The receiver then rejects anything older than a short window (five minutes is
typical) and deduplicates on a delivery ID. Because the timestamp is part of
what was signed, an attacker cannot rewrite it.

GitHub signs the body only and supplies `X-GitHub-Delivery` as the dedupe key,
so replay resistance there comes from tracking delivery IDs — see
[[GitHub - Webhooks]].

## HMAC versus a bearer token

| | HMAC signature | Bearer token |
|---|---|---|
| Proves | Sender holds the secret, body unmodified | Sender holds the secret |
| Secret on the wire | **No** | Yes, every request |
| Bound to the payload | Yes | No |
| Leak via logs | Signature is useless alone | Full compromise |
| Complexity | Higher | Trivial |

For inbound webhooks the payload binding is decisive: a leaked signature grants
nothing, whereas a leaked token grants everything.

## ⚠️ Gotchas

- ⚠️ **Parsing before verifying voids the signature.** Any framework that JSON
  parses by default will silently break verification, and the usual "fix" is to
  re-serialise the object — which produces intermittent failures that look like
  provider bugs. Keep the raw bytes.
- ⚠️ **A non-constant-time comparison leaks the signature.** `if (sig ===
  expected)` is the single most common webhook vulnerability. Always use
  `timingSafeEqual`, and guard the length check separately since it throws on
  mismatched lengths.
- ⚠️ **A missing signature header must be a rejection, not a skip.** Code
  shaped like `if (sig && !verify(...)) return 401` accepts every unsigned
  request. Require the header first.
- ⚠️ **Never log the raw payload before verification**, and never log the
  secret. Unverified bodies in a log aggregator are an injection vector.
- ⚠️ **Verifying does not make the payload trustworthy content.** It proves
  origin and integrity only. The values inside still need validation before they
  reach a query or a shell.
- **Use the strongest signature offered.** GitHub sends both
  `X-Hub-Signature` (SHA-1) and `X-Hub-Signature-256`; verify the SHA-256 one
  and ignore the legacy header.
- **Rotate secrets with an overlap window.** Accept either the old or the new
  secret for a period, then drop the old, or in-flight deliveries fail.
- **Return 401 fast.** Slow rejection is itself a timing signal, and it gives
  attackers a cheap way to consume your capacity.

---

## Related

- [[API - JWT]]
- [[API - Webhooks vs Polling]]
- [[API - Headers]]
- [[GitHub - Webhooks]]

## Sources

- <https://www.rfc-editor.org/rfc/rfc2104.html>
- <https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries>
- <https://nodejs.org/api/crypto.html#cryptotimingsafeequala-b>
