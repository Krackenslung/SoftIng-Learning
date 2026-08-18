---
title: Cherry-pick
domain: git
section: 11
category: history-rewriting
difficulty: intermediate
danger: medium
tags:
  - git/history
commands:
  - git cherry-pick
  - git cherry
related:
  - "[[Git - Rebase]]"
  - "[[Git - Merging]]"
  - "[[Git - Workflows]]"
sources:
  - https://git-scm.com/docs/git-cherry-pick
  - https://git-scm.com/docs/git-cherry
  - https://git-scm.com/book/en/v2/Distributed-Git-Maintaining-a-Project
updated: 2026-08-14
---

# Cherry-pick


Apply the changes from a specific commit onto the current branch, as a new commit
with a new hash.

```bash
git cherry-pick abc123
git cherry-pick abc123 def456          # several
git cherry-pick abc123..def456         # exclusive range (abc123 NOT included)
git cherry-pick abc123^..def456        # inclusive range
git cherry-pick -n abc123              # stage only, don't commit
git cherry-pick -e abc123              # edit the message
git cherry-pick -x abc123              # append "(cherry picked from commit ...)"
git cherry-pick -m 1 <merge-commit>    # pick a merge, relative to parent 1
```

Conflict handling:

```bash
git cherry-pick --continue
git cherry-pick --skip
git cherry-pick --abort                # restore original state
git cherry-pick --quit                 # stop, but KEEP what's applied so far
```

**When it's right:** backporting a hotfix to a release branch; pulling one useful
commit off an abandoned branch; moving a commit you made on the wrong branch.

**When it's wrong:** as a substitute for merging. Cherry-picking the same work
into multiple branches creates duplicate-content commits with different hashes,
which confuses future merges and makes `git log` misleading. Use `-x` so at least
the provenance is recorded.

`git cherry` shows which commits on one branch have no equivalent on another —
useful for auditing backports:

```bash
git cherry -v main release-2.x
```

---

## Related

- [[Git - Rebase]]
- [[Git - Merging]]
- [[Git - Workflows]]

## Sources

- <https://git-scm.com/docs/git-cherry-pick>
- <https://git-scm.com/docs/git-cherry>
- <https://git-scm.com/book/en/v2/Distributed-Git-Maintaining-a-Project>
