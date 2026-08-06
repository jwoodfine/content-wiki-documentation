---
schema: foundry-doc-v1
title: "Cómo autenticar las descargas de binarios"
slug: authenticate-binary-downloads
short_description: "Autentica una versión de software.pointsav.com: confirmar el pedido en cadena, seguir el enlace de descarga que acuña un token Ed25519 y entender en qué punto ocurre realmente la verificación."
category: machine-authorization
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Ingenieros (con acceso directo al terminal); operadores de cliente"
language: es
language_protocol: TRANSLATE-ES
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: authenticate-binary-downloads.md
---

## Requisitos previos

- El hash de transacción de su pago en USDC sobre Polygon, si realizó un pedido de pago
- Un navegador, o `curl` configurado para seguir redirecciones
- Nada más — no hace falta ninguna herramienta local de verificación, archivo de clave ni utilidad de firma

## Propósito

Obtener una versión de `software.pointsav.com` a través de la ruta de descarga firmada, y entender qué parte de esa ruta autentica realmente el archivo — unos dos minutos una vez que su pago se ha confirmado en cadena.

> **Nota:** todos los productos actualmente listados tienen precio de 0 $ durante el periodo BETA y hoy no requieren licencia ni pago. La ruta de pedido y token que se describe abajo es código en funcionamiento y es la que usará un pedido de pago, pero por ahora puede descargar cualquier versión vigente sin pasar por un pedido de pago en absoluto. Los pasos 1 y 2 solo son aplicables si ha realizado uno.

## Procedimiento

1. Abra la página de su pedido en `https://software.pointsav.com/order/<tx_hash>`, donde `<tx_hash>` es el hash de transacción de su pago. El pedido figura como pendiente hasta que `tool-wallet` confirma el pago en cadena.

2. Recargue la página una vez llegue la confirmación. Aparece un código de recibo — un identificador determinista derivado de la transacción. Consérvelo para sus registros; ningún paso de la descarga lo pide, y no es una credencial de descarga.

3. Siga el enlace de descarga en `https://software.pointsav.com/order/<tx_hash>/download`. Esa petición acuña un token nuevo firmado con Ed25519 y redirige directamente a la descarga de la versión, con el token ya incorporado como parámetro de la URL. No hay ningún token aparte que copiar.

4. Deje que la descarga termine. El servicio de versiones verifica la firma Ed25519 del token del lado del servidor antes de transmitir un solo byte, así que no hay ningún comando de verificación que ejecutar después en su equipo.

5. Opcional: acceda a una versión directamente en lugar de hacerlo a través de una página de pedido, usando el patrón de URL de versiones:

   ```text
   https://software.pointsav.com/releases/<product>/<version>/<platform>
   https://software.pointsav.com/releases/<product>/latest/<platform>
   ```

   La forma `latest` redirige a la versión vigente ya resuelta.

## Resultado esperado

Usted tiene el archivo de la versión, y el hecho de tenerlo es la prueba de que su token de descarga se verificó: una petición con un token ausente, mal formado o mal firmado no produce archivo alguno. El formato de transmisión del token es `base64url(signature || payload_json)`, sin relleno, y se comprueba con Ed25519 en el servidor antes de que empiece el cuerpo de la respuesta.

## Verificación

Confirme que ha recibido un archivo de versión y no una página de error — compruebe el tamaño y el tipo del archivo frente a lo que anunciaba la página de la versión. La comprobación de firma ya ha ocurrido a esas alturas; no es un paso que usted repita localmente.

Para inspeccionar de forma independiente la clave pública de firma de la plataforma, el servicio de versiones la publica en `/verify-key.pub` como una cadena hexadecimal simple: 32 bytes en bruto, 64 caracteres hexadecimales.

> **Advertencia:** esa ruta no es alcanzable hoy a través del dominio público `software.pointsav.com`. El servicio subyacente la sirve correctamente, pero un fallo de enrutamiento delante del dominio público hace que una petición a esa ruta no llegue al manejador. Considere la recuperación independiente de la clave como no disponible sobre el dominio público mientras ese enrutamiento no se corrija.

## Reversión

Descargar no cambia nada en el servidor ni nada en su equipo más allá del archivo que ha obtenido, así que no hay nada que revertir. Elimine el archivo y empiece de nuevo desde el paso 3 si una descarga queda incompleta o corrupta.

No reutilice una URL de descarga guardada de una sesión anterior. El token se acuña de nuevo en cada visita al enlace de descarga de la página del pedido, de modo que un enlace caducado se arregla volviendo a la página del pedido, no editando la URL.

## Próximos pasos

- [[self-host-a-deployment]] — arranque una imagen de appliance una vez que la tenga
- [[private-git-paid-customer-endpoint]] — la arquitectura de pedidos y distribución que hay detrás de estas URL
- [[software-distribution-substrate]] — cómo se entregan las versiones de binarios firmados
