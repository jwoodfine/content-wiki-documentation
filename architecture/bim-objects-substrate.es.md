---
schema: foundry-doc-v1
title: "Objetos BIM — Sustrato"
slug: bim-objects-substrate
short_description: "Los BIM Objects se anclan a la jerarquía de entidades IFC 4.3, la clasificación Uniclass 2015 y URIs bSDD, organizándose en ocho categorías primitivas que codifican especificaciones espaciales, elementales, de materiales, de ensamblajes, de sistemas, de desempeño y de zona climática."
language: es
category: architecture
type: topic
content_type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-17
editor: pointsav-engineering
cites: [ifc-4-3, uniclass-2015, bsdd-v1, ids-1-0, dtcg-w3c]
paired_with: bim-objects-substrate.md
---

La biblioteca de [[bim-objects-what-they-are|Objetos BIM]] del [[building-design-system-bim|Sistema de Diseño de la Construcción]] ancla cada objeto a un nodo en la jerarquía de entidades IFC 4.3, clasificado por Uniclass 2015 y publicado como un URI bSDD dereferenceable. Este artículo describe cómo funciona el [[bim-objects-three-layers|sistema de referencia de tres capas]], qué codifican las ocho categorías de objetos BIM primitivos y cómo un operador BIM los lee y aplica al crear un archivo IFC.

## Tres Capas de Referencia

### Capa 1 — Jerarquía de entidades IFC 4.3

IFC 4.3 fue publicado como ISO 16739-1:2024 en abril de 2024. El estándar define una jerarquía de clases de entidad con nombre — `IfcSite`, `IfcBuilding`, `IfcBuildingStorey`, `IfcSpace`, `IfcWall`, `IfcSlab`, `IfcDoor` y cientos más — cada una con Conjuntos de Propiedades (Psets) tipados que especifican qué atributos debe soportar una implementación conforme.

Cada Objeto BIM del [[building-design-system-bim|Sistema de Diseño de la Construcción]] se mapea a una clase de entidad IFC específica o a un Pset.

### Capa 2 — Nivel de clasificación Uniclass 2015

Uniclass 2015 es el sistema de clasificación unificado para la industria de la construcción del Reino Unido. Los Objetos BIM del Sistema de Diseño de la Construcción llevan una referencia Uniclass 2015 en su campo `$extensions.uniclass`.

### Capa 3 — URIs bSDD

El Diccionario de Datos de buildingSMART (bSDD) publica definiciones JSON-LD legibles por máquinas para propiedades y clasificaciones de construcción, cada una con un URI dereferenceable estable. Los Objetos BIM llevan estos URIs en sus campos `$extensions.bsdd_uri`.

## Ocho Categorías de Objetos BIM Primitivos

El [[building-design-system-bim|Sistema de Diseño de la Construcción]] agrupa los Objetos BIM en ocho categorías, cada una mapeada a una capa distinta del modelo de entidades IFC.

### 1. Espaciales (`bim.spatial.*`)

Sitio, Edificio, Planta y Espacio — la jerarquía `IfcSpatialStructureElement`. Los Objetos BIM en esta categoría codifican alturas entre pisos, área neta mínima por tipo de uso y límites de ocupación.

Archivo fuente: `spatial.dtcg.json`

### 2. Elementos (`bim.elements.*`)

Muros, losas, columnas, vigas, muros cortina, puertas y ventanas — subclases de `IfcProduct`. Los Objetos BIM codifican calificaciones de resistencia al fuego estructural, clases de desempeño acústico, proporciones máximas de acristalamiento y anchos mínimos de puerta.

Archivo fuente: `elements.dtcg.json`

### 3. Materiales (`bim.materials.*`)

Conductividad térmica, densidad, coeficientes de absorción acústica y resistencia a la compresión — `Pset_MaterialCommon` y Psets específicos de materiales.

Archivo fuente: `materials.dtcg.json`

### 4. Conjuntos (`bim.assemblies.*`)

Construcciones de elementos compuestos — conjuntos de muros, conjuntos de piso-techo, conjuntos de cubierta. La transmitancia térmica (valor U) e índice de reducción de sonido (Rw) residen aquí.

Archivo fuente: `assemblies.dtcg.json`

### 5. Sistemas (`bim.systems.*`)

Zonas HVAC, circuitos eléctricos y redes de plomería — `IfcSystem` e `IfcDistributionSystem`. El Objeto BIM central en esta categoría es el principio de autonomía climática por módulo: un Módulo equivale a una zona HVAC.

Archivo fuente: `systems.dtcg.json`

### 6. Desempeño (`bim.performance.*`)

Umbrales de energía, iluminación, accesibilidad y seguridad contra incendios — mínimos regulatorios extraídos de EN 12464-1, EN 17037, ADA 2010, IBC 2021 y ASHRAE 90.1. El Objeto BIM de desempeño más arquitectónicamente significativo es `bim.performance.max-workstation-to-window`, establecido en 6.0 metros.

Archivo fuente: `performance.dtcg.json`

### 7. Zonas climáticas (`bim.climate-zones.*`)

Zonas climáticas ASHRAE 90.1 del 1 al 8, que codifican los umbrales de días-grado de calefacción y refrigeración.

Archivo fuente: `climate-zones.dtcg.json`

### 8. Códigos de identidad (`bim.identity-codes.*`)

Códigos de tipo de uso (serie FFE: M1, M2, B1, L1, A1, C1), códigos de módulo (Módulo A al Módulo H) e índices de plano de planta. La biblioteca de Objetos BIM es el léxico que mapea cada código a su significado geométrico y de programa.

Archivo fuente: `identity-codes.dtcg.json`

## Cómo se Entregan los Objetos BIM

La biblioteca de Objetos BIM se distribuye como un conjunto de archivos JSON en formato DTCG. Una herramienta de autoría BIM o un validador lee los archivos DTCG al inicio y construye un índice de Objetos BIM en memoria. Cualquier dimensión, umbral o clasificación referenciada en una sesión de diseño se resuelve a un valor de Objeto BIM en lugar de un número codificado directamente.

## Relación con el Archivo IFC

La biblioteca de Objetos BIM DTCG no modifica los archivos IFC directamente. Es una referencia en tiempo de autoría — la fuente de verdad para qué valores escribir en un Pset IFC cuando se crea o modifica un elemento del modelo.

La canalización de Objeto BIM a IFC es por lo tanto:

```
Valor de Objeto BIM (bim.performance.max-workstation-to-window = 6.0 m)
        ↓ aplicado en tiempo de autoría
Atributo Pset_SpaceOccupancy en IfcSpace
        ↓ validado en tiempo de entrega
Regla IDS 1.0: IfcSpace.MaxWorkstationToWindow ≤ 6000 mm
```

Esta separación — crear con Objetos BIM, validar con IDS — es el sustrato que hace posible el [[city-code-as-composable-geometry]] en la siguiente capa.

## Véase también

- [[bim-objects-what-they-are]] — la tesis de pre-restricción y cómo los Objetos BIM difieren de los conjuntos de propiedades IFC
- [[bim-objects-three-layers]] — las capas de Especificación, Regulación y Zona Climática y su regla de composición
- [[building-design-system-bim]] — el Sistema de Diseño de la Construcción para el entorno construido
- [[flat-file-bim-leapfrog]] — la arquitectura de archivo plano que sustenta la bóveda de Objetos BIM
