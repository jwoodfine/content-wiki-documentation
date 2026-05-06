---
schema: foundry-doc-v1
title: "service-places — Filtrado de Infraestructura Cívica"
slug: service-places-filtering
category: services
type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: service-places-filtering.md
cites: []
---

`service-places` es el servicio responsable de validar y agrupar la infraestructura cívica e institucional. Su función principal es filtrar los datos cívicos en bruto para retener únicamente instalaciones de escala regional — hospitales, universidades y centros de transporte principales — garantizando que las clasificaciones de nivel GIS reflejen la concentración a nivel institucional en lugar de la densidad de servicios locales.

## Umbrales de filtrado

El servicio aplica filtros de ponderación de atributos a los datos cívicos en bruto proporcionados por `service-fs`:

- **Hospitales regionales:** umbral mínimo de capacidad (50+ camas con personal).
- **Universidades regionales:** umbral mínimo de matrícula (1.000+ estudiantes equivalentes a tiempo completo).
- **Aeropuertos:** validados como centros de transporte regional principales; las instalaciones de aviación general se excluyen.

## Agregación espacial

Los grandes campus institucionales frecuentemente aparecen en datos geoespaciales abiertos en bruto como múltiples puntos separados. `service-places` aplica un búfer espacial de 200 m para agruparlos en un único ancla regional con un centro de gravedad unificado, previniendo el doble conteo de grandes huellas de campus.

## Salida de datos

El `cleansed-places.jsonl` resultante proporciona el conjunto de datos de anclas regionales que `app-orchestration-gis` utiliza al otorgar las clasificaciones de nivel de co-ubicación finales.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
