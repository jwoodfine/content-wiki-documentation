---
schema: foundry-doc-v1
title: "os-console: plataforma y arquitectura de cartuchos"
slug: os-console-platform
category: architecture
type: concept
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-06-29
editor: pointsav-engineering
paired_with: os-console-platform.md
short_description: "os-console es un único binario de Rust que aloja espacios de trabajo TUI independientes — cartuchos — dentro de un chasis de navegación por teclado construido sobre app-console-keys; este artículo cubre la estructura de la plataforma, el mapa de cartuchos por tecla de función, la conectividad MBA y la ubicación en la Arquitectura de Tres Anillos."
cites: []
references: []
---

`os-console` es la interfaz de consola nativa de teclado para las operaciones del Totebox Archive de Woodfine. Se compila como un único binario de Rust, se ejecuta de forma nativa en Linux y macOS, renderiza interfaces de usuario de terminal completas y se conecta a servicios `os-*` de backend a través de la [[machine-based-auth|Autorización Basada en Hardware]]. El binario entrega una consola que inicia en milisegundos, responde a la velocidad del teclado y continúa operando con contenido en caché local cuando los servicios de backend están temporalmente no disponibles.

El diseño interno — cómo el binario implementa el Cartridge trait y el despacho de eventos del chasis — se cubre en [[os-console-architecture]]. Este artículo cubre la plataforma en sí: qué es el binario, cómo funciona el modelo de cartuchos, el mapa de teclas de función y la ubicación dentro de la Arquitectura de Tres Anillos.

> **Dirección planificada.** Se pretende evolucionar os-console hacia un escritorio soberano nativo del host con entrada dual: múltiples cartuchos visibles simultáneamente, soporte completo de ratón con paridad de teclado y una superficie de visibilidad de capacidades en tiempo real. Las descripciones a continuación reflejan la plataforma actual tal como está construida; las capacidades orientadas al futuro se marcan como planificadas o previstas.

## El binario

`os-console` es un único binario compilado que contiene todos los cartuchos. No se carga ningún plugin dinámico en tiempo de ejecución. No se lanzan subprocesos. Todos los espacios de trabajo, toda la lógica de navegación y todos los clientes de backend se compilan juntos en un único artefacto desplegable.

Este modelo de compilación produce un comportamiento en tiempo de ejecución predecible: un cartucho ausente de una compilación no se enlaza, y su slot de tecla de función aparece como no disponible en la barra de pestañas. El operador no puede instalar ni eliminar cartuchos en tiempo de ejecución — el conjunto de espacios de trabajo disponibles queda fijado en el momento de la compilación.

El binario se ejecuta en dos plataformas:

**Linux (despliegue principal).** El despliegue de referencia se ejecuta en un sistema Linux en la estación de trabajo principal del operador. Cualquier emulador de terminal basado en VTE es compatible; se recomienda el terminal Kitty para capacidad completa de gráficos de píxeles, incluida la renderización de PDF en terminal.

**macOS (estaciones de trabajo ejecutivas).** Binarios nativos de macOS compilados mediante CI en ejecutores macOS. Los terminales compatibles incluyen Kitty, Ghostty, iTerm2 y WezTerm.

## El chasis base: app-console-keys

`app-console-keys` es el chasis base siempre presente dentro de `os-console`. Su relación con `os-console` es análoga a la relación de `service-fs` con `os-totebox`: es el componente mínimo requerido — todo lo demás es aditivo.

Una instalación mínima — para un operador que solo necesita navegación por teclas de función y conexión a un Totebox Archive — necesita únicamente `app-console-keys`. Cada otro cartucho extiende esa base.

`app-console-keys` proporciona cuatro capacidades principales:

**El Cartridge trait.** La interfaz que implementa cada cartucho. El trait es el único contrato entre un cartucho y el chasis — no existen otras APIs públicas, sin memoria compartida y sin acoplamiento directo entre cartuchos.

**Marco de navegación por teclas de función.** La barra de pestañas renderizada en la parte superior de la consola, el despachador de eventos que enruta la entrada de teclado al cartucho activo, y el mecanismo por el cual F12 siempre activa la Máquina de Ingesta independientemente del cartucho activo (véase [[input-machine]]).

**La barra de estado.** Un panel persistente en la parte inferior de la pantalla que muestra una imagen situacional en tiempo real: identidad del operador, estado de conexión MBA, cartucho activo, nivel SLM en uso y duración de la sesión. Una representación ilustrativa:

```
operador@tenant | MBA LINK ACTIVE | F4: Contenido | Nivel A | 00:04:23
```

**Cliente MBA.** El gestor de conexiones salientes para la [[machine-based-auth|Autorización Basada en Hardware]]: lee la configuración de emparejamiento, inicia conexiones a los servicios `os-*` emparejados y presenta el estado de conexión agregado en la barra de estado.

Una nota sobre nomenclatura: `app-console-keys` se refiere a teclas de función (teclas de función del teclado), no a claves criptográficas. La implementación criptográfica MBA se encuentra en `system-gateway-mba`, un crate de capa de sistema separado.

## Cartuchos

Cada crate `app-console-*` es una biblioteca de Rust que implementa el Cartridge trait y se compila directamente en `os-console`. Los cartuchos no se cargan dinámicamente. La lista de cartuchos en el momento de la compilación es la lista de cartuchos en tiempo de ejecución.

La interfaz de trait único impone un aislamiento estricto: un cartucho no puede llamar directamente a otro. Todo el flujo de datos entre cartuchos pasa a través de los servicios `os-*` de backend. El estado interno de cada cartucho es invisible para todos los demás — un diseño que simplifica tanto la implementación como la revisión de seguridad.

Los cartuchos son opcionales excepto `app-console-keys`. Una instalación que incluye solo el cartucho editorial (F4) y la Máquina de Ingesta (F12) es un despliegue completo y válido para trabajo editorial.

## El mapa de teclas de función

La consola presenta doce slots direccionables mediante teclas de función. F12 está permanentemente asignada a la Máquina de Ingesta — es El Ancla, inamovible por diseño. Los slots restantes están organizados por dominio operativo, con las operaciones de alta frecuencia en los números de función más bajos:

| Tecla | Cartucho | Dominio |
|---|---|---|
| F1 | `app-console-help` | Ayuda contextual — siempre disponible |
| F2 | `app-console-people` | Identidad y contactos |
| F3 | `app-console-email` | Comunicaciones |
| F4 | `app-console-content` | Editorial — corrección, redacción, verificación |
| F5 | `app-console-minutebook` | Gobernanza — actas, resoluciones |
| F6 | `app-console-bookkeeper` | Libro mayor financiero |
| F7 | `app-console-bim` | Gestión de información de edificios |
| F8 | `app-console-gis` | Información geográfica |
| F9 | `app-console-slm` | Gestión de IA y mercado de adaptadores |
| F10 | `app-console-mesh` | Gestión de malla PPN |
| F11 | `app-console-system` | Estado en tiempo real de servicios `os-*` y estado MBA |
| F12 | `app-console-input` | **El Ancla** — Máquina de Ingesta ([[sys-adr-10]]) |

La asignación permanente de F12 a la ingesta de documentos es la restricción registrada en [[sys-adr-10]]. La tecla de función que ancla la frontera de cumplimiento normativo no se mueve independientemente de cómo evolucionen los demás slots.

## Conectividad MBA

`app-console-keys` mantiene conexiones MBA salientes a cada servicio `os-*` emparejado de forma independiente. La consola puede estar activa con `os-totebox` e inactiva con `os-privategit` simultáneamente; la barra de estado muestra el estado agregado. Cuando `MBA LINK INACTIVE`, la consola opera en modo solo local: el contenido en caché permanece accesible y las solicitudes de servicio fallan de forma controlada. Para el mecanismo MBA véase [[machine-based-auth]].

## Renderización de PDF

`os-console` admite la renderización de PDF en terminal utilizando enlaces de Rust a la biblioteca pdfium. Las páginas PDF se renderizan como mapas de bits RGB y se muestran utilizando el protocolo gráfico de Kitty en terminales compatibles, con el protocolo Sixel como alternativa. La renderización es fiel en píxeles — una reproducción exacta del diseño, tipografías y gráficos del PDF — no una extracción o reajuste de texto. Se requiere un terminal compatible; la capacidad se deshabilita en terminales que no admiten ninguno de los dos protocolos.

## Ubicación en la Arquitectura de Tres Anillos

`os-console` es un cliente de la Arquitectura de Tres Anillos, no un anillo en sí mismo. Se conecta a los servicios del Anillo 1 y el Anillo 2 a través de la capa MBA:

- **Servicios del Anillo 1:** `service-input` (a través de la Máquina de Ingesta F12), `service-people` (a través de F2), `service-email` (a través de F3), `service-fs`
- **Servicios del Anillo 2:** `service-content`, `service-search`
- **Servicio del Anillo 3:** `service-slm` (la puerta de inferencia Doorman)

`os-console` es la interfaz humana a través de la cual un operador instruye a los anillos. No realiza el trabajo de ningún anillo; los anillos operan de forma independiente y la consola se conecta a ellos.

## Véase también

- [[os-console-architecture]] — implementación interna del Cartridge trait y despacho de eventos del chasis
- [[input-machine]] — F12: El Ancla; puerta de ingesta de documentos obligatoria
- [[machine-based-auth]] — el mecanismo de autorización que usa os-console para conectarse a los servicios os-*
- [[ppn-mesh-architecture]] — la capa de infraestructura en la que se ejecutan los servicios os-*
- [[three-ring-architecture]] — la arquitectura de servicios dentro de la cual os-console opera como cliente
- [[sys-adr-10]] — el registro de decisión arquitectónica que establece F12 como el punto de control de ingesta obligatorio
