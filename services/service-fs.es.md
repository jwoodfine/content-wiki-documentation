---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: service-fs
title: "service-fs — el núcleo del libro mayor WORM"
short_description: "El libro mayor inmutable Write-Once-Read-Many por inquilino que respalda cada registro escrito en la plataforma — arquitectura, durabilidad y la postura regulatoria que habilita por construcción."
category: services
audience: vendor-public
bcsc_class: current-fact
status: active
aliases: [service-fs-architecture, service-fs-security-compliance]
last_edited: 2026-07-31
editor: pointsav-engineering
paired_with: service-fs.md
---

Cada registro escrito en la plataforma PointSav — anclajes de identidad, comunicaciones de correo electrónico, artefactos de documentos — llega a `service-fs`, un libro contable inmutable de escritura única y lectura múltiple (WORM) por inquilino. Una vez escrito, los registros no pueden modificarse ni eliminarse; el libro contable es la columna vertebral con evidencia de manipulación que los servicios del [[three-ring-architecture|Anillo 2]] consultan y los servicios del Anillo 1 escriben. El artículo sobre [[worm-ledger-design|diseño del libro mayor WORM]] describe la filosofía de diseño WORM en detalle.

`service-fs` no es un sistema de archivos de propósito general. Un sistema de archivos local permite lecturas, escrituras, modificaciones y eliminaciones a través de un árbol de directorios estándar. `service-fs` expone solo tres operaciones: `append` (añadir un registro), `read_since` (leer hacia adelante desde un punto de control) y `checkpoint` (crear una prueba firmada del estado). La superficie de API reducida es lo que hace que las garantías de integridad del libro mayor sean estructuralmente sólidas en lugar de impuestas por políticas — esta misma estrechez estructural es lo que permite que la postura de cumplimiento descrita más abajo se derive de la arquitectura, no de controles configurables.

## Puntos clave

- `service-fs` es un libro mayor WORM, no un sistema de archivos. La superficie de API implementada tiene dos operaciones: `append` y salud. Las operaciones `read_since` y `checkpoint` están planificadas.
- El libro mayor es por inquilino — cada Totebox tiene su propio libro mayor aislado; no son posibles lecturas cruzadas entre inquilinos en la capa de almacenamiento.
- El cumplimiento de SEC Rule 17a-4(f), eIDAS y SOC 2 se deriva de propiedades arquitectónicas, no de controles configurables: el motor de almacenamiento carece físicamente de la capacidad de eliminar o modificar registros.
- El anclaje recurrente a Sigstore Rekor por parte de [[fs-anchor-emitter]] crea una cadena de marca temporal externa y públicamente verificable. **Verificado en vivo**: la unidad systemd `local-fs-anchor.timer` está activa y se ejecuta mensualmente (confirmado contra el sistema en ejecución).
- El aislamiento de inquilinos mediante seguridad basada en capacidades a nivel de microkernel es el objetivo previsto del despliegue [[sel4-microkernel-substrate|seL4]], no el actual — hoy el aislamiento es a nivel de proceso, bajo un daemon estándar de Linux/BSD.

## La arquitectura de cuatro capas

Para garantizar modularidad y supervivencia, `service-fs` se implementa como una pila desacoplada de cuatro capas:

- **L4: Anclaje (nivel de espacio de trabajo):** Trabajo periódico mensual realizado por [[fs-anchor-emitter]] que ancla puntos de control firmados en el registro público de Sigstore Rekor.
- **L3: Protocolo de comunicación:** La interfaz de comunicación (HTTP/axum hoy; [[mcp-substrate-protocol|MCP]] a largo plazo) que aplica límites por inquilino mediante `moduleId`.
- **L2: API del libro mayor WORM (Rust Trait):** El contrato central estable (`append`, `read_since`, `checkpoint`) que sobrevive a los cambios en las capas superior e inferior.
- **L1: Primitiva de almacenamiento en tiles:** El motor de almacenamiento específico del entorno (POSIX en Linux; mediado por capacidades en [[sel4-microkernel-substrate|seL4]]) usando el formato **C2SP tlog-tiles**.

## Entornos de ejecución duales

`service-fs` está **diseñado** para operar en dos entornos de ejecución desde una sola base de código. El artículo sobre [[worm-ledger-storage-architecture|arquitectura de almacenamiento WORM]] describe el modelo de almacenamiento previsto para cada entorno.

1. **Envolvente A (actual):** Un daemon Linux/BSD bajo systemd. Usa E/S de archivos POSIX estándar y aislamiento de procesos. Este es el único entorno implementado; expone `POST /v1/append` y `GET /healthz`.
2. **Envolvente B (seL4 — diferido):** Un dominio de protección [[sel4-microkernel-substrate|seL4]] Microkit verificado es el objetivo futuro planificado. Está previsto que use `moonshot-database` (PSDB) para almacenamiento direccionado por capacidades, proporcionando aislamiento de inquilinos formalmente verificado. El Envolvente B existe solo como un punto de entrada de referencia (`main_sel4_stub.rs`) que no está compilado en la compilación actual.

## Durabilidad

El formato de durabilidad objetivo usa estándares abiertos:

- **C2SP tlog-tiles:** Un formato basado en texto de estándar abierto que garantiza legibilidad a 100 años, permitiendo que futuros archivistas decodifiquen el almacenamiento usando utilidades Unix estándar sin software propietario ni asistencia del proveedor.
- **Puntos de control C2SP signed-note:** Artefactos compactos y firmados que prueban el estado del libro mayor en cualquier momento.

El backend de tiles está planificado; la compilación actual usa un registro JSON de solo adición por inquilino con resúmenes SHA-256 por carga. Un **sub-libro mayor de auditoría** — un libro mayor WORM dedicado que registra cada evento de lectura — satisface los requisitos de integridad de procesamiento de SOC 2 independientemente de que el formato de tiles esté completo.

## Alineación regulatoria y cumplimiento

La postura de seguridad de `service-fs` no es una capa de políticas sino una propiedad arquitectónica fundamental, diseñada para satisfacer múltiples marcos regulatorios internacionales:

- **SEC Rule 17a-4(f):** La plataforma apunta a la ruta estricta de "WORM", denegando estructuralmente la modificación de registros. Esto supera la alternativa de "rastro de auditoría" que suelen usar los proveedores de nube para enmascarar almacenamiento subyacente mutable.
- **eIDAS (UE 2025/1946):** Se alinea con los estándares de Preservación Calificada, garantizando integridad, autenticidad y accesibilidad a largo plazo "independientemente de futuros cambios tecnológicos."
- **Criterios de Servicios de Confianza SOC 2:** Aborda directamente la Integridad de Procesamiento (PI1, PI4) mediante ingesta firmada y sub-libros de auditoría de lectura, y el Acceso Lógico (CC6) mediante aislamiento a nivel de inquilino.

Tres propiedades estructurales sustentan esta postura:

1. **Inmutabilidad estructural.** La superficie de API de Rust y el motor de almacenamiento subyacente carecen físicamente de la capacidad de eliminar o modificar registros.
2. **Integridad de cadena Merkle.** Cada entrada está vinculada criptográficamente a la siguiente mediante [[merkle-proofs-as-substrate-primitive|pruebas de consistencia Merkle]]; cualquier intento de alterar el historial es detectable al instante.
3. **Testificación externa.** El anclaje mensual al registro público de Sigstore Rekor por parte de [[fs-anchor-emitter]] proporciona una prueba de estado independiente de los propios sistemas internos de la plataforma.

**El aislamiento de inquilinos** es la única propiedad aún en construcción: en el despliegue [[sel4-microkernel-substrate|seL4]] previsto, el aislamiento se aplica mediante [[capability-based-security|seguridad basada en capacidades]] a nivel de microkernel, haciendo el acceso entre inquilinos matemáticamente imposible. Hoy, bajo el Envolvente A, el aislamiento es a nivel de proceso bajo los límites estándar de un daemon Linux/BSD — una garantía real pero más débil que el objetivo seL4.

## Mitigación del modelo de amenazas

- **Manipulación por parte del operador.** Incluso un administrador con acceso root no puede alterar el libro mayor sin romper la cadena Merkle y fallar las verificaciones públicas de consistencia de Rekor. El sistema de [[machine-based-auth|autenticación basada en máquina]] impide la firma no autorizada.
- **Obsolescencia del proveedor.** Los formatos de estándar abierto garantizan la supervivencia de los datos más allá de la vida útil del proveedor de software.
- **Agilidad criptográfica.** El sistema está diseñado para migrar a esquemas de firma poscuánticos (por ejemplo, Dilithium) sin necesidad de una migración completa del almacenamiento.

## Véase también

- [[fs-anchor-emitter]] — el emisor periódico de anclajes que registra el libro mayor en Sigstore Rekor
- [[worm-ledger-architecture]] — arquitectura WORM a nivel de infraestructura
- [[worm-ledger-design]] — la filosofía de diseño detrás del enfoque WORM
- [[sel4-microkernel-substrate]] — el envolvente Microkit seL4 (Envolvente B) previsto como tiempo de ejecución
- [[capability-based-security]] — el mecanismo de aislamiento a nivel de microkernel objetivo del Envolvente B
- [[machine-based-auth]] — el sistema de autenticación que impide la firma no autorizada
- [[service-content]] — el Motor de Gravedad que escribe los registros de geometría base L0 en service-fs
- [[service-pointsav-link|Servicio PointSav Link]] — adaptador conectable que conecta nodos os-* a la red de flota
