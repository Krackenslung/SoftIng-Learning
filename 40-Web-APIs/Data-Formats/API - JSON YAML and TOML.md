---
title: JSON YAML and TOML
domain: api
section: "53"
category: data-formats
difficulty: beginner
danger: medium
tags:
  - api/formats
  - api/yaml
commands: []endpoints: []

dashboard_relevant: true
mobile_relevant: false
related:
  - "[[API - Headers]]"
  - "[[API - REST vs GraphQL]]"
  - "[[GitHub - Actions]]"
  - "[[GitHub - Actions Advanced]]"
sources:
  - https://datatracker.ietf.org/doc/html/rfc8259
  - https://yaml.org/spec/1.2.2/
  - https://toml.io/en/v1.0.0
updated: 2026-08-18
---

# JSON YAML and TOML

Three text formats for structured data, with three different jobs: JSON is for
machines talking to machines, YAML is for humans writing configuration, TOML is
for humans writing *flat* configuration. They are not interchangeable, and YAML
in particular carries a set of implicit-typing behaviours that silently change
your values — which matters here because YAML is what every GitHub Actions
workflow in this vault is written in.

## Choosing

| | JSON | YAML | TOML |
|---|---|---|---|
| Primary use | Wire format | Config, CI pipelines | Config, manifests |
| Comments | **No** | Yes (`#`) | Yes (`#`) |
| Whitespace significant | No | **Yes** | No |
| Deep nesting | Fine | Fine | Awkward |
| Implicit typing surprises | No | **Many** | No |
| Trailing commas | No | N/A | Allowed in arrays |
| Multi-line strings | No (escapes only) | Yes (`\|`, `>`) | Yes (`"""`) |
| Dates as a type | No | Yes | **Yes, first class** |
| Spec stability | RFC 8259, frozen | 1.1 vs 1.2 split in practice | 1.0.0, stable |

Rules of thumb: **JSON on the wire** — it is what APIs speak and it has no
ambiguity. **YAML when a human edits deeply nested config** and comments matter.
**TOML for shallow config** (`pyproject.toml`, `Cargo.toml`) where the flat
`[section]` layout stays readable and there are no whitespace traps.

## JSON

```json
{ "number": 42, "ok": true, "nested": { "list": [1, 2, 3] }, "nothing": null }
```

Six types: string, number, boolean, null, object, array. No comments, no dates,
no integers-versus-floats distinction — `1` and `1.0` are both "number", which
is why large integers such as snowflake IDs are transmitted as strings.

⚠️ JSON numbers are IEEE 754 doubles in most parsers, so integers above 2^53
lose precision silently. A 64-bit ID becomes a *different* ID with no error.
Keep them as strings.

JSON is a subset of YAML 1.2, so any YAML parser reads JSON — the reverse is
never true.

## TOML

```toml
title = "My project"
updated = 2026-08-18T10:00:00Z    # a real date type, not a string

[owner]
name = "octocat"
tags = ["cli", "api"]

[[bin]]                            # array of tables
name = "tool"
```

Unambiguous, comment-friendly, dates built in. The cost is nesting: three levels
deep becomes `[a.b.c]` header soup, which is why TOML is the right answer for
project manifests and the wrong one for CI pipelines.

## YAML, and its footguns

```yaml
name: CI
on:                       # see below - this key is a trap in YAML 1.1
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          npm ci
          npm test
```

YAML's power is implicit typing — you write `true` and get a boolean. Its
problem is the same feature applied to things you did not mean as booleans. The
split matters: **YAML 1.1 had a much broader set of implicit conversions than
1.2**, and many widely used parsers still default to 1.1 semantics.

| You write | 1.1 parsers give you | You wanted |
|---|---|---|
| `no`, `NO`, `off`, `n` | `false` | the string `"no"` |
| `yes`, `on`, `y` | `true` | the string `"yes"` |
| `12:30` | `750` (sexagesimal) | the string `"12:30"` |
| `0755` | `493` (octal) | the string `"0755"` |
| `1.10` | `1.1` (float) | the version `"1.10"` |
| `2026-08-18` | a date object | the string, sometimes |
| `Null`, `~`, empty | `null` | possibly an empty string |

### The Norway problem

The canonical case: a list of country codes.

```yaml
countries: [GB, IE, NO, SE]     # NO becomes false
```

Norway's code is `NO`, which YAML 1.1 reads as the boolean `false`. The list
silently becomes `["GB", "IE", false, "SE"]`. Nothing errors — the value simply
changes type, and the failure appears somewhere far away.

The fix is always the same: **quote anything you mean as a string.**

```yaml
countries: ["GB", "IE", "NO", "SE"]
```

### `on:` in a workflow file

This one is live in every Actions workflow. In YAML 1.1, the bare key `on` is a
boolean, so a strict 1.1 parser reads `on:` as the key `true:`. GitHub's own
parser handles it, but linters, editors and scripts that read workflows with a
1.1 library will not — which is why some tooling reports a workflow as having no
triggers. Quoting the key (`"on":`) is valid YAML and removes the ambiguity.

## ⚠️ Gotchas

- ⚠️ **Unquoted YAML scalars change type silently.** The Norway problem and its
  relatives never raise an error; the value is simply wrong downstream. Quote
  strings that could be read as booleans, numbers, dates or times — country
  codes, versions, times, leading-zero identifiers, git SHAs that happen to be
  all digits.
- ⚠️ **Tabs are forbidden for YAML indentation.** A tab pasted from another
  editor produces a parse error whose message points at the wrong line. Configure
  the editor to expand tabs in `.yml`.
- ⚠️ **Indentation is the structure.** One wrong space silently reparents a key
  into the block above rather than failing — a step lands under the wrong job
  and runs at the wrong time. Diffs of pure whitespace are real changes here.
- ⚠️ **JSON integers over 2^53 lose precision.** Serialise large IDs as strings
  on both sides.
- **`|` keeps newlines, `>` folds them into spaces.** Getting this backwards in
  a `run:` block turns a multi-line script into one unrunnable line.
- **YAML anchors and merge keys (`&`, `*`, `<<`) are not supported by GitHub
  Actions**, even though they are valid YAML. Use reusable workflows or
  composite actions instead — see [[GitHub - Actions Advanced]].
- **YAML has no canonical form.** Round-tripping through a parser reorders keys
  and drops comments, so generated YAML makes noisy diffs. Edit by hand or own
  the generator.
- **`.yml` and `.yaml` are the same format.** GitHub accepts both for workflows;
  pick one per repository for consistency.

---

## Related

- [[API - Headers]]
- [[API - REST vs GraphQL]]
- [[GitHub - Actions]]
- [[GitHub - Actions Advanced]]

## Sources

- <https://datatracker.ietf.org/doc/html/rfc8259>
- <https://yaml.org/spec/1.2.2/>
- <https://toml.io/en/v1.0.0>
