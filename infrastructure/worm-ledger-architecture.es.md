---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: worm-ledger-architecture
short_description: "El registro WORM es un sustrato inmutable de solo anexar que utiliza encadenamiento de hash criptográfico y aislamiento estructural para proporcionar una columna vertebral duradera para servicios de ingesta perimetral mientras mantiene registros a prueba de manipulaciones adecuados para cumplimiento regulatorio."
title: "Sustrato del ledger WORM: arquitectura de cuatro capas"
audience: vendor-public
bcsc_class: current-fact
language: es
paired_with: worm-ledger-architecture.md
category: infrastructure
status: active
quality: complete
last_edited: 2026-06-23
editor: pointsav-engineering
---



[[service-fs-architecture|`service-fs`]] proporciona el sustrato de almacenamiento inmutable de "escritura única y lectura múltiple" (WORM) para cada cliente en los [[three-ring-architecture|servicios Ring 1]], incluyendo [[service-people]] y [[service-email]]. Esta arquitectura, descrita en el [[worm-ledger-design|diseño del libro de registros WORM]], garantiza que todos los registros —desde identidades hasta comunicaciones— sean permanentes, imposibles de borrar y verificables criptográficamente.

## Arquitectura de Cuatro Capas

1. **Capa 4 - Anclaje (Anchoring):** Se prevé el anclaje mensual de estados a la red pública Sigstore Rekor, proporcionando una prueba externa de integridad sin exponer datos privados.
2. **Capa 3 - Protocolo de Red:** Comunicación actual mediante HTTP/JSON, con una transición planificada al protocolo MCP (Model Context Protocol).
3. **Capa 2 - API del Ledger:** Un contrato en Rust que define las operaciones de escritura y lectura, independiente del sistema operativo subyacente.
4. **Capa 1 - Almacenamiento de Teselas (Tiles):** El estándar **C2SP tlog-tiles** (RFC 9162 v2) es el formato objetivo para una legibilidad de 100 años; el backend de bloques está planificado y aún no implementado. La implementación actual conserva un registro JSON de solo adición por inquilino con resúmenes SHA-256 por carga.

## Soberanía y Cumplimiento

Este diseño permite que la plataforma funcione hoy como un demonio en Linux y, en el futuro, como un micro-kernel verificado (seL4) en dispositivos físicos (Totebox). Cumple nativamente con los requisitos de inmutabilidad de la SEC estadounidense y los estándares de preservación calificada eIDAS de la Unión Europea, devolviendo el control total del archivo histórico al propietario de los datos.

## Lo que garantiza WORM — y lo que no

Comprender las propiedades de integridad del libro mayor requiere claridad sobre qué cubre el invariante de solo anexar y dónde se detiene.

Lo siguiente describe el modelo de integridad que el libro mayor está **diseñado para proporcionar**. El almacenamiento en formato de bloques, el encadenamiento de hash y el anclaje externo están planificados; hoy el servicio registra un resumen SHA-256 por carga por entrada.

**La garantía WORM cubre (actual):**
- **Inmutabilidad tras la escritura.** Un registro escrito en el libro mayor no puede ser modificado ni eliminado por ningún actor — incluida la propia plataforma. Esto es estructural, no una política.
- **Evidencia de manipulación a nivel de registro.** Cada registro añadido lleva un resumen SHA-256 por carga. La modificación de cualquier registro almacenado es detectable recalculando el resumen.

**La garantía WORM está diseñada para cubrir (planificado):**
- **Evidencia de manipulación a nivel de cadena.** Un auditor con los archivos de bloques C2SP y una implementación SHA-256 podrá verificar la cadena de hash completa sin un servicio activo una vez implementado el backend de bloques.
- **Verificabilidad externa.** El anclaje recurrente a Sigstore Rekor está **previsto** para crear una cadena de marca temporal pública que persiste independientemente de la instancia de la plataforma. No hay anclaje hoy.
- **Legibilidad durante décadas.** El formato de texto plano C2SP tlog-tiles (planificado) requerirá solo utilidades Unix básicas para decodificarse. No se necesitan herramientas propietarias.

**La garantía WORM no cubre:**
- **Corrección de lo que fue escrito.** WORM no puede detectar ni prevenir que un registro incorrecto entre en el libro mayor. La corrección es responsabilidad de la [[app-console-input|compuerta de verificación con intervención humana]] en F12, no de la capa de almacenamiento.
- **Disponibilidad.** WORM garantiza durabilidad; no garantiza que el libro mayor sea siempre accesible. La disponibilidad es una cuestión de infraestructura.
- **Búsqueda o consulta.** El libro mayor almacena registros; no los indexa. La búsqueda de texto completo y las consultas de entidades las proporcionan [[service-search|`service-search`]] y [[service-content|`service-content`]].
- **Aislamiento entre inquilinos por encima de la capa de almacenamiento.** El invariante WORM es por inquilino. El control de acceso entre inquilinos lo aplica el protocolo de red (límites `X-Module-ID`) y está previsto que lo aplique la mediación de capacidades seL4 en el Envolvente B.

## Puntos clave

- El libro mayor WORM es una garantía estructural: la operación de adición se aplica en la capa API, no por convención. Las operaciones `read_since` y `checkpoint` están planificadas.
- La inmutabilidad protege el rastro de auditoría después de que un registro se asienta; la [[app-console-input|Máquina de Entrada F12]] es la compuerta de calidad antes de que se asiente.
- El formato C2SP tlog-tiles y el anclaje a Sigstore son el **modelo previsto** para la verificabilidad por terceros; el backend de bloques y la operación de anclaje están planificados.
- La arquitectura de cuatro capas está diseñada para permitir que el motor de almacenamiento (Envolvente A: POSIX; Envolvente B: capacidades seL4) cambie sin alterar el contrato API ni el protocolo de red.

## Véase también

- [[worm-ledger-design]] — mapeo de cumplimiento regulatorio y argumento de inmutabilidad estructural
- [[worm-ledger-storage-architecture]] — detalle de la capa de almacenamiento: formato de bloques, durabilidad atómica, entornos dual-target
- [[service-fs-architecture]] — el servicio que implementa esta arquitectura como libro mayor desplegado por inquilino
- [[app-console-input]] — la compuerta de intervención humana F12 que es el control de calidad aguas arriba del libro mayor
- [[sel4-microkernel-substrate]] — la trayectoria de aislamiento por capacidades seL4 prevista para inquilinos
- [[verify-worm-ledger]] — guía paso a paso: exportar un bloque, verificar la cadena de hashes y validar el punto de control firmado
- [[read-the-command-ledger]] — guía paso a paso: leer entradas del libro mayor WORM desde la pestaña LEDGER de F12
