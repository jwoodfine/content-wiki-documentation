---
schema: foundry-doc-v1
title: "Servicio de mensajería Courier"
slug: message-courier
short_description: "Un motor deliberadamente delgado que carga dinámicamente el script adaptador privado de un cliente y le entrega el control de ejecución — manteniendo cada detalle operativo de la lógica de automatización web de un cliente completamente fuera del código abierto."
category: services
type: topic
content_type: topic
quality: stub
index_group: specialist-and-domain-services
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: message-courier.md
cites: []
---

`service-message-courier` es deliberadamente pequeño. Su única función es cargar un fragmento de código que el motor mismo nunca ha visto — un adaptador privado — y entregarle el control. Todo lo que una tarea específica de automatización web realmente hace vive en ese adaptador, no en el motor.

## Qué hace el motor

El punto de entrada de línea de comandos recibe dos argumentos: qué adaptador ejecutar y un límite operativo (10 por defecto) para acotar cuánto trabajo realiza un ciclo de ejecución. Luego:

1. Importa dinámicamente el adaptador nombrado desde `private-adapters/<nombre>.py`.
2. Llama a la función `execute_payload(limit=...)` del adaptador.
3. Reporta éxito o fallo — si el adaptador lanza una excepción propia, se captura y se registra.

Eso es todo el motor. No tiene conocimiento incorporado de ningún libro mayor, portal o biblioteca de automatización de navegador — esas son decisiones que toma el adaptador, completamente fuera de este código.

## Por qué el adaptador vive fuera del control de versiones

`private-adapters/` está excluido de Git por el propio `.gitignore` del repositorio, junto con las credenciales locales y cualquier base de datos local de seguimiento de ejecución. La lógica operativa de un cliente — a qué portal acceder, qué hacer allí y cómo autenticarse — nunca entra al historial del monorepo público. El motor falla de forma explícita y termina si el archivo del adaptador solicitado no está presente, en lugar de no hacer nada silenciosamente.

Esto mantiene al motor de código abierto genuinamente agnóstico del inquilino: el mismo script de 56 líneas se ejecuta sin modificación para cualquier implementación, y todo lo específico de la operación de un cliente es un archivo externo que el motor carga en tiempo de ejecución, nunca una bifurcación del motor mismo.

## Véase también

- [[service-people]] — una fuente plausible de registros sobre los que un adaptador podría actuar, aunque el motor mismo no tiene conexión directa con él
