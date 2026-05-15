---
schema: foundry-doc-v1
title: "Tokens de Zona Climática"
slug: climate-zone-tokens
category: design-system
status: stub
bcsc_class: no-disclosure-implication
last_edited: 2026-05-08
editor: pointsav-engineering
language: es
paired_with: climate-zone-tokens.md
cites:
 - ifc-4-3
 - ids-1-0
 - ashrae-90-1
 - nbc-2020
---

Los tokens de zona climática son datos de especificación de rendimiento integrados en el sistema de [[bim-token-what-it-is|Token BIM]]. Cada token registra los requisitos de rendimiento térmico y estructural que aplican a un tipo de elemento IFC determinado dentro de una zona climática registrada. Los datos residen en `tokens/bim/climate-zones.dtcg.json` en el almacén de tokens BIM — ya sea `pointsav-design-system` o un almacén de cliente como `woodfine-design-bim` — y son leídos por `app-orchestration-bim` al arrancar.

## Qué es un token de zona climática

Un token de zona climática no es un valor seleccionable por el usuario. Es dato de referencia: los requisitos de rendimiento que una regulación o norma impone sobre un tipo de elemento específico en una zona climática específica. Cada entrada del token codifica un parámetro de rendimiento (por ejemplo, valor-U máximo) para un tipo de elemento (por ejemplo, `IfcWall`) en una zona (por ejemplo, `ASHRAE-5C`).

## Flujo de resolución del token

La asignación de emplazamiento es el punto de entrada. El emplazamiento del proyecto se vincula a un `IfcSpatialZone` (PredefinedType: `USERDEFINED`, ObjectType: `CLIMATE_ZONE`) con el identificador de zona aplicable. Cuando se coloca un token de elemento, el resolutor de tokens lee `climate-zones.dtcg.json` y encuentra todas las filas en las que `ifc_class` coincide con el tipo de elemento colocado y `zone_id` coincide con la zona asignada al proyecto. Las filas coincidentes se vinculan al elemento como valores de propiedad requeridos y se proyectan en el archivo IFC-SPF como registros `IfcConstraint`.

## Zonas registradas en v0.0.1

| ID de Zona | Descripción | Tipos de elemento cubiertos |
|---|---|---|
| ASHRAE-5C | Marino (Costa Pacífica del Noroeste, costa de BC) | IfcWall, IfcSlab, IfcWindow |
| ASHRAE-6 | Frío | IfcWall, IfcSlab, IfcWindow |
| ASHRAE-7A | Muy frío | IfcWall, IfcSlab |
| NBC-Zone-6 | Clima frío canadiense | IfcWall, IfcSlab, IfcRoof |

Se prevé la incorporación de zonas adicionales en la versión v0.0.3 como parte del conjunto de superposición regulatoria BC RS-1.

## Véase también

- [[bim-token-what-it-is]] — visión general del sistema de Token BIM
- [[bim-token-three-layers]] — cómo se componen las capas de tokens en un proyecto
- [[open-bim-regulatory-acceptance]] — aceptación regulatoria de los registros de conformidad basados en IFC
- [[building-design-system-bim]] — el sistema de diseño que aloja el almacén de tokens

## Referencias

- **IFC 4.3** — ISO 16739-1:2024. Definiciones de esquema `IfcSpatialZone`, `IfcConstraint`, `IfcRelAssociatesConstraint`.
- **IDS 1.0** — buildingSMART Information Delivery Specification, 2024. Formato de contrato para validación de elementos IFC.
- **ASHRAE 90.1-2022** — Energy Standard for Sites and Buildings Except Low-Rise Residential Buildings.
- **NBC 2020** — Código Nacional de Construcción de Canadá, 2020.
