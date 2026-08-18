---
title: Actions
domain: github
section: 12
category: automation
difficulty: intermediate
danger: medium
tags:
  - github/actions
  - github/ci
commands: []
endpoints:
  - GET /repos/{owner}/{repo}/actions/runs
  - GET /repos/{owner}/{repo}/actions/runs/{id}/jobs
  - GET /repos/{owner}/{repo}/actions/workflows
  - GET /repos/{owner}/{repo}/commits/{ref}/check-runs
dashboard_relevant: true
related:
  - "[[GitHub - Actions Advanced]]"
  - "[[Bridge - Actions vs Git Hooks]]"
  - "[[GitHub - Branch Protection and Rulesets]]"
  - "[[API - JSON YAML and TOML]]"
sources:
  - https://docs.github.com/en/actions
  - https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions
  - https://docs.github.com/en/rest/actions/workflow-runs
updated: 2026-08-14
---

# Actions

## Model

```
Workflow (.github/workflows/*.yml)
└── Job          (runs on one runner, parallel by default)
    └── Step     (a `run` shell command or a `uses` action)
```

Jobs are isolated — each gets a fresh runner. Data passes between them via
`outputs` or artifacts, never the filesystem.

## Minimal workflow

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:        # manual trigger button

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v5
        with:
          node-version: 22
          cache: npm
      - run: npm ci
      - run: npm test
```

## Triggers worth knowing

| Event | Notes |
|---|---|
| `push`, `pull_request` | The basics |
| `pull_request_target` | ⚠️ Runs in **base** repo context with secrets — the classic fork-PR privilege escalation. Never check out untrusted code here. |
| `workflow_dispatch` | Manual, with typed inputs |
| `schedule` | Cron. Best-effort — can be delayed or skipped under load, and disabled after 60 days of repo inactivity |
| `workflow_run` | Chain workflows |
| `repository_dispatch` | Triggered by your API call |
| `issues`, `issue_comment`, `release` | Automation hooks |

## Status vs. conclusion

Two separate fields on a run — a constant source of dashboard bugs:

- `status`: `queued` · `in_progress` · `completed` · `waiting`
- `conclusion` (only when `status == completed`): `success` · `failure` ·
  `cancelled` · `skipped` · `timed_out` · `action_required` · `neutral` · `stale`

⚠️ A run that is still `in_progress` has `conclusion: null`. Rendering a null
conclusion as "failed" is the most common CI-widget bug.

## Checks vs. runs

For "is this commit green?", query **check runs** on the SHA rather than workflow
runs — the check API includes non-Actions CI providers too:

```http
GET /repos/{owner}/{repo}/commits/{sha}/check-runs
GET /repos/{owner}/{repo}/commits/{sha}/status     # legacy commit statuses
```

Both exist; a complete picture needs both.

## GITHUB_TOKEN

Auto-generated per run, scoped to that repo, expires when the job ends. Rate
limited to **1,000 requests/hour per repository** — much lower than a PAT. See
[[GitHub - Rate Limits]].

⚠️ Pushes made with `GITHUB_TOKEN` do **not** trigger further workflows. This is
deliberate loop protection; use a PAT or App token if you need chaining.

Set least-privilege permissions explicitly:

```yaml
permissions:
  contents: read
  pull-requests: write
```

---

## Related

- [[GitHub - Actions Advanced]]
- [[Bridge - Actions vs Git Hooks]]
- [[GitHub - Branch Protection and Rulesets]]
- [[API - JSON YAML and TOML]]

## Sources

- <https://docs.github.com/en/actions>
- <https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions>
- <https://docs.github.com/en/rest/actions/workflow-runs>
