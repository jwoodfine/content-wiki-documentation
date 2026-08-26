---
schema: foundry-doc-v1
title: "Esquema de datos de puntos de interés"
slug: poi-data-schema
language: es
category: services
index_group: specialist-and-domain-services
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-26
editor: pointsav-engineering
short_description: "Las estructuras de registro de los datos de localización ingeridos de OpenStreetMap y de Overture Maps Foundation, normalizadas en un esquema JSONL unificado antes del análisis de agrupaciones. Los QID de Wikidata son el identificador principal de cadena, y un modelo padre-hijo resuelve los servicios auxiliares comarcados."
cites: [overture-maps]
paired_with: poi-data-schema.md
---

El esquema de datos de puntos de interés define la estructura de registro de las dos clases de datos de localización que consume el [[location-intelligence-substrate|sustrato de inteligencia de localización]]: ubicaciones de cadenas minoristas ingeridas de OpenStreetMap y ubicaciones de anclas institucionales ingeridas de Overture Maps Foundation. Ambas se normalizan en un esquema JSONL plano y unificado antes de ejecutar el [[service-business-clustering|análisis de agrupaciones]].

**Por qué importa:** no se requiere comprar datos propietarios. Todo registro procede de una fuente con licencia pública y es versionable en el mismo libro que el resto de la plataforma, de modo que el conjunto de datos de localización de un cliente es auditable de principio a fin.

## Tipos de registro

Los **registros de negocio de servicio** representan ubicaciones individuales de cadenas minoristas — ferreterías, clubes de almacén, hipermercados, anclas de alimentación. Cada uno se identifica por una clave `chain_id`, que lo enlaza a un archivo de configuración de cadena, y por un campo `brand_wikidata` con el QID de Wikidata de la marca.

Los **registros de lugares de servicio** representan anclas institucionales — hospitales, universidades, aeropuertos — ingeridas de Overture Maps mediante el campo de categoría `taxonomy.primary`. Estos usan una clave `category_id` (`hospital`, `university`, `airport`) en lugar de `chain_id`.

## Campos comunes

| Campo | Tipo | Notas |
|---|---|---|
| `location_name` | cadena | Nombre visible; COALESCE de nombre de marca y categoría de reserva |
| `brand_wikidata` | cadena o nulo | QID de Wikidata (p. ej. `Q13556979`); nulo en lugares cívicos sin marca |
| `street_address` | cadena o nulo | Dirección libre desde `addr:housenumber` + `addr:street` de OSM, o direcciones de Overture |
| `city` | cadena o nulo | Localidad desde `addr:city`, `addr:town` o `addr:municipality` |
| `region` | cadena o nulo | Provincia, estado o región NUTS-3 |
| `iso_country_code` | cadena | ISO 3166-1 alfa-2 |
| `latitude` | flotante | WGS 84, 7 decimales |
| `longitude` | flotante | WGS 84, 7 decimales |
| `naics_code` | cadena | Clasificación sectorial NAICS |
| `top_category` | cadena | Descripción de la categoría NAICS de nivel superior |
| `sub_category` | cadena | Descripción de la subcategoría NAICS |
| `source` | cadena | `osm` u `overture` |
| `confidence` | flotante | Puntuación de confianza (OSM: fija 0,85; Overture: del conjunto de datos) |

**Por qué importa:** un único conjunto de campos compartido entre ambas clases significa que el código de análisis posterior no se bifurca por tipo de registro salvo en la clave de cadena frente a la de categoría.

## Identificación de cadena y el QID de Wikidata

Los QID de Wikidata son persistentes, independientes del idioma y mantenidos por una comunidad global, lo que los convierte en el identificador de cadena preferido tanto en conjuntos comerciales como abiertos: operan a nivel de marca y no de nombre, así que dos tiendas escritas de forma distinta que comparten QID pertenecen a la misma cadena.

La comunidad de OpenStreetMap etiqueta las ubicaciones minoristas con `brand:wikidata=<QID>`, y la ingesta usa esa etiqueta como filtro principal de consulta: una ubicación etiquetada con el QID correcto se captura con independencia de las variantes locales de escritura. Overture Maps expone la misma identidad mediante `brand.wikidata` en su esquema de Places, extraído durante la ingesta para los registros de lugares de servicio.

**Por qué importa:** la identidad de cadena sobrevive a la traducción, al cambio de rótulo de un local y a la introducción inconsistente de datos, que es lo que hace posible la comparación transfronteriza.

## Esquema de taxonomía de Overture

Overture Maps declaró obsoleta la estructura `categories` en noviembre de 2025 y la retiró en la versión de junio de 2026. La estructura `taxonomy` que la sustituye expone `taxonomy.primary` (equivalente a `categories.primary`) y `taxonomy.alternate`, una matriz de asociaciones de categoría secundaria con estructuras de atributo opcionales. Los identificadores de categoría no cambian: una consulta que antes leía `categories.primary = 'hospital'` pasa a ser `taxonomy.primary = 'hospital'` sin alterar los valores del filtro.

## Deduplicación espacial

Los datos de OSM sobre grandes superficies incluyen a veces tanto un nodo como una vía para la misma ubicación física: la huella del edificio como vía y la entrada como nodo. La ingesta deduplica redondeando las coordenadas a cuatro decimales (unos 11 metros) y tratando como el mismo edificio los registros que redondean al mismo par, conservando el de campos de dirección más completos.

Los registros que comparten coordenadas a esa resolución pero llevan valores distintos de `chain_id` bajo el mismo QID `brand_wikidata` se tratan como tiendas de subformato o comarcadas — una gasolinera que comparte el QID del minorista matriz, por ejemplo — y son candidatos al modelo padre-hijo.

**Por qué importa:** sin este paso, una sola tienda puede aparecer dos o tres veces e inflar todos los recuentos calculados a partir de ella.

## Modelo padre-hijo de sububicaciones

Las grandes superficies operan con frecuencia servicios auxiliares en la misma dirección: farmacias, gasolineras, ópticas, centros de jardinería. En los datos brutos de OSM aparecen como elementos POI separados, cada uno con nombre propio y a veces con `chain_id` propio.

Una correspondencia de padres dirigida por configuración lo resuelve: cada `chain_id` de subentidad conocido como servicio auxiliar se asigna a su cadena matriz canónica. Las subentidades quedan excluidas de la puntuación de agrupaciones y solo se muestran en la ficha de la matriz; el mapa presenta un marcador por ubicación matriz.

El estándar Placekey — un identificador global de ubicación con estructura `What@Where` — expresa la misma relación mediante un componente `Where` compartido: dos POI en una misma dirección comparten el sufijo de geocelda mientras difiere el prefijo de marca. Un emparejamiento espacial basado en Placekey es un mecanismo futuro previsto y no el actual; el esquema conserva un campo `placekey` para ello, aún sin poblar durante la ingesta.

**Por qué importa:** contar la gasolinera de un hipermercado como ancla independiente inflaría la diversidad aparente de marcas de la agrupación, que es la señal sobre la que se construye el sistema de niveles.

## Completitud de direcciones

La cobertura de direcciones varía por país: la de `addr:housenumber` y `addr:street` en OSM es sólida en Europa occidental y Canadá, moderada en Estados Unidos y escasa en algunos mercados nórdicos y del sur de Europa. Está prevista una mejora que una espacialmente los registros POI con el tema de Direcciones de Overture dentro de un radio de 15 metros para completar las direcciones ausentes; ese tema aporta registros estructurados de más de dos mil millones de direcciones derivadas de registros nacionales autoritativos.

## Cadencia de actualización

Los registros de negocio de servicio se reingieren por cadena bajo demanda, normalmente al añadir una cadena a la configuración o cuando las auditorías trimestrales de cobertura señalan anomalías. Los registros de lugares de servicio se reingieren contra cada nueva entrega trimestral de Overture; la ruta al almacén de objetos de Overture en el script de ingesta debe actualizarse para apuntar a cada nueva entrega.

## Véase también

- [[location-intelligence-substrate]] — la arquitectura SIG de archivos planos y su capa de almacenamiento
- [[service-business-clustering]] — el servicio de agrupación que consume estos registros
- [[service-places-filtering]] — el filtrado de anclas cívicas posterior a la ingesta
- [[regional-name-resolution-architecture]] — cómo las coordenadas se convierten en nombres regionales
- [[location-intelligence-platform]] — la superficie de aplicación que sirve estos registros

---

*Datos de OpenStreetMap © colaboradores de OpenStreetMap, bajo licencia ODbL. Datos de Overture Maps Foundation bajo CDLA Permissive 2.0.*
