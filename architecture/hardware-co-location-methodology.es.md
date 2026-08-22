---
schema: foundry-doc-v1
type: concept
content_type: topic
slug: hardware-co-location-methodology
short_description: "Un enfoque estructurado para clasificar candidatos de coubicación de hardware en dimensiones regulatorias, de red, de infraestructura y de costo, restringido primero por requisitos regulatorios antes de que ocurra cualquier otra optimización."
title: "Metodología de co-ubicación de hardware"
category: architecture
index_group: location-intelligence-and-domain
language: es
quality: stub
status: planned
bcsc_class: public-disclosure-safe
last_edited: 2026-08-03
editor: pointsav-engineering
paired_with: hardware-co-location-methodology.md
cites: []
---

La metodología de co-ubicación es un enfoque estructurado planificado para evaluar y clasificar oportunidades de co-ubicación física para despliegues de hardware de clientes — jurisdicción, tránsito de red, ajuste de infraestructura y costo, en ese orden de prioridad. Todavía no existe un canal automatizado de puntuación; la metodología describe el diseño previsto, no un sistema operativo. (Es un concepto distinto de la puntuación de co-ubicación inmobiliaria de la plataforma, usada para la selección de sitios de propiedad comercial — un dominio diferente con su propia metodología, implementada por separado.)

## Qué significa co-ubicación en este contexto

La co-ubicación, en el modelo de despliegue de PointSav, se refiere a colocar hardware propiedad del cliente en las instalaciones de un centro de datos de terceros. El cliente conserva la propiedad del hardware, la pila de software y los datos; las instalaciones proporcionan energía, refrigeración, seguridad física y tránsito de red.

La metodología aborda el paso de selección de sitio: dado un requisito de despliegue, ¿qué instalaciones en qué regiones de desarrollo satisfacen mejor la combinación de restricciones de latencia, jurisdicción, postura de cumplimiento y costo?

## Dimensiones de evaluación

**Adecuación jurisdiccional.** Cada candidato de co-ubicación se evalúa frente al contexto regulatorio de la región operativa del cliente. Para clientes canadienses bajo obligaciones de divulgación de la NI 51-102 o OSC SN 51-721, la residencia de datos dentro de Canadá es un requisito base. La metodología codifica la puntuación con jurisdicción primero: una instalación fuera de la jurisdicción requerida se excluye antes de evaluar otras dimensiones.

**Características del tránsito de red.** La latencia hacia los usuarios primarios del cliente y hacia el punto de acceso del espacio de trabajo PointSav se mide en el momento de la selección de candidatos. Las instalaciones se puntúan por tiempo de ida y vuelta, diversidad de proveedores de tránsito, y disponibilidad de una ruta de emparejamiento BGP compatible con WireGuard.

**Compatibilidad de infraestructura.** El perfil de energía y refrigeración de la instalación se compara con la clase de nodo que se va a colocar. Los nodos [[totebox-os|ToteboxOS]] requieren perfiles de energía modestos y siempre activos; los niveles de inferencia con GPU requieren mayor energía de pico y refrigeración activa.

**Estructura de costos.** Las tarifas mensuales de co-ubicación, los cargos de interconexión y los compromisos de ancho de banda se normalizan a un costo total de propiedad durante un horizonte de 36 meses.

## Integración con regiones de desarrollo

La puntuación de co-ubicación opera dentro de la taxonomía de regiones de desarrollo. Una región de desarrollo define el alcance geográfico y jurisdiccional dentro del cual se consideran los candidatos de co-ubicación.

## Estado

Hoy no existe un canal automatizado de puntuación ni un almacén de datos estructurado de perfiles de instalaciones. Las dimensiones anteriores describen el diseño previsto; actualmente un operador arma y evalúa la lista de candidatos manualmente, sin un canal automatizado.

## Véase también

- Regiones de desarrollo — taxonomía de zonas geográficas y jurisdiccionales
- [[three-ring-architecture]] — modelo de sustrato de datos y cómputo de la plataforma
- [[compounding-substrate]] — mecanismo de sustrato que acumula inteligencia de mercado
- [[leapfrog-2030-architecture]] — arquitectura estratégica en la que se toman las decisiones de co-ubicación
