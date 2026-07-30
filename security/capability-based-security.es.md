---
schema: foundry-doc-v1
title: "Seguridad basada en capacidades"
slug: capability-based-security
short_description: "La seguridad basada en capacidades es el modelo de control de acceso que PointSav utiliza en las capas de hardware y sistema operativo, donde cada componente de software debe mantener un token criptográfico verificado matemáticamente para comunicarse con cualquier otro componente."
category: security
type: topic
content_type: topic
quality: complete
status: active
audience: public
bcsc_class: forward-looking
language_protocol: PROSE-TOPIC
last_edited: 2026-07-30
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

**Corrección — reformulada como planificada/prevista (2026-07-30):** este artículo
describía originalmente un sistema de capacidades en vivo. No existe tal código hoy,
confirmado tanto en una revisión de un solo archivo como en una búsqueda posterior más
amplia en ~25 archivos. El cuerpo a continuación se reformula para presentarlo como
arquitectura planificada/prevista, no como estado actual.

La seguridad basada en capacidades es el modelo de control de acceso que PointSav prevé utilizar en las capas de hardware y sistema operativo, una vez implementado. A diferencia de los sistemas operativos convencionales, que otorgan amplios permisos a través de cuentas administrativas, el diseño exige que cada componente de software aislado posea un [[crypto-attestation|token criptográfico]] verificado matemáticamente — denominado capacidad — antes de poder comunicarse con cualquier otro componente. Esta es una arquitectura planificada, aún no implementada. Véase también [[capability-ledger-substrate|el sustrato del registro de capacidades]] y [[pairing-as-permission|emparejamiento como permiso]].

## Cómo se prevé que funcione

Una capacidad, una vez implementada, no podría falsificarse ni copiarse. [^2] Sería concedida por el kernel al inicio del proceso y revocada al retirar el privilegio. El efecto previsto es que el radio de explosión de cualquier compromiso quedaría matemáticamente acotado a los componentes para los que el proceso comprometido poseía capacidades.

## Por qué importaría

Los sistemas operativos estándar son vulnerables a la escalada de privilegios. El modelo de capacidades está diseñado para eliminar esta clase de vulnerabilidad a nivel de arquitectura. **A la fecha de esta revisión, no existe tal implementación** — no se encontró código de gestor de capacidades, envoltorio de aislamiento, ni puente de hipervisor en ningún archivo del monorepo, y seL4 mismo aún no se ejecuta en ningún componente enviado.

## Propiedades previstas

- **Verificación formal.** El [[sel4-microkernel-substrate|microkernel seL4]] que subyacería al gestor de capacidades está verificado formalmente en Isabelle/HOL [^1] como kernel en sí mismo — es decir, las propiedades de aislamiento *del propio seL4* están matemáticamente probadas, independientemente de si la capa de gestión de capacidades propia de PointSav ha sido construida sobre él.
- **Mínimo privilegio por defecto (previsto).** Los componentes comenzarían sin capacidades; el sistema concedería solo el conjunto mínimo requerido.
- **Contención del radio de explosión (prevista).** El compromiso de un componente no podría propagarse a componentes para los que no posee concesiones.
- **Auditabilidad (prevista).** Las concesiones de capacidades quedarían registradas.

## Véase también

- [[sel4-microkernel-substrate]]
- [[worm-ledger-architecture]]
- [[3-layer-stack]]
- [[machine-based-auth]]
- [[compounding-substrate]]
