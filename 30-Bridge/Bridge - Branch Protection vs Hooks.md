---
title: Branch Protection vs Hooks
domain: bridge
section: B3
category: bridge
difficulty: intermediate
danger: high
tags:
  - bridge
  - git/hooks
  - github/policy
commands:
  - core.hooksPath
  - git commit --no-verify
related:
  - "[[Git - Hooks]]"
  - "[[GitHub - Branch Protection and Rulesets]]"
  - "[[GitHub - Actions]]"
sources:
  - https://git-scm.com/docs/githooks
  - https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
updated: 2026-08-14
---

# Branch Protection vs Hooks

> **Git does X. GitHub wraps it as Y.**

## The core asymmetry

| | Git hooks | Branch protection / rulesets |
|---|---|---|
| Runs | On the developer's machine | On GitHub's servers |
| Version controlled | ❌ (`.git/hooks/` isn't cloned) | ✅ (config, or ruleset-as-code) |
| Bypassable | ✅ `--no-verify` | Only via explicit bypass list |
| Speed | Instant | Requires a push and a CI round-trip |
| Applies to | Whoever installed them | Everyone, always |

**Client hooks are a convenience. Server rules are the enforcement.** Anything
you actually care about must be enforced server-side, because `--no-verify` is
one flag away.

## The correct division of labour

```
Local hooks (fast feedback, ~2s budget)
├── pre-commit  → format, lint staged files
└── commit-msg  → message format check

Server rules (authority)
├── Required status checks   → the real lint + test run
├── Required reviews         → human approval
├── Required signed commits  → identity
└── Linear history           → shape
```

Run the *same* checks in both places. Local for speed, CI for truth. If they
diverge, developers learn to distrust the local ones and start using
`--no-verify` habitually.

## Distributing hooks to a team

`.git/hooks/` is not cloned. To share:

```bash
# commit hooks to a tracked directory, then:
git config core.hooksPath .githooks
```

Or use a framework that wires this up on install — `pre-commit`, `husky`,
`lefthook`. Whichever you pick, **the setup step is still manual per clone**.
That's precisely why it can't be your enforcement layer.

## The gap nobody closes

A developer who never runs the setup step has no hooks and won't know it. Add a
CI job that fails if the formatting is wrong — it's the only feedback loop that
reaches everyone.

---

## Related

- [[Git - Hooks]]
- [[GitHub - Branch Protection and Rulesets]]
- [[GitHub - Actions]]

## Sources

- <https://git-scm.com/docs/githooks>
- <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets>
