---
schema: foundry-doc-v1
title: "Cómo añadir un nodo a una flota en funcionamiento"
slug: add-a-fleet-node
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
language: es
language_protocol: TRANSLATE-ES
paired_with: add-a-fleet-node.md
---

Una flota en funcionamiento tiene uno o más nodos PPN ya inscritos y enviando latidos activamente. Añadir un nodo a una flota en funcionamiento significa inscribir una nueva máquina sin interrumpir la operación de los nodos existentes. Esta guía cubre los pasos específicos para añadir a una flota activa, a diferencia de inscribir el primer nodo.

Para el procedimiento inicial de inscripción de nodos, véase [[enroll-ppn-node]]. Para el servicio controlador de flota, véase [[service-vm-fleet]].

## Requisitos previos

- Al menos un nodo ya inscrito y el controlador de flota en ejecución (véase [[enroll-ppn-node]])
- Una segunda máquina preparada con `service-vm-host` instalado
- Un nuevo `NODE_ID` único que no entre en conflicto con ningún nodo existente en el espacio de nombres del tenant

## Paso 1: Verificar el estado actual del controlador de flota

Antes de añadir un nodo, confirme que la flota existente esté saludable:

```
curl -s "http://<host-controlador-flota>:9203/v1/vms?tenant_id=<su-tenant-id>"
```

Todos los nodos existentes deben mostrar una marca de tiempo `last_heartbeat` reciente (dentro de los últimos 60 segundos con la configuración predeterminada). Un nodo que muestra un latido obsoleto tiene un problema de conectividad — resuélvalo antes de añadir un nuevo nodo para evitar confundir el algoritmo de colocación recomendada.

## Paso 2: Elegir un ID de nodo que no entre en conflicto

El controlador de flota rechaza los valores de `NODE_ID` duplicados dentro de un espacio de nombres de tenant. Liste los IDs actuales:

```
curl -s "http://<host-controlador-flota>:9203/v1/vms?tenant_id=<su-tenant-id>" \
  | jq '.[].node_id'
```

Elija un ID para el nuevo nodo que siga el patrón de nomenclatura de los nodos existentes (p.ej., si los nodos existentes son `compute-west-01` y `compute-west-02`, nombre el nuevo `compute-west-03`).

## Paso 3: Configurar e iniciar el agente de latido en la nueva máquina

En la nueva máquina, establezca la configuración e inicie `service-vm-host`:

```
FLEET_CONTROLLER_URL=http://<host-controlador-flota>:9203
TENANT_ID=<su-tenant-id>
NODE_ID=<nuevo-id-único>

service-vm-host --controller $FLEET_CONTROLLER_URL --tenant $TENANT_ID --node-id $NODE_ID
```

El agente se registra en su primer latido. El controlador de flota actualiza sus datos de colocación recomendada automáticamente — no se requiere reiniciar el controlador ni otros nodos.

## Paso 4: Verificar que el nuevo nodo aparece en la flota

Consulte la flota nuevamente y confirme que el nuevo nodo aparece junto a los existentes:

```
curl -s "http://<host-controlador-flota>:9203/v1/vms?tenant_id=<su-tenant-id>"
```

La respuesta ahora debe incluir el nuevo nodo con un `last_heartbeat` de los últimos 60 segundos.

## Paso 5: Confirmar la distribución de carga

El algoritmo de colocación recomendada del controlador de flota equilibra las nuevas colocaciones de VM de tenants entre los nodos saludables. Después de añadir un nodo, envíe una nueva solicitud de colocación de VM y verifique que el controlador considere el nuevo nodo como candidato:

```
curl -s "http://<host-controlador-flota>:9203/v1/placement?tenant_id=<su-tenant-id>"
```

La respuesta sugiere un nodo de destino basado en la capacidad actual. Si el nuevo nodo no aparece como candidato, verifique que sus campos de capacidad informados estén poblados (memoria, CPU) en los datos del latido.

## Puntos clave

- El controlador de flota acepta nuevos nodos sin requerir que los nodos existentes se reinicien
- Los valores de `NODE_ID` duplicados dentro de un espacio de nombres de tenant son rechazados — verifique los IDs actuales antes de elegir uno
- La colocación recomendada se actualiza automáticamente cuando llega el primer latido de un nuevo nodo
- Un latido obsoleto de los nodos existentes debe resolverse antes de añadir nuevos nodos para evitar sesgos en la colocación

## Véase también

- [[enroll-ppn-node]] — inscribir el primer nodo en una flota desde cero
- [[service-vm-fleet]] — el servicio del controlador de flota que gestiona el inventario de nodos y la colocación recomendada
- [[configure-tenant-namespace]] — el espacio de nombres que contiene los nodos de la flota
- [[ppn-small-business-compute]] — la arquitectura de la flota y el papel de cada nivel de nodo
- [[verify-worm-ledger]] — confirmar que los eventos de inscripción de nodos están registrados permanentemente
