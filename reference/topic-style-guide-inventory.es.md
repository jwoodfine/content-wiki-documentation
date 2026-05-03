---
schema: foundry-doc-v1
title: "Guía de estilo: INVENTORY"
slug: topic-style-guide-inventory.es
category: reference
type: topic
quality: core
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: topic-style-guide-inventory.md
---

Un archivo `INVENTORY.md` cataloga los sub-artefactos contenidos
en un directorio en una tabla escaneable. Es la respuesta a la
pregunta "¿qué hay aquí?" — no "¿qué hace este proyecto?", que
corresponde al README. Los inventarios son comunes en repositorios
de despliegue de flota y en directorios agregadores.

## Cuándo usar esta plantilla

Se usa cuando un directorio contiene una colección de
sub-artefactos nombrados que un mantenedor necesita revisar de
un vistazo. Casos comunes: un catálogo de despliegue en el
repositorio `woodfine-fleet-deployment` con múltiples
subdirectorios, o una instancia de despliegue que contiene
elementos registrados como plantillas o configuraciones activas.

No se usa en lugar de un README o un `ARCHITECTURE.md`: el
inventario responde "qué hay aquí", no "por qué existe" ni
"cómo está organizado".

## Estructura requerida

La plantilla exige dos secciones:

1. **Summary** — un bloque breve en prosa con el total de
   elementos, su desglose por estado o tipo, y cualquier
   condición notable. Dos a cuatro oraciones.
2. **Catalog** — una tabla Markdown con una fila por artefacto.
   Cada fila nombra el elemento, su estado, su inquilino o
   propietario, y notas breves si son necesarias.

La prosa explicativa va fuera de la tabla, no dentro de las
celdas. Las celdas contienen hechos escaneables.

## Registro

Operacional. Promedio de dieciséis palabras por oración en las
secciones de prosa, máximo veintiocho. Las celdas de la tabla
son más cortas: frases de cinco a diez palabras. Se usan los
nombres canónicos del Nomenclature Matrix. Se aplica la lista
de vocabulario prohibido.

## Véase también

- [[topic-style-guide-changelog|Guía de estilo — CHANGELOG]]
- [[topic-style-guide-readme|Guía de estilo — README]]
- [[topic-style-guide-architecture|Guía de estilo — ARCHITECTURE]]
