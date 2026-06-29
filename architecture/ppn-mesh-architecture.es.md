---
schema: foundry-doc-v1
title: "Arquitectura de malla PPN"
slug: ppn-mesh-architecture
category: architecture
type: concept
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-06-29
editor: pointsav-engineering
paired_with: ppn-mesh-architecture.md
short_description: "La Red Privada de PointSav utiliza una malla WireGuard de concentrador y radios para conectar nodos de flota, con custodia física de claves en las instalaciones del operador; este artículo cubre la topología de malla, la incorporación de nodos (Mesh Fusion), el protocolo de supervisión humana del Terminal F8 y el aislamiento deliberado entre la capa de red y la capa de autorización de aplicaciones."
cites: []
references:
  - id: 1
    text: "Donenfeld, J. A. 'WireGuard: Next Generation Kernel Network Tunnel.' NDSS Symposium, 2017."
    url: "https://www.ndss-symposium.org/ndss2017/ndss-2017-programme/wireguard-next-generation-kernel-network-tunnel/"
---

La Red Privada de PointSav (PPN, por sus siglas en inglés) es la malla WireGuard cifrada que conecta los nodos de flota de Woodfine. Es una capa de infraestructura de red: proporciona tránsito cifrado entre máquinas virtuales, mantiene una topología de nodos estable y aloja los servicios `os-*` que ejecutan los Totebox Archives y las pasarelas de orquestación.

La PPN no es un sistema de autorización. La pertenencia a la red no otorga acceso a las aplicaciones. Una máquina en la PPN puede alcanzar otros nodos de la malla; no puede leer el contenido de ningún archivo sin un emparejamiento separado de [[machine-based-auth|Autorización Basada en Hardware]] establecido a nivel de la capa de aplicación. Los dos mecanismos abordan problemas diferentes y se describen por separado. Este artículo cubre la PPN.

Para el modelo de cuatro capas de la PPN como plataforma de cómputo — capa de operador, capa de red, capa de VM y capa de aplicación — véase [[ppn-architecture-overview]].

## Topología de concentrador y radios

La PPN utiliza una topología de concentrador y radios. El tráfico entre nodos radiales transita por el concentrador en la nube en lugar de fluir directamente entre pares. Esta arquitectura proporciona dos propiedades: los nodos radiales con direcciones IP dinámicas o privadas siempre pueden comunicarse entre sí a través del endpoint público estable del concentrador, y ningún nodo radial necesita aceptar conexiones entrantes desde internet público.

| Clase de nodo | Despliegue | Rol WireGuard |
|---|---|---|
| Retransmisor en la nube | Instancia de cómputo GCP con IP pública estática | Concentrador — siempre en escucha; retransmite paquetes WireGuard cifrados entre radios |
| Estación de trabajo local | Máquina principal del operador en la red local | Radio — establece conexión saliente al concentrador en la nube al inicio |
| Endpoints portátiles | Laptops y máquinas de campo | Radio — establece conexión saliente al concentrador cuando están en línea |

Todas las conexiones se inician desde los radios. El concentrador nunca establece conexión hacia los nodos radiales. El tráfico desde internet público no puede alcanzar los nodos radiales directamente — no están en escucha de conexiones entrantes.

El retransmisor en la nube realiza únicamente retransmisión de paquetes. Mueve tramas WireGuard cifradas entre pares radiales; no termina conexiones de capa de aplicación, no puede descifrar el tráfico de los servicios `os-*` y no tiene acceso a los datos de los archivos.

## Custodia física de claves

NODE-IMAC-12, la estación de trabajo local, almacena la configuración WireGuard maestra de la flota: el registro autorizado de pares, las asignaciones de subred y la clave privada WireGuard de ese nodo. Ubicar esta custodia en una máquina física bajo el control directo del operador es una decisión deliberada.

Si el retransmisor en la nube es destruido o desaprovisionado, la configuración maestra sobrevive en NODE-IMAC-12. Un retransmisor de reemplazo solo requiere una nueva instancia en la nube con una nueva IP; las claves WireGuard que definen la red permanecen con el cliente, no con el proveedor. La red puede reconstruirse sin intervención del proveedor.

NODE-IMAC-12 es también el objetivo de despliegue principal para `os-console`, la interfaz de consola nativa de teclado para las operaciones del Totebox Archive (véase [[os-console-platform]]).

## El tejido criptográfico WireGuard

WireGuard [^1] utiliza pares de claves de curva elíptica Curve25519: una clave privada y una pública por nodo. La clave privada nunca abandona el nodo en el que fue generada. Las claves públicas se distribuyen a los pares y se registran en la configuración de pares WireGuard del concentrador.

El ciclo de vida de las claves sigue principios de mínima exposición: las claves privadas se almacenan únicamente en el dispositivo, nunca se transmiten a ninguna otra parte. El registro de pares — el registro de qué máquinas son miembros de la malla — se mantiene en `route-network-admin`, la interfaz administrativa de la red. Las asignaciones de direcciones de subred se gestionan junto con el registro de pares.

La PPN utiliza un patrón de difusión UDP sin intermediario para las señales de estado de la flota: los comandos de estado se difunden simultáneamente a todos los nodos activos en la malla, sin enrutar a través de un intermediario central. Cada nodo que está en línea responde. El patrón elimina el punto único de fallo que introduciría un intermediario central de comandos.

## Mesh Fusion: incorporación a la red

La incorporación de un nuevo nodo físico a la PPN se denomina Mesh Fusion. El procedimiento es únicamente de aprovisionamiento a nivel de infraestructura:

1. Instalar el sistema operativo host en el hardware de destino.
2. Generar un par de claves Curve25519 de WireGuard en el nuevo nodo.
3. Registrar la clave pública en el registro de pares en `route-network-admin`.
4. Configurar la interfaz WireGuard en el nuevo nodo: endpoint del concentrador, IP de subred asignada y pares permitidos.
5. Establecer el túnel cifrado: el nuevo radio establece conexión hacia el retransmisor en la nube.
6. Verificar la conectividad: el concentrador observa el nuevo radio; el radio puede alcanzar otros nodos de la malla.

El Mesh Fusion se completa en el paso 6. El nodo es ahora miembro de la red. No se otorgan permisos de capa de aplicación. Para que un nodo acceda a un Totebox Archive — para leer archivos, ejecutar flujos de trabajo editoriales o gestionar registros de gobernanza — las [[machine-based-auth|ceremonias de emparejamiento de Autorización Basada en Hardware]] deben realizarse por separado.

## El Terminal F8: gestión de malla con supervisión humana

La PPN se gestiona a través de `os-network-admin`, accesible mediante el slot F8 en `os-console`. La interfaz aplica un protocolo de dos pasos que asegura la confirmación humana de todos los cambios de estado de la red.

El operador envía una intención de gestión en lenguaje natural. El sistema traduce la intención a una carga de comando estructurada mediante el servicio de inferencia local. La interfaz se detiene y muestra la acción propuesta para inspección visual antes de difundir. El operador confirma explícitamente antes de que el comando se ejecute.

Ningún cambio de red se difunde desde una traducción ambigua o sin revisar. El servicio de inferencia traduce; el humano autoriza.

## Aislamiento deliberado de la capa de aplicación

La propiedad arquitectónica más significativa de la PPN es lo que deliberadamente no hace: otorgar acceso a los datos de aplicación que se ejecutan en los nodos que conecta.

La capa de red transporta paquetes cifrados entre máquinas virtuales. Una máquina en la PPN que no tiene emparejamientos MBA puede alcanzar la malla y no puede acceder a ningún archivo. Este aislamiento produce una frontera de seguridad específica: el proveedor de infraestructura — la parte que construyó y opera la PPN — no tiene acceso a nivel de aplicación a los Totebox Archives del cliente a través de la infraestructura de red. El proveedor controla la red. El cliente controla la autorización.

## PPN y MBA: capas independientes

La PPN y la [[machine-based-auth|Autorización Basada en Hardware]] están diseñadas para ser independientes. Ninguna depende de la otra para sus garantías de seguridad.

| Capa | Lo que protege | Gestionada por | Lo que no hace |
|---|---|---|---|
| PPN (WireGuard) | Topología de red; cifra el tráfico de tránsito entre nodos | Operador de infraestructura (proveedor) | No otorga acceso a nivel de aplicación a los servicios `os-*` |
| MBA (entre pares) | Acceso a nivel de aplicación a los servicios `os-*` | Operador de la máquina (cliente) | No depende de la topología PPN para sus propiedades de seguridad |

Un atacante que comprometa completamente el retransmisor en la nube obtiene acceso al tráfico WireGuard cifrado entre VMs y nada más — los datos de la aplicación no son accesibles sin emparejamientos MBA. Un operador que revoca un emparejamiento MBA bloquea el acceso a la aplicación independientemente de si la máquina permanece en la PPN.

Las dos capas juntas proporcionan defensa en profundidad. También imponen una frontera de soberanía: el proveedor controla la infraestructura; el cliente controla la autorización.

## Entrelazamiento de Almacenamiento Frío

Los datos de archivo de gran volumen que exceden el alcance del almacenamiento en red — planos arquitectónicos, registros de sensores IoT, activos multimedia extensos — se gestionan mediante división criptográfica y custodia física. Los medios de almacenamiento externos quedan matemáticamente vinculados a un archivo específico utilizando una clave derivada de la identidad de ese archivo. Los medios vinculados son ilegibles en cualquier otro sistema.

El Entrelazamiento de Almacenamiento Frío opera fuera de la PPN. Es un mecanismo de custodia física, no un mecanismo de red. La clave de vinculación reside en el nodo del archivo; los medios solo se leen cuando están conectados a ese nodo específico. El entorno operativo principal permanece ligero; los datos desbordados permanecen bajo la custodia física del cliente.

## Véase también

- [[ppn-architecture-overview]] — el modelo de cuatro capas de la PPN como plataforma de cómputo
- [[machine-based-auth]] — el mecanismo de autorización de capa de aplicación que opera sobre la PPN
- [[os-console-platform]] — la interfaz de consola para operadores que utilizan archivos conectados a través de la PPN
- [[three-ring-architecture]] — la arquitectura de servicios que se ejecuta en la infraestructura PPN
