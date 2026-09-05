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
last_edited: 2026-09-04
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
- [[totebox-archive|Archivo Totebox]] — Un Totebox Archive es una bóveda soberana de datos asignada a una única entidad — empaquetada como una imagen de disco de arranque libremente transferible, almacenando datos como archivos planos WORM, y aceptando consultas solo a través del Diode Standard.
- [[worm-ledger-design|Diseño del libro WORM]] — Sustrato de libro mayor Write-Once-Read-Many de los servicios Ring 1 de PointSav, diseñado hacia un formato encadenado por hash y firmado que cumple la normativa por estructura.
- [[worm-ledger-architecture|Arquitectura del libro WORM]] — El ledger inmutable WORM por tenant al que escriben todos los servicios de ingestión del Anillo 1, construido sobre tiles C2SP con encadenamiento criptográfico de hashes, anclaje mensual a Sigstore Rekor y un diseño de doble sobre que abarca daemon Linux y unikernel seL4.
- [[worm-ledger-storage-architecture|Arquitectura de almacenamiento WORM]] — La arquitectura de almacenamiento especifica C2SP tlog-tiles como primitivo objetivo; la implementación actual de service-fs conserva un registro JSON de solo adición por inquilino pendiente del backend de bloques, con inmutabilidad estructural y legibilidad a largo plazo como diseño previsto.
- [[storage|Almacenamiento]] — El registro resistente a manipulaciones de la plataforma se apoya en permisos de sistema de archivos y una cadena de hash criptográfica, no en un bloqueo de escritura a nivel de hardware — un administrador con privilegios aún puede eludirlo, y cualquier elusión es detectable, no impedida.
- [[data-vault-bookkeeping-substrate|Sustrato contable de Data Vault]] — Una arquitectura de contabilidad para PYMEs construida sobre una bóveda de fuente inmutable, un diario de solo adición y separación estructural entre el registro contable y cualquier herramienta de contabilidad.
<!-- END AUTO-GENERATED -->

## Despliegue de flota y borde

Cómo se provisiona, actualiza y mantiene un despliegue en hardware on-premises y en la nube.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: fleet-and-edge-deployment -->
- [[edge-deployment|Despliegue en el borde]] — La plataforma enruta todas las conexiones de red externas a través de servicios de ingesta perimetral de Ring 1 en el borde del sistema, desinfectando cargas útiles entrantes antes de que lleguen a los anillos de procesamiento central y registrando eventos limpios y validados en el registro de auditoría en lugar de tráfico de red sin procesar.
- [[tier-c-key-wiring|Cableado de claves Tier C]] — El procedimiento operativo para gestionar las claves de API externas en el servicio Doorman — dónde viven las claves, cómo se aprovisionan, cómo rotan y cómo se contiene una brecha.
- [[os-orchestration-stateless-hub]] — os-orchestration coordina el trabajo entre los Archivos Totebox sin almacenar datos de clientes, claves ni registros de auditoría, actuando como superficie de enrutamiento e intermediación sin estado por encima de la capa de capacidades por archivo.
<!-- END AUTO-GENERATED -->

## Red y telemetría

Cómo se comunican los nodos de la flota y cómo se recopilan las señales de observabilidad sin centralizar datos identificables.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: network-and-telemetry -->
- [[sovereign-mesh|Malla soberana]] — La malla soberana es la superposición WireGuard a nivel de aplicación que conecta todos los nodos de la flota PPN, transportando comandos binarios firmados sin depender de un intermediario de mensajes centralizado.
- [[ppn-mesh-architecture|Red privada PointSav]] — Malla WireGuard de concentrador y radios que conecta nodos de flota, con custodia física de claves en las instalaciones del operador e incorporación de nodos Mesh Fusion.
- [[ppn-command-protocol|Protocolo de comandos PPN]] — El PPN Command Protocol es el formato de cable binario de 16 bytes utilizado por app-network-admin para emitir comandos a los nodos os-infrastructure a través de la malla WireGuard, sin intermediario central ni sobrecarga de sesión.
- [[sovereign-telemetry|Telemetría soberana]] — Telemetría de estado cero: una única baliza al cierre de página con URI y marca temporal, emparejada del lado del servidor con la IP y el user agent del solicitante, escrita sin enmascarar en un registro CSV de solo anexado.
- [[telemetry-architecture|Arquitectura de telemetría]] — La plataforma recopila análisis de tráfico web de nodos perimetrales de producción y los enruta a un entorno de procesamiento controlado localmente a través de una ruta cifrada sin pasar por servicios de análisis de terceros en la nube.
<!-- END AUTO-GENERATED -->

## Cómputo y tejido de VM

Cómo se agrupan, aíslan y protegen las máquinas virtuales en los nodos PPN — desde el pool de recursos del hipervisor por nodo hasta la hoja de ruta de arquitectura seL4 y el tejido distribuido planificado que permitirá a las VMs tomar prestado cómputo a través de la malla.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: compute-and-vm-fabric -->
- [[ppn-vm-resource-pool|Pool de recursos VM de la PPN]] — El pool de recursos VM de la PPN es una pila de tres servicios que aprovisiona, coloca y contabiliza máquinas virtuales en una malla WireGuard heterogénea que combina nodos en la nube y hardware físico.
- [[ppn-hypervisor-resource-pool|Pool de recursos del hipervisor PPN]] — La capa de hipervisor PPN está diseñada para gestionar un pool de CPU y RAM por nodo mediante virtio_balloon y pesos cgroups v2 — ningún mecanismo está construido todavía.
- [[ppn-tenant-vm-isolation|Aislamiento de VM por inquilino en la PPN]] — El pool de recursos PPN separa las cargas de trabajo por inquilino mediante aislamiento de espacio de nombres, aislamiento de proceso por VM y redes en modo usuario. El aislamiento a nivel de subred de red es un hito planificado.
- [[ppn-distributed-vm-fabric|Tejido VM distribuido de la PPN]] — El Tejido VM Distribuido PPN es la extensión planificada de la capa de hipervisor PPN por nodo hacia un pool de recursos multinodo, previsto para permitir que las VMs tomen prestado cómputo de otros nodos de la malla y migren a través de la flota sin intervención del operador en cada movimiento.
- [[ppn-three-path-architecture|Arquitectura seL4 de tres caminos de la PPN]] — Tres opciones de arquitectura seL4 secuenciales para nodos de infraestructura PPN: la Opción B se implementa primero (hipervisor seL4 + invitado Linux), la Opción C añade WireGuard como dominio de protección seL4, y la Opción A apunta a un entorno seL4 puro sin máquinas virtuales.
- [[ppn-architecture-overview]] — Plano de infraestructura física del stack PointSav, que incorpora nodos a una malla autenticada criptográficamente y aloja las máquinas virtuales de la flota.
- [[spot-vm-lifecycle-kill-switch]] — Ciclo de vida de controlador único para la VM spot Yo-Yo — un solo temporizador posee arranque y parada, con interruptor centinela de archivo para control inmediato.
<!-- END AUTO-GENERATED -->

## Véase también

- [Cómo Está Construido](/architecture/) — arquitectura transversal de la plataforma y el modelo de tres anillos
- [Sistemas Operativos](/systems/) — los sistemas operativos que se ejecutan sobre esta infraestructura
- [Servicios de la Plataforma](/services/) — los servicios que dependen del sustrato de almacenamiento y red
- [Bloques de Construcción](/substrate/) — los conceptos de mecanismos fundacionales que realiza la infraestructura
