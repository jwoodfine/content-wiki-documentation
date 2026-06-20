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
short_description: "Los arquetipos PRO, VWH y PKS clasifican las composiciones de anclas minoristas según su función dentro de un clúster de co-localización, proporcionando la taxonomía que impulsa el análisis GIS. PRO designa Centros Minoristas, VWH designa Periferia Urbana y PKS designa ubicaciones de Transporte."
cites: []
---

Los arquetipos de inteligencia de localización son las etiquetas de clasificación asignadas a los inquilinos ancla dentro de un clúster de co-localización según su función en el ecosistema minorista. Los tres arquetipos principales — PRO (Centros Minoristas), VWH (Periferia Urbana) y PKS (Transporte) — describen el patrón de atracción comercial dominante de cada ancla y determinan cómo se puntúa el clúster en la estrategia de inteligencia de localización.

## PRO — Centros Minoristas

El arquetipo PRO identifica anclas de centros minoristas cuya atracción principal es el comercio minorista de consumo concentrado: centros comerciales, ejes comerciales urbanos y destinos de centro de ciudad. Las anclas PRO generan picos de tráfico peatonal correlacionados con el horario comercial minorista y tienden a agruparse en ubicaciones urbanas de mayor densidad.

## VWH — Periferia Urbana

El arquetipo VWH identifica anclas de gran formato en la periferia urbana que operan bajo el modelo de club de almacén o gran superficie: hipermercados, ferreterías de gran formato y clubes de compras al por mayor. Las anclas VWH generan el tráfico de consumidores de alto volumen y recurrente que constituye la base del modelo de co-localización.

## PKS — Transporte

El arquetipo PKS identifica anclas orientadas al transporte ubicadas en torno a corredores de tránsito y zonas de captación de aparcamientos disuasorios, donde la atracción está impulsada por los flujos de desplazamiento al trabajo más que por el comercio minorista de destino. Los clústeres PKS exhiben patrones de arrendamiento y tráfico distintos a los clústeres de co-localización en parcelas abiertas.

## Taxonomía y flujo de datos

Cada ancla del conjunto de datos de puntos de interés es clasificada en uno de estos tres arquetipos durante la ejecución nocturna del pipeline. La composición de arquetipos resultante por clúster determina el nivel del clúster (T1, T2, T3) y alimenta las capas de teselas espaciales servidas por la superficie GIS.

## Véase también

- Estrategia de Inteligencia de Localización — el marco estratégico que utiliza la taxonomía de arquetipos

*Woodfine Capital Projects™, MCorp™, PointSav Digital Systems™, Totebox Orchestration™, Totebox Archive™ y Capability Geometry™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos propietarios.*
