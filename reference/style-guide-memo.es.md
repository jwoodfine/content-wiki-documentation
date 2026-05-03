---
schema: foundry-doc-v1
title: "Guía de estilo: Memo"
slug: style-guide-memo.es
category: reference
type: topic
quality: core
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
paired_with: style-guide-memo.md
---

Un **memo** en Foundry es un registro interno de arquitectura o decisión — un relato duradero del problema existente, lo que se eligió y qué cambia como resultado — escrito en un nivel de lectura de grado 12 con citas para cada afirmación no evidente.

Esta plantilla forma parte de la familia PROSE en el registro de plantillas de géneros de `service-disclosure`. Es la forma escrita de un registro de decisión de arquitectura (ADR): un memo explica una decisión con suficiente detalle para que un lector que se une al proyecto años después pueda entender por qué el sistema es como es.

## Cuándo usar esta plantilla

Úsela cuando una decisión afecte la arquitectura, la gobernanza o la postura operacional de la plataforma y necesite un registro duradero en primera persona. No la use para instrucciones operacionales (esas van en archivos GUIDE) ni para antecedentes conceptuales sin una decisión (eso va en un TOPIC).

## Tres secciones obligatorias

La plantilla exige tres secciones:

- **Antecedentes** — el problema y las restricciones relevantes; debe permitir que un lector que no conoce la decisión entienda por qué fue necesaria
- **Decisión** — qué se eligió y por qué; estado la elección con claridad en la primera oración; citar afirmaciones no evidentes; referenciar memos anteriores por nombre canónico cuando corresponda
- **Consecuencias** — qué cambia aguas abajo y qué compromisos se aceptan; nombrar los costos explícitamente

## Registro y tono

El registro es Bloomberg. La longitud objetivo de oración es más amplia que en las plantillas operacionales: media de unas dieciocho palabras, máximo treinta. Los memos llevan argumentos y matices; la longitud de oración lo refleja. Se aplica la lista global de vocabulario prohibido.

## Regla de edición en el lugar

Un memo nunca se versiona creando una copia `_V2` o `_V3`. Se edita el archivo existente; el historial de Git conserva las versiones anteriores. No se reinicia la numeración para las revisiones.

## Véase también

- [[style-guide-topic|Guía de estilo: TOPIC]]
- [[style-guide-guide|Guía de estilo: GUIDE]]
- [[citation-substrate|Sustrato de citas]]
