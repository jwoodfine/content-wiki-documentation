---
schema: foundry-doc-v1
title: "Cómo navegar la TUI de la consola"
slug: navigate-console-tui
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
language: es
language_protocol: TRANSLATE-ES
paired_with: navigate-console-tui.md
---

`os-console` es una aplicación de terminal de pantalla completa que organiza las funciones de la plataforma en ranuras numeradas por tecla de función. Navegar la consola significa cambiar entre ranuras, leer la barra de estado y entender qué muestra la ranura activa. No se requiere ratón — el modelo de teclado es completo.

Para la arquitectura detrás de este modelo, véase [[app-console-keys]] y [[os-console-platform]].

## Requisitos previos

- Un dispositivo emparejado (véase [[pair-a-new-device]])
- `os-console` instalado y abierto
- Una sesión activa (véase [[open-first-totebox-session]])

## Disposición

La consola ocupa toda la ventana del terminal con tres regiones permanentes:

| Región | Ubicación | Contenido |
|---|---|---|
| Barra de estado | Parte superior | Etiqueta de identidad, estado de autorización, nombre de ranura activa, nivel SLM, duración de sesión |
| Área de ranura | Cuerpo principal | Salida de la ranura actualmente activa |
| Franja de navegación | Parte inferior | Etiquetas de tecla de función con las ranuras cargadas |

La franja de navegación muestra los nombres de ranura vinculados a cada tecla de función. Las ranuras no cargadas aparecen atenuadas.

## Cambiar ranuras con teclas de función

Presione cualquier tecla de función etiquetada para activar esa ranura. El área de ranura se actualiza de inmediato. El nombre de ranura activa en la barra de estado confirma cuál está activa.

Las ranuras cargadas conservan su estado al cambiar — una bandeja de entrada desplazada a un mensaje específico permanece en esa posición al regresar a F3.

## Leer la barra de estado

La barra de estado se actualiza de forma continua. De izquierda a derecha:

- **Identidad** — la identidad del dispositivo emparejado y su nivel de permiso
- **Estado de autenticación** — `LINKED` cuando la autorización basada en máquina está activa; `LINK INACTIVE` cuando no está disponible
- **Ranura activa** — el nombre del cartucho mostrado actualmente (p. ej., `INPUT`, `EMAIL`, `SLM`)
- **Nivel SLM** — el estado del circuito de Doorman: `A` (DataGraph activo), `B` (solo SLM) o `C` (respaldo local)
- **Duración de sesión** — tiempo transcurrido desde que se abrió la sesión

## Combinaciones de teclas que funcionan en todas las ranuras

| Tecla | Acción |
|---|---|
| F1–F12 | Cambiar a esa ranura |
| ? | Mostrar ayuda contextual para la ranura activa |
| q o Esc | Salir de la ranura activa al inicio (depende de la ranura) |
| Ctrl-C | Salir de `os-console` |

Las combinaciones específicas de cada ranura se muestran en la franja de navegación de la ranura activa.

## Puntos clave

- La navegación es completamente por teclado — el número de tecla de función = número de ranura
- Las ranuras conservan su estado; cambiar y regresar no destruye datos
- La barra de estado es la fuente de verdad sobre el estado de autorización y disponibilidad de SLM
- F12 es la Máquina de Entrada; siempre está presente y no puede reasignarse

## Véase también

- [[app-console-keys]] — el chasis y la interfaz Cartridge que implementan todas las ranuras
- [[os-console-platform]] — la taxonomía completa de teclas de función y qué cartucho ocupa cada ranura
- [[use-f-key-model]] — cómo trabajar con el modelo de cartuchos de tecla de función
- [[machine-based-auth]] — qué significan los estados de autenticación `LINKED`/`LINK INACTIVE`
- [[pair-a-new-device]] — registrar un dispositivo antes de abrir la consola
