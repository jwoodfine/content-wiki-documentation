---
schema: foundry-doc-v1
title: "Diseño del libro de registros WORM"
slug: worm-ledger-design
category: infrastructure
index_group: storage-substrate
type: topic
content_type: topic
quality: complete
short_description: "Sustrato de libro mayor Write-Once-Read-Many de los servicios Ring 1 de PointSav, diseñado hacia un formato encadenado por hash y firmado que cumple la normativa por estructura."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-06-23
editor: pointsav-engineering
forward_looking: true
cites:
 - c2sp-tlog-tiles
 - c2sp-signed-note
 - sigstore-rekor-v2
 - rfc-9162
 - sec-17a-4-f
references:
  - id: 1
    text: "C2SP. 'tlog-tiles: Tile-based logs specification.' C2SP.org, 2024."
    url: "https://c2sp.org/tlog-tiles"
  - id: 2
    text: "Sigstore Project. 'Rekor — Software Supply Chain Transparency Log.' Sigstore.dev, 2024."
    url: "https://rekor.sigstore.dev/"
  - id: 3
    text: "C2SP. 'signed-note: Signed checkpoint note format.' C2SP.org, 2024."
    url: "https://c2sp.org/signed-note"
  - id: 4
    text: "Laurie, B. et al. 'RFC 9162: Certificate Transparency Version 2.0.' IETF, 2021."
    url: "https://www.rfc-editor.org/rfc/rfc9162"
paired_with: worm-ledger-design.md
---

Un registro regulado es tan confiable como la mano más débil que puede alcanzarlo. Una bandera de administrador, una actualización de software, una restauración de respaldo — cualquiera de ellas puede alterar silenciosamente un registro histórico. Una política que promete que no lo harán no es lo mismo que una estructura que no se lo permite.

Los [[three-ring-architecture|servicios del anillo 1]] de PointSav conservan cada registro de límite — sistema de archivos, datos de personas, correo electrónico, entrada estructurada — en un libro de registros de escritura única y lectura múltiple (WORM), a través del [[service-fs-architecture|sustrato service-fs]]. El hash de cada registro se encadena con el anterior, de modo que alterar cualquier entrada pasada cambia todos los hashes posteriores — una propiedad que ya se cumple hoy, sobre un registro de solo adición plano por inquilino (`log.jsonl`). El libro de registros está **diseñado para adoptar** el formato de registro de transparencia C2SP tlog-tiles como su disposición en disco; esa segmentación en bloques es lo único que aún está por delante de la implementación actual.

El libro de registros está **diseñado como cuatro capas** — almacenamiento por bloques, una API WORM, un protocolo de red y anclaje recurrente de puntos de control firmados en un registro público de transparencia. La inmutabilidad es una propiedad del sustrato de almacenamiento, no de la política operativa.

Para un comprador regulado la consecuencia es concreta. Una sola arquitectura satisface tres regímenes de conservación a la vez: las normas estadounidenses para agentes bursátiles bajo la Norma SEC 17a-4(f), la conservación cualificada de la UE bajo eIDAS y los Criterios de Servicios de Confianza SOC 2. Y un auditor externo puede verificar cualquier registro sin la cooperación del operador de la plataforma.

## La pila de cuatro capas

**Capa 1 — almacenamiento por bloques.** La arquitectura de almacenamiento **especifica** la especificación C2SP tlog-tiles [^1] — el mismo formato de bloques que usan internamente Trillian-Tessera y externamente Sigstore Rekor v2 [^2] — como primitivo de almacenamiento objetivo. La implementación actual de `service-fs` conserva un registro de solo adición JSON por inquilino pendiente del backend de bloques.

**Capa 2 — API del libro de registros WORM.** Las cinco operaciones del trait — abrir un libro para un inquilino, añadir una carga y recibir un cursor, leer entradas desde un cursor, producir un punto de control firmado [^3] y verificar pruebas de inclusión y consistencia — están todas implementadas hoy. El `service-fs` en producción expone `POST /v1/append`, `GET /v1/entries`, `GET /v1/checkpoint`, `GET /v1/contract`, `GET /healthz` y `GET /readyz` por HTTP, además de un endpoint MCP. El backend de producción, `PosixTileLedger`, escribe hoy en un archivo `log.jsonl` plano por inquilino — la segmentación real en bloques C2SP es lo que aún falta.

**Capa 3 — protocolo de red.** Una capa de servicio HTTP expone la API del libro de registros en red, con el protocolo MCP — el estándar de 2026 para servicios de herramientas de IA — superpuesto.

**Capa 4 — anclaje externo.** Los puntos de control firmados se publican mensualmente en Sigstore Rekor [^2] mediante un cliente anchor-emitter dedicado, que obtiene el punto de control actual, lo envía como entrada hashedRekord y añade la entrada Rekor resultante de vuelta al libro de registros — un temporizador de systemd impulsa la cadencia mensual. Esto funciona hoy; un auditor externo ya puede confirmar la integridad de un registro contra el registro público sin involucrar al operador.

## Inmutabilidad estructural

La implementación POSIX sigue un patrón de escritura de cuatro pasos: escribir los bytes del bloque en un archivo temporal, sincronizar con `fsync`, renombrar atómicamente a la ruta canónica y establecer el modo de archivo en solo lectura. La estructura de cadena de hash del formato significa que cualquier modificación de un bloque escrito altera la cadena — el hash registrado del bloque anterior deja de coincidir. La modificación es detectable sin un registro de auditoría aparte.

## Estructura por inquilino

Cada libro de registros está ligado a un `moduleId` — un identificador de inquilino que la capa de red exige en cada llamada a la API. Una solicitud cuyo `moduleId` no coincide con el libro abierto se rechaza. Los archivos de bloques se almacenan bajo una ruta por inquilino, y las claves de firma por inquilino producen puntos de control firmados por inquilino.

Un auditor que inspecciona el libro de un inquilino no necesita confiar en que el proveedor mantuvo la separación entre inquilinos. La estructura criptográfica la hace verificable.

## Mapeo de cumplimiento

La **Norma SEC 17a-4(f)** exige conservar los registros en un formato no reescribible y no borrable, con marcas de tiempo verificables y capacidad de verificación independiente por terceros. El formato plano actual satisface la propiedad de no reescritura estructuralmente hoy, por delante de la propia segmentación en bloques. Los puntos de control firmados aportan la marca de tiempo, y la publicación mensual en el registro Rekor funciona hoy, aportando la verificación de terceros sin necesidad de la cooperación del operador.

La **conservación cualificada bajo eIDAS** exige preservación a largo plazo independiente del cambio tecnológico futuro, preservación de la integridad y autenticación del originador. El libro lleva un campo de algoritmo de hash explícito en cada punto de control, de modo que migrar a otra función de hash es una decisión por inquilino que no exige reescribir los bloques históricos. El formato de bloques es una especificación abierta — RFC 9162 [^4] y C2SP — legible con herramientas estándar.

## Anclaje dual y soberanía del cliente

El despliegue ToteboxOS de un cliente opera sus propias instancias de libro de registros con sus propias claves de firma. El cliente es el sujeto de sus propios registros y posee la clave de firma que los atestigua. El espacio de trabajo del proveedor ancla independientemente los mismos puntos de control, dando verificabilidad redundante; el cliente puede excluir al proveedor del arreglo de anclaje en cualquier momento, y la garantía de integridad no depende de la participación del proveedor.

Esta propiedad — soberanía de claves del cliente con redundancia opcional del proveedor — no está disponible en un servicio en la nube administrado, que es arquitectónicamente el custodio tanto de los datos como de la clave de firma.

## Estado de implementación

El servicio Ring 1 `service-fs` implementa el sustrato completo del libro de registros WORM en producción: adición, entradas, punto de control, contrato, salud y disponibilidad por HTTP, además de la firma de puntos de control y las pruebas de inclusión y consistencia a nivel del trait del libro. Cada registro añadido lleva un resumen SHA-256 por carga, encadenado al hash del libro en curso. El anclaje mensual en Rekor de los puntos de control de producción funciona hoy mediante un cliente anchor-emitter dedicado con temporizador de systemd. Lo que aún queda por delante del propio objetivo del diseño es el formato de almacenamiento: `PosixTileLedger` conserva actualmente los datos en un archivo `log.jsonl` plano por inquilino, aún no segmentado en verdaderos bloques C2SP.

## Véase también

- [[three-ring-architecture]] — el límite del anillo 1 donde opera el libro de registros WORM
- [[worm-ledger-architecture]] — la integración arquitectónica de cuatro capas: almacenamiento por bloques, API WORM, protocolo de red, anclaje
- [[worm-ledger-storage-architecture]] — detalle de la capa de almacenamiento: formato C2SP tlog-tiles, disciplina de escritura atómica
- [[service-fs-architecture]] — la implementación `service-fs` que ejecuta este sustrato en producción
- [[compounding-doorman]] — el servicio del anillo 3 cuyo libro de auditoría usa el mismo primitivo
- [[trajectory-substrate]] — el registro de señal de entrenamiento que usa el mismo formato de libro
