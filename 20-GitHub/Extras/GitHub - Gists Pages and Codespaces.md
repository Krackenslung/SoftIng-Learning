---
title: Gists, Pages and Codespaces
domain: github
section: 25
category: extras
difficulty: beginner
danger: low
tags:
  - github/tools
commands: []
endpoints:
  - GET /gists
  - GET /repos/{owner}/{repo}/pages
related:
  - "[[GitHub - Actions]]"
  - "[[GitHub - Repositories]]"
sources:
  - https://docs.github.com/en/get-started/writing-on-github/editing-and-sharing-content-with-gists
  - https://docs.github.com/en/pages
  - https://docs.github.com/en/codespaces
updated: 2026-08-14
---

# Gists, Pages and Codespaces

## Gists

Small standalone snippets — each gist **is a real Git repository**:

```bash
git clone https://gist.github.com/<gist-id>.git
gh gist create file.py --public
gh gist list
```

- "Secret" gists are unlisted, **not private** — anyone with the URL can read
  them. Never put credentials in one.
- Support comments, forks, and revision history
- Embeddable via a `<script>` tag

## Pages

Static hosting from a repo. Sources: a branch (`/` or `/docs`) or a GitHub
Actions workflow.

```yaml
permissions:
  pages: write
  id-token: write
steps:
  - uses: actions/configure-pages@v5
  - uses: actions/upload-pages-artifact@v3
    with: { path: ./dist }
  - uses: actions/deploy-pages@v4
```

- Jekyll is built in; add `.nojekyll` to bypass it for SPA/static builds
- Custom domains via `CNAME` + DNS, with automatic HTTPS
- Private Pages require Enterprise

## Codespaces

Cloud dev containers configured by `.devcontainer/devcontainer.json`:

```json
{
  "image": "mcr.microsoft.com/devcontainers/javascript-node:22",
  "features": { "ghcr.io/devcontainers/features/github-cli:1": {} },
  "postCreateCommand": "npm ci",
  "forwardPorts": [3000],
  "customizations": { "vscode": { "extensions": ["dbaeumer.vscode-eslint"] } }
}
```

- Prebuilds cut startup from minutes to seconds
- `GITHUB_TOKEN` is available in the environment
- Billed per core-hour + storage; **stop them** — idle timeout defaults to 30 min
- The same `devcontainer.json` works locally in VS Code, so it's worth adding
  even if you never use Codespaces

---

## Related

- [[GitHub - Actions]]
- [[GitHub - Repositories]]

## Sources

- <https://docs.github.com/en/get-started/writing-on-github/editing-and-sharing-content-with-gists>
- <https://docs.github.com/en/pages>
- <https://docs.github.com/en/codespaces>
