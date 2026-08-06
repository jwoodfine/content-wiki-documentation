---
schema: foundry-doc-v1
title: "Configurar un espacio de nombres de tenant"
slug: configure-tenant-namespace
short_description: "Configura un espacio de nombres de tenant en service-vm-tenant mediante variables de entorno y un reinicio — el mecanismo real basado en configuración, ya que no existe ninguna API de registro de tenants en tiempo de ejecución."
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
paired_with: configure-tenant-namespace.md
---

## Requisitos previos

- Acceso de administrador a la máquina que ejecuta `service-vm-tenant` (puerto 9221 por defecto)
- Un ID de tenant: una cadena estable en ASCII minúsculas que identifica al cliente (p. ej. `acme-corp`)
- Valores de cuota acordados con el tenant: máximo de VMs concurrentes, RAM máxima

## Propósito

Añada un espacio de nombres de tenant a `service-vm-tenant` de la manera en que el servicio realmente lo soporta hoy — editando su configuración de entorno y reiniciándolo. No existe ninguna API de registro en tiempo de ejecución; el aprovisionamiento se basa en configuración.

## Procedimiento

1. Añada el tenant a la lista de permitidos. `TENANT_IDS` es una lista simple separada por comas de IDs de tenant — no lleva datos de cuota en sí misma:

   ```
   TENANT_IDS=acme-corp,tenant-existente
   ```

2. Establezca las cuotas del nuevo tenant como variables de entorno separadas por tenant, nombradas poniendo en mayúsculas el ID del tenant:

   ```
   TENANT_ACME_CORP_MAX_VMS=10
   TENANT_ACME_CORP_MAX_RAM_MB=16384
   ```

   Ambas son opcionales — si se omiten, tienen valores predeterminados de 5 VMs y 8192 MB.

3. Establezca un token de autenticación para el tenant. `service-vm-tenant` usa un token Bearer simple, no un token de capacidad firmado:

   ```
   TOKEN_MAP=<un-token-generado>:acme-corp
   ```

   > **Advertencia:** si `TOKEN_MAP` se deja sin establecer por completo, el servicio recae en un **modo inseguro** explícitamente registrado en el log donde el token bearer literalmente *es* el ID del tenant (`Authorization: Bearer acme-corp` autentica como ese tenant, sin necesidad de ningún secreto). Establezca `TOKEN_MAP` para cualquier uso más allá de pruebas locales.

4. Reinicie `service-vm-tenant` para cargar la nueva configuración. No hay recarga en caliente, ni endpoint de administración, ni actualización de configuración basada en señales — `TENANT_IDS` y las variables por tenant se leen exactamente una vez, al iniciar el proceso.

## Resultado esperado

`service-vm-tenant` reconoce las solicitudes que llevan el token del nuevo tenant, limita automáticamente cada respuesta a las propias VMs de ese tenant, y aplica las cuotas que estableció.

## Verificación

Confirme que el tenant es reconocido y vea su uso actual en una sola llamada:

```bash
curl -s http://127.0.0.1:9221/v1/status \
  -H "Authorization: Bearer <token-de-acme-corp>"
```

Esto devuelve `tenant_id`, `vms_running`, `ram_used_mb`, `max_vms` y `max_ram_mb` — un endpoint real y funcional de uso de cuota.

Confirme el aislamiento listando las VMs — no hay ningún filtro de tenant suministrado por el cliente; el servidor limita los resultados a cualquier tenant con el que autentique el token Bearer:

```bash
curl -s http://127.0.0.1:9221/v1/vms \
  -H "Authorization: Bearer <token-de-acme-corp>"
```

Confirme la aplicación de cuotas intentando exceder `max_vms` o `max_ram_mb` mediante `POST /v1/vms`. Ambos límites se aplican de forma síncrona, antes de que la solicitud llegue al controlador de la flota, y devuelven `429 Too Many Requests` con un cuerpo de texto plano que describe el límite.

## Reversión

Elimine el ID del tenant de `TENANT_IDS` (y su entrada en `TOKEN_MAP`, si está establecida) y reinicie el servicio. Las VMs existentes que el tenant posee no se destruyen automáticamente — desasígnelas explícitamente primero mediante `DELETE /v1/vms/:vm_id` si esa es la intención, ya que un tenant eliminado simplemente pierde la capacidad de autenticarse, no sus recursos en ejecución.

## Próximos pasos

- [[issue-capability-token]] — un sistema de credenciales relacionado pero distinto, para autenticación servicio a servicio en lugar de acceso a VMs con alcance de tenant
- [[add-a-fleet-node]] — añada capacidad de cómputo para que los tenants coloquen VMs

## Véase también

- [[service-vm-tenant]] — el servicio proxy de tenant que aplica los límites del espacio de nombres
- [[ppn-small-business-compute]] — la arquitectura de flota de cómputo que particionan los espacios de nombres de tenant
- [[scale-user-tiers]] — un sistema separado y no relacionado de niveles de acceso para usuarios individuales dentro de un archivo
