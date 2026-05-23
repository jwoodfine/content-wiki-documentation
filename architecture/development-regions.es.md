---
schema: foundry-doc-v1
type: concept
slug: development-regions
short_description: "Las regiones de desarrollo son zonas geográficas y jurisdiccionales que segmentan los datos de mercado, contexto regulatorio y topología de implementación de la plataforma. Cada región define un envolvente jurisdiccional, límite geográfico y alcance de datos de mercado que rige la evaluación de coubicación y la aplicación de reglas de cumplimiento."
title: "Regiones de desarrollo"
category: architecture
language: es
quality: complete
status: stable
bcsc_class: public-disclosure-safe
last_edited: 2026-05-13
editor: pointsav-engineering
paired_with: development-regions.md
cites: []
---

Las regiones de desarrollo son las zonas geográficas y jurisdiccionales utilizadas por la plataforma PointSav para segmentar datos de mercado, contexto regulatorio y topología de despliegue. Cada región define un alcance delimitado dentro del cual se evalúan los candidatos de co-ubicación, se aplican posturas de cumplimiento y se acumula inteligencia de mercado. Las regiones no son territorios de entrega; son límites analíticos y operativos que determinan cómo la plataforma razona sobre las decisiones de despliegue.

## Propósito

Una plataforma que sirve a clientes en múltiples jurisdicciones no puede aplicar una única postura regulatoria de forma universal. Un cliente canadiense de gestión de propiedades que opera bajo obligaciones de divulgación continua de la NI 51-102 enfrenta requisitos de residencia de datos diferentes a los de un cliente que opera bajo regímenes equivalentes en EE. UU. o Europa.

Las regiones de desarrollo codifican esta especificidad jurisdiccional a nivel arquitectónico. Cuando un operador especifica un requisito de despliegue, declara la región objetivo. El canal de inteligencia de la plataforma, el motor de puntuación de la [[co-location-methodology]] y el validador de postura de cumplimiento delimitan sus resultados al alcance de esa región.

## Composición de una región

Cada región de desarrollo se define mediante tres componentes:

**Alcance jurisdiccional.** El conjunto de marcos legales y regulatorios aplicables dentro de la región. Para las regiones canadienses, esto incluye el regulador de valores provincial aplicable, el marco de divulgación continua NI 51-102, y las disposiciones relevantes de la PIPEDA o CASL para el manejo de datos.

**Límite geográfico.** La geografía física dentro de la cual se consideran las instalaciones de co-ubicación. Los límites geográficos no siempre se alinean con los jurisdiccionales: un alcance regulatorio canadiense puede abarcar instalaciones en múltiples provincias, cada una con características de tránsito distintas.

**Alcance de datos de mercado.** Las fuentes de datos e índices de mercado que alimentan el canal de inteligencia para la región. Los datos del mercado inmobiliario, los indicadores económicos y las señales demográficas están delimitados por región porque su contenido informativo está jurisdiccionalmente acotado.

## Relación con la metodología de co-ubicación

La [[co-location-methodology]] es la aplicación operativa de las definiciones de regiones de desarrollo. Cuando un operador inicia un proceso de selección de sitio, especifica una región de desarrollo; la metodología de co-ubicación busca dentro del límite geográfico de esa región y devuelve una lista clasificada de candidatos delimitada a esa región.

## Véase también

- [[co-location-methodology]] — el motor de puntuación que opera dentro de una región de desarrollo declarada
- [[leapfrog-2030-architecture]] — arquitectura estratégica que da forma a las decisiones de despliegue regional
- [[three-ring-architecture]] — modelo de sustrato de la plataforma dentro del cual se aprovisionan los despliegues regionales
