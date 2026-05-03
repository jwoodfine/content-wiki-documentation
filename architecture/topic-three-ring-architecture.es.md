---
title: "Arquitectura de Tres Anillos"
slug: topic-three-ring-architecture.es
category: architecture
status: stable
last_edited: 2026-04-30
editor: pointsav-engineering
quality: complete
---

El patrón arquitectónico duradero para la composición de servicios de PointSav: tres anillos con dependencias unidireccionales, donde el anillo de IA es estructuralmente opcional. El patrón permite el desarrollo paralelo, la productización por composición de nivel cliente y el desacoplamiento natural a medida que los servicios maduran.

Esta es la reclamación de Doctrina #16.

## Los tres anillos

**Anillo 1 — Ingestión de Frontera (por inquilino).** service-people, service-email, service-input y service-fs (Libro Mayor Inmutable WORM). Los datos entran; el anillo no depende de ningún otro anillo.

**Anillo 2 — Conocimiento y Procesamiento.** service-extraction (análisis determinista, sin IA), service-content (grafo de conocimiento LadybugDB), service-search (índice Tantivy) y service-egress. El núcleo determinista; depende solo del Anillo 1.

**Anillo 3 — Inteligencia Opcional.** service-slm (Portero) + Yo-Yo. Solo consulta el Anillo 2; nunca es necesario para que los Anillos 1+2 funcionen.

## El principio de capa de inteligencia opcional

La tubería de datos determinista (Anillos 1+2) es totalmente funcional sin IA. El nivel Comunidad distribuye los Anillos 1+2 solo — plataforma de datos completa sin cómputo de IA. El nivel Cliente PYME añade el Anillo 3. Los clientes pueden añadir o eliminar el Anillo 3 sin tocar los Anillos 1+2.

## Disciplina moduleId

`moduleId` es el primitivo multi-inquilino. Cada llamada lleva un `moduleId`; la lógica de enrutamiento aísla a los inquilinos en cada anillo: instancia de servicio por inquilino en el Anillo 1; multi-inquilino via moduleId en el Anillo 2; instancia única de service-slm con carga de LoRA por moduleId en el Anillo 3.

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ y Foundry™ son marcas no registradas de Woodfine Capital Projects Inc.
