---
schema: foundry-doc-v1
title: "Cómo configurar un espacio de nombres de tenant"
slug: configure-tenant-namespace
short_description: "Configura un espacio de nombres de inquilino aislado: registra al inquilino, define los límites de cuota, emite el token de capacidad raíz y verifica el aislamiento y la aplicación de cuotas."
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-07-18
editor: pointsav-engineering
language: es
language_protocol: TRANSLATE-ES
paired_with: configure-tenant-namespace.md
---

Un espacio de nombres de tenant es la partición aislada dentro de la plataforma que contiene los recursos de un solo cliente — nodos de flota, sesiones, registros de auditoría y tokens de capacidad. Configurar un espacio de nombres de tenant significa registrar el tenant con la capa de servicios, definir límites de cuota y verificar que el aislamiento esté aplicado. Esta guía cubre la configuración inicial del espacio de nombres para un solo tenant.

Para el servicio que aplica el aislamiento de tenant, véase [[service-vm-tenant]]. Para la arquitectura de flota que abarcan los espacios de nombres, véase [[ppn-small-business-compute]].

**Corrección mayor (2026-07-18):** la superficie de API que describe esta guía no existe
en la fuente real de `service-vm-tenant`. La verificación directa de la tabla de rutas
(`service-vm-tenant/src/main.rs`) encuentra exactamente cuatro rutas: `GET /healthz`,
`POST /v1/vms` (crear), `GET /v1/vms` (listar), `DELETE /v1/vms/:vm_id`, y
`GET /v1/status` — **ningún endpoint `/v1/tenants` de ningún tipo.** Los Pasos 1 y 2 más
abajo (`POST /v1/tenants` para registrar un tenant, `POST /v1/tenants/acme-corp/tokens`
para emitir un token de capacidad raíz) describen rutas que no están en el servicio. El
registro de tenants no es una llamada API en absoluto en la fuente real — se controla
**mediante configuración al iniciar el servicio** vía una variable de entorno
`TENANT_IDS` (el servicio registra "`TENANT_IDS not set — no tenants registered; all
requests will 401`" cuando está ausente), no una operación de "registrar un tenant" en
tiempo de ejecución que un administrador realiza después de que el servicio ya está
activo. La verificación de aislamiento del Paso 3 (`GET /v1/vms`) y la verificación de
cuota excedida del Paso 4 son plausibles contra la ruta real `/v1/vms`, pero no se han
reverificado individualmente aquí. **Señalado, no reescrito silenciosamente** — esto se
lee como un diseño anterior sustituido por un aprovisionamiento de tenant más simple
basado en variables de entorno, o una guía escrita antes que el servicio que describe;
necesita confirmación de project-totebox sobre el mecanismo real de aprovisionamiento de
tenants antes de corregir o eliminar los Pasos 1–2.

## Requisitos previos

- Acceso de administrador a `service-vm-tenant` (el servicio proxy de tenant, puerto 9221)
- Un ID de tenant: una cadena ASCII minúscula estable que identifica al cliente (p.ej., `acme-corp`)
- Valores de cuota acordados con el tenant: máximo de VMs concurrentes, cuota de almacenamiento, tasa de solicitudes API

## Paso 1: Registrar el tenant

Cree el registro del tenant publicando en el servicio de tenant:

```
curl -X POST http://127.0.0.1:9221/v1/tenants \
  -H "Authorization: Bearer <token-admin>" \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": "acme-corp",
    "display_name": "Acme Corporation",
    "max_vms": 10,
    "storage_quota_gb": 100,
    "api_rate_limit_rpm": 600
  }'
```

Una respuesta exitosa devuelve el registro del tenant con una marca de tiempo `created_at`. El ID del tenant es inmutable después de la creación — elíjalo cuidadosamente. El libro mayor WORM registra el evento de creación automáticamente.

## Paso 2: Emitir el token de capacidad raíz del tenant

Una vez que el espacio de nombres existe, emita un token de capacidad raíz para la primera sesión de administrador del tenant. Este token usa el alcance `service:tenant-admin` y está limitado al nuevo `tenant_id`:

```
curl -X POST http://127.0.0.1:9221/v1/tenants/acme-corp/tokens \
  -H "Authorization: Bearer <token-admin>" \
  -H "Content-Type: application/json" \
  -d '{
    "subject_pubkey": "<clave-publica-admin-tenant>",
    "scope": "service:tenant-admin",
    "expires_in_seconds": 86400
  }'
```

Entregue este token al administrador designado del tenant. Lo utilizarán para emitir subtokens e inscribir sus propios dispositivos.

## Paso 3: Verificar el aislamiento del espacio de nombres

Confirme que el espacio de nombres del tenant está aislado de otros tenants consultando la flota con las credenciales del nuevo tenant:

```
curl -s "http://127.0.0.1:9221/v1/vms" \
  -H "Authorization: Bearer <token-admin-tenant>"
```

La respuesta debe contener únicamente las VMs pertenecientes a `acme-corp`. Si aparecen VMs de otros tenants, el aplicación del espacio de nombres tiene un defecto — no continúe; revise la configuración de `service-vm-tenant`.

## Paso 4: Verificar el cumplimiento de la cuota

Envíe una solicitud que supere la cuota configurada para confirmar que el cumplimiento está activo. Por ejemplo, si `max_vms` es 10, intente registrar una 11ª VM. El servicio debe devolver una respuesta `429 Too Many Requests` con un cuerpo de error de cuota excedida.

El fallo en el cumplimiento de la cuota es un defecto de facturación y equidad — resuélvalo antes de que el tenant comience a usar la producción.

## Paso 5: Confirmar la entrada en el libro mayor WORM

El evento de creación del tenant se registra permanentemente. Verifique que la entrada existe:

```
service-fs read --filter tenant-id=acme-corp --event-type TENANT_CREATED --limit 1
```

La entrada confirma cuándo se creó el espacio de nombres y bajo qué token de administrador. Este registro no puede ser alterado.

## Puntos clave

- Los IDs de tenant son inmutables después de la creación — elija identificadores descriptivos y estables
- Cada espacio de nombres de tenant tiene límites de cuota independientes; configúrelos antes de que el tenant comience a inscribir nodos
- El aislamiento del espacio de nombres debe verificarse antes de entregar las credenciales al tenant
- Se crea una entrada en el libro mayor WORM para cada evento del ciclo de vida del espacio de nombres (creación, cambio de cuota, eliminación)

## Véase también

- [[service-vm-tenant]] — el servicio proxy de tenant que aplica los límites del espacio de nombres
- [[ppn-small-business-compute]] — la arquitectura de la flota de cómputo que particionan los espacios de nombres de tenant
- [[issue-capability-token]] — cómo emitir tokens de capacidad una vez que el espacio de nombres existe
- [[scale-user-tiers]] — ajustar los niveles de acceso por usuario dentro de un espacio de nombres establecido
- [[add-a-fleet-node]] — inscribir el primer nodo de cómputo del tenant después de la configuración del espacio de nombres
