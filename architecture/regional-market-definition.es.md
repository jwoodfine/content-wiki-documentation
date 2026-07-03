---
schema: foundry-doc-v1
title: "Definición de mercado regional"
slug: regional-market-definition
short_description: "Contenedores espaciales del mapa de inteligencia de ubicaciones — en qué difieren los asentamientos con co-localización de los Regional Markets; cobertura no es demanda."
category: architecture
type: concept
content_type: topic
quality: complete
status: stable
bcsc_class: public-disclosure-safe
language: es
last_edited: 2026-07-03
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

## Recomendación, corregida: los umbrales de composición significan composición de anclas, no conteo

**Esta sección proponía originalmente un umbral basado en conteo — un "número mínimo" de co-ubicaciones por polígono — como la solución barata y defendible. Esa recomendación era errónea y queda retractada aquí en lugar de dejarse en pie.** El error: un asentamiento puede superar un umbral de conteo de uno y seguir siendo un mercado genuinamente fuerte, si su única co-ubicación es en sí misma una convergencia de varias categorías de anclas independientes — un hipermercado, un minorista de ferretería y un club de almacén dentro de un mismo clúster ya es un T1 según la propia definición del sistema de niveles (véase "Regional Markets Intelligence System" en el wiki de proyectos), y un T1 es exactamente la señal de demanda concentrada que el término "mercado" debería representar. Por el contrario, un asentamiento que supera un umbral de conteo de dos por tener dos clústeres separados de ancla única (T3) no es evidentemente más fuerte que el caso de un solo clúster T1 que un umbral de conteo excluiría. Contar *cuántos* eventos de co-ubicación tiene un asentamiento y contar *cuán fuerte* es cada uno son preguntas distintas, y solo la segunda es lo que "Mercado Regional" debería significar. La composición — la mezcla de categorías de anclas *dentro* de un clúster — ya está correctamente capturada por la clasificación de niveles T1/T2/T3; un umbral basado en el conteo de clústeres en lugar del nivel del clúster repite exactamente la confusión entre cobertura y mercado que este artículo buscaba corregir.

La separación de objetos que sigue se mantiene — un catálogo de cobertura permisivo es algo legítimo y honestamente etiquetado para publicar, separado de una afirmación sobre la fortaleza del mercado — pero el umbral del objeto más estricto debería basarse en niveles, no en conteo.

### Asentamiento con presencia de co-ubicación

- **Definición.** Cualquier polígono municipal incorporado o CSD que contenga al menos una co-ubicación.
- **Conteo.** Los aproximadamente 3.011 completos (NA más UE/RU). Declarado como estadística de cobertura.
- **Función.** Mapa de cobertura, reclamación de huella, y el conjunto base del cual se extrae el objeto más estricto. No el conteo titular del mercado.

### Mercado Regional

Un asentamiento se promueve a Mercado Regional cuando sus co-ubicaciones superan un umbral declarado **basado en niveles**, no en conteo — por ejemplo, "contiene al menos un clúster T1" o "el puntaje de nivel agregado (T1×4 + T2×2 + T3×1) alcanza un mínimo declarado". Esto vincula el término a la *fortaleza* del clúster en lugar de al *conteo* de clústeres, admitiendo correctamente el caso de un solo clúster fuerte y excluyendo correctamente el caso de muchos clústeres débiles que un umbral de conteo confundiría.

Una alternativa, y analíticamente más sólida, es un **umbral de demanda**: un Mercado Regional supera un umbral declarado de población de cuenca o gasto anual estimado, vinculando el término a la demanda en lugar de la densidad de oferta. Esto depende de que las superficies de cuenca y gasto sean confiables primero; su adopción es apropiada una vez que esas superficies incorporen su propio marco de incertidumbre.

Cualquiera que sea el umbral elegido, **el conteo resultante del Mercado Regional debe re-derivarse y publicarse junto al umbral y la regla que lo produjo**.

## Las Top-400 co-ubicaciones — recomendación de variable de clasificación: adoptada

El Top-400 es una lista de co-ubicaciones (no Mercados Regionales) producida por región, cortada en 400.

**Este artículo originalmente señaló que la variable de clasificación del Top-400 no estaba declarada en ningún lugar, y recomendó publicar una puntuación compuesta explicable como la solución más defendible a largo plazo.** Esa recomendación ya se ha adoptado: la clasificación ahora se basa en una puntuación compuesta publicada, `tier_score × civic_multiplier × confidence_factor` — con cada factor visible, no una caja negra. Véase "Regional Markets Intelligence System" en el wiki de proyectos para la fórmula completa. No se necesita ninguna acción adicional en este punto; se registra aquí solo para que la historia de la recomendación quede legible.

## Mercado Metro

El Mercado Metro es un contenedor contextual más grueso: un área metropolitana principal en una lista de referencia publicada (MSA/CBSA de EE. UU., AMC canadiense). Un Mercado Regional se anida dentro de como máximo un Mercado Metro. El Mercado Metro es solo contexto — nunca es el nivel de zoom de co-ubicación o anillo.

## Conteos declarados honestamente

| Objeto | Regla | Conteo | Qué mide |
|---|---|---|---|
| Asentamientos con presencia de co-ubicación | ≥1 co-ubicación en polígono | ~3.011 (NA + UE/RU, compilación 2026-05-22) | Cobertura y huella |
| Mercados Regionales (umbral basado en niveles, recomendación corregida) | ≥1 clúster T1, o puntaje de nivel agregado declarado | Por re-derivar en la adopción | Co-ubicación concentrada, admitiendo correctamente los mercados de un solo clúster fuerte |
| Objetos RM publicados (gateway, compilación posterior) | Regla permisiva (≥1 co-ubicación), sin cambios | 4.436 (compilación 2026-05-30, 18 países — véase "Regional Markets Intelligence System" en el wiki de proyectos) | Cobertura; crecida por expansión de datos, no por un cambio de umbral |
| Top-400 co-ubicaciones (por región) | Puntuación compuesta — nivel × cívico × confianza, publicada | 400 NA + 400 UE | Sitios candidatos clasificados; adoptada según la recomendación anterior |
| Co-ubicaciones NA (DBSCAN) | eps/minPts/IoU — sensible | 226–476 en el barrido de parámetros | Conteo de clústeres (descriptivo) |

## Véase también

- niveles y puntuación de co-ubicación — cómo se calculan los niveles y el puntaje de fortaleza planeado para cada co-ubicación dentro de un Mercado Regional
- metodología de área de atracción — cómo se define el área de atracción para cada co-ubicación
- procedencia de gasto y población — la cadena de estimación para las cifras de población y gasto
- [[app-orchestration-gis]] — la capa de orquestación que resuelve las co-ubicaciones en Mercados Regionales
