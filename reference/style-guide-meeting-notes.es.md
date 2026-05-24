---
schema: foundry-doc-v1
title: "Guía de estilo: notas de reunión"
slug: style-guide-meeting-notes.es
short_description: "Estándares editoriales para notas de reunión en la plataforma (género COMMS): campos de encabezado, disciplina de agenda, distinción entre decisiones y notas, y formato de tabla de elementos de acción."
category: reference
type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-24
editor: pointsav-engineering
cites: []
paired_with: style-guide-meeting-notes.md
---

Las notas de reunión existen para los elementos de acción y las decisiones. Todo lo demás es material de archivo.

## Cuándo usar esta plantilla

Se usan notas para toda reunión que produzca decisiones o elementos de acción. Las verificaciones informales breves que no producen ninguno no requieren notas: un mensaje de chat al canal es suficiente. Son obligatorias cuando se toma una decisión que afecta el alcance, el cronograma o la propiedad del trabajo, o cuando se asigna un elemento de acción a una persona nombrada.

## Estructura requerida

**Bloque de encabezado** (antes de cualquier sección):

```
Meeting:   <título descriptivo — no "Sync" ni "Check-in">
Date:      <YYYY-MM-DD>
Attendees: <nombres o roles, separados por coma>
```

Cuatro secciones:

1. **Agenda** — temas listados antes de la reunión. Un ítem por línea. Marcados con ✓ si se trataron, — si se aplazaron.
2. **Decisions** — lista con viñetas de decisiones discretas tomadas. Cada viñeta es autónoma y legible sin el contexto de las notas.
3. **Action items** — tabla: `Owner` \| `Action` \| `Due`. Una fila por ítem. `Due` es `TBD` si no se fijó fecha; nunca en blanco. "Alguien" no es un responsable aceptable.
4. **Notes** — opcional. Contexto que apoya las decisiones o elementos de acción. Comprimir agresivamente: tres oraciones suele ser suficiente.

## Registro

Las decisiones se expresan como hechos consumados. Los elementos de acción usan forma imperativa con un responsable específico. Las notas son mínimas en prosa: contexto, no transcripción.

## Véase también

- [[style-guide-ticket-comment|Guía de estilo — Comentario de ticket]]
- [[style-guide-memo|Guía de estilo — Memo]]
- [[language-protocol-substrate|Substrato del Protocolo de Lenguaje]]
