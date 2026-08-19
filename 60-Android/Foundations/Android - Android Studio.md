---
title: Android Studio
domain: android
section: "63"
category: foundations
difficulty: beginner
danger: none
tags:
  - android/tooling
commands: []
endpoints: []
dashboard_relevant: false
mobile_relevant: true
related:
  - "[[Android - Project Structure]]"
  - "[[Android - Gradle and AGP]]"
  - "[[Git - Reset Revert Restore]]"
  - "[[GitHub - CLI]]"
sources:
  - https://developer.android.com/studio/intro
  - https://developer.android.com/studio/debug/am-network
  - https://developer.android.com/studio/profile
updated: 2026-08-18
---

# Android Studio

This is the only IDE note in the vault, and it is deliberately short. Android
Studio is a front end over Gradle, AGP and the SDK — the parts that endure are
documented in [[Android - Gradle and AGP]] and [[Android - Project Structure]].
What changes every release is menus, wizards and keyboard shortcuts, which is
exactly the material that rots in a note. So this covers only the tools that
have no command-line equivalent, and names nothing that a screenshot would be
needed to find.

Menu paths, panel names and shortcut bindings are all `<verify current>`.

## What is worth knowing

| Tool | Use it for | CLI equivalent |
|---|---|---|
| Logcat | Reading device logs, filtered by process | `adb logcat` |
| App Inspection — Network | Every request, with headers and timing | none |
| App Inspection — Database | Querying the live Room database on device | none |
| Layout Inspector | Why the UI looks wrong | none |
| Profiler | CPU, memory and energy over time | none |
| Build Analyzer | Why the build is slow | `./gradlew --scan` |

The three with **no CLI equivalent** are the reason to open the IDE at all.

## Network inspection is the one that matters here

For an API client, the Network profiler answers questions that logging cannot
without leaking secrets: which requests actually left the device, what the
server returned, and — critically for this project — **whether a request was
served from cache or from the network**.

That distinction is invisible in application logs and central to rate-limit
accounting, because OkHttp presents a cached `304` to your code as a `200`. See
[[Android - Networking]] and [[API - Caching and ETags]].

## Database inspection

Room's on-device database is otherwise a black box. App Inspection runs live
queries against the running app, which turns "is the cache actually being
written?" from a logging exercise into a lookup. See
[[Android - Offline First and Room]].

## Git in the IDE, and where to stop

The IDE is good at the reversible, inspection-heavy parts of Git: staging
individual hunks, reading blame inline, resolving conflicts in a three-pane
view, and browsing history.

Use the command line for anything destructive or history-rewriting — reset,
rebase, force-push, cherry-pick onto the wrong branch. The IDE presents these
behind confirmation dialogs that hide which of several very different operations
you are about to run, and the recovery path is `git reflog`, which has no
equivalent button. See [[Git - Reset Revert Restore]] and
[[Git - Blame Bisect Reflog]].

For anything involving GitHub itself — pull requests, reviews, workflow runs —
`gh` is faster and scriptable. See [[GitHub - CLI]].

## ⚠️ Gotchas

- ⚠️ **"Invalidate Caches and Restart" is not a fix.** It hides a real problem
  — usually a Gradle sync failure or a stale generated source — behind a slow
  full reindex. Read the actual sync error first; the CLI build prints it more
  plainly than the IDE does.
- ⚠️ **The IDE build and the CLI build are the same build.** If they disagree,
  the difference is configuration, not tooling: a different JDK, a stale daemon,
  or a variant selected in the IDE that CI never builds. Reproduce with
  `./gradlew` before believing the IDE.
- **Do not commit `.idea/` wholesale.** Some files in it are shared project
  config and some are per-developer state; the safe default is to ignore the
  directory and let each clone regenerate it.
- **The emulator is not a phone.** Doze, App Standby and background execution
  limits behave differently there, so background sync that works in the emulator
  proves very little — see [[Android - Background Limits and Doze]].
- **Screenshots age faster than prose.** This note has none on purpose. If you
  extend it, describe what a tool answers rather than where its button lives.

---

## Related

- [[Android - Project Structure]]
- [[Android - Gradle and AGP]]
- [[Git - Reset Revert Restore]]
- [[GitHub - CLI]]

## Sources

- <https://developer.android.com/studio/intro>
- <https://developer.android.com/studio/debug/am-network>
- <https://developer.android.com/studio/profile>
