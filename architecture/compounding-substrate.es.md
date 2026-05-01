---
schema: foundry-doc-v1
title: "El Sustrato Compuesto"
slug: compounding-substrate.es
category: architecture
type: topic
quality: complete
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
paired_with: compounding-substrate.md
---

## Adaptación estratégica — El Sustrato Compuesto

El **Sustrato Compuesto** es el patrón arquitectónico que PointSav construye y administra. Su propósito es resolver una pregunta estructural: ¿cómo puede una plataforma de software permitir que cada cliente sea propietario de sus datos, opere en su propia infraestructura y componga inteligencia artificial según su criterio — sin dejar de beneficiarse del aprendizaje colectivo?

La respuesta se articula en cinco propiedades estructurales:

**Soberanía de sustrato.** Cada cliente es propietario de su pila completa: datos, cómputo, adaptadores y composición de despliegue. El código del sustrato es abierto y puede ser bifurcado. Los datos del cliente nunca abandonan la infraestructura que el cliente controla.

**Capa de inteligencia opcional.** La capa de datos determinística — sistemas de archivos, registros contables, grafos de conocimiento, índices de búsqueda — funciona plenamente sin cómputo de inteligencia artificial. La IA se incorpora cuando y donde el cliente lo decide, en el nivel que elija: modelo local en CPU, ráfaga de GPU, o API externa.

**Enrutamiento de cómputo en tres niveles.** Cuando opera la IA, enruta entre tres niveles bajo una política explícita por solicitud: local (coste marginal cero, localidad de datos completa), ráfaga de GPU (instancia efímera en la cuenta del cliente), y API externa (registrada en el registro de auditoría del cliente, no en el del proveedor).

**Composición federada.** Cada interacción operativa genera una señal de entrenamiento estructurada que se acumula en el corpus de aprendizaje de cada cliente. Periódicamente, quienes opten por la federación contribuyen señal destilada al curador (PointSav, en esta instancia). El curador incorpora la señal acumulada a un modelo base mejorado que regresa a todos los despliegues. Ningún dato bruto del cliente abandona su infraestructura.

**Preentrenamiento continuo como compuesta.** El curador incorpora la señal de federación en el preentrenamiento continuo del modelo base abierto (actualmente OLMo 3, licencia Apache 2.0) y redistribuye los pesos mejorados como nueva base del sustrato. Los adaptadores del cliente — capas LoRA con estilo, clasificación y voz propios — se recompilan contra la nueva base. El despliegue mejora sin que el cliente vuelva a pagar el trabajo, y sin que sus datos se muevan.

Este patrón es el compromiso estructural de la plataforma con un mercado que exige privacidad, residencia de datos y verificabilidad de auditoría. La especificación técnica completa está disponible en inglés en el artículo principal.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
