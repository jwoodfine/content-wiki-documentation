---
schema: foundry-doc-v1
title: "Motor GIS de PointSav"
slug: pointsav-gis-engine
category: services
type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: pointsav-gis-engine.md
cites:
  - maplibre-gl-js
  - pmtiles-spec
  - tippecanoe-tool
---

El Motor GIS de PointSav es una plataforma de Inteligencia de Ubicación de alto rendimiento y soberana, diseñada para operación offline-first con sustrato de archivos planos. Construido en Rust, representa un alejamiento estructural de los sistemas de información geográfica (SIG) tradicionales que dependen de instancias de bases de datos centralizadas.

## Sustrato de archivos planos

A diferencia de los sistemas GIS tradicionales que requieren gestión persistente de bases de datos, el motor de PointSav consume datos geográficos directamente desde formatos `JSONL`, `GeoParquet` y `YAML` versionados dentro de un Totebox Archive. Esta arquitectura garantiza que la capa de datos permanezca completamente desacoplada de la lógica de aplicación, eliminando la sobrecarga de mantenimiento de bases de datos y previniendo la dependencia de proveedores.

## Pila de renderizado soberana

La plataforma evita dependencias de SaaS de mapas comerciales utilizando una pila de renderizado de alto rendimiento y código abierto:

- **PMTiles** — un formato de archivo único para datos en teselas que permite servir mapas directamente desde servidores web estándar sin un servidor de teselas dedicado.
- **MapLibre GL JS** — una biblioteca basada en WebGL para renderizar mapas vectoriales interactivos con alto rendimiento del lado del cliente.
- **Tippecanoe** — una herramienta utilizada para compilar conjuntos de datos masivos de archivos planos en teselas vectoriales optimizadas.

## Procesamiento espacial

La lógica central del motor reside en el servicio `app-orchestration-gis`, que ejecuta deterministamente la metodología de co-ubicación de Woodfine para identificar y clasificar nodos comerciales en los mercados cubiertos.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
