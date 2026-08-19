---
title: Gradle and AGP
domain: android
section: "62"
category: foundations
difficulty: intermediate
danger: high
tags:
  - android/build
  - android/gradle
  - android/security
commands:
  - ./gradlew assembleDebug
  - ./gradlew :app:dependencies
endpoints: []
dashboard_relevant: false
mobile_relevant: true
related:
  - "[[Android - Project Structure]]"
  - "[[Android - Android Studio]]"
  - "[[API - JSON YAML and TOML]]"
  - "[[Git - Ignoring Files]]"
sources:
  - https://developer.android.com/build
  - https://developer.android.com/build/migrate-to-catalogs
  - https://developer.android.com/studio/publish/app-signing
updated: 2026-08-18
---

# Gradle and AGP

Gradle is a general build tool; the **Android Gradle Plugin** teaches it what an
Android app is — variants, manifests, resources, packaging, signing. Almost
every build problem is really a question of which of the two you are fighting.
The distinction matters because their release cycles and their documentation are
separate, and their version numbers are not interchangeable.

## The three moving parts

| Component | What it is | Declared in |
|---|---|---|
| Gradle | The build tool itself | `gradle/wrapper/gradle-wrapper.properties` |
| AGP | The Android plugin for Gradle | The version catalog, applied in the root build |
| Kotlin plugin | Compiles Kotlin, runs compiler plugins | The version catalog |

These three are **mutually constrained**: each AGP release supports a range of
Gradle versions and expects a compatible Kotlin plugin. The current compatibility
matrix is `<verify current>` and must be read from developer.android.com rather
than inferred — upgrading one alone is the most common way to break a build.

> [!tip] Always build through the wrapper
> `./gradlew` uses the Gradle version pinned in `gradle-wrapper.properties`, so
> your machine and CI agree. A bare `gradle` command uses whatever is installed
> locally, which is how "works on my machine" starts.

## The version catalog

`gradle/libs.versions.toml` is the single place versions are declared. It is
TOML, with all the properties described in [[API - JSON YAML and TOML]]: real
date and string types, comments allowed, no significant whitespace.

```toml
[versions]
kotlin = "<verify current>"
agp = "<verify current>"
okhttp = "<verify current>"

[libraries]
okhttp = { module = "com.squareup.okhttp3:okhttp", version.ref = "okhttp" }
okhttp-logging = { module = "com.squareup.okhttp3:logging-interceptor", version.ref = "okhttp" }

[plugins]
android-application = { id = "com.android.application", version.ref = "agp" }
kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
```

```kotlin
dependencies {
    implementation(libs.okhttp)
    debugImplementation(libs.okhttp.logging)   // debug only. See gotchas
}
```

Note the accessor mapping: a dash in the catalog key becomes a dot in Kotlin, so
`okhttp-logging` is referenced as `libs.okhttp.logging`.

## Configurations: `implementation` versus `api`

A configuration decides who *else* sees a dependency.

| Configuration | Visible to consumers of your module | Rebuild triggered on change |
|---|---|---|
| `implementation` | No | Only this module |
| `api` | **Yes** | Every dependent module |
| `compileOnly` | No, and not packaged | This module |
| `debugImplementation` | Debug variant only | — |
| `testImplementation` | Unit tests only | — |

`api` leaks a dependency into your module's public ABI, so every module that
depends on you recompiles whenever it changes. In a single-module project the
difference is invisible; in a split project it is the difference between a
two-second and a two-minute incremental build. Default to `implementation` and
promote to `api` only when a type genuinely appears in your public signatures.

## Build types and product flavors

They are different axes, and the variant is their product.

| | Build type | Product flavor |
|---|---|---|
| Answers | How is it built? | Which edition is it? |
| Typical values | `debug`, `release` | `free`, `paid`, `internal` |
| Always present | Yes | No, entirely optional |

Two build types and two flavors give four variants. Most apps — including this
dashboard — need no flavors at all.

## Signing

```kotlin
android {
    signingConfigs {
        create("release") {
            storeFile = file(providers.gradleProperty("KEYSTORE_PATH").get())
            storePassword = providers.gradleProperty("KEYSTORE_PASSWORD").get()
            keyAlias = providers.gradleProperty("KEY_ALIAS").get()
            keyPassword = providers.gradleProperty("KEY_PASSWORD").get()
        }
    }
}
```

Values come from `~/.gradle/gradle.properties` or from CI secrets — never from
the build file, and never from the repository.

The debug keystore is generated automatically and is not a secret. The release
keystore is the identity of your app: Android will only accept an update signed
with the same key.

## Useful commands

```bash
./gradlew assembleDebug            # build the debug APK
./gradlew :app:dependencies        # resolved dependency tree, with conflicts
./gradlew :app:assembleRelease     # exercise R8 before you ship
./gradlew --scan                   # publish a build report for slow builds
```

## ⚠️ Gotchas

- ⚠️ **Never commit the release keystore or its passwords.** Losing control of
  the signing key means someone else can publish updates as you; losing the key
  itself means you can never update the app again under that identity. Unlike a
  token, it cannot be rotated. Keep it out of the repo and backed up separately
  — see [[Git - Ignoring Files]].
- ⚠️ **A leaked key stays leaked in history.** Committing then deleting it does
  nothing: it is still in every clone. Treat it as compromised and re-key.
- ⚠️ **Transitive version conflicts resolve silently.** Gradle picks the highest
  requested version by default, so a library upgrade can change a transitive
  dependency underneath you with no warning. `:app:dependencies` shows what was
  actually chosen.
- ⚠️ **`debugImplementation` is not a suggestion.** Putting the OkHttp logging
  interceptor on plain `implementation` ships it in release, where it writes the
  `Authorization` header into logcat — see
  [[API - Token Storage on Public Clients]].
- **Do not upgrade AGP, Gradle and Kotlin independently.** Check the
  compatibility matrix first; it is `<verify current>` and changes every release.
- **`gradle.properties` in the project is committed; the one in `~/.gradle` is
  not.** Machine-specific values and secrets belong in the latter.
- **The wrapper directory must be committed.** Ignoring `gradle/` entirely — a
  common mistake when writing a `.gitignore` by hand — breaks the build for
  everyone else.

---

## Related

- [[Android - Project Structure]]
- [[Android - Android Studio]]
- [[API - JSON YAML and TOML]]
- [[Git - Ignoring Files]]

## Sources

- <https://developer.android.com/build>
- <https://developer.android.com/build/migrate-to-catalogs>
- <https://developer.android.com/studio/publish/app-signing>
