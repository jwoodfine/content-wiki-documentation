---
schema: foundry-doc-v1
title: "Escalar el acceso de usuarios"
slug: scale-user-tiers
short_description: "Otorga tokens de capacidad con alcance de rol a nuevos usuarios a medida que un equipo crece, usando la API real de emparejamiento de service-content — no existe una operación de promoción/degradación ni de revocación masiva, ya que no existe ningún mecanismo de revocación."
category: how-to
index_group: multi-entity-scale
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Ingenieros (con acceso directo al terminal); operadores de cliente"
language: es
language_protocol: TRANSLATE-ES
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: scale-user-tiers.md
---

## Requisitos previos

- Acceso a la instancia de `service-content` que emite tokens para su equipo
- Una lista de usuarios a añadir, con sus claves públicas o identificadores de dispositivo
- Familiaridad con [[issue-capability-token]], sobre el cual se basa esta guía directamente

## Propósito

Otorgue a los nuevos miembros del equipo un token con alcance de rol a medida que su despliegue crece — unos minutos por persona, o un bucle con script corto para todo un equipo a la vez. Esto no es un sistema de promoción de niveles: no hay actualización en el lugar y no hay revocación, así que lea esto antes de tratarlo como una consola de gestión de accesos.

## Procedimiento

> **Nota:** el conjunto real de roles es `User`, `Admin` e `Interface` — no una escala READ/USER/INPUT. Elija el rol que coincida con lo que la persona realmente necesita; no hay un nivel numérico para "promocionar" a alguien después, solo un token nuevo con un rol distinto.

1. Para cada usuario nuevo, emita un token con alcance al rol y los archivos que necesita:

   ```bash
   curl -s "http://<host-de-service-content>/v1/pair/token?role=<rol>&node_label=<etiqueta-de-usuario>&archive_scope=<archivo-a>,<archivo-b>"
   ```

   Véase [[issue-capability-token]] para la forma completa de la respuesta y el paso de registro que le sigue.

2. Para todo un equipo a la vez, recorra en bucle una lista de etiquetas y alcances en lugar de emitir uno por uno a mano:

   ```bash
   while IFS= read -r etiqueta; do
     curl -s "http://<host-de-service-content>/v1/pair/token?role=<rol>&node_label=$etiqueta&archive_scope=<archivo-a>"
   done < etiquetas-equipo.txt
   ```

3. Entregue cada token a su usuario. Registre lo que emitió — ya que no hay ningún endpoint de listado para los tokens ya emitidos, su propio registro es el único inventario que existe.

## Resultado esperado

Cada usuario nuevo tiene un token con alcance exacto al rol y los archivos que necesita, válido durante 24 horas desde su emisión.

## Verificación

Confirme el acceso de un usuario nuevo haciendo que realice una solicitud usando su token contra una ruta protegida por capacidad, según los pasos de verificación de [[issue-capability-token]].

## Reversión

> **Advertencia:** no hay manera de promocionar el token existente de un usuario en el lugar, y no hay manera de revocar un token que emitió por error. Si otorgó el rol o alcance equivocado, la solución es emitir un token corregido y hacer que el usuario cambie a él — el original sigue funcionando hasta su propia expiración de 24 horas de todos modos. Planifique la incorporación del equipo teniendo esto en cuenta: acierte con el rol y el alcance en el momento de la emisión, ya que corregirlo después no elimina la concesión original.

## Próximos pasos

- [[issue-capability-token]] — el procedimiento completo de emisión y registro de un solo token
- [[rotate-keys]] — qué significa realmente la "rotación" en este sistema, y sus límites honestos

## Véase también

- [[machine-based-auth]] — el modelo de autorización en el que operan los tokens
- [[configure-tenant-namespace]] — un sistema separado y no relacionado para cuotas de VM a nivel de tenant, no roles de usuario
