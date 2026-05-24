---
schema: foundry-doc-v1
title: "Guía de estilo: changelog"
slug: style-guide-changelog.es
short_description: "Estándares editoriales para archivos CHANGELOG.md en repositorios de la plataforma: disciplina de versiones, formato de entradas, orden de más reciente a más antiguo y distinción entre changelog y registro de commits."
category: reference
type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-24
editor: pointsav-engineering
cites: []
paired_with: style-guide-changelog.md
---

Un changelog responde una pregunta para cada versión: qué cambió, expresado en una línea, desde el punto de vista del lector.

## Cuándo usar esta plantilla

Todo repositorio que lleva números de versión usa un `CHANGELOG.md`. El archivo se crea cuando existe la primera entrada significativa, no como marcador de posición. Los repositorios que no versionan pueden omitirlo y rastrear los cambios significativos en `NEXT.md` o `cleanup-log.md`.

## Estructura requerida

Lista plana de bloques de versión, el más reciente al inicio:

```markdown
## M.m.P — YYYY-MM-DD

- <entrada en una línea, dirigida al lector>
```

Cada bloque lleva encabezado `##` con número de versión y fecha en ISO 8601 en la misma línea. Una viñeta por cambio significativo, orientada al lector: describe el efecto, no el mecanismo. Se pueden agregar etiquetas de agrupación (`### Added`, `### Fixed`, `### Changed`) cuando un bloque tiene más de cinco entradas; se omiten para cinco o menos.

## Qué incluir y qué excluir

**Incluir:** nuevas capacidades disponibles para los consumidores, cambios que rompen la compatibilidad, correcciones con impacto visible, cambios estructurales importantes.

**Excluir:** refactorizaciones internas sin efecto visible para el consumidor, cambios en pruebas o CI, commits solo de documentación, commits de actualización de versión.

## Registro

Llano, activo, tiempo presente: "Agrega soporte para X", "Corrige el error de análisis Y." Máximo veinte palabras por entrada. ISO 8601 para fechas. No "hemos agregado" ni "esta versión incluye."

## Véase también

- [[style-guide-readme|Guía de estilo — README]]
- [[language-protocol-substrate|Substrato del Protocolo de Lenguaje]]
