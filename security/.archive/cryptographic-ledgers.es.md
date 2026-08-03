---
schema: foundry-doc-v1
title: "Libros contables criptográficos"
slug: cryptographic-ledgers
short_description: "Los libros mayores criptográficos son el patrón de almacenamiento de estado inmutable utilizado en la plataforma PointSav, imponiendo inmutabilidad matemática para que cualquier alteración de un hecho registrado rompa una cadena hash criptográfica verificable en lugar de requerir confianza en controles de acceso administrativo."
category: security
type: topic
content_type: topic
quality: complete
status: archived
archived: 2026-08-03
archived_reason: "reemplazado por el piloto de autoría fresh-draft-first frente a los nuevos tokens de content-schema (schema-topic.yaml)"
superseded_by: cryptographic-ledgers
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-07-31
editor: pointsav-engineering
paired_with: cryptographic-ledgers.md
cites: []
language: es
---


Los libros contables criptográficos son el patrón de almacenamiento de estado inmutable utilizado en la plataforma [[pointsav-overview|PointSav]]. Aplican inmutabilidad matemática de modo que cualquier alteración a un hecho registrado rompe una cadena de hash criptográfica verificable, en lugar de requerir confianza en controles de acceso administrativos. Véase también [[merkle-proofs-as-substrate-primitive|pruebas Merkle como primitiva de sustrato]] y [[worm-ledger-design|el diseño del registro WORM]].

## El problema que resuelven

En los sistemas de bases de datos tradicionales, un administrador de sistema con privilegios suficientes puede editar silenciosamente un registro — alterando una entrada financiera o un registro de cumplimiento sin activar ninguna alarma automática. El libro contable criptográfico elimina esta vulnerabilidad suprimiendo el concepto de una ruta mutable con privilegios.

## Cómo funciona

La arquitectura separa cada carga entrante en dos entidades: el activo y su registro de estado.

**El activo** — cuando un usuario envía un archivo al sistema, la capa de almacenamiento lo coloca en una bóveda aislada y elimina todos los permisos de ejecución. Se convierte en un objeto binario inerte.

**El registro de estado** — el sistema genera concurrentemente un registro determinista con metadatos legibles y un checksum SHA-256 del activo original. El registro de estado se añade al libro contable; no puede modificarse después de ser añadido.

## Estructura de árbol Merkle

Cada nueva entrada es hasheada; el hash de la nueva entrada se combina con el hash de la entrada anterior para producir el hash del estado actual del árbol. El checkpoint es firmado por la clave del inquilino y publicado. Si los hashes coinciden y la [[merkle-proofs-as-substrate-primitive|prueba de inclusión]] se verifica, el registro está intacto.

## Arquitectura

El libro contable criptográfico de [[pointsav-overview|PointSav]] utiliza el formato C2SP tlog-tiles — la misma estructura en disco que usan los registros de Certificate Transparency y Sigstore Rekor. Los "tiles" son archivos de texto estáticos codificados en base64 que contienen 256 entradas cada uno en el nivel hoja, con tiles de nivel intermedio de [[merkle-proofs-as-substrate-primitive|Merkle]] por encima. Este formato es legible por humanos, verificable de forma independiente y compatible con las herramientas estándar de Certificate Transparency.

**Corrección (2026-07-28):** el formato en disco actual es un único archivo de registro JSON delimitado por saltos de línea por inquilino (`<root>/<moduleId>/log.jsonl`), no una estructura multi-archivo C2SP tlog-tiles — verificado contra `service-fs/src/posix_tile.rs`, cuyos propios comentarios de documentación describen "archivos de tile segmentados por lotes (256 entradas por segmento sellado)" como "la mejora de rendimiento natural y un commit de seguimiento," aún no implementado; la estructura `PosixTileLedger` de ese archivo mantiene una única `log_path`, no un conjunto de archivos de tile. Las propiedades criptográficas que este artículo describe — entradas encadenadas por hash, checkpoints firmados con Ed25519, pruebas de inclusión y de consistencia — son reales y están implementadas en ese mismo archivo, solo que no con el diseño específico de archivos de tile en disco descrito aquí. La afirmación de anclaje mensual en Rekor que sigue, en cambio, **está verificada como precisa** — véase la nota tras ese párrafo.

Mensualmente, el checkpoint firmado de cada inquilino se envía al registro público de transparencia Sigstore Rekor v2. Una vez anclado, el checkpoint es público y el inquilino no puede alterar retroactivamente ningún registro anterior sin que el estado manipulado resulte detectable frente al checkpoint anclado.

**Verificado como preciso (2026-07-28):** confirmado contra `service-fs/anchor-emitter` (580 líneas; un cliente real de envío `hashedRekordRequestV002` a Sigstore Rekor v2) y su temporizador systemd `infrastructure/local-fs-anchoring/local-fs-anchor.timer`, que se ejecuta mensualmente el día 1 a las 02:30 UTC. Esta parte del artículo coincide con la implementación real; solo el párrafo sobre el formato de tiles necesitaba corrección.

## Aplicaciones

El libro contable criptográfico se aplica a todos los datos de cara al cliente en la plataforma:

- **Registros corporativos** — las entradas financieras, los documentos de cumplimiento y los registros operativos se anexan todos al libro contable WORM antes de cualquier otro procesamiento.
- **Cumplimiento SOC 2** — la invariante de solo-anexado del libro contable y el anclaje en Rekor satisfacen los requisitos de Integridad de Procesamiento de SOC 2 (PI4 — las salidas son completas, precisas y oportunas).
- **Registro regulatorio** — la arquitectura está estructuralmente alineada con los requisitos de mantenimiento electrónico de registros para corredores de bolsa de la Regla 17a-4(f) de la SEC (vía WORM) y con los requisitos de servicio de preservación calificada de eIDAS para la prueba de existencia a largo plazo.
- **Registro de auditoría** — cada lectura del libro contable se registra a su vez en un sub-registro de auditoría, que también es WORM y también está anclado.

## Véase también

- [[worm-ledger-architecture]]
- [[crypto-attestation]]
- [[capability-based-security]]
- [[compounding-substrate]]
- [[sel4-microkernel-substrate]]
