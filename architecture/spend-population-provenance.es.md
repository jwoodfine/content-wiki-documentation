---
schema: foundry-doc-v1
title: "Estimación de gasto y población: procedencia y supuestos"
slug: spend-population-provenance
category: architecture
type: concept
content_type: topic
quality: complete
status: stable
bcsc_class: public-disclosure-safe
language: es
last_edited: 2026-06-23
editor: pointsav-engineering
paired_with: spend-population-provenance.md
cites: []
---

El mapa de inteligencia de ubicación de Woodfine presenta dos superficies demográficas sintetizadas para cada clúster de co-ubicación: una población de cuenca y un gasto minorista anual estimado. Ambas son entradas de grado decisional — un analista de selección de sitios o un asignador de capital las leerá como mediciones. No son mediciones. Son estimaciones de modelos en capas construidas sobre datos abiertos. Este artículo documenta exactamente cómo se producen esas dos superficies, qué asumen, dónde son más débiles y cómo se comunica — y aún no se comunica — su incertidumbre.

## La cadena de estimación

La cifra de gasto mostrada en un clúster es la salida de tres pasos de modelado secuenciales. Ningún error introducido en cada paso se propaga actualmente hacia adelante al valor mostrado.

### Paso 1 — Población: ráster dasymétreo WorldPop

La población se origina del **producto de población cuadriculada de 100 metros WorldPop 2026** (CC BY 4.0). WorldPop es en sí mismo un modelo: los recuentos del censo recopilados en unidades administrativas gruesas se redistribuyen a una cuadrícula de 100 m usando técnicas dasymétricas. La celda de 100 m es una asignación modelada, no una población contada. Su error es heteroscedástico: más estrecho donde existen microdatos censales recientes y de alta calidad, más amplio donde el censo subyacente es más antiguo o más grueso.

### Paso 2 — Agregación a la resolución 7 de H3

Las celdas de 100 m se filtran a las que están dentro de 150 km del centroide de un clúster de co-ubicación, luego se suman en su **hexágono de resolución 7 de H3** (área promedio aproximadamente 5,16 km²). La población de la cuenca es la suma de las poblaciones de las celdas H3 cuyos centroides caen dentro de los anillos de distancia de un clúster.

### Paso 3 — Gasto: multiplicador per cápita

El gasto anual estimado es **población × un multiplicador de gasto per cápita**, aplicado por país y categoría minorista. Los multiplicadores son proxies derivados de encuestas nacionales de gastos de los hogares: BLS Consumer Expenditure Survey para EE. UU., Statistics Canada Household Expenditures para Canadá, Eurostat Household Budget Survey para los países miembros de la UE, e INEGI para México.

### El supuesto per cápita uniforme

La simplificación más consecuente es: **a cada residente de un país se le asigna el mismo gasto per cápita, independientemente de dónde viva.** El modelo no tiene variación de ingresos, edad, tamaño del hogar ni costo de vida por debajo del nivel nacional. Este supuesto se mantiene y se declara en el modal de Metodología.

### Riesgo de falsa precisión

Cada paso arriba tiene su propio error, y se acumulan. La canalización actual no lleva ningún término de error a través de ningún paso. El gasto se muestra redondeado a una banda que el modelo puede defender — por ejemplo "~$150M de gasto anual en alimentos" o un rango — y etiquetado como estimado.

### El problema de la unidad areal modificable

Ambas superficies se agregan a la cuadrícula de resolución 7 de H3 antes de que se tomen las sumas de la cuenca. El problema de la unidad areal modificable (MAUP) es el resultado bien establecido de que las estadísticas calculadas sobre unidades areales cambian cuando cambia el tamaño o el límite de la unidad. La magnitud del efecto MAUP a la resolución 7 para los anillos de distancia en uso aún no se ha cuantificado.

## Confianza y cómo se muestra

La canalización ya calcula una **bandera de confianza** por mercado en `regional-markets.json`. En la compilación del 2026-05-22, 2.942 de 2.986 objetos del Mercado Regional llevaban la bandera de alta confianza. A pesar de esto, la bandera aún no se representa en ningún lugar — el mapa dibuja cada clúster con opacidad completa y un marcador idéntico.

La intención cartográfica es hacer de la confianza un canal visual en el punto del nivel:

- **Opacidad** — clústeres de menor confianza representados con opacidad de relleno reducida.
- **Marcadores huecos frente a rellenos** — un punto hueco para clústeres de menor confianza y un punto relleno para los de mayor confianza.

## Tabla de multiplicadores de gasto per cápita anual

Los multiplicadores son proxies de gasto per cápita anual expresados en moneda local.

| País | Alimentos | Ferretería | Mayorista | Moneda |
|---|---|---|---|---|
| EE. UU. | $3.500 | $1.200 | $1.500 | USD |
| Canadá | C$3.200 | C$1.100 | C$1.300 | CAD |
| México | MX$18.000 | MX$3.500 | MX$2.500 | MXN |
| Gran Bretaña | £2.800 | £850 | £900 | GBP |
| Alemania | €2.900 | €950 | €1.000 | EUR |
| Francia | €3.100 | €900 | €1.000 | EUR |
| Países Bajos | €2.700 | €1.000 | €1.100 | EUR |
| Austria | €3.000 | €950 | €1.000 | EUR |
| Portugal | €2.400 | €600 | €700 | EUR |
| Grecia | €2.200 | €500 | €600 | EUR |
| Dinamarca | €3.500 | €1.200 | €1.100 | EUR |
| Islandia | €4.000 | €1.500 | €1.500 | EUR |
| Polonia | PLN 8.000 | PLN 2.000 | PLN 2.500 | PLN |

**Nota de moneda.** Dado que los multiplicadores están en moneda local y no están normalizados por tipo de cambio, las comparaciones de gasto entre países no son directamente significativas.

## Cómo leer una cifra de gasto o población

1. **La población y el gasto son estimaciones modeladas, no recuentos.**
2. **El gasto asume que todos en un país gastan lo mismo por persona.** Los tramos pudientes están subestimados; los de menores ingresos están sobreestimados.
3. **Las cifras se redondean a propósito.** Un número redondo señala una estimación.
4. **Un punto tenue o hueco significa menor confianza,** no un nivel inferior.
5. **Las pequeñas diferencias entre clústeres pueden ser artefactos de la cuadrícula** (MAUP), no diferencias reales.
6. **El gasto es comparable dentro de un país, no entre monedas** hasta que se implemente la normalización de tipos de cambio.

## Véase también

- [[trade-area-methodology]] — cómo se define el polígono sobre el cual se suman la población y el gasto
- [[co-location-tiering-scoring]] — cómo la cifra de gasto alimenta el puntaje de fortaleza planeado
- [[regional-market-definition]] — el resumen a nivel de asentamiento que agrega cifras a nivel de clúster
- [[app-orchestration-gis]] — la capa de orquestación que ejecuta la canalización de gasto y población
