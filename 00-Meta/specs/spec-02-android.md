# Spec 02 — construir `60-Android`

Estado: **pendiente de ejecutar**. Convenciones vigentes en `CLAUDE.md`.

---

## Contexto

El vault documenta Git, GitHub y los fundamentos de APIs web (83 notas, 0 rotos,
0 huérfanas). Falta el último dominio: el **cliente Android** del dashboard.

La arquitectura ya está decidida y documentada: **Opción A, solo cliente**, sin
backend, en `40-Web-APIs/Patterns/API - Client-Only vs Backend Architectures.md`.
Este spec no la reabre. La implementa.

Antes de escribir nada, lee para calibrar voz y formato:

- `CLAUDE.md` — esquema de frontmatter, reglas de enlaces, restricciones
- `40-Web-APIs/Patterns/API - Client-Only vs Backend Architectures.md` — la
  decisión que gobierna todo este dominio
- `40-Web-APIs/Auth/API - Token Storage on Public Clients.md` — densidad y tono,
  y el único bloque Kotlin largo que ya existe
- `95-Projects/Dev Dashboard - Data Model.md` y `Dev Dashboard - API Map.md` —
  qué construye realmente la app
- `20-GitHub/GitHub.md` — estructura de hub con consultas Dataview

## Objetivo

Crear `60-Android/` con 13 notas más el hub. Cada nota traduce material que ya
existe en el vault a la plataforma concreta. **Ninguna nota entra por ser
"interesante en Android": entra porque implementa algo ya escrito en
`40-Web-APIs/` o en `95-Projects/`.**

Y reconciliar dos notas existentes que contradicen la Opción A — ver la Fase 5.

## Archivos a crear

```
60-Android/
├── Android.md                                       ★ hub
├── Foundations/
│   ├── Android - Project Structure and Gradle.md         61
│   ├── Android - App Architecture.md                     62
│   └── Android - Coroutines and Flow.md                  63
├── Networking/
│   ├── Android - Retrofit and OkHttp.md                  64
│   ├── Android - Apollo and GraphQL.md                   65
│   └── Android - Serialization.md                        66
├── Data/
│   ├── Android - Room.md                                 67
│   ├── Android - Paging.md                               68
│   └── Android - DataStore.md                            69
├── Background/
│   ├── Android - WorkManager.md                          70
│   └── Android - Background Execution Limits.md          71
└── Security/
    ├── Android - Keystore and Encrypted Storage.md       72
    └── Android - OAuth on Device.md                      73
```

`category`: `foundations` · `networking` · `data` · `background` · `security`

## De dónde sale cada nota

Ninguna nota se escribe desde cero. Cada una tiene un ancla, y el enlace es
obligatorio en ambas direcciones:

| Nota | Ancla en el vault |
|---|---|
| Project Structure and Gradle | — (andamiaje; ver `<versiones>`) |
| App Architecture | `Dev Dashboard - Data Model` |
| Coroutines and Flow | `API - Idempotency and Retries` (backoff, jitter, cancelación) |
| Retrofit and OkHttp | `API - Headers` · `API - Caching and ETags` · `API - HTTP Methods and Status Codes` |
| Apollo and GraphQL | `API - REST vs GraphQL` · `GitHub - GraphQL API` · `Bridge - GitHub API Conventions` |
| Serialization | `API - JSON YAML and TOML` |
| Room | `Dev Dashboard - Data Model` · `API - Caching and ETags` |
| Paging | `API - Pagination Patterns` |
| DataStore | `API - Token Storage on Public Clients` (qué **no** guardar aquí) |
| WorkManager | `API - Webhooks vs Polling` · `API - Client-Only vs Backend Architectures` |
| Background Execution Limits | `API - Client-Only vs Backend Architectures` · `API - Rate Limiting Strategies` |
| Keystore and Encrypted Storage | `API - Token Storage on Public Clients` |
| OAuth on Device | `API - OAuth 2.0 Flows` · `API - Token Storage on Public Clients` |

## Esquema de frontmatter

Completo, según `CLAUDE.md`. Valores nuevos para este dominio:

```yaml
---
title: Retrofit and OkHttp        # sin prefijo de dominio
domain: android                   # VALOR NUEVO
section: "64"
category: networking              # foundations | networking | data | background | security
difficulty: intermediate
danger: none
tags:
  - android/networking
  - android/http
commands: []
endpoints: []
dashboard_relevant: true
mobile_relevant: true             # true en todo 60-Android, por definición
related:
  - "[[API - Caching and ETags]]"
sources:
  - https://developer.android.com/...
updated: <fecha de ejecución>
---
```

`danger` para este dominio: `high` solo donde se pierde el token o se filtra
(Keystore, OAuth on Device). `medium` donde un error deja la app en silencio
desincronizada (WorkManager, Background Execution Limits, Room). El resto,
`low` o `none`.

## Versiones — la restricción que define este dominio

⚠️ **El ecosistema Android se mueve mucho más rápido que Git.** Todo lo demás en
el vault se apoya en RFCs y en `git-scm.com`, que son estables durante años. Aquí
no. Una nota con un `targetSdk` inventado es peor que no tener la nota.

Reglas, sin excepción:

1. **No escribir ningún número de versión** de AGP, Kotlin, Compose, `minSdk`,
   `targetSdk`, ni de ninguna librería. Escribir `<verify current>` en su lugar.
2. Cada nota cierra con una sección `## To verify` **antes** de `## Related`,
   listando sus `<verify current>` en viñetas.
3. Preferir **APIs de plataforma** (Keystore, `WorkManager`) sobre librerías con
   ciclo de vida propio. Cuando haya que nombrar una librería, decir qué hace y
   marcar su estado como `<verify current>` en lugar de afirmarlo.
4. `developer.android.com` es la fuente primaria. Mínimo 2 fuentes por nota; una
   de ellas puede ser la nota de `40-Web-APIs` que implementa.
5. El hub `Android.md` incluye una consulta Dataview que reúne todas las notas
   del dominio, para poder auditar los `<verify current>` de una pasada.

## Requisitos de contenido

Los de `CLAUDE.md`, con tres énfasis propios de este dominio:

1. **Kotlin en todos los bloques de código.** Es el único dominio donde no hay
   excusa para otra cosa. `bash` solo para comandos de Gradle.
2. **Empezar por la restricción, no por la API.** La nota de `WorkManager` no
   trata de `WorkManager`: trata de que un teléfono no puede recibir webhooks y
   de qué se hace con eso. La biblioteca es la respuesta, no el tema.
3. **Cada nota dice qué se rompe si la ignoras**, en `## ⚠️ Gotchas`. Los fallos
   de Android son mayoritariamente silenciosos: trabajo en background que nunca
   se ejecuta, claves invalidadas, procesos matados sin aviso.

Contenido concreto que no puede faltar:

- **Retrofit and OkHttp** — interceptor de `Authorization`; interceptor de
  `ETag` que persiste y reenvía; por qué el logging interceptor filtra tokens en
  release; `304` sin cuerpo; timeouts.
- **Room** — la caché local como fuente de verdad para la UI; qué se guarda de
  la tabla de entidades del `Data Model`; migraciones; por qué el `ETag` se
  guarda junto al dato que valida, y de forma atómica.
- **Paging** — cursores frente a offset sobre `Paging`; `RemoteMediator` como el
  punto donde se juntan red y caché; el problema del desplazamiento de offset ya
  descrito en `API - Pagination Patterns`.
- **WorkManager** — trabajo periódico, restricciones, política de reintento
  exponencial, unicidad del trabajo; que el intervalo mínimo y el comportamiento
  bajo Doze son `<verify current>`; que hay que mostrar en la UI la hora del
  último sync correcto.
- **Background Execution Limits** — Doze, app standby buckets, límites de
  arranque en background. Esta es la nota que explica por qué el dashboard es
  "en vivo con la app abierta y best-effort fuera".
- **Keystore and Encrypted Storage** — no repetir `API - Token Storage on Public
  Clients`: **implementarla**. Invalidación de claves al cambiar el bloqueo de
  pantalla y cómo recuperarse; exclusión de backup; `FLAG_SECURE`.
- **OAuth on Device** — Custom Tabs frente a WebView (y por qué WebView es
  inaceptable para OAuth); App Links frente a esquema propio para el redirect;
  device flow como alternativa; PKCE con `SecureRandom`.
- **DataStore** — para preferencias, y una advertencia explícita: **no es
  almacenamiento seguro**; el token va al Keystore.

## Requisitos de enlaces

1. Mínimo **3** enlaces `related` por nota, mezclando `60-Android` con las notas
   ancla de la tabla de arriba.
2. **Bidireccionales**: añadir el enlace inverso en el frontmatter `related` **y**
   en la sección `## Related` visible de la nota destino.
3. `Android.md` se enlaza desde `00-Meta/Home.md` y desde `40-Web-APIs/Web-APIs.md`.
4. Nuevas fuentes a la tabla `## Primary — Android` de `90-Reference/Sources.md`,
   que ya existe.
5. Términos nuevos al glosario solo si son conceptos, no nombres de librerías.

## Restricciones

- Las de `CLAUDE.md`, incluida la de no tocar el cuerpo de notas existentes.
  **Excepción explícita: la Fase 5**, que sí lo pide.
- No renumerar carpetas ni renombrar archivos.
- Solo Dataview. Callouts en minúscula.
- No inventar versiones. Ver `<versiones>` arriba.

## Flujo de trabajo

Parar entre fases. Máximo ~5 notas por tanda.

**Fase 1 — Plan.** Leer los archivos de contexto. Mostrar la lista con
`section`, `category`, `difficulty`, `danger` y los `related` de cada nota, más
los enlaces inversos previstos. Esperar aprobación.

**Fase 2 — Foundations + hub** (61–63 y `Android.md`). Parar.

**Fase 3 — Networking + Serialization** (64–66). Parar.

**Fase 4 — Data + Background** (67–71). Parar.

**Fase 5 — Security y reconciliación** (72–73), y arreglar la contradicción:

`95-Projects/Dev Dashboard - Data Model.md` describe una arquitectura de sync
basada en webhooks (`webhook → verify HMAC → dedupe → enqueue → update cache`) y
`95-Projects/Dev Dashboard - API Map.md` tiene una tabla de caché cuya columna
"Invalidated by" nombra webhooks de `pull_request`, `check_run` e `issues`.
**Ninguna de las dos es realizable en un cliente Android sin backend.** Ambas son
anteriores a la decisión de la Opción A. Reescribir esas dos secciones en
términos de polling con `WorkManager` y revalidación con `ETag`, enlazando a
`API - Client-Only vs Backend Architectures` y a `Android - WorkManager`. Es el
único cambio de cuerpo autorizado por este spec.

**Fase 6 — Cablear.** Enlaces inversos, `Home.md`, `Web-APIs.md`, `Sources.md`,
glosario. Y actualizar los documentos de convenciones, que hoy no conocen este
dominio:

- `CLAUDE.md` — añadir `60-Android/` al árbol, `android` a los valores de
  `domain`, `Android - <Topic>.md` al bloque de nomenclatura, secciones `61`–`73`,
  y reemplazar la sección "Próximo dominio previsto" por el estado real
- `00-Meta/Vault Structure.md` — mismas tres cosas
- `README.md` — añadir la fila de `60-Android/` a la tabla de carpetas y
  actualizar el total de notas

**Fase 7 — Validar.** `python 00-Meta/scripts/validate.py` desde la raíz.
Corregir todo. Enseñar la salida limpia.

⚠️ El comando es `python`, no `python3`: en esta máquina `python3` no existe y
abre la Microsoft Store.

## Criterios de éxito

- 14 archivos nuevos, 0 enlaces rotos, 0 huérfanas
- Frontmatter completo y ≥3 enlaces **bidireccionales** por nota
- Todos los bloques de código en Kotlin, salvo `bash` para Gradle
- Cero números de versión afirmados; todos marcados `<verify current>` y
  recogidos en la sección `## To verify` de cada nota
- Las dos notas de `95-Projects/` ya no describen webhooks
- `CLAUDE.md`, `Vault Structure.md` y `README.md` reflejan el dominio nuevo
- El validador sale limpio

## Decisiones abiertas

Resolver en la Fase 1, antes de escribir.

1. **¿Entra la capa de UI?** He dejado fuera `Android - Compose` y
   `Android - Navigation` a propósito: son los dos únicos temas que no derivan de
   nada ya escrito, y meterlos convierte el vault en documentación general de
   Android. La regla de este spec es que cada nota implementa material existente.
   Si quieres la UI dentro, entran como sección `74`–`75` y hay que aceptar el
   ensanchamiento de alcance.

2. **¿Nota puente?** `30-Bridge/` era "donde Git y GitHub se cruzan", pero ya
   contiene `Bridge - GitHub API Conventions`, que es genérico-API frente a
   GitHub. Un `Bridge - Android Client Constraints` (`B8`) encajaría en ese
   precedente. Alternativa: dejar el puenteo dentro de las propias notas de
   `60-Android`, que es lo que asume este spec.

3. **¿Testing?** Un `Android - Testing the API Layer` (MockWebServer, respuestas
   `304`, fixtures de rate limit) sería la nota con mejor relación valor/esfuerzo
   de las que no están en la lista. Fuera por ahora.
