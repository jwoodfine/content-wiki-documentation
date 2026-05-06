---
schema: foundry-doc-v1
title: "Fundación seL4"
slug: sel4-foundation
category: architecture
type: topic
quality: stub
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: sel4-foundation.md
cites: []
---

La fundación seL4 es el microkernel verificado formalmente que actúa como raíz de confianza en la capa del sistema operativo de PointSav. Proporciona aislamiento matemáticamente probado entre todos los recursos de hardware y los componentes de software.

## Qué es seL4

seL4 es un microkernel basado en C verificado formalmente en Isabelle/HOL. Sus propiedades de aislamiento están matemáticamente probadas para la configuración de hardware verificada — no afirmadas por política. Actúa como la raíz de confianza absoluta: cada recurso de hardware — tiempo de CPU, memoria física, interfaces de red, almacenamiento — es asignado y aislado a través del kernel seL4.

## Diseño minimalista deliberado

El diseño del microkernel es deliberadamente mínimo. seL4 maneja solo las operaciones más primitivas: enrutar la memoria física a espacios de direcciones aislados y programar el tiempo de CPU. Todos los controladores, interfaces de red y servicios de aplicaciones se ejecutan fuera del kernel en procesos protegidos en espacio de usuario.

Esto significa que la base de código del kernel verificado formalmente es lo suficientemente pequeña como para verificarse de forma exhaustiva — toda la garantía de aislamiento está probada, no aproximada.

## Postura flexible de hardware

Cuando la plataforma PointSav opera en hardware donde seL4 puede arrancar de forma nativa, el límite de aislamiento es aplicado por el kernel y verificado formalmente. Cuando el hardware no admite el arranque nativo de seL4, una VM invitada de Linux o BSD alojada dentro de un hipervisor basado en seL4 proporciona un aislamiento estructural equivalente alrededor del invitado.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
