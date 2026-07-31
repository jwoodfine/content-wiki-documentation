---
schema: foundry-doc-v1
title: "Enrutamiento de IA y la esclusa lingüística"
slug: sovereign-ai-routing
short_description: "El enrutamiento de IA en la plataforma PointSav procesa solicitudes de modelo de lenguaje a través de un paso de sanitización local antes de que cualquier dato llegue a modelos externos, asegurando que los datos estructurados internos nunca viajen a servidores de terceros en forma identificable."
category: ai
type: topic
content_type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-07-31
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

## Arquitectura

[[service-slm|`service-slm`]] es la única frontera del [[doorman-protocol|Doorman]] a través de los tres niveles de cómputo:

- **Nivel A — Local:** OLMo 3 7B Q4 en la máquina del cliente (CPU). Ningún dato sale del hardware del cliente.
- **Nivel B — [[yoyo-compute-substrate|ráfaga Yo-Yo]]:** OLMo 3.1 32B Think en ráfaga de GPU multi-nube (GCP Cloud Run / RunPod / Modal / GPU del cliente). Solo el prompt sanitizado.
- **Nivel C — API externa:** Anthropic Claude / Google Gemini / OpenAI para tareas de precisión acotada. Solo el prompt sanitizado; las claves de API las conserva exclusivamente el Doorman.

El cliente no selecciona el nivel. La forma de la solicitud, la longitud del prompt y los límites de presupuesto configurados del inquilino determinan el enrutamiento. La decisión de enrutamiento del Doorman se registra en el libro contable de auditoría junto con el registro de la solicitud.

## Aplicaciones

- **Flujo editorial:** los borradores TOPIC y GUIDE enrutados a través de modelos externos llevan solo el prompt editorial sanitizado; los mapas de terminología específicos del cliente se aplican localmente.
- **Firmas de asesoría financiera:** los resúmenes del libro contable enrutados para análisis eliminan números de cuenta, nombres de clientes e identificadores de jurisdicción antes de salir de la red de la oficina.
- **Operaciones inmobiliarias:** los registros de propiedades enrutados para generación de descripciones reemplazan direcciones y nombres de propietarios con tokens seudónimos para la llamada externa.

## Véase también

- [[compounding-substrate]]
- [[worm-ledger-architecture]]
- [[decode-time-constraints]]
- [[machine-based-auth]]
- [[3-layer-stack]]
