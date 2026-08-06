---
schema: foundry-doc-v1
title: "Abrir su primera sesión Totebox"
slug: open-first-totebox-session
short_description: "Abre una primera sesión Totebox en un único archivo: lea el manifiesto, revise su bandeja de entrada, entienda qué puede y no puede escribir la sesión, y complete el barrido de cierre antes de cerrar."
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
paired_with: open-first-totebox-session.md
---

## Requisitos previos

- Un dispositivo ya emparejado con el espacio de trabajo (véase [[pair-a-new-device]])
- Al menos un archivo Totebox al que su cuenta tenga acceso
- Un nivel de permiso suficiente para el trabajo que pretende realizar (véase [[personnel-permissions]])

## Propósito

Abra una sesión Totebox — el entorno de trabajo asistido por IA, con alcance a un único archivo — y entienda qué puede y no puede hacer antes de empezar. Toda tarea de desarrollo en la Orquestación Totebox comienza así, ya sea que colabore en el espacio de trabajo de desarrollo o se conecte como cliente a través de [[os-console]].

## Procedimiento

1. Identifique el archivo en el que va a abrir una sesión. Una sesión siempre tiene alcance a exactamente un archivo; no existe una sesión entre archivos.

2. Lea el manifiesto del archivo antes de hacer cualquier otra cosa. Contiene la misión del archivo, el estado de su [[totebox-orchestration-development|Tétrada]] (cuáles de las cuatro patas — vendor, customer, deployment y wiki — están activas) y su punto final de la pasarela de IA.

3. Revise la bandeja de entrada del archivo. Un recuento pendiente distinto de cero significa que otro archivo o sesión le ha dejado un mensaje — una decisión, un bloqueo o contexto que puede cambiar lo que hace esta sesión. Léalo antes de empezar a trabajar; archive cada mensaje como accionado una vez que lo haya atendido.

4. Confirme que su nivel de permiso cubre el trabajo por delante. Los niveles se aplican mediante emparejamientos, no mediante un rol que usted escribe — véase [[personnel-permissions]] para lo que alcanza cada nivel.

5. Trabaje dentro del alcance de la sesión (véase abajo). El límite es estructural, no una política que deba recordar seguir.

6. Antes de cerrar, ejecute el barrido de cierre:

   1. Actualice o cree el registro duradero de trabajo en curso del archivo para todo lo que siga abierto
   2. Anteponga cualquier mensaje saliente para otros archivos a la bandeja de salida
   3. Confirme los cambios sin confirmar en la rama de preparación del archivo

## Resultado esperado

Una sesión de trabajo con alcance a un único archivo: puede leer y escribir en los repositorios que ese archivo declara, su bandeja de entrada ha sido revisada, y cualquier solicitud entre archivos queda en cola como mensajes de salida en lugar de escrituras directas.

## Verificación

- Confirme que la sesión no puede escribir fuera de los repositorios declarados del archivo — esto se aplica de forma estructural, no por convención, así que un intento de escritura fuera del alcance falla en lugar de simplemente ser desalentado.
- Confirme que el recuento pendiente de la bandeja de entrada es cero, o que cada mensaje pendiente restante es uno que usted ha decidido aplazar deliberadamente, no que pasó por alto.
- Antes de terminar la sesión, confirme que `git status` no muestra nada sin confirmar que el barrido de cierre debería haber capturado.

## Reversión

Cerrar una sesión sin el barrido de cierre no es destructivo, pero deja trabajo sin preparar y sin documentar — la siguiente sesión (la suya o la de otra persona) comienza sin saber qué estaba en curso. No existe un "deshacer" independiente para un barrido omitido; la recuperación consiste en abrir una nueva sesión en el mismo archivo y ejecutar el barrido tarde, revisando `git status` y las propias notas de seguimiento del archivo para ver qué quedó abierto.

## Próximos pasos

- [[navigate-console-tui]] — trabaje en la consola una vez que su sesión esté abierta
- [[explore-the-console]] — un recorrido de primera vez por el diseño de la consola y las ranuras de teclas de función
- [[read-write-totebox-archives]] — el flujo completo de lectura/escritura para trabajar en un archivo

## Véase también

- [[totebox-session]] — la arquitectura completa: alcance de la sesión, la Tétrada y los niveles de permiso en profundidad
- [[pairing-as-permission]] — cómo se aplican los límites de acceso de la sesión
- [[os-console]] — el punto de entrada orientado al cliente que realiza la misma función
