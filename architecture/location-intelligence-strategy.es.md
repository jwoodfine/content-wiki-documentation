---
schema: foundry-doc-v1
title: "Plataforma de Inteligencia de Localización — Estrategia y Arquitectura"
slug: location-intelligence-strategy.es
category: architecture
type: topic
quality: core
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
paired_with: location-intelligence-strategy.md
---

## Adaptación estratégica — Inteligencia de Localización

El sustrato de Inteligencia de Localización proporciona a los clientes un conjunto de datos de lugares — negocios, puntos de interés, geometrías de aparcamiento — almacenados como archivos planos que el cliente posee, versionados en el mismo libro mayor que cualquier otro registro de Totebox, y presentados a través de una pila de cartografía de código abierto sin costes recurrentes por solicitud o por asiento.

La primera aplicación es un mapa de co-localización: cada localización de la familia Walmart, la familia Home Depot y Costco en Estados Unidos, Canadá, México y España, con los grupos de tiendas que caen dentro de rangos de proximidad definidos como la analítica visible.

## El mercado de Inteligencia de Localización

El segmento de Inteligencia de Localización en 2026 se organiza en cuatro familias arquitectónicas, cada una con un mecanismo de ingresos estructural que condiciona lo que puede ofrecer.

Las **plataformas de consulta en almacén de datos** ejecutan consultas espaciales directamente dentro del almacén del cliente y no almacenan sus datos, pero requieren que el cliente mantenga un almacén de datos como infraestructura base.

El **GIS empresarial heredado** vende licencias progresivas por tipo de usuario y utiliza créditos como moneda interna, lo que lo hace inadecuado para clientes de pequeñas y medianas empresas que operan un conjunto de datos pequeño y propio sin presupuesto por asiento.

Las **plataformas de cartografía para desarrolladores** vinculan el coste al tráfico; un sitio público con tráfico sustancial genera una factura proporcionalmente elevada.

El **análisis de visitas y movimiento** opera un panel de dispositivos móviles y extrapola visitas a tiendas mediante métodos estadísticos. La arquitectura es necesariamente centralizada y agrupada para preservar la privacidad.

Cada familia vincula sus ingresos a algo por lo que pasan los datos del cliente. Ninguna puede ofrecer el inverso: un sustrato que el cliente posee de extremo a extremo, opera sin conexión y replica sin pagar costes recurrentes. La plataforma ocupa esa posición.

## Por qué datos planos, no una base de datos

Para la carga de trabajo actual — decenas de miles de registros de puntos de interés en cuatro países, tres familias de marcas, escrituras por lotes infrecuentes, consulta principalmente de lectura — los archivos planos son suficientes. Foursquare y la Overture Maps Foundation eligieron el mismo formato para sus publicaciones de datos abiertos.

La recomendación es **GeoParquet como formato canónico en reposo** (un archivo por país por servicio, renovado mensualmente), **hermanos JSONL para el historial legible por git**, y **FlatGeobuf como derivado para la transmisión en el navegador**.

## El análogo de Home Depot en España

Identificar el análogo estructural de Home Depot en España requiere distinguir entre el formato de bricolaje para el consumidor y el formato de almacén para el comercio profesional.

**Bricomart (rebautizado Obramat en 2024)** — propiedad del grupo Adeo, formato almacén orientado hacia el cliente profesional y el autoconstructor, aproximadamente 22 localizaciones en España. La correspondencia de formato — escala de almacén, orientado al comercio profesional, posicionamiento de gran volumen — es el análogo estructural más cercano a Home Depot.

**Leroy Merlin** — también del grupo Adeo, la marca de bricolaje para el consumidor dominante en España con más de 120 localizaciones. Es la más conocida por visibilidad, pero el formato es de bricolaje para el consumidor en lugar de almacén comercial; la comparación con Lowe's encaja mejor que con Home Depot.

La asignación de la familia de marcas: `walmart_family` incluye walmart e ikea-spain (gran formato, mercancía general para el consumidor); `homedepot_family` incluye homedepot y bricomart-spain (almacén de bricolaje y comercio profesional); `costco_family` incluye costco (club almacén con presencia directa en España desde 2014).

## Pila técnica recomendada

Para la entrega de teselas y capas del mapa, la pila de código abierto recomendada es: **MapLibre GL JS** como renderizador en el navegador (tenedor de la comunidad sin costes de licencia por tráfico), **deck.gl** para capas de visualización de datos, **Tippecanoe** para la generación de teselas desde GeoJSON, **Martin** (el servidor de teselas Rust de la Fundación MapLibre) para la entrega dinámica, y **PMTiles** como formato de archivo de teselas para servir directamente desde nginx cuando las teselas están pre-generadas.

Regla de implementación: generar teselas estáticas para los puntos de interés de las familias de marcas y los círculos de radio de co-localización mediante Tippecanoe y PMTiles; servirlas directamente desde nginx. Migrar a Martin solo cuando sea necesaria la generación dinámica de teselas.

## Camino de implementación planificado

Todos los hitos a continuación son objetivos planificados, sujetos a criterios de aceptación y revisión del operador en cada etapa. [ni-51-102] [osc-sn-51-721]

La secuencia prevista es: Semana 1 (aprovisionamiento del marco de despliegue y host virtual nginx); Semana 2 (andamiaje de la aplicación con datos ficticios estáticos para verificar la cadena de renderizado); Semana 3 (ingesta de datos de EE.UU. desde Foursquare Open Source Places u Overture Maps Foundation, aproximadamente 7.600 registros); Semana 4 (superficie de co-localización lista para demostración); Semanas 5–6 (extensión de cobertura a Canadá y México); Semana 7 (España); Semanas 8+ (service-places, service-parking, andamiaje del Workplace OS, y derivaciones editoriales).

La especificación técnica completa, incluyendo el esquema de registros, el algoritmo de co-localización, las cifras de recuento de tiendas y la investigación de fuentes de datos, está disponible en inglés en el artículo principal.

## Véase también

- [[three-ring-architecture]] — la composición de los anillos que service-business, service-places y service-parking implementan
- [[compounding-substrate]] — las propiedades de soberanía e inteligencia opcional que este sustrato implementa
- [[worm-ledger-architecture]] — el libro mayor de solo adición que ancla los registros de co-localización en el Totebox Archive del cliente
- [[service-slm]] — el servicio opcional del Anillo 3 disponible para anotación y detección de anomalías

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
