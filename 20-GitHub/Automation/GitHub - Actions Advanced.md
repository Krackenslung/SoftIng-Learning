---
title: Actions Advanced
domain: github
section: 13
category: automation
difficulty: advanced
danger: medium
tags:
  - github/actions
  - github/ci
commands: []
related:
  - "[[GitHub - Actions]]"
  - "[[GitHub - Rate Limits]]"
  - "[[API - OIDC and Federated Identity]]"
sources:
  - https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows
  - https://docs.github.com/en/actions/reference/limits
  - https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets
updated: 2026-08-14
---

# Actions Advanced

## Matrix builds

```yaml
strategy:
  fail-fast: false
  max-parallel: 4
  matrix:
    os: [ubuntu-latest, macos-latest, windows-latest]
    node: [20, 22]
    include:
      - os: ubuntu-latest
        node: 24
        experimental: true
    exclude:
      - os: windows-latest
        node: 20
```

`fail-fast: false` is almost always what you want — otherwise one failure
cancels every other leg and you lose the diagnostic signal.

## Reusable workflows vs. composite actions

| | Reusable workflow | Composite action |
|---|---|---|
| Called with | `uses:` at **job** level | `uses:` at **step** level |
| Contains | Whole jobs | Steps only |
| Own runner | Yes | No — runs in caller's job |
| Secrets | `secrets: inherit` or explicit | Inherits from job |
| Nesting depth | 4 | 10 |

```yaml
jobs:
  call:
    uses: org/repo/.github/workflows/deploy.yml@v1
    with: { environment: production }
    secrets: inherit
```

## Caching

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
    restore-keys: ${{ runner.os }}-npm-
```

- Caches are **immutable** once written — change the key, don't overwrite
- Scoped to a branch; branches can read the default branch's cache but not
  each other's
- Evicted after 7 days unused, or when the repo cache exceeds its size limit

## Secrets, variables, environments

- **Secrets** — encrypted, masked in logs, not passed to fork PRs
- **Variables** — plaintext config
- Scoped at org → repo → environment (most specific wins)
- **Environments** add required reviewers, wait timers, and branch restrictions
  — the right place for a production deploy gate

⚠️ Masking is string matching. A secret that gets base64-encoded or JSON-escaped
in your logs is **not** masked.

## OIDC instead of long-lived secrets

```yaml
permissions:
  id-token: write
  contents: read
```

Exchanges a short-lived OIDC token with AWS/GCP/Azure. Removes stored cloud
credentials entirely — the single biggest CI security upgrade available.

## Concurrency and cancellation

```yaml
concurrency:
  group: deploy-${{ github.ref }}
  cancel-in-progress: false     # false for deploys, true for CI
```

## Limits worth remembering

- Job: 6 hours max · Workflow run: 35 days · Queue wait: 24 hours
- 1,000 API requests/hour per repo from `GITHUB_TOKEN`
- Concurrent job limits vary by plan
- Artifacts and logs retained 90 days by default (configurable 1–400)

## Debugging

- Re-run with debug logging enabled from the UI
- Set repo secrets `ACTIONS_STEP_DEBUG` / `ACTIONS_RUNNER_DEBUG` to `true`
- `act` runs workflows locally (imperfect but fast)

---

## Related

- [[GitHub - Actions]]
- [[GitHub - Rate Limits]]
- [[API - OIDC and Federated Identity]]

## Sources

- <https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows>
- <https://docs.github.com/en/actions/reference/limits>
- <https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets>
