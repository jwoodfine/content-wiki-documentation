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
language_protocol: TRANSLATE-ES
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

## Conjunto de datos de producción

El sistema de producción PKS utiliza clústeres DBSCAN de infraestructura de tránsito — aeropuertos comerciales, estaciones de tren interurbano, ferrocarril de cercanías, estaciones de metro/suburbano y terminales de autobús interurbano — enriquecidos con señales comerciales: alquiler de vehículos, aparcamientos de disuasión y hoteles.

**7.045 clústeres** en 17 países de visualización según la versión de producción de junio de 2026:

| Nivel | Recuento | Proporción |
|---|---|---|
| T1 Centro Comercial Confirmado | 692 | 9,8% |
| T2 Centro Drive-to | 2.665 | 37,8% |
| T3 Parada de Tránsito Funcional | 3.688 | 52,4% |

Las estaciones ferroviarias dominan el conjunto de datos en todos los países. El patrón europeo de aparcamiento y tren (*park-and-train*) implica que los sitios de ferrocarril interurbano superan con creces a los aeroportuarios en la UE; las estaciones ferroviarias son candidatos PKS fiables allí donde el servicio interurbano alcanza ciudades regionales.

## Clasificación por niveles

Los niveles PKS utilizan un **modelo de colapso por grupo de modos** que evita la doble contabilización de la infraestructura de tránsito en el mismo nodo físico. Una estación que ofrece tanto servicio ferroviario interurbano como de cercanías en el mismo andén cuenta como un grupo de modo de tránsito (FERROCARRIL), no dos. Un verdadero intercambiador multimodal debe tener tipos modales distintos — aeropuerto más ferrocarril, por ejemplo — para contar como multimodal.

Se reconocen cuatro grupos de modos de tránsito: AÉREO (aeropuertos), FERROVIARIO (ferrocarril interurbano y de cercanías combinados), URBANO (metro y suburbano) y BUS (terminales de autobús interurbano).

No todos los clústeres de tránsito califican como Estructuras de Aparcamiento. Las paradas urbanas de acceso a pie sin infraestructura comercial de acceso en vehículo quedan excluidas por un criterio de calificación: un clúster califica cuando tiene un ancla aeroportuaria (inherentemente drive-to), múltiples grupos modales distintos, o señales de enriquecimiento comerciales que indican comportamiento drive-to (alquiler de vehículos o aparcamiento de disuasión).

**T1 Centro Comercial Confirmado:** Aeropuerto con alquiler de vehículos u hotel presentes, tres o más grupos modales distintos, o un aeropuerto con al menos una señal de enriquecimiento. Son los sitios de aparcamiento y viaje con mayor nivel de confianza.

**T2 Centro Drive-to:** Ancla aeroportuaria sin el pleno enriquecimiento comercial de T1, o sitio multimodal con al menos una señal de enriquecimiento. Fuertes candidatos PKS con evidencia directa de comportamiento drive-to.

**T3 Parada de Tránsito Funcional:** Grupo modal único con una señal de enriquecimiento que califica el sitio como drive-to en lugar de acceso a pie. La infraestructura de tránsito está presente; el ecosistema comercial completo de los niveles superiores aún no está consolidado.

## Referencias

- [Aparcamiento de disuasión](https://en.wikipedia.org/wiki/Park_and_ride) — Wikipedia, acceso 2026-06-14

*Contenido de Wikipedia reproducido bajo [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).*
