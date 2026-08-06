---
schema: foundry-doc-v1
title: "Cómo emitir un token de capacidad"
slug: issue-capability-token
short_description: "Emite desde service-content un token de emparejamiento firmado con Ed25519 sobre HTTP plano, lo registra en el par receptor y explica la cabecera X-Foundry-Capability, que es una credencial aparte."
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
paired_with: issue-capability-token.md
---

## Requisitos previos

- Una instancia de `service-content` en ejecución y alcanzable por HTTP, con su par de claves Ed25519 persistente en disco
- `curl` o un cliente HTTP equivalente — no existe herramienta de línea de comandos para ninguna parte de este procedimiento
- La cadena de rol que pretende conceder
- Opcionalmente, una etiqueta de nodo y una lista de alcance de archivos separada por comas para acotar el token
- El endpoint `POST /v1/pair` del par receptor, accesible desde donde vaya a registrarse

## Propósito

Acuñar en `service-content` un token de emparejamiento firmado con Ed25519 y registrarlo en un servicio par, de modo que ambos puedan autenticarse entre sí sobre HTTP — unos cinco minutos.

## Procedimiento

> **Advertencia:** no existe mecanismo de revocación para ninguno de los dos tipos de token descritos aquí. Un token emitido está vivo durante sus 24 horas completas y nada lo invalida antes. Acote cada token tanto como el trabajo lo permita antes de emitirlo.

1. Solicite un token de emparejamiento al servicio emisor. `node_label` y `archive_scope` son opcionales; `role` no lo es:

   ```bash
   curl -s 'http://<service-content-host>/v1/pair/token?role=<role>&node_label=<label>&archive_scope=<archive-a>,<archive-b>'
   ```

2. Lea la respuesta, un JSON con dos campos:

   ```json
   {"token": "<signed-token>", "public_key": "<issuer-public-key>"}
   ```

3. Opcional: decodifique el token para confirmar qué acaba de emitir. El formato de transmisión es `<base64url(payload_json)>.<base64url(ed25519_signature)>`, de modo que decodificar en base64url el primer segmento separado por el punto devuelve la carga útil: `issuer`, `role`, `nonce`, `expiry`, `archive_scope` y `peer_type`.

4. Anote la caducidad. Se fija 24 horas después de la emisión, y es lo único que pone fin en algún momento a la validez del token.

5. Registre el token en el par receptor. Este es el paso que crea el emparejamiento — la llamada la hace la otra parte, no el emisor:

   ```bash
   curl -s -X POST http://<peer-host>/v1/pair \
     -H 'Content-Type: application/json' \
     -d '{"token":"<signed-token>","public_key":"<issuer-public-key>","node_label":"<label>"}'
   ```

   El servicio receptor verifica la firma contra la clave pública suministrada y deja constancia del emparejamiento.

6. Envíe las llamadas posteriores a rutas protegidas por capacidad con la cabecera `X-Foundry-Capability`:

   ```bash
   curl -s -H 'X-Foundry-Capability: <capability-value>' http://<host>/<capability-gated-path>
   ```

## Resultado esperado

El par receptor conserva un emparejamiento registrado cuya firma ha verificado, y que caduca 24 horas después de la emisión del token. Las peticiones que llevan una cabecera `X-Foundry-Capability` bien formada, correctamente firmada y en vigor llegan a su manejador en las rutas protegidas.

## Verificación

Confirme primero el token de emparejamiento, antes de registrarlo: decodifique en base64url el segmento de carga útil y compruebe que `role`, `archive_scope` y `expiry` coinciden con lo que pidió. Un token cuyo `archive_scope` sea más amplio de lo previsto no puede acotarse después de emitido ni puede retirarse.

Confirme la cabecera de capacidad usándola. Ejercite con ella una ruta protegida por capacidad y compruebe que la petición llega al manejador; una cabecera ausente, mal formada, mal firmada o caducada se rechaza en la puerta, antes de que el manejador se ejecute. No hay endpoint de verificación dedicado — la propia puerta es la comprobación.

> **Nota:** las dos credenciales son realmente distintas, no una sola credencial con dos nombres. El token de emparejamiento establece el emparejamiento y transporta `issuer`/`role`/`nonce`/`expiry`/`archive_scope`/`peer_type`. La cabecera `X-Foundry-Capability` acredita la identidad en cada llamada posterior y transporta `from_instance`, `user_scope`, `archive_scope`, `nonce`, `expiry`, `peer_type` y un `forwarded_for` opcional. Comparten la forma de carga útil en base64url más firma Ed25519, y nada más.

> **Nota:** hoy son exactamente dos las rutas de la API protegidas por la cabecera de capacidad. El resto de rutas del servicio no la comprueban, de modo que la presencia de la cabecera no constituye un control de acceso de propósito general sobre toda la API.

## Reversión

No hay nada que revertir ni forma alguna de deshacer una emisión. Un token que no pretendía crear sigue siendo válido durante lo que le reste de sus 24 horas; emitir un sustituto no lo altera.

La única actuación que deja un token emitido permanentemente inservible antes de su caducidad es un cambio en el par de claves subyacente del servicio firmante, algo que ocurre únicamente si se elimina su archivo de clave persistido y el servicio se reinicia. Es una acción manual de operador, no es una funcionalidad soportada, e invalida todos los tokens y emparejamientos que ese servicio haya firmado alguna vez, no solo el que lamenta haber emitido. [[rotate-keys]] describe en qué consiste realmente la sustitución dadas estas restricciones.

## Próximos pasos

- [[rotate-keys]] — sustituya una credencial dentro del modelo de caducidad de 24 horas
- [[service-content]] — el servicio que emite y verifica estos tokens
- [[capability-based-security]] — el modelo de autorización que hay detrás de la cabecera
