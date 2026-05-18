---
schema: foundry-doc-v1
title: "Infraestructura"
slug: _index.es
short_description: "Topología de implementación de flota, runtime operacional en la nube e infraestructura física — desde el sustrato de almacenamiento del registro WORM hasta patrones de implementación perimetral, la malla soberana y la arquitectura de telemetría."
lang: es
category: infrastructure
type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: _index.md
---

Los artículos de infraestructura se sitúan en el límite entre la arquitectura abstracta de la plataforma y las máquinas, servicios y rutas de red concretos que forman un despliegue activo. Esta categoría cubre el diseño del sustrato de almacenamiento, la topología de flota, los patrones de despliegue en el borde, la gestión operativa de claves y la red de malla y telemetría que conecta una flota.

## Sustrato de almacenamiento

La capa de persistencia fundacional — el libro WORM y la superficie de auditoría que proporciona.

- [[worm-ledger-design]] — El libro de Solo Escritura y Múltiple Lectura de cuatro capas: basado en tiles, encadenado por hash, firmado criptográficamente; satisface SEC 17a-4(f), eIDAS y SOC 2 por estructura, no por política.
- [[worm-ledger-architecture]] — Disposición arquitectónica del libro WORM a través de los servicios del Anillo 1.
- [[worm-ledger-storage-architecture]] — Organización del almacenamiento físico para despliegues del libro WORM.
- [[storage]] — Topología de almacenamiento y configuración de dispositivos de bloque para despliegues PointSav.
- [[data-vault-bookkeeping-substrate]] — Una arquitectura de contabilidad para PYME construida sobre un vault de origen inmutable y un diario de solo anexado, con separación estructural entre el registro contable y cualquier herramienta de contabilidad.

## Despliegue de flota y borde

Cómo se provisiona, actualiza y mantiene un despliegue en hardware on-premises y en la nube.

- [[edge-deployment]] — Patrones de despliegue en el borde para instancias PointSav que operan en el borde de la red o en entornos de baja conectividad.
- [[tier-c-key-wiring]] — El procedimiento operativo para gestionar claves API externas en el servicio Portero: dónde viven las claves, cómo rotan y cómo se contiene una brecha.

## Red y telemetría

Cómo se comunican los nodos de la flota y cómo se recopilan las señales de observabilidad sin centralizar datos identificables.

- [[sovereign-mesh]] — La red de malla entre pares basada en WireGuard que conecta los nodos de flota PointSav sin una autoridad de enrutamiento central.
- [[sovereign-telemetry]] — Telemetría de estado cero: el V4 Intent Beacon recopila señales de comportamiento y hardware de clientes en el borde sin cookies, identificadores de sesión ni análisis de terceros.
- [[telemetry-architecture]] — Arquitectura del pipeline de telemetría en los despliegues PointSav.

## Véase también

- [Arquitectura](/architecture/) — arquitectura transversal de la plataforma y el modelo de tres anillos
- [Sistemas](/systems/) — los sistemas operativos que se ejecutan sobre esta infraestructura
- [Servicios](/services/) — los servicios que dependen del sustrato de almacenamiento y red
