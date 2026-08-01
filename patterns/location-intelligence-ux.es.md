---
schema: foundry-doc-v1
title: "Filosofía de diseño UX de inteligencia de ubicación"
slug: location-intelligence-ux
aliases:
  - location-intelligence-ux
category: patterns
type: topic
content_type: topic
quality: complete
short_description: "Filosofía de interfaz Conclusion-First que renderiza conclusiones clasificadas en lugar de puntos de datos, destacando de inmediato los nodos comerciales defendibles."
status: active
audience: public
bcsc_class: no-disclosure-implication
language_protocol: TRANSLATE-ES
last_edited: 2026-08-01
editor: pointsav-engineering
paired_with: location-intelligence-ux.md
---

La interfaz de [[location-intelligence-platform|Inteligencia de Ubicación]] de PointSav utiliza una filosofía de diseño Conclusion-First — renderizando conclusiones de nivel clasificadas en lugar de puntos de datos individuales — de modo que un usuario que compara mercados a nivel de zoom nacional ve los nodos comerciales más defendibles de inmediato, y solo profundiza en operadores individuales cuando un nodo ha ganado la atención. La superficie [[app-orchestration-gis|de orquestación GIS]] entrega este diseño a escala de producción.

## Diferenciación: El Grado de Clúster como Unidad Primaria

A diferencia de los productos GIS comerciales que muestran puntos individuales por defecto, la plataforma de PointSav utiliza el **Grado de Clúster** como la unidad visual y analítica principal:

1. **Rampa de Confianza:** Los sitios se codifican mediante una rampa de color (desde el ámbar pálido hasta el intenso). Los marcadores más oscuros y grandes indican mayores niveles de convergencia de capital.
2. **Jerarquía Estructural:** La interfaz guía al usuario hacia los nodos comerciales más defendibles, haciendo que los sitios Tier 5 y Tier 4 dominen la vista nacional.
3. **Tarjetas de Índice Contextuales:** Al hacer clic en un clúster, se activa un panel lateral que proporciona metadatos inmediatos (ranking municipal, operadores presentes) sin perder el contexto del mapa.

## Véase también

- [[location-intelligence-platform]] — la plataforma de inteligencia de ubicación que estos patrones UX sirven
- [[app-orchestration-gis]] — la superficie de orquestación GIS que implementa este diseño
- [[retail-co-location-tier-methodology]] — la metodología de niveles que produce las conclusiones de nivel mostradas

---
## Procedencia
- **Adaptación Estratégica:** Basada en el documento inglés `location-intelligence-ux.md`.
- **Refinement:** 2026-05-02 por project-language Task.
