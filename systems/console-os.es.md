---
schema: foundry-doc-v1
title: "os-console — El libro mayor de comandos"
slug: console-os
category: systems
type: concept
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-07-18
editor: pointsav-engineering
paired_with: console-os.md
short_description: "os-console es la superficie de cara al operador de la plataforma PointSav — un Libro Mayor de Comandos que se conecta a un Totebox y le presenta su estado al operador a través de una interfaz estructurada por teclas de función."
cites: []
references:
  - id: 1
    text: "Green, C. 'Improved Alpha-Tested Magnification for Vector Textures and Special Effects.' ACM SIGGRAPH 2007 courses, 2007."
    url: "https://dl.acm.org/doi/10.1145/1281500.1281665"
  - id: 2
    text: "ISO 19650-1:2018 — Organización y digitalización de la información sobre edificios e ingeniería civil, incluido el modelado de información de construcción (BIM)."
    url: "https://www.iso.org/standard/68078.html"
---

`os-console` es la superficie de cara al operador de la plataforma PointSav — un Libro Mayor de Comandos que se conecta a un [[totebox-os|Totebox]] y le presenta su estado al operador. No almacena datos ni ejecuta servicios; es un terminal de alta fidelidad diseñado específicamente para el flujo de trabajo del operador mediante teclado. El punto de referencia es el terminal financiero profesional: un único teclado, un pequeño conjunto de [[os-console-platform|teclas de función]], y un enfoque implacable en el contexto del operador. El binario está escrito desde cero en Rust para un arranque en frío por debajo de los 50 milisegundos y un tamaño de 15 megabytes. Este artículo cubre el funcionamiento de os-console, la superficie de teclas de función, la pila de renderizado y los dos modos de operación.

## Cómo funciona

`os-console` se distribuye como un único ejecutable y hoy funciona como una aplicación de
terminal estándar, construida sobre `ratatui` y `crossterm`. **Planificado, no actual**:
un entorno de ejecución con aislamiento de hardware en el que la API de virtualización
nativa del sistema operativo anfitrión (Windows Hypervisor Platform, `Hypervisor.
framework` o KVM) arranca un pequeño entorno [[sel4-microkernel-substrate|seL4]] aislado
alrededor de la aplicación. Esto es trabajo de hoja de ruta, no una descripción del binario
tal como se distribuye hoy — reservar afirmaciones como "reforzado por el kernel" para ese
estado futuro, no para el presente.

El modelo de seguridad depende de [[machine-based-auth|emparejamientos vinculados al
hardware]] en lugar de nombres de usuario o contraseñas, independientemente del elemento
de hoja de ruta de aislamiento por VM mencionado arriba.

## La superficie de teclas de función

La interfaz organiza la realidad de cada entidad en un conjunto fijo de pilares. Cada pilar es una tecla de función:

| Tecla | Pilar | Servicio |
|---|---|---|
| F1 | AYUDA | Procedimientos operativos de solo lectura |
| F2 | PERSONAS | [[service-people|service-people]] — el libro mayor de identidades |
| F3 | CORREO | [[service-email|service-email]] — el Diodo de Comunicación |
| F4 | CONTENIDO | [[service-content|service-content]] — el motor de redacción y síntesis |
| F5 | MINUTEBOOK | service-minutebook — registros profundos |
| F6 | BOOKKEEPER | service-bookkeeper — el libro mayor financiero |
| F12 | MÁQUINA DE ENTRADA | [[app-console-input]] — la puerta de ingesta con intervención humana |

F12 es obligatorio según [[architecture-decisions|SYS-ADR-10]]. La [[app-console-input|Máquina de Entrada]] es la única superficie a través de la cual archivos externos sin procesar pueden entrar a un Totebox. Los archivos depositados en F12 tienen eliminados sus permisos de ejecución, se etiquetan contra el [[archetypes-and-chart-of-accounts|Plan de Cuentas]] del operador y se enrutan a F5 o F6.

## La pila de renderizado

`os-console` hoy es una interfaz de terminal: la lógica de widgets y el renderizado se
construyen sobre `ratatui`, con `crossterm` gestionando el backend de terminal.
**Planificado, no actual**: una canalización de renderizado independiente y nativa de GPU
(una abstracción basada en WGPU para Vulkan/Metal/DX12 con un renderizador de glifos por
Campo de Distancia con Signo [^1] para fidelidad de zoom infinito, encabezados de peso
variable y efectos de brillo) que reemplazaría por completo al renderizador alojado en
terminal. La intención de diseño para esa futura canalización comparte su filosofía con
[[design-philosophy|el sistema de diseño más amplio de PointSav]], pero no es la pila que
funciona hoy.

## Modo directo y modo agregado

`os-console` opera en dos modos determinados por aquello con lo que se empareja:

| Modo | Par | Caso de uso |
|---|---|---|
| Directo | Un [[totebox-os|Totebox]] | Vista profunda de una única entidad; el predeterminado para operadores individuales |
| Agregado | Un [[os-orchestration|os-orchestration]] (que agrega muchos Toteboxes) | Vista de portafolio para ejecutivos y despliegues de nivel comercial |

Ambos modos utilizan el mismo binario de `os-console`. El agregador no requiere una Consola diferente. La complejidad reside en `os-orchestration`.

## Único, unificado, universal

`os-console` es un único producto. No existe edición "Doméstica" ni edición "Pro". Un individuo que aloja un Totebox utiliza el mismo Libro Mayor de Comandos que el administrador de un [[compliance-and-continuous-disclosure|Emisor Informante]] que agrega cientos. La diferenciación comercial la determina la presencia o ausencia de `os-orchestration`, nunca una Consola escalonada. La [[six-tier-sovereignty-matrix|matriz de soberanía de seis niveles]] rige cómo se estructuran los niveles comerciales en toda la plataforma.

## Véase también

- [[totebox-os]] — el archivo Totebox al que os-console se conecta y cuyo estado presenta
- [[app-console-input]] — la Máquina de Entrada F12; cobertura detallada de la puerta de ingesta obligatoria
- [[diode-standard]] — por qué los comandos fluyen en una sola dirección a través del par establecido
- [[os-family-overview]] — las cinco superficies de SO y cómo os-console encaja entre ellas
- [[deployment-patterns]] — cómo os-console aparece en cada una de las seis configuraciones de despliegue canónicas
