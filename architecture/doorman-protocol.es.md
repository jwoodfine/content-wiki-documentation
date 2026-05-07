---
schema: foundry-doc-v1
title: "Protocolo Doorman"
slug: doorman-protocol
category: architecture
status: stub
bcsc_class: current-fact
last_edited: 2026-04-28
editor: pointsav-engineering
language: es
paired_with: doorman-protocol.md
cites:
  - doctrine-claim-1
---

El Protocolo Doorman describe la disciplina de enrutamiento y auditoría implementada por `service-slm`, el único servicio en el Anillo 3 de la [[three-ring-architecture]]. Toda llamada de inferencia que sale de un Totebox pasa por un único servicio en un único límite — el Doorman — que aplica la disciplina sanitizar-y-rehidratar, enruta al nivel de cómputo apropiado y registra cada evento en un libro de auditoría inmutable.

## Por qué un Doorman

El problema del límite: un Totebox contiene los datos estructurados autorizados del cliente; el cómputo externo (los grandes modelos de lenguaje) no puede recibir esos datos sin procesamiento previo. Sin un único límite, cada servicio del Totebox desarrolla su propia ruta de salida, cada ruta necesita su propia auditoría, y la disciplina sanitizar-y-rehidratar (SYS-ADR-07) se convierte en disciplina por servicio en lugar de disciplina de sustrato.

## Enrutamiento de cómputo en tres niveles

El Doorman enruta las llamadas de inferencia en tres niveles:

**Nivel A — Local.** Se ejecuta en la VM del servidor usando CPU y RAM. Para inferencia local en el modelo alojado (`OLMo-2-0425-1B-Instruct` en el despliegue de referencia). El Nivel A es operativamente verificado.

**Nivel B — Grupo Yo-Yo (previsto).** Enruta cargas de trabajo a instancias GPU dedicadas en Google Cloud Platform, que se inician bajo demanda y se detienen en reposo. El enrutamiento al Nivel B está previsto; no está operativo hoy.

**Nivel C — Proxy de API externa (previsto).** Enruta tareas especializadas de refinamiento lingüístico a modelos fronteras externos. El Doorman aplica límites de coste e inyecta ontologías de contenido de servicio predefinidas.

## El libro de auditoría

Cada llamada de inferencia produce una entrada JSONL en un archivo diario de solo adición. Campos requeridos: marca de tiempo, ID de solicitud, ID de módulo, nivel, modelo, duración de inferencia, estimación de coste, indicador de sanitización y estado de finalización.

## La disciplina de moduleId

Un único campo `moduleId` cumple cinco funciones: selecciona la unidad systemd; delimita bloques de caché Mooncake KV; circunscribe los recorridos del grafo LadybugDB al arrendatario correcto; selecciona la pila de adaptadores LoRA; y etiqueta las entradas del libro de auditoría para la contabilidad de costes por proyecto.

## Enrutamiento del Substrato de Aprendizaje

El Doorman implementa la inversión de polaridad del [[apprenticeship-substrate]] para trabajo con forma de código y editorial: `service-slm` intenta primero; la sesión senior revisa. Cada veredicto firmado se captura en el corpus de aprendizaje como una tupla de entrenamiento.

## Véase también

- [[compounding-doorman]] — descripción conceptual del Doorman como patrón de sustrato de IA soberana
- [[apprenticeship-substrate]] — la inversión de enrutamiento y el protocolo de firma de veredictos
- [[three-ring-architecture]] — el Doorman es el único servicio del Anillo 3

## Referencias

- **Afirmación doctrinal #1** — El Límite Soberano. Foundry DOCTRINE.md v0.1.0.
- **`conventions/llm-substrate-decision.md`** — registro de decisión para la arquitectura de enrutamiento en tres niveles.
- **`service-slm/ARCHITECTURE.md`** — especificación de implementación completa del servicio Doorman.
