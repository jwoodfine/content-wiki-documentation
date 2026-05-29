---
schema: foundry-doc-v1
title: "Red Privada de PointSav"
slug: pointsav-private-network
short_description: "La Red Privada de PointSav es la malla WireGuard privada que conecta los nodos de la flota de Woodfine, proporcionando transporte cifrado sin otorgar acceso a la capa de aplicación de los servicios que se ejecutan en esos nodos."
category: infrastructure
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: pointsav-private-network.md
language: es
---

La Red Privada de PointSav (PPN) es la malla WireGuard privada que conecta los nodos de la flota de Woodfine, sobre la que opera la [[sovereign-mesh|malla soberana]]. Es una capa de infraestructura: aprovisiona las máquinas virtuales que ejecutan los servicios `os-*`, enruta el tráfico cifrado entre ellas y proporciona una topología estática sobre la que funciona [[totebox-orchestration|Totebox Orchestration]].

La PPN no es un sistema de autorización. No otorga acceso a los datos de la aplicación. Estar en la PPN significa que una máquina puede alcanzar la red; no significa que pueda abrir ninguna puerta. La autorización se gestiona en la capa de aplicación mediante la autorización basada en máquinas, que opera de forma independiente y por encima de la PPN.

## La topología en estrella

La PPN utiliza una topología en estrella con tres roles de nodo: un nodo concentrador (hub) en GCP con IP pública estática que acepta todas las conexiones de radios; un nodo radio (spoke) en las instalaciones que marca hacia el concentrador en la nube; y nodos radio de portátiles que también marcan hacia el concentrador en la nube.

Todo el tráfico se inicia desde los radios. El concentrador nunca marca a los nodos. Internet público no puede iniciar conexiones a los nodos radio.

## Custodia de claves maestras

El nodo en las instalaciones — el iMac ejecutando Linux Mint — conserva las claves criptográficas maestras de toda la red. Esta es una decisión deliberada de custodia física: la máquina que mantiene las claves maestras de WireGuard está bajo la custodia física de Woodfine Management Corp. El material de claves WireGuard que define la topología de red está en posesión física del cliente, no del proveedor.

## Aislamiento deliberado de la capa de aplicación

La propiedad arquitectónica más importante de la PPN: está deliberadamente aislada de la capa de aplicación `os-*`.

Esto significa que una máquina en la PPN no puede leer los datos de `os-totebox` sin un emparejamiento de aplicación. PointSav Digital Systems, como proveedor y operador de la PPN, no tiene acceso a nivel de aplicación a los Archivos Totebox de los clientes a través de la infraestructura de red. El proveedor es dueño de las tuberías. El cliente es dueño de las puertas.

## La PPN y la autorización basada en máquinas: dos capas de seguridad independientes

La PPN y la autorización basada en máquinas están diseñadas para ser independientes. Ninguna depende de la otra para sus garantías de seguridad. Un atacante que compromete completamente la PPN obtiene tráfico WireGuard cifrado entre máquinas virtuales y nada más. Un operador que revoca un emparejamiento de aplicación bloquea el acceso a la aplicación incluso si la máquina permanece en la PPN.

## Véase también

- [[machine-based-auth]] — la autorización a nivel de aplicación que opera sobre la PPN
- [[sovereign-mesh]] — detalle de la arquitectura de malla
- [[ppn-command-protocol]] — el formato de cable binario de 16 bytes para comandos de flota
- [[genesis-protocol]] — cómo los nuevos nodos se unen a la flota de forma segura
