---
schema: foundry-doc-v1
title: "GIS como sustrato BIM"
slug: gis-as-bim-substrate
short_description: "Lo que el dataset de co-ubicación GIS de PointSav ofrece a un canal de composición BIM: campos del manifold de clusters, capas de contexto cívico y garantías de estabilidad."
category: architecture
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: gis-as-bim-substrate.md
---

# GIS como sustrato BIM

La Modelización de Información de Construcción (BIM, por sus siglas en inglés) opera a escala de edificio: geometría estructural, ensamblajes de materiales, sistemas mecánicos, ocupación. Un modelo tiene sentido por sí solo, pero su valor comercial emerge cuando se emplaza — cuando se posiciona en una geografía real con vecinos reales, áreas de influencia reales y contexto regulatorio real. El dataset de co-ubicación GIS de PointSav está diseñado para proporcionar ese contexto de emplazamiento a los canales de composición BIM.

Este artículo documenta lo que el dataset GIS ofrece a un consumidor BIM, qué campos son estables y qué extensiones están previstas.

---

## El manifold de clusters

La salida primaria del GIS es un manifold de aproximadamente 6.400 clusters comerciales de co-ubicación deduplicados en Estados Unidos, Canadá, México, el Reino Unido y Europa continental. Cada cluster contiene:

- un identificador estable y una posición geográfica fija (latitud/longitud)
- el nombre regional resuelto a través del motor de límites por capas
- la clasificación de nivel (Regional, Distrital, Local, Marginal)
- la composición categórica (qué tipos de anclaje están presentes)
- el número de tiendas dentro de radios de influencia anidados (1 km, 2 km, 3 km)

Para un consumidor BIM, este manifold responde preguntas que un modelo solo no puede: ¿Qué densidad comercial tiene el área dentro de 3 km de este edificio propuesto? ¿Qué formatos de anclaje ya sirven el área de influencia? ¿Dónde está el sitio equivalente más cercano contra el que se podría comparar un modelo?

---

## Propiedades del cluster disponibles para la ingestión BIM

El registro de propiedades de cada cluster contiene campos adecuados para la ingestión directa por parte de un canal de composición de código de ciudad:

| Campo | Tipo | Uso en BIM |
|---|---|---|
| `cluster_id` | cadena | Clave de unión estable |
| `latitude`, `longitude`, `centroid_lat`, `centroid_lon` | flotante | Posiciones de anclaje y centroide para el emplazamiento |
| `region_name` | cadena | Nombre metropolitano o municipal resuelto; útil como parámetro de modelo |
| `tier_descriptor` | cadena | Regional / Distrital / Local / Marginal — señal de densidad |
| `count_1km`, `count_3km` | entero | Densidad del área de influencia |
| `unique_brands` | entero | Marcas comerciales distintas dentro del área de influencia |
| `iso`, `state` | cadena | Códigos de jurisdicción |

El manifold de clusters se publica como PMTiles con un esquema de capas que soporta posiciones individuales de tiendas (Capa 1) y envolventes de clusters con anillos de proximidad (Capa 2).

---

## Profundidad de resolución regional

El motor de límites resuelve las coordenadas a uno de cinco niveles de granularidad, de más específico a más general: GADM admin-3, GADM admin-2, NUTS-3 de Eurostat, CMA de Statistics Canada / CBSA del Censo de EE.UU., y Natural Earth admin-1 (respaldo global a nivel de estado o provincia).

---

## Capas de contexto cívico

Además del manifold de clusters, el dataset GIS incluye dos capas cívicas relevantes para programas de construcción que dependen de la adyacencia cívica:

- **Catálogo de hospitales.** Aproximadamente 28.000 ubicaciones de hospitales en la huella operativa, obtenidas de OpenStreetMap.
- **Catálogo de universidades.** Aproximadamente 19.000 ubicaciones de educación superior, obtenidas de la misma fuente.

La distancia al hospital más cercano y a la universidad más cercana se calcula por cluster dentro de un límite práctico de 5 km.

---

## Garantías de estabilidad

**Estable entre versiones:** identificadores de clusters, la estructura del manifold, el esquema de clasificación de niveles, el algoritmo de resolución de nombres regionales y los radios de influencia.

**Es probable que cambie:** el tamaño de la taxonomía de familias de marcas (las familias de alimentación y farmacia están en expansión) y el número absoluto de tiendas (la cobertura de OpenStreetMap mejora año tras año).

---

## Véase también

- [[co-location-methodology]]
- [[regional-name-resolution-architecture]]
- [[city-code-as-composable-geometry]]
