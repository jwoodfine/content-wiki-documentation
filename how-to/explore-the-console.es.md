---
schema: foundry-doc-v1
title: "Explorar la consola por primera vez"
slug: explore-the-console
short_description: "Orienta a un operador de primera vez en os-console — la barra de estado, el panel F9 de la pasarela de inferencia y el punto de control obligatorio F12 que escribe en el libro mayor WORM."
category: how-to
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Ingenieros (con acceso directo al terminal); operadores de cliente"
language: es
language_protocol: TRANSLATE-ES
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: explore-the-console.md
---

## Requisitos previos

- Un dispositivo emparejado (véase [[pair-a-new-device]])
- El binario `os-console` disponible en su PATH, o compilado localmente desde `os-console/`
- Un emulador de terminal — el color de 24 bits y los protocolos gráficos Kitty o Sixel se usan cuando están disponibles y mejoran la pantalla, pero la consola se degrada con elegancia a colores con nombre y renderizado solo de texto sin ellos

## Propósito

Oriéntese en `os-console` por primera vez: la imagen situacional en vivo de la barra de estado, el panel de salud de la pasarela de inferencia en F9, y el punto de control de entrada en F12. Cada cambio de estado de la plataforma pasa por ahí — hágalo antes de empezar una tarea real.

## Procedimiento

1. Inicie la consola desde la línea de comandos:

   ```
   os-console
   ```

2. Lea la barra de estado en la parte inferior de la pantalla. Muestra, de izquierda a derecha: su identidad como `usuario@tenant`; el estado del enlace de Autorización Basada en Máquina (`MBA LINK ACTIVE`, `MBA LINK INACTIVE: <razón>`, o `MBA LINK PENDING`); la ranura activa, mostrada con su etiqueta completa (p. ej. `F9: SLM`, no un número de tecla de función aislado); y el tiempo transcurrido de la sesión. Un distintivo `[N pendientes]` aparece solo cuando tiene solicitudes de emparejamiento pendientes de revisar.

3. Presione **F9** para abrir el panel de Infraestructura SLM. Consulta la pasarela de inferencia cada 10 segundos y muestra cinco secciones: **Gateway** (rendimiento del Nivel A, estado del circuito del Nivel B, clase de nodo), **Flota YoYo** (estado por nodo de la capacidad de ráfaga de GPU en la nube), **DataGraph** (recuento de entidades y su propio estado de circuito — DataGraph es un campo separado, no un cuarto nivel), **Cola** (recuentos de pendientes, en curso, pausados, terminados, en cuarentena y envenenados) y **Costo de hoy**.

   > **Nota:** los tres niveles de inferencia son el Nivel A (modelo local, en esta máquina), el Nivel B (Yo-Yo — ráfaga hacia capacidad de GPU en la nube) y el Nivel C (API externa, tareas de precisión acotada contra una lista de permitidos explícita). Esto no es la misma división de tres vías que la disponibilidad de DataGraph, que el panel rastrea por separado.

4. Presione **R** para forzar una actualización inmediata del panel F9 en lugar de esperar al siguiente sondeo de 10 segundos. La línea de sugerencias en pantalla confirma que el atajo está activo.

5. Presione **F12** para abrir la Máquina de Entrada — el punto de control de ingesta obligatorio de la plataforma. Cada entrada del operador que modifica el estado de la plataforma pasa por esta ranura; no se puede omitir mediante un menú ni con el ratón.

   > **Advertencia:** F12 no es una zona de pruebas. Un envío aquí es una escritura real. Si tiene éxito, se anexa al libro mayor WORM inmutable de la plataforma y no se puede retirar — no envíe contenido desechable "solo para ver qué pasa".

6. Envíe una nota de prueba corta y genuinamente desechable si quiere ver el flujo completo. Verá uno de dos resultados: una confirmación que muestra un ID de carga útil y la altura/raíz del libro mayor en la que se escribió (con una variante de advertencia si el envío llevaba un problema no fatal), o un panel de error simple si el envío falló. No existe un resultado independiente de "cuarentena" en este flujo — ese concepto pertenece a un subsistema distinto (la cola de inferencia que se muestra en F9), no a F12.

7. Muévase entre F3, F9 y F12 y confirme que la etiqueta de ranura activa de la barra de estado se actualiza para coincidir cada vez.

## Resultado esperado

Puede leer de un vistazo los campos de identidad, estado del enlace y ranura activa de la barra de estado. El panel F9 muestra datos en vivo de Gateway/Flota YoYo/DataGraph/Cola/Costo y responde a una actualización manual. F12 ha aceptado o rechazado un envío real, con el resultado visible en pantalla.

## Verificación

- La etiqueta de ranura activa de la barra de estado cambia correctamente al alternar entre F3, F9 y F12.
- La marca de tiempo "actualizado" en pantalla de F9 cambia al presionar **R**.
- Un envío exitoso en F12 muestra un ID de carga útil y una posición en el libro mayor; el libro mayor WORM de la plataforma lo registra como una entrada genuina y permanente.

## Reversión

Explorar la barra de estado y el panel F9 no cambia nada — salga de la consola en cualquier momento sin necesidad de limpieza. Un envío real en F12 es la única excepción: no se puede revertir una vez confirmado, por lo que el paso 6 anterior es opcional y solo vale la pena hacerlo con contenido con el que se sienta cómodo dejando permanente.

Si la consola no responde como se espera, salga y reiníciela. Observe la salida de su propia terminal en busca de errores en lugar de revisar los registros del sistema — un `os-console` simple lanzado desde su propia shell no se ejecuta bajo ningún servicio del sistema, así que un registro del sistema no tiene nada que haber capturado.

## Próximos pasos

- [[navigate-console-tui]] — la referencia completa de la TUI: cada atajo de teclado y campo de la barra de estado
- [[use-f-key-model]] — la arquitectura de ranuras de teclas de función y la asignación predeterminada de cada Cartucho
- [[run-first-slm-query]] — envíe una consulta de inferencia real una vez que F9 muestre el Nivel B en vivo

## Véase también

- [[pair-a-new-device]] — cómo adquirir el emparejamiento de dispositivo del que depende esta sesión de consola
- [[read-the-command-ledger]] — leer las entradas del libro mayor WORM que escribe F12
- [[os-console]] — la arquitectura completa detrás de la consola que acaba de explorar
