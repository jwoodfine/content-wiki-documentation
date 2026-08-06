---
schema: foundry-doc-v1
title: "Sustrato de inteligencia de localización"
slug: location-intelligence-substrate
short_description: "Una arquitectura de SIG plano y abierto que permite a los clientes poseer conjuntos de datos geográficos de extremo a extremo usando datos abiertos con licencia Apache y una pila de renderización alineada con Rust de código abierto, con análisis de coubicación de venta minorista como la primera superficie implementada."
category: substrate
type: topic
content_type: topic
quality: complete
index_group: core-named-substrates
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-01
editor: pointsav-engineering
paired_with: location-intelligence-substrate.md
aliases:
  - pointsav-gis-engine
---


Una plataforma que depende de una base de datos en ejecución y una conexión de red activa es una plataforma que el cliente alquila, no posee — de ahí se derivan interrupciones, costos por usuario e inelegibilidad para entornos aislados de red. El Sustrato de Inteligencia de Localización evita esa dependencia por construcción: es una arquitectura SIG de archivos planos y código abierto que permite a los clientes [[customer-hostability|poseer sus conjuntos de datos geográficos de extremo a extremo]] — sin facturación de API de tiles, sin licencias de almacén de datos, sin bloqueo a ningún proveedor de nube. El sustrato se construye sobre fundamentos de datos abiertos con licencia Apache (Overture Maps Foundation, Foursquare Open Source Places) y se renderiza mediante una pila de código abierto alineada con Rust (MapLibre GL JS, servidor de tiles Martin, PMTiles).

La primera superficie desplegada es `gis.woodfinegroup.com` — un mapa de co-localización que muestra la co-presencia de anclas minoristas en Estados Unidos, Canadá, México y España.

## Arquitectura — archivo plano frente a base de datos

Para cargas de trabajo de decenas de miles de registros POI en un pequeño número de países, con escrituras por lotes poco frecuentes y consultas principalmente de lectura, el archivo plano es suficiente y es la arquitectura que tanto Foursquare como Overture Maps Foundation eligieron para sus lanzamientos de sustrato.

Recomendación: **GeoParquet como formato canónico en reposo** (un archivo por país y servicio, actualizado mensualmente), **JSONL paralelos para historial rastreable con git y legible por humanos**, **FlatGeobuf como derivado transmisible al navegador**. FlatGeobuf lleva un R-tree de Hilbert empaquetado en la cabecera del archivo que permite a un navegador transmitir solo las características dentro de la ventana gráfica actual mediante solicitudes de rango HTTP.

## Stack de renderización

El stack de renderización utiliza MapLibre GL JS en el navegador — un renderizador de mosaicos vectoriales de código abierto impulsado por la comunidad que soporta WebGL, estilización dinámica, animación suave y 3D sin coste de licencia por tráfico.

La generación de tiles utiliza Tippecanoe para convertir GeoJSON en MBTiles o PMTiles, reduciendo el tamaño del archivo en un 85-95% frente al GeoJSON sin procesar. El servicio de tiles utiliza Martin, el servidor de tiles Rust de la Fundación MapLibre. El formato de archivo de tiles es PMTiles — un archivo de único archivo con soporte de solicitudes de rango HTTP, que permite servir tiles directamente desde nginx sin ejecutar Martin cuando los tiles están pre-cocinados.

## Esquema de servicio — service-business, service-places, service-parking

Una sola forma de registro cubre los tres servicios de localización del Anillo 1, con campos discriminadores:

```jsonc
{
 "id": "01HZ...", // ULID
 "service": "business" | "places" | "parking",
 "operator": "walmart", // slug de marca
 "operator_brand_family": "walmart", // unifica equivalentes regionales
 "name": "Walmart Supercenter Burnaby",
 "country_code": "US" | "CA" | "MX" | "ES",
 "address": "...",
 "lat": 49.2827,
 "lng": -123.1207,
 "geometry": { "type": "Point", ... },
 "store_type": "supercenter" | "warehouse" | "diy" | "warehouse-club",
 "data_source": "official-store-locator" | "openstreetmap" | "overture" | "foursquare-os" | "manual",
 "captured_at": "2026-04-30T00:00:00Z"
}
```

La normalización por familia de marca permite que las consultas de co-localización traten equivalentes regionales como un único operador lógico a través de países. `service-places` lleva un campo `place_type` (hospital, educación superior, aeropuerto). `service-parking` lleva una `geometry` de tipo Polígono (el perímetro del estacionamiento) en lugar de un Punto, además de un campo `associated_business_id` que vincula el estacionamiento con su negocio ancla cuando se conoce.

## Renderizado de nivel

Los registros de clúster llevan una propiedad `tier` una vez que [[app-orchestration-gis]] aplica la [[retail-co-location-tier-methodology|metodología de niveles]] a los datos ingeridos. La función del sustrato a partir de ese punto es la presentación: emitir una `FeatureCollection` GeoJSON por clúster (puntos de ancla, un polígono de radio de captación y la propiedad `tier`), y dejar que las capas del navegador la rendericen — POIs como círculos coloreados por familia de marca (Capa 1), clústeres con nivel y sus halos de captación (Capa 2), y límites de país con fichas de filtro (Capa 3). Los popovers al pasar el cursor muestran marca, formato, año de apertura y nivel sin navegación de página.

A 15,000 registros POI (cobertura combinada en cuatro países y tres familias de marca), la renderización del lado del cliente en MapLibre está cómodamente dentro del rango operativo. La agrupación de clústeres del lado del cliente con Supercluster se vuelve relevante en torno a los 50,000 registros; la generación de mosaicos vectoriales en el servidor, a partir de los 500,000.

## Base de investigación de la co-localización minorista

La agrupación por co-localización minorista es un fenómeno documentado con precedente académico: las principales categorías de anclas minoristas exhiben tendencias marcadas hacia la proximidad mutua. Los efectos de entrada de Costco sobre los minoristas vecinos se han estudiado formalmente. El análisis de co-localización que produce el sustrato se corresponde directamente con la metodología establecida (distancia media al vecino más cercano, contrastada frente a una distribución nula de permutación).

## Composición con el resto de la plataforma

Los triples de co-localización producidos por el sustrato de inteligencia de localización se componen con el resto del sustrato de la plataforma: un polígono de área de captación minorista de la capa GIS y una envolvente de edificio de la capa BIM pueden compartir el mismo marco de coordenadas, los mismos archivos YAML laterales por elemento y el mismo anclaje de [[worm-ledger-architecture|libro mayor WORM]]. Dos clústeres; un sustrato.

[[service-slm]] está disponible para trabajo de anotación rutinaria (sugerir categorías para POIs recién ingeridos, resumir deltas de conjuntos de datos, etiquetar anomalías) pero la plataforma es completamente funcional con el [[compounding-doorman|Portero]] apagado — el principio de [[substrate-without-inference-base-case|Inteligencia Opcional]] aplicado a los datos geográficos.

## Fuentes de datos

Los conjuntos de datos abiertos con licencia Apache 2.0 son el sustrato primario: Foursquare Open Source Places (más de 100 millones de POIs, caídas mensuales de Parquet) y Overture Maps Foundation (lugares, edificios, transportes y direcciones como GeoParquet). OpenStreetMap (vía el geocodificador Nominatim o Photon) es la fuente secundaria para las brechas de cobertura.

El scraping directo de sitios web de minoristas no se utiliza cuando los términos de servicio prohíben la minería de datos. Los fundamentos de datos abiertos ya han acumulado los registros POI que de otro modo requerirían scraping.

## Información prospectiva

Las declaraciones sobre el calendario de despliegue, los resultados para el cliente y la hoja de ruta de funcionalidades del Sustrato de Inteligencia de Localización son objetivos previstos sujetos a cambio. Los plazos reales dependen de la revisión del operador en cada etapa, de la precisión de la cobertura de datos abiertos y de la velocidad de desarrollo. Estas declaraciones llevan el matiz "planificado"/"previsto"/"puede" conforme a la postura de divulgación continua del espacio de trabajo, según el National Instrument 51-102 (Continuous Disclosure Obligations) de la BCSC y el OSC Staff Notice 51-721 (Forward-Looking Information Disclosure).

## Véase también

- [[three-ring-architecture]]
- [[substrate-without-inference-base-case]]
- [[customer-owned-graph-ip]]
- [[retail-co-location-tier-methodology]] — las condiciones de nivel aplicadas a la propiedad `tier` renderizada aquí
- [[app-orchestration-gis]] — el motor que calcula la asignación de nivel a partir de los datos de clúster ingeridos
