---
schema: foundry-doc-v1
title: "Enrutamiento de IA y la esclusa lingüística"
slug: sovereign-ai-routing
short_description: "El enrutamiento de IA en la plataforma PointSav procesa solicitudes de modelo de lenguaje a través de un paso de sanitización local antes de que cualquier dato llegue a modelos externos, asegurando que los datos estructurados internos nunca viajen a servidores de terceros en forma identificable."
category: architecture
type: topic
content_type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: sovereign-ai-routing.md
cites: []
---


El enrutamiento de IA en la plataforma [[pointsav-overview|PointSav]] procesa las solicitudes de modelos de lenguaje a través de una etapa de sanitización local antes de que cualquier dato llegue a modelos externos. Esto garantiza que los datos estructurados internos nunca viajen a servidores de terceros en forma identificable. Véase [[single-boundary-compute-discipline|la disciplina de cómputo de frontera única]].

## El problema estructural

Los modelos de lenguaje comerciales operan como servicios externos. Cuando un operador envía documentos internos o registros del libro contable a un proveedor de IA centralizado, esos datos entran en servidores de terceros. Para sectores regulados — inmobiliario, asesoramiento financiero, clínicas pequeñas, despachos jurídicos — esto crea un problema de cumplimiento que no puede resolverse solo con acuerdos contractuales, porque los datos han salido físicamente de la infraestructura del cliente.

## La esclusa lingüística

[[service-slm|`service-slm`]] actúa como la única frontera que posee claves de API, registra cada llamada externa al libro contable de auditoría por inquilino, y aplica la disciplina de sanitizar-salida / rehidratar-entrada en cada solicitud.

El flujo es el siguiente:
1. El operador envía la solicitud al [[doorman-protocol|Doorman]] ([[service-slm|`service-slm`]]).
2. El Modelo de Lenguaje Pequeño local ejecuta la pasada de sanitización: identifica patrones de PII, elimina coordenadas físicas, reemplaza referencias identificables con tokens seudónimos, y registra el mapeo token-original en una tabla de rehidratación en memoria local.
3. El prompt sanitizado se enruta al exterior hacia el modelo externo.
4. El [[doorman-protocol|Doorman]] aplica la pasada de rehidratación antes de devolver la respuesta al solicitante.

El modelo externo nunca posee los registros estructurados reales del libro contable del cliente.

## Véase también

- [[compounding-substrate]]
- [[worm-ledger-architecture]]
- [[decode-time-constraints]]
- [[machine-based-auth]]
- [[3-layer-stack]]
