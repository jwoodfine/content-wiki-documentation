---
schema: foundry-doc-v1
title: "Topología de Capacidades seL4"
slug: sel4-capability-topology
category: architecture
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-06-29
editor: pointsav-engineering
paired_with: sel4-capability-topology.md
short_description: "En un sistema seL4, la seguridad está determinada por la forma del grafo de capacidades — la topología. Si el componente A no tiene un camino de capacidades hacia B, A no puede alcanzar B por ningún medio; propiedad demostrada mediante verificación formal con asistencia mecánica."
cites: []
references:
  - id: 1
    text: "Shapiro, J. S. y Miller, M. S. 'EROS: A Capability System.' USENIX Annual Technical Conference, 1999."
  - id: 2
    text: "Murray, T. et al. 'seL4: From General Purpose to a Proof of Information Flow Enforcement.' IEEE Symposium on Security and Privacy, 2013."
  - id: 3
    text: "Drossopoulou, S. et al. 'Holistic Specifications for Robust Programs.' ECOOP, 2016."
---

En el micronúcleo seL4, todo acceso a un objeto está mediado por una **capacidad** — un token infalsificable que otorga un derecho específico sobre un objeto específico. Un proceso que no posee una capacidad sobre un objeto no puede observarlo, modificarlo ni invocarlo. No existe autoridad ambiental. No existe privilegio de raíz a nivel del núcleo.

Las capacidades se almacenan en **CSpaces** — tablas de espacio de capacidades por proceso, gestionadas por el núcleo seL4. El CSpace es un grafo dirigido acotado: los punteros de capacidades son aristas; los objetos del núcleo (hilos, regiones de memoria, puntos de comunicación entre procesos, objetos de notificación) son nodos.

## El invariante topológico

La colección de todos los CSpaces en un sistema seL4 en ejecución forma un grafo dirigido denominado **topología de capacidades**. El núcleo seL4 impone un invariante fundamental:

> *Solo la conectividad engendra conectividad.*
> — Shapiro y Miller, 1999 [^1]

En términos formales: si el componente A no tiene capacidad de alcanzar al componente B — directa o transitivamente a través de cualquier cadena de capacidades intermedias — entonces A no puede obtener información de B, no puede modificar el estado de B y no puede hacer que B ejecute ninguna acción.

Este invariante está verificado con asistencia mecánica. La Fundación seL4 ha publicado pruebas formales en el asistente de demostración Isabelle/HOL que cubren:

1. **Corrección funcional** (a nivel C, todas las arquitecturas): la implementación del núcleo corresponde a su especificación abstracta.
2. **Integridad** (AArch64 EL2, abril de 2025): ningún proceso puede modificar objetos del núcleo ni las capacidades de otro proceso sin poseer un derecho de concesión sobre la capacidad correspondiente.
3. **Confidencialidad** (RISC-V64, publicada; AArch64 en curso): ningún proceso puede leer los datos de otro proceso sin poseer un derecho de lectura. [^2]

## Lo que significa "la topología determina la seguridad"

La seguridad en un sistema seL4 no está determinada por políticas, listas de control de acceso ni comprobaciones de software. Está determinada por la forma del grafo de capacidades — la topología.

Un arquitecto que dibuja la topología de capacidades de un sistema ha dibujado su perímetro de seguridad. Dos componentes que no comparten ningún camino en el grafo de capacidades no tienen canal de información entre ellos, independientemente del software que se ejecute en su interior. Un componente comprometido no puede escapar de su partición porque hacerlo requeriría obtener una capacidad que no posee — y el núcleo demuestra que la creación de capacidades es monótona: un proceso no puede crear una capacidad que no posea ya.

## Cobertura arquitectónica por objetivo seL4

| Arquitectura | Afirmación de seguridad formal | Notas |
|---|---|---|
| AArch64 EL2 | Corrección funcional + integridad | Prueba de integridad publicada en abril de 2025 |
| RISC-V64 | Corrección funcional + integridad + confidencialidad | Pruebas más completas; hardware HiFive Unleashed |
| x86-64 | Solo corrección funcional | Sin prueba de integridad ni confidencialidad |

La afirmación formal de que "la topología determina la seguridad" se aplica a los despliegues en AArch64 EL2 y RISC-V64. Los despliegues en x86-64 solo cuentan con pruebas de corrección funcional; la afirmación de seguridad topológica no se extiende a esa arquitectura.

## Antecedentes industriales — topología de componentes de Fuchsia

El sistema operativo Fuchsia de Google utiliza el mismo modelo de capacidades y la misma terminología. La documentación de Fuchsia se refiere a la "topología de componentes" para describir el árbol de relaciones de capacidades entre componentes que determina qué llamadas al sistema e interfaces son accesibles. La misma terminología aparece en tratamientos formales de seguridad basada en capacidades mediante estructuras de grafo dirigido [^3], con raíces en la literatura temprana de sistemas operativos basados en capacidades [^1].

## Aplicación en PPN

La Red Privada PointSav tiene previsto/la intención de utilizar seL4 como capa de hipervisor en nodos AArch64. En esa configuración, la topología de capacidades seL4 gobierna qué componentes pueden comunicarse a través de la malla. La interfaz de malla WireGuard, el servidor de ceremonia de emparejamiento y el servicio de gestión de flota ocupan cada uno dominios de protección seL4 distintos con canales de capacidades concedidos explícitamente. Un componente sin capacidad de acceder al dominio de protección WireGuard no puede modificar las tablas de pares — independientemente de si está comprometido.

Esta es la base formal del modelo de seguridad PPN en la capa del hipervisor.

## Véase también

- [[ppn-three-path-architecture]] — las tres opciones de arquitectura seL4 secuenciales para nodos de infraestructura PPN
- [[sel4-microkernel-substrate]] — el micronúcleo seL4 como sustrato de infraestructura
- [[capability-based-security]] — el modelo de seguridad basado en capacidades aplicado en la pila PointSav
- [[ppn-architecture-overview]] — cómo seL4 encaja en la pila PPN de cuatro capas
