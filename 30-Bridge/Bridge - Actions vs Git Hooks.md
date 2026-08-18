---
title: Actions vs Git Hooks
domain: bridge
section: B5
category: bridge
difficulty: intermediate
danger: low
tags:
  - bridge
  - git/hooks
  - github/actions
commands: []
related:
  - "[[Git - Hooks]]"
  - "[[GitHub - Actions]]"
  - "[[Bridge - Branch Protection vs Hooks]]"
sources:
  - https://git-scm.com/docs/githooks
  - https://docs.github.com/en/actions
updated: 2026-08-14
---

# Actions vs Git Hooks

> **Git does X. GitHub wraps it as Y.**

Both run code in response to Git events. Almost nothing else is the same.

| | Git hooks | GitHub Actions |
|---|---|---|
| Trigger | Local Git operations | GitHub events (push, PR, issue, schedule, API) |
| Environment | Your machine, your tools | A clean runner you specify |
| Latency | Milliseconds | Seconds to minutes |
| Cost | Free | Minutes (free for public repos) |
| Secrets | Whatever's in your shell | Managed, masked, environment-scoped |
| Visible to team | ❌ | ✅ every run logged |
| Blocks a merge | ❌ | ✅ as a required check |

## The event surface barely overlaps

Git hooks fire on: commit, merge, rebase, checkout, push, receive.

Actions fire on all of those **plus** things Git has no concept of: PR opened,
review submitted, issue labeled, release published, comment created, schedule,
manual dispatch, and arbitrary API calls (`repository_dispatch`).

That's the real distinction. Most of what you want to automate on GitHub isn't a
Git event at all.

## Which to use

| Task | Where |
|---|---|
| Format staged files | Hook (`pre-commit`) |
| Validate commit message | Hook (`commit-msg`) + CI check |
| Run the full test suite | Actions |
| Block a merge on failure | Actions (as a required check) |
| Deploy | Actions |
| Auto-label a PR | Actions |
| Notify Slack on release | Actions |
| Prevent committing a secret | **Both** — hook for speed, push protection for truth |

## Rule of thumb

> Hooks give **fast feedback to one developer**.
> Actions give **enforceable outcomes to the whole team**.

If losing the check would matter, it belongs in Actions. See
[[Bridge - Branch Protection vs Hooks]] for the enforcement half.

---

## Related

- [[Git - Hooks]]
- [[GitHub - Actions]]
- [[Bridge - Branch Protection vs Hooks]]

## Sources

- <https://git-scm.com/docs/githooks>
- <https://docs.github.com/en/actions>
