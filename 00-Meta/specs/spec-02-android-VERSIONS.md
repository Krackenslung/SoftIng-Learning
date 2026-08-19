# spec-02-android — lista de verificación de versiones

Todo lo que las notas de `60-Android/` marcaron como `<verify current>`, con la
nota donde vive y dónde contrastarlo. **Ninguna de estas cifras está afirmada en
el vault**: cada una aparece literalmente como `<verify current>`.

Al comprobar una, sustituye la marca en la nota indicada y tacha la fila aquí.

- **31 marcas** en 16 notas de `60-Android/`, más 3 en `40-Web-APIs/` y 1 en
  `30-Bridge/`.
- Generado: 2026-08-18.

---

## 1. Cadena de compilación

| # | Qué verificar | Nota | Dónde |
|---|---|---|---|
| 1.1 | Matriz de compatibilidad Gradle ↔ AGP ↔ plugin de Kotlin. **Es la más importante**: subir uno solo rompe la build | `Android - Gradle and AGP` | <https://developer.android.com/build/releases/gradle-plugin> |
| 1.2 | Versión de Kotlin para `libs.versions.toml` | `Android - Gradle and AGP` | <https://kotlinlang.org/docs/releases.html> |
| 1.3 | Versión de AGP para `libs.versions.toml` | `Android - Gradle and AGP` | <https://developer.android.com/build/releases/gradle-plugin> |
| 1.4 | Versión de OkHttp para `libs.versions.toml` | `Android - Gradle and AGP` | <https://square.github.io/okhttp/> |
| 1.5 | Comportamiento por defecto de R8 y qué hace AGP alrededor | `Android - Project Structure` | <https://developer.android.com/build/shrink-code> |

## 2. Librerías Jetpack

| # | Qué verificar | Nota | Dónde |
|---|---|---|---|
| 2.1 | Versión de Room y configuración de su procesador de anotaciones | `Android - Offline First and Room` | <https://developer.android.com/jetpack/androidx/releases/room> |
| 2.2 | Versión del artefacto de Paging | `Android - Paging` | <https://developer.android.com/jetpack/androidx/releases/paging> |
| 2.3 | BOM de Compose y configuración del plugin de compilador | `Android - Jetpack Compose` | <https://developer.android.com/develop/ui/compose/bom> |
| 2.4 | Artefactos de Hilt, plugin y procesador | `Android - Dependency Injection` | <https://developer.android.com/training/dependency-injection/hilt-android> |
| 2.5 | API para registrar un `WorkerFactory` propio y desactivar la inicialización automática de `WorkManager` | `Android - Dependency Injection` | <https://developer.android.com/topic/libraries/architecture/workmanager/advanced/custom-configuration> |
| 2.6 | Versión y artefactos de `WorkManager` | `Android - WorkManager` | <https://developer.android.com/jetpack/androidx/releases/work> |
| 2.7 | Artefacto que provee `collectAsStateWithLifecycle` | `Android - State and ViewModel` | <https://developer.android.com/jetpack/androidx/releases/lifecycle> |
| 2.8 | Nivel de API y artefacto de `repeatOnLifecycle` | `Android - App Lifecycle` | <https://developer.android.com/topic/libraries/architecture/coroutines> |
| 2.9 | Disponibilidad y estabilidad de las rutas tipadas de Navigation | `Android - Navigation` | <https://developer.android.com/guide/navigation> |

## 3. Comportamiento de plataforma

Esta sección es la que más se mueve. Las tres primeras filas sostienen decisiones
de arquitectura, no detalles de implementación.

| # | Qué verificar | Nota | Dónde |
|---|---|---|---|
| 3.1 | **Intervalo mínimo de trabajo periódico (15 min).** Es la restricción arquitectónica del dashboard: si cambia, cambia la promesa de frescura | `Android - WorkManager`, `Bridge - GitHub API on Android`, `API - Client-Only vs Backend Architectures` | <https://developer.android.com/topic/libraries/architecture/workmanager/how-to/define-work> |
| 3.2 | Umbrales de Doze, nombres de los App Standby buckets y su efecto por release | `Android - Background Limits and Doze`, `API - Client-Only vs Backend Architectures` | <https://developer.android.com/training/monitoring-device-state/doze-standby> |
| 3.3 | Requisitos de foreground service y tipos permitidos en el `targetSdk` elegido | `Android - Background Limits and Doze` | <https://developer.android.com/develop/background-work/services/fgs> |
| 3.4 | Sintaxis de `adb shell dumpsys deviceidle` y `am set-standby-bucket` | `Android - Background Limits and Doze` | <https://developer.android.com/tools/adb> |
| 3.5 | Requisitos de verificación de App Links y atributos del manifest | `Android - Navigation` | <https://developer.android.com/training/app-links/verify-android-applinks> |

## 4. Seguridad y almacenamiento

| # | Qué verificar | Nota | Dónde |
|---|---|---|---|
| 4.1 | Estado de la librería Jetpack Security crypto y de `EncryptedSharedPreferences`, y cuál es hoy el reemplazo recomendado | `Android - Keystore and Secure Storage`, `API - Token Storage on Public Clients` | <https://developer.android.com/privacy-and-security/cryptography> |
| 4.2 | API de `setUserAuthenticationParameters` y sus constantes | `Android - Keystore and Secure Storage` | <https://developer.android.com/privacy-and-security/keystore> |
| 4.3 | Disponibilidad de StrongBox y cómo consultarla | `Android - Keystore and Secure Storage` | <https://developer.android.com/privacy-and-security/keystore> |
| 4.4 | `minSdk` de cada opción de `KeyGenParameterSpec` usada | `API - Token Storage on Public Clients` | <https://developer.android.com/privacy-and-security/keystore> |
| 4.5 | Atributo y formato actual de las reglas de exclusión de backup | `Android - Keystore and Secure Storage`, `API - Token Storage on Public Clients` | <https://developer.android.com/identity/data/autobackup> |

## 5. Fuera de Android

| # | Qué verificar | Nota | Dónde |
|---|---|---|---|
| 5.1 | Valor vigente de la cabecera `X-GitHub-Api-Version` (es una fecha) | `Android - Networking` | <https://docs.github.com/en/rest/about-the-rest-api/api-versions> |
| 5.2 | Versiones y artefactos de OkHttp, Retrofit y Apollo Kotlin | `Android - Networking` | <https://square.github.io/okhttp/> · <https://square.github.io/retrofit/> |

## 6. Documentación que envejece sola

| # | Qué verificar | Nota | Dónde |
|---|---|---|---|
| 6.1 | Rutas de menú, nombres de paneles y atajos de Android Studio. La nota avisa de esto en su propio texto y se mantiene deliberadamente corta | `Android - Android Studio` | <https://developer.android.com/studio/intro> |

---

## Cómo cerrarlo

1. Verificar de arriba abajo; las secciones 1 y 3 son las que bloquean escribir
   código real.
2. Sustituir cada `<verify current>` en la nota indicada por el valor
   comprobado, **con la fecha de comprobación entre paréntesis** — sin fecha, un
   número vuelve a ser una afirmación sin respaldo dentro de seis meses.
3. Actualizar `updated:` en el frontmatter de las notas tocadas.
4. Ejecutar `python 00-Meta/scripts/validate.py`.

> [!warning] La regla no caduca
> Que estas marcas se resuelvan una vez no convierte el vault en inmune. Toda
> nota nueva de `60-Android/` vuelve a escribir `<verify current>` y vuelve a
> añadir su fila aquí. Es la única parte del vault cuyas fuentes cambian más
> rápido de lo que se revisa.
