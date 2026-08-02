---
schema: foundry-doc-v1
title: "Arquitectura interna de os-console"
slug: os-console-architecture
category: systems
type: topic
content_type: topic
quality: complete
status: archived
archived: 2026-07-31
archived_reason: "Fragmentación de contenido genuina con console-os.md y os-console-platform.md — los tres describían el mismo producto (os-console) en profundidades técnicas superpuestas, con inconsistencias reales. Fusionado en un artículo canónico único, systems/os-console.md."
superseded_by: os-console
audience: vendor-public
bcsc_class: current-fact
language_protocol: PROSE-TOPIC
language: es
last_edited: 2026-07-09
editor: pointsav-engineering
paired_with: os-console-architecture.md
short_description: "os-console aloja múltiples espacios de trabajo TUI independientes — cartuchos — dentro de un chasis unificado de navegación por teclado. Este artículo cubre el rasgo Cartridge, la negociación de capacidades y el protocolo de hipervínculos OSC 8."
cites: []
---

`os-console` es un binario compilado en Rust que aloja múltiples espacios de trabajo TUI
independientes — cartuchos — dentro de un marco unificado de navegación por teclado.
Este artículo describe el diseño interno de ese marco: cómo se definen los cartuchos,
cómo el chasis despacha eventos, cómo se negocian las capacidades del terminal y cómo
los cartuchos comunican la intención de enlace al terminal.

## El rasgo Cartridge

Cada crate `app-console-*` expone exactamente un tipo que implementa el rasgo
`Cartridge`, definido en `app-console-keys`. El rasgo es la única interfaz entre un
cartucho y el chasis — no existen otras API públicas:

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

`tick()` y `render()` se invocan en cada iteración del bucle de eventos.
`handle_event()` se invoca únicamente cuando llega un evento de teclado o ratón.
`set_graphics_caps()` se invoca una sola vez al iniciar, después de que el chasis
consulta las capacidades del terminal conectado. `flush_hyperlinks()` se invoca tras
cada llamada a `render()`, permitiendo a los cartuchos emitir secuencias de hipervínculo
OSC 8 en el flujo de salida del terminal. Tanto `set_graphics_caps()` como
`flush_hyperlinks()` tienen implementaciones predeterminadas vacías en el rasgo, de modo
que los cartuchos que no usan gráficos ni hipervínculos no incurren en código adicional.

## Registro de cartuchos

Los cartuchos se registran al inicio mediante `chassis.register(Box<dyn Cartridge>)`.
El registro es independiente del orden con respecto al renderizado, pero el orden
determina la presentación en la barra de pestañas cuando las [[use-f-key-model|ranuras de teclas de función]]
no son únicas. Cada cartucho registrado debe reclamar una ranura `FKey` distinta.

La compilación predeterminada registra seis cartuchos:

| Tecla F | Cartucho | Se conecta a |
|---|---|---|
| F2 | `app-console-people` | `service-people` |
| F3 | `app-console-email` | `service-email` |
| F4 | `app-console-content` | `service-content`, `service-slm` |
| F9 | `app-console-slm` | Doorman / `service-slm` |
| F11 | `app-console-system` | servidor de emparejamiento |
| F12 | `app-console-input` | servicio de ingesta |

El cartucho F12 (`app-console-input`) es obligatorio en todo despliegue. Es la puerta de ingesta a través de la cual debe pasar todo texto originado por el operador antes de entrar a la capa de datos de la plataforma. Omitirlo es una violación de las restricciones de compilación.

## Paneles activos (despliegue actual)

De los seis cartuchos de la compilación predeterminada, cuatro son miembros activos del
espacio de trabajo hoy. Su alcance funcional actual:

- **F3 — Correo (`app-console-email`).** `EmailCartridge` se conecta a Exchange Web
  Services (EWS) a través del backend `service-email` y presenta tres vistas: una lista
  de bandeja de entrada (resúmenes de mensajes en hilo con recuentos de no leídos), una
  vista de lectura (cuerpo completo del mensaje con indicadores de adjuntos) y
  redactar/enviar (composición en texto plano con campos `Para:` y `Asunto:`). Se admite
  el modo sin gráficos (sin Kitty/Sixel) para terminales que carecen de soporte de
  protocolo gráfico.
- **F9 — SLM (`app-console-slm`).** `SlmCartridge` renderiza un panel de estado en vivo
  para la [[doorman-protocol|pasarela de inferencia local]], consultando el endpoint de
  estado de la pasarela cada 10 segundos y mostrando la disponibilidad de los niveles
  A/B/C y el estado del disyuntor de circuito, el número de entidades en el almacén de
  datos local, y la profundidad de la cola de corpus con el resumen de coste diario. El
  operador puede forzar una actualización manual con `R`.
- **F11 — Sistema (`app-console-system`).** `SystemCartridge` proporciona el panel de
  operador para la gestión de sesiones Totebox. Su función principal en la fase actual es
  mostrar las aprobaciones de pairing pendientes — sesiones de preparación que esperan la
  firma del Command Session antes de que un commit sea promovido.

| Crate | Estado | Notas |
|---|---|---|
| `app-console-keys` | Activo | Chasis |
| `app-console-email` | Activo | EmailCartridge |
| `app-console-slm` | Activo | SlmCartridge |
| `app-console-system` | Activo | SystemCartridge |

Las superficies de consola adicionales (`app-console-bim`, `app-console-bookkeeper`,
`app-console-content`, `app-console-input`, `app-console-mesh`,
`app-console-minutebook`, `app-console-people`, `app-console-vault`) se encuentran en
estado Reserved-folder o Scaffold-coded y no son miembros del espacio de trabajo.

## Negociación de capacidades del terminal

Al inicio, el chasis consulta el terminal conectado mediante secuencias de escape
estándar e inspección del entorno:

- **Protocolo gráfico Kitty:** detectado mediante respuesta APC a una secuencia de sondeo.
- **Sixel:** detectado mediante la variable de entorno `TERM` y atributos de dispositivo DA2.
- **Tamaño de celda de fuente:** consultado mediante xtwinops (CSI 16 t) cuando está
  disponible; recurre a una estimación de 10×20 px.
- **Truecolor:** detectado mediante `COLORTERM=truecolor` o `COLORTERM=24bit`.

Las capacidades resueltas se pasan a cada cartucho registrado mediante
`set_graphics_caps(kitty, sixel, font_size, truecolor)`. Los cartuchos las utilizan para
elegir entre colores RGB de 24 bits y la paleta de reserva de ocho colores con nombre.
El chasis nunca vuelve a llamar a `set_graphics_caps()` tras la negociación inicial —
las capacidades quedan fijas durante la vida útil de la sesión.

### Convenciones de color en truecolor

Cuando truecolor está disponible, los cartuchos utilizan un conjunto de colores coherente:

- Acento (bordes, resaltados): `Rgb(32, 178, 170)` — un verde azulado cercano al CSS
  LightSeaGreen.
- Fondo de selección: `Rgb(0, 95, 135)` — un azul verdoso oscuro.
- Peligro / error: `Rgb(200, 0, 0)` — rojo intenso.

Cuando truecolor no está disponible — terminales simples, consolas serie — los cartuchos
recurren a colores con nombre: Cyan para acentos, DarkGray para fondos de selección,
Red para errores. La jerarquía visual se preserva; solo cambia la precisión.

## Hipervínculos OSC 8

`ContentCartridge` (F4) implementa `flush_hyperlinks()`. Durante `render()`, recopila
destinos de URL de resultados de búsqueda y citas en un búfer interno. Tras completarse
el ciclo de dibujo de ratatui, el chasis llama a `flush_hyperlinks()`, que emite
secuencias OSC 8:

```
OSC 8 ; params ; uri ST   (abrir enlace)
OSC 8 ; ; ST              (cerrar enlace)
```

Los enlaces solo se emiten cuando el protocolo gráfico Kitty está activo — los terminales
que admiten gráficos Kitty también admiten OSC 8 de forma fiable. El no-op predeterminado
de `flush_hyperlinks()` en el rasgo significa que los cartuchos que no participan no
incurren en sobrecarga.

## Intención de despliegue centrada en el cliente

Todos los puntos de acceso de servicio predeterminados en la configuración de la consola
se resuelven a direcciones localhost. El binario es operable sin archivo de configuración
y no tiene dependencia fija de ninguna red externa. La intención es que `os-console`
arranque y se renderice completamente en una máquina sin acceso saliente a internet,
conectándose solo a servicios que se ejecutan en el mismo nodo o dentro de la misma
[[ppn-mesh-architecture|malla de PPN]].

## Véase también

- [[ppn-small-business-compute]] — el sustrato de red al que se conecta os-console
- [[architecture-decisions]] — decisiones arquitectónicas que rigen la capa de datos de la plataforma
