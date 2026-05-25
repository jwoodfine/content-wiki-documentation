---
schema: foundry-doc-v1
title: "service-input"
slug: service-input
short_description: "service-input es el servicio de ingesta de documentos del Anillo 1 que acepta archivos en el perímetro por arrendatario, los enruta a través de analizadores específicos de formato y escribe la salida normalizada en el ledger WORM a través de service-fs."
category: services
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: service-input.md
language: es
---

`service-input` es el servicio de ingesta de documentos del Anillo 1 en la arquitectura del sistema de PointSav. Acepta archivos en el perímetro por arrendatario, los enruta a través de analizadores específicos de formato y escribe la salida normalizada en el Ledger Inmutable WORM por arrendatario a través de `service-fs`.

## La posición de Ancla

SYS-ADR-10 designa esta posición como El Ancla (tecla de función F12 en `os-console`): el único punto de ingesta obligatorio donde los bytes del documento entran en el Anillo 1, se someten a análisis determinista y se entregan a `service-fs` para almacenamiento permanente de solo adición. Nada sobre el análisis se delega a un modelo de IA; la misma entrada siempre produce el mismo `ParsedDocument`.

## Detección de formato

La detección de formato aplica dos estrategias en orden: coincidencia por extensión (`.pdf`, `.md`, `.docx`, `.xlsx`) y luego inspección de bytes mágicos como alternativa de respaldo. Esta detección es completamente determinista — sin inferencia de IA — conforme a SYS-ADR-07.

## Analizadores

Cuatro analizadores específicos de formato están registrados al inicio del daemon: PDF mediante oxidize-pdf 2.x, Markdown mediante pulldown-cmark 0.12, DOCX mediante docx-rust 0.1.x, y XLSX mediante calamine 0.34. Todos devuelven un `ParsedDocument` normalizado con campos `format`, `source_id`, `text` y `metadata`.

## Conformidad con ADR-07

ADR-07 prohíbe la inferencia de IA en el Anillo 1. `service-input` mantiene esta restricción en todo momento: la detección de formato utiliza coincidencia por extensión seguida de inspección de bytes mágicos; el análisis utiliza bibliotecas específicas que aplican algoritmos deterministas. `service-input` no intenta extraer significado del texto analizado. La interpretación semántica es responsabilidad de los servicios del Anillo 2 más abajo en la cadena.

## Relaciones con otros servicios del Anillo 1

`service-input` es uno de cuatro servicios de ingesta en el perímetro del Anillo 1: `service-input` para documentos genéricos, `service-email` para buzones de Microsoft Exchange, `service-people` para registros de identidad, y `service-fs` que es el ledger WORM mismo.

## Véase también

- [[fs-anchor-emitter]] — el servicio de anclaje del ledger WORM
- [[three-ring-architecture]] — ubicación en el perímetro del Anillo 1
- [[input-machine]] — la interfaz del lado cliente F12 a service-input
