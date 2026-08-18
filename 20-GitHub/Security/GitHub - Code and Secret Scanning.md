---
title: Code and Secret Scanning
domain: github
section: 21
category: security
difficulty: intermediate
danger: high
tags:
  - github/security
commands: []
endpoints:
  - GET /repos/{owner}/{repo}/code-scanning/alerts
  - GET /repos/{owner}/{repo}/secret-scanning/alerts
  - GET /repos/{owner}/{repo}/dependabot/alerts
dashboard_relevant: true
related:
  - "[[GitHub - Advisories and Supply Chain]]"
  - "[[GitHub - Actions]]"
  - "[[Git - Undo Cookbook]]"
sources:
  - https://docs.github.com/en/code-security
  - https://docs.github.com/en/code-security/code-scanning
  - https://docs.github.com/en/code-security/secret-scanning
updated: 2026-08-14
---

# Code and Secret Scanning

Three distinct alert systems, three separate APIs.

## Dependabot alerts

Known CVEs in your dependency graph, matched against the GitHub Advisory
Database. Configure automated fix PRs in `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: npm
    directory: "/"
    schedule: { interval: weekly }
    open-pull-requests-limit: 5
    groups:
      minor-and-patch:
        update-types: [minor, patch]
```

Grouping is essential — ungrouped Dependabot floods the PR list and trains people
to ignore it.

## Code scanning (CodeQL)

Static analysis on a schedule and on PRs. Results are SARIF, so third-party
scanners can upload too.

```yaml
- uses: github/codeql-action/init@v3
  with: { languages: javascript-typescript }
- uses: github/codeql-action/analyze@v3
```

Alerts carry `state` (`open`/`dismissed`/`fixed`), `rule.severity`, and
`most_recent_instance.location`.

## Secret scanning

Detects committed credentials by pattern, across **all history**, and notifies
the issuing provider so they can revoke.

- **Push protection** blocks the push before the secret ever lands — enable it;
  it is the only one of the three that prevents rather than reports
- Custom patterns available on Enterprise
- Alerts have `state` and a `resolution` reason

⚠️ A secret-scanning alert means **rotate first**. Removing it from history is
secondary and does not undo exposure — see [[Git - Undo Cookbook]].

## Dashboard note

All three alert APIs need explicit fine-grained permissions
(**Code scanning alerts**, **Secret scanning alerts**, **Dependabot alerts** —
each separate, all read). Missing one yields a 403 on that endpoint only, so
degrade per-widget rather than failing the whole security panel.

---

## Related

- [[GitHub - Advisories and Supply Chain]]
- [[GitHub - Actions]]
- [[Git - Undo Cookbook]]

## Sources

- <https://docs.github.com/en/code-security>
- <https://docs.github.com/en/code-security/code-scanning>
- <https://docs.github.com/en/code-security/secret-scanning>
