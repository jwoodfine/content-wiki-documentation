---
schema: foundry-doc-v1
title: "Arquitectura interna de os-console"
slug: os-console-architecture
category: architecture
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: current-fact
language_protocol: PROSE-TOPIC
language: es
last_edited: 2026-06-13
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
determina la presentación en la barra de pestañas cuando las ranuras de teclas de función
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

## Intención de despliegue soberano

Todos los puntos de acceso de servicio predeterminados en la configuración de la consola
se resuelven a direcciones localhost. El binario es operable sin archivo de configuración
y no tiene dependencia fija de ninguna red externa. La intención es que `os-console`
arranque y se renderice completamente en una máquina sin acceso saliente a internet,
conectándose solo a servicios que se ejecutan en el mismo nodo o dentro de la misma
malla de PPN.

## Véase también

- [[ppn-small-business-compute]] — el sustrato de red al que se conecta os-console
- [[architecture-decisions]] — decisiones arquitectónicas que rigen la capa de datos de la plataforma
