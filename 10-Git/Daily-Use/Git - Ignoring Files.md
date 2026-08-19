---
title: Ignoring Files
domain: git
section: 06
category: daily-use
difficulty: beginner
danger: low
tags:
  - git/config
commands:
  - git check-ignore
  - git rm --cached
related:
  - "[[Git - Setup and Config]]"
  - "[[Git - Submodules and LFS]]"
  - "[[Android - Project Structure]]"
sources:
  - https://git-scm.com/docs/gitignore
  - https://git-scm.com/docs/gitattributes
  - https://git-scm.com/docs/git-check-ignore
  - https://github.com/github/gitignore
  - https://git-scm.com/book/en/v2/Customizing-Git-Git-Attributes
updated: 2026-08-14
---

# Ignoring Files


## `.gitignore` syntax

```gitignore
# comment
*.log                # any .log anywhere
build/               # directory named build, anywhere
/build               # only build/ at repo ROOT
doc/*.txt            # .txt directly in doc/
doc/**/*.txt         # .txt at any depth under doc/
!important.log       # negate — re-include
temp?.txt            # single-char wildcard
[abc].txt            # character class
\#literal-hash.txt   # escape
```

Rules:
- Later patterns override earlier ones.
- A trailing `/` means directory-only.
- A leading `/` anchors to the `.gitignore` file's own directory.
- **You cannot re-include a file if its parent directory is excluded.** Use
  `dir/*` + `!dir/keep` rather than `dir/`.
- `.gitignore` files nest — one per directory, deeper ones take precedence.

## Where ignore rules live

| File | Scope | Committed? |
|---|---|---|
| `.gitignore` | Repo, shared with team | Yes |
| `.git/info/exclude` | This clone only | No |
| Global excludes file | All your repos | No |

```bash
git config --global core.excludesfile ~/.gitignore_global
```

Convention: project-wide artifacts go in `.gitignore`; your personal editor
noise (`.idea/`, `.DS_Store`) belongs in the global file, not in the team's.

## `.gitattributes`

Per-path behavior, committed to the repo:

```gitattributes
* text=auto                          # normalize line endings for all text
*.sh   text eol=lf                   # always LF
*.bat  text eol=crlf
*.png  binary                        # = -diff -merge -text
*.lock -diff                         # don't show diffs for lockfiles
*.md   diff=markdown                 # language-aware hunk headers
CHANGELOG.md merge=union             # append both sides on conflict
secrets.enc filter=git-crypt
dist/  linguist-generated=true       # GitHub: collapse in PR view
```

## The already-tracked gotcha

**`.gitignore` only affects untracked files.** Adding a pattern for a file Git
already tracks does nothing. To fix:

```bash
git rm --cached path/to/file       # single file
git rm -r --cached .               # or nuke the index
git add .
git commit -m "Apply updated .gitignore"
```

Useful debugging:

```bash
git check-ignore -v path/to/file   # shows WHICH rule in WHICH file matched
git status --ignored
```

⚠️ If you accidentally committed a secret, removing it in a *new* commit does not
remove it from history. See §12.10.

---

## Related

- [[Git - Setup and Config]]
- [[Git - Submodules and LFS]]
- [[Android - Project Structure]]

## Sources

- <https://git-scm.com/docs/gitignore>
- <https://git-scm.com/docs/gitattributes>
- <https://git-scm.com/docs/git-check-ignore>
- <https://github.com/github/gitignore>
- <https://git-scm.com/book/en/v2/Customizing-Git-Git-Attributes>
