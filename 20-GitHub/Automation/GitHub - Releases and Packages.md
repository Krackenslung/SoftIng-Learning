---
title: Releases and Packages
domain: github
section: 14
category: automation
difficulty: intermediate
danger: medium
tags:
  - github/releases
commands: []
endpoints:
  - GET /repos/{owner}/{repo}/releases
  - GET /repos/{owner}/{repo}/releases/latest
  - POST /repos/{owner}/{repo}/releases
dashboard_relevant: true
related:
  - "[[Bridge - Tags vs Releases]]"
  - "[[Git - Tags and Releases]]"
  - "[[GitHub - Actions]]"
sources:
  - https://docs.github.com/en/repositories/releasing-projects-on-github
  - https://docs.github.com/en/packages
  - https://docs.github.com/en/rest/releases/releases
updated: 2026-08-14
---

# Releases and Packages

## Releases

A GitHub-only object wrapping a Git tag with a name, description, assets, and
flags. See [[Bridge - Tags vs Releases]] for why they are not the same thing.

Fields: `tag_name`, `name`, `body`, `draft`, `prerelease`, `assets[]`,
`published_at`, `target_commitish`.

- Creating a release **creates the tag** if it doesn't exist
- Deleting a release does **not** delete the tag
- `/releases/latest` returns the most recent **non-draft, non-prerelease** —
  not simply the newest
- Assets are arbitrary binaries with download counts

## Auto-generated notes

```yaml
- uses: softprops/action-gh-release@v2
  with:
    generate_release_notes: true
```

Configure grouping in `.github/release.yml` by label. Combined with
[[Git - Commit Conventions]], this gets you a real changelog for free.

## Packages

Registries hosted alongside the repo: `npm`, `container` (ghcr.io), `maven`,
`nuget`, `rubygems`, `gradle`.

```bash
echo $TOKEN | docker login ghcr.io -u USERNAME --password-stdin
docker push ghcr.io/owner/image:tag
```

⚠️ Package visibility is **independent of repo visibility**. A public repo can
publish a private package and vice versa. Check both when debugging a 403.

Container images support attestations and provenance for supply-chain
verification — see [[GitHub - Advisories and Supply Chain]].

---

## Related

- [[Bridge - Tags vs Releases]]
- [[Git - Tags and Releases]]
- [[GitHub - Actions]]

## Sources

- <https://docs.github.com/en/repositories/releasing-projects-on-github>
- <https://docs.github.com/en/packages>
- <https://docs.github.com/en/rest/releases/releases>
