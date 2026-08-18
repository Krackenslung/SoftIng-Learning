---
title: Commit Conventions & Signing
domain: git
section: 15
category: collaboration
difficulty: beginner
danger: none
tags:
  - git/commits
  - git/conventions
commands:
  - git commit
  - git verify-commit
related:
  - "[[Git - The Core Loop]]"
  - "[[Git - Tags and Releases]]"
  - "[[Git - Hooks]]"
sources:
  - https://www.conventionalcommits.org/en/v1.0.0/
  - https://semver.org/
  - https://cbea.ms/git-commit/
  - https://git-scm.com/docs/SubmittingPatches
  - https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits
  - https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification
  - https://commitlint.js.org/
updated: 2026-08-14
---

# Commit Conventions & Signing


## Atomic commits

One commit = one logical change. Test: can you write the subject line without
using "and"? If not, split it (`git add -p` makes this easy).

Benefits: reviewable diffs, meaningful `git blame`, `git bisect` actually works,
clean `git revert`.

## Message format

The widely-followed convention:

```
Short summary, imperative mood, ≤50 chars

Wrap the body at 72 characters. Explain WHAT changed and, far more
importantly, WHY. The diff already shows what. It cannot show the
reasoning, the alternatives you rejected, or the constraint that
forced this approach.

- Bullets are fine
- Reference issues: Fixes #123

Co-authored-by: Name <email@example.com>
```

Rules that hold up: imperative mood ("Add feature", not "Added"/"Adds"); no
trailing period in the subject; blank line between subject and body; capitalize
the subject.

Why imperative? It matches Git's own generated messages ("Merge branch...",
"Revert..."), and reads as a command describing what applying the commit does.

## Conventional Commits

A machine-parseable superset, widely used to drive automated changelogs and
semantic version bumps.

```
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`,
`ci`, `chore`, `revert`.

```
feat(auth): add OAuth2 login flow
fix: prevent race condition in token refresh
docs(readme): clarify install steps
refactor!: drop support for Node 16

BREAKING CHANGE: Node 18 is now the minimum.
```

Mapping to SemVer: `fix` → PATCH, `feat` → MINOR, `!` or `BREAKING CHANGE:` →
MAJOR.

## Signing

Proves a commit came from you. Two mechanisms:

**GPG:**
```bash
gpg --full-generate-key
gpg --list-secret-keys --keyid-format=long
git config --global user.signingkey <KEY_ID>
git config --global commit.gpgsign true
git config --global tag.gpgsign true
```

**SSH** (simpler — reuse your existing key; Git 2.34+):
```bash
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
```

Verify:
```bash
git log --show-signature
git verify-commit HEAD
git verify-tag v1.0.0
```

## Commit templates & hooks

```bash
git config --global commit.template ~/.gitmessage
```

Enforce conventions in CI or via a `commit-msg` hook (see §21); `commitlint` is
the common tool.

---

## Related

- [[Git - The Core Loop]]
- [[Git - Tags and Releases]]
- [[Git - Hooks]]

## Sources

- <https://www.conventionalcommits.org/en/v1.0.0/>
- <https://semver.org/>
- <https://cbea.ms/git-commit/>
- <https://git-scm.com/docs/SubmittingPatches>
- <https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits>
- <https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification>
- <https://commitlint.js.org/>
