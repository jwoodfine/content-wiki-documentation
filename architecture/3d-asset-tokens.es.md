---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: 3d-asset-tokens
short_description: "La unidad de datos almacenados en el Totebox Archive, que combina una carga útil binaria inmutable, un esqueleto de metadatos legible por máquina y una conexión gráfica taxonómica dinámica que codifica la procedencia y el contexto."
title: Token de activo tridimensional
category: architecture
language: es
paired_with: 3d-asset-tokens.md
status: stub
last_edited: 2026-05-07
editor: pointsav-engineering
---

Un token de activo tridimensional es la unidad de datos almacenados del Archivo Totebox, que combina una carga binaria inmutable, un esqueleto de metadatos legible por máquina y una conexión al grafo taxonómico activo que codifica la procedencia y el contexto.

## Estructura

Cada token tiene tres componentes: una carga útil binaria de escritura única y dirección por contenido; un esqueleto de metadatos con campos validados por esquema que describen el tipo de contenido, la procedencia y la propiedad; y una conexión al grafo que vincula el token a su posición en la jerarquía taxonómica mantenida por el servicio de grafo de conocimiento.

Los tres componentes — carga útil, metadatos y posición en el grafo — se escriben juntos como un registro atómico único. Ningún componente existe de forma aislada dentro del archivo.

## Véase también

- [[totebox-archive|Archivo Totebox]] — el registro WORM que almacena los tokens de activo tridimensional
- [[worm-ledger-architecture|Arquitectura del Registro WORM]] — el modelo de almacenamiento de solo adición subyacente
