---
schema: foundry-doc-v1
title: "Añadir un nodo a una flota en funcionamiento"
slug: add-a-fleet-node
short_description: "Añade un segundo nodo a una flota PPN ya en funcionamiento usando la configuración real por variables de entorno de service-vm-host — el mismo mecanismo que el primer nodo, ya que nada cambia en la inscripción una vez que existe una flota."
category: how-to
index_group: multi-entity-scale
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Ingenieros (con acceso directo al terminal); operadores de flota"
language: es
language_protocol: TRANSLATE-ES
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: add-a-fleet-node.md
---

## Requisitos previos

- Al menos un nodo ya inscrito y emitiendo latidos (véase [[enroll-ppn-node]])
- Una segunda máquina con `service-vm-host` desplegado
- Un `VM_NODE_ID` que no coincida con ningún nodo ya en la flota

## Propósito

Inscriba un segundo nodo (o un tercero, o el enésimo) en una flota que ya está en funcionamiento — unos minutos, y es exactamente el mismo procedimiento que inscribir el primer nodo. No existe ningún mecanismo separado de "añadir a una flota en funcionamiento"; el controlador de la flota acepta nodos nuevos en cualquier momento sin perturbar los existentes.

## Procedimiento

1. Verifique los IDs de nodo actuales de la flota existente para que el suyo no colisione:

   ```bash
   curl -s http://<host-del-controlador-de-flota>:9203/v1/nodes
   ```

   El controlador de la flota no rechaza nada en el momento de la inscripción basándose en el nombre — pero reutilizar un ID simplemente significaría que los latidos del nodo nuevo sobrescriben el registro del nodo existente, no un rechazo limpio. Elija un `VM_NODE_ID` genuinamente distinto.

2. En la máquina nueva, establezca las mismas tres variables de entorno requeridas que en cualquier inscripción de nodo:

   ```bash
   VM_FLEET_ENDPOINT=http://<host-del-controlador-de-flota>:9203
   VM_NODE_ID=<nuevo-id-de-nodo-unico>
   VM_WG_IP=<ip-wireguard-del-nuevo-nodo>
   ```

3. Inicie `service-vm-host` bajo systemd, como con cualquier nodo. Comienza a emitir latidos de inmediato — sin llamada de registro, y sin necesidad de reiniciar el controlador ni ningún nodo existente.

## Resultado esperado

El nodo nuevo aparece en el listado del controlador de la flota junto a cada nodo existente, cada uno emitiendo latidos de forma independiente, en el plazo de un intervalo de latido (10 segundos por defecto).

## Verificación

```bash
curl -s http://<host-del-controlador-de-flota>:9203/v1/nodes
```

Confirme que su nuevo `VM_NODE_ID` aparece con un `last_heartbeat` reciente, y confirme que cada nodo que existía previamente sigue presente y emitiendo latidos también — añadir un nodo no toca el estado de ningún otro nodo.

## Reversión

Detenga el proceso `service-vm-host` del nodo nuevo. Sale del listado de la flota por sí solo tras aproximadamente 30 segundos sin latido — sin paso de eliminación separado, y sin efecto sobre el resto de la flota.

## Próximos pasos

- [[enroll-ppn-node]] — el mismo procedimiento en detalle, incluyendo cada variable de entorno y su valor predeterminado
- [[configure-tenant-namespace]] — configure cuotas para los tenants que colocan VMs en esta flota ampliada

## Véase también

- [[service-vm-fleet]] — la tabla de rutas real y el modelo de estado del controlador de la flota
- [[ppn-small-business-compute]] — la arquitectura de flota a la que se une este nodo
