---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: service-fs
title: "service-fs — el núcleo del libro mayor WORM"
short_description: "El libro mayor inmutable Write-Once-Read-Many por inquilino que respalda cada registro escrito en la plataforma — una interfaz HTTP y MCP real e implementada sobre un registro de anexado encadenado por hash, con anclaje externo mensual a un registro público de transparencia."
category: services
index_group: ring-1-boundary-ingest
quality: complete
audience: vendor-public
bcsc_class: current-fact
language_protocol: PROSE-TOPIC
status: active
aliases: [service-fs-architecture, service-fs-security-compliance]
last_edited: 2026-09-05
editor: pointsav-engineering
paired_with: service-fs.md
---

Cada registro escrito en la plataforma PointSav — anclajes de identidad, comunicaciones de correo electrónico, artefactos de documentos — llega a `service-fs`, un libro contable inmutable de escritura única y lectura múltiple (WORM) por inquilino. Una vez escrito, los registros no pueden modificarse ni eliminarse; el libro contable es la columna vertebral con evidencia de manipulación que los servicios del [[three-ring-architecture|Anillo 2]] consultan y los servicios del Anillo 1 escriben. El artículo sobre [[worm-ledger-design|diseño del libro mayor WORM]] describe la filosofía de diseño WORM en detalle.

`service-fs` no es un sistema de archivos de propósito general. Un sistema de archivos local permite lecturas, escrituras, modificaciones y eliminaciones a través de un árbol de directorios estándar. `service-fs` expone una superficie reducida de anexar-y-verificar: escribir un nuevo registro, leer hacia adelante desde un punto del registro, y producir una prueba firmada del estado actual del libro mayor — además de las operaciones criptográficas que permiten a quien llama verificar una entrada específica o confirmar que dos puntos de control son consistentes entre sí. Esta superficie reducida es lo que hace que las garantías de integridad del libro mayor sean estructuralmente sólidas en lugar de aplicadas por política.

## Puntos clave

- El servicio expone anexado, lectura, punto de control, y verificación tanto de entrada única como entre puntos de control, tanto por HTTP como por MCP — todo implementado, no planeado.
- El libro mayor es por inquilino — cada Totebox mantiene su propio libro mayor aislado; no son posibles lecturas entre inquilinos en la capa de almacenamiento.
- Cada entrada se encadena criptográficamente con la anterior (una cadena de hash SHA-256 lineal), y un sub-libro mayor de auditoría dedicado registra cada evento de lectura junto al libro mayor de registros principal.
- El anclaje recurrente a Sigstore Rekor por [[fs-anchor-emitter]] crea una cadena de marcas de tiempo externa y públicamente verificable para todo el libro mayor, con una cadencia mensual.
- El despliegue actual es un demonio Linux/BSD estándar con aislamiento a nivel de proceso — una garantía real pero más débil que la que ofrecería un límite impuesto por un microkernel. Se exploró un entorno de microkernel seL4 como diseño de unikernel de bajo nivel bajo este mismo nombre de paquete; ese diseño ahora vive en su propio paquete de proveedor separado, y no hay un objetivo seL4 en desarrollo activo dentro del código actual de `service-fs`.

## La arquitectura por capas

`service-fs` separa las responsabilidades en capas que pueden cambiar de forma independiente:

- **Anclaje:** trabajo mensual realizado por [[fs-anchor-emitter]], anclando puntos de control firmados al registro público de Sigstore Rekor.
- **Protocolo de transporte:** una interfaz HTTP (vía axum) y una interfaz de servidor MCP, ambas exponiendo las mismas operaciones subyacentes a distintos tipos de llamadores.
- **Contrato del libro mayor:** un trait de Rust estable — anexar, leer desde un cursor, punto de control, y ambas operaciones de prueba — sobre el que se componen tanto la capa de transporte como la de almacenamiento, de modo que cualquiera puede cambiar sin romper a la otra.
- **Almacenamiento:** hoy, un registro de cadena de hash por inquilino basado en archivos POSIX, usando el formato C2SP tlog-tiles para la estructura de mosaicos en disco y el formato C2SP signed-note para los puntos de control.

## Durabilidad

El formato en disco del libro mayor sigue estándares abiertos en lugar de un esquema propietario — C2SP tlog-tiles para el registro mismo, C2SP signed-note para los puntos de control — de modo que un lector futuro pueda decodificar los archivos en bruto con herramientas estándar incluso sin el software propio de la plataforma. Cada escritura también llega al sub-libro mayor de auditoría, un registro WORM independiente de la actividad de lectura junto a los datos principales.

## Modelo de amenazas

- **Manipulación por el operador.** Incluso un administrador con acceso directo al almacenamiento no puede alterar un registro pasado sin romper la cadena de hash — y una cadena rota es detectable tanto localmente como contra los puntos de control anclados externamente en Rekor.
- **Obsolescencia del proveedor.** El formato en disco de estándar abierto está diseñado para sobrevivir al software de cualquier proveedor en particular.

## Véase también

- [[fs-anchor-emitter]] — el emisor de anclaje periódico que registra puntos de control del libro mayor en Sigstore Rekor
- [[worm-ledger-design]] — la filosofía de diseño detrás del enfoque WORM
- [[machine-based-auth]] — el sistema de autenticación que gobierna quién puede actuar en nombre del libro mayor
- [[service-content]] — un consumidor del Anillo 2 de los registros que mantiene `service-fs`
