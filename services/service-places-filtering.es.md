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
last_edited: 2026-05-08
editor: pointsav-engineering
paired_with: service-places-filtering.md
cites: []
---

Las clasificaciones de nivel GIS dependen de saber dónde se ubican las instituciones regionales, no dónde se ubica cada clínica y colegio comunitario. **`service-places`** filtra los datos cívicos en bruto para retener únicamente instalaciones de escala regional — hospitales con al menos 50 camas dotadas, universidades con al menos 1.000 estudiantes equivalentes a tiempo completo, centros de transporte principales validados — y aplica un búfer espacial de 200 m para consolidar grandes campus institucionales en anclas regionales únicas. La densidad de servicios locales se filtra en esta etapa; las clasificaciones descendentes reflejan la concentración institucional en lugar del recuento de instalaciones.

## Umbrales de filtrado

El servicio aplica filtros de ponderación de atributos a los datos cívicos en bruto proporcionados por `service-fs`:

- **Hospitales regionales:** umbral mínimo de capacidad (50+ camas con personal).
- **Universidades regionales:** umbral mínimo de matrícula (1.000+ estudiantes equivalentes a tiempo completo).
- **Aeropuertos:** validados como centros de transporte regional principales; las instalaciones de aviación general se excluyen.

## Agregación espacial

Los grandes campus institucionales frecuentemente aparecen en datos geoespaciales abiertos en bruto como múltiples puntos separados. `service-places` aplica un búfer espacial de 200 m para agruparlos en un único ancla regional con un centro de gravedad unificado, previniendo el doble conteo de grandes huellas de campus.

## Salida de datos

El `cleansed-places.jsonl` resultante proporciona el conjunto de datos de anclas regionales que `app-orchestration-gis` utiliza al otorgar las clasificaciones de nivel de co-ubicación finales.

## Véase también

- [[service-fs-data-lake]]
- [[service-business-clustering]]
- [[app-orchestration-gis]]
