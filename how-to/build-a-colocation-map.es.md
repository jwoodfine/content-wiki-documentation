---
schema: foundry-doc-v1
title: "Cómo construir un mapa de co-ubicación"
slug: build-a-colocation-map
category: how-to
content_type: how-to
type: how-to
status: stub
language_protocol: TRANSLATE-ES
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: build-a-colocation-map.md
---

El motor GIS de PointSav expone una API de tiles y un punto de conexión de clústeres que puedes integrar en cualquier aplicación MapLibre GL. Esta guía cubre la autenticación con la API GIS, la obtención de la capa GeoJSON de clústeres y la renderización de marcadores de clústeres con color por nivel en un lienzo MapLibre.

Para la arquitectura del motor GIS, consulta [[pointsav-gis-engine]]. Para el sistema de puntuación de co-ubicación que produce los datos de clústeres, consulta [[topic-co-location-ranking-system|sistema de clasificación de co-ubicación]].

## Véase también

- [[pointsav-gis-engine]] — arquitectura del motor GIS y superficies de API disponibles
- [[topic-co-location-methodology|metodología de co-ubicación]] — cómo se puntúan los niveles de los clústeres
- [[topic-od-catchment-methodology|metodología de captación O-D]] — cómo se definen las áreas comerciales
- [[federate-archives-via-content-mounts]] — monta datos de inteligencia de ubicación en una segunda instancia
