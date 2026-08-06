---
schema: foundry-doc-v1
title: "Navegar la TUI de la consola"
slug: navigate-console-tui
short_description: "Navega os-console por teclado — la barra de teclas de función arriba, los campos reales de la barra de estado abajo, y el cambio de ranuras sin perder estado."
category: how-to
index_group: working-in-the-console
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Ingenieros (con acceso directo al terminal); operadores de cliente"
language: es
language_protocol: TRANSLATE-ES
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: navigate-console-tui.md
---

## Requisitos previos

- Un dispositivo emparejado (véase [[pair-a-new-device]])
- `os-console` instalado y lanzado
- Una sesión activa (véase [[open-first-totebox-session]])

## Propósito

Aprenda el diseño real de pantalla de la consola y los campos de la barra de estado lo suficientemente bien como para navegar con confianza — unos minutos, y se mantiene preciso para cada cartucho que use después.

## Procedimiento

1. Lance `os-console` y observe las tres regiones fijas, de arriba a abajo: una fila de barra de teclas de función, el contenido del cartucho activo llenando el resto de la pantalla, y una fila de barra de estado en la parte inferior.

2. Lea la barra de teclas de función. Muestra una etiqueta para cada ranura de tecla de función, con la activa resaltada y las ranuras no cargadas atenuadas.

3. Lea la barra de estado. De izquierda a derecha: su identidad como `usuario@tenant`; el estado del enlace de Autorización Basada en Máquina (`MBA LINK ACTIVE`, `MBA LINK INACTIVE: <razón>`, o `MBA LINK PENDING`); la etiqueta completa de la ranura activa (p. ej. `F9: SLM`, no un número aislado); y el tiempo transcurrido de la sesión. Un distintivo `[N pendientes]` aparece solo cuando tiene solicitudes de emparejamiento pendientes.

   > **Nota:** no hay ningún indicador de nivel SLM en la barra de estado. El nivel de inferencia y el estado del circuito se muestran dentro del propio panel F9, no en la barra de estado persistente.

4. Presione cualquier tecla de función para cambiar a esa ranura. El área de contenido se actualiza de inmediato, y tanto el resaltado de la barra de teclas de función como el campo de ranura activa de la barra de estado confirman cuál está en vivo.

5. Cambie de una ranura y regrese. Los cartuchos mantienen su propio estado — un documento que estaba editando o un panel que estaba viendo queda exactamente como lo dejó.

6. Consulte la línea de sugerencias propia de cada cartucho para sus atajos de teclado específicos. No son universales — el panel de F9 responde a **R** (actualizar) y **?** (ayuda), por ejemplo, pero los atajos de un cartucho distinto son suyos propios y se muestran en su propia interfaz, no en una tabla de referencia compartida.

## Resultado esperado

Puede leer correctamente cada campo de la barra de estado, cambiar entre ranuras de teclas de función cargadas sin perder el estado de un cartucho, y sabe que debe consultar la línea de sugerencias propia de cada cartucho para los atajos específicos de este.

## Verificación

Cambie a al menos dos ranuras cargadas distintas y confirme que tanto la etiqueta resaltada de la barra de teclas de función como el campo de ranura activa de la barra de estado se actualizan para coincidir cada vez.

## Reversión

La navegación no tiene estado que revertir — cambiar de ranura o salir de la consola no cambia nada persistente por sí mismo. Si la propia acción de un cartucho sí escribe algo (enviar una entrada en F12, por ejemplo), la guía de ese cartucho cubre su propia reversión.

## Próximos pasos

- [[use-f-key-model]] — qué hace realmente cada cartucho predeterminado, corregido contra la fuente real
- [[explore-the-console]] — un primer recorrido guiado que combina el diseño, F9 y F12

## Véase también

- [[app-console-keys]] — el chasis, el trait Cartridge y la implementación de la barra de estado
- [[machine-based-auth]] — qué significan los estados del enlace MBA
- [[pair-a-new-device]] — registre un dispositivo antes de abrir la consola
