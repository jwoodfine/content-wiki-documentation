---
schema: foundry-doc-v1
title: "Seguridad basada en capacidades"
slug: capability-based-security
short_description: "La seguridad basada en capacidades es el modelo de control de acceso que PointSav utiliza en las capas de hardware y sistema operativo, donde cada componente de software debe mantener un token criptográfico verificado matemáticamente para comunicarse con cualquier otro componente."
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
paired_with: capability-based-security.md
cites: []
references:
  - id: 1
    text: "Klein, G. et al. 'seL4: Formal Verification of an OS Kernel.' ACM SOSP, 2009."
    url: "https://dl.acm.org/doi/10.1145/1629575.1629596"
  - id: 2
    text: "Lampson, B. W. 'Protection.' ACM SIGOPS Operating Systems Review, 8(1):18–24, 1974."
    url: "https://dl.acm.org/doi/10.1145/775265.775268"
---


La seguridad basada en capacidades es el modelo de control de acceso utilizado en las capas de hardware y sistema operativo de la plataforma [[pointsav-overview|PointSav]]. A diferencia de los sistemas operativos convencionales, que otorgan amplios permisos a través de cuentas administrativas, la seguridad basada en capacidades exige que cada componente de software aislado posea un [[crypto-attestation|token criptográfico]] verificado matemáticamente — denominado capacidad — antes de poder comunicarse con cualquier otro componente. Véase también [[capability-ledger-substrate|el sustrato del registro de capacidades]] y [[pairing-as-permission|emparejamiento como permiso]].

## Cómo funciona

Una capacidad no puede falsificarse ni copiarse. [^2] La concede el kernel al inicio del proceso y se revoca cuando se retira el privilegio. Esto hace que el radio de explosión de cualquier compromiso esté matemáticamente acotado a los componentes para los que el proceso comprometido poseía capacidades.

## Por qué importa

Los sistemas operativos estándar son vulnerables a la escalada de privilegios. Un único componente comprometido puede, en muchas arquitecturas, alcanzar la memoria central de la máquina anfitriona y acceder a otros componentes de la red. El modelo de capacidades elimina esta clase de vulnerabilidad a nivel de arquitectura.

## Propiedades clave

- **Verificación formal.** El [[sel4-microkernel-substrate|microkernel seL4]] subyacente está verificado formalmente en Isabelle/HOL [^1]: las propiedades de aislamiento son matemáticamente probadas, no afirmadas.
- **Mínimo privilegio por defecto.** Los componentes comienzan sin capacidades; el sistema concede el conjunto mínimo requerido para su función declarada.
- **Contención del radio de explosión.** El compromiso de un componente no puede propagarse a componentes para los que no posee concesiones de capacidad.
- **Auditabilidad.** Las concesiones de capacidades se registran; el conjunto de concesiones en vigor en cualquier momento es inspeccionable.

## Véase también

- [[sel4-microkernel-substrate]]
- [[worm-ledger-architecture]]
- [[3-layer-stack]]
- [[machine-based-auth]]
- [[compounding-substrate]]
