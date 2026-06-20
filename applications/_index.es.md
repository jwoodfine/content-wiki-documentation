---
schema: foundry-doc-v1
title: "Aplicaciones"
slug: _index.es
short_description: "Aplicaciones internas y orientadas al usuario construidas sobre el sustrato de plataforma PointSav — el motor wiki, la superficie de marketing, el motor de análisis GIS, el workbench de desarrollo en navegador, la puerta de entrada de datos estructurados y los artículos de intención de diseño que enmarcan cómo se componen esas superficies."
lang: es
category: applications
type: topic
content_type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-29
editor: pointsav-engineering
paired_with: _index.md
---

Las aplicaciones se sitúan por encima de la capa de servicios de tres anillos. Consumen datos deterministas y salida opcional de IA de los anillos y los presentan a través de una interfaz definida. Una aplicación no contiene datos canónicos — es una vista sobre la capa de servicios y puede ser reprovisada sin pérdida de datos apuntando una instancia nueva a los datos inmutables subyacentes. Los artículos de esta categoría cubren tanto las aplicaciones nombradas como el material de intención de diseño que explica cómo se compone cada superficie.

Cada aplicación aquí corresponde a un directorio `app-*` en el monorepo y hereda la separación de [[three-ring-architecture|arquitectura de tres anillos]]; ninguna contiene el registro autoritativo. Los artículos de cromo orientados al lector y de fundamentos de diseño se agrupan junto a los artículos de aplicación para que los operadores que evalúan una superficie puedan pasar del artículo de ingeniería a la intención de diseño sin salir de la categoría.

## Conocimiento y editorial

El motor wiki, la superficie de marketing y los artículos de intención de diseño que describen su cromo orientado al lector.

- [[app-mediakit-knowledge]] — El motor de wiki Rust de binario único que renderiza la documentación de ingeniería de PointSav; una vista sobre un árbol de Markdown donde los commits de git son canónicos y cada binario en ejecución es estado derivado desechable.
- [[app-mediakit-marketing]] — Páginas de aterrizaje de marketing multiinquilino desde un único binario Rust compilado estáticamente; memoria muscular de WordPress.org en la URL orientada al operador, infraestructura soberana debajo.
- [[knowledge-wiki-home-page-design|Diseño de la página de inicio del wiki]] — Cómo la página de inicio de documentación hereda las convenciones estructurales de Wikipedia y las extiende para lectores de ingeniería y de la comunidad financiera.
- [[wikipedia-leapfrog-design|Diseño de salto sobre Wikipedia]] — Qué hereda el motor wiki de Wikipedia, qué añade más allá y qué significa el margen de salto del cinco por ciento para lectores e ingenieros.
- [[documentation-pointsav-com-launch-2026-04-27|Lanzamiento de documentation.pointsav.com]] — El lanzamiento TLS de abril de 2026 de `documentation.pointsav.com`: pila de servicio, postura de marcador de posición y comandos de verificación.

## Inteligencia de ubicación

El motor de análisis GIS, el artículo de plataforma que lo enmarca junto a la capa de renderizado y la intención de diseño de experiencia de usuario.

- [[app-orchestration-gis]] — El motor de análisis espacial sin estado para cálculos de geometría lineal y clasificación de co-localización; una función pura sin datos canónicos que puede reprovisarse apuntando una instancia nueva a la capa de datos.
- [[location-intelligence-platform|Plataforma de inteligencia de ubicación]] — La plataforma completa de inteligencia de ubicación: app-orchestration-gis (análisis) emparejado con el motor de renderizado; cada conjunto de datos, algoritmo y decisión de renderizado bajo el control del cliente.
- [[location-intelligence-ux|Experiencia de inteligencia de ubicación]] — La filosofía de diseño Conclusión Primero: conclusiones de nivel ordenadas en lugar de puntos de datos individuales, para que los usuarios vean los nodos comerciales más defendibles a zoom nacional antes de profundizar en operadores individuales.

## Superficies de entrada y desarrollo

La puerta de entrada estructurada que admite archivos externos a un Totebox, y el workbench en navegador para trabajar con archivos sin una sesión de terminal.

- [[app-console-input]] — La superficie F12 en os-console: la puerta de entrada estructurada a través de la cual los archivos externos brutos entran en un Totebox antes de ser sellados en el libro verificado.
- [[app-privategit-workbench|Workbench de PrivateGit]] — Un editor de archivos de tres columnas basado en navegador incluido en os-privategit; para trabajar con archivos sin una sesión de terminal.

## Aplicaciones de dominio

Superficies dedicadas a un dominio operativo específico — Modelado de Información de Edificios y flujos de trabajo de propiedad inmobiliaria.

- [[bim-and-real-property-surfaces|Superficies BIM y propiedad inmobiliaria]] — Cómo PointSav trata el Modelado de Información de Edificios como un dominio operativo de primera clase, con herramientas de sistema de diseño dedicadas y disciplina de mantenimiento de registros ISO 19650.
- Sistema de diseño para BIM — Herramientas del sistema de diseño adaptadas para flujos de trabajo de BIM y propiedad inmobiliaria.
- Salto BIM en archivos planos — Cómo se gestiona el Modelado de Información de Edificios como registros ISO 19650 en archivos planos en lugar de instancias alojadas en base de datos.
- Convenciones de interfaz AEC — Convenciones de interfaz para superficies AEC que las aplicaciones BIM heredan y extienden.
- Brecha BIM del gestor inmobiliario — La brecha entre las herramientas de autoría BIM y los flujos de trabajo del gestor inmobiliario, y cómo las superficies de aplicación la cierran.

## Véase también

- [Servicios](/services/) — la capa de servicios sobre la que construyen las aplicaciones
- [Sistemas](/systems/) — los sistemas operativos que alojan las aplicaciones
- [Arquitectura](/architecture/) — el modelo de tres anillos y los principios de propiedad del cliente
- [Sistema de diseño](/design-system/) — el vocabulario de tokens y componentes que hereda el cromo de las aplicaciones
