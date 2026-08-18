---
title: Troubleshooting
domain: reference
section: 23
category: reference
difficulty: beginner
danger: low
tags:
  - git/errors
  - reference
commands: []
related:
  - "[[Git - Undo Cookbook]]"
  - "[[Git - Remotes]]"
sources:
  - https://git-scm.com/docs
  - https://docs.github.com/en/authentication/troubleshooting-ssh
  - https://docs.github.com/en/get-started/using-git/dealing-with-non-fast-forward-errors
  - https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github
  - https://git-scm.com/book/en/v2/Customizing-Git-Git-Attributes
updated: 2026-08-14
---

# Troubleshooting


## `fatal: not a git repository`
Not inside a repo. `git rev-parse --show-toplevel` to check; `git init` or `cd`.

## `Updates were rejected because the remote contains work that you do not have locally`
Someone pushed since your last fetch.
```bash
git pull --rebase
git push
```

## `Your branch and 'origin/main' have diverged`
Both sides have unique commits.
```bash
git pull --rebase        # replay yours on top (preferred for feature branches)
git pull --no-rebase     # or create a merge commit
```

## `error: Your local changes would be overwritten by merge`
```bash
git stash && git pull && git stash pop
# or commit first
```

## `fatal: refusing to merge unrelated histories`
Two repos with no common ancestor (common after `git init` on both sides).
```bash
git pull origin main --allow-unrelated-histories
```

## `Permission denied (publickey)`
```bash
ssh -T git@github.com          # test
ssh-add -l                     # is the key loaded?
ssh-add ~/.ssh/id_ed25519
```

## `remote: Support for password authentication was removed`
Use a personal access token instead of a password, or switch to SSH.

## `fatal: The current branch has no upstream branch`
```bash
git push -u origin HEAD
# or permanently:
git config --global push.autoSetupRemote true
```

## `detached HEAD` warning
See §7.4. If you made commits: `git switch -c new-branch`.

## `error: cannot lock ref` / `.git/index.lock exists`
A crashed or concurrent Git process. Confirm nothing is running, then:
```bash
rm -f .git/index.lock
```

## `warning: LF will be replaced by CRLF`
Line-ending normalization. Configure `core.autocrlf` (§3.3) and commit a
`.gitattributes` (§6.3).

## `You have unmerged paths`
Finish the conflict resolution: edit files, `git add` them, then `git commit`.
Or `git merge --abort`.

## Files keep showing as modified with no visible change
Usually line endings or file mode. Try:
```bash
git config core.fileMode false
git diff --stat            # check what Git thinks changed
```

## Push rejected: file exceeds size limit
The file is in *history*, not just your working tree. See §12.12 and §20.4.

## `fatal: refusing to fetch into branch ... checked out`
Fetching into the currently checked-out branch. Fetch normally and merge, or use
a different worktree.

---

## Related

- [[Git - Undo Cookbook]]
- [[Git - Remotes]]

## Sources

- <https://git-scm.com/docs>
- <https://docs.github.com/en/authentication/troubleshooting-ssh>
- <https://docs.github.com/en/get-started/using-git/dealing-with-non-fast-forward-errors>
- <https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github>
- <https://git-scm.com/book/en/v2/Customizing-Git-Git-Attributes>
