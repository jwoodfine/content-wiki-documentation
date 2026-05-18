---
schema: foundry-doc-v1
type: topic
slug: service-fs-architecture
short_description: "Un libro mayor inmutable Write-Once-Read-Many por tenant que sirve como la columna vertebral resistente a manipulación para todos los registros de plataforma, implementado como pila desacoplada de cuatro capas con envolventes de tiempo de ejecución de núcleo de microkernels duales Linux y seL4."
title: "Arquitectura de Service-FS: El Núcleo WORM"
category: services
audience: vendor-public
bcsc_class: current-fact
status: active
language: es
last_edited: 2026-05-08
editor: pointsav-engineering
paired_with: service-fs-architecture.md
---

Cada registro escrito en la plataforma PointSav — anclajes de identidad, comunicaciones de correo electrónico, artefactos de documentos — llega a `service-fs`, un libro contable inmutable de escritura única y lectura múltiple (WORM) por inquilino. Una vez escrito, los registros no pueden modificarse ni eliminarse; el libro contable es la columna vertebral con evidencia de manipulación que los servicios del Anillo 2 consultan y los servicios del Anillo 1 escriben.

## Estructura de Cuatro Capas

- **Anclaje (L4):** Publicación mensual de pruebas de integridad en registros públicos externos (Sigstore Rekor).
- **Protocolo (L3):** Interfaz de comunicación que asegura que los datos de un cliente nunca se mezclen con otros — límites por inquilino aplicados por `moduleId`.
- **Contrato API WORM (L2):** Definiciones en Rust (`append`, `read_since`, `checkpoint`) que aseguran la consistencia del sistema independientemente de la tecnología de disco.
- **Almacenamiento (L1):** El motor físico que guarda los datos en formato de texto estándar (C2SP tlog-tiles), asegurando su legibilidad por un siglo.

## Entornos de Ejecución

El sistema es dual por diseño:
- **Actualidad:** Funciona como un servicio estándar en Linux (daemon), ideal para servidores actuales.
- **Futuro previsto:** Está preparado para ejecutarse como un dominio de protección seL4 verificado en dispositivos físicos, proporcionando la máxima seguridad matemáticamente verificable.

## Durabilidad y Cumplimiento

La plataforma logra el cumplimiento estructural WORM al denegar estructuralmente la modificación de registros en la capa de almacenamiento. Los puntos de control firmados (C2SP signed-note) prueban el estado del libro contable en cualquier momento. Un sub-libro contable de auditoría registra cada evento de lectura para satisfacer los requisitos de integridad de procesamiento de SOC 2.

## Véase también

- [[fs-anchor-emitter]]
- [[service-fs-security-compliance]]
- [[worm-ledger-architecture]]
- [[sel4-foundation]]
