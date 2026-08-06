---
schema: foundry-doc-v1
title: "Cómo emparejar un dispositivo nuevo"
slug: pair-a-new-device
short_description: "Empareja un dispositivo os-console todavía sin emparejar con la malla PPN: leer el código de emparejamiento en la pantalla de arranque, conseguir que un administrador lo apruebe y confirmar la admisión en la red."
category: machine-authorization
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Ingenieros (con acceso directo al terminal); administradores de red"
language: es
language_protocol: TRANSLATE-ES
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: pair-a-new-device.md
---

## Requisitos previos

- Un dispositivo que ejecute `os-console` y que todavía no se haya emparejado — la autorización basada en máquina permanece inactiva en él (véase [[machine-based-auth]])
- Un par de claves WireGuard presente en ese dispositivo; el cliente envía su clave pública como parte de la solicitud de incorporación
- Alcance de red desde el dispositivo hasta su servidor de emparejamiento, puerto 9205 por defecto
- Un administrador que pueda alcanzar ese mismo servidor de emparejamiento y ejecutar `os-network-admin`
- Un identificador de nodo con la forma `<username>@<tenant>` para el dispositivo

## Propósito

Registrar un dispositivo sin emparejar en `service-ppn-pairing` para que un administrador pueda aprobar su entrada en la malla WireGuard — unos cinco minutos de trabajo efectivo repartidos entre dos personas, más una espera de duración indeterminada entre la aprobación y el alcance real por red.

## Procedimiento

### En el dispositivo que se va a emparejar

1. Inicie `os-console` en el dispositivo sin emparejar. La pantalla de emparejamiento se abre automáticamente al arrancar y ocupa la pantalla entera hasta que el dispositivo queda emparejado; no hay ruta de menú ni tecla F que llegue a ella.

2. Lea en pantalla el código de emparejamiento de ocho caracteres. Se muestra como `XXXX-XXXX` y procede del juego de caracteres Crockford base32 `0123456789ABCDEFGHJKMNPQRSTVWXYZ` — la I, la L, la O y la U no figuran en él, así que un código dictado en voz alta no arrastra ninguna ambigüedad entre O y 0 ni entre I y 1.

3. Opcional: escanee el bloque QR situado junto al código en lugar de transcribirlo. El QR codifica `PAIR:<code>` con el guion eliminado, y se dibuja como imagen de píxeles en los terminales compatibles con los protocolos gráficos Kitty o Sixel, o como imagen de medios bloques Unicode en el resto.

4. Entregue el código a su administrador antes de que pasen 600 segundos. El código caduca diez minutos después de emitirse, y a partir de ahí el cliente debe enviar una solicitud de incorporación nueva.

5. Deje el dispositivo en la pantalla de emparejamiento. El cliente consulta su estado cada dos segundos y no abandonará esa pantalla hasta que la consulta devuelva aprobado, denegado o caducado.

### En la estación de trabajo del administrador

6. Inicie `os-network-admin`. Consulta la lista de solicitudes pendientes cada cinco segundos e imprime cada solicitud con su código, su ID de nodo, su `bottom` (sustrato de destino) y su `arch`.

7. Compare el código impreso con el código leído en la pantalla del dispositivo. Esta comparación es la única verificación de identidad de todo el flujo — los propios endpoints no realizan ninguna.

   > **Advertencia:** los endpoints de aprobación y denegación no incorporan comprobación alguna de control de acceso. Cualquiera que alcance el puerto del servidor de emparejamiento y disponga de un código válido puede aprobar o denegar una solicitud. El acceso de red al puerto 9205 constituye la totalidad del límite de seguridad de este mecanismo; ubique el servidor de emparejamiento y configure su cortafuegos partiendo de esa base.

8. Apruebe la solicitud con el comando curl que `os-network-admin` imprime junto a ella:

   ```bash
   curl -s -X POST http://<pairing-server>:9205/v1/node-join/approve \
     -H 'Content-Type: application/json' \
     -d '{"code":"XXXX-XXXX"}'
   ```

   Para rechazar la solicitud en lugar de aprobarla, envíe un cuerpo con la misma forma a `/v1/node-join/deny`.

9. Espere a que la admisión en la malla se ejecute por separado. La aprobación añade un registro — ID de nodo, clave pública WireGuard, `bottom`, `arch` y una marca de tiempo de aprobación — a un archivo del servidor de emparejamiento. No pone el dispositivo en la red. Un proceso en segundo plano consulta el controlador de flota cada 30 segundos y ejecuta el comando de WireGuard que admite al par solo una vez que el nodo aprobado ha aparecido además en la flota de cómputo.

## Resultado esperado

La pantalla de emparejamiento del dispositivo pasa al estado Aprobado, la solicitud desaparece de la lista de pendientes y el registro de aprobación queda escrito en disco en el servidor de emparejamiento. Aprobado y alcanzable son dos estados distintos: el dispositivo solo resulta alcanzable en la malla después de que el sondeo de admisión de 30 segundos lo haya visto en la flota y haya ejecutado WireGuard.

## Verificación

En el dispositivo: la pantalla pasa a Aprobado en torno a dos segundos después de la aprobación, en la siguiente consulta de estado.

Del lado del administrador, confirme que la solicitud ha salido de la cola:

```bash
curl -s http://<pairing-server>:9205/v1/node-join/pending
```

Una solicitud aprobada no figura en esa respuesta. Ninguna de las dos comprobaciones demuestra alcance por red — ese es un estado posterior e independiente, producido por el proceso de admisión descrito en el paso 9.

> **Nota:** el campo `bottom` de la solicitud de incorporación se deriva de la arquitectura del dispositivo, no se elige — `aarch64` se corresponde con `seL4`, y `x86_64` con `netbsd-compat`. Tampoco hay nivel de acceso, rol ni nivel de permiso en ningún punto de este flujo. La admisión en la red es lo único que concede este mecanismo.

## Reversión

Antes de la aprobación: envíe el código a `/v1/node-join/deny`, o no haga nada y deje que la caducidad de 600 segundos cierre la solicitud.

Después de la aprobación: hoy no existe ningún comando integrado para deshacer el emparejamiento. Retirar un dispositivo emparejado implica pedir a su administrador que elimine manualmente el par de WireGuard del lado de la malla — no hay endpoint de revocación ni acción de consola que deshaga una aprobación.

## Próximos pasos

- [[navigate-console-tui]] — trabaje con la consola una vez que la pantalla de emparejamiento la libera
- [[machine-based-auth]] — el modelo de autorización que este emparejamiento activa
- [[enroll-ppn-node]] — inscriba la máquina en una flota de cómputo, un procedimiento distinto del emparejamiento de malla
