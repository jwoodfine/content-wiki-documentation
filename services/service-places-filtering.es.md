---
schema: foundry-doc-v1
title: "service-places — Filtrado de infraestructura cívica"
slug: service-places-filtering
short_description: "service-places filtra datos crudos de infraestructura cívica e institucional para retener solo instalaciones de nivel regional — hospitales, universidades y centros de transporte importantes — así los rankings de nivel de GIS reflejan concentración de nivel institucional en lugar de densidad de servicios locales."
category: services
type: topic
content_type: topic
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

Las [[co-location-methodology|clasificaciones de nivel GIS]] dependen de saber dónde se ubican las instituciones regionales, no dónde se ubica cada clínica y colegio comunitario. **`service-places`** filtra los datos cívicos en bruto para retener únicamente instalaciones de escala regional — hospitales con al menos 50 camas dotadas, universidades con al menos 1.000 estudiantes equivalentes a tiempo completo, centros de transporte principales validados — y aplica un búfer espacial de 200 m para consolidar grandes campus institucionales en anclas regionales únicas. La densidad de servicios locales se filtra en esta etapa; las clasificaciones descendentes reflejan la concentración institucional en lugar del recuento de instalaciones.

## Puntos clave

- Los umbrales de nivel regional son estructurales en el servicio: hospitales con ≥50 camas dotadas, universidades con ≥1.000 estudiantes equivalentes a tiempo completo, y aeropuertos de aviación general excluidos de la puntuación. Estos filtros no son parámetros configurables.
- Un búfer espacial de 200 m consolida registros de campus multipunto — un hospital grande puede aparecer en OSM como decenas de nodos — en un único ancla regional con un centroide unificado. Esto previene el doble conteo en grandes huellas institucionales.
- La salida es `cleansed-places.jsonl`, consumida por `[[app-orchestration-gis]]` junto al conjunto de datos de clústeres minoristas de `[[service-business-clustering]]` al asignar los niveles de co-ubicación finales.
- La etapa de filtrado es deliberadamente anterior a la puntuación de nivel. Una vez que la densidad de servicios locales se elimina aquí, toda la puntuación posterior opera sobre una señal limpia de instituciones regionales.

## Umbrales de filtrado

El servicio aplica filtros de ponderación de atributos a los datos cívicos en bruto proporcionados por [[service-fs-data-lake|`service-fs`]]:

- **Hospitales regionales:** umbral mínimo de capacidad (50+ camas con personal).
- **Universidades regionales:** umbral mínimo de matrícula (1.000+ estudiantes equivalentes a tiempo completo).
- **Aeropuertos:** validados como centros de transporte regional principales; las instalaciones de aviación general se excluyen.

## Agregación espacial

Los grandes campus institucionales frecuentemente aparecen en datos geoespaciales abiertos en bruto como múltiples puntos separados. `service-places` aplica un búfer espacial de 200 m para agruparlos en un único ancla regional con un centro de gravedad unificado, previniendo el doble conteo de grandes huellas de campus.

## Salida de datos

El `cleansed-places.jsonl` resultante proporciona el conjunto de datos de anclas regionales que [[app-orchestration-gis]] utiliza al otorgar las [[co-location-methodology|clasificaciones de nivel de co-ubicación]] finales.

## Véase también

- [[service-fs-data-lake]] — lago de datos GIS que suministra los datos cívicos y minoristas en bruto
- [[service-business-clustering]] — servicio de agrupación minorista que consume los datos de lugares filtrados
- [[app-orchestration-gis]] — capa de orquestación que ensambla las clasificaciones de nivel
- [[co-location-methodology]] — la metodología de clasificación que impulsa las asignaciones de nivel
