---
schema: foundry-doc-v1
title: "service-fs — Lago de Datos GIS"
slug: service-fs-data-lake
category: services
type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: service-fs-data-lake.md
cites: []
## Véase también

- [[service-business-clustering]]
- [[service-places-filtering]]
- [[app-orchestration-gis]]

---

`service-fs` es la capa de almacenamiento fundacional para la plataforma GIS de PointSav. Implementa un modelo de lago de datos donde los puntos geoespaciales en bruto ingeridos desde fuentes geoespaciales abiertas se almacenan en un sistema de archivos duradero y modular para el procesamiento analítico descendente.

## Ingestión y almacenamiento de datos

El servicio mantiene una estructura de sistema de archivos unificada con zonas de aterrizaje separadas para datos minoristas e infraestructura cívica.

- **Zona de aterrizaje minorista:** registros de operadores comerciales en bruto ingeridos desde registros geoespaciales abiertos (OpenStreetMap, Overture Maps Foundation).
- **Zona de aterrizaje cívica:** registros de instalaciones cívicas e institucionales de las mismas fuentes abiertas.

## Rol arquitectónico

Como capa con estado de la plataforma, `service-fs` es responsable de la persistencia de datos. Está diseñado para ser independiente del software analítico: si la capa de orquestación GIS se re-aprovisiona, los activos de datos principales permanecen intactos dentro de esta capa. La separación limpia entre persistencia de datos y lógica analítica es un invariante de diseño fundamental.

## Implementación como unikernel

En producción, `service-fs` se despliega como un unikernel de baja sobrecarga. Proporciona una API restringida para que las capas de inteligencia `service-business` y `service-places` lean datos en bruto y escriban resultados procesados, aplicando una separación limpia entre preocupaciones de almacenamiento y análisis.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
