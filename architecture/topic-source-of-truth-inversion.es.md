---
schema: foundry-topic-v1
title: "Inversión de la fuente de verdad"
status: published
category: architecture
last_edited: 2026-04-30
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
language: es
companion: architecture/topic-source-of-truth-inversion.md
cites:
  - doctrine-claim-29
  - doctrine-claim-34
  - ni-51-102
---

## Descripción del patrón

La inversión de la fuente de verdad es un patrón de sustrato nombrado en Foundry. En cada aplicación de PointSav, una capa de almacenamiento se declara canónica — el registro autoritativo que se confirma en git, se firma, se replica y se divulga. Una segunda capa es una vista derivada: el índice en memoria del proceso en ejecución, la salida renderizada o el resumen computado — reconstruido de forma determinista desde el registro canónico bajo demanda y descartable sin pérdida de información. Una tercera capa, cuando la edición colaborativa está activa, es efímera de sesión: existe durante la duración de una sesión de edición compartida y no escribe de vuelta al canónico hasta que un autor humano realiza un commit deliberado.

El patrón se repite en el motor wiki, en la canalización de extracción de Ring 2, y en las aplicaciones planificadas `app-workplace-presentation` y `app-workplace-proforma`. En cada caso, la elección de qué es canónico sigue la misma lógica estructural: la capa con el mayor requisito de durabilidad, la obligación de auditoría más fuerte y la historia de replicación más limpia es la canónica. Todo lo demás es derivado.

## Por qué el patrón importa

En el motor wiki, git es canónico; el proceso en ejecución es una vista; la superposición CRDT de colaboración en tiempo real (planificada, desactivada por defecto) es efímera de sesión. El índice de búsqueda Tantivy, el grafo de wikilinks redb (planificado), y todo el HTML renderizado se derivan bajo demanda del árbol de Markdown en disco. Cualquiera de estos artefactos derivados puede descartarse y reconstruirse; ninguno se respalda ni se divulga. Lo que se respalda, replica, firma y divulga es el árbol git.

Para `service-extraction` (canalización de revisión multiautor de Ring 2), el registro canónico es el registro de eventos de extracción confirmado en el ledger WORM inmutable gestionado por `service-fs`. El ledger aplica un orden total sobre todos los eventos. La cola de revisión mostrada a cada revisor se deriva del conjunto de entradas del ledger que aún no han recibido un commit de veredicto. Esta derivación es determinista: el mismo ledger produce la misma cola en cada consulta.

## Postura de divulgación continua

En cada aplicación, lo canónico es el estado divulgado. Conforme a los requisitos de divulgación continua de [ni-51-102], el registro que se divulga es el que está firmado, confirmado y replicado — no la vista renderizada, no el índice de búsqueda, no el búfer CRDT efímero de sesión. La inversión de la fuente de verdad hace cumplir esto por construcción: el sustrato no puede divulgar accidentalmente un artefacto de capa de vista como autoritativo, porque la vista no es el registro por definición. La trazabilidad de auditoría para cualquier afirmación divulgada es un `git log`.

La reclamación #34 de Doctrine (Sustrato Soberano de Dos Fondos) establece que los mismos binarios `os-*` se ejecutan en ambos fondos del sustrato (seL4 nativo y NetBSD de compatibilidad). La consecuencia a nivel de aplicación es que el almacenamiento canónico debe ser agnóstico al kernel: un árbol git firmado y una entrada de ledger WORM firmada son registros válidos independientemente de qué kernel del sistema operativo ejecute el proceso de vista.

## Aplicaciones planificadas

Para las aplicaciones planificadas `app-workplace-presentation` (autoría colaborativa de presentaciones) y `app-workplace-proforma` (edición de tablas estructuradas en contextos de negocio regulados), el mismo mapeo de fuente de verdad se aplica: el repositorio git del cliente es canónico; la interfaz de usuario renderizada es una vista; el estado CRDT de colaboración durante sesiones compartidas es efímero de sesión. Nada persiste al registro canónico sin un commit explícito de un autor humano. Estas capas de colaboración son planificadas y no están implementadas al 2026-04-27.

## Véase también

- [[topic-app-mediakit-knowledge]] — Instancia base del patrón (git como canónico).
- [[collab-via-passthrough-relay]] — La capa efímera de sesión en detalle.
- [[topic-substrate-native-compatibility]] — Almacenamiento canónico agnóstico al kernel en el contexto de Sustrato Soberano de Dos Fondos.
- [[topic-disclosure-substrate]] — La convención de postura de divulgación que este patrón satisface.

## Procedencia

Vista general estratégica en español elaborada por project-language el 2026-04-30. Basada en el borrador de project-knowledge (sub-agente brief 03, 2026-04-28). Por DOCTRINE.md §XII, esta vista general no es una traducción literal — adapta el concepto central para lectores en español.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
