---
schema: foundry-doc-v1
title: "Guía de estilo: comentario de ticket"
slug: style-guide-ticket-comment.es
short_description: "Estándares editoriales para comentarios de ticket en la plataforma (género COMMS): disciplina de encabezado, estructura qué-cambió-y-qué-sigue, convenciones de campo de estado y cuándo comentar frente a cuándo actualizar la descripción del ticket."
category: reference
type: topic
content_type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-24
editor: pointsav-engineering
cites: []
paired_with: style-guide-ticket-comment.md
---

Un comentario de ticket registra un cambio de estado o una decisión, no un pensamiento. Todo comentario hace avanzar el ticket.

## Cuándo usar esta plantilla

Se escribe un comentario cuando el estado del trabajo cambió y los interesados necesitan saberlo, cuando se tomó una decisión que afecta al ticket, cuando se identificó o resolvió un bloqueo, o cuando se completó una acción y la finalización debe quedar registrada. No se comenta para decir que se está trabajando en el ítem: se actualiza el campo de estado.

## Estructura requerida

**Bloque de encabezado** (antes del cuerpo):

```
Ticket: <id o título del ticket>
Status: <nuevo estado — Open | In progress | Blocked | Review | Done>
```

Dos secciones:

1. **What changed** — uno a tres oraciones: el cambio específico en el estado, la decisión tomada o el hecho establecido. Nombra el artefacto, SHA de commit o decisión explícitamente.
2. **Next** — el siguiente paso concreto con responsable. Si el ticket está Done, "Next" es "Closed."

## Registro

Factual y breve. Tiempo pasado para lo que cambió; tiempo presente o futuro para los pasos siguientes. Sin conjeturas. Los valores del campo Status son un conjunto cerrado: `Open`, `In progress`, `Blocked`, `Review`, `Done`. Si "What changed" requiere más de tres oraciones, el cambio es suficientemente complejo para un brief o un [[style-guide-memo|memo]]; referenciar desde el comentario.

## Véase también

- [[style-guide-chat|Guía de estilo — Chat]]
- [[style-guide-meeting-notes|Guía de estilo — Notas de reunión]]
- [[language-protocol-substrate|Substrato del Protocolo de Lenguaje]]
