---
title: Auth — SSH, HTTPS and Tokens
domain: bridge
section: B6
category: bridge
difficulty: intermediate
danger: high
tags:
  - bridge
  - git/config
  - github/auth
commands:
  - ssh-keygen
  - git config credential.helper
  - gh auth login
related:
  - "[[Git - Setup and Config]]"
  - "[[GitHub - Authentication]]"
  - "[[GitHub - CLI]]"
  - "[[API - OAuth 2.0 Flows]]"
  - "[[API - JWT]]"
  - "[[API - OIDC and Federated Identity]]"
  - "[[API - Token Storage on Public Clients]]"
sources:
  - https://git-scm.com/docs/gitcredentials
  - https://docs.github.com/en/authentication/connecting-to-github-with-ssh
  - https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
updated: 2026-08-14
---

# Auth — SSH, HTTPS and Tokens

> **Git does X. GitHub wraps it as Y.**

Two different auth systems that people constantly conflate: one for **Git
transport** (push/pull), one for the **API**.

## Git transport

| Protocol | Credential | Stored in |
|---|---|---|
| SSH | Key pair | `~/.ssh/`, agent |
| HTTPS | PAT (as password) | Credential helper |

```bash
# SSH
ssh-keygen -t ed25519 -C "you@example.com"
ssh -T git@github.com

# HTTPS
git config --global credential.helper osxkeychain   # or: manager (Win)
gh auth login                                       # sets this up for you
```

## API access

**Never uses SSH.** The API is HTTPS-only and takes a token:

```http
Authorization: Bearer ghp_xxx
```

So an SSH key that lets you push does **nothing** for your dashboard. This is the
confusion worth naming explicitly.

## Choosing

| Context | Use |
|---|---|
| Your laptop, pushing code | SSH |
| CI / containers | HTTPS + short-lived token |
| API integration | Fine-grained PAT, or App installation token |
| Actions workflow | `GITHUB_TOKEN`, or OIDC for cloud |
| Signing commits | SSH key (reuse the same one) — see [[Git - Commit Conventions]] |

## Switching an existing clone

```bash
git remote set-url origin git@github.com:owner/repo.git      # → SSH
git remote set-url origin https://github.com/owner/repo.git  # → HTTPS
```

## ⚠️ Notes

- GitHub removed password auth for Git operations — a "password" prompt wants a
  **token**.
- SSH over port 22 is often blocked on corporate networks. Fall back to
  `ssh.github.com:443` via `~/.ssh/config`.
- `credential.helper store` writes **plaintext** to `~/.git-credentials`. Avoid.
- Deploy keys are per-repo SSH keys, read-only by default — the right choice for
  a server that only needs to clone one repo.
- SAML-enforced orgs require PATs to be **explicitly authorized** for the org, in
  addition to having the right scopes. Failure looks like a 404.

See [[GitHub - Authentication]] for the full token matrix.

---

## Related

- [[Git - Setup and Config]]
- [[GitHub - Authentication]]
- [[GitHub - CLI]]
- [[API - OAuth 2.0 Flows]]
- [[API - JWT]]
- [[API - OIDC and Federated Identity]]
- [[API - Token Storage on Public Clients]]

## Sources

- <https://git-scm.com/docs/gitcredentials>
- <https://docs.github.com/en/authentication/connecting-to-github-with-ssh>
- <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens>
