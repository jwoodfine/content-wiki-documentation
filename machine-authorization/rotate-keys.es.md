---
schema: foundry-doc-v1
title: "Cómo rotar claves y tokens de capacidad"
slug: rotate-keys
short_description: "Sustituye una credencial de service-content dentro de los límites reales del sistema: los tokens caducan según un reloj fijo de 24 horas, el solapamiento es inevitable y ningún mecanismo acorta la vida de un token en vigor."
category: machine-authorization
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Ingenieros (con acceso directo al terminal); operadores de servicios"
language: es
language_protocol: TRANSLATE-ES
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: rotate-keys.md
---

## Requisitos previos

- Familiaridad con [[issue-capability-token]], que cubre el formato de transmisión, las dos formas de carga útil y la llamada de emisión — esta guía no los repite
- Acceso HTTP a la instancia emisora de `service-content`
- La hora de emisión de la credencial que va a sustituir, o su campo `expiry` decodificado

## Propósito

Sustituir una credencial de capacidad en vigor por otra nueva — unos cinco minutos de trabajo, tras los cuales la credencial sustituida sigue siendo válida durante lo que le reste de sus propias 24 horas.

## Procedimiento

> **Advertencia:** en este sistema no existe ninguna operación de revocación, borrado o invalidación. La secuencia de emitir la nueva y retirar la antigua no está disponible. Planifique el cambio dando por hecho que la credencial antigua seguirá funcionando hasta que su reloj se agote.

1. Decodifique la carga útil de la credencial que va a sustituir y lea su `expiry`. Esa marca de tiempo cae 24 horas después de la emisión y es el momento en que la credencial antigua deja de funcionar.

2. Solicite un token de sustitución con el mismo rol y el mismo alcance que quiera conservar:

   ```bash
   curl -s 'http://<service-content-host>/v1/pair/token?role=<role>&node_label=<label>&archive_scope=<archive-a>,<archive-b>'
   ```

3. Registre la sustitución en el par receptor:

   ```bash
   curl -s -X POST http://<peer-host>/v1/pair \
     -H 'Content-Type: application/json' \
     -d '{"token":"<new-token>","public_key":"<issuer-public-key>","node_label":"<label>"}'
   ```

4. Apunte el servicio llamante a la nueva credencial y confirme que su siguiente petición tiene éxito antes de dejar de usar la antigua.

5. Deje que la credencial antigua caduque por su propio reloj. Ninguna actuación posterior lo acorta.

## Resultado esperado

Hay dos credenciales válidas a la vez: la nueva durante las próximas 24 horas, y la antigua hasta el `expiry` que leyó en el paso 1. El solapamiento es una propiedad del sistema, no una ventana de transición que usted configure, y no se puede acortar.

## Verificación

Confirme que la nueva credencial funciona ejercitando con ella una ruta protegida por capacidad y comprobando que la petición llega a su manejador.

Confirme la retirada de la credencial antigua leyendo su campo `expiry`, no probando si es rechazada. Probar la credencial antigua antes de esa marca de tiempo la mostrará superando la puerta — ese es el resultado esperado, no una rotación fallida.

## Reversión

La rotación puede repetirse sin riesgo y también abandonarse sin riesgo. Solicitar otro token no altera ningún token ya emitido, y la credencial que estaba sustituyendo sigue siendo válida hasta su caducidad, de modo que volver a apuntar el llamante hacia ella restaura exactamente el estado anterior.

## Próximos pasos

- [[issue-capability-token]] — la llamada de emisión, las dos formas de carga útil y la decisión de alcance
- [[service-content]] — el servicio que firma y verifica estas credenciales
- [[capability-based-security]] — el modelo de autorización dentro del cual operan estos tokens

## Limitaciones conocidas, tal como está construido (2026-08-06)

- **No hay invalidación por token.** Si se sospecha que una credencial está comprometida, nada en este sistema detiene ese token concreto antes de su caducidad de 24 horas.
- **El único recurso inmediato afecta a todo el servicio.** Regenerar el propio par de claves de firma del servicio emisor — eliminando su archivo de clave persistido y reiniciando el servicio — sí invalida la credencial comprometida, junto con todos los demás tokens y emparejamientos que ese servicio haya firmado. No hay comando para hacerlo, no es una operación documentada ni soportada, y no constituye un procedimiento de rotación.
- **Acote con precisión en el momento de la emisión.** Como el reloj de 24 horas es el único control disponible, el `archive_scope` y el `role` elegidos al emitir son el límite práctico del alcance de una credencial comprometida.
