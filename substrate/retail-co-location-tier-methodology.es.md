---
schema: foundry-doc-v1
title: "Metodología de niveles de co-localización minorista"
slug: retail-co-location-tier-methodology
category: substrate
type: concept
content_type: topic
quality: complete
index_group: core-named-substrates
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: TRANSLATE-ES
last_edited: 2026-08-24
editor: pointsav-engineering
paired_with: retail-co-location-tier-methodology.md
cites:
 - ni-51-102
 - np-51-201
---

Un clúster de co-localización minorista obtiene un nivel al superar un conjunto fijo de
condiciones, no al acumular puntos hacia una puntuación. La plataforma de
[[location-intelligence-platform|Inteligencia de Ubicación]] asigna a cada clúster uno de
cuatro niveles — Regional, Distrital, Local o Marginal — evaluando la composición, el
rango de población de captación, el respaldo cívico y el solapamiento con vecinos más
fuertes frente a umbrales específicos por país. Un clúster supera todas las condiciones de
un nivel o no lo hace; no hay crédito parcial ni un número compuesto que un cliente deba
interpretar.

## Por qué condiciones en lugar de una puntuación

Una versión anterior de esta metodología combinaba distancias de proximidad en una única
puntuación continua. Ese enfoque se retiró: un número compuesto invita a la lectura de que
la plataforma pronostica resultados financieros, cuando lo que realmente mide es
proximidad espacial y diversidad de marca. El sistema basado en condiciones hace ese
límite explícito en el propio mecanismo — el nivel es una clasificación, no una proyección
de ingresos, tráfico peatonal, cuota de mercado, ni una recomendación de adquirir,
desarrollar o arrendar ningún sitio.

## Definiciones de nivel

| Nivel | Nombre | Qué representa |
|---|---|---|
| 1 | Regional | Un ancla mayor de área comercial — se ubica entre los más fuertes a nivel nacional por población de captación primaria |
| 2 | Distrital | Un nodo multiformato significativo — se ubica en el rango superior a nivel nacional por captación primaria |
| 3 | Local | Un centro de ferretería o mayorista con respaldo cívico |
| 4 | Marginal | Cualquier clúster que no supere una condición de Nivel 1–3 |

Los nombres de nivel siguen la jerarquía propia del sector de centros comerciales —
Regional → Distrital → Local — de modo que las etiquetas significan aquí lo mismo que en
el vocabulario de un corredor de arrendamiento.

## Qué debe superar un clúster

Todo nivel exige que se cumplan todas sus condiciones — composición, rango de captación,
rango de gasto donde aplica, respaldo cívico y no solapamiento:

- **Composición** — qué categorías de ancla de capital intensivo deben coexistir. Regional
  exige un ancla de club mayorista o de estilo de vida junto con un hipermercado; Distrital
  exige un hipermercado junto con ferretería o mayorista; Local exige un ancla de
  ferretería o mayorista por sí sola.
- **Rango de población de captación** — la población de captación de cada clúster
  se clasifica frente a todos los demás clústeres *dentro de su propio país*, no
  globalmente, de modo que un clúster de Nivel 1 en un mercado más pequeño se compara con
  la distribución de su propio mercado en lugar de ser penalizado por el tamaño general de
  ese mercado. Regional exige ubicarse entre los clústeres más fuertes a nivel nacional en
  captación primaria (más una verificación de captación secundaria); Distrital exige un
  rango nacional materialmente inferior, pero aún por encima del promedio, en captación
  primaria; Local exige superar un umbral de rango de población de referencia.
- **Rango de gasto** — Distrital exige además que el clúster se ubique en el rango superior
  a nivel nacional en al menos una de varias medidas de gasto del consumidor, no solo en
  población.
- **Respaldo cívico** — un recuento mínimo de hospitales clasificados como regionales o
  locales dentro del anillo exterior de captación del clúster. Regional exige un hospital
  de grado regional; Distrital acepta un hospital regional o distrital; Local acepta
  cualquier hospital clasificado.
- **No solapamiento** — un clúster que se ubica mayormente dentro del área de captación de
  un clúster vecino más fuerte no califica adicionalmente en un nivel inferior para la
  misma geografía. Esto se mide como el solapamiento entre las áreas de captación de los
  dos clústeres; los clústeres Regionales deben ser casi enteramente no solapados con
  cualquier par más fuerte, los clústeres Distritales permiten más solapamiento.

La precisión de los umbrales es deliberadamente gruesa — el objetivo es separar los
clústeres de importancia nacional de los locales, no producir una clasificación numérica
precisa. El refinamiento de umbrales es un área activa de trabajo en curso.

## Qué se excluye deliberadamente

Los formatos de tienda de abarrotes de vecindario (que operan en miles de ubicaciones de
huella reducida por país) no se ingieren como anclas. Su densidad produciría un gran
número de clústeres de bajo valor por debajo de cualquier umbral útil para la selección de
sitios — una decisión de alcance deliberada, no una brecha de cobertura de datos.

## Relación con la plataforma

La asignación de nivel es lo que la [[location-intelligence-platform|interfaz de mapa]]
renderiza directamente — el [[location-intelligence-ux|diseño de Conclusión Primero]]
muestra el nivel de un clúster, no los valores de las condiciones subyacentes, de modo que
un usuario que compara mercados ve primero la conclusión y profundiza en las anclas
subyacentes solo cuando un clúster ha merecido esa atención. [[app-orchestration-gis]]
calcula la asignación de nivel a partir de los datos de clúster depurados; el resultado se
renderiza a través de [[location-intelligence-substrate|la pila de renderizado de la
plataforma]] como la capa de mapa con niveles.

## Información prospectiva

Las declaraciones relativas al refinamiento de umbrales y a futuros cambios de
metodología son objetivos previstos sujetos a cambio. Los plazos reales dependen de la
revisión del operador, la cobertura de datos y la velocidad de desarrollo. [ni-51-102]
[np-51-201]

## Véase también

- [[location-intelligence-platform]] — la plataforma para la que esta metodología clasifica clústeres
- [[app-orchestration-gis]] — el motor que calcula la asignación de nivel
- [[location-intelligence-substrate]] — la arquitectura técnica que almacena y renderiza los clústeres con nivel
- [[location-intelligence-ux]] — el diseño de interfaz que muestra las conclusiones de nivel
