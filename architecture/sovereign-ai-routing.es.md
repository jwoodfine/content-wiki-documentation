---
schema: foundry-doc-v1
title: "Enrutamiento de IA y la Esclusa Lingüística"
slug: sovereign-ai-routing
category: architecture
type: topic
quality: core
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: sovereign-ai-routing.md
cites: []
---

El enrutamiento de IA en la plataforma PointSav procesa las solicitudes de modelos de lenguaje a través de una etapa de sanitización local antes de que cualquier dato llegue a modelos externos. Esto garantiza que los datos estructurados internos nunca viajen a servidores de terceros en forma identificable.

## El problema estructural

Los modelos de lenguaje comerciales operan como servicios externos. Cuando un operador envía documentos internos o registros del libro contable a un proveedor de IA centralizado, esos datos entran en servidores de terceros. Para sectores regulados — inmobiliario, asesoramiento financiero, clínicas pequeñas, despachos jurídicos — esto crea un problema de cumplimiento que no puede resolverse solo con acuerdos contractuales, porque los datos han salido físicamente de la infraestructura del cliente.

## La esclusa lingüística

`service-slm` actúa como la única frontera que posee claves de API, registra cada llamada externa al libro contable de auditoría por inquilino, y aplica la disciplina de sanitizar-salida / rehidratar-entrada en cada solicitud.

El flujo es el siguiente:
1. El operador envía la solicitud al Doorman (`service-slm`).
2. El Modelo de Lenguaje Pequeño local ejecuta la pasada de sanitización: identifica patrones de PII, elimina coordenadas físicas, reemplaza referencias identificables con tokens seudónimos, y registra el mapeo token-original en una tabla de rehidratación en memoria local.
3. El prompt sanitizado se enruta al exterior hacia el modelo externo.
4. El Doorman aplica la pasada de rehidratación antes de devolver la respuesta al solicitante.

El modelo externo nunca posee los registros estructurados reales del libro contable del cliente.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
