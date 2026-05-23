---
schema: foundry-doc-v1
title: "service-fs — Lago de datos GIS"
slug: service-fs-data-lake
short_description: "service-fs es la capa de almacenamiento fundamental para la canalización GIS de la plataforma — un lago de datos de archivos planos que almacena puntos geoespaciales sin procesar ingeridos de fuentes abiertas en zonas de aterrizaje separadas de venta minorista y cívicas, disponibles inmediatamente para cada servicio descendente sin un paso ETL."
category: services
type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-08
editor: pointsav-engineering
paired_with: service-fs-data-lake.md
cites: []
---

**`service-fs`** es la capa de almacenamiento fundacional para la canalización GIS de la plataforma — un lago de datos en archivos planos que almacena puntos geoespaciales en bruto ingeridos desde fuentes abiertas (OpenStreetMap, Overture Maps Foundation) en zonas de aterrizaje separadas para datos minoristas y cívicos, disponibles inmediatamente para cada servicio descendente sin una etapa ETL. Los registros minoristas — operadores comerciales, tiendas ancla, estaciones de combustible — y los registros cívicos — hospitales, universidades, centros de transporte — se mantienen en subárboles distintos para que los servicios de filtrado y agrupación puedan trabajar en cada dominio de forma independiente.

## Ingestión y almacenamiento de datos

El servicio mantiene una estructura de sistema de archivos unificada con zonas de aterrizaje separadas para datos minoristas e infraestructura cívica.

- **Zona de aterrizaje minorista:** registros de operadores comerciales en bruto ingeridos desde registros geoespaciales abiertos (OpenStreetMap, Overture Maps Foundation).
- **Zona de aterrizaje cívica:** registros de instalaciones cívicas e institucionales de las mismas fuentes abiertas.

## Rol arquitectónico

Como capa con estado de la plataforma, `service-fs` es responsable de la persistencia de datos. Está diseñado para ser independiente del software analítico: si la capa de orquestación GIS se re-aprovisiona, los activos de datos principales permanecen intactos dentro de esta capa. La separación limpia entre persistencia de datos y lógica analítica es un invariante de diseño fundamental.

## Implementación como unikernel

En producción, `service-fs` se despliega como un unikernel de baja sobrecarga. Proporciona una API restringida para que las capas de inteligencia `service-business` y `service-places` lean datos en bruto y escriban resultados procesados, aplicando una separación limpia entre preocupaciones de almacenamiento y análisis.

## Véase también

- [[service-business-clustering]]
- [[service-places-filtering]]
- [[app-orchestration-gis]]
