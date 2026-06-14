---
schema: foundry-doc-v1
title: "Infraestructura"
slug: _index.es
short_description: "Topología de implementación de flota, runtime operacional en la nube e infraestructura física — el sustrato de almacenamiento del registro WORM, patrones de despliegue en el borde, la malla privada WireGuard, la telemetría soberana, las operaciones de cableado de claves y el vault contable que ancla la superficie contable PYME."
lang: es
category: infrastructure
type: topic
content_type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-29
editor: pointsav-engineering
paired_with: _index.md
---

Los artículos de infraestructura se sitúan en el límite entre la arquitectura abstracta de la plataforma y las máquinas, servicios y rutas de red concretos que forman un despliegue activo. Esta categoría cubre el diseño del sustrato de almacenamiento, la topología de flota, los patrones de despliegue en el borde, la gestión operativa de claves y la red de malla y telemetría que conecta una flota. Donde los artículos de [[three-ring-architecture|arquitectura de tres anillos]] describen el modelo lógico, los artículos de infraestructura describen el runtime — el sustrato físico, los túneles WireGuard y el libro WORM en disco que cualquier auditor puede verificar byte por byte.

## Sustrato de almacenamiento

La capa de persistencia fundacional — el libro de Solo Escritura y Múltiple Lectura y el vault contable construido sobre él.

- [[worm-ledger-design|Diseño del libro WORM]] — El libro de Solo Escritura y Múltiple Lectura de cuatro capas: basado en tiles, encadenado por hash, firmado criptográficamente; satisface SEC 17a-4(f), eIDAS y SOC 2 por estructura, no por política.
- [[worm-ledger-architecture|Arquitectura del libro WORM]] — Disposición arquitectónica del libro WORM a través de los servicios del Anillo 1.
- [[worm-ledger-storage-architecture|Arquitectura de almacenamiento WORM]] — Organización del almacenamiento físico para despliegues del libro WORM.
- [[storage|Almacenamiento]] — Escrituras de solo adición a nivel de hardware, registros evidentes a la manipulación, eliminación legal mediante destrucción de claves criptográficas y protección de respaldo mediante unidades secundarias emparejadas criptográficamente.
- [[data-vault-bookkeeping-substrate|Sustrato contable de Data Vault]] — Una arquitectura de contabilidad para PYME construida sobre un vault de origen inmutable y un diario de solo anexado, con separación estructural entre el registro contable y cualquier herramienta de contabilidad.
- [[cryptographic-ledgers|Libros criptográficos]] — Almacenamiento de estado inmutable mediante cadena de hash; cualquier alteración rompe una prueba criptográfica verificable en lugar de una comprobación de política.

## Despliegue de flota y borde

Cómo se provisiona, actualiza y mantiene un despliegue en hardware on-premises y en la nube.

- [[edge-deployment|Despliegue en el borde]] — Patrones de despliegue en el borde: conexiones de red externas enrutadas a través de servicios de ingesta de frontera del Anillo 1, saneamiento de carga útil antes de los anillos de procesamiento central, eventos limpios registrados en el libro de auditoría en lugar del tráfico de red bruto.
- [[tier-c-key-wiring|Cableado de claves Tier C]] — El procedimiento operativo para gestionar claves API externas en el servicio Portero: dónde viven las claves, cómo rotan y cómo se contiene una brecha.
- [[genesis-protocol|Protocolo Génesis]] — Cómo una flota aislada arranca desde un estado frío, derivando su identidad y emparejamientos sin una autoridad externa.
- [[five-stage-supply-chain|Cadena de suministro de cinco etapas]] — El código pasa de contribuyente a producción a través de cinco etapas, con un aislamiento doble ciego que separa las credenciales de producción de los espacios de trabajo de contribuyentes.

## Red y telemetría

Cómo se comunican los nodos de la flota y cómo se recopilan las señales de observabilidad sin centralizar datos identificables.

- [[sovereign-mesh|Malla soberana]] — La red de malla entre pares basada en WireGuard que conecta los nodos de flota PointSav sin una autoridad de enrutamiento central.
- [[pointsav-private-network|Red privada PointSav]] — La malla privada WireGuard que conecta los nodos de flota de Woodfine, proporcionando transporte cifrado sin otorgar acceso de capa de aplicación a los servicios en esos nodos.
- [[ppn-command-protocol|Protocolo de comandos PPN]] — El protocolo de comandos utilizado sobre la malla privada: paquetes binarios compactos transportados dentro de túneles WireGuard.
- [[sovereign-telemetry|Telemetría soberana]] — Telemetría de estado cero: el V4 Intent Beacon recopila señales de comportamiento y hardware de clientes en el borde sin cookies, identificadores de sesión ni análisis de terceros.
- [[telemetry-architecture|Arquitectura de telemetría]] — Pipeline de telemetría de extremo a extremo: recopilación en los nodos de borde de producción, transporte cifrado, procesamiento controlado localmente, sin dependencias de nube de terceros.
- [[data-sovereignty-telemetry|Soberanía de datos en telemetría]] — Cómo la telemetría preserva las garantías de soberanía de datos mientras sigue produciendo señal operativamente útil.

## Véase también

- [Arquitectura](/architecture/) — arquitectura transversal de la plataforma y el modelo de tres anillos
- [Sistemas](/systems/) — los sistemas operativos que se ejecutan sobre esta infraestructura
- [Servicios](/services/) — los servicios que dependen del sustrato de almacenamiento y red
- [Sustrato](/substrate/) — los conceptos de mecanismos fundacionales que realiza la infraestructura
