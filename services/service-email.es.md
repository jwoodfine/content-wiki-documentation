---
schema: foundry-doc-v1
title: "service-email — Puente de Transporte de Correo"
slug: service-email
category: services
type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-08
editor: pointsav-engineering
paired_with: service-email.md
cites: []
---

El correo electrónico entrante llega a la plataforma PointSav en un único punto auditable — **service-email** se autentica contra el buzón de Microsoft 365 a través de la API de Microsoft Graph, recupera los mensajes entrantes y escribe las cargas útiles en bruto en una cola local sin interpretar el contenido. Los servicios del Anillo 2 se encargan de todo lo que sigue. El servicio no mantiene ningún conocimiento del contenido del mensaje: su único trabajo es la extracción autenticada y confiable a través del límite de la nube.

## Línea de base arquitectónica

El servicio aborda una limitación estructural de IMAP y SMTP: ambos protocolos requieren mantener una conexión persistente y exponen la gestión del estado de mensajes a través de mecanismos heredados. `service-email` utiliza autenticación OAuth2 contra la API de Microsoft Graph, lo que convierte cada ciclo de sondeo en un intercambio HTTP discreto y autenticado. Este enfoque confina el límite de confianza en la nube a un único punto bien definido en el pipeline.

## Anillo y función

`service-email` ocupa el **Anillo 1 — Ingestión Perimetral** en la arquitectura de tres anillos. Los servicios del Anillo 1 son por inquilino e implementan una interfaz de servidor MCP. No hay ningún servicio del Anillo 1 que procese contenido semánticamente — ese es el ámbito del Anillo 2.

## Flujo de extracción

1. **Autenticación.** Un handshake OAuth2 contra la API de Microsoft Graph produce un token de portador.
2. **Extracción.** El servicio sondea mensajes no leídos y recupera la carga útil JSON OData en bruto para cada mensaje encontrado.
3. **Escritura y marcado.** La carga útil se escribe en la cola temporal local. El servicio emite una solicitud `PATCH` autorizada para marcar cada mensaje extraído como leído en el servidor remoto, evitando la re-extracción en el siguiente ciclo de sondeo.

## Véase también

- [[service-extraction]]
- [[service-people]]
- [[service-slm]]
- [[trajectory-substrate]]
