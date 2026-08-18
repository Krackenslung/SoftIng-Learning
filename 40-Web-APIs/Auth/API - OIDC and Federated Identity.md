---
title: OIDC and Federated Identity
domain: api
section: "49"
category: auth
difficulty: advanced
danger: medium
tags:
  - api/auth
  - api/oidc
  - api/security
commands: []
dashboard_relevant: true
related:
  - "[[API - OAuth 2.0 Flows]]"
  - "[[API - JWT]]"
  - "[[GitHub - Actions Advanced]]"
  - "[[Bridge - Auth SSH HTTPS and Tokens]]"
sources:
  - https://openid.net/specs/openid-connect-core-1_0.html
  - https://openid.net/specs/openid-connect-discovery-1_0.html
  - https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-cloud-providers
updated: 2026-08-18
---

# OIDC and Federated Identity

OpenID Connect is a thin identity layer on top of [[API - OAuth 2.0 Flows]]. It
adds one thing OAuth deliberately lacks: a verifiable statement of **who the
user is**, in the form of an `id_token`. Its second and increasingly more
important use is machine identity — letting a CI job prove what it is to a cloud
provider so that no long-lived secret has to exist at all.

## What OIDC adds to OAuth

| | OAuth 2.0 | OpenID Connect |
|---|---|---|
| Answers | May this app act for the user? | Who is the user? |
| Returns | `access_token` (opaque) | `access_token` + `id_token` (a JWT) |
| Audience of the token | The resource server | **The client** |
| Discovery | Out of band | `/.well-known/openid-configuration` |
| Key distribution | Out of band | JWKS endpoint, with `kid` rotation |

The `id_token` is a JWT and is validated exactly as [[API - JWT]] describes,
with one addition: `nonce`, echoed from the authorization request, binds the
token to your specific login attempt and blocks replay.

## Discovery and keys

```http
GET /.well-known/openid-configuration
```

```json
{
  "issuer": "https://token.actions.githubusercontent.com",
  "jwks_uri": "https://token.actions.githubusercontent.com/.well-known/jwks",
  "id_token_signing_alg_values_supported": ["RS256"]
}
```

Fetch the JWKS, select the key by `kid`, cache it, and refetch when an unknown
`kid` appears — that is how issuers rotate keys without breaking verifiers.
Cache with a floor on refetch frequency, or an attacker can force unbounded
outbound requests by sending random `kid` values.

## Workload identity: the keyless pattern

This is where OIDC matters most day to day. Instead of storing a cloud
credential in CI secrets, the CI platform mints a short-lived OIDC token
describing the running job, and the cloud provider exchanges it for temporary
credentials:

```text
1. workflow starts -> requests an id_token from the CI provider
2. token claims:      iss = the CI provider
                      sub = repo:octocat/hello:ref:refs/heads/main
                      aud = sts.amazonaws.com
3. workflow -> cloud STS: "here is my token, give me a role"
4. cloud verifies signature + iss + aud + sub against a trust policy
5. cloud <- temporary credentials, valid for minutes
```

```yaml
permissions:
  id-token: write        # required to mint the token
  contents: read
```

Nothing long-lived is stored anywhere. There is no secret to leak, rotate or
find in a git history. See [[GitHub - Actions Advanced]].

## The trust policy is the security boundary

The cloud side decides which tokens it honours, and that condition is the whole
control:

| Condition | Effect |
|---|---|
| `sub = repo:org/repo:ref:refs/heads/main` | Only `main` in that repo |
| `sub = repo:org/repo:environment:prod` | Only the `prod` environment |
| `sub = repo:org/*` | **Any repo in the org** |
| `sub = repo:org/repo:*` | Any branch, tag or **pull request** in that repo |

## ⚠️ Gotchas

- ⚠️ **A wildcard `sub` in a trust policy is a full compromise.** `repo:org/*`
  means anyone who can create a repository in the organisation can assume your
  production role. `repo:org/repo:*` means anyone who can open a pull request
  can. Pin to specific refs or environments, and prefer environments with
  required reviewers.
- ⚠️ **`aud` must be pinned on the cloud side.** Without it, a token minted for
  any other audience is accepted, and tokens are handed out freely to workflows
  across the whole platform.
- ⚠️ **`iss` must be pinned to the exact issuer URL.** Matching loosely, or
  trusting whatever the token claims, lets an attacker stand up their own
  issuer and mint whatever `sub` they like.
- ⚠️ **An `id_token` is not an access token.** It is proof of identity, for
  *you*, and should never be forwarded to a third-party API as a credential.
  Sending it onward hands that party a token they can present elsewhere if the
  `aud` check is weak.
- ⚠️ **`email` in an `id_token` is not proof of email ownership** unless
  `email_verified` is true. Matching accounts on an unverified email lets
  someone claim an account by signing up with that address at a federated
  provider.
- **Validate `nonce` on interactive logins.** It is the OIDC-layer equivalent of
  `state` and defends against token replay into a different session.
- **These tokens are short-lived by design** — often minutes. Do not try to
  cache or persist one; request a fresh token per job.
- **`sub` format is provider-specific and versioned.** GitHub's claim format is
  configurable per repository or organisation, so a trust policy written against
  the default can break when someone customises it.

> [!tip] The point of federation
> Every long-lived cloud key in a CI secret store is a credential that can leak,
> gets copied into a second place "temporarily", and outlives the person who
> created it. OIDC replaces the class of problem rather than managing it.

---

## Related

- [[API - OAuth 2.0 Flows]]
- [[API - JWT]]
- [[GitHub - Actions Advanced]]
- [[Bridge - Auth SSH HTTPS and Tokens]]

## Sources

- <https://openid.net/specs/openid-connect-core-1_0.html>
- <https://openid.net/specs/openid-connect-discovery-1_0.html>
- <https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-cloud-providers>
