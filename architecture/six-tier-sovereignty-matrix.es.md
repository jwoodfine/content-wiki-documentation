---
schema: foundry-doc-v1
title: "La matriz de seis niveles de soberanía"
slug: six-tier-sovereignty-matrix
category: architecture
type: concept
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: six-tier-sovereignty-matrix.md
short_description: "La matriz de seis niveles de soberanía organiza cada directorio del monorepo de PointSav por propósito, no por lenguaje o formato de compilación — seis prefijos fijos (app-, asset-, moonshot-, os-, service-, system-) que hacen que el repositorio sea autodocumentado y refuerzan la higiene de dependencias por convención."
cites: []
---

El monorepo de [[pointsav-overview|PointSav]] organiza cada directorio por propósito, no por lenguaje de programación o formato de compilación. Cada directorio en la raíz del repositorio pertenece a uno de seis niveles — `app-`, `asset-`, `moonshot-`, `os-`, `service-`, o `system-` — identificado por un prefijo fijo. Un contribuyente que lee el prefijo sabe inmediatamente en qué capa opera un directorio sin abrir ningún archivo. Este artículo cubre los seis niveles, la regla de propósito que rige la clasificación de nuevos directorios, la restricción kebab-case que hace que la taxonomía sea portable entre sistemas operativos y registros de contenedores, y los nombres anteriores que la taxonomía reemplaza.

## Los seis niveles

Cada directorio en la raíz del monorepo pertenece a uno de los siguientes niveles:

| Nivel | Prefijo | Propósito | Componentes de ejemplo |
|---|---|---|---|
| 1 — Aplicación | `app-` | Superficies orientadas al usuario — los cartuchos de personalidad que definen el aspecto y la sensación de un trabajo | `app-console-input`, `app-mediakit-marketing`, `app-orchestration-command` |
| 2 — Activo | `asset-` | Recursos no-código — fuentes, íconos, modelos 3D, tokens de diseño, activos de marca | `asset-brand-pointsav`, `asset-brand-wcp` |
| 3 — Moonshot | `moonshot-` | Experimentos de investigación y desarrollo aún no promovidos a producción | `moonshot-gpu` |
| 4 — OS | `os-` | Composiciones de sistemas operativos — los contenedores de ejecución que cargan otros componentes | [[console-os|`os-console`]], [[totebox-os|`os-totebox`]], [[os-orchestration|`os-orchestration`]] |
| 5 — Servicio | `service-` | Daemons de lógica de negocio en segundo plano | [[service-slm|`service-slm`]], [[service-content|`service-content`]], [[service-email|`service-email`]], [[service-people|`service-people`]] |
| 6 — Sistema | `system-` | Tecnología fundacional — controladores, redes, utilidades de base | `system-foundation`, `system-driver-network`, `system-audit` |

La palabra "librería" está explícitamente retirada como etiqueta de categoría. Describe cómo se compila el código, no qué hace.

## La regla de propósito

Un nuevo directorio se clasifica por su propósito, no por su formato. La decisión es corta:

| Pregunta | Nivel |
|---|---|
| ¿Habla con la computadora — análisis de fechas, redes, matemáticas, sistema de archivos? | `system-*` |
| ¿Habla con la vida del usuario — contactos, correo, fotos, contabilidad? | `service-*` |
| ¿Define el aspecto y la sensación para un trabajo específico? | `app-*` |
| ¿Es un recurso no-código — una fuente, un ícono, un token de diseño? | `asset-*` |
| ¿Es investigación especulativa aún no comprometida con producción? | `moonshot-*` |
| ¿Compone otros componentes en un contenedor de ejecución? | `os-*` |

## Por qué la disciplina de prefijos escala

Tres ventajas estructurales emergen de la taxonomía:

| Ventaja | Efecto |
|---|---|
| Descubribilidad | Un nuevo contribuyente que lee el nombre de un directorio sabe inmediatamente en qué capa opera sin abrir ningún archivo |
| Higiene de dependencias | `app-*` puede depender de `service-*` y `system-*`; `service-*` puede depender de `system-*`; `system-*` no tiene dependencias hacia arriba — las dependencias cíclicas son mecánicamente imposibles |
| Composición sobre herencia | Un sistema operativo es una composición `os-*` que carga cartuchos `app-*` y se conecta a daemons `service-*`; el SO no contiene código específico de características |

Esta es la expresión a nivel de sistema de archivos de la composición sobre herencia: el SO es un motor genérico; la aplicación es la personalidad.

## Kebab-case estricto

Los seis niveles usan ASCII en minúsculas con guiones. Las letras mayúsculas no están permitidas. La restricción se mantiene en registros Docker, sistemas de archivos Linux sensibles a mayúsculas/minúsculas, sistemas de archivos macOS insensibles a mayúsculas/minúsculas y subdominios DNS.

| Forma | Estado | Razón |
|---|---|---|
| `os-totebox` | Canónico | Kebab-case en minúsculas |
| `Totebox-OS` | No permitido | Las mayúsculas crean deriva fantasma entre sistemas operativos |
| `Totebox_OS` | No permitido | Los guiones bajos no son estándar en nombres de repositorios o contenedores |
| `toteboxos` | No permitido | Pierde legibilidad sin delimitador |

Las mayúsculas se preservan únicamente para un pequeño conjunto de archivos operacionales en la raíz — `README`, `LICENSE`, `CLAUDE.md`, `AGENT.md` — donde la convención es anterior a la regla kebab-case.

## Supersesión de nombres

La taxonomía tardó varias generaciones en estabilizarse. Los nombres anteriores aparecen en el archivo fuente y se normalizan cuando se migra el contenido:

| Nombre anterior | Canónico actual |
|---|---|
| `lib-pointsav-*` | `package-*` (bibliotecas compartidas) |
| `software-pdfs`, `software-wordprocessing` | `app-workplace-pdfs`, `app-workplace-wordprocessor` |
| `console-people`, `node-console-people` | `app-console-people` |
| `sys-marketing`, `sys-knowledge`, `sys-distro` | `app-mediakit-marketing`, `app-mediakit-knowledge`, `app-mediakit-distribution` |
| `fleet-infrastructure-*`, `gateway-interface-*`, `route-network-admin` | `app-infrastructure-onprem` / `-leased` / `-cloud`, `app-orchestration-command`, `app-network-admin` |

## Véase también

- [[os-family-overview]] — los ocho sistemas operativos compuestos usando el nivel `os-*`
- [[three-layer-architecture]] — el arreglo de tres capas de proveedor, cliente y operador en el que reside el monorepo
- [[five-stage-supply-chain]] — cómo los commits verificados del monorepo llegan a las implementaciones de producción
