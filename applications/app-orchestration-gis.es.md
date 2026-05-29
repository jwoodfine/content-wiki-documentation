---
schema: foundry-doc-v1
title: "Aplicación de orquestación GIS"
slug: app-orchestration-gis.es
category: applications
type: topic
quality: complete
status: active
audience: public
short_description: "app-orchestration-gis es el motor de análisis espacial sin estado que realiza cálculos de geometría lineal y mapeo de coordenadas para producir las clasificaciones de co-ubicación de Woodfine y el mapa interactivo en gis.woodfinegroup.com — una función pura que no contiene datos canónicos y puede ser reprovisionada apuntando una nueva instancia a la capa de datos inmutable."
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-08
editor: pointsav-engineering
paired_with: app-orchestration-gis.md
cites:
 - pmtiles-spec
 - maplibre-gl-js
---

`app-orchestration-gis` es el motor de análisis espacial sin estado que realiza cálculos de geometría lineal y mapeo de coordenadas para producir las clasificaciones de co-ubicación de Woodfine y el mapa interactivo en [gis.woodfinegroup.com](https://gis.woodfinegroup.com). La aplicación no contiene datos canónicos — opera como una función pura desde archivos de clúster depurados hacia mosaicos geográficos clasificados, de modo que una instancia perdida puede reprovisionarse apuntando un nuevo proceso a la capa de datos inmutable [[totebox-archive|del Archivo Totebox]] sin migración de estado. Se ejecuta sobre [[os-orchestration|`os-orchestration`]] y se compone con [[service-business-clustering]] y [[service-places-filtering]] para producir sus conjuntos de datos de entrada.

## Posición estructural

La aplicación opera como la capa de análisis determinista entre el lago de datos soberano y la interfaz visual. Cada ejecución produce un artefacto reproducible: dado el mismo conjunto de datos de entrada, el índice resultante es idéntico. Esta garantía de reproducibilidad sustituye la dependencia de servicios de análisis gestionados por terceros.

## Metodología de análisis

El motor ejecuta tres pasadas de proximidad espacial — radios de 1,0 km, 3,0 km y 5,0 km — aplicando la matriz de 12 anclas nominadas para generar rangos de calidad de sitio. Los sitios se clasifican del Nivel 1 al Nivel 5 según la convergencia de capital validado en cada nodo comercial.

## Pila de renderizado soberana

La salida se entrega como archivos PMTiles — un formato de archivo plano que elimina la necesidad de un servidor de teselas dedicado. MapLibre GL JS renderiza los resultados directamente en el navegador con alto rendimiento WebGL, sin dependencias de servicios de mapeo SaaS comerciales.

## Diseño sin estado

La arquitectura de la aplicación es completamente sin estado: no persiste datos entre ejecuciones. Todo el estado reside en el archivo PMTiles de salida, versionado en el [[totebox-archive|Archivo Totebox]]. Esto permite re-provisionar el entorno GIS completo de forma instantánea desde la capa de datos inmutable, aplicando la [[co-location-methodology|metodología de co-ubicación]] de forma reproducible.

## Véase también

- [[pointsav-gis-engine]] — la capa de renderizado que sirve los mosaicos producidos por este motor
- [[service-business-clustering]] — el servicio de agrupamiento que forma los clústeres de co-ubicación
- [[service-places-filtering]] — el servicio de filtrado que prepara los datos de entrada depurados
- [[co-location-methodology]] — la metodología de puntuación y clasificación implementada por el motor
- [[location-intelligence-platform]] — el artículo de plataforma que cubre el despliegue GIS completo
