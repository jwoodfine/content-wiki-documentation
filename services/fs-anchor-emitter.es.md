---
schema: foundry-doc-v1
title: "Emisor de anclaje FS"
slug: fs-anchor-emitter
category: services
type: topic
content_type: topic
quality: complete
index_group: specialist-and-domain-services
short_description: "Un binario de un solo uso que obtiene un punto de control firmado del libro mayor WORM desde service-fs, lo ancla en el registro público de transparencia Sigstore Rekor y escribe el resultado de vuelta — haciendo el estado del libro mayor auditable desde fuera de la plataforma."
status: active
audience: vendor-public
bcsc_class: current-fact
last_edited: 2026-08-24
editor: pointsav-engineering
paired_with: fs-anchor-emitter.md
---

`fs-anchor-emitter` conecta el [[worm-ledger-design|libro mayor Write-Once-Read-Many]] inmutable de la plataforma con un registro público de transparencia de terceros. No genera él mismo el punto de control del libro mayor — eso lo hace [[service-fs|service-fs]] — la función del emisor es obtener un punto de control ya firmado, enviarlo a Sigstore Rekor y registrar el resultado. Este diseño mantiene la generación del punto de control y el anclaje público como pasos separados y auditables de forma independiente.

## Qué hace, en orden

El emisor es un binario de un solo uso, invocado según un calendario por un proceso externo, en lugar de ejecutar su propio temporizador:

1. **Obtener.** `GET /v1/checkpoint` desde `service-fs`, limitado al ID de módulo del inquilino en ejecución. El punto de control lleva una cadena de origen, un tamaño de árbol monótono, una raíz Merkle codificada en base64 y — ya aplicados por `service-fs` — una firma y una clave pública.
2. **Anclar en Rekor.** El punto de control se serializa, se aplica SHA-256 y se envuelve en una entrada Sigstore `hashedRekordRequestV002` (la forma de solicitud de Rekor v0.0.2). El emisor genera un par de claves Ed25519 nuevo solo para este paso, en cada ejecución — esa clave efímera existe únicamente para producir la marca de tiempo y la prueba de inclusión de Rekor, no para afirmar una identidad persistente. La solicitud se envía al endpoint de Rekor configurado.
3. **Escribir de vuelta.** La entrada resultante del registro de transparencia se envía a `/v1/append` de `service-fs`, de modo que el propio registro de la plataforma muestre exactamente qué se ancló públicamente y cuándo.

## Configuración

Tres variables de entorno, leídas una vez al inicio:

| Variable | Propósito | Predeterminado |
|---|---|---|
| `FS_ENDPOINT` | URL base de la instancia de `service-fs` desde la que obtener y a la que escribir de vuelta | ninguno — requerido |
| `FS_MODULE_ID` | Módulo de inquilino que delimita la obtención del punto de control | ninguno — requerido |
| `REKOR_URL` | Endpoint de entradas de registro de Rekor | la API v2 de `log2025-1.rekor.sigstore.dev` |

Un código de salida distinto identifica dónde falló una ejecución: error de configuración, fallo al obtener el punto de control, fallo al enviar a Rekor, o fallo en la escritura final de vuelta a `service-fs`.

## Cadencia y alcance

El binario en sí no tiene lógica interna de generación ni de prueba de consistencia — ambas requerirían mantener el estado del libro mayor, algo que este diseño mantiene deliberadamente fuera del paso de anclaje. Su propio código fuente lo identifica como "Doctrine Invention #7," documentado como anclaje mensual en Rekor de los puntos de control de `service-fs` — un equilibrio deliberado entre densidad probatoria y sobrecarga de red, no un límite técnico de con qué frecuencia podría ejecutarse.

## Véase también

- [[service-fs]] — genera y firma los puntos de control que este emisor obtiene
- [[worm-ledger-design]] — el libro mayor que el punto de control certifica
- `service-fs` — la postura de cumplimiento que respalda este anclaje
