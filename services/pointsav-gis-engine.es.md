---
schema: foundry-doc-v1
title: "Motor GIS de PointSav"
slug: pointsav-gis-engine.es
category: services
type: topic
content_type: topic
quality: complete
status: active
audience: public
short_description: "El Motor GIS de PointSav es una plataforma de inteligencia de ubicación de alto rendimiento y propiedad del cliente construida en Rust para operación offline-first sobre archivos planos — una desviación estructural de los sistemas de información geográfica tradicionales que dependen de instancias de bases de datos centralizadas y conectividad de red continua."
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-08
editor: pointsav-engineering
paired_with: pointsav-gis-engine.md
cites:
 - maplibre-gl-js
 - pmtiles-spec
 - tippecanoe-tool
---

El Motor GIS de PointSav es una plataforma de inteligencia de ubicación de alto rendimiento y propiedad del cliente construida en Rust para operación offline-first sobre archivos planos — una desviación estructural de los sistemas de información geográfica tradicionales que dependen de instancias de bases de datos centralizadas y conectividad de red continua. El motor lee desde un archivo PMTiles estático en el [[service-fs-data-lake|sistema de archivos del propio cliente]], renderiza interactivamente a través de MapLibre GL JS en el navegador y sirve cada consulta sin una dependencia externa. Los datos del mapa viven en el archivo del cliente; nada sale del despliegue a menos que el operador elija explícitamente publicar.

## Sustrato de archivos planos

A diferencia de los sistemas GIS tradicionales que requieren gestión persistente de bases de datos, el motor de PointSav consume datos geográficos directamente desde formatos `JSONL`, `GeoParquet` y `YAML` versionados dentro de un Totebox Archive. Esta arquitectura garantiza que la capa de datos permanezca completamente desacoplada de la lógica de aplicación, eliminando la sobrecarga de mantenimiento de bases de datos y previniendo la dependencia de proveedores.

## Pila de renderizado soberana

La plataforma evita dependencias de SaaS de mapas comerciales utilizando una pila de renderizado de alto rendimiento y código abierto:

- **PMTiles** — un formato de archivo único para datos en teselas que permite servir mapas directamente desde servidores web estándar sin un servidor de teselas dedicado.
- **MapLibre GL JS** — una biblioteca basada en WebGL para renderizar mapas vectoriales interactivos con alto rendimiento del lado del cliente.
- **Tippecanoe** — una herramienta utilizada para compilar conjuntos de datos masivos de archivos planos en teselas vectoriales optimizadas.

## Procesamiento espacial

La lógica central del motor reside en el servicio [[app-orchestration-gis]], que ejecuta deterministamente la [[co-location-methodology|metodología de co-ubicación de Woodfine]] para identificar y clasificar nodos comerciales en los mercados cubiertos a partir de datos de [[service-business-clustering]] y [[service-places-filtering]].

## Véase también

- [[co-location-methodology]] — la metodología de clasificación que impulsa la asignación de nivel en el motor GIS
- [[app-orchestration-gis]] — la capa de orquestación que ejecuta el pipeline de análisis espacial
- [[service-business-clustering]] — servicio de agrupación minorista que alimenta el cálculo de nivel GIS
- [[service-places-filtering]] — servicio de filtrado de infraestructura cívica que alimenta el cálculo de nivel GIS
- [[service-fs-data-lake]] — el lago de datos de archivos planos que respalda todos los datos de origen GIS
