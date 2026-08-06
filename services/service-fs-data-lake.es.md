---
schema: foundry-doc-v1
title: "service-fs — Lago de datos GIS"
slug: service-fs-data-lake
short_description: "service-fs es la capa de almacenamiento fundamental para la canalización GIS de la plataforma — un lago de datos de archivos planos que almacena puntos geoespaciales sin procesar ingeridos de fuentes abiertas en zonas de aterrizaje separadas de venta minorista y cívicas, disponibles inmediatamente para cada servicio descendente sin un paso ETL."
category: services
type: topic
content_type: topic
quality: complete
index_group: specialist-and-domain-services
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-07-31
editor: pointsav-engineering
paired_with: service-fs-data-lake.md
cites: []
---

**`service-fs`** es la capa de almacenamiento fundacional para la [[pointsav-gis-engine|canalización GIS]] de la plataforma — un lago de datos en archivos planos que almacena puntos geoespaciales en bruto ingeridos desde fuentes abiertas (OpenStreetMap, Overture Maps Foundation) en zonas de aterrizaje separadas para datos minoristas y cívicos, disponibles inmediatamente para cada servicio descendente sin una etapa ETL. Los registros minoristas — operadores comerciales, tiendas ancla, estaciones de combustible — y los registros cívicos — hospitales, universidades, centros de transporte — se mantienen en subárboles distintos para que los servicios de [[service-places-filtering|filtrado]] y [[service-business-clustering|agrupación]] puedan trabajar en cada dominio de forma independiente.

## Puntos clave

- Dos zonas de aterrizaje separadas — minorista y cívica — almacenan puntos en bruto de OpenStreetMap y Overture Maps Foundation. Los servicios descendentes leen directamente desde las zonas de aterrizaje; no hay etapa de transformación ETL entre la ingestión y el consumo.
- La persistencia de datos está desacoplada de la lógica analítica. Si `[[app-orchestration-gis]]` se re-aprovisiona, los activos de datos en bruto de `service-fs` permanecen intactos e inmediatamente disponibles para cualquier capa analítica de reemplazo.
- El despliegue de producción previsto es un unikernel de baja sobrecarga que expone una API restringida, en el que solo las capas de inteligencia ([[service-business-clustering|`service-business`]] y [[service-places-filtering|`service-places`]]) pueden leer datos en bruto y escribir resultados procesados. **Aún no construido**: hoy las zonas de aterrizaje son directorios planos en el sistema de archivos del host, poblados y leídos directamente por los scripts de ingesta y análisis — sin unikernel, sin API restringida, sin crates dedicados `service-business`/`service-places` confirmados en el código todavía.
- El diseño en archivos planos y formato abierto evita la dependencia de formatos propietarios. Los registros geoespaciales en bruto son archivos de texto legibles por cualquier herramienta en cualquier década.

## Ingestión y almacenamiento de datos

El servicio mantiene una estructura de sistema de archivos unificada con zonas de aterrizaje separadas para datos minoristas e infraestructura cívica.

- **Zona de aterrizaje minorista:** registros de operadores comerciales en bruto ingeridos desde registros geoespaciales abiertos (OpenStreetMap, Overture Maps Foundation).
- **Zona de aterrizaje cívica:** registros de instalaciones cívicas e institucionales de las mismas fuentes abiertas.

## Rol arquitectónico

Como capa con estado de la plataforma, `service-fs` es responsable de la persistencia de datos. Está diseñado para ser independiente del software analítico: si la [[app-orchestration-gis|capa de orquestación GIS]] se re-aprovisiona, los activos de datos principales permanecen intactos dentro de esta capa. La separación limpia entre persistencia de datos y lógica analítica es un invariante de diseño fundamental. Este mismo principio de separación se extiende al libro mayor WORM utilizado para registros institucionales; véase [[service-fs-architecture|arquitectura FS]] para el diseño completo de cuatro capas.

## Implementación como unikernel (planificada)

El despliegue de producción previsto es un unikernel de baja sobrecarga que proporciona una API restringida para que las capas de inteligencia [[service-business-clustering|`service-business`]] y [[service-places-filtering|`service-places`]] lean datos en bruto y escriban resultados procesados, aplicando una separación limpia entre preocupaciones de almacenamiento y análisis. **Estado actual**: el entorno unikernel aún no existe — las zonas de aterrizaje descritas arriba son directorios planos del sistema de archivos del host, leídos y escritos directamente por los scripts de ingesta y análisis GIS (verificado contra los propios scripts de ingesta de `app-orchestration-gis`, que leen/escriben estas rutas mediante E/S de archivos ordinaria). La [[retail-co-location-tier-methodology|metodología de niveles de co-ubicación minorista]] describe cómo se usará la salida de agrupación para generar clasificaciones por nivel, una vez que esa capa de análisis exista.

## Véase también

- [[service-business-clustering]]
- [[service-places-filtering]]
- [[app-orchestration-gis]]
