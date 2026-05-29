---
schema: foundry-doc-v1
type: topic
slug: bim-token-taxonomy
short_description: "El Building Design System se organiza en ocho categorías de token primitivos ancladas a IFC 4.3, establece Uniclass 2015 como el piso de clasificación universal, y define 18 componentes centrales en categorías universales de AEC, únicas de consola y únicas de lugar de trabajo."
title: Taxonomía de tokens BIM
audience: vendor-public
bcsc_class: current-fact
language: es
paired_with: bim-token-taxonomy.md
category: reference
---



La taxonomía de tokens BIM de la plataforma organiza el [[building-design-system-bim|Sistema de Diseño de Edificios]] en ocho categorías primitivas ancladas a la jerarquía de entidades de IFC 4.3 (ISO 16739-1:2024). Esta alineación garantiza que los tokens del sistema de diseño correspondan directamente a las convenciones de clasificación AEC universales. Cada token lleva la [[bim-token-three-layers|estructura de tres capas]]: Especificación, Normativa y Zona climática.

## Categorías Primitivas

Las ocho categorías base son:
1. **ESPACIAL (SPATIAL):** Jerarquía de sitio, edificio y plantas.
2. **ELEMENTOS (ELEMENTS):** Componentes físicos (muros, puertas, ventanas).
3. **SISTEMAS (SYSTEMS):** Redes de instalaciones (fontanería, electricidad, clima).
4. **MATERIALES (MATERIALS):** Definiciones y conjuntos de capas de materiales.
5. **ENSAMBLAJES (ASSEMBLIES):** Composiciones jerárquicas y mobiliario.
6. **RENDIMIENTO (PERFORMANCE):** Conjuntos de propiedades (Pset) y cantidades.
7. **IDENTIDAD Y CÓDIGOS:** Referencias de clasificación y normativas.
8. **RELACIONES:** Conectividad y asociaciones semánticas entre elementos.

## Estándar de Clasificación: Uniclass 2015

La plataforma adopta **Uniclass 2015** como su base de clasificación obligatoria. Actúa como el sustrato semántico sobre el cual se pueden añadir otras clasificaciones (como OmniClass o MasterFormat), garantizando que todos los elementos tengan una estructura de datos coherente desde su creación.

## Patrón de Recetas de Componentes

Cada uno de los 18 componentes del sistema se define mediante una "receta" independiente del framework:
- `recipe.html`: Marcado semántico puro.
- `recipe.css`: Estilos encapsulados con BEM.
- `aria.md`: El contrato de accesibilidad e interacción.

Este enfoque permite que cualquier tecnología (Yew, Leptos o TS) pueda implementar los componentes respetando siempre el contrato de diseño y accesibilidad de PointSav.

## Véase también

- [[bim-design-philosophy]]
- [[bim-aec-muscle-memory]]
- [[flat-file-bim-leapfrog]]
- [[bim-token-what-it-is]] — qué es un token BIM y la tesis de pre-condicionamiento
- [[bim-token-three-layers]] — la estructura de tres capas de cada token
