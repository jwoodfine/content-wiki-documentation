---
schema: foundry-doc-v1
title: "os-console — El Libro Mayor de Comandos"
slug: console-os
category: systems
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
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

`os-console` es la superficie de cara al operador de la plataforma PointSav — un Libro Mayor de Comandos que se conecta a un [[totebox-os|Totebox]] y le presenta su estado al operador. No almacena datos ni ejecuta servicios; es un terminal de alta fidelidad diseñado específicamente para el flujo de trabajo del operador mediante teclado. El punto de referencia es el Bloomberg Terminal: un único teclado, un pequeño conjunto de teclas de función y un enfoque implacable en el contexto del operador. El binario está escrito desde cero en Rust para un arranque en frío por debajo de los 50 milisegundos y un tamaño de 15 megabytes. Este artículo cubre el funcionamiento de os-console, la superficie de teclas de función, la pila de renderizado y los dos modos de operación.

## Cómo funciona

`os-console` se distribuye como un único ejecutable. En el sistema operativo anfitrión — Windows, macOS o Linux — actúa como Monitor de Máquina Virtual: utiliza la API de virtualización nativa del anfitrión para crear una pequeña VM aislada en RAM y arranca un entorno seL4 dentro de ella.

| Anfitrión | API VMM nativa |
|---|---|
| Windows | Windows Hypervisor Platform (WHPX) |
| macOS | `Hypervisor.framework` |
| Linux | KVM |

El operador cree que abrió una aplicación. Lo que hizo fue iniciar un entorno seguro con aislamiento de hardware en aproximadamente 50 milisegundos. Cuando la aplicación se cierra, la memoria segura se borra. Nada toca el disco duro del anfitrión.

## La superficie de teclas de función

La interfaz organiza la realidad de cada entidad en un conjunto fijo de pilares. Cada pilar es una tecla de función:

| Tecla | Pilar | Servicio |
|---|---|---|
| F1 | AYUDA | [[app-console-input|content-wiki-documentation]] (procedimientos operativos de solo lectura) |
| F2 | PERSONAS | [[service-people|service-people]] — el libro mayor de identidades |
| F3 | CORREO | [[service-email|service-email]] — el Diodo de Comunicación |
| F4 | CONTENIDO | [[service-content|service-content]] — el motor de redacción y síntesis |
| F5 | MINUTEBOOK | service-minutebook — registros profundos |
| F6 | BOOKKEEPER | service-bookkeeper — el libro mayor financiero |
| F12 | MÁQUINA DE ENTRADA | [[app-console-input]] — la puerta de ingesta con intervención humana |

F12 es obligatorio según [[architecture-decisions|SYS-ADR-10]]. La [[app-console-input|Máquina de Entrada]] es la única superficie a través de la cual archivos externos sin procesar pueden entrar a un Totebox. Los archivos depositados en F12 tienen eliminados sus permisos de ejecución, se etiquetan contra el [[archetypes-and-chart-of-accounts|Plan de Cuentas]] del operador y se enrutan a F5 o F6.

## La pila de renderizado

`os-console` no es un TUI dentro de un terminal del anfitrión. Es una aplicación gráfica independiente que, por casualidad, muestra texto. La pila es de propiedad integral:

| Capa | Componente | Notas |
|---|---|---|
| Ventana | `pointsav-window` | Envoltorio personalizado Win32 / Cocoa / X11/Wayland |
| GPU | `pointsav-gpu` | WGPU (abstracción Vulkan / Metal / DX12); licencia embebida en el binario |
| Texto | `pointsav-text` | Renderizador de glifos por Campo de Distancia con Signo (SDF) [^1]; fidelidad de zoom infinito |
| Disposición | `pointsav-layout` | Cuadrícula recursiva de filas/columnas en aproximadamente 500 líneas de Rust |
| Lógica de widgets | Bifurcación del núcleo de ratatui | Solo lógica; el renderizador de ratatui reemplazado por la cadena WGPU |

El resultado es una interfaz de terminal con encabezados de peso variable, efectos de brillo y desplazamiento suave — manteniéndose puramente controlada por teclado y renderizando con la fidelidad requerida por los sufijos de estado de documentos ISO 19650 [^2].

## Modo directo y modo agregado

`os-console` opera en dos modos determinados por aquello con lo que se empareja:

| Modo | Par | Caso de uso |
|---|---|---|
| Directo | Un [[totebox-os|Totebox]] | Vista profunda de una única entidad; el predeterminado para operadores individuales |
| Agregado | Un [[os-orchestration|os-orchestration]] (que agrega muchos Toteboxes) | Vista de portafolio para ejecutivos y despliegues de nivel comercial |

Ambos modos utilizan el mismo binario de `os-console`. El agregador no requiere una Consola diferente. La complejidad reside en `os-orchestration`.

## Único, unificado, universal

`os-console` es un único producto. No existe edición "Doméstica" ni edición "Pro". Un individuo que aloja un Totebox utiliza el mismo Libro Mayor de Comandos que el administrador de un Emisor Informante que agrega cientos. La diferenciación comercial la determina la presencia o ausencia de `os-orchestration`, nunca una Consola escalonada.

## Véase también

- [[totebox-os]] — el archivo Totebox al que os-console se conecta y cuyo estado presenta
- [[app-console-input]] — la Máquina de Entrada F12; cobertura detallada de la puerta de ingesta obligatoria
- [[diode-standard]] — por qué los comandos fluyen en una sola dirección a través del par establecido
- [[os-family-overview]] — las cinco superficies de SO y cómo os-console encaja entre ellas
- [[deployment-patterns]] — cómo os-console aparece en cada una de las seis configuraciones de despliegue canónicas
