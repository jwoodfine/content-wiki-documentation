---
schema: foundry-doc-v1
title: "Plataforma de inteligencia de ubicación"
slug: location-intelligence-platform.es
category: applications
type: topic
quality: complete
short_description: "La plataforma de Inteligencia de Ubicación de PointSav es una aplicación GIS de archivos planos propiedad del cliente diseñada para análisis de clústeres minoristas y selección estratégica de sitios — compuesta por app-orchestration-gis (el motor analítico) y pointsav-gis-engine (la capa de renderizado), con cada conjunto de datos, algoritmo y decisión de renderizado bajo el control directo del cliente."
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: TRANSLATE-ES
last_edited: 2026-05-08
editor: pointsav-engineering
paired_with: location-intelligence-platform.md
cites:
 - osm-odbl
 - overture-maps-cdla-2-0
 - ni-51-102
 - osc-sn-51-721
---

La plataforma de Inteligencia de Ubicación de PointSav es una aplicación GIS de archivos planos propiedad del cliente diseñada para análisis de clústeres minoristas y selección estratégica de sitios — compuesta por [[app-orchestration-gis]] (el motor analítico) y [[pointsav-gis-engine]] (la capa de renderizado), con cada conjunto de datos, algoritmo y decisión de renderizado bajo el control directo del cliente. La plataforma responde a una pregunta comercial fundamental — *¿qué nodos geográficos poseen la densidad validada por capital requerida para soportar desarrollo adyacente?* — transformando ubicaciones de tiendas en bruto en nodos comerciales accionables a través de la [[co-location-methodology]]. Todos los conjuntos de datos canónicos residen en un [[totebox-archive|Archivo Totebox]] como archivos planos JSONL y GeoParquet, aplicando la [[worm-ledger-design|disciplina del libro mayor WORM]] a los registros geoespaciales.

## Capacidades Operativas

La plataforma transforma los datos brutos de ubicación de tiendas en nodos comerciales accionables mediante la ejecución de la [Metodología de Co-ubicación](co-location-methodology). Responde a una pregunta comercial fundamental: *¿qué nodos geográficos poseen la densidad validada por capital necesaria para sustentar un desarrollo inmobiliario adyacente?*

### 1. Identificación de Clústeres
La plataforma calcula clústeres de co-ubicación alrededor de anclas principales (ej. Walmart Supercentres, IKEA) utilizando un algoritmo espacial determinista. Cada clúster se califica según la convergencia de operadores independientes y la infraestructura cívica de apoyo.

### 2. Interfaz Interactiva Multicapa
El mapa interactivo en [gis.woodfinegroup.com](https://gis.woodfinegroup.com) utiliza una arquitectura de tres capas:
- **Capa 1 — Puntos de Interés Globales:** Vista de más de 31,000 ubicaciones minoristas individuales.
- **Capa 2 — Clústeres de Co-ubicación:** La vista analítica principal, que codifica la fuerza del clúster mediante saturación visual y tamaño.
- **Capa 3 — Radios de Captación:** Visualización de los límites de proximidad (predeterminado 3.0 km) que definen el alcance del análisis de área de influencia.

## Arquitectura Soberana

La plataforma se adhiere a los principios de [[customer-hostability|soberanía de datos centrada en el cliente]] del [[pointsav-gis-engine|Motor GIS de PointSav]]:
- **Operación basada en Archivos Planos:** Los datos persisten como archivos JSONL y GeoParquet versionados en un [[totebox-archive|Archivo Totebox]].
- **Visualización con Estándares Abiertos:** Utiliza PMTiles y MapLibre GL JS para servir mapas vectoriales sin dependencias de APIs de terceros.

## Véase también

- [[app-orchestration-gis]] — el motor analítico sin estado que produce las clasificaciones de co-ubicación
- [[pointsav-gis-engine]] — la capa de renderizado que sirve los mosaicos vectoriales a la interfaz del mapa
- [[co-location-methodology]] — el algoritmo de puntuación y clasificación que sustenta el análisis de clústeres
- [[location-intelligence-ux]] — la filosofía de diseño UX para la superficie del mapa interactivo
- [[totebox-archive]] — el archivo de archivos planos que contiene todos los datos geoespaciales canónicos
