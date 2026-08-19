---
title: Project Structure
domain: android
section: "61"
category: foundations
difficulty: beginner
danger: low
tags:
  - android/project
  - android/build
commands: []
endpoints: []
dashboard_relevant: false
mobile_relevant: true
related:
  - "[[Android - Gradle and AGP]]"
  - "[[Android - Android Studio]]"
  - "[[Android - Layered Architecture]]"
  - "[[Git - Ignoring Files]]"
sources:
  - https://developer.android.com/studio/projects
  - https://developer.android.com/build/manage-manifests
  - https://developer.android.com/build/shrink-code
updated: 2026-08-18
---

# Project Structure

An Android project is a Gradle build that happens to produce an APK. Almost
every "why is this file here?" question resolves to a Gradle convention rather
than an Android one, and the two layouts that matter — the module tree and the
source set tree — are orthogonal: modules divide the app by *responsibility*,
source sets divide each module by *build variant*.

## The module tree

```text
MyDashboard/
├── settings.gradle.kts        which modules exist, and where plugins come from
├── build.gradle.kts           root: plugin declarations, nothing else
├── gradle/
│   └── libs.versions.toml     the version catalog
├── gradle.properties          JVM args, AndroidX flags, build features
└── app/
    ├── build.gradle.kts       the module that actually configures the app
    └── src/
```

The root `build.gradle.kts` should not configure anything. Its job is to declare
plugins (usually `apply false`) so that modules can apply them. Configuration
lives in the module. See [[Android - Gradle and AGP]].

A single `app` module is correct until it is not. Splitting into `:core:data`,
`:feature:pulls` and so on buys parallel compilation and enforced boundaries;
it costs indirection. Split when build times or layering violations justify it,
not on principle — see [[Android - Layered Architecture]].

## Source sets

Inside a module, `src/<sourceSet>/` mirrors the same shape:

| Source set | Applies to |
|---|---|
| `main` | Every variant |
| `debug` / `release` | That build type only |
| `test` | Local JVM unit tests |
| `androidTest` | Instrumented tests, on device or emulator |

```text
app/src/
├── main/
│   ├── AndroidManifest.xml
│   ├── java/com/example/dashboard/     (yes, "java", even for Kotlin)
│   └── res/
├── debug/                              debug-only manifest and code
├── test/
└── androidTest/
```

Gradle merges `main` with the variant's own source set. That is how a debug-only
logging interceptor stays out of the release binary entirely — not behind an
`if`, but absent from the compiled output.

The `java/` directory name is historical. Kotlin sources live there.

## Resources and qualifiers

`res/` is not a free-form asset folder: the directory name *is* the query.

| Directory | Selected when |
|---|---|
| `res/values/` | Default |
| `res/values-es/` | System language is Spanish |
| `res/values-night/` | Dark theme is active |
| `res/drawable-xxhdpi/` | Screen density matches |
| `res/values-sw600dp/` | Smallest width is at least 600dp |

The system picks the best match at runtime and falls back to the unqualified
directory. Anything with no sensible default belongs in `assets/` instead, which
is an opaque file tree with no matching logic.

## The manifest, and what merges into it

`AndroidManifest.xml` declares components, permissions and app-level
configuration. What ships is **not** the file you wrote: the manifest merger
combines yours with the manifest of every dependency, plus the build type's.

```text
library manifests  ─┐
build type manifest ├─► merged manifest ─► APK
main manifest      ─┘
```

Priority runs main > build type > dependencies, and conflicts are resolved with
`tools:` attributes such as `tools:replace` and `tools:node="remove"`.

## Shrinking for release

R8 does three jobs at once on release builds: removes unreachable code, renames
what remains, and inlines. Keep rules go in `proguard-rules.pro`.

Anything resolved by **reflection** is invisible to R8, which is why
serialization models and Room entities need keep rules or a plugin that
generates them. A release build that crashes with a missing field while the
debug build works is nearly always this — see [[Android - Networking]].

Exact R8 defaults and the AGP behaviour around them are `<verify current>`.

## ⚠️ Gotchas

- ⚠️ **The merged manifest can add permissions you never requested.** A
  dependency declaring `INTERNET` or `ACCESS_NETWORK_STATE` silently adds it to
  your app, and users see it on the store listing. Inspect the merged output
  before every release, not the file you wrote.
- ⚠️ **R8 breaks reflection silently, and only in release.** The symptom is a
  null field or a `ClassNotFoundException` in production while debug is fine.
  Test the release variant before shipping, every time.
- ⚠️ **Do not commit `local.properties`.** It contains absolute SDK paths from
  your machine and breaks every other clone. It is also the file people
  accidentally put keys in — see [[Git - Ignoring Files]].
- **`build/`, `.gradle/` and `.idea/` are generated.** Ignore them. The
  `gradle/wrapper/` directory is the exception and must be committed, so that
  every clone and CI runner builds with the same Gradle.
- **Resource qualifiers are matched, not merged.** Providing `values-es` does
  not inherit missing strings from a partial translation file — untranslated
  keys fall back to `values/`, which is why a half-translated app shows mixed
  languages rather than failing.
- **Kotlin sources in `src/main/java/` is correct**, however wrong it looks.
  Renaming the directory requires reconfiguring the source set for no gain.

---

## Related

- [[Android - Gradle and AGP]]
- [[Android - Android Studio]]
- [[Android - Layered Architecture]]
- [[Git - Ignoring Files]]

## Sources

- <https://developer.android.com/studio/projects>
- <https://developer.android.com/build/manage-manifests>
- <https://developer.android.com/build/shrink-code>
