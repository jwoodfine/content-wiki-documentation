---
schema: foundry-doc-v1
title: "Cómo explorar la consola por primera vez"
slug: explore-the-console
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
language: es
language_protocol: TRANSLATE-ES
paired_with: explore-the-console.md
---

La consola de la plataforma es una aplicación de terminal que organiza las herramientas orientadas al operador en un conjunto de ranuras de teclas de función, cada una ejecutando un Cartucho distinto. Cuando abre la consola por primera vez, la interfaz puede parecer desconocida — esta guía le muestra el diseño, cómo moverse entre ranuras y cómo confirmar que el sistema funciona antes de comenzar su primera tarea real.

Para la referencia completa de la TUI, véase [[navigate-console-tui]]. Para el modelo de ranura de tecla de función en profundidad, véase [[use-f-key-model]].

## Requisitos previos

- Un dispositivo emparejado con acceso de nivel apropiado (véase [[pair-a-new-device]])
- El binario de la consola compilado y disponible en su PATH, o el binario del espacio de trabajo en `~/Foundry/clones/<archivo>/os-console/`
- Un emulador de terminal que admita color de 24 bits y al menos 80×24 caracteres

## Paso 1: Iniciar la consola

Inicie la consola desde la línea de comandos:

```
os-console
```

Si el binario no está en PATH, ejecútelo directamente desde la salida de compilación:

```
~/Foundry/clones/<archivo>/target/debug/os-console
```

La consola se abre en modo de pantalla completa. Verá un diseño de tres zonas: una barra de estado en la parte superior, un área de contenido principal en el centro y una tira de navegación en la parte inferior.

## Paso 2: Leer la barra de estado

La barra de estado en la parte superior de la pantalla muestra el estado actual del sistema de un vistazo. De izquierda a derecha:

- **Identidad** — la identidad del operador activo (una cadena de nombre corta establecida en el momento del emparejamiento)
- **Estado de autenticación** — `INPUT`, `USER` o `READ` — el nivel de acceso de la sesión actual
- **Ranura activa** — la tecla de función actualmente activa (p.ej., `F3`)
- **Nivel SLM** — el nivel de Doorman en uso: `A` (DataGraph activo), `B` (solo SLM) o `C` (respaldo local)
- **Duración de la sesión** — tiempo desde que se inició la consola

Si el estado de autenticación muestra `READ` y esperaba `INPUT` o `USER`, el dispositivo no ha completado la secuencia de emparejamiento para el nivel solicitado. Véase [[pair-a-new-device]] para resolver esto.

## Paso 3: Navegar a la ranura de salud de Doorman

Presione **F9** para activar el Cartucho SLM. Esta ranura muestra el panel de salud de Doorman — el estado actual del circuito de inferencia de Nivel A/B/C.

Cada nivel muestra su estado:

- `A — DataGraph` — verde si el almacén de entidades es accesible; `OPEN` si el circuito se ha abierto
- `B — SLM` — verde si el modelo de inferencia local está cargado y respondiendo; `OPEN` si no pudo iniciarse
- `C — Respaldo local` — siempre `AVAILABLE` a menos que el binario del modelo OLMo local esté faltante

La salud de Doorman es lo primero que hay que verificar al iniciar una sesión. Un A y B verdes significa que la pila completa de inferencia y búsqueda de entidades está disponible. Un circuito abierto en cualquier nivel significa que algunas características están degradadas; la consola retrocede automáticamente, pero debe notar qué nivel se ve afectado.

## Paso 4: Presionar R para actualizar

Mientras está en F9, presione **R** para forzar una actualización del estado de Doorman. La línea de estado se actualiza en un segundo. Esto confirma que la consola está sondeando el servicio Doorman y el teclado responde correctamente.

## Paso 5: Navegar a la ranura de la Máquina de Entrada

Presione **F12** para activar el Cartucho de la Máquina de Entrada. Este es el punto de control de entrada obligatorio requerido por SYS-ADR-10 — cada entrada del operador que modifica el estado de la plataforma pasa por esta ranura.

Verá un área de entrada. Intente enviar una nota de texto simple. La consola muestra si la entrada fue **confirmada** (escrita en el libro mayor WORM) o **rechazada** (en cuarentena con un código de motivo).

## Paso 6: Revisar los cambios de la barra de estado

A medida que se mueve entre ranuras, el indicador de **Ranura activa** de la barra de estado cambia. Confirme que cambiar entre F3, F9 y F12 actualiza el indicador correctamente. Si el indicador no se actualiza, es posible que el bucle de renderizado de la TUI haya encontrado un error — salga y reinicie la consola, luego verifique `journalctl -u os-console` para ver la salida de errores.

## Puntos clave

- Las tres zonas principales son: barra de estado (superior), área de contenido (centro), tira de navegación (inferior)
- F9 = panel de salud de Doorman; verifique esto primero al inicio de cada sesión
- R actualiza la ranura actual sin cambiar de ranura
- F12 es el punto de control de entrada obligatorio; todas las modificaciones al estado de la plataforma pasan por él
- El estado de autenticación `READ` significa que el emparejamiento INPUT o USER no ha sido completado para esta sesión

## Véase también

- [[navigate-console-tui]] — referencia completa de TUI: teclas de acceso rápido, definiciones de campos de la barra de estado
- [[use-f-key-model]] — la arquitectura de ranura de tecla de función, el modelo de Cartucho, todas las asignaciones de ranura predeterminadas
- [[pair-a-new-device]] — cómo adquirir niveles de autenticación más altos para la sesión de consola
- [[run-first-slm-query]] — enviar una consulta de inferencia SLM una vez que F9 muestra el Nivel B activo
- [[read-the-command-ledger]] — leer el libro mayor WORM desde la pestaña LEDGER de F12
