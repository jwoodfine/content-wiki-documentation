---
schema: foundry-doc-v1
title: "Aplicaciones"
slug: _index.es
short_description: "Aplicaciones internas y orientadas al usuario construidas sobre el sustrato de plataforma PointSav — el motor wiki, la superficie de mercado, el motor de análisis GIS y la puerta de entrada de datos estructurados a través de la cual los archivos externos ingresan en un Totebox."
lang: es
category: applications
type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: _index.md
---

Las aplicaciones se sitúan por encima de la capa de servicios de tres anillos. Consumen datos deterministas y salida opcional de IA de los anillos y los presentan a través de una interfaz definida. Una aplicación no contiene datos canónicos — es una vista sobre la capa de servicios y puede ser reprovisada sin pérdida de datos apuntando una instancia nueva a los datos inmutables subyacentes.

## Conocimiento y editorial

- [[app-mediakit-knowledge]] — El motor de wiki Rust de binario único que renderiza la documentación de ingeniería de PointSav; una vista sobre un árbol de Markdown donde los commits de git son canónicos y cada binario en ejecución es estado derivado desechable.
- [[app-mediakit-marketing]] — Páginas de aterrizaje de marketing multiinquilino desde un único binario Rust compilado estáticamente; memoria muscular de WordPress.org en la URL orientada al operador, infraestructura soberana debajo.

## GIS e inteligencia de ubicación

- [[app-orchestration-gis]] — El motor de análisis espacial sin estado para cálculos de geometría lineal y clasificación de co-localización; una función pura sin datos canónicos que puede reprovisarse apuntando una instancia nueva a la capa de datos.
- [[location-intelligence-platform]] — La plataforma completa de inteligencia de ubicación: app-orchestration-gis (análisis) y pointsav-gis-engine (renderizado), con cada conjunto de datos, algoritmo y decisión de renderizado bajo el control del cliente.

## Entrada e ingesta

- [[app-console-input]] — La superficie F12 en os-console: la puerta de entrada estructurada a través de la cual los archivos externos brutos entran en un Totebox antes de ser sellados en el libro verificado.

## Aplicaciones de dominio

- [[bim-and-real-property-surfaces]] — Cómo PointSav trata el Modelado de Información de Edificios como un dominio operativo de primera clase, con herramientas de sistema de diseño dedicadas y disciplina de mantenimiento de registros ISO 19650.

## Véase también

- [Servicios](/services/) — la capa de servicios sobre la que construyen las aplicaciones
- [Sistemas](/systems/) — los sistemas operativos que alojan las aplicaciones
- [Arquitectura](/architecture/) — el modelo de tres anillos y los principios de propiedad del cliente
