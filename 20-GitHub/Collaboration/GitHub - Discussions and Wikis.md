---
title: Discussions and Wikis
domain: github
section: 11
category: collaboration
difficulty: beginner
danger: none
tags:
  - github/community
commands: []
endpoints:
  - GraphQL: repository.discussions
related:
  - "[[GitHub - Issues]]"
  - "[[GitHub - GraphQL API]]"
sources:
  - https://docs.github.com/en/discussions
  - https://docs.github.com/en/communities/documenting-your-project-with-wikis
updated: 2026-08-14
---

# Discussions and Wikis

## Discussions

Threaded forum attached to a repo or org. Unlike issues, discussions are not
work items — no assignees, no milestones, no closing as "done".

- **Categories** with formats: Announcement (maintainers post only), Q&A
  (answers can be marked accepted), Open-ended, Poll
- Comments support **nested replies** (issues do not)
- Upvotes
- A discussion can be **converted to an issue** when it becomes actionable
- **GraphQL only** — no REST coverage

Good default: Discussions for questions and ideas, Issues for tracked work. It
keeps the issue tracker an accurate backlog.

## Wikis

A separate Git repository at `<repo>.wiki.git`. You can clone and push to it:

```bash
git clone https://github.com/owner/repo.wiki.git
```

- No pull requests, no review, no branch protection
- Not searchable in code search
- No API

Because of those limits, most projects are better served by a `docs/` folder in
the main repo, which gets review, history, and [[GitHub - Actions]] publishing to
Pages. Reach for a wiki only when you want low-friction editing by
non-contributors.

---

## Related

- [[GitHub - Issues]]
- [[GitHub - GraphQL API]]

## Sources

- <https://docs.github.com/en/discussions>
- <https://docs.github.com/en/communities/documenting-your-project-with-wikis>
