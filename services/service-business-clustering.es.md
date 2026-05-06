---
schema: foundry-doc-v1
title: "service-business — Agrupación Comercial"
slug: service-business-clustering
category: services
type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: service-business-clustering.md
cites: []
## Véase también

- [[app-orchestration-gis]]
- [[service-fs-data-lake]]
- [[service-places-filtering]]

---

`service-business` es la capa de inteligencia responsable de transformar puntos de datos minoristas crudos en clústeres comerciales accionables. Implementa un patrón de agrupación padre-hijo para manejar entornos minoristas físicos complejos donde múltiples operadores distintos comparten un único nodo comercial.

## El problema de los datos minoristas

Los datos minoristas son inherentemente ruidosos. Un único nodo comercial frecuentemente contiene múltiples puntos distintos — por ejemplo, una tienda ancla de gran formato, una farmacia integrada y una estación de combustible en la misma área de estacionamiento. `service-business` procesa estos puntos de modo que el motor GIS produzca una única entidad comercial unificada por sitio físico.

## Índice espacial basado en cuadrícula

Para realizar esto a escala, el servicio utiliza un índice espacial basado en cuadrícula (aproximadamente 1 km de celdas). Itera a través del lago de datos crudo de `service-fs` y agrupa entidades que comparten una huella física dentro de un umbral de proximidad de 100 m.

## Esquema padre-hijo

- **Nodo padre** — el motor comercial primario: típicamente el ancla nombrada de mayor peso en el sitio.
- **Hijos (subentidades)** — operadores secundarios ubicados dentro del mismo nodo espacial.

## Salida de datos depurada

La salida es un archivo `cleansed-clusters.jsonl` refinado. Este conjunto de datos procesado es consumido por el `app-orchestration-gis` descendente para construir el índice de co-ubicación regional.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
