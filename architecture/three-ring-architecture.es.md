---
schema: foundry-doc-v1
title: "Arquitectura de Tres Anillos"
slug: three-ring-architecture.es
category: architecture
type: topic
quality: complete
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
paired_with: three-ring-architecture.md
---

## Adaptación estratégica — Arquitectura de Tres Anillos

La **Arquitectura de Tres Anillos** es el patrón de composición central de la plataforma PointSav. Organiza todos los servicios en uno de tres anillos con dependencias estrictas en una sola dirección. El anillo exterior incorpora inferencia de inteligencia artificial. Los dos anillos interiores — ingesta en el límite y conocimiento determinístico — operan plenamente sin ella.

Esta separación es una decisión estructural, no una preferencia de diseño. Un cliente que requiere un despliegue sin conexión de red externa puede ejecutar toda la cadena de datos en los anillos 1 y 2 con plena capacidad. Añadir el anillo 3 incorpora inteligencia sin modificar el modelo de datos, la trazabilidad de auditoría ni los límites de identidad que mantienen los anillos interiores.

## Los tres anillos

**Anillo 1 — Ingesta en el límite.** Cada servicio de este anillo acepta datos sin procesar de una fuente externa — sistema de archivos, bandeja de correo, carga de documentos, proveedor de identidad — y los escribe en un registro duradero. No hay transformación ni clasificación en el anillo 1; solo almacenamiento. Cada servicio implementa una interfaz MCP (Model Context Protocol), lo que permite añadir nuevas fuentes de datos como servidores MCP adicionales sin modificar los servicios existentes. Los datos de cada cliente residen en una instancia de servicio separada con su propio almacenamiento.

**Anillo 2 — Conocimiento y procesamiento.** Lee del anillo 1 y produce conocimiento estructurado: registros analizados, grafos de conocimiento, entidades clasificadas, índices de búsqueda. Todo el procesamiento del anillo 2 es determinístico. SYS-ADR-07 prohíbe que la IA escriba en el grafo de conocimiento o en los almacenes de registros estructurados. El efecto práctico: la salida del anillo 2 es reproducible dado el mismo input del anillo 1. Una auditoría puede reproducir el análisis determinístico contra el registro inmutable del anillo 1 y obtener el mismo resultado.

**Anillo 3 — Inteligencia opcional.** `service-slm` es el único servicio del anillo 3. Es solo lectura respecto al anillo 2 — nunca escribe en el grafo de conocimiento, el registro contable ni los almacenes estructurados. Implementa el patrón Doorman: cada solicitud entra por un único límite que sanea los datos salientes, enruta entre los tres niveles de cómputo (local, ráfaga de GPU, API externa) y registra cada llamada en el libro mayor de auditoría del cliente. Ninguna clave de API existe fuera del límite del Doorman.

## Por qué la IA es opcional por diseño

Los anillos 1 y 2 no tienen ningún import, dependencia ni llamada en tiempo de ejecución al anillo 3. Un despliegue que excluye el anillo 3 por completo opera con menos procesos, menos superficie de ataque y cumple los requisitos de aislamiento de red que prohíben llamadas a API externas. Para los despliegues que incluyen el anillo 3, la restricción de solo lectura garantiza que el núcleo determinístico siga siendo el registro autoritativo.

## Aislamiento multi-tenant

El aislamiento varía por anillo de forma deliberada: aislamiento duro por instancia de servicio en el anillo 1; aislamiento lógico por `moduleId` en el anillo 2; única instancia de `service-slm` con carga de adaptador LoRA por `moduleId` en el anillo 3. En ningún nivel hay un camino de código desde los datos de un tenant hasta los de otro.

La especificación técnica completa, incluyendo la taxonomía de servicios, las invariantes direccionales y el modelo de aislamiento, está disponible en inglés en el artículo principal.

## Véase también

- [[compounding-substrate]] — las cinco propiedades estructurales que implementa la Arquitectura de Tres Anillos
- [[service-slm]] — el servicio Doorman del anillo 3
- [[compounding-doorman]] — el patrón operativo que implementa el Doorman y por qué se compone con el tiempo
- [[worm-ledger-architecture]] — el registro inmutable de solo adición del anillo 1

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
