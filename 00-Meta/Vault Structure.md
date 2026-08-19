---
title: Vault Structure
type: meta
tags:
  - meta
updated: 2026-08-14
---

# Vault Structure

## Folders

```
00-Meta/          Home, this note, Templates/
10-Git/           Git concepts, grouped by category
20-GitHub/        GitHub platform, grouped by area
30-Bridge/        Where Git and GitHub concepts meet
40-Web-APIs/      HTTP and API fundamentals the GitHub notes build on
60-Android/       The Android client that consumes them
90-Reference/     Lookup material — cookbook, cheat sheet, glossary
95-Projects/      Applied notes (dashboard specs)
_attachments/     Images, canvases
```

Numeric prefixes exist purely to control Obsidian's alphabetical sort order.

## Naming

Every note is prefixed with its domain:

```
Git - <Topic>.md
GitHub - <Topic>.md
Bridge - <Topic>.md
API - <Topic>.md
Android - <Topic>.md
```

This prevents collisions (`Git - Merging` vs `GitHub - Pull Requests` both cover
merging) and makes link autocomplete unambiguous.

## Frontmatter schema

| Key | Type | Values |
|---|---|---|
| `title` | string | Display title (no domain prefix) |
| `domain` | string | `git` · `github` · `bridge` · `reference` · `api` · `android` |
| `section` | string | Ordering key — `01`–`25`, `41`–`53`, `61`–`76`, `B1`–`B8` |
| `category` | string | Sub-grouping within the domain |
| `difficulty` | string | `beginner` · `intermediate` · `advanced` |
| `danger` | string | `none` · `low` · `medium` · `high` |
| `tags` | list | Nested: `git/rebase`, `github/api` |
| `commands` | list | CLI commands covered — builds a command index |
| `endpoints` | list | API endpoints covered (GitHub notes) |
| `dashboard_relevant` | bool | Flags notes feeding the dev dashboard |
| `related` | list | `"[[Wikilinks]]"` — must be quoted in YAML |
| `sources` | list | Bare URLs |
| `updated` | date | ISO date |

`danger` and `dashboard_relevant` exist to drive Dataview queries — they are the
two fields that make the vault queryable rather than just browsable.

## Adding a note

1. Copy the matching template: [[Concept]], [[Command]] or [[Hub]]
2. Fill the frontmatter completely — partial frontmatter breaks the hub queries
3. Link it from the relevant hub ([[Git]], [[GitHub]], [[Web-APIs]] or [[Android]])
4. Add at least two `related` links, and add the reverse link in those notes
5. Cite a primary source — git-scm.com or docs.github.com, not a blog

## Recommended Obsidian settings

- **Core plugins:** Templates (point to `00-Meta/Templates`), Graph view, Canvas,
  Outline, Backlinks in document
- **Community plugins:** Dataview (required for the hub queries), Advanced Tables,
  Linter
- **Files & Links:** attachments → `_attachments`, use wikilinks, new links as
  shortest path
- **Editor:** Strict line breaks *off* (content is wrapped at ~80 chars)

## Conventions

- Code blocks always tagged with a language
- ⚠️ marks anything that can lose data or silently misbehave
- Tables over prose for anything comparative
- Every note ends with `## Related` and `## Sources`
- Content wrapped at ~80 characters so diffs stay readable if this vault is
  itself version-controlled

## Versioning this vault

The vault is plain Markdown, so put it in Git:

```bash
cd vault && git init && git add . && git commit -m "Initial vault"
```

Add a `.gitignore` for `.obsidian/workspace.json` (churns constantly) while
keeping the rest of `.obsidian/` so plugin config travels with the vault.
