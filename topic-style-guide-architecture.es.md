---
schema: foundry-doc-v1
title: "Guía de estilo: ARCHITECTURE"
slug: topic-style-guide-architecture.es
category: reference
type: topic
quality: core
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: topic-style-guide-architecture.md
---

Un archivo `ARCHITECTURE.md` en la raíz de un proyecto explica la
posición del proyecto dentro del sistema más amplio, la interfaz
que expone, la organización interna de sus módulos y, con igual
importancia, lo que el proyecto no hace.

## Cuándo usar esta plantilla

Se utiliza cuando el diseño del proyecto es suficientemente
complejo como para que un colaborador nuevo no pueda reconstruir
su estructura leyendo únicamente el código fuente. Los proyectos
con más de dos módulos significativos, una decisión de capas no
obvia, o un contrato de consumidor relevante con otras partes
del sistema, requieren un `ARCHITECTURE.md`.

Las utilidades de un solo archivo y los adaptadores delgados
generalmente no lo requieren.

## Estructura requerida

La plantilla exige cuatro secciones en este orden:

1. **Position** — dónde se ubica este proyecto en el sistema más
   amplio, con referencias a sus pares por nombre canónico.
2. **Public surface** — la API, interfaz o contrato que el
   proyecto expone al resto del sistema.
3. **Module layout** — árbol de directorios anotado de la
   organización interna del proyecto.
4. **What this is not** — objetivos explícitamente excluidos, para
   limitar la interpretación del lector.

## Registro

Técnico. Se asume familiaridad con el dominio. Las oraciones son
concisas — promedio de dieciocho palabras, máximo treinta. Se
aplica la lista de vocabulario prohibido. Los nombres canónicos
del Nomenclature Matrix se usan con exactitud.

## Véase también

- [[topic-style-guide-readme|Guía de estilo — README]]
- [[topic-style-guide-topic|Guía de estilo — TOPIC]]
- [[topic-language-protocol-substrate|Substrato del Protocolo de Lenguaje]]
