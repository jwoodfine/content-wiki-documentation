---
schema: foundry-doc-v1
title: "Lago de datos GIS"
slug: service-fs-data-lake
short_description: "El lago de datos de la canalización GIS es su capa de almacenamiento fundamental — un almacén de archivos planos que guarda puntos geoespaciales sin procesar, disponible para cada paso descendente de la misma canalización. Distinto de service-fs, el libro mayor WORM separado de la plataforma."
category: services
type: topic
content_type: topic
quality: complete
index_group: specialist-and-domain-services
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-09-05
editor: pointsav-engineering
paired_with: service-fs-data-lake.md
cites: []
---

**El lago de datos GIS** es la capa de almacenamiento fundacional para la [[location-intelligence-substrate|canalización GIS]] de la plataforma — un almacén en archivos planos que guarda puntos geoespaciales en bruto ingeridos desde fuentes abiertas (OpenStreetMap, Overture Maps Foundation) en zonas de aterrizaje separadas para datos minoristas y cívicos, disponibles inmediatamente para cada paso descendente de la misma canalización sin una etapa ETL. Los registros minoristas — operadores comerciales, tiendas ancla, estaciones de combustible — y los registros cívicos — hospitales, universidades, centros de transporte — se mantienen en subárboles distintos para que los pasos de [[service-places-filtering|filtrado]] y [[service-business-clustering|agrupación]] puedan trabajar en cada dominio de forma independiente. Este lago de datos es un componente distinto de [[service-fs]], el libro mayor WORM por inquilino separado de la plataforma — los dos no comparten código ni formato de almacenamiento.

## Puntos clave

- Dos zonas de aterrizaje separadas — minorista y cívica — almacenan puntos en bruto de OpenStreetMap y Overture Maps Foundation. Los pasos descendentes leen directamente desde las zonas de aterrizaje; no hay etapa de transformación ETL entre la ingestión y el consumo.
- La persistencia de datos está desacoplada de la lógica analítica. Si [[app-orchestration-gis]] se re-aprovisiona, los activos de datos en bruto del lago de datos permanecen intactos e inmediatamente disponibles para cualquier capa analítica de reemplazo.
- Hoy las zonas de aterrizaje son directorios planos en el sistema de archivos del host, poblados y leídos directamente por los propios scripts de ingesta y análisis de la canalización GIS. No existe ningún servicio de almacenamiento dedicado, ninguna API restringida, ni ningún entorno unikernel delante de ellos. Los pasos de [[service-business-clustering|agrupación comercial]] y [[service-places-filtering|filtrado de lugares]] que leen estos datos se ejecutan como pasos dentro de la misma canalización basada en Python documentada en [[app-orchestration-gis]], no como crates o servicios separados que leen a través de un límite.
- El diseño en archivos planos y formato abierto evita la dependencia de formatos propietarios. Los registros geoespaciales en bruto son archivos de texto legibles por cualquier herramienta en cualquier década.

## Ingestión y almacenamiento de datos

La canalización mantiene una estructura de sistema de archivos unificada con zonas de aterrizaje separadas para datos minoristas e infraestructura cívica.

- **Zona de aterrizaje minorista:** registros de operadores comerciales en bruto ingeridos desde registros geoespaciales abiertos (OpenStreetMap, Overture Maps Foundation).
- **Zona de aterrizaje cívica:** registros de instalaciones cívicas e institucionales de las mismas fuentes abiertas.

## Rol arquitectónico

Como capa con estado de la canalización GIS, el lago de datos es responsable de la persistencia de datos, mantenida independiente del código analítico que la lee: si la [[app-orchestration-gis|capa de orquestación GIS]] se re-aprovisiona, los activos de datos principales permanecen intactos dentro de esta capa. La separación limpia entre persistencia de datos y lógica analítica es un invariante de diseño fundamental de esta canalización. Es un diseño separado del libro mayor WORM de la plataforma ([[service-fs]]), que ancla registros institucionales para cumplimiento en lugar de almacenar puntos geoespaciales en bruto — los dos no son capas de un mismo sistema compartido de cuatro capas.

## Lo que esto no es

Hoy no existe ningún servicio de almacenamiento dedicado ni ninguna API restringida delante de estas zonas de aterrizaje — son directorios planos del sistema de archivos del host, leídos y escritos directamente por los scripts de ingesta y análisis GIS mediante E/S de archivos ordinaria. Ningún crate `service-business` o `service-places` existe en el código; los pasos de agrupación comercial y filtrado de lugares son pasos en Python dentro de la propia canalización de [[app-orchestration-gis]], no servicios desplegados por separado con su propio límite de almacenamiento. La [[retail-co-location-tier-methodology|metodología de niveles de co-ubicación minorista]] describe cómo se usa la salida de agrupación para generar clasificaciones por nivel.

## Véase también

- [[service-business-clustering]]
- [[service-places-filtering]]
- [[app-orchestration-gis]]
- [[service-fs]] — el libro mayor WORM separado de la plataforma; un componente distinto de este lago de datos
