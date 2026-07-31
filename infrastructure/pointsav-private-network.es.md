---
schema: foundry-doc-v1
title: "Red Privada de PointSav"
slug: pointsav-private-network
short_description: "La Red Privada de PointSav es la malla WireGuard privada que conecta los nodos de la flota de Woodfine, proporcionando transporte cifrado sin otorgar acceso a la capa de aplicación de los servicios que se ejecutan en esos nodos."
category: infrastructure
type: topic
content_type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-07-31
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

El nodo en las instalaciones — el iMac ejecutando Linux Mint — conserva las claves criptográficas maestras de toda la red. Esta es una decisión deliberada de custodia física: la máquina que mantiene las claves maestras de WireGuard está bajo la custodia física de MCorp. El material de claves WireGuard que define la topología de red está en posesión física del cliente, no del proveedor.

El nodo en las instalaciones es también el destino de despliegue principal de `os-console`. Es la máquina desde la cual el operador utiliza la interfaz del Archivo Totebox.

## La estructura criptográfica de WireGuard

WireGuard utiliza pares de claves de curva elíptica Curve25519: un par privado y público por nodo. La clave privada nunca sale de su nodo; las claves públicas se distribuyen a los pares y se registran en la configuración de WireGuard del concentrador.

Las claves privadas se almacenan únicamente en el dispositivo y nunca se transmiten. `route-network-admin` mantiene el registro autoritativo de claves de pares y las asignaciones de subred. El rango de direcciones previsto para la PPN es `10.50.0.0/24`.

La PPN utiliza un enfoque de difusión UDP sin intermediario (zero-broker) para los comandos de estado de la flota: los comandos se difunden como señales UDP a través de la malla hacia todos los nodos activos simultáneamente, sin pasar por ningún intermediario central.

## Mesh Fusion: incorporación a la red

Vincular un nuevo nodo físico a la PPN se denomina Mesh Fusion:

1. Instalar el sistema operativo host en el hardware de destino.
2. Generar un par de claves WireGuard Curve25519 en el nuevo nodo.
3. Registrar la clave pública en `route-network-admin`.
4. Configurar la interfaz WireGuard del nuevo nodo con el punto de conexión del concentrador y la IP de subred.
5. Establecer el túnel cifrado: el nodo marca hacia el relé en la nube.
6. Verificar la conectividad.

Mesh Fusion es únicamente aprovisionamiento a nivel de infraestructura. No establece ningún emparejamiento de aplicación `os-*`. Después de Mesh Fusion, el nodo está en la red; las ceremonias de emparejamiento de aplicación se realizan por separado para otorgar acceso a nivel de aplicación.

## La Terminal F8: interfaz de gestión de la malla

La PPN se gestiona a través de `os-network-admin`, expuesta como la Terminal F8 — una interfaz operada por teclado en el nodo `route-network-admin`. Los operadores envían comandos de gestión de red en inglés natural. La interfaz utiliza un protocolo de ejecución de dos pasos para garantizar la supervisión humana de todos los cambios de red: el operador escribe un comando en inglés natural; la interfaz se detiene y muestra la acción traducida a máquina propuesta por el modelo de lenguaje; el operador confirma visualmente la traducción y hace clic explícitamente en EJECUTAR para difundir el comando. Ninguna acción de red se ejecuta sin la confirmación visual del operador.

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
