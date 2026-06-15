---
schema: foundry-doc-v1
title: "Despliegue en el borde e ingesta en el perímetro"
slug: edge-deployment.es
short_description: "La plataforma enruta todas las conexiones de red externas a través de servicios de ingesta perimetral de Ring 1 en el borde del sistema, desinfectando cargas útiles entrantes antes de que lleguen a los anillos de procesamiento central y registrando eventos limpios y validados en el registro de auditoría en lugar de tráfico de red sin procesar."
category: infrastructure
type: topic
content_type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-09
editor: pointsav-engineering
paired_with: edge-deployment.md
---

La plataforma traslada todas las conexiones de red externas al perímetro más externo del sistema antes de que cualquier dato llegue a los anillos de procesamiento central, siguiendo la [[three-ring-architecture|arquitectura de tres anillos]]. Esta arquitectura impide que los ataques de red habituales alcancen los registros financieros y los datos estructurados almacenados en el Anillo 2, que son protegidos por el [[worm-ledger-design|registro WORM]].

## Puntos clave

- Todo el tráfico de internet entrante se procesa exclusivamente en el Anillo 1 — la capa de perímetro. Ningún payload externo llega al Anillo 2 sin antes haber sido saneado, validado y despojado de metadatos de transporte por el servicio de ingesta del Anillo 1 correspondiente. El internet público nunca está en contacto directo con el Anillo 2 ni con el Anillo 3.
- El Anillo 1 se implementa como un conjunto de procesos servidores MCP por canal (uno por tipo de ingesta: correo electrónico, sistema de archivos, registros de personas, input externo). Cada uno acepta, sanea y entrega únicamente registros limpios y estructurados hacia el interior — un canal de ingesta comprometido no puede escalar al nivel del libro mayor.
- El registro de auditoría del Anillo 2 registra lo que el sistema procesó, no lo que llegó al perímetro de red. Esta separación es una condición previa del [[worm-ledger-architecture|diseño del registro WORM]]: eventos limpios y validados — no tráfico en bruto — son lo que se escribe en el registro inmutable.
- El Anillo 2 no tiene ruta de salida a internet salvo a través de [[service-egress]]. El perímetro se aplica en ambas direcciones: entrada a través de la ingesta del Anillo 1, salida a través del servicio de egreso.

## El problema de la ingesta profunda

Las configuraciones de servidor estándar procesan el tráfico de internet entrante dentro del mismo entorno de ejecución que contiene los datos centrales. Una vulnerabilidad en cualquier ruta de ingesta otorga acceso al mismo espacio de memoria que los registros principales. El aislamiento no puede añadirse retroactivamente una vez que un proceso comparte memoria con otro.

## Posicionamiento en el perímetro

La plataforma sitúa todos los procesos de ingesta en el borde físico y lógico del sistema. Ningún payload de internet entrante cruza hacia el Anillo 2 sin antes pasar por la capa de perímetro del Anillo 1. El Anillo 1 se implementa como un conjunto de procesos servidores MCP (Model Context Protocol), uno por canal de ingesta (correo electrónico, sistema de archivos, registros de personas, input externo).

Cada proceso del Anillo 1 acepta el payload, lo desinfecta —elimina metadatos de transporte, valida la estructura y descarta entradas malformadas— y luego entrega únicamente el registro limpio y estructurado al Anillo 2. El internet público nunca está en contacto directo con el Anillo 2 ni con el Anillo 3.

## Efecto sobre la integridad de la auditoría

Dado que los payloads en bruto se sanean en el perímetro y son los registros limpios los que procesa el Anillo 2, el registro de auditoría refleja sobre qué actuó el sistema, no lo que llegó a nivel de red. Esta separación es una condición previa del diseño del registro WORM.

## Véase también

- [[three-ring-architecture]] — la arquitectura de tres anillos que define los límites del Anillo 1 y el Anillo 2
- [[worm-ledger-architecture]] — el registro WORM que almacena los datos saneados
- [[service-email]] — ingesta del Anillo 1 para correo electrónico
- [[compounding-substrate]] — la arquitectura de tres anillos en contexto
- [[self-host-a-deployment]] — guía paso a paso: desplegar la plataforma en infraestructura propia con ingesta del Anillo 1 configurada
