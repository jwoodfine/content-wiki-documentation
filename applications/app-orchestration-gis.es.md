---
schema: foundry-doc-v1
title: "app-orchestration-gis"
slug: app-orchestration-gis
category: applications
type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: app-orchestration-gis.md
cites:
  - pmtiles-spec
  - maplibre-gl-js
---

`app-orchestration-gis` es el motor de procesamiento geoespacial que transforma datos sin procesar de operadores minoristas e infraestructura cívica en índices de co-ubicación por niveles, listos para renderizado en la interfaz de inteligencia de ubicación de PointSav.

## Posición estructural

La aplicación opera como la capa de análisis determinista entre el lago de datos soberano y la interfaz visual. Cada ejecución produce un artefacto reproducible: dado el mismo conjunto de datos de entrada, el índice resultante es idéntico. Esta garantía de reproducibilidad sustituye la dependencia de servicios de análisis gestionados por terceros.

## Metodología de análisis

El motor ejecuta tres pasadas de proximidad espacial — radios de 1,0 km, 3,0 km y 5,0 km — aplicando la matriz de 12 anclas nominadas para generar rangos de calidad de sitio. Los sitios se clasifican del Nivel 1 al Nivel 5 según la convergencia de capital validado en cada nodo comercial.

## Pila de renderizado soberana

La salida se entrega como archivos PMTiles — un formato de archivo plano que elimina la necesidad de un servidor de teselas dedicado. MapLibre GL JS renderiza los resultados directamente en el navegador con alto rendimiento WebGL, sin dependencias de servicios de mapeo SaaS comerciales.

## Diseño sin estado

La arquitectura de la aplicación es completamente sin estado: no persiste datos entre ejecuciones. Todo el estado reside en el archivo PMTiles de salida, versionado en el Totebox Archive. Esto permite re-provisionar el entorno GIS completo de forma instantánea desde la capa de datos inmutable.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™ y Totebox Archive™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos dueños.*
