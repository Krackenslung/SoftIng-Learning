---
title: Hooks & Automation
domain: git
section: 21
category: advanced
difficulty: intermediate
danger: low
tags:
  - git/automation
  - git/hooks
commands:
  - core.hooksPath
related:
  - "[[Bridge - Actions vs Git Hooks]]"
  - "[[GitHub - Actions]]"
  - "[[Git - Commit Conventions]]"
sources:
  - https://git-scm.com/docs/githooks
  - https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks
  - https://git-scm.com/book/en/v2/Customizing-Git-An-Example-Git-Enforced-Policy
  - https://pre-commit.com/
  - https://typicode.github.io/husky/
  - https://github.com/lint-staged/lint-staged
  - https://lefthook.dev/
  - https://docs.github.com/en/actions
updated: 2026-08-14
---

# Hooks & Automation


## How hooks work

Scripts in `.git/hooks/` that Git executes at defined points. Any executable file
with the right name and the executable bit set. Samples ship with `.sample`
suffixes.

⚠️ **Hooks in `.git/hooks/` are not cloned or version-controlled.** To share them
across a team, commit them to a tracked directory and point Git at it:

```bash
git config core.hooksPath .githooks
```

## Client-side hooks

| Hook | Fires | Can abort? | Typical use |
|---|---|---|---|
| `pre-commit` | Before commit message editor | Yes | Lint, format, run fast tests |
| `prepare-commit-msg` | Before editor opens | Yes | Insert a template / ticket ID |
| `commit-msg` | After message entered | Yes | Enforce message format |
| `post-commit` | After commit | No | Notifications |
| `pre-rebase` | Before rebase | Yes | Protect certain branches |
| `post-checkout` | After checkout/switch | No | Rebuild deps, print reminders |
| `post-merge` | After merge | No | `npm install` if lockfile changed |
| `pre-push` | Before push | Yes | Full test suite, block WIP commits |

Nonzero exit from an abortable hook cancels the operation.

## Server-side hooks

| Hook | Fires | Use |
|---|---|---|
| `pre-receive` | Before any ref updates | Global policy enforcement |
| `update` | Once per ref | Per-branch permissions |
| `post-receive` | After all updates | Deploy, notify, trigger CI |

Note: hosted forges (GitHub, GitLab SaaS) don't let you install raw server hooks
— use their branch protection rules, required status checks, and Actions/CI
instead.

## Minimal example

```bash
#!/bin/sh
# .githooks/pre-commit
if git diff --cached --name-only | grep -qE '\.(js|ts)$'; then
    npm run lint:staged || {
        echo "❌ Lint failed. Commit aborted."
        exit 1
    }
fi
```

```bash
chmod +x .githooks/pre-commit
```

## Frameworks

Managing hooks by hand doesn't scale. Common tools:

- **pre-commit** (Python, language-agnostic) — declarative `.pre-commit-config.yaml`
- **Husky** (JS ecosystem) — hooks committed to the repo
- **lint-staged** — run linters only on staged files, pairs with Husky
- **lefthook** (Go, fast, parallel)

## Bypassing

```bash
git commit --no-verify        # skip pre-commit + commit-msg
git push --no-verify          # skip pre-push
```

Available, occasionally necessary, and a habit worth not forming. Hooks should be
fast enough that skipping them isn't tempting — this is why `lint-staged` exists.

---

## Related

- [[Bridge - Actions vs Git Hooks]]
- [[GitHub - Actions]]
- [[Git - Commit Conventions]]

## Sources

- <https://git-scm.com/docs/githooks>
- <https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks>
- <https://git-scm.com/book/en/v2/Customizing-Git-An-Example-Git-Enforced-Policy>
- <https://pre-commit.com/>
- <https://typicode.github.io/husky/>
- <https://github.com/lint-staged/lint-staged>
- <https://lefthook.dev/>
- <https://docs.github.com/en/actions>
