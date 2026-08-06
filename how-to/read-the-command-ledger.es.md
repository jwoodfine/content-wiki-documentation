---
schema: foundry-doc-v1
title: "Leer el libro mayor de comandos"
slug: read-the-command-ledger
short_description: "Lee el libro mayor WORM de solo anexado a través de la API HTTP real de service-fs — paginando entradas con un cursor y obteniendo un punto de control firmado — ya que no existe ninguna interfaz de navegación del libro mayor en la consola."
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
paired_with: read-the-command-ledger.md
---

## Requisitos previos

- Acceso de red a su instancia de `service-fs`
- Su identificador de módulo para la cabecera obligatoria `X-Foundry-Module-ID`

## Propósito

Lea el historial del libro mayor y obtenga un punto de control verificable a través de la API HTTP real de `service-fs` — un par de minutos. No existe ninguna pantalla de navegación del libro mayor en `os-console`; F12 solo muestra un indicador en línea de altura/raíz mientras un envío está en curso, no un historial que pueda recorrer.

## Procedimiento

1. Obtenga entradas desde un cursor, comenzando en 0 para el historial completo:

   ```bash
   curl -s -H "X-Foundry-Module-ID: <su-id-de-modulo>" \
     "http://<host-de-service-fs>/v1/entries?since=0"
   ```

   La cabecera es obligatoria — un `X-Foundry-Module-ID` ausente devuelve un 400, y uno no coincidente devuelve un 403. Cada entrada en la respuesta lleva un `cursor`, un `payload_id` y la propia `payload`.

2. Avance usando el propio campo `next_cursor` de la respuesta:

   ```bash
   curl -s -H "X-Foundry-Module-ID: <su-id-de-modulo>" \
     "http://<host-de-service-fs>/v1/entries?since=<next_cursor>"
   ```

   Repita hasta que la lista de entradas devuelta esté vacía — ese es el final del libro mayor al momento de su solicitud.

3. Obtenga el punto de control actual para anclar lo que acaba de leer:

   ```bash
   curl -s -H "X-Foundry-Module-ID: <su-id-de-modulo>" \
     "http://<host-de-service-fs>/v1/checkpoint"
   ```

   La respuesta lleva `tree_size` (la altura del libro mayor — el recuento total de entradas), `root_hash` (un hash SHA-256 de la punta, codificado en hexadecimal), `algorithm` (`"sha256"`), un `timestamp` y una `signature`.

   > **Nota:** `signature` solo está presente si la instancia de `service-fs` se inició con una clave de firma configurada. Un despliegue sin firmar devuelve `signature: null` — ese es un estado de configuración real y válido, no una respuesta rota.

## Resultado esperado

El conjunto completo de entradas del libro mayor desde su cursor inicial en adelante, más un punto de control que le da la altura actual del libro mayor y el hash raíz contra el cual verificarlas.

## Verificación

Confirme que el número de entradas que recorrió es coherente con el `tree_size` del punto de control en el momento en que lo obtuvo. Obtener entradas y el punto de control no son atómicos entre sí, así que una pequeña brecha por actividad entre las dos llamadas es esperada, no un error. Para un procedimiento completo paso a paso de verificación contra manipulación usando el hash y la firma del punto de control, véase [[verify-worm-ledger]] — esta guía cubre la lectura del libro mayor, no la demostración de que no ha sido alterado.

## Reversión

La lectura no es destructiva — no hay nada que deshacer. Volver a ejecutar cualquiera de las llamadas anteriores siempre es seguro.

## Próximos pasos

- [[verify-worm-ledger]] — verifique el hash y la firma de un punto de control contra las entradas que cubre
- [[run-first-slm-query]] — una ruta HTTP real separada, para inferencia en lugar de lecturas del libro mayor

## Véase también

- [[service-fs]] — la capa de almacenamiento WORM a la que pertenecen estos endpoints
- [[worm-ledger-architecture]] — qué cubre la garantía WORM y qué no
- [[app-console-input]] — la Máquina de Entrada F12 que escribe las entradas que está leyendo aquí
