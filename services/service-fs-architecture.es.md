---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: service-fs-architecture
short_description: "Un libro mayor inmutable Write-Once-Read-Many por tenant que sirve como la columna vertebral resistente a manipulación para todos los registros de plataforma, implementado como pila desacoplada de cuatro capas con envolventes de tiempo de ejecución de núcleo de microkernels duales Linux y seL4."
title: "Arquitectura de Service-FS: el núcleo WORM"
category: services
audience: vendor-public
bcsc_class: current-fact
status: active
language: es
last_edited: 2026-05-08
editor: pointsav-engineering
paired_with: service-fs-architecture.md
---

Cada registro escrito en la plataforma PointSav — anclajes de identidad, comunicaciones de correo electrónico, artefactos de documentos — llega a `service-fs`, un libro contable inmutable de escritura única y lectura múltiple (WORM) por inquilino. Una vez escrito, los registros no pueden modificarse ni eliminarse; el libro contable es la columna vertebral con evidencia de manipulación que los servicios del [[three-ring-architecture|Anillo 2]] consultan y los servicios del Anillo 1 escriben. El artículo sobre [[worm-ledger-design|diseño del libro mayor WORM]] describe la filosofía de diseño WORM en detalle.

`service-fs` no es un sistema de archivos de propósito general. Un sistema de archivos local permite lecturas, escrituras, modificaciones y eliminaciones a través de un árbol de directorios estándar. `service-fs` expone solo tres operaciones: `append` (añadir un registro), `read_since` (leer hacia adelante desde un punto de control) y `checkpoint` (crear una prueba firmada del estado). La superficie de API reducida es lo que hace que las garantías de integridad del libro mayor sean estructuralmente sólidas en lugar de impuestas por políticas.

## Estructura de Cuatro Capas

El artículo sobre [[worm-ledger-storage-architecture|arquitectura de almacenamiento WORM]] describe cómo cada envolvente satisface la restricción de solo adición.

- **Anclaje (L4):** Publicación mensual de pruebas de integridad realizadas por [[fs-anchor-emitter]] en registros públicos externos (Sigstore Rekor).
- **Protocolo (L3):** Interfaz de comunicación (HTTP/axum hoy; [[mcp-substrate-protocol|MCP]] a largo plazo) que asegura que los datos de un cliente nunca se mezclen con otros — límites por inquilino aplicados por `moduleId`.
- **Contrato API WORM (L2):** Definiciones en Rust (`append`, `read_since`, `checkpoint`) que aseguran la consistencia del sistema independientemente de la tecnología de disco.
- **Almacenamiento (L1):** El motor físico que guarda los datos en formato de texto estándar (C2SP tlog-tiles), asegurando su legibilidad por un siglo.

## Entornos de Ejecución

El sistema es dual por diseño:
- **Actualidad:** Funciona como un servicio estándar en Linux (daemon), ideal para servidores actuales.
- **Futuro previsto:** Está preparado para ejecutarse como un dominio de protección [[sel4-microkernel-substrate|seL4]] verificado en dispositivos físicos, proporcionando la máxima seguridad matemáticamente verificable.

## Durabilidad y Cumplimiento

La plataforma logra el cumplimiento estructural WORM al denegar estructuralmente la modificación de registros en la capa de almacenamiento. Los puntos de control firmados (C2SP signed-note) prueban el estado del libro contable en cualquier momento. Un sub-libro contable de auditoría registra cada evento de lectura para satisfacer los requisitos de integridad de procesamiento de SOC 2.

## Puntos clave

- `service-fs` es un libro mayor WORM, no un sistema de archivos. Su superficie de API tiene tres operaciones: `append`, `read_since`, `checkpoint`.
- El libro mayor es por inquilino — cada Totebox tiene su propio libro mayor aislado; no son posibles lecturas cruzadas entre inquilinos en la capa de almacenamiento.
- La arquitectura de cuatro capas desacopla el protocolo de comunicación, el contrato de API y el motor de almacenamiento, de modo que el intercambio al Envolvente B de seL4 no requiere reescribir el servicio.
- La durabilidad usa estándares abiertos: C2SP tlog-tiles (legibilidad de 100 años) y puntos de control C2SP signed-note (demostrabilidad compacta).
- El anclaje mensual a Sigstore Rekor por parte de [[fs-anchor-emitter]] crea una cadena de marca temporal externa y públicamente verificable para todo el libro mayor.

## Véase también

- [[fs-anchor-emitter]] — el emisor periódico de anclajes que registra el libro mayor en Sigstore Rekor
- [[service-fs-security-compliance]] — perfil de cumplimiento: SOC 2, alineación regulatoria WORM
- [[worm-ledger-architecture]] — arquitectura WORM a nivel de infraestructura
- [[worm-ledger-design]] — la filosofía de diseño detrás del enfoque WORM
- [[sel4-microkernel-substrate]] — el envolvente Microkit seL4 (Envolvente B) previsto como tiempo de ejecución
- [[service-content]] — el Motor de Gravedad que escribe los registros de geometría base L0 en service-fs
- [[service-pointsav-link|Servicio PointSav Link]] — adaptador conectable que conecta nodos os-* a la red de flota
