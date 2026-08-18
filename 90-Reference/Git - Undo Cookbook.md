---
title: Undo Cookbook
domain: reference
section: 12
category: reference
difficulty: intermediate
danger: high
tags:
  - git/undo
  - reference
commands:
  - git reflog
  - git reset
  - git filter-repo
related:
  - "[[Git - Reset Revert Restore]]"
  - "[[Git - Blame Bisect Reflog]]"
sources:
  - https://git-scm.com/docs/git-reflog
  - https://git-scm.com/docs/git-fsck
  - https://git-scm.com/docs/git-clean
  - https://github.com/newren/git-filter-repo
  - https://git-scm.com/docs/git-filter-branch
  - https://rtyley.github.io/bfg-repo-cleaner/
  - https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
  - https://git-scm.com/docs/git-gc
updated: 2026-08-14
---

# Undo Cookbook


Recipes for the situations that cause panic. **Almost nothing is truly lost for
~90 days** — see §12.13.

## Typo in the last commit message
```bash
git commit --amend -m "Corrected message"
```

## Forgot a file in the last commit
```bash
git add forgotten.txt
git commit --amend --no-edit
```

## Committed to the wrong branch (not pushed)
```bash
git reset HEAD~1          # undo commit, keep changes in working dir
git stash
git switch correct-branch
git stash pop
git add . && git commit -m "msg"
```
Or, if the commit is already made and clean:
```bash
git switch correct-branch
git cherry-pick abc123
git switch wrong-branch
git reset --hard HEAD~1
```

## Need to undo a `git reset --hard`
```bash
git reflog                       # find the pre-reset HEAD, e.g. HEAD@{1}
git reset --hard HEAD@{1}
```

## Deleted a branch by mistake
```bash
git reflog                       # find its last commit
git switch -c recovered-branch abc123
# or:
git fsck --lost-found            # if it's not in the reflog
```

## Bad `git commit --amend` — want the original back
```bash
git reflog                       # the pre-amend commit is still there
git reset --hard HEAD@{1}
```

## Pulled and got an unwanted merge commit
```bash
git reset --hard HEAD~1          # if the merge is the last commit
git pull --rebase                # redo it correctly
```

## Rebase went wrong, mid-flight
```bash
git rebase --abort
```
Already finished and it's a mess:
```bash
git reflog                       # find the pre-rebase state
git reset --hard HEAD@{5}
# or, if ORIG_HEAD is still valid:
git reset --hard ORIG_HEAD
```

## Accidentally force-pushed over someone's work
```bash
git reflog                             # LOCAL reflog may have the old tip
# or, on the server / another clone:
git fetch origin
git reset --hard <good-commit>
git push --force-with-lease
```
On GitHub, the events API or a protected-branch audit log may retain the old SHA.

## Committed a secret
Rotate the credential first — assume it's compromised. Then scrub history:
```bash
# recommended tool (much faster than filter-branch)
git filter-repo --path secrets.env --invert-paths
git push --force --all
git push --force --tags
```
Then have every collaborator re-clone. `git filter-branch` is deprecated in favor
of `git-filter-repo`; BFG Repo-Cleaner is another option.

## Want to discard ALL local changes and match the remote
```bash
git fetch origin
git reset --hard origin/main
git clean -fd                    # remove untracked files/dirs ⚠️
git clean -fdx                   # ...including ignored files ⚠️⚠️
git clean -nd                    # DRY RUN — always do this first
```

## Committed a huge file and the repo is now bloated
```bash
git filter-repo --strip-blobs-bigger-than 10M
# then set up Git LFS for that file type (§20.4)
```

## How the safety net works
Every update to HEAD or a branch tip is logged in the **reflog**. Unreferenced
objects survive until garbage collection. Defaults:

- `gc.reflogExpire` = 90 days (reachable entries)
- `gc.reflogExpireUnreachable` = 30 days
- `gc.pruneExpire` = 2 weeks (loose object grace period)

So: if it was ever committed, you have weeks to get it back. If it was never
committed (`git clean`, unstaged `restore`), it's gone — that's the real danger
zone.

---

## Related

- [[Git - Reset Revert Restore]]
- [[Git - Blame Bisect Reflog]]

## Sources

- <https://git-scm.com/docs/git-reflog>
- <https://git-scm.com/docs/git-fsck>
- <https://git-scm.com/docs/git-clean>
- <https://github.com/newren/git-filter-repo>
- <https://git-scm.com/docs/git-filter-branch>
- <https://rtyley.github.io/bfg-repo-cleaner/>
- <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository>
- <https://git-scm.com/docs/git-gc>
