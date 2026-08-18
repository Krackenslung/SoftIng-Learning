# CLAUDE.md

Contexto permanente para Claude Code. Se lee automáticamente en cada sesión.
**Las notas del vault se escriben en inglés**; este archivo y los specs pueden
estar en español.

---

## Qué es este vault

Vault de Obsidian que documenta Git, GitHub y los fundamentos de APIs web. Sirve
para dos cosas:

1. Referencia personal
2. Entrada estructurada para un **dashboard de desarrollo que será una app
   Android nativa** consumiendo la API de GitHub

La decisión de arquitectura asumida es **Opción A: solo cliente** — sin backend,
polling con `WorkManager`, token en Keystore. Está documentada en
`40-Web-APIs/Patterns/API - Client-Only vs Backend Architectures.md`.

## Estructura

```
00-Meta/          Home, Vault Structure, Templates/, scripts/, specs/
10-Git/           Foundations, Daily-Use, History-Rewriting,
                  Collaboration, Investigation, Advanced
20-GitHub/        Platform, Collaboration, Automation, API, Security, Extras
30-Bridge/        Donde Git y GitHub se cruzan
40-Web-APIs/      Fundamentals, Auth, Patterns, Data-Formats
90-Reference/     Cookbook, troubleshooting, cheat sheet, glosario, sources
95-Projects/      Especificaciones del dashboard
_attachments/     Imágenes y canvases
```

Los prefijos numéricos controlan el orden alfabético del explorador. Huecos de 10
para poder insertar sin renumerar. `90+` es material de consulta.

## Nomenclatura

Cada nota lleva prefijo de dominio, para evitar colisiones y desambiguar el
autocompletado:

```
Git - <Topic>.md
GitHub - <Topic>.md
Bridge - <Topic>.md
API - <Topic>.md
```

Los hubs son la excepción: `Git.md`, `GitHub.md`, `Web-APIs.md`, `Home.md`.

## Frontmatter obligatorio

Frontmatter parcial **rompe las consultas Dataview de los hubs**.

```yaml
---
title: Caching and ETags          # sin prefijo de dominio
domain: api                       # git | github | api | bridge | reference | project
section: "43"                     # clave de orden; "B7" para notas Bridge
category: fundamentals            # subgrupo dentro del dominio
difficulty: intermediate          # beginner | intermediate | advanced
danger: none                      # none | low | medium | high
tags:
  - api/http                      # anidados con /
commands: []                      # comandos CLI cubiertos
endpoints: []                     # endpoints de API cubiertos (notas GitHub)
dashboard_relevant: true          # informa la construcción del dashboard
mobile_relevant: true             # restricción específica del cliente Android
related:
  - "[[GitHub - REST API]]"       # OBLIGATORIO entrecomillar
sources:
  - https://developer.mozilla.org/...
updated: 2026-08-14
---
```

⚠️ Un wikilink sin comillas en YAML se parsea como secuencia anidada, no como
string. Siempre `"[[Nota]]"`.

## Estructura del cuerpo

1. Un párrafo de orientación al principio, **sin encabezado encima**
2. El concepto antes que la sintaxis
3. Tablas para todo lo comparativo
4. Bloques de código siempre con lenguaje. **Kotlin** para código de cliente
   (el dashboard es Android), HTTP crudo para formato de cable, bash para CLI
5. Sección `## ⚠️ Gotchas` donde aplique; ⚠️ marca pérdida de datos o fallo
   silencioso — es convención central del vault
6. Cerrar siempre con `## Related` y luego `## Sources`
7. Texto ajustado a ~80 caracteres por línea

## Reglas de enlaces

- Mínimo **3** enlaces `related` por nota
- **Bidireccionales**: añadir el enlace inverso en el frontmatter `related` **y**
  en la sección `## Related` visible de la nota destino
- Toda nota nueva se enlaza desde su hub correspondiente
- Cero notas huérfanas

## Fuentes

Mínimo 2 fuentes primarias por nota. En orden de preferencia:

| Tema | Fuente |
|---|---|
| Git | git-scm.com/docs, Pro Git |
| GitHub | docs.github.com |
| HTTP / APIs | RFCs en datatracker.ietf.org, MDN |
| OAuth / OIDC | RFC 6749, 7636, 8252; openid.net |
| Android | developer.android.com |

Blogs solo si no existe fuente primaria. Nunca inventar URLs.

## Restricciones

- **Solo Dataview** como plugin de comunidad. No usar sintaxis de otros plugins.
- **Callouts en minúscula** (`> [!tip]`, `> [!warning]`). Las alertas GFM en
  mayúscula (`> [!NOTE]`) **no** renderizan en Obsidian.
- Sin guiones largos dentro de valores YAML salvo que se entrecomille el valor.
- **No inventar números de versión** de AGP, Kotlin, Compose, `targetSdk` ni de
  ninguna librería. Escribir `<verify current>` y listarlo al final para
  contrastar.
- No renumerar carpetas ni renombrar archivos existentes.
- No modificar el cuerpo de notas existentes salvo que el spec lo pida
  explícitamente; fuera de eso, solo añadir a sus arrays `related`.

## Flujo de trabajo

Los specs llegan como archivos en `00-Meta/specs/`. Para cualquier spec:

1. **Planificar primero.** Mostrar la lista de archivos con `section`,
   `category`, `difficulty`, `danger` y los enlaces `related` de cada uno.
   Esperar aprobación.
2. **Trabajar por fases**, parando entre cada una. No generar más de ~6 notas de
   una vez — la voz se degrada y el frontmatter se vuelve descuidado.
3. **Cablear**: enlaces inversos, entradas en hubs, `Sources.md`, `Glossary.md`.
4. **Validar**: `python 00-Meta/scripts/validate.py` desde la raíz. Corregir
   todo lo que reporte. Enseñar la salida limpia.

## Validación

`00-Meta/scripts/validate.py` comprueba:
- wikilinks rotos (ignora bloques de código y backticks en línea — si no, da
  falsos positivos con la documentación del esquema)
- frontmatter ausente o wikilinks sin comillas en YAML
- notas huérfanas
- conteo por carpeta

Debe salir limpio antes de dar por terminada cualquier tarea.

## Estado actual

83 notas. 0 enlaces rotos, 0 huérfanas.

| Carpeta | Notas |
|---|---|
| 10-Git | 21 + hub |
| 20-GitHub | 25 + hub |
| 30-Bridge | 7 |
| 40-Web-APIs | 15 + hub |
| 90-Reference | 5 |
| 95-Projects | 2 |

## Próximo dominio previsto

`60-Android` — el cliente del dashboard. Sale casi entero de lo ya escrito:
Retrofit/Apollo desde `API - REST vs GraphQL`, WorkManager desde
`API - Webhooks vs Polling`, Room desde la tabla de caché de
`Dev Dashboard - Data Model`, Keystore desde
`API - Token Storage on Public Clients`.

⚠️ El ecosistema Android se mueve mucho más rápido que Git. Cualquier número de
versión en esas notas hay que contrastarlo con developer.android.com.
