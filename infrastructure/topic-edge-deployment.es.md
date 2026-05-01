---
schema: foundry-topic-v1
title: "Despliegue en el Borde e Ingesta en el Perímetro"
slug: topic-edge-deployment
category: infrastructure
status: published
last_edited: 2026-04-30
editor: pointsav-engineering
---

La plataforma traslada todas las conexiones de red externas al perímetro más externo del sistema antes de que cualquier dato llegue a los anillos de procesamiento central. Esta arquitectura impide que los ataques de red habituales alcancen los registros financieros y los datos estructurados almacenados en el Anillo 2.

## El problema de la ingesta profunda

Las configuraciones de servidor estándar procesan el tráfico de internet entrante dentro del mismo entorno de ejecución que contiene los datos centrales. Una vulnerabilidad en cualquier ruta de ingesta otorga acceso al mismo espacio de memoria que los registros principales. El aislamiento no puede añadirse retroactivamente una vez que un proceso comparte memoria con otro.

## Posicionamiento en el perímetro

La plataforma sitúa todos los procesos de ingesta en el borde físico y lógico del sistema. Ningún payload de internet entrante cruza hacia el Anillo 2 sin antes pasar por la capa de perímetro del Anillo 1. El Anillo 1 se implementa como un conjunto de procesos servidores MCP (Model Context Protocol), uno por canal de ingesta (correo electrónico, sistema de archivos, registros de personas, input externo).

Cada proceso del Anillo 1 acepta el payload, lo desinfecta —elimina metadatos de transporte, valida la estructura y descarta entradas malformadas— y luego entrega únicamente el registro limpio y estructurado al Anillo 2. El internet público nunca está en contacto directo con el Anillo 2 ni con el Anillo 3.

## Efecto sobre la integridad de la auditoría

Dado que los payloads en bruto se sanean en el perímetro y son los registros limpios los que procesa el Anillo 2, el registro de auditoría refleja sobre qué actuó el sistema, no lo que llegó a nivel de red. Esta separación es una condición previa del diseño del registro WORM.

## Véase también

- [[topic-worm-ledger-architecture]] — el registro WORM que almacena los datos saneados
- [[topic-service-email]] — ingesta del Anillo 1 para correo electrónico
- [[compounding-substrate]] — la arquitectura de tres anillos en contexto

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
