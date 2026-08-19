---
title: Home
type: hub
tags:
  - hub
updated: 2026-08-14
---

# Home

> [!info] Two domains, one bridge
> **[[Git]]** is the tool. **[[GitHub]]** is the platform built on it.
> The [[#Bridge notes|Bridge]] folder covers where they meet — and where the
> mental models diverge. **[[Web-APIs]]** covers the HTTP layer both sit on.

## Start here

| | |
|---|---|
| 🌱 **Learning Git** | [[Git]] → follow the learning path |
| 🐙 **Learning GitHub** | [[GitHub - GitHub vs Git]] first, then [[GitHub]] |
| 🚨 **Something broke** | [[Git - Undo Cookbook]] |
| 🔌 **Building an integration** | [[Web-APIs]], [[GitHub - REST API]], [[GitHub - Rate Limits]] |
| 📱 **Building the Android client** | [[Android]] → [[API - Client-Only vs Backend Architectures]] |
| 📋 **Quick lookup** | [[Git - Cheat Sheet]], [[Glossary]] |

## Bridge notes

- [[Bridge - Forks and Remotes]]
- [[Bridge - PRs vs Merge]]
- [[Bridge - Branch Protection vs Hooks]]
- [[Bridge - Tags vs Releases]]
- [[Bridge - Actions vs Git Hooks]]
- [[Bridge - Auth SSH HTTPS and Tokens]]
- [[Bridge - GitHub API Conventions]]
- [[Bridge - GitHub API on Android]]

## Projects

- [[Dev Dashboard - Data Model]]
- [[Dev Dashboard - API Map]]

## Vault

- [[Vault Structure]] — conventions, frontmatter schema, how to add a note
- [[Sources]] — master source list

---

## Recently updated

```dataview
TABLE updated, domain
FROM ""
WHERE updated
SORT updated DESC
LIMIT 10
```

## Everything, by domain

```dataview
TABLE length(rows) AS Notes
FROM ""
WHERE domain
GROUP BY domain
```

## ⚠️ High-risk topics

```dataview
LIST
FROM ""
WHERE danger = "high"
SORT file.name ASC
```
