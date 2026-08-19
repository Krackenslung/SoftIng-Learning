---
title: Glossary
domain: reference
section: 25
category: reference
difficulty: beginner
danger: none
tags:
  - reference
  - glossary
commands: []
related:
  - "[[Git - Mental Model]]"
  - "[[Git - Internals]]"
  - "[[Web-APIs]]"
  - "[[Android]]"
sources:
  - https://git-scm.com/docs/gitglossary
  - https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain
updated: 2026-08-14
---

# Glossary


**Ancestor** — a commit reachable by following parent links backwards.

**App Link** — an `https` deep link a single app owns, proven by a signed
association file on the domain. Unlike a custom scheme, no other app can claim
it, which is why it is the right OAuth redirect target.

**Backoff** — waiting progressively longer between retries. Exponential backoff
doubles the delay each attempt; **jitter** randomises it so many clients do not
retry in unison.

**Bare repository** — a repo with no working directory, containing only the
`.git` contents. What lives on a server.

**Bearer token** — a credential where possession alone grants access, sent as
`Authorization: Bearer <token>`. Anyone who intercepts it can use it.

**Blob** — a Git object storing file contents. No filename, no permissions.

**Branch** — a movable pointer to a commit. Physically, a file containing a hash.

**Checkout** — updating the working directory to match a commit or ref.

**Cherry-pick** — applying one commit's changes onto another branch as a new
commit.

**Clone** — a full local copy of a repository, including all history.

**Commit** — a snapshot of the tree plus metadata and parent pointer(s).

**Commit-ish** — anything resolvable to a commit: hash, branch, tag, `HEAD~2`.

**Composable** — a function that emits UI in Jetpack Compose. Called again when
its inputs change; must contain no side effects.

**Conditional request** — a request carrying a validator (`If-None-Match`,
`If-Modified-Since`) so the server can answer `304 Not Modified` instead of
resending the body.

**Confidential client** — an OAuth client that can keep a secret, because it
runs on a server you control. The opposite of a public client.

**Coroutine** — work that can suspend without blocking a thread. Belongs to a
scope, so cancelling the scope cancels the work.

**Cursor** — an opaque token marking a position in a result set, used for
pagination that stays correct while the collection is being written to.

**DAG** — directed acyclic graph. The shape of Git history.

**DAO** — data access object. In Room, the annotated interface whose methods
map to SQL queries.

**Deep link** — a URI that opens a specific destination inside an app, skipping
the screens that would normally precede it.

**Detached HEAD** — HEAD points at a commit instead of a branch.

**Device authorization flow** — an OAuth grant for input-constrained clients:
the device shows a code, the user approves it on another device (RFC 8628).

**Doze** — the state an idle Android device enters with the screen off, batching
deferred work into widening maintenance windows and suspending network access
between them.

**ETag** — an opaque version identifier for a representation of a resource.
Strong means byte-identical; weak (`W/` prefix) means semantically equivalent.

**Fast-forward** — a merge that only moves a pointer, because the target is an
ancestor.

**Fetch** — download objects and update remote-tracking refs. Changes nothing
local.

**Flow** — a cold stream of values in Kotlin: nothing runs until something
collects it, and each collector gets its own execution.

**Foreground service** — a service with a persistent notification, exempt from
most background limits. For work the user started and can see, never for
polling.

**Fork** — a server-side copy of a repository under a different owner. Not a Git
concept; a forge concept.

**GraphQL** — a query language where the client specifies the response shape.
One endpoint, no HTTP caching, cost metered by query complexity.

**HEAD** — pointer to the current branch (or commit, if detached).

**Hilt** — the dependency-injection framework Google documents for Android,
built on Dagger, with hooks for ViewModels and Workers.

**HMAC** — a keyed hash proving a message came from a holder of the shared
secret and was not modified. How webhook deliveries are verified.

**Hunk** — a contiguous block of changed lines in a diff.

**Idempotent** — an operation that leaves the same state whether applied once or
N times. Determines whether a client may safely retry.

**Index** — the staging area. The proposed next commit. Stored in `.git/index`.

**JWKS** — JSON Web Key Set. The public keys an issuer publishes so verifiers
can check signatures, selected by the token's `kid`.

**JWT** — JSON Web Token. Base64url-encoded claims plus a signature. Readable
by anyone holding it — signed, not encrypted.

**LFS** — Large File Storage. Extension replacing big files with pointers.

**Merge base** — the best common ancestor of two commits.

**Merge commit** — a commit with two or more parents.

**Monorepo** — one repository holding many projects.

**Nonce** — a number used once, included in a request and echoed back to prove
a response belongs to that specific exchange.

**OAuth 2.0** — a delegation protocol: it authorises an application to act on a
user's behalf. It does not authenticate the user.

**Object** — blob, tree, commit, or tag. Content-addressed and immutable.

**Offset pagination** — paging by position (`?page=3`). Simple, but items shift
between pages when the collection changes underneath you.

**OIDC** — OpenID Connect. An identity layer over OAuth 2.0 adding an
`id_token`; also the basis of keyless CI authentication to cloud providers.

**ort** — the default merge strategy since Git 2.34.

**Packfile** — many objects delta-compressed into one file.

**Pickaxe** — `git log -S` / `-G`. Searching history by diff content.

**PKCE** — Proof Key for Code Exchange. A secret the client proves it knew at
the start of an OAuth flow, so a stolen authorization code is unusable.

**Porcelain** — user-facing commands (`add`, `commit`). Contrast: **plumbing**,
the low-level scriptable commands (`cat-file`, `rev-parse`).

**Public client** — an OAuth client that cannot keep a secret: mobile, SPA,
desktop, CLI. Anything shipped to a user can be decompiled, so PKCE is
mandatory and no client secret may be embedded.

**Pull** — fetch plus merge or rebase.

**Push** — upload local commits to a remote.

**Rate limit** — a server-imposed cap on request volume, reported in
`x-ratelimit-*` headers and enforced with `429 Too Many Requests`.

**Rebase** — replay commits onto a new base, creating new commits.

**Recomposition** — Compose calling a composable again because its inputs
changed. Can happen many times per frame, in any order, and be abandoned.

**Ref** — a named pointer to a commit. Under `refs/`.

**Refspec** — `<src>:<dst>` mapping controlling fetch and push.

**Reflog** — local log of every change to HEAD and branch tips. Your safety net.

**Reftable** — binary ref storage format; Git 3.0 default for new repos.

**Remote** — a named URL for another repository. Conventionally `origin`.

**Remote-tracking branch** — a local read-only cache of a remote branch's
position (`origin/main`).

**rerere** — "reuse recorded resolution". Replays previous conflict resolutions.

**Revert** — a new commit that undoes a previous one. History-safe.

**Scope** — what an OAuth client requested. Effective permission is the
intersection of the scope, the user's grant and the user's own rights.

**SHA / hash** — content-addressed object ID. SHA-1 today, SHA-256 going forward.

**Sparse-checkout** — populating only part of the tree in the working directory.

**Squash** — combining several commits into one.

**Staging** — adding changes to the index for the next commit.

**Stash** — temporary storage for uncommitted changes.

**StateFlow** — a hot Flow that always holds a current value and replays it to
new collectors. The usual carrier for screen state; wrong for one-time events.

**Submodule** — a pointer to a specific commit in another repository.

**Subtree** — another repo's content merged into a subdirectory.

**Tag** — a ref marking a specific commit. Annotated tags are full objects.

**Token bucket** — a rate-limiting algorithm holding N tokens that refill at a
fixed rate, allowing bursts up to N and a sustained rate of the refill.

**Tracking branch** — a local branch configured with an upstream.

**Tree** — a Git object representing a directory.

**Upstream** — the remote branch a local branch is configured to track.

**Webhook** — an HTTP callback the provider sends when an event occurs.
At-least-once, unordered, and unauthenticated until you verify the signature.

**Working directory / working tree** — the checked-out files you actually edit.

**Worktree** — an additional checkout attached to the same repository.

**YAML** — an indentation-sensitive config format with implicit typing. Under
1.1 semantics `no` becomes `false` and `12:30` becomes `750`, so quote strings.

---

## Related

- [[Git - Mental Model]]
- [[Git - Internals]]
- [[Web-APIs]]
- [[Android]]

## Sources

- <https://git-scm.com/docs/gitglossary>
- <https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain>
