---
schema: foundry-doc-v1
title: "Inteligencia de ubicación: recopilación de datos"
slug: collect-location-intelligence-data
category: how-to
content_type: how-to
type: how-to
quality: complete
short_description: "Cómo se añaden nuevas cadenas comerciales y de infraestructura a la taxonomía del pipeline de inteligencia de ubicación, y cómo el pipeline ingesta sus datos de ubicación desde OpenStreetMap."
status: active
audience: vendor-internal
bcsc_class: no-disclosure-implication
language_protocol: TRANSLATE-ES
last_edited: 2026-07-11
editor: pointsav-engineering
paired_with: collect-location-intelligence-data.md
research_trail:
  sources: [pointsav-monorepo app-orchestration-gis taxonomy.py, config.py, ingest-osm.py]
  verification_method: "re-verified 2026-09-05 against app-orchestration-gis: build-vwh-clusters.py does not exist under that name; test-cluster-archetypes.py, build-clusters.py, and export-clusters-ols.py do"
---

El pipeline de inteligencia de ubicación clasifica ubicaciones comerciales y de infraestructura en dos arquetipos — Vertical Warehouse (VWH) y Parking Structures (PKS) — comparando los registros de OpenStreetMap contra una taxonomía de cadenas mantenida. Este manual cubre cómo extender esa taxonomía a una nueva cadena, país o categoría de infraestructura, y cómo volver a ejecutar los pasos de ingesta y agrupación (clustering) que siguen.

Directorio de trabajo para todos los comandos: `app-orchestration-gis/` (dentro del clon del monorepo de GIS).

## Requisitos previos

- Acceso a la API de Overpass (las consultas se ejecutan a través del script de ingesta OSM del pipeline; no se requiere clave de API)
- Python 3.11+ con las dependencias del pipeline instaladas
- La ruta del directorio de datos del despliegue activo configurada

## Propósito

Añadir una nueva cadena, país o categoría de infraestructura a la taxonomía de inteligencia de ubicación, ingestar sus registros de OpenStreetMap, y volver a ejecutar la compilación de agrupación para que los nuevos datos se reflejen en las salidas de arquetipo VWH/PKS.

## Procedimiento

1. **Verifique que el pipeline esté limpio** importando los módulos de taxonomía y configuración y confirmando que ambos cargan sin error.

2. **Añada una nueva cadena a la taxonomía.** Cada cadena se declara en su propio registro YAML: un identificador de cadena, país y región, una categoría (asignada a un código NAICS), el nombre legal canónico del minorista y su empresa matriz, un identificador público usado para vincular con registros de OpenStreetMap (típicamente un QID de Wikidata a través de la etiqueta OSM `brand:wikidata`), y un número aproximado de tiendas usado solo como verificación de cordura sobre los resultados de ingesta — nunca como entrada para la calificación de nivel. Una cadena que abarca varios países se marca como tal en lugar de duplicarse por país.

3. **Registre la categoría de la cadena en el módulo de taxonomía**, si introduce una categoría que aún no existe. Cada categoría lleva una etiqueta, un código NAICS y una nota sobre a qué señal de arquetipo contribuye (VWH o PKS) — ninguna de estas categorías condiciona por sí sola la lógica de nivel de arquetipo; la asignación de nivel es un paso posterior independiente.

4. **Ejecute la ingesta OSM para la(s) nueva(s) cadena(s).** El script de ingesta consulta Overpass en busca de las ubicaciones etiquetadas de la cadena y escribe los resultados en el directorio de datos comerciales del pipeline. Si una cadena devuelve cero registros, verifique si la cobertura de la etiqueta Wikidata es escasa en OSM para esa cadena y añada una consulta de respaldo basada en nombre a su registro YAML.

5. **Para una nueva categoría de infraestructura** (por ejemplo, aeropuertos comerciales o estaciones de tren interurbano, a diferencia de una cadena minorista), escriba un script de ingesta dedicado siguiendo el patrón de ingesta de infraestructura existente: una consulta de Overpass acotada a las etiquetas `aeroway`/`railway` relevantes, filtrada para excluir subtipos fuera de alcance (pistas de aterrizaje privadas y campos militares para aeropuertos; metro, tren ligero y tranvía para estaciones de ferrocarril), con enriquecimiento por operador o código IATA por país donde el etiquetado de origen lo permita.

6. **Vuelva a ejecutar la compilación de agrupación** una vez que todas las nuevas ingestas de cadenas e infraestructura estén en su lugar, usando los scripts de compilación de clústeres DBSCAN del pipeline para cada arquetipo. Copie las salidas al directorio de datos del despliegue activo y confirme que los nuevos recuentos de clústeres estén en o por encima de la línea base de producción anterior — una caída por debajo de la línea base indica una regresión de ingesta o taxonomía, no un resultado esperado de añadir datos.

## Resultado esperado

La nueva cadena, país o categoría de infraestructura aparece en la salida de ingesta OSM del arquetipo con un recuento de registros verosímil para su escala real, y la compilación de agrupación posterior produce recuentos de clústeres en o por encima de la línea base de producción anterior del pipeline.

## Verificación

Cuente los registros en el archivo de salida de cada cadena recién ingestada y compárelos contra la escala real de la cadena como verificación de cordura, no como un objetivo exacto. Confirme que los recuentos de características de salida de la compilación de agrupación para VWH y PKS estén en o por encima de su última línea base de producción conocida antes de considerar la ejecución completa.

## Reversión

Un nuevo YAML de cadena o una entrada de categoría de taxonomía puede eliminarse y la ingesta volver a ejecutarse sin efectos secundarios — el paso de ingesta es idempotente por cadena. La compilación de agrupación puede volver a ejecutarse en cualquier momento a partir de sus entradas existentes; no necesita revertirse, solo volver a ejecutarse una vez que la corrección de taxonomía esté en su lugar.

## Próximos pasos

- [[connect-osm-data-pipeline]] — la vía de ingesta genérica de una sola cadena que este manual extiende

## Véase también

- Urban Fringe — el modelo de arquetipo VWH y la taxonomía de cadenas
- Commuter — el modelo de arquetipo PKS y la taxonomía de cadenas
- Arquetipos de inteligencia de ubicación (projects.woodfinegroup.com/site-selection) — descripción general PRO/VWH/PKS e integración de mapas
- [[connect-osm-data-pipeline]] — ingesta genérica de una sola cadena para nuevas categorías minoristas
