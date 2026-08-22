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
index_group: interface-and-user-experience
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

## Diferenciación de diseño: el grado de clúster como unidad primaria

A diferencia de los productos GIS comerciales que muestran puntos individuales por defecto, la plataforma de PointSav utiliza el **grado de clúster** como la unidad visual y analítica principal. **Un usuario que examina el mapa nacional ve qué clústeres merecen su atención antes de ver cualquier sitio individual.** El mapa responde primero la pregunta de clasificación, no al final. Esta diferenciación refleja tres decisiones:

1. **Codificación por color multi-tono.** Los sitios se codifican en cuatro niveles — Regional, Distrital, Local y Periférico — cada uno con un tono de color distinto, no con un solo degradado. El usuario distingue niveles por familia de color, no juzgando la intensidad de la sombra.
2. **Jerarquía estructural.** La interfaz guía al usuario hacia los nodos comerciales más defendibles, haciendo que los niveles Regional y Distrital dominen la vista nacional antes de que los niveles inferiores compitan por la atención.
3. **Panel contextual, no una ventana modal.** Al hacer clic en un clúster se abre un panel lateral con ranking municipal inmediato, detalle de operadores y conteos de respaldo institucional, sin perder el contexto del mapa detrás del panel.

## Arquitectura de componentes

El inspector de clústeres de la superficie GIS es un componente de panel (nombrado internamente "BentoBox") que renderiza los metadatos de nivel de clúster en un diseño denso y legible sin que el usuario tenga que abandonar la vista de mapa.

## Véase también

- [[location-intelligence-platform]] — la plataforma de inteligencia de ubicación que estos patrones UX sirven
- [[app-orchestration-gis]] — la superficie de orquestación GIS que implementa este diseño
- [[retail-co-location-tier-methodology]] — la metodología de niveles que produce las conclusiones de nivel mostradas

---
## Procedencia
- **Adaptación Estratégica:** Basada en el documento inglés `location-intelligence-ux.md`.
- **Refinement:** 2026-05-02 por project-language Task.
