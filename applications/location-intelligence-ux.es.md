---
schema: foundry-doc-v1
title: "Filosofía de diseño UX de inteligencia de ubicación"
slug: location-intelligence-ux
category: applications
type: topic
content_type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: TRANSLATE-ES
last_edited: 2026-05-19
editor: pointsav-engineering
short_description: "La interfaz de Inteligencia de Ubicación de PointSav está diseñada para priorizar la claridad en la toma de decisiones, utilizando una filosofía de conclusión primero que comunica la confianza en la selección de sitios mediante jerarquía visual y clasificación estructural."
paired_with: location-intelligence-ux.md
---

La interfaz de la [[location-intelligence-platform]] de PointSav está diseñada para priorizar la claridad en la toma de decisiones por encima del volumen de datos brutos. Utilizando una filosofía de conclusión primero, la plataforma comunica la confianza en la selección de sitios mediante jerarquía visual y clasificación estructural, aplicando la [[co-location-methodology|metodología de co-ubicación]] como unidad analítica principal.

## Puntos clave

- El principio de conclusión primero significa que la interfaz comunica la confianza en la selección de sitios — no el volumen de datos brutos. La codificación por grados de nivel y rampa de color le indica al tomador de decisiones en qué actuar antes de leer cualquier etiqueta de datos.
- El Grado de Clúster es la unidad visual y analítica principal. A diferencia de los productos GIS comerciales que muestran puntos de interés individuales por defecto, la plataforma renderiza los grados de nivel de co-ubicación como la capa base del mapa. Esta elección estructural codifica la confianza (convergencia validada por capital) en lugar de la simple presencia.
- Al hacer clic en un clúster se abre un panel lateral, no una ventana modal. Esto preserva el contexto del mapa mientras entrega el ranking municipal, los operadores presentes y los recuentos de apoyo institucional. La distinción es deliberada: los tomadores de decisiones comparan clústeres en el mapa; una modal rompe ese flujo al ocultar el contexto espacial.
- La interfaz está construida sobre [[app-orchestration-gis]] (motor analítico) y [[pointsav-gis-engine]] (capa de renderizado). Estos componentes están diseñados para el re-aprovisionamiento entre despliegues, no como un front end de instancia única.

## Diferenciación: el grado de clúster como unidad primaria

A diferencia de los productos GIS comerciales que muestran puntos individuales por defecto, la plataforma de PointSav utiliza el **Grado de Clúster** como la unidad visual y analítica principal:

1. **Rampa de confianza:** Los sitios se codifican mediante una rampa de color de un solo tono (desde el ámbar pálido hasta el intenso). Los marcadores más oscuros y grandes indican mayores niveles de convergencia de capital.
2. **Jerarquía estructural:** La interfaz guía al usuario hacia los nodos comerciales más defendibles, haciendo que los sitios Tier 5 y Tier 4 dominen la vista nacional.
3. **Tarjetas de índice contextuales:** Al hacer clic en un clúster, se activa un panel lateral — no una ventana modal — que proporciona el ranking municipal, los operadores presentes y el recuento de apoyo institucional sin perder el contexto del mapa.

## Arquitectura de componentes

La superficie GIS utiliza un conjunto de componentes estandarizado construido sobre [[app-orchestration-gis]] (el motor analítico) y [[pointsav-gis-engine]] (la capa de renderizado), diseñado para un re-aprovisionamiento rápido entre despliegues.

## Véase también

- [[location-intelligence-platform]] — el artículo de plataforma completo que cubre los fundamentos de datos y la arquitectura soberana
- [[app-orchestration-gis]] — el motor analítico que produce los grados de clúster visualizados en la interfaz
- [[pointsav-gis-engine]] — la capa de renderizado que sirve los mosaicos vectoriales a la superficie del mapa
- [[co-location-methodology]] — la metodología de puntuación y clasificación visualizada por la interfaz
