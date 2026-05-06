---
title: "Sustrato de Inteligencia de Localización"
slug: location-intelligence-substrate.es
category: architecture
status: stable
bcsc_class: public-disclosure-safe
last_edited: 2026-04-30
editor: pointsav-engineering
quality: complete
---

El Sustrato de Inteligencia de Localización de Foundry es una arquitectura SIG de archivos planos y código abierto que permite a los clientes poseer sus conjuntos de datos geográficos de extremo a extremo — sin facturación de API de tiles, sin licencias de almacén de datos, sin bloqueo a ningún proveedor de nube. El sustrato se construye sobre fundamentos de datos abiertos con licencia Apache (Overture Maps Foundation, Foursquare Open Source Places) y se renderiza mediante una pila de código abierto alineada con Rust (MapLibre GL JS, servidor de tiles Martin, PMTiles).

La primera superficie desplegada es `gis.woodfinegroup.com` — un mapa de co-localización que muestra la co-presencia de anclas minoristas en Estados Unidos, Canadá, México y España.

## Arquitectura — archivo plano frente a base de datos

Para cargas de trabajo de decenas de miles de registros POI en un pequeño número de países, con escrituras por lotes poco frecuentes y consultas principalmente de lectura, el archivo plano es suficiente y es la arquitectura que tanto Foursquare como Overture Maps Foundation eligieron para sus lanzamientos de sustrato.

Recomendación: **GeoParquet como formato canónico en reposo** (un archivo por país y servicio, actualizado mensualmente), **JSONL paralelos para historial rastreable con git y legible por humanos**, **FlatGeobuf como derivado transmisible al navegador**. FlatGeobuf lleva un R-tree de Hilbert empaquetado en la cabecera del archivo que permite a un navegador transmitir solo las características dentro de la ventana gráfica actual mediante solicitudes de rango HTTP.

## Stack de renderización

El stack de renderización utiliza MapLibre GL JS en el navegador — un renderizador de mosaicos vectoriales de código abierto impulsado por la comunidad que soporta WebGL, estilización dinámica, animación suave y 3D sin coste de licencia por tráfico.

La generación de tiles utiliza Tippecanoe para convertir GeoJSON en MBTiles o PMTiles, reduciendo el tamaño del archivo en un 85-95% frente al GeoJSON sin procesar. El servicio de tiles utiliza Martin, el servidor de tiles Rust de la Fundación MapLibre. El formato de archivo de tiles es PMTiles — un archivo de único archivo con soporte de solicitudes de rango HTTP, que permite servir tiles directamente desde nginx sin ejecutar Martin cuando los tiles están pre-cocinados.

## Análisis de co-localización

La consulta de co-localización identifica ubicaciones de la familia de marcas A dentro de 1 km, 2 km y 3 km de ubicaciones de la familia de marcas B (y opcionalmente una tercera familia). El algoritmo utiliza distancia haversiana frente a un índice R-tree en memoria; a decenas de miles de registros, cada búsqueda se ejecuta en microsegundos.

El sustrato emite una FeatureCollection GeoJSON: centroide de la tupla, polilínea triangular que conecta las ubicaciones, círculos de radio y una propiedad `cluster_grade`. Las capas de visualización del navegador muestran POIs como círculos coloreados por familia de marca, tuplas de co-localización con sus halos de radio y fichas de filtro por país.

## Composición con el resto de Foundry

Los triples de co-localización producidos por el sustrato de inteligencia de localización se componen con el resto del sustrato de Foundry: un polígono de área de captación minorista de la capa GIS y una envolvente de edificio de la capa BIM pueden compartir el mismo marco de coordenadas, los mismos archivos YAML laterales por elemento y el mismo anclaje de libro mayor WORM. Dos clústeres; un sustrato.

`service-slm` está disponible para trabajo de anotación rutinaria (sugerir categorías para POIs recién ingeridos, resumir deltas de conjuntos de datos, etiquetar anomalías) pero la plataforma es completamente funcional con el Portero apagado — el principio de Inteligencia Opcional aplicado a los datos geográficos.

## Fuentes de datos

Los conjuntos de datos abiertos con licencia Apache 2.0 son el sustrato primario: Foursquare Open Source Places (más de 100 millones de POIs, caídas mensuales de Parquet) y Overture Maps Foundation (lugares, edificios, transportes y direcciones como GeoParquet). OpenStreetMap es la fuente secundaria para las brechas de cobertura.

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ y Foundry™ son marcas no registradas de Woodfine Capital Projects Inc.


---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™ y Totebox Archive™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos titulares.*
