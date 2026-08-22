---
schema: foundry-doc-v1
title: "Ingesta de correo"
slug: service-email
category: services
type: concept
content_type: topic
quality: complete
index_group: ring-1-boundary-ingest
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: service-email.md
short_description: "service-email extrae correo de un buzón de Microsoft Exchange vía EWS, escribe el mensaje en bruto en almacenamiento local y lo elimina del buzón de origen inmediatamente después de extraerlo — el buzón en la nube es un punto de tránsito, no una copia de registro."
cites: []
references:
  - id: 1
    text: "Hardt, D. (Ed.). 'El Marco de Autorización OAuth 2.0.' IETF RFC 6749, 2012."
    url: "https://www.rfc-editor.org/rfc/rfc6749"
---

`service-email` extrae correo de un buzón de Microsoft Exchange y lo lleva a almacenamiento local. Se autentica con OAuth2 de credenciales de cliente, se conecta a Exchange Web Services (EWS) — la API SOAP de Exchange, no la más reciente API de Microsoft Graph — y, para cada mensaje que encuentra, extrae el contenido MIME en bruto, lo escribe como un archivo local y emite una eliminación definitiva contra el buzón de origen. No interpreta, clasifica ni enruta contenido; eso ocurre más adelante en `service-content` y `service-extraction`.

## El ciclo de extracción

Para cada carpeta que sondea, el servicio:

1. Se autentica ante Exchange usando un token OAuth2 de credenciales de cliente, con el alcance predeterminado propio de Exchange, no un permiso específico de Graph.
2. Lista los ID de mensajes en la carpeta mediante llamadas SOAP de EWS.
3. Obtiene el contenido MIME en bruto de cada mensaje, decodificado en base64 desde la respuesta SOAP, y lo escribe en un archivo local.
4. Emite una solicitud de eliminación definitiva de EWS para ese mensaje contra el buzón de origen.

Este es un flujo de extraer-y-eliminar, no una política de retención suave — un mensaje se elimina del buzón de origen tan pronto como su contenido se ha escrito localmente, no después de que transcurra un tiempo.

## Por qué el buzón en la nube no es la copia de registro

Como la extracción y la eliminación ocurren juntas, el buzón de Exchange nunca acumula un archivo duradero propio — el archivo local escrito en el momento de la extracción es la única copia que persiste. Esto limita lo que el proveedor en la nube llega a retener a los mensajes que esperan extracción, no a un registro histórico completo.

## Lo que service-email no es

`service-email` es el límite de ingesta, no el cliente de correo. No renderiza HTML para que un operador lo lea, no sintetiza contenido y no clasifica ni enruta mensajes — entrega el archivo local en bruto a los servicios posteriores y se detiene. La [[three-ring-architecture|arquitectura de tres anillos]] posiciona a `service-email` en el Anillo 1, el perímetro de confianza donde las cargas útiles entran por primera vez a la plataforma.

## Véase también

- [[service-egress]] — lleva el correo escrito localmente hacia adelante para transferencia saliente, usando su propio mecanismo de liberación separado
- [[service-content]] — consume los archivos locales en bruto que produce este servicio
- [[app-console-input]] — la Máquina de Ingesta F12; superficie de ingesta complementaria para cargas útiles que no son de correo
