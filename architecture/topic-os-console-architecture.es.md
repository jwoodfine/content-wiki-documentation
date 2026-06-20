---
schema: foundry-doc-v1
content_type: topic
title: "Arquitectura del OS Console"
slug: topic-os-console-architecture
aliases:
  - topic-os-console-architecture
short_description: "El OS Console es una interfaz de operador nativa de terminal para sesiones Totebox, construida sobre un modelo de chasis y cartuchos donde cada panel se conecta en una ranura de tecla de función."
category: architecture
type: reference
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: TRANSLATE-ES
last_edited: 2026-06-20
editor: pointsav-engineering
paired_with: topic-os-console-architecture.md
cites: []
---

# Arquitectura del OS Console

El OS Console es una interfaz de operador nativa de terminal para sesiones Totebox.
Presenta un sistema de paneles múltiples controlado por teclas de función, donde cada
panel se implementa como un `Cartridge` independiente que se conecta al chasis de la
consola en una ranura de tecla de función designada.

## Modelo de Chasis y Cartucho

`app-console-keys` proporciona el chasis: un esqueleto TUI basado en ratatui que gestiona
el ciclo de vida del terminal, el bucle de eventos y el pipeline de renderizado gráfico
Kitty/Sixel. El chasis expone el trait `Cartridge`, que implementa cada crate de panel:

```rust
pub trait Cartridge {
    fn title(&self) -> &str;
    fn render(&self, frame: &mut Frame, area: Rect);
    fn handle_event(&mut self, event: &Event) -> CartridgeAction;
}
```

En tiempo de ejecución, el chasis carga exactamente un `Cartridge` activo a la vez. El
operador cambia de panel mediante teclas de función. El chasis gestiona la generación de
códigos QR (huellas digitales de claves Ed25519 renderizadas como imágenes en línea
Kitty/Sixel) de forma independiente al contenido del panel.

## Paneles Activos

### F3 — Correo (`app-console-email`)

`EmailCartridge` se conecta a Exchange Web Services (EWS) a través del backend
`service-email`. Presenta tres vistas:

- Lista de bandeja de entrada — resúmenes de mensajes en hilo con recuentos de no leídos
- Lectura — cuerpo completo del mensaje con indicadores de adjuntos
- Redactar/enviar — composición en texto plano con campos `Para:` y `Asunto:`

Se admite el modo sin gráficos (sin Kitty/Sixel) para terminales que carecen de soporte
de protocolo gráfico.

### F9 — SLM (`app-console-slm`)

`SlmCartridge` renderiza un panel de estado en vivo para la pasarela de inferencia local.
Consulta el endpoint de estado de la pasarela cada 10 segundos y muestra:

- Disponibilidad de los niveles A/B/C y estado del disyuntor de circuito
- Número de entidades en el almacén de datos local
- Profundidad de la cola de corpus y resumen de coste diario

El operador puede forzar una actualización manual con `R`.

### F11 — Sistema (`app-console-system`)

`SystemCartridge` proporciona el panel de operador para la gestión de sesiones Totebox.
Su función principal en la fase actual es mostrar las aprobaciones de pairing pendientes:
sesiones de preparación que esperan la firma del Command Session antes de que un commit
sea promovido.

## Capacidades del Terminal

La consola detecta las capacidades del terminal al iniciar:

| Función | Método de detección |
|---|---|
| Protocolo gráfico Kitty | Variables de entorno `TERM` / `TERM_PROGRAM` |
| Alternativa Sixel | `$COLORTERM` y consulta de capacidad del terminal |
| Modo sin gráficos | Flag explícito `--plain` o capacidad ausente |

El renderizado de códigos QR (usado por `app-console-keys` para mostrar huellas de
claves) emplea el protocolo de imagen en línea Kitty cuando está disponible y recurre al
renderizado de caracteres de bloque de ratatui en caso contrario.

## Pertenencia al Espacio de Trabajo

Los crates de consola que son miembros activos del espacio de trabajo:

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

## Véase También

- [[topic-os-console-totebox-browser|os-console: El Navegador de Totebox Orchestration]] —
  la superficie del navegador nativa de Totebox dentro de la consola
- [[topic-ppn-small-business-compute|Cómputo PPN para Pequeñas Empresas]] — superficie
  de gestión de flota accesible a través del panel de operador
- [[topic-software-distribution-substrate|Sustrato de Distribución de Software]] — la
  capa de licencias que controla el despliegue de los binarios de la consola

---

*Woodfine Capital Projects™, MCorp™, PointSav Digital Systems™, Totebox Orchestration™, Totebox Archive™ y Capability Geometry™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos propietarios.*
