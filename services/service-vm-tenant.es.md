---
schema: foundry-doc-v1
title: "service-vm-tenant"
slug: service-vm-tenant
category: services
type: service
content_type: topic
quality: stub
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: TRANSLATE-ES
last_edited: 2026-06-20
editor: pointsav-engineering
paired_with: service-vm-tenant.md
short_description: "El proxy de inquilino aplica autenticación, aislamiento de espacio de nombres, límites de cuota y una pista de auditoría inmutable en el límite del cliente del pool de recursos VM de la PPN."
cites: []
---

El proxy de inquilino es la capa orientada al cliente del pool de recursos VM de la PPN. Acepta solicitudes de creación, destrucción y consulta de estado de llamadores autenticados y aplica el contrato de inquilino antes de reenviarlas al [[service-vm-fleet|controlador de flota]].

## Autenticación y aislamiento de espacio de nombres

La autenticación utiliza tokens de portador emitidos en el momento del aprovisionamiento del inquilino. Cada token lleva un identificador de inquilino que el proxy utiliza para separar todos los registros de VMs. Un inquilino no puede consultar, modificar ni destruir VMs de otro inquilino; el proxy aplica esta restricción en cada endpoint antes de cualquier interacción con la flota.

## Aplicación de cuotas

A cada inquilino se le asigna un límite de capacidad en el momento del aprovisionamiento. El proxy verifica la capacidad actualmente asignada contra ese límite antes de reenviar una solicitud de creación; las solicitudes que superarían la cuota son rechazadas. Las creaciones concurrentes del mismo inquilino se serializan para evitar que dos solicitudes simultáneas pasen ambas la verificación de cuota contra el mismo total previo a la creación.

## Pista de auditoría

Todas las operaciones de escritura se añaden a un registro de auditoría inmutable. Cada entrada registra el identificador del inquilino, el identificador de la VM, el tipo de operación, la marca de tiempo y el origen de la solicitud.

## Véase también

- [[ppn-vm-resource-pool|Arquitectura del Pool de Recursos VM PPN]] — visión completa de la arquitectura
- [[ppn-tenant-vm-isolation|Aislamiento de VM por Inquilino en la PPN]] — el modelo de aislamiento aplicado por el proxy
- [[service-vm-fleet|service-vm-fleet]] — el controlador de flota que recibe las solicitudes de creación

*Woodfine Capital Projects™, MCorp™, PointSav Digital Systems™, Totebox Orchestration™, Totebox Archive™ y Capability Geometry™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos propietarios.*
