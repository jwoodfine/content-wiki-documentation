---
schema: foundry-doc-v1
title: "Malla Soberana"
slug: sovereign-mesh
short_description: "La malla soberana es la superposición WireGuard a nivel de aplicación que conecta todos los nodos de la flota PPN, transportando comandos binarios firmados sin depender de un intermediario de mensajes centralizado."
category: infrastructure
type: topic
content_type: topic
status: stable
bcsc_class: public-disclosure-safe
language: es
language_protocol: TRANSLATE-ES
paired_with: sovereign-mesh.md
last_edited: 2026-06-23
editor: pointsav-engineering
---

La **malla soberana** es la capa de red a nivel de aplicación que conecta todos los nodos de la flota de la Red Privada PointSav (PPN). Funciona sobre túneles criptográficos WireGuard a través de una interfaz `ppn0` dedicada y entrega comandos binarios firmados sin depender de un intermediario de mensajes centralizado. Cada nodo se comunica directamente con sus pares autorizados; la capa de malla aplica la misma jerarquía de autoridad que el [[diode-standard|Diode Standard]] como propiedad estructural, no como opción de configuración.

## Topología en hub y radios

La malla utiliza una disposición de hub central con radios. El nodo de retransmisión en la nube se sitúa en el centro y retransmite paquetes entre nodos radio que pueden no tener una ruta directa entre sí.

| Rol | Nodo | Dirección prevista | Paquete |
|---|---|---|---|
| Hub | Retransmisión en la nube (GCP) | `10.8.0.1` | `app-infrastructure-cloud` |
| Radio | Nodo en instalaciones propias | `10.8.0.2` | `app-infrastructure-onprem` |
| Radio | Nodo arrendado | `10.8.0.3` | `app-infrastructure-leased` |

La subred `10.8.0.0/24` es el rango de direcciones previsto para la PPN. Todo el tráfico de la malla queda encapsulado dentro de WireGuard antes de salir de un nodo; el transporte subyacente — internet público, LAN privada o red interna de GCP — es irrelevante para la capa de malla.

## Superposición WireGuard

Cada nodo levanta una interfaz WireGuard `ppn0` como parte de su secuencia de arranque. WireGuard proporciona:

- **Acuerdo de claves** — intercambio Noise Protocol IK; el par de claves a largo plazo de cada nodo es generado y almacenado en el primer ingreso a la malla por `os-network-admin` en el nodo de plano de control, o a través del Genesis Protocol en nodos de borde bare-metal
- **Cifrado e integridad** — ChaCha20-Poly1305 por paquete; ningún tráfico de malla en texto plano abandona nunca un nodo
- **Alcanzabilidad entre pares** — el retransmisor en la nube es el único par con dirección estática; los nodos en instalaciones propias y arrendados se localizan entre sí a través del retransmisor hasta que se disponga de una ruta directa

La configuración WireGuard de cada nodo se almacena en el directorio de instancia de despliegue (local únicamente, excluido de git). Los pares de claves nunca se guardan en ningún repositorio.

## Protocolo de comandos

Todos los comandos de la malla utilizan un formato de paquete binario de 16 bytes entregado por UDP en el puerto 8090. El tamaño reducido es deliberado: el paquete contiene un token de intención, un selector de destino, un nonce y una firma de autoridad truncada — suficiente para identificar el comando, verificar su procedencia y detectar ataques de repetición sin necesitar una sesión TLS completa por cada comando.

El flujo de comandos desde el operador hasta el nodo de destino es:

```
Intención del operador (lenguaje natural)
      ↓
Terminal F8  —  os-network-admin  HTTP :8085
      ↓
Enrutador semántico service-slm
      ↓
Comando binario de 16 bytes (autorizado y firmado)
      ↓
Difusión service-udp  →  ppn0  →  Túnel WireGuard
      ↓
Nodo destino  —  UDP puerto 8090
```

Los comandos fluyen en una sola dirección — desde `os-network-admin` hacia la malla, nunca en sentido inverso — restricción aplicada por `service-pointsav-link` en la capa de aplicación. Véase [[diode-standard]] para la jerarquía de autoridad completa.

## Roles de los nodos en la malla

### os-infrastructure — ancla de borde

El nodo bare-metal `os-infrastructure` es un par de la malla, no un controlador. Escucha en el puerto 8090 los comandos binarios firmados dirigidos a él y los ejecuta; no inicia comandos. La tarjeta de red Broadcom 14e4:16b4 del nodo transporta el tráfico de la malla a través de la interfaz `ppn0` una vez que concluye la secuencia de ingreso del Genesis Protocol.

### os-network-admin — plano de control

`os-network-admin` posee la autoridad de comandos sobre la malla. La Terminal F8 — una interfaz de comandos en lenguaje natural en el puerto HTTP 8085 — acepta la intención del operador y la enruta a través de `service-slm` para producir un comando binario firmado de 16 bytes. El comando se difunde luego a través de `service-udp` en el puerto 8090 a uno o más pares de la malla. `os-network-admin` también alberga el registro de emparejamiento y gestiona la admisión de nuevos nodos mediante el protocolo [[machine-based-auth|autenticación basada en máquina]].

### Retransmisor en la nube — hub

El nodo de retransmisión en GCP retransmite paquetes encapsulados en WireGuard entre nodos radio. No interpreta comandos de la malla; es únicamente una capa de transporte. La IP pública fija del retransmisor y su configuración WireGuard estática lo convierten en el punto de anclaje que permite a los nodos en instalaciones propias y arrendados localizarse mutuamente sin depender de DNS ni DHCP.

## Integración con el Genesis Protocol

Un nodo bare-metal se incorpora a la malla a través del [[genesis-protocol|Genesis Protocol]], no mediante aprovisionamiento WireGuard manual. En el primer arranque:

1. seL4 genera un par de claves sembrado con entropía de fuentes de hardware
2. El nodo entra en modo de arranque ciego — ignorando todo DHCP y DNS — y explora el balizamiento de `os-network-admin` en el puerto 8090
3. Si se encuentra la baliza, `os-network-admin` guía al nodo a través del proceso de ingreso a la malla: registro del par WireGuard, asignación de IP y vinculación del par de claves al registro de emparejamiento
4. Si no se encuentra ninguna baliza dentro de la ventana de exploración, el nodo realiza su auto-génesis: escribe su par de claves en el almacenamiento de variables seguras UEFI y entra en un patrón de espera en el puerto 9443, aguardando una reclamación de administrador

Este mecanismo garantiza que ningún nodo se incorpore nunca a la malla sin un protocolo de autoridad verificado. Los flujos de trabajo manuales con `wg genkey` aplican únicamente durante el aprovisionamiento inicial de la flota; no constituyen la ruta de ingreso en tiempo de ejecución para nodos en producción.

## Relación con el Diode Standard

El [[diode-standard|Diode Standard]] define tres categorías de tráfico en la malla: comandos de autoridad, telemetría y sincronización entre nodos. Las tres fluyen a través de la malla soberana, pero solo los comandos de autoridad utilizan el formato binario de 16 bytes en el puerto 8090. El tráfico de telemetría y sincronización utiliza TCP o UDP encapsulado en WireGuard en otros puertos.

La restricción de unidireccionalidad del Diode Standard — los comandos de autoridad fluyen desde `os-network-admin` hacia los nodos, nunca en sentido inverso — se implementa en la capa de la malla mediante `service-pointsav-link`, un adaptador conectable en caliente que aplica la dirección del flujo sin requerir cambios en la política de WireGuard.

## Véase también

- [[infrastructure-os]] — posiciones de despliegue, secuencia del Genesis Protocol, sustrato NIC Broadcom
- [[os-network-admin]] — Terminal F8, integración con service-slm, propiedad de la política de malla
- [[diode-standard]] — jerarquía de autoridad y definiciones de categorías de tráfico
- [[machine-based-auth]] — gestión de pares de claves Noise Protocol y tipos de emparejamiento
