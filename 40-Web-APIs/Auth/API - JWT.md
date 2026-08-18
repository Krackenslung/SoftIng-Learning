---
title: JWT
domain: api
section: "47"
category: auth
difficulty: advanced
danger: high
tags:
  - api/auth
  - api/jwt
commands: []
dashboard_relevant: true
related:
  - "[[API - OAuth 2.0 Flows]]"
  - "[[API - OIDC and Federated Identity]]"
  - "[[API - HMAC Signatures]]"
  - "[[GitHub - Bots and Apps]]"
sources:
  - https://www.rfc-editor.org/rfc/rfc7519.html
  - https://www.rfc-editor.org/rfc/rfc8725.html
  - https://jwt.io/introduction
updated: 2026-08-18
---

# JWT

A JSON Web Token is a set of claims, serialised as JSON, base64url-encoded and
signed. Its defining property is that it is **self-contained**: the receiver can
verify it without calling the issuer, which is what makes it useful for
stateless APIs — and what makes revoking one hard. Everything difficult about
JWTs follows from that trade-off.

## Structure

Three base64url segments joined by dots:

```text
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9 . eyJpc3MiOiIxMjMiLCJleHAiOjE3NTV9 . SIG
└────────── header ──────────────────┘ └────────── payload ───────────┘ └sig┘
```

```json
{ "alg": "RS256", "typ": "JWT", "kid": "2026-08-key-1" }
```

```json
{
  "iss": "123456",
  "sub": "user-42",
  "aud": "https://api.example.com",
  "exp": 1755500000,
  "iat": 1755499400,
  "jti": "b1f0c3a7"
}
```

> [!warning] Encoded is not encrypted
> base64url is reversible by anyone. A signed JWT (JWS) is **readable by the
> bearer and anyone who intercepts it**; the signature protects integrity, not
> confidentiality. Never put secrets, PII or internal identifiers you would not
> print in a log into a JWT payload. Encryption requires JWE, which is a
> different and much less common construction.

## Registered claims

| Claim | Name | Must you validate it? |
|---|---|---|
| `iss` | Issuer | **Yes** — pin to the expected issuer |
| `sub` | Subject | Yes, if it drives authorisation |
| `aud` | Audience | **Yes** — is this token for *you*? |
| `exp` | Expiry | **Yes** |
| `nbf` | Not before | Yes, when present |
| `iat` | Issued at | Yes, for maximum-age policies |
| `jti` | JWT ID | Yes, if you need replay protection |

## Algorithms

| Family | Example | Key model |
|---|---|---|
| HMAC | `HS256` | One shared secret signs and verifies |
| RSA | `RS256` | Private key signs, public key verifies |
| ECDSA | `ES256` | As RSA, smaller keys |
| EdDSA | `Ed25519` | As RSA, modern |
| **None** | `none` | **No signature at all** |

Asymmetric algorithms are the right default for anything crossing a trust
boundary: verifiers only need the public key, so a compromised verifier cannot
mint tokens. GitHub Apps use `RS256` — see [[GitHub - Bots and Apps]].

## Verifying, in the right order

```js
import { jwtVerify, createRemoteJWKSet } from "jose";

const jwks = createRemoteJWKSet(new URL(`${ISSUER}/.well-known/jwks.json`));

const { payload } = await jwtVerify(token, jwks, {
  algorithms: ["RS256"],           // pin: never trust the header's alg
  issuer: ISSUER,                  // iss
  audience: "https://api.example.com",  // aud
  clockTolerance: 60,              // seconds
});
```

Verify the **signature first**, then the claims. Any decision made on a decoded
but unverified payload is a decision made on attacker-controlled input.

## The `alg: none` vulnerability

RFC 7519 defines `none` for tokens whose integrity is already assured by other
means. Naive libraries honoured it on input: strip the signature, set
`"alg":"none"`, and a forged token verifies. Its sibling is **algorithm
confusion** — take a server's RSA *public* key, sign a token with `HS256` using
that public key as the HMAC secret, and a verifier that picks its algorithm from
the header validates it.

Both have the same fix, and it is not "check for none": **pin the accepted
algorithms in the verifier and ignore the header's `alg` entirely.** The header
is supplied by the attacker.

## ⚠️ Gotchas

- ⚠️ **Never let the token choose its own verification algorithm.** Always pass
  an explicit allowlist. This single rule kills both `alg: none` and algorithm
  confusion.
- ⚠️ **An unvalidated `aud` makes a token portable across services.** A token
  minted for a low-value service is then accepted by a high-value one. Check
  `aud` on every verification.
- ⚠️ **An unvalidated `exp` makes a leaked token permanent.** Some libraries
  skip expiry checks when you call a low-level `decode` instead of `verify`;
  `decode` performs **no** verification of any kind and must never be used for
  authorisation.
- ⚠️ **`kid` is attacker-controlled too.** Using it to build a filesystem path
  or a SQL lookup is a path-traversal and injection sink. Look it up in a fixed
  key set only.
- ⚠️ **JWTs cannot be revoked.** A stateless verifier accepts a stolen token
  until `exp`. Mitigate with short lifetimes (minutes) plus a deny-list of `jti`
  values for emergencies — which reintroduces the state JWTs were meant to
  avoid. That trade is the decision, so make it deliberately.
- **Clock skew breaks `exp` and `nbf`.** Allow a small tolerance (30–60s), and
  no more.
- **Size matters.** JWTs travel in a header on every request; stuffing claims in
  can exceed proxy header limits and returns a confusing 431 or 400.
- **`HS256` with a weak secret is offline-crackable.** If you must use HMAC, the
  secret needs to be high-entropy and long — see [[API - HMAC Signatures]].

---

## Related

- [[API - OAuth 2.0 Flows]]
- [[API - OIDC and Federated Identity]]
- [[API - HMAC Signatures]]
- [[GitHub - Bots and Apps]]

## Sources

- <https://www.rfc-editor.org/rfc/rfc7519.html>
- <https://www.rfc-editor.org/rfc/rfc8725.html>
- <https://jwt.io/introduction>
