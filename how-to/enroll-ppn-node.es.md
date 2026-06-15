---
schema: foundry-doc-v1
title: "Cómo registrar un nodo PPN"
slug: enroll-ppn-node
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
language: es
language_protocol: TRANSLATE-ES
paired_with: enroll-ppn-node.md
---

Un nodo PPN (PointSav Private Network) es una máquina física o virtual que se une a la flota de cómputo de la plataforma. Registrar un nodo significa registrarlo con el controlador de flota, iniciar el agente de latido y verificar que el nodo aparezca en el inventario activo de la flota. Esta guía cubre la secuencia de registro para un solo nodo.

Para la arquitectura de la flota, véase [[ppn-small-business-compute]]. Para el servicio que gestiona el estado de la flota, véase [[service-vm-fleet]].

## Requisitos previos

- Una máquina con acceso de red al endpoint del controlador de flota
- El binario `service-vm-host` desplegado en el nodo (el agente de latido por nodo)
- La dirección del controlador de flota y el ID de tenant proporcionados por el administrador de la plataforma
- Una sesión de terminal en el nodo que se está registrando

## Paso 1: Verificar que el controlador de flota es accesible

Desde el nodo, confirme que el controlador de flota responde antes de iniciar el agente de latido:

```
curl -s http://<host-controlador-flota>:9203/health
```

Una respuesta exitosa devuelve `{"status":"ok"}`. Si el controlador no es accesible, verifique el enrutamiento de red y las reglas del cortafuegos antes de continuar. El registro requiere una conexión activa con el controlador.

## Paso 2: Configurar el agente de latido

El agente de latido `service-vm-host` lee su configuración desde variables de entorno o un archivo de configuración local. Establezca los valores mínimos requeridos:

```
FLEET_CONTROLLER_URL=http://<host-controlador-flota>:9203
TENANT_ID=<su-tenant-id>
NODE_ID=<nombre-nodo-único>
```

`NODE_ID` debe ser único dentro del espacio de nombres del tenant. Use un nombre descriptivo que identifique el rol y la ubicación de la máquina (p.ej., `compute-west-01`). Una vez establecido, este identificador aparece en el inventario de la flota y en el libro mayor de auditoría WORM.

## Paso 3: Iniciar el agente de latido

Inicie `service-vm-host` como un servicio systemd o directamente desde la línea de comandos:

```
service-vm-host --controller $FLEET_CONTROLLER_URL --tenant $TENANT_ID --node-id $NODE_ID
```

El agente envía un latido inicial inmediatamente y luego en su intervalo configurado (predeterminado: 30 segundos). El primer latido exitoso registra el nodo con el controlador de flota.

## Paso 4: Verificar el registro en el inventario de la flota

Desde una sesión con acceso a la API del controlador de flota, consulte la flota para el nuevo nodo:

```
curl -s "http://<host-controlador-flota>:9203/v1/vms?tenant_id=<su-tenant-id>"
```

La respuesta incluye una matriz de nodos registrados. Encuentre la entrada para el `NODE_ID` que estableció en el paso 2. La entrada muestra los campos `status`, `last_heartbeat` y capacidad de recursos, poblados a partir del primer latido.

Si el nodo no aparece dentro de 60 segundos de iniciar el agente, verifique los registros del agente para ver errores de conexión. Las causas más comunes son una URL de controlador incorrecta o un cortafuegos que bloquea las conexiones salientes en el puerto 9203.

## Paso 5: Confirmar la entrada en el libro mayor

Cada latido escribe una entrada en el libro mayor WORM. Desde el controlador de flota o desde `service-fs`, confirme que existe un registro en el libro mayor para el nuevo nodo:

```
service-fs read --filter node-id=<NODE_ID> --limit 5
```

Un registro exitoso produce al menos una entrada `NODE_HEARTBEAT`. La entrada del libro mayor es el registro de inscripción permanente — no puede ser eliminada ni alterada.

## Puntos clave

- El registro ocurre en el primer latido; no se necesita un paso de registro separado
- `NODE_ID` debe ser único por espacio de nombres de tenant; el controlador de flota rechaza duplicados
- Se crea una entrada en el libro mayor WORM para cada latido — el registro queda registrado permanentemente
- Si el nodo no aparece después de 60 segundos, verifique los registros del agente antes de asumir un problema de red

## Véase también

- [[ppn-small-business-compute]] — la arquitectura de la flota PPN y el modelo de tenant
- [[service-vm-fleet]] — el servicio del controlador de flota que gestiona los nodos registrados
- [[add-a-fleet-node]] — cómo añadir un nodo a una flota de múltiples nodos en funcionamiento
- [[verify-worm-ledger]] — verificar las entradas del libro mayor creadas durante el registro
- [[pair-a-new-device]] — el protocolo de emparejamiento que rige los niveles de acceso a nivel de dispositivo
