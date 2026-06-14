---
schema: foundry-doc-v1
title: "service-business — Agrupación comercial"
slug: service-business-clustering
short_description: "service-business convierte puntos de datos de venta minorista sin procesar en clústeres comerciales accionables aplicando un esquema espacial padre-hijo — así cuando múltiples operadores distintos comparten un único sitio físico, el motor GIS recibe una entidad comercial por sitio en lugar de varios puntos superpuestos."
category: services
type: topic
content_type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: service-business-clustering.md
cites: []
---

Los datos minoristas son inherentemente ruidosos — un único sitio comercial frecuentemente contiene múltiples puntos distintos, como una tienda ancla de gran formato, una farmacia integrada y una estación de combustible que comparten la misma zona de estacionamiento. **`service-business`** convierte esos puntos crudos en clústeres comerciales accionables utilizando un esquema espacial padre-hijo, de modo que el motor GIS recibe una entidad comercial unificada por sitio físico en lugar de varios registros superpuestos. El servicio itera el lago de datos crudos de `service-fs`, agrupa entidades que comparten una huella dentro de un umbral de proximidad de 100 m y asigna el ancla nombrada de mayor peso como el padre.

## Lógica de agrupación

`service-business` procesa nodos comerciales crudos de modo que el motor GIS produzca una única entidad comercial unificada por sitio físico.

## Índice espacial basado en cuadrícula

Para realizar esto a escala, el servicio utiliza un índice espacial basado en cuadrícula (aproximadamente 1 km de celdas). Itera a través del lago de datos crudo de `service-fs` y agrupa entidades que comparten una huella física dentro de un umbral de proximidad de 100 m.

## Esquema padre-hijo

- **Nodo padre** — el motor comercial primario: típicamente el ancla nombrada de mayor peso en el sitio.
- **Hijos (subentidades)** — operadores secundarios ubicados dentro del mismo nodo espacial.

## Salida de datos depurada

La salida es un archivo `cleansed-clusters.jsonl` refinado. Este conjunto de datos procesado es consumido por el `app-orchestration-gis` descendente para construir el índice de co-ubicación regional.

## Véase también

- [[app-orchestration-gis]]
- [[service-fs-data-lake]]
- [[service-places-filtering]]
