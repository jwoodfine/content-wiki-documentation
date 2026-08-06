---
schema: foundry-doc-v1
title: "Ejecutar su primera consulta SLM"
slug: run-first-slm-query
short_description: "Envía una primera solicitud de inferencia directamente a Doorman por HTTP — la ruta real, ya que la ranura F9 de la consola es un panel de monitoreo sin ninguna interfaz de consulta."
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
paired_with: run-first-slm-query.md
---

## Requisitos previos

- El servicio SLM local y Doorman en ejecución y accesibles (véase [[run-local-slm-inference]])
- `curl`, o el script de referencia en `service-slm/scripts/slm-chat.sh` si lo tiene disponible
- Su identificador de módulo para la cabecera `X-Foundry-Module-ID`

## Propósito

Envíe una primera solicitud de inferencia y obtenga una respuesta — menos de un minuto una vez que Doorman esté activo. Esta no es una tarea de consola: F9 en `os-console` es un panel de salud de solo lectura sin manera de escribir o enviar una consulta, así que la ruta real es una llamada HTTP directa a Doorman.

## Procedimiento

1. Confirme que Doorman es accesible. La dirección local predeterminada es `http://127.0.0.1:9080`, aunque su despliegue puede diferir.

2. Envíe una solicitud al endpoint de finalización de chat:

   ```bash
   curl -s -X POST \
     -H "Content-Type: application/json" \
     -H "X-Foundry-Module-ID: <su-id-de-modulo>" \
     -d '{"messages": [{"role": "user", "content": "Di hola en una oración."}]}' \
     http://127.0.0.1:9080/v1/chat/completions
   ```

   Las cabeceras son flexibles en desarrollo: Doorman genera valores predeterminados seguros cuando están ausentes, específicamente para que sondeos ad hoc con curl como este funcionen sin configuración adicional. Aun así, establezca `X-Foundry-Module-ID` explícitamente una vez que haga trabajo real — así es como la plataforma atribuye el uso a su módulo.

3. Lea la respuesta. Llega como una única carga útil JSON, no como un flujo — toda la respuesta llega en un campo `content` una vez que el modelo termina, no palabra por palabra.

   > **Nota:** existe un script REPL de referencia en `service-slm/scripts/slm-chat.sh` que envuelve esta misma llamada en un bucle, para que pueda mantener una conversación sin volver a escribir las cabeceras cada vez. A pesar de lo que afirma una nota interna antigua, ese script tampoco transmite en flujo — es la misma llamada bloqueante por turno, simplemente repetida en bucle.

## Resultado esperado

Una respuesta JSON que contiene la respuesta del modelo en su campo `content`, devuelta como una única carga útil completa.

## Verificación

Confirme que el campo `content` de la respuesta contiene una respuesta real y pertinente en lugar de un cuerpo de error. Un estado de error HTTP o un campo `error` en el JSON significa que Doorman no pudo completar la solicitud — verifique que el servicio SLM local esté realmente en ejecución antes de reintentar.

> **Nota:** no necesita que ningún nivel de inferencia específico esté "activo" para que esto funcione. Doorman dirige las solicitudes ordinarias al nivel local por defecto; un nivel superior solo entra en juego para solicitudes explícitamente marcadas como de alta complejidad, e incluso entonces recae automáticamente en el nivel local en caso de fallo en lugar de hacer fallar su solicitud.

## Reversión

Nada que revertir — una consulta es de solo lectura contra su propio historial de conversación. Enviar otra solicitud no requiere deshacer la anterior.

## Próximos pasos

- [[read-the-command-ledger]] — lea el historial de actividad de la plataforma a través de su propia API HTTP real
- [[use-f-key-model]] — qué muestra realmente F9, ahora que sabe que no es ahí donde van las consultas

## Véase también

- [[run-local-slm-inference]] — inicie el servicio SLM local y Doorman en un despliegue nuevo
- [[doorman-protocol]] — el modelo de enrutamiento y disyuntor de circuito de Doorman
- [[slm-stack-architecture]] — la pila de inferencia completa y las definiciones de nivel
