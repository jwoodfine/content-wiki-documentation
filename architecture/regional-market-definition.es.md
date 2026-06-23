---
schema: foundry-doc-v1
title: "Definición de mercado regional"
slug: regional-market-definition
category: architecture
type: concept
content_type: topic
quality: complete
status: stable
bcsc_class: public-disclosure-safe
language: es
last_edited: 2026-06-23
editor: pointsav-engineering
paired_with: regional-market-definition.md
cites: []
---

El mapa de inteligencia de ubicación de Woodfine organiza los clústeres de co-ubicación en dos contenedores espaciales: el **asentamiento con presencia de co-ubicación** (una estadística de cobertura) y el **Mercado Regional** (un objeto más estricto reservado para asentamientos con concentraciones significativas de comercio minorista co-ubicado). Un tercer contenedor más grueso — el **Mercado Metro** — proporciona contexto a nivel metropolitano principal. Este artículo define cada objeto, declara la regla que lo produce y distingue entre lo que mide cada conteo y lo que no mide.

## Los dos objetos actualmente llamados Mercados Regionales

La canalización resuelve cada clúster de co-ubicación a un polígono municipal incorporado o CSD utilizando `RegionEngine.resolve_market()` — una asignación de punto en polígono contra archivos de límites TIGER 2023 para EE. UU., GISCO LAU 2021 más GADM GBR para la UE y el Reino Unido. Un asentamiento se convierte en objeto de Mercado Regional en el momento en que **una** co-ubicación cae dentro de su polígono.

Bajo esta regla permisiva, en la compilación del 2026-05-22, la canalización produce aproximadamente **3.011 asentamientos** (América del Norte y UE/RU) con presencia de co-ubicación, de los cuales **2.986** se publican en `regional-markets.json` del gateway y **2.942** llevan la bandera de geocodificación de alta confianza.

Eso es una estadística de cobertura. Registra cuán ampliamente se observan las cadenas de ancla rastreadas. No identifica dónde se concentra realmente la demanda minorista.

## La distinción: cobertura frente a mercado

Dos modos de falla se derivan de confundir cobertura con mercado:

**Los asentamientos de ancla única dominan la población.** Un pueblo con una co-ubicación calificante es, bajo la regla actual, la misma clase de objeto que un área metropolitana con decenas. La etiqueta "Mercado Regional" implica demanda minorista concentrada; la regla admite el caso de ancla única.

**El conteo parece un artefacto del umbral, no de la geografía.** Un revisor puede mover el conteo hacia arriba o hacia abajo simplemente argumentando el umbral, lo cual es la señal clásica de que el umbral — no los datos — está haciendo el trabajo.

`mkt_conf` es precisión de geocodificación — específicamente la calidad de la asignación de límites — no calidad del mercado, y no debe presentarse como una clasificación o señal de calidad.

## Recomendación: separar los objetos

Se recomienda mantener ambos objetos pero distinguirlos claramente por nombre:

### Asentamiento con presencia de co-ubicación

- **Definición.** Cualquier polígono municipal incorporado o CSD que contenga al menos una co-ubicación.
- **Conteo.** Los aproximadamente 3.011 completos (NA más UE/RU). Declarado como estadística de cobertura.
- **Función.** Mapa de cobertura, reclamación de huella, y el conjunto base del cual se extrae el objeto más estricto. No el conteo titular del mercado.

### Mercado Regional

Un asentamiento se promueve a Mercado Regional solo cuando supera un umbral declarado. Dos umbrales candidatos están sobre la mesa:

**Opción de umbral 1 — composición.** Un Mercado Regional contiene un número mínimo de co-ubicaciones dentro de su polígono. Un umbral de dos excluye inmediatamente a todos los asentamientos de ancla única. Este umbral es el más barato de calcular y el más fácil de defender.

**Opción de umbral 2 — umbral de demanda.** Un Mercado Regional supera un umbral declarado de población de cuenca o gasto anual estimado. Esto es más defendible analíticamente — vincula el término a la demanda en lugar de la densidad de oferta — pero depende de que las superficies de cuenca y gasto sean confiables primero.

La secuencia recomendada es adoptar un umbral de composición ahora y declarar la intención de migrar a un umbral de demanda una vez que las superficies de cuenca y gasto completen sus propias revisiones. Cualquiera que sea el umbral elegido, **el conteo resultante del Mercado Regional debe re-derivarse y publicarse junto al umbral**.

## Las Top-400 co-ubicaciones

El Top-400 es una lista de co-ubicaciones (no Mercados Regionales) producida por región, cortada en 400. La lista se publica, clasifica y corta en 400, pero la **variable de clasificación actualmente no se declara** en ningún lugar de la cara del mapa ni en la documentación.

La recomendación es publicar una variable de clasificación y un criterio de desempate, en lenguaje sencillo, en el modal de Metodología y en este artículo. La secuencia recomendada es declarar la variable de clasificación actual honestamente hoy y declarar la migración prevista a una puntuación basada en la demanda o compuesta a medida que las revisiones de cuenca, gasto y puntuación se implementen.

## Mercado Metro

El Mercado Metro es un contenedor contextual más grueso: un área metropolitana principal en una lista de referencia publicada (MSA/CBSA de EE. UU., AMC canadiense). Un Mercado Regional se anida dentro de como máximo un Mercado Metro. El Mercado Metro es solo contexto — nunca es el nivel de zoom de co-ubicación o anillo.

## Conteos declarados honestamente

| Objeto | Regla | Conteo | Qué mide |
|---|---|---|---|
| Asentamientos con presencia de co-ubicación | ≥1 co-ubicación en polígono | ~3.011 (NA + UE/RU) | Cobertura y huella |
| Mercados Regionales (propuesto, umbral de 2) | ≥2 co-ubicaciones en polígono | Por re-derivar en la adopción | Co-ubicación concentrada |
| Objetos RM publicados (gateway) | Regla permisiva actual | 2.986 (2.942 alta confianza) | Cobertura; calidad de geocodificación |
| Top-400 co-ubicaciones (por región) | Top 400 por una variable declarada | 400 NA + 400 UE | Sitios candidatos clasificados |
| Co-ubicaciones NA (DBSCAN) | eps/minPts/IoU — sensible | 226–476 en el barrido de parámetros | Conteo de clústeres (descriptivo) |

## Véase también

- [[co-location-tiering-scoring]] — cómo se calculan los niveles y el puntaje de fortaleza planeado para cada co-ubicación dentro de un Mercado Regional
- [[trade-area-methodology]] — cómo se define el área de atracción para cada co-ubicación
- [[spend-population-provenance]] — la cadena de estimación para las cifras de población y gasto
- [[app-orchestration-gis]] — la capa de orquestación que resuelve las co-ubicaciones en Mercados Regionales
