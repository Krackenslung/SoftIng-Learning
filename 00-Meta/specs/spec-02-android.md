# spec-02-android

Añadir el dominio `60-Android/` — el cliente del dashboard.

Convenciones, frontmatter, reglas de enlaces y flujo de trabajo: ver `CLAUDE.md`.
Este spec solo describe lo nuevo.

---

## Por qué "Android" y no "Android Studio"

Android Studio es una interfaz sobre Gradle, AGP y el SDK. Lo que cambia cada
release son menús, atajos y asistentes — justo lo que se pudre en una nota. Lo
duradero está debajo. **Una sola nota cubre el IDE**; el resto es plataforma.

## ⚠️ Regla especial de este spec: versiones

El ecosistema Android se mueve mucho más rápido que Git o HTTP.

**No inventes ningún número de versión** — ni de AGP, Gradle, Kotlin, Compose
BOM, `compileSdk`, `targetSdk`, `minSdk`, ni de ninguna librería. Escribe
`<verify current>` en su lugar.

Al terminar, deja en `00-Meta/specs/spec-02-android-VERSIONS.md` la lista de todo
lo marcado, con el enlace de developer.android.com donde contrastarlo. Yo lo
verifico.

Prefiere describir **el mecanismo** en vez de la versión: "el catálogo de
versiones vive en `gradle/libs.versions.toml`" envejece bien; "usa AGP 8.x" no.

## Contexto que deben asumir las notas

El dashboard es una app Android nativa, cliente de la API de GitHub,
**arquitectura Opción A: solo cliente**. Sin backend, polling con WorkManager,
token en Keystore. Ver `API - Client-Only vs Backend Architectures`.

Kotlin en todos los ejemplos. Compose para UI.

---

## Archivos

```
60-Android/
├── Android.md                                        ★ hub
├── Foundations/
│   ├── Android - Project Structure.md                61
│   ├── Android - Gradle and AGP.md                   62
│   ├── Android - Android Studio.md                   63
│   └── Android - App Lifecycle.md                    64
├── Architecture/
│   ├── Android - Layered Architecture.md             65
│   ├── Android - Offline First and Room.md           66
│   └── Android - Dependency Injection.md             67
├── UI/
│   ├── Android - Jetpack Compose.md                  68
│   ├── Android - State and ViewModel.md              69
│   └── Android - Navigation.md                       70
├── Data/
│   ├── Android - Networking.md                       71
│   ├── Android - Coroutines and Flow.md              72
│   └── Android - Paging.md                           73
├── Background/
│   ├── Android - WorkManager.md                      74
│   └── Android - Background Limits and Doze.md       75
└── Security/
    └── Android - Keystore and Secure Storage.md      76

30-Bridge/
└── Bridge - GitHub API on Android.md                 B8
```

`domain: android`, `category`: `foundations` | `architecture` | `ui` | `data` |
`background` | `security`. Casi todas llevan `mobile_relevant: true`; marca
`dashboard_relevant: true` en las que informan directamente la construcción.

---

## Contenido por nota

**61 Project Structure** — módulos vs source sets, `app/src/main`,
`AndroidManifest.xml`, recursos y qualifiers, `build.gradle.kts` de proyecto vs
de módulo, R8/ProGuard. ⚠️ el manifest fusiona el de las dependencias — las
sorpresas de permisos vienen de ahí.

**62 Gradle and AGP** — tareas y configuraciones, `libs.versions.toml`, build
types vs product flavors, `signingConfigs`, por qué el keystore de firma nunca se
commitea. ⚠️ `implementation` vs `api` y su efecto en tiempos de compilación.

**63 Android Studio** — la única nota de IDE. Atajos que valen la pena, Logcat,
Layout Inspector, App Inspection (Database + Network), perfilador, integración
con Git y por qué es preferible la CLI para operaciones destructivas. Mantenla
corta y sin capturas: envejece rápido, y hay que decirlo en la propia nota.

**64 App Lifecycle** — Activity y su ciclo, muerte de proceso y
`SavedStateHandle`, cambios de configuración, `Lifecycle` y
`repeatOnLifecycle`. ⚠️ el sistema puede matar el proceso en cualquier momento:
el estado de sync se persiste, no se guarda en memoria.

**65 Layered Architecture** — UI / domain / data, el patrón repository, modelos
de dominio separados de los DTO de red. Conecta con
`API - Client-Only vs Backend Architectures`: poner la red detrás de una
interfaz es lo que deja abierta la migración a un backend.

**66 Offline First and Room** — la base de datos local como fuente de verdad,
entidades/DAO/migraciones, `Flow` desde queries, estrategia de sincronización y
resolución de conflictos. Enlaza con la tabla de caché de
`Dev Dashboard - Data Model`.

**67 Dependency Injection** — por qué inyectar, Hilt vs manual vs Koin, scopes,
inyección en ViewModels y Workers. ⚠️ inyectar en `WorkManager` requiere una
factory propia.

**68 Jetpack Compose** — declarativo vs vistas, composables, recomposición,
modificadores, `remember` vs `rememberSaveable`, listas con `key`. ⚠️
recomposición innecesaria: claves estables y parámetros inmutables.

**69 State and ViewModel** — elevación de estado, `StateFlow` en el ViewModel,
`collectAsStateWithLifecycle`, modelar carga/éxito/error como sealed class,
eventos de una sola vez. ⚠️ `collectAsState` sin lifecycle sigue recolectando en
background.

**70 Navigation** — grafo de navegación, rutas con tipos, back stack, deep links.
⚠️ los deep links son la vía de retorno del OAuth — conecta con
`API - OAuth 2.0 Flows` y las App Links.

**71 Networking** — OkHttp e interceptores (auth, User-Agent, versión de API),
Retrofit para REST, Apollo Kotlin para GraphQL, caché en disco de OkHttp y ETags,
manejo de errores. ⚠️ recuerda que OkHttp convierte el `304` en un `200` cacheado
— inspecciona `networkResponse` para medir cuota. Enlaza fuerte con
`API - Caching and ETags`, `GitHub - REST API`, `API - REST vs GraphQL`.

**72 Coroutines and Flow** — suspend, scopes, dispatchers, structured
concurrency, cancelación, `Flow` frío vs `StateFlow`/`SharedFlow` calientes,
operadores útiles. ⚠️ `GlobalScope` filtra trabajo; usa el scope del ViewModel.

**73 Paging** — Paging 3, `PagingSource`, `RemoteMediator` con Room. Mapea sobre
`API - Pagination Patterns`: claves `Int` para paginación por página, `String`
para cursores.

**74 WorkManager** — trabajo único vs periódico, constraints, backoff,
`Result.retry()`, encadenar trabajos, observar estado. ⚠️ **suelo de 15 minutos**
en trabajo periódico — es la restricción arquitectónica del dashboard.

**75 Background Limits and Doze** — Doze, App Standby buckets, límites de
servicios en background, optimización de batería, foreground services y sus
requisitos. Explica por qué "cada 5 minutos" no es realista y por qué hace falta
pull-to-refresh.

**76 Keystore and Secure Storage** — implementación Android de
`API - Token Storage on Public Clients`: generación de claves, AES-GCM, binding a
autenticación de usuario, `allowBackup`, qué no meter en logs ni crash reports.
No repitas el modelo de amenazas — enlaza a la nota de API.

**B8 Bridge - GitHub API on Android** — formato Bridge, abre con
`> **The general pattern is X. On Android it becomes Y.**` Cubre:
- polling en vez de webhooks, y el suelo de 15 min
- el `304` de OkHttp que se ve como `200`
- OAuth con Custom Tabs + App Links en vez de redirect de servidor
- el token en Keystore en vez de en una sesión de servidor
- Room como fuente de verdad en vez de caché de servidor
- `ignoreUnknownKeys` obligatorio contra una API que añade campos

---

## Cableado

Enlaces inversos a añadir (frontmatter `related` **y** sección `## Related`):

- `API - Client-Only vs Backend Architectures` → Layered Architecture,
  WorkManager, Offline First and Room
- `API - Caching and ETags` → Networking
- `API - Pagination Patterns` → Paging
- `API - Idempotency and Retries` → WorkManager
- `API - OAuth 2.0 Flows` → Navigation, Keystore and Secure Storage
- `API - Token Storage on Public Clients` → Keystore and Secure Storage
- `API - Webhooks vs Polling` → WorkManager, Background Limits and Doze
- `API - REST vs GraphQL` → Networking
- `API - JSON YAML and TOML` → Networking, Gradle and AGP
- `GitHub - REST API` → Networking
- `Git - Ignoring Files` → Project Structure (qué ignorar en un proyecto Android)

Además:
- `Bridge - GitHub API on Android` en: `Home.md` -> `## Bridge notes`;
  `Git.md` -> `## Where Git ends and GitHub begins`; `GitHub.md` -> `## API`
  (no tiene lista Bridge); `Web-APIs.md` -> `## Where this meets GitHub`
- `[[Android]]` en la tabla `## Start here` de `Home.md` (no hay sección
  "Domains"), y en `Web-APIs.md`
- `Dev Dashboard - Data Model` y `Dev Dashboard - API Map`: enlazar las notas
  Android que implementan cada decisión (Room, WorkManager, Keystore, Networking)
- `Vault Structure.md`: añadir `60-Android/` al árbol y `android` a los valores
  de `domain`
- `Glossary.md`: composable, recomposición, coroutine, Flow, StateFlow, Doze,
  foreground service, DAO, Hilt, deep link, App Link
- `Sources.md`: la tabla de Android ya existe — amplíala con Compose, Room,
  Paging, Coroutines, Hilt

---

## Fases

1. Plan — lista completa con metadatos y enlaces. Para.
2. Foundations (4) + hub. Para.
3. Architecture (3) + UI (3). Para.
4. Data (3) + Background (2) + Security (1). Para.
5. Bridge B8 + todo el cableado.
6. `python 00-Meta/scripts/validate.py`, corregir, salida limpia.
   (`python3` no existe en esta maquina: abre la Microsoft Store.)
7. Escribir `spec-02-android-VERSIONS.md` con todo lo marcado `<verify current>`.
   Actualizar el conteo de notas en `CLAUDE.md`.

Un commit por fase, mensajes en imperativo.
