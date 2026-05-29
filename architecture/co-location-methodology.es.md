---
schema: foundry-doc-v1
type: concept
slug: co-location-methodology
short_description: "Un enfoque estructurado para clasificar candidatos de coubicación de hardware en dimensiones regulatorias, de red, de infraestructura y de costo, restringido primero por requisitos regulatorios antes de que ocurra cualquier otra optimización."
title: "Metodología de co-ubicación"
category: architecture
language: es
quality: complete
status: stable
bcsc_class: public-disclosure-safe
last_edited: 2026-05-13
editor: pointsav-engineering
paired_with: co-location-methodology.md
cites: []
---

La metodología de co-ubicación es el enfoque estructurado que utiliza [[pointsav-overview|PointSav]] para evaluar y clasificar oportunidades de co-ubicación física para despliegues de clientes. Combina datos de mercado, contexto regulatorio y características de infraestructura extraídos del canal de inteligencia de la plataforma y del [[compounding-substrate]] para producir una lista clasificada de sitios candidatos para un requisito de despliegue dado.

## Qué significa co-ubicación en este contexto

La co-ubicación, en el modelo de despliegue de PointSav, se refiere a colocar hardware propiedad del cliente en las instalaciones de un centro de datos de terceros. El cliente conserva la propiedad del hardware, la pila de software y los datos; las instalaciones proporcionan energía, refrigeración, seguridad física y tránsito de red.

La metodología aborda el paso de selección de sitio: dado un requisito de despliegue, ¿qué instalaciones en qué [[development-regions]] satisfacen mejor la combinación de restricciones de latencia, jurisdicción, postura de cumplimiento y costo?

## Dimensiones de evaluación

**Adecuación jurisdiccional.** Cada candidato de co-ubicación se evalúa frente al contexto regulatorio de la región operativa del cliente. Para clientes canadienses bajo obligaciones de divulgación de la NI 51-102 o OSC SN 51-721, la residencia de datos dentro de Canadá es un requisito base. La metodología codifica la puntuación con jurisdicción primero: una instalación fuera de la jurisdicción requerida se excluye antes de evaluar otras dimensiones.

**Características del tránsito de red.** La latencia hacia los usuarios primarios del cliente y hacia el punto de acceso del espacio de trabajo PointSav se mide en el momento de la selección de candidatos. Las instalaciones se puntúan por tiempo de ida y vuelta, diversidad de proveedores de tránsito, y disponibilidad de una ruta de emparejamiento BGP compatible con WireGuard.

**Compatibilidad de infraestructura.** El perfil de energía y refrigeración de la instalación se compara con la clase de nodo que se va a colocar. Los nodos [[totebox-os|ToteboxOS]] requieren perfiles de energía modestos y siempre activos; los niveles de inferencia con GPU requieren mayor energía de pico y refrigeración activa.

**Estructura de costos.** Las tarifas mensuales de co-ubicación, los cargos de interconexión y los compromisos de ancho de banda se normalizan a un costo total de propiedad durante un horizonte de 36 meses.

## Integración con regiones de desarrollo

La puntuación de co-ubicación opera dentro de la taxonomía de [[development-regions]]. Una región de desarrollo define el alcance geográfico y jurisdiccional dentro del cual se consideran los candidatos de co-ubicación. El operador revisa la lista clasificada producida por el canal de inteligencia y toma la decisión final de selección de sitio.

## Véase también

- [[development-regions]] — taxonomía de zonas geográficas y jurisdiccionales
- [[three-ring-architecture]] — modelo de sustrato de datos y cómputo de la plataforma
- [[compounding-substrate]] — mecanismo de sustrato que acumula inteligencia de mercado
- [[leapfrog-2030-architecture]] — arquitectura estratégica en la que se toman las decisiones de co-ubicación
