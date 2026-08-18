# SoftIng Learning

An [Obsidian](https://obsidian.md) vault documenting **Git**, **GitHub** and the
**web API fundamentals** that sit underneath them. 83 notes, heavily
cross-linked, written to be read in any order and to answer a question in one
hop rather than five.

It doubles as the reference material for a GitHub developer dashboard being
built as a native Android client.

## Opening it

1. Clone the repository.
2. In Obsidian: **Open folder as vault** → pick the cloned directory.
3. Enable the **Dataview** community plugin. The hub notes (`Git.md`,
   `GitHub.md`, `Web-APIs.md`, `Home.md`) build their index tables with it, and
   without it those sections render as empty code blocks. Everything else is
   plain Markdown and reads fine in any editor.

Start at `00-Meta/Home.md`.

## What is in it

| Folder | Notes | Covers |
|---|---|---|
| `00-Meta/` | 5 | Home, vault conventions, note templates |
| `10-Git/` | 22 | Git itself: mental model, daily loop, history rewriting, collaboration, investigation, internals |
| `20-GitHub/` | 26 | The platform: repos, issues, PRs, Actions, the REST and GraphQL APIs, webhooks, security |
| `30-Bridge/` | 7 | Where Git and GitHub concepts collide and get confused |
| `40-Web-APIs/` | 16 | HTTP and API fundamentals: status codes, headers, ETags, pagination, idempotency, OAuth, JWT, HMAC, OIDC, rate limiting, data formats |
| `90-Reference/` | 5 | Cheat sheet, undo cookbook, troubleshooting, glossary, master source list |
| `95-Projects/` | 2 | Dashboard specifications |

Counts include each folder's hub note. Numeric prefixes exist to control
Obsidian's sort order; gaps of ten leave room to insert a domain without
renumbering.

## How the notes are written

Every note opens with a paragraph of orientation, leads with the concept before
the syntax, uses tables for anything comparative, and ends with `## Related` and
`## Sources`. A `## ⚠️ Gotchas` section carries the things that lose data or
fail silently — the ⚠️ marker is used deliberately and sparingly.

Links are bidirectional: if A links to B, B links back. Every claim cites a
primary source (git-scm.com, docs.github.com, RFCs, MDN), never a blog where a
specification exists.

## Checking the vault

```bash
python 00-Meta/scripts/validate.py
```

Reports broken wikilinks, notes missing frontmatter, unquoted wikilinks in YAML,
orphaned notes and a per-folder count. It ignores anything inside code fences or
backticks, so the documented frontmatter schema does not register as broken
links. Exits non-zero if anything is wrong.

## Contributing to your own copy

`00-Meta/Vault Structure.md` documents the frontmatter schema and naming rules.
Copy a template from `00-Meta/Templates/`, fill the frontmatter completely —
partial frontmatter breaks the hub queries — link the note from its hub, and run
the validator before committing.
