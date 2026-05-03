---
schema: foundry-doc-v1
title: "Guía de estilo — TOPIC (resumen)"
slug: style-guide-topic.es
category: reference
type: topic
quality: core
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
paired_with: style-guide-topic.md
---
# Guía de estilo — TOPIC (resumen)

Un archivo TOPIC (`topic-<asunto>.md`) en una wiki de contenido
de Foundry explica *qué es* algo. Es doctrina, arquitectura o
contexto — material que un lector nuevo necesita para entender
el sistema. No describe cómo operar algo; eso corresponde a un
archivo GUIDE.

Este artículo es en sí mismo un TOPIC. La forma que sigue es la
forma que documenta.

## Reglas centrales

- **Frontmatter requerido.** Cada TOPIC declara sus dependencias
  de citación en YAML por la disciplina de citación de
  CLAUDE.md §16. Los IDs se resuelven contra
  `~/Foundry/citations.yaml`.
- **Pareja bilingüe obligatoria.** Cada `topic-<asunto>.md` se
  acompaña de `topic-<asunto>.es.md`. El español es adaptación
  estratégica, no traducción 1:1.
- **Mostrar antes de explicar.** El TOPIC abre con el artefacto
  que el lector puede sostener mentalmente — diagrama, ejemplo
  o afirmación central en una oración. El razonamiento, las
  citas y los compromisos vienen después.
- **Voz Bloomberg.** Voz activa por defecto. Promedio de
  oraciones cerca de dieciocho palabras. La lista de
  vocabulario prohibido aplica en su totalidad.
- **Lenguaje a futuro con cautela.** Capacidad o cronograma
  futuros se describen como "planeado", "previsto", "puede",
  "objetivo". La Sovereign Data Foundation se referencia
  específicamente en términos planeados / previstos.
- **Citar cada afirmación no obvia.** La disciplina es
  auditabilidad, no exhaustividad académica.
- **Editar en el mismo archivo.** Sin sufijos `_V2` / `_V3` —
  el historial de Git es el registro de versiones.

## Qué no es un TOPIC

- No es un manual operativo. Las instrucciones operativas viven
  en archivos GUIDE dentro de la subcarpeta de despliegue que
  operan.
- No es material de marketing. La audiencia es colaboradores,
  clientes, reguladores e ingenieros.
- No es material solo para uso interno. Lo interno vive en
  `.claude/` o en instancias de despliegue, no en una wiki de
  contenido.

## Véase también

- [Documento canónico en inglés](topic-style-guide-topic.md)
- [Guía de estilo — README](topic-style-guide-readme.md)
- [Guía de estilo — GUIDE](topic-style-guide-guide.md)


---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™ y Totebox Archive™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos titulares.*
