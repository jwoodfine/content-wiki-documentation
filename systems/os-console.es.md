---
schema: foundry-doc-v1
title: "os-console"
slug: os-console
category: systems
type: concept
content_type: topic
quality: complete
index_group: operator-surfaces
status: active
audience: vendor-public
bcsc_class: current-fact
language_protocol: PROSE-TOPIC
language: es
last_edited: 2026-07-31
editor: pointsav-engineering
paired_with: os-console.md
aliases: [console-os, os-console-architecture, os-console-platform, topic-os-console-architecture]
cites: []
references:
  - id: 1
    text: "Green, C. 'Improved Alpha-Tested Magnification for Vector Textures and Special Effects.' ACM SIGGRAPH 2007 courses, 2007."
    url: "https://dl.acm.org/doi/10.1145/1281500.1281665"
short_description: "os-console es la superficie de cara al operador de la plataforma PointSav — un Libro Mayor de Comandos, en un único binario nativo de teclado, que se conecta a un Totebox y aloja cartuchos TUI independientes mediante un chasis unificado."
---

`os-console` es la superficie de cara al operador de la plataforma PointSav — un Libro Mayor de Comandos que se conecta a un [[totebox-os|Totebox]] y le presenta su estado al operador. No almacena datos ni ejecuta servicios; es un terminal de alta fidelidad diseñado específicamente para el flujo de trabajo del operador mediante teclado. El punto de referencia es el terminal financiero profesional: un único teclado, un pequeño conjunto de teclas de función, y un enfoque implacable en el contexto del operador. El binario está escrito desde cero en Rust para un arranque en frío por debajo de los 50 milisegundos y un tamaño de 15 megabytes.

`os-console` es un binario compilado en Rust que aloja múltiples espacios de trabajo TUI independientes — cartuchos — dentro de un marco unificado de navegación por teclado. El principio de diseño es la propiedad de extremo a extremo: cada componente se compila en un único binario, sin carga dinámica de plugins, sin lanzamiento de subprocesos y sin anidamiento.

## Puntos clave

- `os-console` se distribuye hoy como una aplicación de terminal `ratatui`/`crossterm`, no la canalización de renderizado nativa de GPU o con aislamiento seL4 descrita en su hoja de ruta — esas son planificadas, no actuales. Reservar afirmaciones como "reforzado por el kernel" para ese estado futuro.
- Los cartuchos se compilan directamente en el binario — no se cargan dinámicamente ni se lanzan como subprocesos. `app-console-keys` (el chasis) y `app-console-input` (F12) son los únicos cartuchos obligatorios; todo lo demás es opcional.
- Según el registro de proyectos propio de la plataforma, 5 de 12 cartuchos posibles están `Active` hoy (bookkeeper, email, keys, slm, system); 3 están `Scaffold-coded` (content, input, people); los 4 restantes son marcadores de posición `Reserved-folder` (bim, help, mesh, minutebook — vault también está reservado).
- Ambos modos (Directo y Agregado) utilizan el mismo binario; el agregador no requiere una Consola diferente.
- Todos los puntos de acceso de servicio predeterminados se resuelven a direcciones localhost — el binario es operable sin archivo de configuración y no tiene dependencia fija de ninguna red externa.

## Cómo funciona

`os-console` se distribuye como un único ejecutable y hoy funciona como una aplicación de terminal estándar, construida sobre `ratatui` y `crossterm`. **Planificado, no actual**: un entorno de ejecución con aislamiento de hardware en el que la API de virtualización nativa del sistema operativo anfitrión (Windows Hypervisor Platform, `Hypervisor.framework` o KVM) arranca un pequeño entorno [[sel4-microkernel-substrate|seL4]] aislado alrededor de la aplicación. Esto es trabajo de hoja de ruta, no una descripción del binario tal como se distribuye hoy.

El modelo de seguridad depende de [[machine-based-auth|emparejamientos vinculados al hardware]] en lugar de nombres de usuario o contraseñas, independientemente del elemento de hoja de ruta de aislamiento por VM mencionado arriba.

Las plataformas de destino incluyen Linux Mint en el equipo de escritorio local y macOS 13 o posterior en estaciones de trabajo ejecutivas. Un modo de servidor SSH opcional, compilado con el indicador `--features ssh-server`, permite el acceso remoto para su uso en una VM de GCE. En esta configuración de PTY remoto, el proceso que emite píxeles y el terminal que los decodifica están en máquinas distintas, por lo que la canalización gráfica de Kitty y Sixel está deshabilitada. La dirección planificada es el despliegue nativo en el equipo anfitrión — el binario se ejecuta en la propia máquina del operador en un terminal local con capacidad gráfica, conectándose a un Archivo Totebox remoto a través de internet mediante [[machine-based-auth|autorización basada en máquinas]].

## La pila de renderizado

`os-console` hoy es una interfaz de terminal: la lógica de widgets y el renderizado se construyen sobre `ratatui`, con `crossterm` gestionando el backend de terminal. **Planificado, no actual**: una canalización de renderizado independiente y nativa de GPU (una abstracción basada en WGPU para Vulkan/Metal/DX12 con un renderizador de glifos por Campo de Distancia con Signo[^1] para fidelidad de zoom infinito, encabezados de peso variable y efectos de brillo) que reemplazaría por completo al renderizador alojado en terminal. La intención de diseño para esa futura canalización comparte su filosofía con [[design-philosophy|el sistema de diseño más amplio de PointSav]], pero no es la pila que funciona hoy.

## El chasis base: app-console-keys

`app-console-keys` es el chasis base siempre instalado dentro de `os-console`. Su relación con `os-console` es análoga a la que [[service-fs|`service-fs`]] tiene con `os-totebox`: es el componente mínimo requerido que debe estar presente; todo lo demás es opcional. Proporciona el rasgo `Cartridge`, el marco de navegación por teclas de función (la tira de pestañas horizontal, el despacho de entrada de teclas de función y el enrutamiento del cartucho activo), la barra de estado que muestra el estado de la conexión de [[machine-based-auth|autorización basada en máquinas]] y la identidad de sesión, el cliente de autorización que gestiona las conexiones a los servicios `os-*` emparejados, y la configuración basada en perfiles almacenada en `~/.config/os-console/config.toml`.

**Nota de nomenclatura:** "keys" en `app-console-keys` se refiere a teclas de función — F-keys. No se refiere a claves criptográficas. La autorización basada en máquinas es implementada por `system-gateway-mba`, un crate separado.

## El rasgo Cartridge

Cada crate `app-console-*` expone exactamente un tipo que implementa el rasgo `Cartridge`, definido en `app-console-keys`. El rasgo es la única interfaz entre un cartucho y el chasis — no existen otras API públicas:

```
trait Cartridge {
    fn fkey(&self) -> FKey;
    fn title(&self) -> &str;
    fn tick(&mut self);
    fn render(&mut self, frame, area);
    fn handle_event(&mut self, event) -> CartridgeAction;
    fn set_graphics_caps(&mut self, kitty, sixel, font_size, truecolor);
    fn flush_hyperlinks(&mut self, writer);
}
```

`tick()` y `render()` se invocan en cada iteración del bucle de eventos. `handle_event()` se invoca únicamente cuando llega un evento de teclado o ratón. `set_graphics_caps()` se invoca una sola vez al iniciar, después de que el chasis consulta las capacidades del terminal conectado. `flush_hyperlinks()` se invoca tras cada llamada a `render()`, permitiendo a los cartuchos emitir secuencias de hipervínculo OSC 8 en el flujo de salida del terminal. Tanto `set_graphics_caps()` como `flush_hyperlinks()` tienen implementaciones predeterminadas vacías en el rasgo, de modo que los cartuchos que no usan gráficos ni hipervínculos no incurren en código adicional.

Los cartuchos se registran al inicio mediante `chassis.register(Box<dyn Cartridge>)`. El registro es independiente del orden con respecto al renderizado, pero el orden determina la presentación en la barra de pestañas cuando las ranuras de teclas de función no son únicas. Cada cartucho registrado debe reclamar una ranura `FKey` distinta. Un cartucho que no está instalado tiene su ranura de tecla de función atenuada en la tira de pestañas. Los cartuchos son opcionales excepto `app-console-keys` y `app-console-input` (F12) — una instalación que incluya únicamente `app-console-content` (F4) y `app-console-input` (F12) es un despliegue de os-console completo y válido para trabajo editorial.

## El mapa de teclas de función

La consola presenta doce ranuras direccionables mediante teclas de función. F12 está fijada como El Ancla — la [[input-machine|Máquina de Entrada]] — y nunca se mueve. F12 es obligatorio según [[architecture-decisions|SYS-ADR-10]]: es la única superficie a través de la cual archivos externos sin procesar pueden entrar a un Totebox. Los archivos depositados en F12 tienen eliminados sus permisos de ejecución, se etiquetan contra el [[archetypes-and-chart-of-accounts|Plan de Cuentas]] del operador y se enrutan en consecuencia.

| Tecla F | Cartucho | Dominio | Estado del crate |
|---|---|---|---|
| F1 | `app-console-help` | Panel de ayuda | Reserved-folder |
| F2 | `app-console-people` | Identidad y contactos — [[service-people|service-people]] | Scaffold-coded |
| F3 | `app-console-email` | Comunicaciones — [[service-email|service-email]] | Active |
| F4 | `app-console-content` | Editorial — corrección, redacción, verificación — [[service-content|service-content]] | Scaffold-coded |
| F5 | `app-console-minutebook` | Gobernanza — actas, resoluciones | Reserved-folder |
| F6 | `app-console-bookkeeper` | Libro mayor financiero | Active |
| F7 | `app-console-bim` | Gestión de información de construcción | Reserved-folder |
| F8 | `app-console-gis` | Información geográfica | Reserved-folder |
| F9 | `app-console-slm` | Gestión de IA y mercado de adaptadores — Doorman / `service-slm` | Active |
| F10 | `app-console-mesh` | Gestión de malla de red | Reserved-folder |
| F11 | `app-console-system` | Estado de salud en vivo de los servicios `os-*` y estado de emparejamiento | Active |
| F12 | `app-console-input` | El Ancla — Máquina de Entrada (SYS-ADR-10) | Scaffold-coded |

El estado del crate corresponde al registro de proyectos propio de la plataforma, verificado contra las afirmaciones de este mismo artículo — borradores anteriores de este contenido subestimaban el conjunto activo (nombrando solo 4 de los 5 cartuchos actualmente `Active`). `app-console-vault` (sin asignación de tecla F) también es `Reserved-folder`.

### Cartuchos activos hoy

- **F3 — Correo (`app-console-email`).** `EmailCartridge` se conecta a Exchange Web Services (EWS) a través del backend `service-email` y presenta tres vistas: una lista de bandeja de entrada (resúmenes de mensajes en hilo con recuentos de no leídos), una vista de lectura (cuerpo completo del mensaje con indicadores de adjuntos) y redactar/enviar (composición en texto plano con campos `Para:` y `Asunto:`). Se admite el modo sin gráficos (sin Kitty/Sixel) para terminales que carecen de soporte de protocolo gráfico.
- **F6 — Bookkeeper (`app-console-bookkeeper`).** Patrón de plugin HTML (vista + cartucho); activado el 2026-04-22 como piloto de framework.
- **F9 — SLM (`app-console-slm`).** `SlmCartridge` renderiza un panel de estado en vivo para la [[doorman-protocol|pasarela de inferencia local]], consultando el endpoint de estado de la pasarela cada 10 segundos y mostrando la disponibilidad de los niveles A/B/C y el estado del disyuntor de circuito, el número de entidades en el almacén de datos local, y la profundidad de la cola de corpus con el resumen de coste diario. El operador puede forzar una actualización manual con `R`.
- **F11 — Sistema (`app-console-system`).** `SystemCartridge` proporciona el panel de operador para la gestión de sesiones Totebox. Su función principal en la fase actual es mostrar las aprobaciones de pairing pendientes — sesiones de preparación que esperan la firma del Command Session antes de que un commit sea promovido.

## Negociación de capacidades del terminal

Al inicio, el chasis consulta el terminal conectado mediante secuencias de escape estándar e inspección del entorno:

- **Protocolo gráfico Kitty:** detectado mediante respuesta APC a una secuencia de sondeo.
- **Sixel:** detectado mediante la variable de entorno `TERM` y atributos de dispositivo DA2.
- **Tamaño de celda de fuente:** consultado mediante xtwinops (CSI 16 t) cuando está disponible; recurre a una estimación de 10×20 px.
- **Truecolor:** detectado mediante `COLORTERM=truecolor` o `COLORTERM=24bit`.

Las capacidades resueltas se pasan a cada cartucho registrado mediante `set_graphics_caps(kitty, sixel, font_size, truecolor)`. El chasis nunca vuelve a llamar a `set_graphics_caps()` tras la negociación inicial — las capacidades quedan fijas durante la vida útil de la sesión.

Cuando truecolor está disponible, los cartuchos utilizan un conjunto de colores coherente: acento (bordes, resaltados) `Rgb(32, 178, 170)` — un verde azulado cercano al CSS LightSeaGreen; fondo de selección `Rgb(0, 95, 135)` — un azul verdoso oscuro; peligro/error `Rgb(200, 0, 0)` — rojo intenso. Cuando truecolor no está disponible — terminales simples, consolas serie — los cartuchos recurren a colores con nombre: Cyan para acentos, DarkGray para fondos de selección, Red para errores. La jerarquía visual se preserva; solo cambia la precisión.

`ContentCartridge` (F4) implementa `flush_hyperlinks()`. Durante `render()`, recopila destinos de URL de resultados de búsqueda y citas en un búfer interno. Tras completarse el ciclo de dibujo de ratatui, el chasis llama a `flush_hyperlinks()`, que emite secuencias OSC 8 (`OSC 8 ; params ; uri ST` para abrir un enlace, `OSC 8 ; ; ST` para cerrarlo). Los enlaces solo se emiten cuando el protocolo gráfico Kitty está activo — los terminales que admiten gráficos Kitty también admiten OSC 8 de forma fiable.

## La barra de estado

La barra de estado de `app-console-keys` siempre es visible en la parte inferior de la consola y proporciona al operador un panorama situacional en tiempo real:

```
operador@woodfine | MBA LINK ACTIVE | F4: Content | Tier A | 00:04:23
```

El componente de identidad muestra el nombre de usuario y el inquilino establecidos durante la ceremonia de emparejamiento. El estado de autorización muestra `MBA LINK ACTIVE`, `MBA LINK INACTIVE <motivo>` o `MBA LINK PENDING`. El nombre de la ranura del cartucho activo, el nivel de SLM en uso (A para local, B para ráfaga en la nube, C para API de frontera) y la duración de la sesión completan la barra.

## Conectividad de autorización

`app-console-keys` mantiene conexiones salientes con los servicios `os-*` emparejados. Cada emparejamiento es independiente: la consola puede estar activa con `os-totebox` e inactiva con `os-privategit` simultáneamente. Cuando el enlace de autorización está inactivo, `os-console` opera en modo solo local. El contenido almacenado en caché local permanece accesible. Las solicitudes a los servicios de backend `service-proofreader`, `service-input` y `service-content` fallan de manera controlada en lugar de bloquearse.

## Renderizado de PDF

`os-console` admite el renderizado de PDF dentro de la terminal mediante la biblioteca `pdfium-render` — bindings de Rust sobre pdfium de Chromium. Las páginas del PDF se renderizan como mapas de bits RGB y se muestran usando el protocolo gráfico Kitty como ruta principal, con Sixel como alternativa y un error para las terminales que no admiten ninguno de los dos. Esto es renderizado de píxeles, no extracción de texto.

## Ubicación en la arquitectura de la plataforma

`os-console` es un cliente de la [[three-ring-architecture|Arquitectura de Tres Anillos]], no un anillo en sí mismo. Se conecta a los servicios del Anillo 1 a través de la capa de autorización — `service-input` vía F12, [[service-people|`service-people`]] vía F2, [[service-email|`service-email`]] vía F3, y [[service-fs|`service-fs`]]; a los servicios del Anillo 2, incluyendo [[service-content|`service-content`]] y [[service-search|`service-search`]]; y al servicio del Anillo 3 [[service-slm|`service-slm`]] vía [[compounding-doorman|Doorman]]. `os-console` es la interfaz humana mediante la cual un operador instruye a los anillos.

Todos los puntos de acceso de servicio predeterminados en la configuración de la consola se resuelven a direcciones localhost. El binario es operable sin archivo de configuración y no tiene dependencia fija de ninguna red externa. La intención es que `os-console` arranque y se renderice completamente en una máquina sin acceso saliente a internet, conectándose solo a servicios que se ejecutan en el mismo nodo o dentro de la misma [[ppn-mesh-architecture|malla de PPN]].

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
- [[os-family-overview]] — la familia de SO y cómo os-console encaja entre ellas
- [[deployment-patterns]] — cómo os-console aparece en cada una de las seis configuraciones de despliegue canónicas
- [[machine-based-auth]] — el mecanismo de autorización que utiliza os-console
- [[input-machine]] — El Ancla; puerta de ingesta obligatoria en F12
- [[three-ring-architecture]] — la arquitectura de anillos a la que se conecta os-console
- [[compounding-doorman]] — el límite de auditoría Doorman para el acceso a service-slm
- [[os-console-totebox-browser]] — el explicador de la analogía del navegador para la filosofía de diseño de os-console
- [[ppn-small-business-compute]] — el sustrato de red al que se conecta os-console
- [[architecture-decisions]] — decisiones arquitectónicas que rigen la capa de datos de la plataforma
