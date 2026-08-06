---
schema: foundry-doc-v1
title: "Usar el modelo de cartuchos de tecla de función"
slug: use-f-key-model
short_description: "Trabaja con el modelo de cartuchos de tecla de función de os-console — correo en F3, el panel SLM de solo monitoreo en F9, la Máquina de Entrada basada en archivos en F12 — donde cada cartucho compilado posee el renderizado y la entrada de su ranura."
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
paired_with: use-f-key-model.md
---

## Requisitos previos

- Una sesión activa con `os-console` abierto (véase [[open-first-totebox-session]])
- Familiaridad con el diseño de la consola (véase [[navigate-console-tui]])

## Propósito

Entienda qué hace realmente cada cartucho predeterminado antes de confiar en uno para trabajo real — unos minutos, y corrige dos fabricaciones reales que estaban antes en esta guía: F9 no es una interfaz de chat, y F12 no tiene un resultado de rechazo/cuarentena.

## Procedimiento

1. Reconozca que un Cartucho está compilado directamente en el binario `os-console` — no es un plugin, no es un subproceso. Presionar su tecla de función entrega el control a ese módulo registrado, que posee su propio renderizado y manejo de teclado hasta que cambie de ranura.

2. Use el Cartucho de Correo en **F3**: presione **F3**, lea la lista de la bandeja de entrada (recuentos de no leídos y resúmenes del remitente), navegue con las flechas, presione **Enter** para abrir un mensaje, y **c** para redactar. El correo saliente se enruta a través de `service-email`, no mediante una conexión SMTP directa.

3. Use el Cartucho SLM en **F9** por lo que realmente es: un panel de monitoreo en vivo, no una herramienta de consulta. Presione **F9** y lea sus cinco secciones — Gateway, Flota YoYo, DataGraph, Cola y Costo de hoy. Presione **R** para forzar una actualización inmediata en lugar de esperar al siguiente sondeo.

   > **Nota:** F9 no tiene ninguna entrada de tipo prompt — ni campo de texto, ni tecla de envío, ni respuesta en flujo. Si busca cómo ejecutar realmente una consulta de inferencia, véase [[run-first-slm-query]], que cubre la ruta real.

4. Use la Máquina de Entrada en **F12** por lo que realmente hace: es el punto de control de ingesta de archivos obligatorio de la plataforma, no una pantalla de revisión y aprobación de registros. Los archivos que entran por F12 tienen sus permisos de ejecución eliminados y son etiquetados antes de ser enrutados — esta es la única ruta por la que pueden entrar archivos externos en bruto a un Totebox.

   > **Advertencia:** un envío a través de F12 o bien tiene éxito (se muestra como Hecho, con un ID de carga útil y una posición en el libro mayor — ocasionalmente con una advertencia no fatal adjunta) o falla con un error genérico. No existe un resultado separado de "rechazar y poner en cuarentena" en este flujo — un envío rechazado simplemente se muestra como un error, no como un estado de cuarentena distinto.

## Resultado esperado

Sabe qué hace cada cartucho sin adivinar: F3 para correo, F9 para el estado de solo lectura de la pasarela de inferencia, F12 para el punto de control obligatorio de ingesta de archivos — y sabe que F9 no es donde se envía una consulta.

## Verificación

Abra cada uno de F3, F9 y F12 por turno. Confirme que lo que ve coincide con esta guía: una bandeja de entrada en F3, un panel de salud de cinco secciones sin campo de entrada en F9, y una interfaz de ingesta de archivos en F12.

## Reversión

Ver F3 o F9 no cambia nada. Un envío real en F12 no es reversible — véase [[explore-the-console]] para esa advertencia con más detalle antes de enviar algo a través de él.

## Próximos pasos

- [[run-first-slm-query]] — la manera real de enviar una consulta de inferencia, ya que F9 no lo es
- [[read-the-command-ledger]] — lea lo que F12 ha escrito, a través de la API HTTP real del libro mayor

## Véase también

- [[app-console-keys]] — arquitectura del chasis y el trait Cartridge que implementa cada ranura
- [[app-console-email]] — el Cartucho de Correo en detalle
- [[app-console-slm]] — el panel del Cartucho SLM en detalle
- [[app-console-input]] — la Máquina de Entrada en detalle
- [[navigate-console-tui]] — diseño general de la TUI y navegación de ranuras
