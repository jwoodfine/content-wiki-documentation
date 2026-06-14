---
schema: foundry-doc-v1
title: "Guía de estilo: inventario"
slug: style-guide-inventory.es
short_description: "Estándares editoriales para documentos de inventario (familia PROSE): disciplina de tabla, vocabulario de clasificación, enumeración de estados y cuándo un inventario es el artefacto correcto frente a un registro o un brief."
category: reference
type: topic
content_type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-24
editor: pointsav-engineering
cites: []
paired_with: style-guide-inventory.md
---

Un inventario es un conteo fechado de lo que existe, en qué estado se encuentra y de qué tipo es. No es un plan ni un registro de cambios. Para la disciplina de [[citation-substrate|citas]] que rige cómo los inventarios referencian otros documentos, consulte el sustrato de citas.

## Cuándo usar esta plantilla

Se usa un inventario cuando se necesita un recuento para comprender el tamaño de una tarea de migración, limpieza o auditoría, o cuando la clasificación en sí misma es el entregable, o cuando se necesita una instantánea antes de un cambio estructural para registrar el estado anterior. Los inventarios son instantáneas: llevan fecha, envejecen y son reemplazados por uno nuevo cuando el alcance cambia significativamente.

## Estructura requerida

Tres secciones en orden:

1. **Opening** — un párrafo: qué alcance fue inventariado, a qué fecha y qué revela el recuento a alto nivel.
2. **Inventory table** — la enumeración. Columnas: `Item` (nombre canónico), `State` (enumeración cerrada), `Type` (enumeración cerrada), `Notes` (máximo una cláusula).
3. **Summary** — recuentos por estado y tipo. Totales. Puede incluir un apuntador de "acción siguiente" si el inventario es la entrada para una migración o auditoría.

Sección opcional **Classification vocabulary** cuando los valores de State y Type no son evidentes por sí mismos.

## Disciplina de la tabla

Una fila por ítem. Sin celdas combinadas. Los valores de `State` y `Type` provienen de enumeraciones cerradas. La columna Notes admite máximo una cláusula.

## Registro

Factual. Sin interpretación en la tabla: las filas son observaciones, no recomendaciones. Fechas en ISO 8601. Nombres canónicos del Nomenclature Matrix.

## Véase también

- [[style-guide-readme|Guía de estilo — README]]
- [[language-protocol-substrate|Substrato del Protocolo de Lenguaje]]
