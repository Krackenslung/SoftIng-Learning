---
title: Searching History
domain: git
section: 17
category: investigation
difficulty: intermediate
danger: none
tags:
  - git/search
commands:
  - git log -S
  - git grep
  - git shortlog
  - git range-diff
related:
  - "[[Git - Blame Bisect Reflog]]"
  - "[[GitHub - Search Syntax]]"
sources:
  - https://git-scm.com/docs/git-log
  - https://git-scm.com/docs/git-grep
  - https://git-scm.com/docs/git-shortlog
  - https://git-scm.com/docs/git-range-diff
  - https://git-scm.com/docs/git-rev-list
  - https://git-scm.com/docs/gitrevisions
  - https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History
updated: 2026-08-14
---

# Searching History


## Filtering `git log`

```bash
git log --author="Jane"
git log --committer="Bot"
git log --grep="fix" --grep="bug" --all-match -i    # message search
git log --since="2026-01-01" --until="2026-06-30"
git log --since="2 weeks ago"
git log -- src/auth/          # commits touching a path
git log --follow -- file.js   # follow through renames
git log --merges / --no-merges
git log --first-parent main   # trunk history only, skipping merged-in commits
git log -n 20
git log --reverse
git log --cherry-pick main...feature   # drop commits present on both sides
```

## The pickaxe — searching *content*

The most underused capability in Git.

```bash
git log -S "functionName"          # commits where the COUNT of occurrences changed
                                   # → finds where it was added/removed
git log -S "API_KEY" --pickaxe-regex
git log -G "regex.*pattern"        # commits whose DIFF matches the regex
git log -S "thing" -p              # show the patches too
git log -L 10,20:file.js           # evolution of LINES 10–20
git log -L :functionName:file.js   # evolution of a whole function
```

`-S` answers "when did this string appear or disappear?" `-G` answers "which
commits have a diff mentioning this?"

## `git grep` — searching the tree

Much faster than `grep -r` because it only searches tracked files.

```bash
git grep "TODO"
git grep -n "TODO"                 # line numbers
git grep -i --heading --break "todo"
git grep "pattern" v1.0.0          # search at a past revision
git grep "pattern" $(git rev-list --all)    # search ALL history ⚠️ slow
git grep -c "pattern"              # count per file
git grep -l "pattern"              # filenames only
git grep -e "a" --and -e "b"
git grep "pattern" -- "*.js"       # limit by pathspec
```

## `git shortlog`

```bash
git shortlog -sn                   # commit counts per author
git shortlog -sne                  # + emails
git shortlog -sn --since="1 year ago"
git shortlog --no-merges v1.0.0..v2.0.0   # changelog material, grouped by author
```

## Comparing refs

```bash
git log main..feature              # in feature, not main
git log feature..main              # in main, not feature
git log main...feature             # in either but not both
git diff main...feature            # feature's changes since divergence
git range-diff main feature-v1 feature-v2   # compare two versions of a series
git rev-list --count main..feature # how many commits ahead
git merge-base main feature        # the common ancestor
```

`git range-diff` is invaluable for reviewing "what changed between v1 and v2 of
this patch series/PR".

---

## Related

- [[Git - Blame Bisect Reflog]]
- [[GitHub - Search Syntax]]

## Sources

- <https://git-scm.com/docs/git-log>
- <https://git-scm.com/docs/git-grep>
- <https://git-scm.com/docs/git-shortlog>
- <https://git-scm.com/docs/git-range-diff>
- <https://git-scm.com/docs/git-rev-list>
- <https://git-scm.com/docs/gitrevisions>
- <https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History>
