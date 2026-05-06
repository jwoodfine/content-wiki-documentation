---
schema: foundry-doc-v1
title: "Seguridad Basada en Capacidades"
slug: capability-based-security
category: architecture
type: topic
quality: core
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: capability-based-security.md
cites: []
---

La seguridad basada en capacidades es el modelo de control de acceso utilizado en las capas de hardware y sistema operativo de la plataforma PointSav. A diferencia de los sistemas operativos convencionales, que otorgan amplios permisos a través de cuentas administrativas, la seguridad basada en capacidades exige que cada componente de software aislado posea un token criptográfico verificado matemáticamente — denominado capacidad — antes de poder comunicarse con cualquier otro componente.

## Cómo funciona

Una capacidad no puede falsificarse ni copiarse. La concede el kernel al inicio del proceso y se revoca cuando se retira el privilegio. Esto hace que el radio de explosión de cualquier compromiso esté matemáticamente acotado a los componentes para los que el proceso comprometido poseía capacidades.

## Por qué importa

Los sistemas operativos estándar son vulnerables a la escalada de privilegios. Un único componente comprometido puede, en muchas arquitecturas, alcanzar la memoria central de la máquina anfitriona y acceder a otros componentes de la red. El modelo de capacidades elimina esta clase de vulnerabilidad a nivel de arquitectura.

## Propiedades clave

- **Verificación formal.** El microkernel seL4 subyacente está verificado formalmente en Isabelle/HOL: las propiedades de aislamiento son matemáticamente probadas, no afirmadas.
- **Mínimo privilegio por defecto.** Los componentes comienzan sin capacidades; el sistema concede el conjunto mínimo requerido para su función declarada.
- **Contención del radio de explosión.** El compromiso de un componente no puede propagarse a componentes para los que no posee concesiones de capacidad.
- **Auditabilidad.** Las concesiones de capacidades se registran; el conjunto de concesiones en vigor en cualquier momento es inspeccionable.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
