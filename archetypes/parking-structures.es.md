---
schema: foundry-doc-v1
title: "Estructuras de Aparcamiento (PKS)"
slug: parking-structures
category: archetypes
type: concept
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-06-02
editor: pointsav-engineering
paired_with: parking-structures.md
short_description: "Una Estructura de Aparcamiento es un aparcamiento multinivel de 3–9 plantas en un aeropuerto regional o estación de tren interurbano — uno de los tres arquetipos de Inteligencia de Localización. Su relación definitoria: un Mercado Regional alimenta un Mercado Metropolitano en avión o tren."
cites: []
---

Una **Estructura de Aparcamiento** es un aparcamiento multinivel de 3–9 plantas situado en un aeropuerto regional o una estación de tren interurbano. Su función es servir a los residentes de un Mercado Regional que conducen hasta el nodo de tránsito, aparcan el coche y viajan en avión o tren hacia un Mercado Metropolitano.

La relación definitoria: un **Mercado Regional alimenta un Mercado Metropolitano** en avión o en tren. La estructura de aparcamiento es la infraestructura física que hace posible este viaje a escala.

Código de tres letras: **PKS**. Uno de los tres arquetipos de Inteligencia de Localización junto a los [[professional-centres|Centros Profesionales (PRO)]] y los [[vertical-warehouse|Almacenes Verticales (VWH)]].

## La relación regional-metropolitana

Un sitio PKS se sitúa en el vértice entre dos tipos de mercado:

- **Mercado Regional** — la ciudad o suburbio donde viven y compran los usuarios de la estructura de aparcamiento (capturado por el sistema de clústeres T1/T2/T3 PRO existente)
- **Mercado Metropolitano** — la gran ciudad a la que esos usuarios viajan en avión o tren

La estructura PKS existe porque el viaje entre ambos es suficientemente largo como que conducir hasta el nodo de tránsito y aparcar es mejor que conducir hasta la metrópoli. Este umbral es de aproximadamente 15–150 km:

| Distancia al área metropolitana | Viabilidad PKS |
|---|---|
| ≤15 km | Demasiado cerca — suburbio; conducir hasta la metrópoli es más rápido |
| 15–100 km | Zona PKS óptima — 1–2 horas en coche; el tránsito ahorra tiempo significativo |
| 100–150 km | Viable si el tránsito es rápido (alta velocidad, vuelo directo) |
| >150 km | Mercado independiente; puede tener su propia relación metropolitana |

## Tipos de ancla de tránsito

### Aeropuertos regionales

Un aeropuerto regional se distingue de un gran hub por:
- Servir principalmente rutas domésticas o destinos internacionales de corta distancia
- Volumen de pasajeros típicamente 500.000–5.000.000 anuales
- Ubicado a 15–150 km de un centro metropolitano
- Sin clúster de Centros Profesionales T1 inmediatamente adyacente

**Excepciones nacionales:**
- México: Sin ferrocarril interurbano nacional de pasajeros — PKS es sólo aeroportuario
- Islandia: Sin ferrocarril de pasajeros — sólo aeroportuario

### Estaciones de tren interurbano

Una estación de tren interurbano sirve trenes que viajan 30–150 km hasta un gran centro metropolitano. Se distingue de estaciones de metro/subterráneo, andenes de cercanías y paradas de tranvía.

**Operadores interurbanos nacionales por país:**

| País | Operador |
|---|---|
| EE.UU. | Amtrak |
| CA | VIA Rail Canada |
| FR | SNCF (TGV, Intercités, TER) |
| DE | Deutsche Bahn (ICE, IC, EC, RE, RB) |
| ES | Renfe (AVE, Alvia, Regional) |
| IT | Trenitalia, Italo |
| AT | ÖBB (Railjet, Intercity) |
| NL | NS |
| SE | SJ |
| DK | DSB |
| NO | Vy (antes NSB) |
| FI | VR Group |
| PT | CP (Comboios de Portugal) |
| PL | PKP Intercity, RegioJet |

## Señales de co-localización para selección de sitio

**Esenciales:**

| Señal | Umbral | Justificación |
|---|---|---|
| Ancla de tránsito regional | ≤3 km | Aeropuerto o estación interurbana con servicio directo a la metrópoli |
| Aislamiento metropolitano | 15–150 km | Define la relación regional |
| Clúster PRO T1 o T2 | ≤10 km | El Mercado Regional cuya población genera demanda de aparcamiento |
| Acceso por vía multicarril | ≤1 km | El flujo de entrada/salida requiere capacidad arterial |
| Población regional | ≥150.000 | Demanda mínima para la viabilidad de la estructura |

## Resultados de pruebas actuales — al 2026-06-01

**6.640 candidatos PKS** en 17 países. "Integrados" = candidato PKS con un clúster PRO T1/T2 en un radio de 10 km — los sitios de mayor valor:

| País | Total | Integrados | % Integración |
|---|---|---|---|
| EE.UU. | 3.678 | 1.071 | 29% |
| DE | 547 | 216 | 39% |
| CA | 421 | 133 | 32% |
| FR | 405 | 97 | 24% |
| GB | 338 | 129 | 38% |
| IT | 245 | 41 | 17% |
| MX | 214 | 28 | 13% |
| ES | 189 | 27 | 14% |
| PL | 143 | 24 | 17% |

Estos recuentos se espera que se reduzcan sustancialmente una vez que `ingest-osm-airports.py` aplique el filtro IATA/aerodrome:type, eliminando aeródromos privados y de aviación general. Los datos de estaciones ferroviarias añadirán entonces un conjunto complementario de candidatos PKS de estaciones interurbanas.
