---
schema: foundry-doc-v1
title: "Verificar una entrada del libro mayor WORM"
slug: verify-worm-ledger
short_description: "Verifica entradas del libro mayor WORM contra un punto de control obtenido a través de la API HTTP real de service-fs, usando un conjunto de herramientas SHA-256 estándar — no existe ni se necesita ninguna CLI ni herramienta propietaria."
category: how-to
index_group: records-storage
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Ingenieros (con acceso directo al terminal); operadores de cliente"
language: es
language_protocol: TRANSLATE-ES
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: verify-worm-ledger.md
---

## Requisitos previos

- Acceso de red a su instancia de `service-fs`
- Su identificador de módulo para la cabecera `X-Foundry-Module-ID`
- Una utilidad SHA-256 (`sha256sum` en Linux, `shasum -a 256` en macOS)

## Propósito

Confirme que una entrada del libro mayor no ha sido alterada desde que se escribió, usando solo `curl` y herramientas de hash estándar — no existe ninguna herramienta de verificación CLI ni propietaria para esto, y no se necesita ninguna.

## Procedimiento

1. Obtenga la entrada (o rango de entradas) que quiere verificar, según [[read-the-command-ledger]]:

   ```bash
   curl -s -H "X-Foundry-Module-ID: <su-id-de-modulo>" \
     "http://<host-de-service-fs>/v1/entries?since=<cursor>"
   ```

2. Obtenga el punto de control actual:

   ```bash
   curl -s -H "X-Foundry-Module-ID: <su-id-de-modulo>" \
     "http://<host-de-service-fs>/v1/checkpoint"
   ```

   El punto de control lleva `tree_size` (el recuento total de entradas en el momento en que se emitió), `root_hash` (un compromiso SHA-256 codificado en hexadecimal que cubre cada entrada hasta `tree_size`), `algorithm` (`"sha256"`), un `timestamp` y una `signature`.

3. Confirme que sus entradas obtenidas están cubiertas por el punto de control: sus cursores deben caer dentro de `tree_size`. Si el cursor de su entrada objetivo es mayor que el `tree_size` del punto de control, obtenga primero un punto de control más reciente.

4. Si el punto de control lleva una firma, verifíquela. `signature` contiene una firma Ed25519 sobre el cuerpo del signed-note C2SP (`origin`, `tree_size` y el `root_hash` codificado en base64), usando la clave de verificación publicada de la plataforma. Una firma válida significa que el estado de la cadena fue atestiguado en ese punto — independientemente de confiar en el servicio en vivo en el momento en que lo lee.

   > **Nota:** `signature` solo está presente si la instancia de `service-fs` se inició con una clave de firma configurada. El punto de control de un despliegue sin firmar sigue siendo una instantánea real y honesta de `tree_size`/`root_hash` — simplemente no lleva una atestación independiente de terceros. No trate una firma ausente como un error.

## Resultado esperado

Un punto de control cuyo `root_hash` y `tree_size` puede mantener de forma independiente como un compromiso con el estado del libro mayor en ese punto. Cuando hay una firma presente, además obtiene prueba criptográfica de que ese compromiso fue atestiguado, no simplemente afirmado por el servicio en ejecución.

## Verificación

Vuelva a obtener el punto de control más tarde y confirme que `tree_size` solo aumenta y que el `root_hash` para cualquier `tree_size` que haya visto antes nunca cambia. Una entrada cubierta por el `root_hash` de un punto de control anterior, que sigue presente y sin modificar bajo el `tree_size` mayor de un punto de control posterior, nunca ha sido alterada. Esa consistencia entre puntos de control a lo largo del tiempo es la verificación práctica y repetible disponible con solo estos dos endpoints.

## Reversión

La verificación es de solo lectura. Nada que deshacer.

## Próximos pasos

- [[read-the-command-ledger]] — el procedimiento de lectura de entradas contra el que verifica esta guía

## Véase también

- [[worm-ledger-architecture]] — qué cubre la garantía WORM y qué no
- [[service-fs]] — el servicio que implementa y sirve el libro mayor
