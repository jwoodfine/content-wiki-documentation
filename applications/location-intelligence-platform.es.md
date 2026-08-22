---
schema: foundry-doc-v1
title: "Plataforma de inteligencia de ubicación"
slug: location-intelligence-platform
category: applications
type: topic
content_type: topic
quality: complete
index_group: location-intelligence-applications
short_description: "Aplicación GIS de archivos planos propiedad del cliente para análisis de clústeres minoristas y selección de sitios, que une una canalización de puntuación nocturna con una capa de renderizado interactiva."
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: TRANSLATE-ES
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: location-intelligence-platform.md
cites:
 - osm-odbl
 - overture-maps-cdla-2-0
---

La plataforma de Inteligencia de Ubicación de PointSav es una aplicación GIS de archivos planos propiedad del cliente para análisis de clústeres minoristas y selección estratégica de sitios — una [[app-orchestration-gis|canalización]] nocturna que puntúa y clasifica nodos comerciales, junto con [[location-intelligence-substrate|una capa de renderizado]] que sirve el resultado como un mapa interactivo, con cada conjunto de datos, algoritmo y decisión de renderizado bajo el control directo del cliente. La plataforma responde a una pregunta comercial fundamental — *¿qué nodos geográficos poseen la densidad validada por capital requerida para soportar desarrollo adyacente?* — transformando ubicaciones de tiendas en bruto en nodos comerciales accionables a través de la [[retail-co-location-tier-methodology]]. Todos los conjuntos de datos canónicos residen en un [[totebox-archive|Archivo Totebox]] como archivos planos JSONL y GeoParquet.

## Capacidades operativas

La plataforma transforma los datos brutos de ubicación de tiendas en nodos comerciales accionables mediante la ejecución de la [[retail-co-location-tier-methodology|Metodología de Niveles de Co-ubicación]]. Responde a una pregunta comercial fundamental: *¿qué nodos geográficos poseen la densidad validada por capital necesaria para sustentar un desarrollo inmobiliario adyacente?*

### Identificación de clústeres

La canalización agrupa operadores intensivos en capital cercanos entre sí (Walmart, Costco,
Home Depot y anclas similares) e infraestructura cívica de apoyo (hospitales, universidades)
en clústeres mediante un algoritmo de agrupamiento espacial, luego puntúa cada clúster y le
asigna uno de cuatro niveles según la metodología de niveles.

### Interfaz de mapa interactivo

El mapa interactivo en [gis.woodfinegroup.com](https://gis.woodfinegroup.com) renderiza
conclusiones de nivel en lugar de puntos de datos individuales, según la
[[location-intelligence-ux|filosofía de diseño Conclusión Primero]] de la plataforma. Las
capas analíticas — Clústeres, Captación y Estudio OD — se presentan como controles de
navegación principales dentro de un componente de cajón, con el esquema de color de cuatro
niveles Regional/Distrito/Local/Periferia mostrando los nodos más sólidos a escala nacional
antes de que el usuario profundice en sitios individuales. Los radios de captación de área de
influencia son de aproximadamente 150 km para análisis regional estándar, reduciéndose a
unos 27 km en corredores urbanos densos.

## Soberanía de datos

El modelo de datos de la plataforma es deliberadamente de archivos planos en lugar de un
demonio de base de datos en ejecución:
- **Operación basada en archivos planos:** Los datos persisten como archivos JSONL y GeoParquet versionados en un [[totebox-archive|Archivo Totebox]].
- **Renderizado con estándares abiertos:** Utiliza PMTiles y MapLibre GL JS para servir mapas vectoriales directamente desde servidores web estándar, eliminando dependencias de APIs de mosaicos propietarias.
- **Reconstrucción reproducible:** La superficie de la aplicación puede reaprovisionarse apuntando una instancia nueva a la capa de datos inmutable y reejecutando la canalización nocturna.

## Fundamentos de datos y licenciamiento

La plataforma integra fuentes de datos abiertas para transparencia y auditabilidad:
- **Datos minoristas:** Provenientes de colaboradores de OpenStreetMap y Overture Maps Foundation.
- **Infraestructura cívica:** Registros de salud e institucionales del conjunto de datos Places de Overture Maps Foundation.
- **Mapa base:** Mosaicos vectoriales servidos por la propia infraestructura de la plataforma, no una API de mosaicos de terceros.

La cobertura ya abarca mercados de Norteamérica y Europa — los datos de movilidad
origen-destino para análisis de flujo de área de influencia están disponibles hoy, no son
una adición futura (la capa "Estudio OD" descrita arriba). *Los supuestos materiales para el
rendimiento actual de la plataforma incluyen la disponibilidad continua de conjuntos de datos
geográficos abiertos de alta fidelidad. [osm-odbl] [overture-maps-cdla-2-0]*

## Véase también

- [[app-orchestration-gis]] — la canalización que produce las clasificaciones de co-ubicación
- [[location-intelligence-substrate]] — la capa de renderizado que sirve los mosaicos vectoriales a la interfaz del mapa
- [[retail-co-location-tier-methodology]] — la metodología de niveles que sustenta el análisis de clústeres
- [[location-intelligence-ux]] — la filosofía de diseño UX para la superficie del mapa interactivo
- [[totebox-archive]] — el archivo de archivos planos que contiene todos los datos geoespaciales canónicos
