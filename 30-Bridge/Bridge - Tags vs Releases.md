---
title: Tags vs Releases
domain: bridge
section: B4
category: bridge
difficulty: beginner
danger: medium
tags:
  - bridge
  - git/tags
  - github/releases
commands:
  - git tag -a
  - git push --follow-tags
  - gh release create
related:
  - "[[Git - Tags and Releases]]"
  - "[[GitHub - Releases and Packages]]"
sources:
  - https://git-scm.com/docs/git-tag
  - https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases
updated: 2026-08-14
---

# Tags vs Releases

> **Git does X. GitHub wraps it as Y.**

## Git's side

A **tag** is a ref pointing at a commit. Annotated tags are full objects with a
tagger, date, message, and optional signature. That is the whole feature.

```bash
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0
```

## GitHub's side

A **release** is a database record *attached to* a tag, adding:

- A display name distinct from the tag
- Rich Markdown release notes (auto-generatable)
- **Binary assets** with download counts
- `draft` and `prerelease` flags
- A publication timestamp and an Atom feed

## The relationship, precisely

```
Git tag  ──1:0..1──►  GitHub release
```

- A tag can exist with **no** release. Very common.
- A release **cannot** exist without a tag — creating one creates the tag if
  needed.
- Deleting a release leaves the tag. Deleting the tag leaves an orphaned release.

## ⚠️ Gotchas

- **`git push` does not push tags.** Use `--follow-tags` (annotated only,
  reachable from what you're pushing) — the safest default.
- **`/releases/latest` ≠ newest.** It returns the latest **non-draft,
  non-prerelease** release. A repo whose newest release is a prerelease returns
  an older one — or 404s if there are none.
- **Tags are mutable if you force them.** Don't. Downstream consumers,
  `actions/checkout@v4`-style refs, and package managers all pin to tags.
- Source tarballs auto-attached by GitHub are generated on demand and their
  checksums have changed historically. Don't pin checksums to them; attach your
  own artifacts.

## Automating it

```bash
git tag -a v1.2.0 -m "Release 1.2.0"
git push --follow-tags
gh release create v1.2.0 --generate-notes ./dist/*
```

Or trigger from a workflow on `push: tags: ['v*']` — see [[GitHub - Actions]].

---

## Related

- [[Git - Tags and Releases]]
- [[GitHub - Releases and Packages]]

## Sources

- <https://git-scm.com/docs/git-tag>
- <https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases>
