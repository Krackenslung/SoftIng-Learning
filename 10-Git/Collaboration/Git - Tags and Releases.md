---
title: Tags & Releases
domain: git
section: 16
category: collaboration
difficulty: intermediate
danger: medium
tags:
  - git/tags
  - git/releases
commands:
  - git tag
  - git describe
  - git push --follow-tags
related:
  - "[[Bridge - Tags vs Releases]]"
  - "[[GitHub - Releases and Packages]]"
sources:
  - https://git-scm.com/docs/git-tag
  - https://git-scm.com/docs/git-describe
  - https://git-scm.com/book/en/v2/Git-Basics-Tagging
  - https://semver.org/
  - https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository
updated: 2026-08-14
---

# Tags & Releases


## Lightweight vs. annotated

| | Lightweight | Annotated |
|---|---|---|
| Storage | A ref pointing at a commit | A full Git **object** |
| Metadata | None | Tagger, date, message, optional signature |
| Use for | Private/temporary markers | **Releases** — always |

```bash
git tag v1.0.0                                  # lightweight
git tag -a v1.0.0 -m "Release version 1.0.0"    # annotated ← use this
git tag -s v1.0.0 -m "Signed release"           # signed
git tag -a v1.0.0 abc123                        # tag a past commit
```

## Managing tags

```bash
git tag                       # list
git tag -l "v1.*"             # filter
git tag -n                    # with messages
git show v1.0.0
git tag -d v1.0.0             # delete locally
git push origin --delete v1.0.0   # delete remotely
```

⚠️ **Tags are not pushed by default.**

```bash
git push origin v1.0.0
git push origin --tags        # all tags
git push --follow-tags        # only annotated tags reachable from what you push ← best
```

⚠️ **Never move a published tag.** People and build systems pin to them.

## `git describe`

Generates a human-readable version string from the nearest tag:

```bash
git describe                    # v1.2.0-14-gabc1234
git describe --tags             # include lightweight tags
git describe --always --dirty   # fall back to hash; mark uncommitted changes
```

Reads as: 14 commits after `v1.2.0`, at commit `abc1234`. Extremely useful for
embedding a build version.

## SemVer

`MAJOR.MINOR.PATCH`

- **MAJOR** — incompatible API changes
- **MINOR** — backwards-compatible functionality
- **PATCH** — backwards-compatible bug fixes

Pre-release: `1.0.0-alpha.1`. Build metadata: `1.0.0+20260814`.

Convention is to prefix Git tags with `v` (`v1.0.0`) even though SemVer itself
doesn't include it.

## Checking out a tag

```bash
git checkout v1.0.0             # → detached HEAD
git switch -c hotfix-1.0.1 v1.0.0   # branch from a tag to make changes
```

---

## Related

- [[Bridge - Tags vs Releases]]
- [[GitHub - Releases and Packages]]

## Sources

- <https://git-scm.com/docs/git-tag>
- <https://git-scm.com/docs/git-describe>
- <https://git-scm.com/book/en/v2/Git-Basics-Tagging>
- <https://semver.org/>
- <https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository>
