---
schema: foundry-doc-v1
title: "service-people — el servicio de libro de identidades"
slug: service-people
category: services
type: concept
content_type: topic
quality: complete
index_group: ring-1-boundary-ingest
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-24
editor: pointsav-engineering
paired_with: service-people.md
short_description: "service-people es la superficie F2 en os-console — un servidor MCP sobre un libro de identidades de solo-anexado y respaldado por WORM, con tres herramientas: anexar, buscar y escanear correos por expresión regular."
cites: []
references: []
---

`service-people` es la superficie F2 en `os-console` y el libro de identidades de la
plataforma. Expone tres herramientas sobre un endpoint MCP — anexar un registro de persona,
buscarlo, y escanear texto libre en busca de direcciones de correo — respaldadas por un
almacén de solo-anexado que nunca sobrescribe una identidad en conflicto. El esquema completo
del registro (el tipo `Person`, su derivación determinista de ID, y el comportamiento de
conflicto del almacén) está documentado en [[identity-ledger-schema-design]]; este artículo
cubre la superficie del servicio y la ruta de extracción automatizada.

## Las tres herramientas MCP

| Herramienta | Qué hace |
|---|---|
| `identity.append` | Escribe un nuevo registro `Person` en el libro |
| `identity.lookup` | Busca un registro por correo o por ID |
| `identity.scan_text` | Escanea un bloque de texto en busca de direcciones de correo y produce un registro por cada dirección encontrada |

Las tres se invocan sobre un único endpoint `POST /mcp`; el servicio también expone
`/healthz` y `/readyz`. No hay una ruta REST separada por operación — el protocolo MCP es
toda la superficie de la API.

## La extracción automatizada es por expresión regular, y hoy es solo-correo

`identity.scan_text` está implementado por un motor interno que el propio código fuente
llama "ACS" — Anchor-Claim-Source, no un modelo de tres entidades con un puente de "Socket
Semántico". Encuentra direcciones de correo con una única expresión regular y, por cada
coincidencia, deriva un ID estable (UUIDv5 de la dirección en minúsculas) y produce un par
ancla-y-reclamo que registra dónde se vio la dirección. Esto es deliberadamente estrecho: no
se extraen números de teléfono, nombres, ni cadenas de organización, y ninguna otra
estrategia de coincidencia — Aho-Corasick u otra — se ejecuta en ninguna parte de esta ruta.
Según su propio comentario de código fuente, el objetivo de diseño es el determinismo:
"ADR-07: cero IA — la extracción es solo por expresión regular."

## Lo que no tiene base en el código actual

Ningún "Chart-of-Accounts" tipo socket, puntuación de gravedad, o mecanismo de expiración
existe en `service-people`. Una identidad extraída no se clasifica, puntúa, ni expira tras
ningún tiempo transcurrido por este crate — se anexa al libro y permanece allí. Cotejar contra
otros servicios para promover o retirar un registro, si ocurre en absoluto, no es código que
contenga este crate.

## El sustrato de archivos planos

Los registros se escriben a través de la ruta de anexado de `service-fs` en lugar de
escribirse directamente en disco, preservando la garantía de escritura-única del libro — un
almacén portable y auditable que no requiere una migración de base de datos cuando el esquema
crece.

## Véase también

- [[identity-ledger-schema-design]] — el esquema completo del registro `Person`, su
  derivación de ID, y el comportamiento de conflicto
- [[service-email]] — una ruta de ingesta que puede alimentar texto a `identity.scan_text`
- [[service-fs]] — el almacén de solo-anexado a través del cual escribe `service-people`
- [[totebox-os]] — la plataforma a la que pertenece el almacenamiento WORM de este libro
