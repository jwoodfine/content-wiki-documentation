---
schema: foundry-doc-v1
type: topic
slug: bim-token-taxonomy
title: Taxonomía de Tokens BIM
audience: vendor-public
bcsc_class: current-fact
language: es
paired_with: bim-token-taxonomy.md
---

# Taxonomía de Tokens BIM

La taxonomía de tokens BIM de Foundry organiza el sistema en ocho categorías primitivas ancladas a la jerarquía de entidades de IFC 4.3 (ISO 16739-1:2024). Esta alineación garantiza que los tokens del sistema de diseño correspondan directamente a las convenciones de clasificación AEC universales.

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

Foundry adopta **Uniclass 2015** como su base de clasificación obligatoria. Actúa como el sustrato semántico sobre el cual se pueden añadir otras clasificaciones (como OmniClass o MasterFormat), garantizando que todos los elementos tengan una estructura de datos coherente desde su creación.

## Patrón de Recetas de Componentes

Cada uno de los 18 componentes del sistema se define mediante una "receta" independiente del framework:
- `recipe.html`: Marcado semántico puro.
- `recipe.css`: Estilos encapsulados con BEM.
- `aria.md`: El contrato de accesibilidad e interacción.

Este enfoque permite que cualquier tecnología (Yew, Leptos o TS) pueda implementar los componentes respetando siempre el contrato de diseño y accesibilidad de PointSav.
