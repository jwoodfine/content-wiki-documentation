---
schema: foundry-doc-v1
title: "Malla Soberana"
slug: sovereign-mesh
short_description: "La malla soberana es la superposición WireGuard a nivel de aplicación que conecta todos los nodos de la flota PPN, transportando comandos binarios firmados sin depender de un intermediario de mensajes centralizado."
category: infrastructure
index_group: network-and-telemetry
type: topic
content_type: topic
status: stable
bcsc_class: public-disclosure-safe
language: es
language_protocol: TRANSLATE-ES
paired_with: sovereign-mesh.md
last_edited: 2026-08-01
editor: pointsav-engineering
---

La **malla soberana** es la superposición WireGuard que conecta todos los nodos de la flota de la Red Privada PointSav (PPN), sobre una interfaz `wg0` dedicada. Dos mecanismos distintos y reales operan sobre ella: una difusión de carga JSON sin intermediario (`system-udp`, puerto 8090) y un canal de comandos binarios firmados (`app-network-admin`, puerto 9206) que transporta los comandos emitidos por el operador desde la Terminal F8. Cada nodo se comunica directamente con sus pares autorizados; ningún intermediario de mensajes central se sitúa en la ruta.

## Topología en hub y radios

La malla utiliza una disposición de hub central con radios. El nodo de retransmisión en la nube se sitúa en el centro y retransmite paquetes entre nodos radio que pueden no tener una ruta directa entre sí. `os-infrastructure` se ejecuta de forma idéntica en los tres roles — el operador elige dónde reside su cómputo, y la misma malla WireGuard abarca cualquier combinación.

| Rol | Nodo | Dirección prevista | Paquete | Perfil de confianza |
|---|---|---|---|---|
| Hub | Retransmisión en la nube (GCP) | `10.8.0.1` | `app-infrastructure-cloud` | Más bajo — el proveedor de la nube conserva acceso físico al hardware; previsto para retransmisión sin estado, no para almacenamiento persistente |
| Radio | Nodo en instalaciones propias | `10.8.0.2` | `app-infrastructure-onprem` | Más alto — el operador posee y puede verificar físicamente el hardware |
| Radio | Nodo arrendado | `10.8.0.3` | `app-infrastructure-leased` | Híbrido — el operador controla el SO pero no puede verificar físicamente cada arranque |

El cifrado de WireGuard protege el tráfico entre nodos, pero por sí solo no resuelve la brecha de confianza de los perfiles arrendado y en la nube: quien posea el hardware físico aún puede acceder directamente a él. Cerrar esa brecha está previsto mediante aislamiento a nivel de hardware del micronúcleo seL4 — planificado, aún no en ejecución sobre bare metal hoy.

La subred `10.8.0.0/24` es el rango de direcciones previsto para la PPN. Todo el tráfico de la malla queda encapsulado dentro de WireGuard antes de salir de un nodo; el transporte subyacente — internet público, LAN privada o red interna de GCP — es irrelevante para la capa de malla. Un esquema de direccionamiento `10.42.0.0/16` es el objetivo futuro ratificado, con la migración ("Parte A") en curso; ningún nodo desplegado lo utiliza todavía.

## Superposición WireGuard

Cada nodo levanta una interfaz WireGuard `wg0` como parte de su secuencia de arranque. WireGuard proporciona:

- **Acuerdo de claves** — intercambio Noise Protocol IK, el predeterminado de WireGuard; el par de claves a largo plazo de cada nodo es generado y almacenado en el primer ingreso a la malla, hoy de forma manual en el nodo de plano de control, o mediante el Genesis Protocol (diseñado, aún no construido) en nodos de borde bare-metal
- **Cifrado e integridad** — ChaCha20-Poly1305 por paquete; ningún tráfico de malla en texto plano abandona nunca un nodo
- **Alcanzabilidad entre pares** — el retransmisor en la nube es el único par con dirección estática; los nodos en instalaciones propias y arrendados se localizan entre sí a través del retransmisor hasta que se disponga de una ruta directa

La configuración WireGuard de cada nodo se almacena en el directorio de instancia de despliegue (local únicamente, excluido de git). Los pares de claves nunca se guardan en ningún repositorio.

## Protocolo de comandos

Los comandos de autoridad utilizan un formato de paquete binario de 16 bytes entregado por UDP en el puerto 9206: un código de operación de 2 bytes (ping, isolate, pong), un selector de nodo destino de 2 bytes, una marca temporal de 4 bytes y 8 bytes reservados. Es una malla distinta y más pequeña que la difusión JSON descrita arriba — pertenece a `app-network-admin`, no a `system-udp`.

El flujo de comandos desde el operador hasta el nodo de destino es:

```
Intención del operador (lenguaje natural)
      ↓
Terminal F8  —  app-network-admin  HTTP :8085  (/translate)
      ↓
Doorman :9080/v1/translate — devuelve una propuesta pendiente
      ↓
Aprobación del operador  —  app-network-admin HTTP :8085  (/authorize)
      ↓
Comando binario de 16 bytes
      ↓
UDP unicast  →  wg0  →  Túnel WireGuard
      ↓
Nodo destino  —  UDP puerto 9206
```

Traducir una intención y autorizarla son dos llamadas separadas — un comando nunca se envía solo con la propuesta del Doorman. Véase [[diode-standard]] para la jerarquía de autoridad más amplia en la que se inserta esta doble verificación.

## Roles de los nodos en la malla

### os-infrastructure — ancla de borde

El nodo bare-metal `os-infrastructure` es un par de la malla, no un controlador. Escucha los comandos binarios firmados dirigidos a él y los ejecuta; no inicia comandos. La tarjeta de red Broadcom 14e4:16b4 del nodo transporta el tráfico de la malla a través de la interfaz `wg0` una vez que concluye la secuencia de ingreso del Genesis Protocol.

### app-network-admin — plano de control

`app-network-admin` posee la autoridad de comandos sobre la malla — no `os-network-admin`, que hoy es una página estática sin servicio detrás. La Terminal F8, una interfaz de comandos en lenguaje natural en el puerto HTTP 8085, acepta la intención del operador, la reenvía al Doorman para su traducción y — una vez que el operador autoriza explícitamente la propuesta resultante — difunde el comando binario firmado de 16 bytes a uno o más pares de la malla en el puerto 9206.

### Retransmisor en la nube — hub

El nodo de retransmisión en GCP retransmite paquetes encapsulados en WireGuard entre nodos radio. No interpreta comandos de la malla; es únicamente una capa de transporte. La IP pública fija del retransmisor y su configuración WireGuard estática lo convierten en el punto de anclaje que permite a los nodos en instalaciones propias y arrendados localizarse mutuamente sin depender de DNS ni DHCP.

## La brecha que este diseño busca cerrar

La topología en hub y radios anterior está pensada para explotar una brecha estructural en las ofertas convencionales de nube, no simplemente para sortearla:

| Nube convencional | Intención de este diseño |
|---|---|
| Acopla el cómputo a almacenamiento propietario; cobra por egreso de datos | Tratar el retransmisor en la nube como un simple paso sin estado; el almacenamiento persistente permanece en el hardware propio del operador |
| Ofrece acceso en alquiler; retiene la propiedad custodial de la máquina subyacente | El operador puede desconectar y trasladar físicamente un nodo en instalaciones propias o arrendado |
| Requiere ingeniería de red antes de poder añadir cómputo | Se prevé que un nodo pueda unirse a la malla con un aprovisionamiento manual de WireGuard mínimo, una vez completada la secuencia de ingreso descrita más abajo |
| El plano de control de un único proveedor es un punto único de fallo | Cada nodo está diseñado para que una flota no dependa de la disponibilidad continua de un único proveedor de nube |

Se prevé que un operador que ejecute un nodo en instalaciones propias, un retransmisor en la nube para conectividad pública y `app-network-admin` en una estación de trabajo administrativa termine con una flota que no está atada a ningún proveedor de nube en particular. La [[worm-ledger-design|disciplina WORM]] que rige la persistencia de datos de PointSav se aplica a cada nodo, independientemente del perfil de confianza bajo el que opere.

## Integración con el Genesis Protocol

Un nodo bare-metal está pensado para incorporarse a la malla a través del [[genesis-protocol|Genesis Protocol]], no mediante aprovisionamiento WireGuard manual: descubrimiento por mDNS de un servidor de emparejamiento, un intercambio UDP con un código corto, un intercambio de claves autenticado por contraseña CPace, una ceremonia de reclamación aprobada por un administrador y, finalmente, la entrega de la configuración de malla. El trabajo del controlador de red del que depende esta secuencia aún no está listo — cada paso existe como código diseñado, no como comportamiento en ejecución. El aprovisionamiento manual con `wg genkey` es hoy la ruta de ingreso en tiempo de ejecución para todos los nodos de la malla.

## Relación con el Diode Standard

El [[diode-standard|Diode Standard]] describe un flujo de comandos en una sola dirección — los comandos de autoridad viajan desde `app-network-admin` hacia los nodos, nunca en sentido inverso — como regla de diseño declarada para la plataforma. Solo los comandos de autoridad utilizan el formato binario de 16 bytes en el puerto 9206; el tráfico de telemetría y sincronización utiliza TCP o UDP encapsulado en WireGuard en otros puertos. Ningún componente individual verifica ni aplica esta direccionalidad como invariante comprobada por conformidad; se cumple porque nada en la malla implementa una ruta inversa, no porque un adaptador dedicado la bloquee.

## Véase también

- [[os-infrastructure-ppn-node]] — el SO del sustrato de cómputo en sí: estado de despliegue actual, secuencia del Genesis Protocol
- [[os-network-admin]] — la entrada de wiki provisional para este rol de nodo; el servicio real de la Terminal F8 es el crate `app-network-admin`, aún no documentado bajo su propio nombre
- [[diode-standard]] — jerarquía de autoridad y definiciones de categorías de tráfico
- [[machine-based-auth]] — gestión de pares de claves Noise Protocol y tipos de emparejamiento
- [[ppn-command-protocol]] — el análisis detallado dedicado al formato de trama: restricciones de diseño, disposición del paquete, secuencia de despacho
