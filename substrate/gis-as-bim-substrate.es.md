---
schema: foundry-doc-v1
title: "El SIG como sustrato del BIM"
slug: gis-as-bim-substrate
language: es
category: substrate
index_group: core-named-substrates
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-26
editor: pointsav-engineering
short_description: "Qué ofrece el conjunto de datos de coubicación a una tubería de composición BIM: el manifiesto de agrupaciones y sus campos enlazables, la profundidad de resolución regional, las capas de contexto cívico y las garantías de estabilidad con las que puede contar un consumidor posterior."
cites: []
paired_with: gis-as-bim-substrate.md
---

El modelado de información de edificación opera a escala de edificio: geometría estructural, conjuntos de materiales, sistemas mecánicos, ocupación. Un modelo tiene sentido de forma aislada, pero su valor comercial aparece cuando se *emplaza*: situado en una geografía real, con vecinos reales, áreas de captación reales y contexto normativo real. El conjunto de datos de coubicación del [[location-intelligence-substrate|sustrato de inteligencia de localización]] está diseñado para aportar ese contexto de emplazamiento a una tubería de composición BIM.

**Por qué importa:** dos sustratos que comparten sistema de coordenadas y libro de registro pueden unirse por una clave en lugar de reconciliarse a mano, y eso es lo que convierte «dónde está este edificio» en una propiedad consultable del modelo y no en un documento aparte.

Este artículo documenta qué ofrece el conjunto de datos a un consumidor BIM, qué campos son estables y qué extensiones se prevén.

## El manifiesto de agrupaciones

La salida principal es un manifiesto de unas 6.400 agrupaciones comerciales de coubicación deduplicadas en Estados Unidos, Canadá, México, el Reino Unido y Europa continental. Cada agrupación porta un identificador estable y una posición geográfica fija, el nombre regional resuelto por el [[regional-name-resolution-architecture|motor de límites por capas]], una clasificación por nivel, su composición categórica y los recuentos de tiendas dentro de radios de captación anidados de uno, dos y tres kilómetros.

Para un consumidor BIM, el manifiesto responde preguntas que el modelo por sí solo no puede: qué densidad comercial hay en los tres kilómetros alrededor del edificio propuesto, qué formatos de ancla sirven ya a la captación y cuál es el emplazamiento existente equivalente más próximo contra el que comparar el modelo.

**Por qué importa:** son las preguntas que deciden si merece la pena diseñar un edificio, y hasta ahora vivían en el informe de un consultor y no en un conjunto de datos consultable.

## Propiedades disponibles para la ingesta BIM

| Campo | Tipo | Uso en BIM |
|---|---|---|
| `cluster_id` | cadena | Clave de unión estable |
| `latitude`, `longitude`, `centroid_lat`, `centroid_lon` | flotante | Posiciones de ancla y centroide para el emplazamiento |
| `region_name` | cadena | Nombre metropolitano o municipal resuelto; útil como parámetro del modelo |
| `tier_descriptor` | cadena | Regional / Distrito / Local / Periférico — señal de densidad |
| `count_1km`, `count_3km` | entero | Densidad de captación |
| `unique_brands` | entero | Marcas minoristas distintas en la captación |
| `merged_zones` | matriz | Agrupaciones de la misma zona consolidadas; se muestran por transparencia |
| `iso`, `state` | cadena | Códigos jurisdiccionales |

El manifiesto se publica en PMTiles, con un esquema de capas que admite posiciones de tienda individuales (capa 1) y envolventes de agrupación con anillos de proximidad (capa 2). Un consumidor puede obtener el manifiesto GeoJSON para acceso directo a coordenadas, o leer los PMTiles mediante solicitudes de rango de bytes para consultas indexadas espacialmente.

**Por qué importa:** el consumidor no necesita base de datos ni clave de API — el conjunto de datos es un archivo que puede leer directamente, en línea con la postura de archivos planos del sustrato.

## Profundidad de resolución regional

El motor de límites resuelve las coordenadas a una de cinco granularidades, de la más específica a la más general: GADM admin-3 (aproximaciones a las subdivisiones censales canadienses, municipios mexicanos); GADM admin-2 cuando no hay admin-3; NUTS-3 de Eurostat para las regiones europeas; áreas metropolitanas censales de Statistics Canada o áreas estadísticas basadas en núcleo del censo estadounidense; y admin-1 de Natural Earth como reserva global de estado o provincia.

Una composición que necesita anclarse a una jurisdicción municipal recibe ese nivel de resolución; una que solo necesita un marco metropolitano de referencia recibe el área circundante.

**Por qué importa:** la resolución jurisdiccional es lo que permite seleccionar automáticamente una [[city-code-as-composable-geometry|capa normativa]] en vez de elegirla a mano en cada proyecto.

## Capas de contexto cívico

Además del manifiesto, dos capas cívicas resultan relevantes para programas edificatorios que dependen de la adyacencia cívica: un catálogo de unas 28.000 ubicaciones hospitalarias en el ámbito operativo y otro de unas 19.000 ubicaciones de educación superior, ambos procedentes de OpenStreetMap. La distancia al hospital y a la universidad más próximos se calcula por agrupación dentro de un límite práctico de cinco kilómetros.

**Por qué importa:** para un programa adyacente a un hospital o a un campus, esas distancias son entradas directas del modelo y no contexto que alguien deba investigar por separado.

## Garantías de estabilidad

**Estables entre versiones:** los identificadores de agrupación, la estructura del manifiesto, el esquema de clasificación por niveles, el algoritmo de resolución de nombres regionales y los radios de captación.

**Sujetos a cambio:** el tamaño de la taxonomía de familias de marca (las familias de alimentación y farmacia están en expansión), los recuentos absolutos de tiendas (la cobertura de OpenStreetMap mejora año a año) y el conjunto de países incluidos.

Una composición que se une por `cluster_id` verá crecimiento pero ninguna eliminación de identificadores existentes. Una que se una por `region_name` debe contar con que los valores de texto varíen ligeramente conforme se refine el motor de regiones.

**Por qué importa:** el consumidor puede decidir sobre qué campos es seguro construir antes de escribir la unión, en lugar de descubrir un cambio incompatible tras una reconstrucción.

## Véase también

- [[location-intelligence-substrate]] — la arquitectura SIG de archivos planos que produce este conjunto de datos
- [[regional-name-resolution-architecture]] — cómo se resuelve `region_name`
- [[city-code-as-composable-geometry]] — la capa jurisdiccional que selecciona la región resuelta
- [[service-business-clustering]] — el servicio de agrupación que produce el manifiesto
