---
schema: foundry-doc-v1
content_type: topic
title: "Cómputo PPN para Pequeñas Empresas"
slug: topic-ppn-small-business-compute
aliases:
  - topic-ppn-small-business-compute
short_description: "La capa de cómputo de la Red Privada PointSav (PPN) proporciona capacidad de máquinas virtuales agrupadas a clientes de pequeñas empresas a través de tres servicios cooperativos: controlador de flota, agente por nodo y proxy de inquilino."
category: architecture
type: reference
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: TRANSLATE-ES
last_edited: 2026-06-20
editor: pointsav-engineering
paired_with: topic-ppn-small-business-compute.md
cites: []
---

# Cómputo PPN para Pequeñas Empresas

La capa de cómputo de la Red Privada PointSav (PPN) proporciona capacidad de máquinas
virtuales agrupadas a clientes de pequeñas empresas. La capacidad se ejecuta en
instancias cloud e2 bajo el hipervisor QEMU TCG y se gestiona mediante tres servicios
cooperativos: un controlador de flota, un agente de latidos por nodo y un proxy de
inquilino orientado al cliente.

## Arquitectura

### Imagen de VM

Cada instancia de VM arranca desde una imagen de disco QCOW2 de NetBSD 10.1 construida
por `os-totebox/scripts/build-image.sh`. La imagen lleva un conjunto curado de servicios
en su capa superpuesta:

- `system-ledger-server` — registro de capacidades de solo escritura (socket Unix en
  `/run/system-ledger/ledger.sock`)
- `slm-doorman-server` — pasarela de inferencia de modelos de lenguaje pequeños
- `sshd` — acceso de operador; `UseDNS no` para evitar timeout de banner bajo TCG

Veriexec se ejecuta en modo estricto (`kern.veriexec.strict=1`). Un manifiesto generado
en el momento de la construcción de la imagen cubre todos los ejecutables de la capa
superpuesta; los binarios sin firmar son denegados en tiempo de ejecución.

### Controlador de Flota (`service-vm-fleet`)

`service-vm-fleet` es el coordinador central de la capa de cómputo PPN. Expone tres
endpoints:

| Endpoint | Método | Propósito |
|---|---|---|
| `/v1/vms` | POST | Registrar una nueva VM y recibir ubicación orientativa |
| `/v1/vms` | GET | Listar VMs; filtro opcional `?tenant_id=` |
| `/healthz` | GET | Sonda de salud |

El controlador ingiere latidos periódicos de los agentes `service-vm-host` que se
ejecutan en cada nodo. El consejo de ubicación se basa en la memoria disponible
reportada; el controlador no tiene autoridad de programación sobre el hipervisor.

### Agente por Nodo (`service-vm-host`)

`service-vm-host` se ejecuta en cada host físico. Lee `/proc/meminfo` en cada intervalo
de latido e informa de la disponibilidad de memoria actual al controlador de flota. Un
stub de monitor QEMU está presente para el futuro soporte de migración en vivo.

### Proxy de Inquilino (`service-vm-tenant`)

`service-vm-tenant` es el único endpoint expuesto a los clientes. Las solicitudes
llevan un token `Bearer` en el encabezado `Authorization`. El proxy:

1. Valida el token contra el `TenantStore` en memoria.
2. Comprueba la cuota (número máximo de VMs por inquilino) antes de reenviar las
   solicitudes de creación al controlador de flota.
3. Escribe una entrada de auditoría en `system-ledger-server` para cada intento de
   creación, aprobación, denegación y eliminación.

Si el socket del registro no está disponible, el proxy registra una advertencia y
continúa — el registro es orientativo en la fase actual.

### Tipos de Cable (`system-vm-fleet-types`)

`system-vm-fleet-types` es un crate de biblioteca compatible con `no_std` que define los
tipos de cable compartidos por los tres servicios:

- `VmRecord` — representa una instancia de VM registrada; lleva `tenant_id: Option<String>`
- `CreateVmRequest` — carga útil de creación del cliente
- `HeartbeatPayload` — informe de disponibilidad por nodo

## Cuota y Aislamiento

Cada inquilino está aislado por un límite numérico de VMs almacenado en `TenantRecord`.
El proxy aplica el límite antes de reenviar al controlador de flota; el controlador de
flota no valida la identidad del inquilino. Una ruta de creación segura frente a TOCTOU
mantiene un `Mutex` por inquilino durante el ciclo completo de creación-respuesta,
evitando el exceso de cuota bajo solicitudes concurrentes del mismo inquilino.

## Despliegue

La capa de cómputo PPN está prevista para desplegarse con un nodo de controlador de
flota y uno o más hosts QEMU, con el controlador de flota y el proxy de inquilino como
miembros del espacio de trabajo en `pointsav-monorepo`. La imagen NetBSD se construye
desde el código fuente en cada versión mediante `build-image.sh`.

## Véase También

- [[topic-os-console-architecture|Arquitectura del OS Console]] — la TUI de operador
  para gestionar el estado de la flota
- [[topic-software-distribution-substrate|Sustrato de Distribución de Software]] — la
  capa de licencias que controla el acceso del cliente a la capacidad PPN
- [[topic-private-git-paid-customer-endpoint|Endpoint de Cliente de Pago en Git Privado]] —
  entrega de binarios a clientes licenciados

---

*Woodfine Capital Projects™, MCorp™, PointSav Digital Systems™, Totebox Orchestration™, Totebox Archive™ y Capability Geometry™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos propietarios.*
