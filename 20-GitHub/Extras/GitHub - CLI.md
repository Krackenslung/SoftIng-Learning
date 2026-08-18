---
title: GitHub CLI (gh)
domain: github
section: 23
category: extras
difficulty: beginner
danger: low
tags:
  - github/cli
  - github/tools
commands:
  - gh pr
  - gh issue
  - gh run
  - gh api
  - gh repo
dashboard_relevant: true
related:
  - "[[GitHub - REST API]]"
  - "[[GitHub - Pull Requests]]"
  - "[[GitHub - Actions]]"
  - "[[API - Pagination Patterns]]"
sources:
  - https://cli.github.com/manual/
  - https://docs.github.com/en/github-cli
updated: 2026-08-14
---

# GitHub CLI (gh)

## Daily commands

```bash
gh auth login
gh repo clone owner/repo
gh repo create my-app --private --clone

gh pr create --fill --draft
gh pr list --state open --assignee @me
gh pr checkout 123
gh pr diff 123
gh pr review 123 --approve
gh pr merge 123 --squash --delete-branch
gh pr status                      # the single best "what's on my plate" command

gh issue create --title "Bug" --label bug
gh issue list --search "is:open label:bug"

gh run list --workflow ci.yml
gh run watch                      # live-tail the current run
gh run rerun --failed

gh release create v1.0.0 --generate-notes ./dist/*
gh browse                         # open current repo/file in a browser
```

## `gh api` — the escape hatch

Handles auth, pagination, and the version header for you:

```bash
gh api /user
gh api --paginate /repos/{owner}/{repo}/pulls
gh api graphql -f query='{ viewer { login } }'
gh api -X PATCH /repos/o/r --field has_wiki=false
gh api /repos/{owner}/{repo}/pulls --jq '.[] | {n: .number, t: .title}'
```

`{owner}` and `{repo}` are auto-filled from the current directory. Combined with
`--jq`, this is the fastest way to prototype an API query before writing code.

## Aliases and extensions

```bash
gh alias set prs 'pr list --assignee @me --state open'
gh extension install dlvhdr/gh-dash    # a TUI PR/issue dashboard
gh extension list
```

`gh-dash` is worth studying if you're building a dashboard — it's a working
reference implementation of the same problem.

## For scripting

`gh auth token` prints the current token, which is a convenient way to bootstrap
a local dev environment without minting a separate PAT.

---

## Related

- [[GitHub - REST API]]
- [[GitHub - Pull Requests]]
- [[GitHub - Actions]]
- [[API - Pagination Patterns]]

## Sources

- <https://cli.github.com/manual/>
- <https://docs.github.com/en/github-cli>
