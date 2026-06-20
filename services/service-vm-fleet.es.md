---
schema: foundry-doc-v1
title: "service-vm-fleet"
slug: service-vm-fleet
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
paired_with: service-vm-fleet.md
short_description: "El controlador de flota mantiene una vista global de la capacidad de nodos en la malla WireGuard de la PPN y gestiona las decisiones de colocación de máquinas virtuales."
cites: []
---

El controlador de flota es el servicio de colocación y registro del pool de recursos VM de la PPN. Mantiene un registro en memoria del estado de los nodos — capacidad disponible, disponibilidad de virtualización por hardware, recuento actual de VMs y estado de reserva — y resuelve las solicitudes de colocación del [[service-vm-tenant|proxy de inquilino]].

## Algoritmo de colocación

La colocación utiliza un algoritmo de selección en dos pasadas. La primera pasada considera únicamente los nodos no reservados que satisfacen el límite de capacidad solicitado. Si la primera pasada no produce candidatos, la segunda pasada amplía la búsqueda para incluir los nodos reservados. Esta separación permite a los operadores designar nodos para cargas de trabajo sensibles a la latencia mientras se permite la colocación por desbordamiento bajo carga.

## Ingesta de latidos

Los agentes de host informan el estado del nodo al controlador de flota mediante latidos periódicos. La ingesta está acotada por la subyacente WireGuard y la identidad del nodo, sin credenciales adicionales.

## Véase también

- [[ppn-vm-resource-pool|Arquitectura del Pool de Recursos VM PPN]] — visión completa de la arquitectura
- [[service-vm-tenant|service-vm-tenant]] — el proxy de inquilino que envía solicitudes de colocación

*Woodfine Capital Projects™, MCorp™, PointSav Digital Systems™, Totebox Orchestration™, Totebox Archive™ y Capability Geometry™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos propietarios.*
