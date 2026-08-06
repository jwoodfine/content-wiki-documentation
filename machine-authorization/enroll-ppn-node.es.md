---
schema: foundry-doc-v1
title: "Cómo inscribir un nodo PPN"
slug: enroll-ppn-node
short_description: "Inscribe una máquina en una flota de cómputo PPN estableciendo las tres variables de entorno obligatorias de service-vm-host, ejecutándolo bajo systemd y confirmando el nodo en el listado del controlador."
category: machine-authorization
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Ingenieros (con acceso directo al terminal); operadores de flota"
language: es
language_protocol: TRANSLATE-ES
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: enroll-ppn-node.md
---

## Requisitos previos

- El binario `service-vm-host` desplegado en la máquina que va a inscribir
- Alcance de red desde esa máquina hasta el controlador de flota en el puerto 9203 — el puerto del controlador está fijado en el código y no es configurable
- Un identificador de nodo único dentro de la flota
- La dirección IP de WireGuard del nodo
- systemd, u otro supervisor que reinicie un proceso caído

## Propósito

Registrar una máquina en `service-vm-fleet` iniciando en ella el agente de latido por nodo — unos cinco minutos, tras los cuales el nodo aparece en el listado del controlador dentro de un intervalo de latido.

## Procedimiento

1. Establezca las tres variables de entorno obligatorias de `service-vm-host`. El agente no tiene opciones de línea de comandos ni lee archivo de configuración alguno; se niega a arrancar si falta cualquiera de las tres:

   ```bash
   VM_FLEET_ENDPOINT=http://<fleet-controller-host>:9203
   VM_NODE_ID=<unique-node-identifier>
   VM_WG_IP=<node-wireguard-ip>
   ```

2. Opcional: sobrescriba cualquiera de los tres valores por defecto, todos ellos utilizables tal como vienen:

   | Variable | Valor por defecto | Efecto |
   |---|---|---|
   | `VM_HEARTBEAT_INTERVAL_S` | `10` | Segundos entre latidos hacia el controlador |
   | `VM_SPAWN_PORT` | `9204` | Puerto en el que escucha la API local del propio agente |
   | `VM_RESERVED` | `false` | Marca el nodo como último recurso a efectos de colocación |

3. Arranque `service-vm-host` bajo systemd, configurado para reiniciarse automáticamente ante un fallo. El agente empieza a enviar latidos a `POST /v1/nodes/heartbeat` de inmediato y no necesita ninguna llamada de registro previa.

4. Confirme que el nodo ha llegado al controlador:

   ```bash
   curl -s http://<fleet-controller-host>:9203/v1/nodes/<VM_NODE_ID>
   ```

## Resultado esperado

El nodo aparece en `GET /v1/nodes` y en `GET /v1/fleet` dentro de un intervalo de latido — diez segundos con el valor por defecto. Su registro contiene `node_id`, `hostname`, `wg_ip`, `ram_available_mb`, `vm_count`, `kvm_available`, `reserved` y `last_heartbeat` como marca de tiempo RFC3339.

## Verificación

```bash
curl -s http://<fleet-controller-host>:9203/v1/nodes    # listado completo de nodos
curl -s http://<fleet-controller-host>:9203/v1/fleet    # estado de toda la flota
```

Busque su `VM_NODE_ID` con un `last_heartbeat` que no sea más antiguo que un intervalo de latido. El registro de un nodo no tiene campo `status` — lo reciente que sea `last_heartbeat` es la única señal de vida que el controlador expone, y un nodo que deje de latir durante más de 30 segundos se elimina del listado por completo, en lugar de mostrarse como obsoleto o fuera de línea. Un nodo ausente de `/v1/nodes` es, por tanto, o bien un nodo nunca inscrito, o bien uno que lleva más de 30 segundos en silencio; la API no distingue entre ambos casos.

> **Nota:** `service-vm-fleet` no tiene ruta `/healthz`. Para confirmar que el propio controlador responde, llame a `GET /v1/fleet`.

> **Nota:** cada latido reemplaza íntegramente el registro que el controlador tiene de ese nodo — las VM y las estadísticas de recursos se sobrescriben, no se fusionan con el estado anterior.

> **Nota:** para inspeccionar una VM, liste las VM con `GET /v1/vms` (filtrando opcionalmente con `?tenant_id=`) y filtre del lado del cliente. `DELETE /v1/vms/:vm_id` existe, pero no hay ningún GET que devuelva una sola VM por su id.

> **Advertencia:** el estado de la flota reside únicamente en la memoria del controlador. Si el proceso del controlador se reinicia, todos los registros de nodos y de VM se pierden hasta que los nodos vuelvan a latir. Ni la inscripción ni el latido escriben entrada alguna en el libro mayor, de modo que un reinicio no deja constancia de lo que contenía la flota antes.

## Reversión

Detenga el proceso `service-vm-host`. Pasados unos 30 segundos sin latido, el controlador elimina el nodo de su listado por sí solo. No hace falta ninguna llamada de baja, y tampoco existe.

Volver a inscribirlo es el mismo procedimiento: arranque de nuevo el agente con el mismo `VM_NODE_ID` y el nodo reaparece en el siguiente latido.

## Próximos pasos

- [[add-a-fleet-node]] — el procedimiento complementario del lado de la flota
- [[service-vm-fleet]] — el modelo de estado del controlador y su superficie de rutas
- [[ppn-small-business-compute]] — la arquitectura de flota a la que este nodo se une
- [[os-infrastructure-ppn-node]] — la imagen de nodo construida en torno a este agente
