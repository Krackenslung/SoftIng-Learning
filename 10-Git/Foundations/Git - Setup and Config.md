---
title: Setup & Configuration
domain: git
section: 03
category: foundations
difficulty: beginner
danger: none
tags:
  - git/config
commands:
  - git config
  - ssh-keygen
related:
  - "[[Bridge - Auth SSH HTTPS and Tokens]]"
  - "[[Git - Ignoring Files]]"
sources:
  - https://git-scm.com/docs/git-config
  - https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup
  - https://git-scm.com/book/en/v2/Customizing-Git-Git-Attributes
  - https://git-scm.com/docs/gitcredentials
  - https://docs.github.com/en/authentication/connecting-to-github-with-ssh
  - https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
updated: 2026-08-14
---

# Setup & Configuration


## Config levels

Later levels override earlier ones.

| Level | Flag | Location |
|---|---|---|
| System | `--system` | `/etc/gitconfig` |
| Global (user) | `--global` | `~/.gitconfig` or `~/.config/git/config` |
| Local (repo) | `--local` | `.git/config` |
| Worktree | `--worktree` | `.git/config.worktree` |

```bash
git config --list --show-origin     # every setting + which file set it
git config user.email               # read one value
git config --global user.email "you@example.com"
git config --edit --global          # open in $EDITOR
```

## Minimum viable setup

```bash
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
git config --global core.editor "code --wait"    # or vim, nano, etc.
git config --global pull.rebase true             # avoid noisy merge commits
git config --global push.autoSetupRemote true    # bare `git push` on new branch
git config --global rerere.enabled true          # remember conflict resolutions
git config --global diff.algorithm histogram     # better diffs than default
git config --global fetch.prune true             # drop deleted remote branches
```

## Line endings

The classic cross-platform footgun. Windows uses CRLF, Unix uses LF.

```bash
# Windows
git config --global core.autocrlf true    # LF in repo, CRLF in working dir
# macOS / Linux
git config --global core.autocrlf input   # convert CRLF→LF on commit only
```

Better still, commit a `.gitattributes` so behavior is repo-defined rather than
per-developer (see §6.3).

## Aliases

```bash
git config --global alias.st  status
git config --global alias.co  checkout
git config --global alias.br  branch
git config --global alias.lg  "log --oneline --graph --decorate --all"
git config --global alias.last "log -1 HEAD --stat"
git config --global alias.unstage "restore --staged"
# shell command alias — prefix with !
git config --global alias.root '!pwd'
```

## Authentication: SSH vs. HTTPS

**SSH** — key-based, no per-push prompt.

```bash
ssh-keygen -t ed25519 -C "you@example.com"
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub          # paste into the forge's SSH key settings
ssh -T git@github.com              # verify
```

**HTTPS** — uses a credential helper plus a personal access token (not your
account password; forges disabled password auth for Git years ago).

```bash
git config --global credential.helper osxkeychain   # macOS
git config --global credential.helper manager       # Windows (Git Credential Manager)
git config --global credential.helper "cache --timeout=3600"  # Linux, in-memory
git config --global credential.helper store         # Linux, PLAINTEXT on disk — avoid
```

Rule of thumb: SSH for your own machines, HTTPS + token for CI and containers.

---

## Related

- [[Bridge - Auth SSH HTTPS and Tokens]]
- [[Git - Ignoring Files]]

## Sources

- <https://git-scm.com/docs/git-config>
- <https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup>
- <https://git-scm.com/book/en/v2/Customizing-Git-Git-Attributes>
- <https://git-scm.com/docs/gitcredentials>
- <https://docs.github.com/en/authentication/connecting-to-github-with-ssh>
- <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens>
