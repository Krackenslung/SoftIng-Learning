---
title: Advisories and Supply Chain
domain: github
section: 22
category: security
difficulty: advanced
danger: medium
tags:
  - github/security
  - github/supply-chain
commands: []
endpoints:
  - GET /advisories
  - GET /repos/{owner}/{repo}/dependency-graph/sbom
related:
  - "[[GitHub - Code and Secret Scanning]]"
  - "[[GitHub - Releases and Packages]]"
  - "[[API - OIDC and Federated Identity]]"
sources:
  - https://docs.github.com/en/code-security/security-advisories
  - https://docs.github.com/en/code-security/supply-chain-security
  - https://slsa.dev/
updated: 2026-08-14
---

# Advisories and Supply Chain

## Repository security advisories

Private drafts for coordinated disclosure. The workflow that responsible
maintainers use:

1. Draft an advisory privately
2. Open a **temporary private fork** to develop the fix out of public view
3. Request a CVE through GitHub (a CNA)
4. Merge and publish simultaneously
5. Publication pushes the advisory to the Global Advisory Database, which
   triggers Dependabot alerts downstream

`SECURITY.md` in the repo root surfaces your reporting policy and enables the
private vulnerability reporting button.

## Dependency graph and SBOM

- Parsed from manifest/lock files
- Exportable as **SPDX SBOM** via API or UI
- Submission API lets you push dependencies discovered at build time for
  ecosystems GitHub can't parse statically

## Artifact attestation

```yaml
permissions:
  id-token: write
  attestations: write
steps:
  - uses: actions/attest-build-provenance@v2
    with: { subject-path: dist/* }
```

Produces signed, verifiable provenance (SLSA-aligned) binding an artifact to the
workflow, commit, and repo that built it. Verify with:

```bash
gh attestation verify ./dist/app --owner my-org
```

## Hardening checklist

- Pin third-party actions to a **full commit SHA**, not a tag — tags are mutable
- Set `permissions:` explicitly at workflow level (default to `read`)
- Never use `pull_request_target` with a checkout of PR head
- Prefer OIDC over stored cloud credentials
- Require signed commits on release branches
- Enable push protection for secrets

---

## Related

- [[GitHub - Code and Secret Scanning]]
- [[GitHub - Releases and Packages]]
- [[API - OIDC and Federated Identity]]

## Sources

- <https://docs.github.com/en/code-security/security-advisories>
- <https://docs.github.com/en/code-security/supply-chain-security>
- <https://slsa.dev/>
