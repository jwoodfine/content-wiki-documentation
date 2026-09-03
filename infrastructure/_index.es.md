---
schema: foundry-doc-v1
title: "Dónde Se Ejecuta"
slug: infrastructure-index
short_description: "Topología de implementación de flota, runtime operacional en la nube e infraestructura física — el sustrato de almacenamiento del registro WORM, patrones de despliegue en el borde, la malla privada WireGuard, la telemetría soberana, las operaciones de cableado de claves y el vault contable que ancla la superficie contable PYME."
lang: es
category: infrastructure
type: topic
content_type: topic
quality: complete
index_type: thematic
index_scope: infrastructure
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: _index.md
---

Los artículos de infraestructura se sitúan en el límite entre la arquitectura abstracta de la plataforma y las máquinas, servicios y rutas de red concretos que forman un despliegue activo. Esta categoría cubre el diseño del sustrato de almacenamiento, la topología de flota, los patrones de despliegue en el borde, la gestión operativa de claves y la red de malla y telemetría que conecta una flota. Donde los artículos de [[three-ring-architecture|arquitectura de tres anillos]] describen el modelo lógico, los artículos de infraestructura describen el runtime — el sustrato físico, los túneles WireGuard y el libro WORM en disco que cualquier auditor puede verificar byte por byte.

<!-- START-HERE-HIGHLIGHT: el motor lee este bloque para la tarjeta "empezar aquí"
     (reutiliza el componente cluster-card--start-here existente). No añadir más de una. -->

**Empiece aquí:** [[worm-ledger-design|El diseño del libro WORM]] — el libro de cuatro capas, basado en tiles y encadenado por hash sobre el que se apoya, directa o indirectamente, cada otro artículo de esta categoría.

<!-- END-START-HERE-HIGHLIGHT -->

## Sustrato de almacenamiento

La capa de persistencia fundacional — el libro de Solo Escritura y Múltiple Lectura y el vault contable construido sobre él.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: storage-substrate -->
- [[totebox-archive|Archivo Totebox]] — Una máquina virtual micro-autónoma y libremente transferible que persiste datos institucionales como archivos planos inmutables; la unidad de despliegue y almacenamiento de la capa de archivo [[totebox-os|os-totebox]].
- [[worm-ledger-design|Diseño del libro WORM]] — El libro de Solo Escritura y Múltiple Lectura de cuatro capas: basado en tiles, encadenado por hash, firmado criptográficamente; satisface SEC 17a-4(f), eIDAS y SOC 2 por estructura, no por política.
- [[worm-ledger-architecture|Arquitectura del libro WORM]] — Disposición arquitectónica del libro WORM a través de los servicios del Anillo 1.
- [[worm-ledger-storage-architecture|Arquitectura de almacenamiento WORM]] — Organización del almacenamiento físico para despliegues del libro WORM.
- [[storage|Almacenamiento]] — Escrituras de solo adición a nivel de hardware, registros evidentes a la manipulación, eliminación legal mediante destrucción de claves criptográficas y protección de respaldo mediante unidades secundarias emparejadas criptográficamente.
- [[data-vault-bookkeeping-substrate|Sustrato contable de Data Vault]] — Una arquitectura de contabilidad para PYME construida sobre un vault de origen inmutable y un diario de solo anexado, con separación estructural entre el registro contable y cualquier herramienta de contabilidad.
- [[cryptographic-ledgers|Libros criptográficos]] — Almacenamiento de estado inmutable mediante cadena de hash; cualquier alteración rompe una prueba criptográfica verificable en lugar de una comprobación de política.
<!-- END AUTO-GENERATED -->

## Despliegue de flota y borde

Cómo se provisiona, actualiza y mantiene un despliegue en hardware on-premises y en la nube.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: fleet-and-edge-deployment -->
- [[edge-deployment|Despliegue en el borde]] — Patrones de despliegue en el borde: conexiones de red externas enrutadas a través de servicios de ingesta de frontera del Anillo 1, saneamiento de carga útil antes de los anillos de procesamiento central, eventos limpios registrados en el libro de auditoría en lugar del tráfico de red bruto.
- [[tier-c-key-wiring|Cableado de claves Tier C]] — El procedimiento operativo para gestionar claves API externas en el servicio Portero: dónde viven las claves, cómo rotan y cómo se contiene una brecha.
- [[genesis-protocol|Protocolo Génesis]] — Cómo una flota aislada arranca desde un estado frío, derivando su identidad y emparejamientos sin una autoridad externa.
- [[five-stage-supply-chain|Cadena de suministro de cinco etapas]] — El código pasa de contribuyente a producción a través de cinco etapas, con un aislamiento doble ciego que separa las credenciales de producción de los espacios de trabajo de contribuyentes.
<!-- END AUTO-GENERATED -->

## Red y telemetría

Cómo se comunican los nodos de la flota y cómo se recopilan las señales de observabilidad sin centralizar datos identificables.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: network-and-telemetry -->
- [[sovereign-mesh|Malla soberana]] — La red de malla entre pares basada en WireGuard que conecta los nodos de flota PointSav sin una autoridad de enrutamiento central.
- [[ppn-mesh-architecture|Red privada PointSav]] — La malla privada WireGuard que conecta los nodos de flota de Woodfine, proporcionando transporte cifrado sin otorgar acceso de capa de aplicación a los servicios en esos nodos.
- [[ppn-command-protocol|Protocolo de comandos PPN]] — El protocolo de comandos utilizado sobre la malla privada: paquetes binarios compactos transportados dentro de túneles WireGuard.
- [[sovereign-telemetry|Telemetría soberana]] — Telemetría de estado cero: el V4 Intent Beacon recopila señales de comportamiento y hardware de clientes en el borde sin cookies, identificadores de sesión ni análisis de terceros.
- [[telemetry-architecture|Arquitectura de telemetría]] — Pipeline de telemetría de extremo a extremo: recopilación en los nodos de borde de producción, transporte cifrado, procesamiento controlado localmente, sin dependencias de nube de terceros.
- [[data-sovereignty-telemetry|Soberanía de datos en telemetría]] — Cómo la telemetría preserva las garantías de soberanía de datos mientras sigue produciendo señal operativamente útil.
<!-- END AUTO-GENERATED -->

## Cómputo y tejido de VM

Cómo se agrupan, aíslan y protegen las máquinas virtuales en los nodos PPN — desde el pool de recursos del hipervisor por nodo hasta la hoja de ruta de arquitectura seL4 y el tejido distribuido planificado que permitirá a las VMs tomar prestado cómputo a través de la malla.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: compute-and-vm-fabric -->
- [[ppn-vm-resource-pool|Pool de recursos VM de la PPN]] — La pila de tres servicios — controlador de flota, agente de host, proxy de inquilino — que aprovisiona, coloca y contabiliza VMs en una malla WireGuard heterogénea.
- [[ppn-hypervisor-resource-pool|Pool de recursos del hipervisor PPN]] — Agrupación de CPU y RAM por nodo mediante virtio_balloon y pesos cgroups v2, estructuralmente ciega al agregador de la capa de datos que se ejecuta por encima.
- [[ppn-tenant-vm-isolation|Aislamiento de VM por inquilino en la PPN]] — Qué aislamiento de espacio de nombres, proceso y red ofrece hoy el pool de recursos PPN, y el camino planificado hacia subredes WireGuard por inquilino.
- [[ppn-distributed-vm-fabric|Tejido VM distribuido de la PPN]] — La extensión planificada de la capa de hipervisor por nodo a un pool multinodo: préstamo de memoria entre nodos, un libro de capacidades distribuido y una cadena de atestación soberana.
- [[ppn-three-path-architecture|Arquitectura seL4 de tres caminos de la PPN]] — Tres opciones seL4 secuenciales para nodos de infraestructura PPN, desde un hipervisor con invitado Linux hasta dominios de protección sin ninguna máquina virtual.
<!-- END AUTO-GENERATED -->

## Véase también

- [Cómo Está Construido](/architecture/) — arquitectura transversal de la plataforma y el modelo de tres anillos
- [Sistemas Operativos](/systems/) — los sistemas operativos que se ejecutan sobre esta infraestructura
- [Servicios de la Plataforma](/services/) — los servicios que dependen del sustrato de almacenamiento y red
- [Bloques de Construcción](/substrate/) — los conceptos de mecanismos fundacionales que realiza la infraestructura
