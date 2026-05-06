---
schema: foundry-doc-v1
title: "Servicio de Mensajería Courier"
slug: message-courier
category: services
type: topic
quality: stub
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: message-courier.md
cites: []
## Véase también

- [[ontological-governance]]
- [[verification-surveyor]]
- [[sovereign-telemetry]]

---

`service-message-courier` es un componente de automatización web sin cabeza y mensajería diseñado para conectar `service-people`, el libro contable de identidades interno, con portales web externos. El servicio opera como un motor de ejecución genérico: toda la lógica específica del portal se suministra en tiempo de ejecución a través del patrón de adaptadores.

## Patrón de adaptadores

El motor central no contiene conocimiento de ningún portal o sitio específico. La lógica operativa — selectores CSS, formas de URL, flujos de autenticación — se inyecta en tiempo de ejecución a través de scripts colocados en `private-adapters/`. Este directorio está explícitamente excluido por `.gitignore`. La separación significa que el monorepo de código abierto permanece agnóstico al inquilino mientras cada instancia de despliegue lleva su propio conjunto de adaptadores privados.

## Por qué importa la separación

El diseño garantiza que los datos operativos propietarios — selectores de portales de clientes, flujos de autenticación, URL objetivo — nunca entren en el historial de Git público. El motor en sí es revisable y reutilizable; la lógica del portal es privada y específica del despliegue.

## Flujo operativo

El servicio lee los registros de despacho pendientes del libro contable interno, ejecuta las interacciones del portal a través de los adaptadores privados en tiempo de ejecución, y escribe las marcas de tiempo de finalización de vuelta sin incrustar ninguna lógica específica del cliente en la base de código de código abierto.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
