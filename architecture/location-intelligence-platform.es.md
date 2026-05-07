---
schema: foundry-doc-v1
title: "Plataforma de Inteligencia de Ubicación"
slug: location-intelligence-platform.es
category: architecture
type: topic
quality: core
status: active
language: es
bcsc_class: public-disclosure-safe
last_edited: 2026-05-07
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
paired_with: location-intelligence-platform.md
---

## Resumen estratégico

La Plataforma de Inteligencia de Ubicación de PointSav es un sistema de análisis de co-ubicación minorista que identifica y jerarquiza nodos inmobiliarios con base comercial defensible. La plataforma ingesta registros de ubicaciones de tiendas desde OpenStreetMap y la Fundación Overture Maps, aplica un modelo de anclas nominadas para puntuar cada ubicación y representa los resultados en un mapa interactivo por capas. Todos los datos, mosaicos y algoritmos son propiedad del cliente y operan en infraestructura del cliente, sin costes por solicitud. El primer despliegue en producción sirve `gis.woodfinegroup.com`.

## El Modelo de Anclas Nominadas

El modelo categoriza a los operadores de gran formato en tres niveles según su función comercial y radio de captación:

- **Objetivo Primario** — ancla fundamental del nodo. En Norteamérica, Walmart Supercentre. En los mercados europeos, IKEA opera como objetivo primario bajo la configuración de análisis actual.
- **Anclas Secundarias** — operadores complementarios en radio de 1,0 a 3,0 km: ferreterías de gran formato y clubes de almacén.
- **Anclas Terciarias** — infraestructura cívica e institucional en radio de 5,0 km: hospitales, centros médicos, universidades.

La metodología completa, incluidos los radios de captación y los equivalentes regionales de operadores, se documenta en [[co-location-methodology]].

## Modelo de puntuación V2

Los sitios se evalúan en una escala de 0 a 1.000 puntos y se clasifican en tres niveles de calidad:

| Nivel | Nombre | Umbral | Validación comercial |
|-------|--------|--------|---------------------|
| T3 | Apex | score_final ≥ 700 | Convergencia comercial absoluta; pequeña fracción del total. |
| T2 | Hub | score_final ≥ 450 | Emparejamiento comercial validado. |
| T1 | Valid | score_final ≥ 150 | Ancla + al menos un secundario confirmado. |

Un control de saturación por país evita la inflación de calificaciones: si los sitios T3 de cualquier país ISO superan el 5% del total evaluado, el umbral T3 sube en incrementos de 25 puntos hasta que la proporción caiga por debajo del límite.

## Soberanía de datos y stack de código abierto

Todos los componentes de la plataforma son propiedad del cliente: registros de cadenas minoristas en JSONL de archivo plano, datos de la Fundación Overture Maps, mosaicos PMTiles generados por Tippecanoe y servidos por nginx, y un pipeline Python abierto para el algoritmo de puntuación. Si el portal GIS no está disponible, los datos persisten en el Totebox Archive y pueden restaurarse en una instancia de repuesto. La arquitectura de archivo plano se documenta en [[location-intelligence-substrate]].

Todo el stack de mosaicos y renderizado usa licencias permisivas: MapLibre GL JS (BSD-3-Clause), PMTiles (Apache 2.0), Tippecanoe (BSD-2-Clause), DuckDB (Apache 2.0).

## Véase también

- [[co-location-methodology]] — metodología de anclas nominadas y definiciones de nivel
- [[location-intelligence-strategy]] — contexto de mercado y decisiones arquitectónicas
- [[location-intelligence-substrate]] — arquitectura de datos GIS de archivo plano
- [[app-orchestration-gis]] — aplicación de servicio GIS que opera la plataforma
- [[poi-data-schema]] — estructura de registros de datos minoristas e institucionales
