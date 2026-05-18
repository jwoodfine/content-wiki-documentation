---
schema: foundry-doc-v1
title: "Arquitectura de Tres Anillos"
slug: three-ring-architecture.es
short_description: "El patrón de composición duradero para la plataforma PointSav: tres anillos concéntricos con dependencias estrictamente unidireccionales, donde el anillo de IA es estructuralmente opcional y la canalización de datos determinista funciona completamente sin él."
category: architecture
type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: three-ring-architecture.md
---

Un despliegue regulado de PointSav puede operar sin ningún componente de inteligencia artificial — no mediante un parámetro de configuración, sino porque la arquitectura de la plataforma hace que la IA sea estructuralmente opcional desde el inicio. La Arquitectura de Tres Anillos organiza cada servicio en uno de tres anillos concéntricos con dependencias estrictas en una sola dirección. Los dos anillos interiores — ingesta en el límite y procesamiento determinístico del conocimiento — operan plenamente sin el anillo exterior, que añade inferencia de IA y puede excluirse por completo.

Esta disposición responde a una pregunta de cumplimiento que surge en toda adquisición regulada: ¿cómo verifica un comprador que la IA no ha tocado el registro autoritativo? La respuesta es arquitectónica, no procedimental. Los anillos 1 y 2 no tienen ningún import, dependencia ni llamada en tiempo de ejecución que llegue al anillo 3. Un despliegue que excluye el anillo 3 ejecuta menos procesos, expone menor superficie de ataque y cumple los requisitos de aislamiento de red habituales en operaciones financieras e inmobiliarias reguladas. Para los despliegues que incluyen el anillo 3, la restricción de solo lectura garantiza que el núcleo determinístico siga siendo el único registro autoritativo: las propuestas de IA solo entran en el registro después de que un humano las aprueba a través del punto de control obligatorio de la plataforma.

## Los tres anillos

**Anillo 1 — Ingesta en el límite.** Cada servicio de este anillo acepta datos sin procesar de una fuente externa — sistema de archivos, bandeja de correo, carga de documentos, proveedor de identidad — y los escribe en un registro duradero. No hay transformación ni clasificación en el anillo 1; solo almacenamiento. Cada servicio implementa una interfaz MCP (Model Context Protocol), lo que permite añadir nuevas fuentes de datos como servidores MCP adicionales sin modificar los servicios existentes. Los datos de cada cliente residen en una instancia de servicio separada con su propio almacenamiento.

**Anillo 2 — Conocimiento y procesamiento.** Lee del anillo 1 y produce conocimiento estructurado: registros analizados, grafos de conocimiento, entidades clasificadas, índices de búsqueda. Todo el procesamiento del anillo 2 es determinístico. Una de las [[architecture-decisions|decisiones de arquitectura vinculantes]] de la plataforma prohíbe que la IA escriba en el grafo de conocimiento o en los almacenes de registros estructurados. El efecto práctico: la salida del anillo 2 es reproducible dado el mismo input del anillo 1. Una auditoría puede reproducir el análisis determinístico contra el registro inmutable del anillo 1 y obtener el mismo resultado.

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
