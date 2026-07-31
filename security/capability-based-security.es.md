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
last_edited: 2026-07-31
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

## Arquitectura (planificada)

La capa de capacidades prevista se ubicaría entre el [[sel4-microkernel-substrate|microkernel seL4]] y los procesos de servicio en Rust que componen los servicios del [[three-ring-architecture|Anillo 1 y Anillo 2]] de PointSav, con gestores de capacidades basados en Rust encargados de construir los envoltorios de aislamiento y los puentes de hipervisor que median la comunicación entre componentes.

El diseño exige un flujo de comandos estricto y unidireccional entre dominios de aislamiento: un proceso aislado de entrega en el borde — por ejemplo, [[mediakit-os|MediaKit OS]] — no podría emitir comandos de vuelta hacia la bóveda segura de [[totebox-os|ToteboxOS]], de modo que un proceso de borde comprometido quedaría contenido dentro de su propia zona de memoria aislada, sin que ninguna concesión de capacidad alcance el resto del sistema — impuesto por el kernel, no por un documento de política.

## Aplicaciones previstas

Una vez construido, el modelo de capacidades está previsto para aplicarse en toda la pila de despliegue de [[pointsav-overview|PointSav]]:

- **[[totebox-os|ToteboxOS]]** — el sistema operativo de bóveda segura principal; los datos en reposo solo serían accesibles para los procesos que posean el token de capacidad correspondiente.
- **[[mediakit-os|MediaKit OS]]** — el entorno de entrega en el borde; previsto para no poseer ninguna concesión de capacidad que alcance ToteboxOS, de modo que un nodo de entrega comprometido no pudiera acceder a los datos almacenados.
- **[[service-fs-architecture|service-fs]]** — el [[worm-ledger-architecture|libro contable WORM]]; la capacidad de anexado se concedería únicamente a los servicios de ingesta del [[three-ring-architecture|Anillo 1]].

## Véase también

- [[sel4-microkernel-substrate]]
- [[worm-ledger-architecture]]
- [[3-layer-stack]]
- [[machine-based-auth]]
- [[compounding-substrate]]
