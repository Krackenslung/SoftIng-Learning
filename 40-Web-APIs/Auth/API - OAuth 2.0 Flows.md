---
title: OAuth 2.0 Flows
domain: api
section: "46"
category: auth
difficulty: intermediate
danger: medium
tags:
  - api/auth
  - api/oauth
commands: []
dashboard_relevant: true
related:
  - "[[API - JWT]]"
  - "[[API - OIDC and Federated Identity]]"
  - "[[GitHub - Authentication]]"
  - "[[Bridge - Auth SSH HTTPS and Tokens]]"
sources:
  - https://www.rfc-editor.org/rfc/rfc6749.html
  - https://www.rfc-editor.org/rfc/rfc7636.html
  - https://www.rfc-editor.org/rfc/rfc9700.html
updated: 2026-08-18
---

# OAuth 2.0 Flows

OAuth 2.0 is a **delegation** protocol, not an authentication protocol. It
answers "may this application act on the user's behalf, and how far?" — never
"who is this user?". Confusing the two is the root of most OAuth security
incidents; for identity you want [[API - OIDC and Federated Identity]], which is
a layer on top.

## The four parties

| Party | Role |
|---|---|
| Resource owner | The user who owns the data |
| Client | The application asking for access |
| Authorization server | Issues tokens after the user consents |
| Resource server | The API that accepts the token |

The client never sees the user's password. That is the entire point: the user
authenticates to the authorization server, and the client receives a scoped,
revocable, expiring token instead of a credential.

## Grant types

| Grant | Use it for | Status |
|---|---|---|
| Authorization code + PKCE | Web apps, SPAs, mobile, CLI | **The default** |
| Client credentials | Machine-to-machine, no user involved | Current |
| Device authorization | TVs, CLIs, input-constrained devices | Current |
| Refresh token | Renewing access without re-prompting | Current |
| Implicit | — | **Deprecated** |
| Resource owner password | — | **Deprecated** |

RFC 9700 (the OAuth 2.0 Security Best Current Practice) formally removes the
last two. **Implicit** returned the access token in the URL fragment, where it
leaked into browser history, referrers and logs, and could not be authenticated.
**Password grant** requires the user to hand their password to the client, which
defeats the reason OAuth exists and is incompatible with MFA.

## Authorization code with PKCE

PKCE ("pixie", RFC 7636) closes the interception attack: an attacker who steals
the authorization code off the redirect cannot redeem it without a secret the
legitimate client never transmitted.

```text
1. client  -> generates code_verifier (random), code_challenge = S256(verifier)
2. browser -> GET /authorize?response_type=code
                &client_id=...&redirect_uri=...&scope=...&state=...
                &code_challenge=...&code_challenge_method=S256
3. user consents; server redirects back with ?code=...&state=...
4. client  -> POST /token  { code, code_verifier, client_id }
5. server  <- { access_token, refresh_token, expires_in, scope }
```

```js
const verifier = base64url(crypto.getRandomValues(new Uint8Array(32)));
const challenge = base64url(
  await crypto.subtle.digest("SHA-256", new TextEncoder().encode(verifier)),
);
```

Originally a mobile-only mitigation, PKCE is now recommended for **every**
client type, including confidential server-side ones.

## `state` versus PKCE

They defend different things and you need both:

| Parameter | Defends against | Mechanism |
|---|---|---|
| `state` | CSRF on the redirect endpoint | Random value echoed back and compared |
| `code_verifier` | Code interception | Proof the redeemer started the flow |

## Scopes are not permissions

A scope is what the *client asked for*; the effective permission is the
intersection of the scope, what the user actually granted, and what that user is
allowed to do. A token with `repo` scope belonging to a read-only collaborator
still cannot push.

Grant the narrowest scope that works, and re-check on the resource server. Scope
strings are opaque conventions — `repo`, `read:org`, `admin:repo_hook` are
GitHub's, and mean nothing to another provider.

## Token lifetimes

| Token | Lifetime | Storage |
|---|---|---|
| Access token | Minutes to an hour | Memory; send as `Authorization: Bearer` |
| Refresh token | Days to months | Encrypted at rest, server side |

Refresh tokens should **rotate**: each use issues a new one and invalidates the
old. If an old refresh token is presented again, that is evidence of theft and
the whole family should be revoked.

## ⚠️ Gotchas

- ⚠️ **OAuth does not authenticate the user.** An access token proves delegated
  access, not identity. Treating a successful token exchange as "logged in as
  whoever this token belongs to" enables token substitution: a token minted for
  a different application, or a different user, is still a valid token. Use an
  OIDC `id_token` and validate its `aud`.
- ⚠️ **Validate `redirect_uri` by exact string match.** Prefix or wildcard
  matching lets an open redirect on your domain forward codes to an attacker.
  This is the most-exploited OAuth misconfiguration.
- ⚠️ **Always verify `state` on return.** Skipping it lets an attacker splice
  their own authorization code into a victim's session, linking the victim's
  account to the attacker's identity.
- ⚠️ **Never put tokens in query strings.** URLs land in server logs, proxy
  logs, browser history and `Referer` headers. Use the `Authorization` header —
  see [[API - Headers]].
- **A refresh token is the more valuable secret.** It outlives access tokens and
  regenerates them; leaking one is a durable compromise.
- **Revocation is not instant.** Most resource servers validate tokens locally
  until expiry, so "revoked" means "revoked at next refresh". Keep access token
  lifetimes short for this reason.
- **Consent screens are anti-phishing UI.** Requesting sweeping scopes trains
  users to click through, which is exactly the behaviour attackers rely on.

---

## Related

- [[API - JWT]]
- [[API - OIDC and Federated Identity]]
- [[GitHub - Authentication]]
- [[Bridge - Auth SSH HTTPS and Tokens]]

## Sources

- <https://www.rfc-editor.org/rfc/rfc6749.html>
- <https://www.rfc-editor.org/rfc/rfc7636.html>
- <https://www.rfc-editor.org/rfc/rfc9700.html>
