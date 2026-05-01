---
schema: foundry-doc-v1
title: "El Substrato WORM de Foundry — Arquitectura del Registro Inmutable de Cuatro Capas"
slug: topic-worm-ledger-architecture
lang: es
paired_with: topic-worm-ledger-architecture.md
category: architecture
status: pre-build
last_edited: 2026-04-28
editor: pointsav-engineering
cites:
  - c2sp-tlog-tiles
  - c2sp-signed-note
  - rfc-9162
  - sigstore-rekor-v2
  - trillian-tessera
  - sec-17a-4-f
  - eidas-qualified-preservation
  - etsi-ts-119-511
  - etsi-en-319-401
  - cen-ts-18170-2025
  - ni-51-102
  - osc-sn-51-721
---

El registro inmutable WORM (Write-Once-Read-Many) es el substrato sobre el que descansa todo el flujo de datos del cliente en Foundry. Antes de que cualquier dato llegue a los servicios de análisis o de conocimiento, pasa por `service-fs` — el servicio de ledger por tenant que no puede modificarse retroactivamente. Este artículo orienta al lector técnico hacia la arquitectura de cuatro capas, los dos sobres de ejecución, el mecanismo de anclaje público y la alineación estructural con normas WORM externas.

## Las cuatro capas

La arquitectura divide sus responsabilidades en cuatro capas independientemente reemplazables. La clave de diseño es que la capa intermedia — el contrato de API en Rust — sobrevive a cambios en las capas que la rodean.

**L1 — Almacenamiento de tiles.** El formato en disco es C2SP tlog-tiles `[c2sp-tlog-tiles]`, el mismo que usan Certificate Transparency v2 `[rfc-9162]`, Trillian-Tessera `[trillian-tessera]` y Sigstore Rekor v2 `[sigstore-rekor-v2]`. Cada tile es un archivo de texto plano codificado en base64 con 256 entradas (o 256 hashes en los niveles intermedios del árbol Merkle). La elección de texto plano no es cosmética: cualquier operador puede inspeccionar el tile con las herramientas Unix habituales sin depender de software propietario.

**L2 — API del registro WORM.** El trait `LedgerBackend` de Rust es el contrato duradero. Su superficie pública — `open`, `append`, `read_since`, `root`, `checkpoint`, `verify_inclusion`, `verify_consistency` — no expone ningún método que elimine o modifique una entrada. El invariante de solo-añadir vive en la superficie de la API, no en una política operativa.

**L3 — Protocolo de cable.** Rutas HTTP con axum 0.7 más un servidor MCP por tenant. La cabecera `X-Foundry-Module-ID` se valida antes de cualquier handler de negocio; una discordancia devuelve un 403 con los valores esperado y recibido. El formato de cable es idéntico en los dos sobres de ejecución.

**L4 — Anclaje.** Doctrina Invención #7 — anclaje mensual de los puntos de verificación firmados por tenant a Sigstore Rekor v2 `[sigstore-rekor-v2]`. La ejecución mensual empaqueta el punto de verificación más reciente de cada tenant, lo envía al fragmento anual del log de Rekor y escribe la entrada devuelta de vuelta en el propio registro del tenant. El anclaje es independiente del trabajo en tiempo de solicitud — el daemon produce puntos de verificación firmados; el proceso de anclaje del workspace los consume.

## Los dos sobres de ejecución

El mismo formato de almacenamiento y el mismo protocolo de cable funcionan en dos entornos de ejecución distintos.

**Sobre A — daemon Linux/BSD bajo systemd (actual).** Runtime asíncrono Tokio, almacenamiento POSIX en `FS_LEDGER_ROOT/<moduleId>/`. El aislamiento por tenant se mantiene mediante espacios de direcciones de proceso separados, permisos de sistema de archivos y la validación de la cabecera en el nivel de cable. Se despliega como una unidad systemd. Funciona en cualquier kernel Linux o BSD — la VM del workspace de Foundry, hardware on-premises del cliente, GCE, EC2, o dentro de una VM huésped Linux/BSD alojada por seL4 en hardware donde seL4 no puede arrancar de forma nativa.

**Sobre B — unikernel seL4 Microkit Protection Domain (trayectoria planificada a largo plazo).** Runtime `sel4-microkit` en Rust. Almacenamiento mediante IPC mediado por capacidades hacia `moonshot-database`. Los tokens de capacidad se otorgan por tenant; el acceso entre tenants requiere una transferencia explícita de capacidades — verificación formal, no una cabecera de cabecera. El límite por tenant es impuesto por el microkernel verificado formalmente, no por convención de software.

La transición del Sobre A al Sobre B no requiere migración de datos: los bytes del tile C2SP son bit a bit idénticos en ambos backends. Los clientes del Sobre A reciben la misma propiedad WORM y la misma cobertura de anclaje de Rekor; el aislamiento verificado formalmente es la capacidad adicional del Sobre B.

## Puntos de verificación y trazabilidad pública

Cada punto de verificación firmado sigue el formato C2SP signed-note `[c2sp-signed-note]` — el mismo que usa Sigstore Rekor v2. Es un artefacto de texto plano pequeño: nombre del log, tamaño del árbol, hash raíz en base64, y una o más líneas de firma Ed25519. Los testigos co-firman añadiendo líneas de firma adicionales. El workspace de Foundry co-firma cada Totebox del cliente por defecto; el cliente puede añadir un testigo externo de su elección.

El anclaje mensual a Rekor convierte la verificabilidad en algo público y externo. Un tercero que no tenga acceso al sistema del cliente puede verificar, a partir del log público de Rekor, que el punto de verificación del tenant existía en el momento del anclaje y que el árbol no ha sido alterado desde entonces.

## Alineación estructural con normas WORM externas

`service-fs` está estructuralmente alineado con dos marcos regulatorios externos. **Esta alineación es estructural, no una declaración de certificación.**

**SEC Rule 17a-4(f)** `[sec-17a-4-f]` — norma estadounidense de conservación electrónica para corredores-agentes (17 CFR §240.17a-4(f)). La enmienda de 2022 introdujo una alternativa de pista de auditoría al WORM; Foundry sigue el camino WORM. El cumplimiento es estructural: la cadena de hashes criptográfica hace imposible la modificación sin invalidar el punto de verificación publicado.

**Servicio cualificado de preservación de eIDAS** `[eidas-qualified-preservation]` — Reglamento de Ejecución (UE) 2025/1946, en vigor desde el 6 de enero de 2026; ETSI TS 119 511 `[etsi-ts-119-511]`; ETSI EN 319 401 v3.2.1 `[etsi-en-319-401]`; CEN TS 18170:2025 `[cen-ts-18170-2025]`. El diseño con agilidad criptográfica y el formato de texto plano C2SP tlog-tiles abordan el requisito del artículo 4(3) de que la prueba de existencia sea válida "con independencia de los cambios tecnológicos futuros."

La distinción entre cumplimiento estructural y cumplimiento por política tiene importancia doctrinal. Una propiedad WORM mantenida por política ("prometemos no modificar") es rebatible. Una mantenida por estructura ("los bytes no pueden modificarse sin romper la firma del punto de verificación publicado") es verificable por cualquier tercero con acceso al log público de Rekor.

## Trayectoria a largo plazo

> **Información prospectiva.** Los elementos descritos a continuación son direcciones de desarrollo planificadas e intencionales. Están sujetos a incertidumbres materiales y no constituyen garantías de resultados futuros. La postura de divulgación continua de Foundry se rige por `[ni-51-102]` y `[osc-sn-51-721]`. Los resultados reales pueden diferir materialmente de lo descrito.
>
> Supuestos materiales: (1) el ecosistema rust-sel4 y sel4-microkit continúa madurando; (2) el trabajo de Fase 2 del Substrato Soberano para moonshot-database se completa conforme a la hoja de ruta de Active Sovereign Replacements; (3) la demanda del cliente justifica la inversión en desarrollo. Ninguna de estas condiciones está garantizada.

El Sobre B (unikernel seL4) y la capa de persistencia con conciencia de capacidades vía `moonshot-database` son elementos previstos de la trayectoria v1.0.0+ por MEMO §7 Active Sovereign Replacements. El Sobre A de POSIX está previsto que permanezca como alternativa indefinida incluso tras la entrega del Sobre B, por la identidad de bytes entre backends.

## Véase también

- [Documento canónico en inglés](topic-worm-ledger-architecture.md)
- Convención: `~/Foundry/conventions/worm-ledger-design.md`
- Arquitectura de tres anillos: `~/Foundry/conventions/three-ring-architecture.md`
- Doctrina Invención #7: `~/Foundry/DOCTRINE.md` §II.7

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.