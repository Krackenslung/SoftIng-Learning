---
title: Navigation
domain: android
section: "70"
category: ui
difficulty: intermediate
danger: high
tags:
  - android/ui
  - android/navigation
  - android/security
commands: []
endpoints: []
dashboard_relevant: true
mobile_relevant: true
related:
  - "[[API - OAuth 2.0 Flows]]"
  - "[[Android - Jetpack Compose]]"
  - "[[Android - Keystore and Secure Storage]]"
  - "[[Bridge - GitHub API on Android]]"
sources:
  - https://developer.android.com/guide/navigation
  - https://developer.android.com/training/app-links
  - https://developer.android.com/training/app-links/verify-android-applinks
updated: 2026-08-18
---

# Navigation

Navigation is mostly bookkeeping — a back stack, some routes, arguments passed
between screens — until it becomes the security boundary of your login flow.
An OAuth authorization code comes back to the app through a **deep link**, and
whether another app can claim that link decides whether the code is yours or
theirs. That is why this note is marked high risk: everything else here is
ergonomics.

## The back stack

Navigation is a stack of destinations. Pushing adds; the system back gesture
pops. Two operations exist beyond that, and both are about *not* growing the
stack:

| Operation | Effect | Use for |
|---|---|---|
| `navigate(route)` | Push | Normal forward navigation |
| `popUpTo(route)` | Pop back to a destination first | Returning to a tab root |
| `launchSingleTop = true` | Do not re-add if already on top | Re-tapping a tab |
| `popUpTo(start) { inclusive }` | Clear the stack | Post-login, post-logout |

```kotlin
navController.navigate(Route.Pulls(repoId = "octocat/hello")) {
    popUpTo(Route.Login) { inclusive = true }   // login must not be reachable back
    launchSingleTop = true
}
```

After sign-in, clearing the login destination is not cosmetic: leaving it on the
stack means the back gesture returns the user to a login screen for a session
that already exists.

## Typed routes

Passing arguments as strings concatenated into a path is how a repository name
containing a slash breaks navigation. Prefer the type-safe API, where a route is
a serializable class:

```kotlin
@Serializable
data class PullsRoute(val repoId: String)

composable<PullsRoute> { backStackEntry ->
    val route: PullsRoute = backStackEntry.toRoute()
    PullsScreen(repoId = route.repoId)
}
```

Availability and stability of the type-safe navigation API are
`<verify current>`. If the string-based API is what the project uses, encode
arguments and never interpolate raw API values into a route.

Pass **identifiers**, not objects. The destination re-reads from the repository;
a serialized payload in a route is stale the moment it is created — see
[[Android - Layered Architecture]].

## Deep links and the OAuth return path

The authorization flow leaves your app, the user approves in a browser, and the
provider redirects to a URI your app claims. That redirect carries the
authorization code.

```text
app ──► Custom Tab ──► github.com/login/oauth/authorize?...&code_challenge=...
                                    │  user approves
                                    ▼
        https://dashboard.example.com/callback?code=...&state=...
                                    │  App Link, verified
                                    ▼
                              your app, back stack intact
```

Two ways to claim that redirect, and they are not equivalent:

| Mechanism | Claimed by | Can another app claim it? |
|---|---|---|
| Custom scheme (`myapp://callback`) | Any app declaring the same scheme | **Yes** |
| App Link (`https://` + verified) | Only the app matching the site's `assetlinks.json` | No |

A custom scheme is first-come, arbitrary: a malicious app registering the same
scheme can receive the redirect. App Links require a signed association file
served from the domain, which the system verifies at install time.

This is precisely the interception attack PKCE mitigates — the stolen code is
useless without the verifier — which is why PKCE is mandatory for public clients
and not merely recommended. See [[API - OAuth 2.0 Flows]]. Use both: verified
App Links *and* PKCE.

The verification requirements and manifest attributes involved are
`<verify current>`.

## Never use a WebView for OAuth

| | Custom Tabs | WebView |
|---|---|---|
| Shares browser session and 2FA state | Yes | No |
| App can read what the user types | **No** | **Yes** |
| Shows the real URL and lock icon | Yes | No |
| Accepted by providers | Yes | Often blocked |

A WebView is a browser your app controls, so the user cannot verify they are
typing their GitHub password into GitHub. RFC 8252 rules it out for native
OAuth, and providers increasingly reject it outright.

## ⚠️ Gotchas

- ⚠️ **An unverified custom-scheme redirect can be intercepted by another
  installed app**, handing it the authorization code. Use verified App Links,
  and rely on PKCE so that an intercepted code cannot be redeemed.
- ⚠️ **Never authenticate in a WebView.** It lets the app observe credentials,
  breaks 2FA and password managers, and destroys the one signal users have that
  they are on the real site.
- ⚠️ **Validate `state` when the deep link arrives.** The redirect is an
  externally triggered entry point into your app; without the `state` check an
  attacker can inject their own authorization code into the victim's session.
- ⚠️ **A deep link can open any destination, skipping the ones before it.** Do
  not assume a screen's prerequisites ran; a destination reached by link must
  handle missing session or arguments itself.
- **Do not put tokens or codes in route arguments.** They end up in the back
  stack, in saved state, and in logs. Hand them to the data layer immediately —
  see [[Android - Keystore and Secure Storage]].
- **Clear the login destination after sign-in** with `popUpTo(inclusive = true)`,
  or the back gesture returns to it.
- **Test deep links on a real device.** Emulator link verification does not
  reflect the real install-time check.

---

## Related

- [[API - OAuth 2.0 Flows]]
- [[Android - Jetpack Compose]]
- [[Android - Keystore and Secure Storage]]
- [[Bridge - GitHub API on Android]]

## Sources

- <https://developer.android.com/guide/navigation>
- <https://developer.android.com/training/app-links>
- <https://developer.android.com/training/app-links/verify-android-applinks>
