# Claude Code prompt — build `40-Web-APIs`

> Paste everything below the line into Claude Code, from inside your vault
> directory. Replace nothing except the checked assumptions in `<context>` if
> they're wrong.

---

<context>
I'm working in an Obsidian vault documenting Git and GitHub. It currently has 66
notes across these top-level folders:

```
00-Meta/          Home, Vault Structure, Templates/
10-Git/           21 notes + Git.md hub
20-GitHub/        25 notes + GitHub.md hub
30-Bridge/        6 notes — where Git and GitHub concepts meet
90-Reference/     Cookbook, troubleshooting, cheat sheet, glossary, sources
95-Projects/      Dev dashboard specs
```

The vault feeds two purposes: personal reference, and structured input for a
GitHub developer dashboard I'm building.

Before writing anything, read these files to learn the conventions and match the
existing voice:
- `00-Meta/Vault Structure.md` — the full frontmatter schema and naming rules
- `20-GitHub/API/GitHub - REST API.md` — the density and tone I want
- `30-Bridge/Bridge - Auth SSH HTTPS and Tokens.md` — the Bridge note format
- `10-Git/Git.md` — hub note structure, including the Dataview queries
</context>

<task>
Create a new top-level folder `40-Web-APIs/` containing 13 notes plus a hub, and
one new Bridge note. These cover the HTTP and API fundamentals that the existing
GitHub notes currently assume without explaining.

The gap I'm closing: `GitHub - REST API` says a 304 costs no rate limit quota but
never explains conditional requests. `GitHub - Webhooks` ships HMAC verification
code without explaining timing attacks. `GitHub - Bots and Apps` walks through a
JWT flow without defining JWT. Six notes reference ETags, five reference
pagination, four reference OIDC — none of it is defined anywhere in the vault.
</task>

<files_to_create>
```
40-Web-APIs/
├── Web-APIs.md                                  ★ hub
├── Fundamentals/
│   ├── API - HTTP Methods and Status Codes.md
│   ├── API - Headers.md
│   ├── API - Caching and ETags.md
│   ├── API - Pagination Patterns.md
│   └── API - Idempotency and Retries.md
├── Auth/
│   ├── API - OAuth 2.0 Flows.md
│   ├── API - JWT.md
│   ├── API - HMAC Signatures.md
│   └── API - OIDC and Federated Identity.md
├── Patterns/
│   ├── API - REST vs GraphQL.md
│   ├── API - Webhooks vs Polling.md
│   └── API - Rate Limiting Strategies.md
└── Data-Formats/
    └── API - JSON YAML and TOML.md

30-Bridge/
└── Bridge - GitHub API Conventions.md
```
</files_to_create>

<frontmatter_schema>
Every note gets complete frontmatter. Partial frontmatter breaks the hub
Dataview queries.

```yaml
---
title: Caching and ETags          # no domain prefix
domain: api                       # new value — git | github | bridge | reference | api
section: "43"                     # see numbering below
category: fundamentals            # fundamentals | auth | patterns | data-formats
difficulty: intermediate          # beginner | intermediate | advanced
danger: none                      # none | low | medium | high
tags:
  - api/http
  - api/caching
commands: []                      # CLI commands demonstrated, if any
dashboard_relevant: true          # true if it informs the dev dashboard build
related:
  - "[[GitHub - REST API]]"       # MUST be quoted — unquoted breaks YAML
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/ETag
updated: 2026-08-14
---
```

Section numbers, for sort order:
- `41`–`45` Fundamentals (in the order listed above)
- `46`–`49` Auth
- `50`–`52` Patterns
- `53` Data-Formats
- Bridge note: `B7`
</frontmatter_schema>

<content_requirements>
For each note:

1. **Open with one paragraph** of orientation — what this is, why it matters. No
   heading above it.
2. **Lead with the concept, not the syntax.** Explain the mechanism before
   showing code.
3. **Tables for anything comparative.** Status code meanings, OAuth grant types,
   pagination trade-offs, format comparisons.
4. **Code blocks always language-tagged.** Prefer JS/TS for client examples and
   raw HTTP for wire format.
5. **A `## ⚠️ Gotchas` section** where one is warranted. Mark data-loss or
   silent-failure risks with ⚠️. This is a load-bearing convention in the vault.
6. **Close with `## Related` then `## Sources`**, matching existing notes.
7. **Wrap prose at ~80 characters.** The vault is version-controlled and this
   keeps diffs readable.
8. **Cite primary sources**: MDN, RFCs (rfc-editor.org or datatracker.ietf.org),
   the OAuth 2.0 and OIDC specs, graphql.org, jwt.io for JWT structure. Blog
   posts only where no primary source exists.

Specific content notes:

- **Caching and ETags** — strong vs weak validators, `If-None-Match` vs
  `If-Modified-Since`, `Cache-Control` directives, why a 304 is cheap.
- **Pagination Patterns** — offset/limit vs cursor vs `Link` header. Cover the
  offset-drift problem (items shifting between pages during writes).
- **Idempotency and Retries** — which HTTP methods are idempotent by spec,
  idempotency keys, exponential backoff **with jitter**, retry budgets, and why
  retrying non-idempotent writes is dangerous.
- **OAuth 2.0 Flows** — authorization code + PKCE as the modern default; mark
  implicit and password grants as deprecated. Explain scopes vs permissions.
- **JWT** — header/payload/signature structure, signing vs encryption, the
  `alg: none` vulnerability, why you must validate `exp`, `iss`, `aud`.
- **HMAC Signatures** — why raw bytes must be hashed before parsing, why
  constant-time comparison is required, replay protection via timestamps.
- **Rate Limiting Strategies** — token bucket vs leaky bucket vs sliding window;
  `Retry-After`; client-side vs server-side perspectives.
- **JSON YAML and TOML** — when each fits. Include YAML's real footguns: the
  Norway problem (`no` → false), sexagesimal numbers, tabs forbidden,
  significant whitespace. This one matters because YAML appears in 10 existing
  notes.

**`Bridge - GitHub API Conventions`** follows the existing Bridge format —
opens with the blockquote `> **The general pattern is X. GitHub does Y.**` —
and covers where GitHub deviates from generic REST/GraphQL:
- GraphQL errors return HTTP 200 with an `errors` array
- 404 instead of 403 for unauthorized private resources
- Search API has a separate rate-limit bucket and a 1,000-result ceiling
- GraphQL bills by node points, not request count
- `User-Agent` header is mandatory
- Date-based API versioning via `X-GitHub-Api-Version`
</content_requirements>

<linking_requirements>
Links are the point of the vault. Bidirectional, or it doesn't count.

1. Every new note needs **at least 3** `related` links, mixing new-folder notes
   and existing GitHub notes.
2. **Add the reverse link in the existing note's `related` frontmatter.** At
   minimum:
   - `GitHub - REST API` → Caching and ETags, Pagination Patterns, Idempotency
   - `GitHub - GraphQL API` → REST vs GraphQL
   - `GitHub - Webhooks` → HMAC Signatures, Webhooks vs Polling, Idempotency
   - `GitHub - Rate Limits` → Rate Limiting Strategies
   - `GitHub - Authentication` → OAuth 2.0 Flows, JWT
   - `GitHub - Bots and Apps` → JWT, OAuth 2.0 Flows
   - `GitHub - Actions Advanced` → OIDC and Federated Identity
   - `Bridge - Auth SSH HTTPS and Tokens` → OAuth 2.0 Flows, JWT
   - `GitHub - Actions` → JSON YAML and TOML
3. Add `[[Web-APIs]]` to the Projects/hub sections of `00-Meta/Home.md`, and add
   `[[Bridge - GitHub API Conventions]]` to the Bridge lists in `Home.md`,
   `10-Git/Git.md` and `20-GitHub/GitHub.md`.
4. `Web-APIs.md` hub mirrors the structure of `20-GitHub/GitHub.md`: a short
   orientation paragraph, grouped link lists by category, then Dataview blocks:

   ````
   ```dataview
   TABLE category AS Category, difficulty AS Level
   FROM "40-Web-APIs"
   WHERE type != "hub"
   SORT section ASC
   ```
   ````

   Plus a second query filtering `WHERE dashboard_relevant = true`.
5. Append a `## Primary — Web standards` table to `90-Reference/Sources.md` with
   the MDN and RFC links used.
6. Add the new API terms to `90-Reference/Glossary.md`, alphabetically, matching
   the existing `**Term** — definition.` format.
</linking_requirements>

<constraints>
- **Do not modify the body content of existing notes.** Only add entries to their
  `related` frontmatter arrays and to the specific link lists named above.
- Do not renumber existing folders or rename existing files.
- Do not add community-plugin syntax beyond Dataview — the vault only assumes
  Dataview.
- GFM alerts (`> [!NOTE]` uppercase) do **not** render in Obsidian. Use lowercase
  Obsidian callouts (`> [!tip]`, `> [!warning]`) or plain blockquotes.
- No em-dashes inside YAML values without quoting the whole value.
</constraints>

<workflow>
Work in phases and stop for my review between each. Do not one-shot all 15 files.

**Phase 1 — Plan.** Read the four reference files listed in `<context>`. Then
show me: the exact file list with each note's `section`, `category`,
`difficulty`, `danger`, and its 3+ `related` links. Confirm the reverse-link
edits you'll make to existing notes. Wait for my approval.

**Phase 2 — Fundamentals + hub.** Write the 5 Fundamentals notes and
`Web-APIs.md`. Stop.

**Phase 3 — Auth.** Write the 4 Auth notes. Stop.

**Phase 4 — Patterns + Data-Formats + Bridge.** Write the remaining 5 notes.
Stop.

**Phase 5 — Wire it up.** Apply all reverse links, hub-list additions,
`Sources.md` and `Glossary.md` updates.

**Phase 6 — Validate.** Write `00-Meta/scripts/validate.py` that walks the vault
and reports:
- broken wikilinks (resolve `[[Target]]` and `[[Target|alias]]` against note
  filenames; **ignore anything inside fenced code blocks or inline backticks**,
  or you'll get false positives from the schema documentation)
- notes missing frontmatter, or with unquoted wikilinks in YAML
- orphan notes not linked from anywhere
- a per-folder note count

Run it. Fix everything it reports. Show me the final clean output.
</workflow>

<success_criteria>
- 15 new files created, 0 broken links, 0 orphans
- Every new note has complete frontmatter and at least 3 bidirectional links
- Every note cites at least 2 primary sources
- `validate.py` exits clean and is committed for reuse
- The 6 notes that referenced ETags and the 5 that referenced pagination now
  link to real definitions
</success_criteria>
