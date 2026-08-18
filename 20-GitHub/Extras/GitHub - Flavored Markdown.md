---
title: GitHub Flavored Markdown
domain: github
section: 24
category: extras
difficulty: beginner
danger: none
tags:
  - github/markdown
commands: []
endpoints:
  - POST /markdown
related:
  - "[[GitHub - Issues]]"
  - "[[GitHub - Repositories]]"
sources:
  - https://github.github.com/gfm/
  - https://docs.github.com/en/get-started/writing-on-github
  - https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams
updated: 2026-08-14
---

# GitHub Flavored Markdown

GFM is CommonMark plus extensions. Relevant here because your Obsidian notes and
your GitHub content will **not** render identically.

## GFM extensions

```markdown
~~strikethrough~~
- [x] task list
- [ ] unchecked

| table | header |
|-------|:------:|
| cell  | cell   |

https://example.com          ← autolinked
#123  owner/repo#123  @user  @org/team  GH-123
:sparkles: :shipit:
```

## Alerts

```markdown
> [!NOTE]
> Useful information.

> [!TIP]
> [!IMPORTANT]
> [!WARNING]
> [!CAUTION]
```

Renders as coloured callouts on GitHub. **Does not render in Obsidian** — Obsidian
uses `> [!note]` callouts with different names and casing. Keep this in mind when
moving content between the vault and a repo README.

## Diagrams

Mermaid renders natively in GitHub Markdown *and* in Obsidian — one of the few
things that works in both:

````markdown
```mermaid
graph LR
  A[Feature branch] -->|PR| B[Review]
  B -->|Approve| C[Merge]
```
````

Also supported: GeoJSON, TopoJSON, STL, and LaTeX via `$...$` / `$$...$$`.

## Collapsible sections

```html
<details>
<summary>Click to expand</summary>

Content here — needs a blank line above.

</details>
```

## Permalinks

Pasting a GitHub file URL with a line range (`#L10-L20`) into a comment embeds a
rendered code snippet. Press `y` on a file view first to get a commit-pinned
permalink — branch-based links rot.

## Rendering via API

```bash
gh api -X POST /markdown -f text='Hello #123' -f mode=gfm -f context=owner/repo
```

Use this if your dashboard needs to render issue bodies exactly as GitHub does,
including reference autolinking.

---

## Related

- [[GitHub - Issues]]
- [[GitHub - Repositories]]

## Sources

- <https://github.github.com/gfm/>
- <https://docs.github.com/en/get-started/writing-on-github>
- <https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams>
