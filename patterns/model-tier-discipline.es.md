---
schema: foundry-doc-v1
title: "Disciplina de niveles de modelo"
slug: model-tier-discipline
category: patterns
type: topic
content_type: topic
quality: complete
index_group: collaboration-and-editorial-workflow
short_description: "El Doorman enruta cada solicitud de inferencia a uno de tres niveles de cómputo — local, ráfaga en GPU, o API externa — según una indicación de complejidad y el estado presupuestario en vivo, no una elección directa del solicitante."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-22
editor: pointsav-engineering
cites: []
paired_with: model-tier-discipline.md
---

Una plataforma que enruta cada solicitud de inferencia por la misma ruta de cómputo fija gasta significativamente más de lo necesario, o falla solicitudes que una ruta más económica podría haber atendido. La disciplina de niveles de modelo es el mecanismo de enrutamiento del [[doorman-protocol|servicio Doorman]]. Cada solicitud de inferencia lleva una indicación de complejidad, y es el Doorman — no el solicitante — quien decide cuál de los tres niveles la atiende, según esa indicación más los límites presupuestarios y el estado de las instancias activas.

## Tres niveles, un enrutador

**Local** — inferencia en el mismo host, actualmente un modelo OLMo 3 de 7B cuantizado servido por HTTP en la misma máquina que el Doorman. Sin salida de red, sin costo por solicitud más allá del consumo eléctrico de la máquina.

**Yoyo** — cómputo en ráfaga sobre una instancia de GPU multi-nube prescindible, actualmente un modelo OLMo 3 más grande ajustado para razonamiento profundo. Se usa cuando la complejidad de una solicitud supera lo que el nivel local puede atender bien, a costa de la latencia de arranque de la instancia en ráfaga.

**External** — una API externa (Anthropic, Google u OpenAI), reservada para tareas estrechas y críticas de precisión, restringida por una lista de permitidos explícita en lugar de abrirse a solicitudes arbitrarias. **Una solicitud solo llega a una API externa cuando la tarea genuinamente lo requiere** — toda solicitud por defecto permanece en infraestructura controlada por el operador.

## El solicitante indica; el Doorman decide

Un solicitante no elige el nivel directamente. Envía una indicación de complejidad — baja, media o alta — y el Doorman la traduce a un nivel concreto usando sus propios límites presupuestarios y el estado actual de las instancias. La misma indicación de "complejidad alta" podría enrutar a Yoyo cuando ya hay una instancia activa, o permanecer en Local bajo condiciones de presupuesto ajustadas.

Esta indirección es lo que hace la disciplina exigible en lugar de aspiracional. Si cada solicitante eligiera su propio nivel, la disciplina de costos dependería de que cada uno eligiera consistentemente el nivel más económico que funcionara — el mismo problema que tiene una plataforma sin ninguna guía de nivel. Enrutar a través del Doorman convierte el punto de cumplimiento en un solo lugar del código, no en el criterio de cada solicitante.

## Por qué esto importa para el costo

Ejecutar el trabajo en el nivel que realmente puede atenderlo — en lugar de enviar cada solicitud por defecto al nivel más capaz disponible — produce un multiplicador de costo efectivo considerable con un presupuesto de cómputo fijo. Las solicitudes simples y bien especificadas que un modelo local atiende correctamente nunca tocan los niveles de ráfaga o externos, más costosos. El ahorro se acumula: una plataforma que opera con esta disciplina sostiene un volumen de solicitudes sustancialmente mayor dentro del mismo costo de infraestructura.

## Véase también

- [[service-slm-operationalization-plan]] — la arquitectura de enrutamiento de cómputo que implementa el Doorman
- [[doorman-protocol]] — el servicio Doorman que realiza este enrutamiento en la puerta de enlace de inferencia
- [[zero-container-runtime]] — la disciplina de despliegue que el propio Doorman sigue como binario gestionado por systemd

## Procedencia

Versión en español elaborada por project-language, adaptación estratégica — no es una traducción literal del artículo canónico en inglés.
