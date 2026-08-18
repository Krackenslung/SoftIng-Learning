---
title: Blame, Bisect, Reflog
domain: git
section: 18
category: investigation
difficulty: intermediate
danger: low
tags:
  - git/search
  - git/debugging
commands:
  - git blame
  - git bisect
  - git reflog
related:
  - "[[Git - Undo Cookbook]]"
  - "[[Git - Searching History]]"
sources:
  - https://git-scm.com/docs/git-blame
  - https://git-scm.com/docs/git-bisect
  - https://git-scm.com/docs/git-reflog
  - https://git-scm.com/book/en/v2/Git-Tools-Debugging-with-Git
  - https://git-scm.com/book/en/v2/Git-Tools-Revision-Selection
  - https://docs.github.com/en/repositories/working-with-files/using-files/viewing-and-understanding-files#ignore-commits-in-the-blame-view
updated: 2026-08-14
---

# Blame, Bisect, Reflog


## `git blame` — who wrote this line

```bash
git blame file.js
git blame -L 50,75 file.js              # a line range
git blame -w file.js                    # ignore whitespace changes
git blame -C file.js                    # detect code moved from other files
git blame -CCC file.js                  # try harder
git blame abc123 -- file.js             # blame as of a past commit
git blame --ignore-rev <format-commit> file.js
git blame --ignore-revs-file .git-blame-ignore-revs
```

**Pro move:** commit a `.git-blame-ignore-revs` file listing pure-formatting
commits (the day you ran Prettier across the codebase), then:

```bash
git config blame.ignoreRevsFile .git-blame-ignore-revs
```

GitHub honors this file too. It keeps blame meaningful after mass reformats.

Blame is for archaeology, not accusation — the goal is finding the commit whose
message explains *why*.

## `git bisect` — binary search for the breaking commit

```bash
git bisect start
git bisect bad                  # current commit is broken
git bisect good v1.0.0          # this old one was fine
# Git checks out a midpoint. Test it, then:
git bisect good     # ...or...     git bisect bad
# repeat — Git narrows by half each time
git bisect reset                # return to where you started
```

Over 1000 commits, this takes ~10 tests.

**Automated bisect** — the real power:

```bash
git bisect start HEAD v1.0.0
git bisect run npm test
# or any script: exit 0 = good, exit 1–124/126/127 = bad, 125 = skip
git bisect run ./test-script.sh
```

Other subcommands:
```bash
git bisect skip                 # can't test this commit (won't build)
git bisect log                  # transcript of the session
git bisect replay logfile
git bisect terms --term-old=fast --term-new=slow   # bisect for non-bug regressions
```

Bisect quality depends on commit quality: atomic commits that each build and pass
tests make bisect trivial; giant "WIP" commits make it useless.

## `git reflog` — the safety net

Records every change to HEAD and branch tips, **locally**.

```bash
git reflog                      # HEAD's history
git reflog show main            # a specific branch
git reflog --date=iso
git log -g --oneline            # reflog with log formatting
git reflog expire --expire=now --all   # ⚠️ destroys your safety net
```

Entries look like:
```
abc1234 HEAD@{0}: commit: Add feature
def5678 HEAD@{1}: rebase (finish): returning to refs/heads/main
9012345 HEAD@{2}: reset: moving to HEAD~3
```

`HEAD@{n}` is usable anywhere a commit-ish is expected:
```bash
git reset --hard HEAD@{3}
git switch -c recovered HEAD@{5}
git diff HEAD@{1} HEAD
```

Also useful: `ORIG_HEAD`, which Git sets before dangerous operations (merge,
rebase, reset), giving you a one-word undo target.

Key limits: the reflog is **local only** (not cloned, not pushed), and entries
expire (§12.13).

---

## Related

- [[Git - Undo Cookbook]]
- [[Git - Searching History]]

## Sources

- <https://git-scm.com/docs/git-blame>
- <https://git-scm.com/docs/git-bisect>
- <https://git-scm.com/docs/git-reflog>
- <https://git-scm.com/book/en/v2/Git-Tools-Debugging-with-Git>
- <https://git-scm.com/book/en/v2/Git-Tools-Revision-Selection>
- <https://docs.github.com/en/repositories/working-with-files/using-files/viewing-and-understanding-files#ignore-commits-in-the-blame-view>
