---
schema: foundry-doc-v1
title: "Servicio de mensajería Courier"
slug: message-courier
short_description: "El servicio de mensajería es un motor de automatización web sin interfaz que vincula registros de identidad internos con portales web externos usando adaptadores inyectados en tiempo de ejecución, manteniendo lógica operativa propietaria fuera del monorepo de código abierto."
category: services
type: topic
content_type: topic
quality: stub
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-08
editor: pointsav-engineering
paired_with: message-courier.md
cites: []
---

`service-message-courier` es el motor de automatización web sin cabeza que conecta el [[service-people|libro contable de identidades]] interno de la plataforma con portales web externos — sin incrustar ninguna lógica específica del cliente en la base de código abierta. El motor central lee registros de despacho pendientes del [[worm-ledger-design|libro mayor WORM]], ejecuta interacciones con portales a través de adaptadores en tiempo de ejecución distribuidos de forma privada, y escribe marcas de tiempo de finalización; el motor en sí permanece libre de selectores codificados, credenciales o lógica específica del portal.

## Patrón de adaptadores

El motor central no contiene conocimiento de ningún portal o sitio específico. La lógica operativa — selectores CSS, formas de URL, flujos de autenticación — se inyecta en tiempo de ejecución a través de scripts colocados en `private-adapters/`. Este directorio está explícitamente excluido por `.gitignore`. La separación significa que el monorepo de código abierto permanece agnóstico al inquilino mientras cada instancia de despliegue lleva su propio conjunto de adaptadores privados. Esta arquitectura de inyección en tiempo de ejecución es coherente con el principio de [[sovereign-airlock-doctrine|exclusa soberana]] — la lógica propietaria del cliente nunca cruza hacia el código base abierto.

## Por qué importa la separación

El diseño garantiza que los datos operativos propietarios — selectores de portales de clientes, flujos de autenticación, URL objetivo — nunca entren en el historial de Git público. El motor en sí es revisable y reutilizable; la lógica del portal es privada y específica del despliegue.

## Flujo operativo

El servicio lee los registros de despacho pendientes del [[service-fs-architecture|libro mayor WORM]] interno, ejecuta las interacciones del portal a través de los adaptadores privados en tiempo de ejecución, y escribe las marcas de tiempo de finalización de vuelta sin incrustar ninguna lógica específica del cliente en la base de código de código abierto. Los registros completados son capturados por la [[sovereign-telemetry|telemetría de estado cero]] con fines de auditoría.

## Véase también

- [[ontological-governance|Gobernanza ontológica]] — el marco de gobernanza que rige los permisos de adaptadores
- [[verification-surveyor|Supervisor de verificación]] — el servicio que monitorea los volúmenes diarios de despacho
- [[sovereign-telemetry|Arquitectura de telemetría de estado cero]] — la capa de telemetría que consume eventos de registro
- [[service-people]] — el libro mayor de identidades que el servicio courier vincula con portales externos
