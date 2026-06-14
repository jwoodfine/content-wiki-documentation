---
schema: foundry-doc-v1
title: "Objetos BIM — Tres capas de composición"
slug: bim-objects-three-layers
short_description: "Los BIM Objects incrustan tres capas de restricción simultáneas — Especificación (identidad permanente del elemento), Regulación (requisitos específicos de jurisdicción) y Zona Climática (requisitos de desempeño) — como datos de referencia estática con una regla de composición que aplica el valor más restrictivo."
language: es
category: architecture
type: topic
content_type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-17
editor: pointsav-engineering
cites: [ifc-4-3, uniclass-2015, bsdd-v1, ids-1-0, dtcg-w3c, ashrae-90-1, nbc-2020]
paired_with: bim-objects-three-layers.md
---

Un [[bim-objects-what-they-are|Objeto BIM]] tiene tres capas: Especificación, Regulación y Zona Climática. Las tres son datos integrados en el objeto. Ninguna de las tres capas es una opción seleccionable por el usuario en tiempo de ejecución — un diseñador no "cambia" entre zonas climáticas del mismo modo que no cambia de códigos de construcción. Las tres capas se muestran simultáneamente como tablas de referencia estáticas, cada una mostrando todas las superposiciones registradas para el tipo de elemento del Objeto BIM. Esta estructura refleja una realidad física: un elemento construido tiene un tipo fijo (Especificación), existe en una jurisdicción fija (Regulación) y se desempeña en un clima fijo (Zona Climática).

## Por qué Tres Capas

Los tokens de los [[design-system-substrate|sistemas de diseño]] de software típicamente tienen dos preocupaciones: qué ES un valor (su rol semántico) y a qué valor se resuelve (su resultado calculado). Los Objetos BIM abordan un espacio de problemas fundamentalmente diferente que requiere tres preocupaciones.

Una especificación de elemento del entorno construido debe responder simultáneamente:
- **¿Qué es este elemento?** — su tipo en un esquema neutral e independiente de herramientas (IFC), su clasificación en un sistema de referencia neutral (Uniclass), y su identidad semántica en un diccionario que abarca jurisdicciones (bSDD).
- **¿Qué requiere la jurisdicción de él?** — los requisitos regulatorios específicos impuestos por la ley del lugar donde se ubica el edificio. Varían por jurisdicción, cambian cuando se actualizan las regulaciones y pueden incluir restricciones geométricas que no pueden expresarse como valores numéricos.
- **¿Qué requiere el clima de él?** — los requisitos de desempeño térmico, de humedad y estructural impuestos por el clima físico del sitio.

## Capa 1 — Especificación

La capa de Especificación es la identidad permanente del objeto. No varía según la jurisdicción o el clima.

**Campos:**

| Campo | Contenido | Formato |
|---|---|---|
| `ifc_class` | Clase de entidad IFC 4.3 | `IfcWall`, `IfcSlab`, etc. |
| `uniclass_ref` | Código Uniclass 2015 | `Ss_20_05_30_75` |
| `bsdd_uri` | URI de concepto bSDD | `https://identifier.buildingsmart.org/...` |
| `description` | Descripción en lenguaje llano | Texto libre, máx. 280 caracteres |
| `applicable_psets` | Conjuntos de Propiedades IFC aplicables | Array de nombres Pset |

## Capa 2 — Regulación

La capa de Regulación contiene requisitos específicos de la jurisdicción. Es una tabla de superposiciones registradas — una fila por jurisdicción por restricción.

**Por qué una tabla, no un menú desplegable.** Un requisito regulatorio es un hecho sobre la jurisdicción donde se ubica un edificio, no una elección que hace un diseñador. El objeto muestra los requisitos de todas las jurisdicciones registradas como datos de referencia, del mismo modo que una hoja de datos de estándares técnicos muestra múltiples filas de normas nacionales lado a lado.

**Filas de ejemplo para `IfcWall` (muro exterior, residencial):**

| Jurisdicción | Estándar | Parámetro | Valor requerido | Unidad |
|---|---|---|---|---|
| CA-BC | NBC 2020 Parte 11 | Resistencia térmica (muro opaco) | ≥ RSI 3.85 | m²K/W |
| DE | EnEV 2020 | Transmitancia térmica (valor U) | ≤ 0.28 | W/m²K |
| SG | SGBC BCA Green Mark | Transmitancia térmica (OTTV) | ≤ 45 | W/m² |
| US-VA (federal) | ASHRAE 90.1-2022 | Factor U del conjunto (zona climática 4A) | ≤ 0.124 | Btu/h·ft²·°F |

**Estado vacío.** En v0.0.1, la mayoría de los Objetos BIM no tienen superposiciones registradas — la estructura de superposición está definida pero sin datos. El hito v0.0.3 está planificado para entregar el primer conjunto de superposiciones: requisitos de zonificación residencial BC RS-1.

## Capa 3 — Zona Climática

La capa de Zona Climática contiene requisitos de desempeño basados en el clima. Es una tabla de filas de zonas climáticas registradas — todas las zonas mostradas simultáneamente.

**Filas de ejemplo para `IfcWall` (muro exterior):**

| ID de Zona | Parámetro | Valor requerido | Unidad | Fuente |
|---|---|---|---|---|
| ASHRAE-4A | Factor U del conjunto (muro de estructura de acero) | ≤ 0.064 | Btu/h·ft²·°F | ASHRAE 90.1-2022 Tabla 5.5-4 |
| ASHRAE-5C | Factor U del conjunto (muro de masa) | ≤ 0.104 | Btu/h·ft²·°F | ASHRAE 90.1-2022 Tabla 5.5-5 |
| NBC-Zone-6 | Resistencia térmica efectiva (muro sobre el nivel del suelo) | ≥ RSI 4.91 | m²K/W | NBC 2020 |

## Regla de Composición

Cuando Regulación y Zona Climática especifican una restricción numérica sobre el mismo parámetro de desempeño, el requisito efectivo es el valor más restrictivo.

```
effective_value = max(regulation_requirement, climate_zone_requirement)
```

Esta es una composición de límite inferior: ambas capas expresan mínimos de desempeño. El máximo de los dos mínimos es el requisito vinculante.

**Precedencia incondicional de la exclusión geométrica.** Un fragmento de exclusión geométrica IFC en cualquier superposición no puede ser anulado por ninguna restricción numérica.

**Fallo abierto.** Cuando una capa no tiene datos registrados para un tipo de elemento dado, el objeto permanece válido. La capa de Especificación siempre está presente; las capas de Regulación y Zona Climática son adiciones opcionales.

## El Modelo de Autoría CMS de Cuatro Zonas

Cuando se crea un nuevo Objeto BIM, la interfaz de autoría sigue un modelo de cuatro zonas que se corresponde directamente con las tres capas del objeto más una zona de flujo de trabajo de publicación.

La interfaz CMS es la interfaz prevista para `app-console-bim` (planificado, v0.1.x). En v0.0.1, los [[bim-objects-what-they-are|Objetos BIM]] se crean directamente como archivos JSON DTCG y se confirman mediante git.

## Véase también

- [[bim-objects-what-they-are]] — qué es un Objeto BIM y cómo difiere de los tipos de entidad IFC, familias de Revit y conjuntos de propiedades
- [[bim-objects-substrate]] — las ocho categorías de Objetos BIM primitivos y su formato de entrega DTCG
- [[open-bim-regulatory-acceptance]] — cómo las jurisdicciones adoptan los estándares BIM abiertos
- [[building-design-system-bim]] — el Sistema de Diseño de la Construcción para el entorno construido
