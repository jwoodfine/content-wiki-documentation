---
schema: foundry-doc-v1
title: "Cómo leer el libro mayor de comandos"
slug: read-the-command-ledger
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
language: es
language_protocol: TRANSLATE-ES
paired_with: read-the-command-ledger.md
---

El Libro Mayor de Comandos es el registro de auditoría de solo anexar de todo lo que ha producido una sesión de operador de Totebox — comandos ejecutados, registros verificados, mensajes enviados y límites de sesión. Leer el libro mayor es cómo se entiende el historial de una sesión, se audita lo que cambió durante una ventana y se verifica que un registro fue escrito en la secuencia esperada.

Para el papel del Libro Mayor de Comandos en la arquitectura de sesión, véase [[console-os]]. Para cómo funciona la capa de almacenamiento subyacente, véase [[service-fs-architecture]].

## Requisitos previos

- Una sesión Totebox activa (véase [[open-first-totebox-session]])
- Máquina de Entrada F12 disponible (véase [[app-console-input]])

## Leer el libro mayor en la Máquina de Entrada (F12)

La Máquina de Entrada en F12 muestra la actividad del libro mayor junto a la cola de verificación.

1. Presione **F12** para abrir la Máquina de Entrada.
2. Use las teclas de tabulador o flecha para navegar a la vista **Libro Mayor** (mostrada en la franja de navegación como `LEDGER`).
3. El libro mayor muestra entradas en orden cronológico, las más recientes al final. Cada entrada muestra una marca de tiempo, tipo de entrada y un resumen breve.
4. Use **Página Arriba** / **Página Abajo** para desplazarse; **/** para buscar entradas por palabra clave.

## Tipos de entrada

| Tipo | Significado |
|---|---|
| `SESSION_OPEN` | Se inició una sesión Totebox con la identidad indicada |
| `SESSION_CLOSE` | La sesión se cerró; duración registrada |
| `RECORD_VERIFIED` | Un operador humano confirmó un registro a través de F12 |
| `RECORD_REJECTED` | Un registro fue rechazado; enrutado a cuarentena |
| `MESSAGE_SENT` | Se despachó un mensaje saliente |
| `CHECKPOINT` | Se escribió una prueba firmada del estado del libro mayor (periódica) |

## Verificar una entrada específica

Para confirmar que un registro está genuinamente en el libro mayor (y no fue alterado después):

1. Anote la posición de la entrada (índice de fila) y el sufijo de hash mostrado.
2. Exporte el tile correspondiente usando la operación `read_since` en la CLI o la API de service-fs.
3. Calcule el hash SHA-256 del tile y compárelo con el hash de punto de control para esa posición.

Una discrepancia indica manipulación — la garantía WORM cubre la cadena desde la primera escritura, no solo el resumen visible.

Para el procedimiento de verificación detallado, véase [[verify-worm-ledger]].

## Exportar entradas del libro mayor

En la vista Libro Mayor de la Máquina de Entrada, presione **e** para exportar un rango de fechas como archivo de texto local. El formato del archivo es C2SP tlog-tiles en texto plano — legible sin herramientas de PointSav.

## Puntos clave

- El Libro Mayor de Comandos es de solo anexar; ninguna entrada puede modificarse ni eliminarse
- La Máquina de Entrada (F12) muestra la actividad del libro mayor junto a la cola de verificación — son dos vistas del mismo rastro de auditoría
- Los hashes de punto de control permiten verificación por terceros sin un servicio activo
- Exportar tiles produce formato C2SP tlog-tiles estándar; cualquier implementación SHA-256 puede verificar la cadena

## Véase también

- [[console-os]] — el papel del Libro Mayor de Comandos en la arquitectura de sesión
- [[service-fs-architecture]] — la capa de almacenamiento WORM que persiste las entradas del libro mayor
- [[worm-ledger-architecture]] — qué cubre la garantía WORM y qué no
- [[verify-worm-ledger]] — procedimiento paso a paso para verificar el libro mayor
- [[app-console-input]] — la Máquina de Entrada y su vista del libro mayor
