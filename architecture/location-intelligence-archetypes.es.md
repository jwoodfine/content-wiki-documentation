---
schema: foundry-doc-v1
title: "Arquetipos de Inteligencia de Localización"
slug: location-intelligence-archetypes
category: architecture
type: concept
content_type: topic
quality: stub
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: TRANSLATE-ES
last_edited: 2026-06-20
editor: pointsav-engineering
paired_with: location-intelligence-archetypes.md
short_description: "Los arquetipos PRO, VWH y PKS clasifican las composiciones de anclas minoristas según su función dentro de un clúster de co-localización, proporcionando la taxonomía que impulsa el análisis GIS."
cites: []
---

Los arquetipos de inteligencia de localización son las etiquetas de clasificación asignadas a los inquilinos ancla dentro de un clúster de co-localización según su función en el ecosistema minorista. Los tres arquetipos principales — PRO (Profesional), VWH (Almacén) y PKS (Parque comercial) — describen el patrón de atracción comercial dominante de cada ancla y determinan cómo se puntúa el clúster en la [[location-intelligence-strategy|estrategia de inteligencia de localización]].

## PRO — Profesional

El arquetipo PRO identifica anclas cuya atracción principal son los servicios profesionales: bancos, clínicas, oficinas gubernamentales y franquicias de servicios profesionales. Las anclas PRO generan picos de tráfico peatonal correlacionados con el horario comercial.

## VWH — Almacén

El arquetipo VWH identifica anclas de gran formato que operan bajo el modelo de club de almacén o gran superficie: hipermercados, ferreterías de gran formato y clubes de compras al por mayor. Las anclas VWH generan el tráfico de consumidores de alto volumen y recurrente que constituye la base del modelo de co-localización.

## PKS — Parque comercial

El arquetipo PKS identifica anclas dentro de configuraciones de centro comercial cerrado o parque comercial, donde un único propietario controla la relación de co-tenencia entre las anclas. Los clústeres PKS exhiben patrones de arrendamiento y tráfico distintos a los clústeres de co-localización en parcelas abiertas.

## Taxonomía y flujo de datos

Cada ancla del conjunto de datos de puntos de interés es clasificada en uno de estos tres arquetipos durante la ejecución nocturna del pipeline. La composición de arquetipos resultante por clúster determina el nivel del clúster (T1, T2, T3) y alimenta las capas de teselas espaciales servidas por la superficie GIS.

## Véase también

- [[location-intelligence-strategy|Estrategia de Inteligencia de Localización]] — el marco estratégico que utiliza la taxonomía de arquetipos

*Woodfine Capital Projects™, MCorp™, PointSav Digital Systems™, Totebox Orchestration™, Totebox Archive™ y Capability Geometry™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos propietarios.*
