---
schema: foundry-doc-v1
title: "El Sustrato de Cola de Briefs"
slug: brief-queue-substrate.es
category: architecture
type: topic
quality: core
short_description: "Una cola persistente respaldada en archivos que hace viable el apagado inactivo de Yo-Yo sin perder datos del corpus de aprendizaje — la capa de durabilidad del sustrato SLM de tres niveles."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
paired_with: brief-queue-substrate.md
---

El **Sustrato de Cola de Briefs** es una cola persistente respaldada en archivos que conecta el flujo editorial de la plataforma PointSav con el sistema de captura del corpus de aprendizaje. Su propósito central es recibir registros de ejecución de briefs — eventos en formato JSON Lines que describen una operación editorial — y conservarlos de forma confiable hasta que el proceso de vaciado pueda escribirlos en el corpus a largo plazo.

## El problema que resuelve

El nivel de cómputo Yo-Yo (OLMo 3.1 32B Think en GPU en ráfaga) se apaga automáticamente tras un período de inactividad para evitar costos innecesarios. Sin la cola, cualquier evento generado durante una sesión Yo-Yo tendría que escribirse sincrónicamente en el corpus antes del apagado, acoplando el bucle de inferencia del modelo de lenguaje a operaciones de disco. Con la cola, el bucle de inferencia escribe un archivo ligero en el directorio `queue/` y continúa; el proceso de vaciado gestiona la persistencia del corpus de forma independiente. El apagado puede ocurrir en cuanto termina la inferencia, sin eventos pendientes.

El mismo mecanismo absorbe los eventos de apropiación de instancias spot en proveedores de nube: los archivos en `queue/` y `queue-in-flight/` sobreviven a la apropiación porque residen en almacenamiento persistente, no en el almacenamiento efímero de la instancia.

## Cómo funciona

La cola es un conjunto de cuatro directorios que funcionan como una máquina de estados para archivos de eventos JSONL:

- **`queue/`** — los eventos entrantes llegan aquí sin necesidad de bloqueo.
- **`queue-in-flight/`** — el proceso de vaciado renombra atómicamente un archivo desde `queue/` a este directorio al comenzar a procesarlo. Si el proceso falla, el archivo permanece aquí y se recupera al reiniciar.
- **`queue-done/`** — tras escribir exitosamente el evento en el corpus, el archivo se mueve aquí.
- **`queue-poison/`** — los archivos que fallan en validación o agotan los reintentos se mueven aquí para revisión manual.

El patrón de arrendamiento por renombre atómico garantiza que exactamente un proceso de vaciado adquiera cada archivo, incluso con múltiples consumidores concurrentes.

## Por qué archivos JSONL y no un broker de mensajes

La elección de archivos JSONL locales en lugar de un broker como NATS JetStream o Redis Streams responde al principio de soberanía de la plataforma: el productor de la cola, el consumidor y el almacenamiento del corpus residen en la misma máquina o volumen persistente en la nube. Un broker de red añadiría latencia y un modo de fallo sin aportar una capacidad que la plataforma requiera a esta escala. Los archivos JSONL son directamente inspeccionables con cualquier editor de texto, alineados con el Pilar 1 de la Doctrina PointSav: solo texto plano.

## Estado de implementación

La convención del Sustrato de Cola de Briefs fue ratificada en la versión v0.1.78 del workspace. La implementación — API de cola, proceso de vaciado en el Doorman, y graduación del hook post-commit — está en curso bajo el ámbito del cluster project-slm. El formato del corpus JSONL no cambia; solo el camino de escritura.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
