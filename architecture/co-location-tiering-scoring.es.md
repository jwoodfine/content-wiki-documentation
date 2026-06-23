---
schema: foundry-doc-v1
title: "Niveles y puntuación de co-ubicación"
slug: co-location-tiering-scoring
category: architecture
type: concept
content_type: topic
quality: complete
status: stable
bcsc_class: public-disclosure-safe
language: es
last_edited: 2026-06-23
editor: pointsav-engineering
paired_with: co-location-tiering-scoring.md
cites: []
---

El mapa de inteligencia de ubicación de Woodfine asigna a cada clúster de co-ubicación uno de tres niveles — T1, T2 o T3 — sobre la base de la composición de categorías de minoristas. Los niveles se representan como puntos de colores graduados de T1 (co-ubicación más profunda) a T3 (co-ubicación calificada más superficial). Comprender con precisión qué miden los niveles — y qué no — es necesario para leer correctamente cualquier resultado de clúster.

## Qué miden los niveles

La variable que impulsa el nivel es la **composición de categorías de minoristas**: el conteo y la combinación de categorías de ancla distintas co-presentes dentro de un solo clúster espacial. El nivel es, por tanto, una clasificación composicional ordinal.

Los niveles miden la composición. No miden la fortaleza del área de atracción, el potencial de ventas, la población alcanzada ni el gasto capturado. La composición no implica demanda: un clúster T1 tiene más diversidad de anclas que un clúster T3, pero no se sigue que tenga más personas, más gasto o mejor accesibilidad en su área de atracción.

El etiquetado en el mapa dice "profundidad de co-ubicación (conteo de anclas)" en lugar de "niveles de calidad", y la definición en lenguaje sencillo de cada nivel está vinculada a la composición:

- **T1** — mayor profundidad de co-ubicación (más categorías de ancla co-presentes)
- **T2** — profundidad de co-ubicación intermedia
- **T3** — co-ubicación calificada más superficial

## Cómo se forman los clústeres: parámetros DBSCAN

Los clústeres se producen mediante agrupación espacial de ubicaciones de minoristas ancla usando **DBSCAN** (agrupación espacial basada en densidad), seguido de un pase de deduplicación. DBSCAN se rige por tres parámetros publicados en el modal de Metodología:

- **eps** — el radio de vecindad que define si dos puntos ancla son accesibles por densidad.
- **minPts** — el número mínimo de puntos necesarios para iniciar un clúster.
- **Umbral de IoU** — el corte de intersección sobre unión utilizado para deduplicar clústeres candidatos superpuestos.

Un límite duro de **3,0 km** en el alcance del clúster (diámetro máximo por pares) se aplica uniformemente. Un alcance de 1,0 km o menos lleva una bandera de calidad `tight_intact`.

### Sensibilidad: el conteo de clústeres es una salida del modelo

DBSCAN es un procedimiento **descriptivo**. El número de clústeres que devuelve el algoritmo es una función de eps, minPts y el umbral de IoU, y se mueve materialmente cuando estos varían dentro de rangos razonables. Los barridos de parámetros realizados durante el desarrollo demuestran esto directamente: en el rango razonable probado, el **conteo de clústeres norteamericanos se mueve de aproximadamente 226 a 476** dependiendo de la configuración. Un conteo titular de clústeres es, por tanto, una salida del modelo bajo una parametrización elegida, no un conteo preciso de un fenómeno objetivo.

## El puntaje de fortaleza planeado

El nivel de composición responde "¿qué combinación de minoristas hay aquí?" Un **puntaje de fortaleza** por clúster separado — planeado, aún no construido — está destinado a responder "¿cuánto mercado comanda esta ubicación?" Las dos dimensiones se informan una al lado de la otra una vez que el cuadro de mando esté conectado; nunca se colapsan en un solo color o un solo número.

### Conjunto de variables propuesto

Tres cantidades del lado de la demanda que las capas de datos ya admiten:

1. **Población alcanzada** — población de la cuenca e hogares, del ráster dasymétreo WorldPop 2026 agregado a la resolución 7 de H3.
2. **Gasto capturado** — gasto minorista anual estimado en la cuenca, derivado de la población y proxies de gasto per cápita (BLS, StatCan, Eurostat). Lleva las advertencias de estimación documentadas en [[spend-population-provenance]].
3. **Accesibilidad** — qué tan accesible es la cuenca, expresada a través de la demanda de origen-destino observada donde está disponible y una reserva de banda de distancia en otro lugar.

### Ponderaciones: una cuestión abierta

Cómo se combinan estos tres factores en un solo número es una cuestión abierta que este artículo deliberadamente no resuelve. Hasta que se ratifique la ponderación, el cuadro de mando muestra los valores de los factores individualmente para que cualquier compuesto mostrado siempre sea descomponible.

## Véase también

- [[trade-area-methodology]] — derivación de la cuenca y la migración desde bandas de distancia hacia áreas de atracción observadas
- [[spend-population-provenance]] — la cadena de estimación para el factor de gasto en el puntaje de fortaleza
- [[regional-market-definition]] — el resumen a nivel de asentamiento y el criterio de selección Top-400
- [[app-orchestration-gis]] — la capa de orquestación que produce los clústeres por niveles
