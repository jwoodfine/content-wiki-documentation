---
schema: foundry-doc-v1
title: "service-extraction — Analizador determinista"
slug: service-extraction
short_description: "service-extraction es el controlador de tráfico central Ring 2 que elimina formato propietario de cargas útiles sin procesar, construye Entity Bundles estructurados, asigna IDs de transacción y enruta datos a servicios deterministas o a service-slm para extracción asistida por IA."
category: services
type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-08
editor: pointsav-engineering
paired_with: service-extraction.md
cites: []
---

Cada carga útil que cruza el límite de la plataforma llega a `service-extraction`, el controlador de tráfico del [[three-ring-architecture|Anillo 2]] que elimina el formato propietario (JSON, MIME, Base64), construye un Paquete de Entidades legible por máquina y asigna el identificador de transacción que sigue al paquete a través de cada paso descendente. Las cargas útiles estructuradas se enrutan completamente dentro del Anillo 2; el texto no estructurado se enruta a [[service-slm]] para extracción asistida por IA. `service-extraction` es el sucesor canónico del nombre de trabajo heredado `service-parser`.

## Línea de base arquitectónica

Cada mensaje que pasa a través del Anillo 1 llega a `service-extraction` como una carga útil sin procesar con formato del proveedor. El primer servicio del Anillo 1 en producir tales cargas útiles es típicamente [[service-email]] o [[service-input]]. El servicio tiene una responsabilidad: transformar esa carga útil en un Paquete de Entidades limpio y trazable, y enrutarlo al servicio descendente correcto. Asigna un ID de transacción a cada paquete, proporcionando una referencia de cadena de custodia que persiste a través de cada paso de procesamiento posterior.

## Anillo y función

`service-extraction` ocupa el **Anillo 2 — Conocimiento y Procesamiento** en la [[three-ring-architecture|arquitectura de tres anillos]]. El Anillo 2 es multiinquilino (a través del espacio de nombres `moduleId`) y determinista: procesa datos sin invocar inferencia de IA a menos que la forma de los datos lo requiera. Cuando una carga útil contiene texto no estructurado que no puede clasificarse por reglas deterministas, `service-extraction` enruta ese texto al Anillo 3 ([[service-slm]]) para extracción asistida por IA. Los identificadores de entidades producidos aquí son consumidos por la lógica de [[archetypes-and-chart-of-accounts|asignación de conectores del Plan de Cuentas]] en [[service-people]].

## El Paquete de Entidades

Cada carga útil se aísla en un directorio Unix nombrado por su marca de tiempo e ID de enrutamiento. El paquete se almacena eventualmente como registro inmutable en [[service-fs-architecture|`service-fs`]]. El paquete contiene `payload.txt` — el registro legible permanente — más adjuntos binarios almacenados de forma nativa junto al texto.

## Véase también

- [[service-email]]
- [[service-people]]
- [[service-slm]]
- [[service-search]]
