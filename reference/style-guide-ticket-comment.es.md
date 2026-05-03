---
schema: foundry-doc-v1
title: "Guía de estilo: Comentario de tíquet"
slug: style-guide-ticket-comment.es
category: reference
type: topic
quality: core
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
paired_with: style-guide-ticket-comment.md
---

Un **comentario de tíquet** es un registro duradero con conclusión al principio en un rastreador de incidencias, revisión de pull request, o hilo de soporte — escrito para una audiencia asincrónica que puede leerlo sin contexto años después de haberlo publicado.

Esta plantilla forma parte de la familia COMMS en el registro de plantillas de géneros de `service-disclosure`. Abarca comentarios en GitHub Issues, revisiones de PR, tíckets de soporte y hilos asincrónicos similares. A diferencia de las actas de reunión o los memos, un comentario de tíquet es simultáneamente el mensaje y el registro.

## Cuándo usar esta plantilla

Úsela cuando escriba un comentario que formará parte de un registro rastreado: una revisión de PR, una respuesta a un informe de error, una actualización de estado en un tíquet de soporte.

## Estructura: la conclusión primero

La plantilla no impone secciones fijas, pero sí un orden obligatorio:

1. **Lo que hizo o lo que propone** — la conclusión, en la primera oración; un revisor que lee diez comentarios debe poder leer solo la primera oración de cada uno y saber qué decidió cada comentarista
2. **El razonamiento** — el argumento de respaldo, con referencias específicas a commits, archivos y tíckets anteriores
3. **Preguntas abiertas** — elementos que el comentarista no pudo resolver y que necesita que el hilo aborde

## Convenciones de referencia

| Tipo de referencia | Formato |
|---|---|
| Commit | SHA corto en backticks: `` `4244a02` `` |
| Archivo y línea | Ruta:línea en backticks: `` `validate.rs:47` `` |
| Tíquet anterior | ID del rastreador: `#123` |
| PR | `PR #789` |

Evite resumir lo que dice el artefact enlazado; refiérase a él con precisión.

## Registro y tono

El registro es operacional. Longitud objetivo de oración: media de unas catorce palabras, máximo veintidós. Voz activa. Un comentario de tíquet es duradero: no escriba nada que no quisiera que un auditor o un nuevo miembro del equipo leyera sin contexto. Se aplica la lista global de vocabulario prohibido.

Los comentarios de tíquet son documentos internos; no se requiere par bilingüe.

## Véase también

- [[style-guide-meeting-notes|Guía de estilo: Actas de reunión]]
- [[style-guide-memo|Guía de estilo: Memo]]
- [[language-protocol-substrate|Sustrato de protocolo de lenguaje]]
