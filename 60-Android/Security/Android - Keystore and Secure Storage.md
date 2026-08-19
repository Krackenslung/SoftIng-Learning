---
title: Keystore and Secure Storage
domain: android
section: "76"
category: security
difficulty: advanced
danger: high
tags:
  - android/security
  - android/auth
commands: []
endpoints: []
dashboard_relevant: true
mobile_relevant: true
related:
  - "[[API - Token Storage on Public Clients]]"
  - "[[API - OAuth 2.0 Flows]]"
  - "[[Android - Navigation]]"
  - "[[Android - Networking]]"
sources:
  - https://developer.android.com/privacy-and-security/keystore
  - https://developer.android.com/privacy-and-security/cryptography
  - https://developer.android.com/identity/data/autobackup
updated: 2026-08-18
---

# Keystore and Secure Storage

[[API - Token Storage on Public Clients]] establishes *what* a public client can
and cannot protect, and why. This note is the Android implementation of that:
the concrete store, the failure modes the platform adds, and the three places a
token escapes an app that otherwise stores it correctly — backup, logs and the
screen. It deliberately does not restate the threat model; read that note first.

Artifact names and the status of the Jetpack Security crypto library are
`<verify current>`. Everything below uses platform APIs, which is the point.

## A complete store

The Keystore holds the key; you hold the ciphertext.

```kotlin
class KeystoreTokenStore(private val context: Context) {

    private val file = File(context.filesDir, "token.bin")

    private fun key(): SecretKey {
        val store = KeyStore.getInstance(ANDROID_KEYSTORE).apply { load(null) }
        (store.getEntry(ALIAS, null) as? KeyStore.SecretKeyEntry)
            ?.let { return it.secretKey }

        val spec = KeyGenParameterSpec.Builder(
            ALIAS,
            KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT,
        )
            .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
            .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
            .setUserAuthenticationRequired(false)
            .build()

        return KeyGenerator
            .getInstance(KeyProperties.KEY_ALGORITHM_AES, ANDROID_KEYSTORE)
            .apply { init(spec) }
            .generateKey()
    }

    fun write(token: String) {
        val cipher = Cipher.getInstance(TRANSFORMATION)
        cipher.init(Cipher.ENCRYPT_MODE, key())
        file.writeBytes(cipher.iv + cipher.doFinal(token.toByteArray()))
    }

    fun read(): String? {
        if (!file.exists()) return null
        return try {
            val blob = file.readBytes()
            val cipher = Cipher.getInstance(TRANSFORMATION)
            cipher.init(Cipher.DECRYPT_MODE, key(), GCMParameterSpec(128, blob, 0, 12))
            String(cipher.doFinal(blob, 12, blob.size - 12))
        } catch (e: GeneralSecurityException) {
            clear()          // key invalidated: the ciphertext is unrecoverable
            null
        }
    }

    fun clear() {
        file.delete()
        KeyStore.getInstance(ANDROID_KEYSTORE)
            .apply { load(null) }
            .deleteEntry(ALIAS)
    }
}
```

The `catch` is not defensive padding. It is the recovery path for the failure
described next, and without it the app crashes on every launch forever.

## Key invalidation

A Keystore key can be destroyed by the system, permanently, while your ciphertext
remains on disk:

| Cause | When |
|---|---|
| Lock screen removed or changed | If the key requires user authentication |
| New biometric enrolled | If the key is invalidated on enrolment |
| App data cleared | Always |
| Restore to a new device | Keystore keys never leave the device |

The correct response is always the same: treat the token as gone, clear the
stored blob, and send the user through sign-in again. Detect it by catching
`KeyPermanentlyInvalidatedException` — a subclass of `GeneralSecurityException`
— rather than letting it propagate.

## Binding to the user

```kotlin
.setUserAuthenticationRequired(true)
.setUserAuthenticationParameters(timeoutSeconds, KeyProperties.AUTH_DEVICE_CREDENTIAL)
```

This is what converts a stolen unlocked-later phone from a compromise into an
inconvenience: the key is unusable until the user authenticates. The cost is that
background sync cannot decrypt while the device is locked, which for a polling
dashboard means no background refresh until the user unlocks.

That is a real product trade-off, not a purely technical one. For a read-only
dashboard token, `false` with a short-lived token is defensible; for anything
that can write, prefer `true`. The exact parameter API is `<verify current>`.

## The three escape routes

Storage is only one of them, and the other two are where working apps leak.

**Backup.** Application data is backed up off-device by default. Keystore
ciphertext is useless elsewhere, but excluding the file removes the question
entirely — declare backup rules that exclude the token file. Attribute names and
file format are `<verify current>`.

**Logs.** The OkHttp logging interceptor at header or body level writes
`Authorization` into logcat and into every crash report attached to it. Gate it
to debug builds *and* redact the header — see [[Android - Networking]] and
[[Android - Gradle and AGP]].

```kotlin
HttpLoggingInterceptor().apply {
    level = HttpLoggingInterceptor.Level.HEADERS
    redactHeader("Authorization")
    redactHeader("Cookie")
}
```

**The screen.** The recents thumbnail is captured by the system, and screenshots
are captured by the user. Apply `FLAG_SECURE` to any screen showing a token, and
never display one in full.

## What not to use

| Storage | Verdict |
|---|---|
| Keystore-wrapped ciphertext | Correct |
| `SharedPreferences` / DataStore, plain | **Never** — cleartext in the data directory |
| Room | **Never** — a plain SQLite file |
| Hardcoded in the APK | **Never** — trivially extracted |
| A file with no encryption | **Never** — readable with backup or root |

DataStore is right for preferences and wrong for secrets. The distinction is not
about the API's quality; it is that neither encrypts anything by itself.

## ⚠️ Gotchas

- ⚠️ **Not handling key invalidation crashes the app permanently.** The stored
  blob outlives the key, so every launch throws in the same place and the user
  cannot even reach sign-in. Catch it, clear, re-authenticate.
- ⚠️ **`setUserAuthenticationRequired(true)` stops background sync while
  locked.** Decide this deliberately: it is a genuine security-versus-freshness
  trade, and discovering it after shipping means either a downgrade or a broken
  feature.
- ⚠️ **A release logging interceptor leaks the token** into logcat and crash
  reports. Redaction and `debugImplementation`, both.
- ⚠️ **The Keystore does not protect a rooted or compromised device.** It will
  decrypt for whoever runs as your app. Pair it with short-lived tokens and
  working revocation — see [[API - Token Storage on Public Clients]].
- ⚠️ **Never put the token in a navigation route or saved state.** It ends up in
  the back stack and in the saved-state bundle — see [[Android - Navigation]].
- **Ship no client secret.** A public client cannot hold one, which is why PKCE
  is mandatory — see [[API - OAuth 2.0 Flows]].
- **StrongBox is not available on every device.** Request it, and fall back
  rather than failing; availability is `<verify current>`.
- **Clear the token on 401.** A revoked token that stays on disk produces an app
  that retries forever against a credential that will never work again.

---

## Related

- [[API - Token Storage on Public Clients]]
- [[API - OAuth 2.0 Flows]]
- [[Android - Navigation]]
- [[Android - Networking]]

## Sources

- <https://developer.android.com/privacy-and-security/keystore>
- <https://developer.android.com/privacy-and-security/cryptography>
- <https://developer.android.com/identity/data/autobackup>
