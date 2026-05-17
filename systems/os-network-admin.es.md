---
schema: foundry-doc-v1
title: "os-network-admin — El Plano de Control de Flota"
slug: os-network-admin
category: systems
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: os-network-admin.md
short_description: "os-network-admin es el plano de control de una flota PointSav — una instancia por flota, gestionando el registro de emparejamientos, las reglas Diodo y la política de enrutamiento de malla. Los comandos se componen en un terminal semántico F8 y se transmiten como paquetes binarios de 16 bytes a través de la malla WireGuard."
cites: []
---

`os-network-admin` es el plano de control de una flota PointSav — una instancia por despliegue, gestionando el registro de emparejamientos, las reglas de cumplimiento del Diodo y la política de enrutamiento WireGuard para todos los nodos `os-infrastructure` de la flota. Los administradores componen comandos en un terminal semántico F8, donde la intención en lenguaje natural es traducida localmente por `service-slm` a comandos binarios de 16 bytes que se transmiten simultáneamente a todos los nodos de la malla. No hay ningún agente de mensajes central ni servicio externo en este flujo. Este artículo cubre el rol del plano de control, la arquitectura de despacho de comandos y la relación entre `os-network-admin` y los nodos `os-infrastructure` que gobierna.

## El rol del plano de control

`os-network-admin` ejecuta una instancia por flota. Sus responsabilidades son:

| Función | Descripción |
|---|---|
| Registro de emparejamientos | Mantiene la lista autoritativa de entradas válidas de `service-pairing` en toda la flota; emite y revoca tokens fiduciarios vinculados al hardware |
| Cumplimiento de reglas Diodo | Define qué flujos de comandos están permitidos entre los miembros de la flota según el [[diode-standard|Estándar Diodo]]; los cambios se propagan a todos los nodos mediante transmisión en malla |
| Política de enrutamiento en malla | Gestiona la topología de superposición WireGuard — listas de pares, rangos de IP permitidos, calendarios de intercambio de claves |
| Reclamaciones de flota | Acepta solicitudes de reclamación del Protocolo Génesis de nuevos nodos `os-infrastructure` que se unen a la flota |

## El terminal F8 y el despacho de comandos

`os-network-admin` opera un terminal F8 — una superficie de entrada semántica controlada por teclado. Un administrador escribe la intención en lenguaje natural; `service-slm` ejecutándose localmente en el mismo nodo la traduce a un comando binario sin contactar ningún servicio externo.

La secuencia de despacho:

1. El administrador escribe la intención en el terminal F8 — por ejemplo, instruyendo al sistema que aísle un nodo perimetral específico.
2. `service-slm` (ejecutándose en el mismo nodo `os-network-admin`) analiza la oración y produce un comando binario de dos bytes que identifica la operación y el nodo objetivo.
3. `service-udp` transmite el paquete de comando de 16 bytes a través de la malla WireGuard en el puerto 8090.
4. Cada nodo de la flota recibe el paquete simultáneamente. Solo el nodo destinatario actúa; los demás lo descartan.

La capa de traducción es invisible en el límite del protocolo — la malla solo ve el comando binario, no la oración en lenguaje natural. El administrador solo ve el terminal F8, no una interfaz de chat.

## Relación con os-infrastructure

`os-network-admin` y `os-infrastructure` están diseñados como pareja:

| Capa | Rol |
|---|---|
| `os-infrastructure` | Sustrato de cómputo — arranca en hardware, ejecuta el par WireGuard, aloja instancias de Totebox y otros SO |
| `os-network-admin` | Plano de control — gobierna la flota, posee el registro de emparejamientos, transmite comandos |

Una flota mínima es una instancia de `os-network-admin` y uno o más nodos `os-infrastructure`. El plano de control no se ejecuta en el mismo nodo que el sustrato de cómputo en despliegues de producción, aunque una configuración de desarrollo en una sola máquina es posible.

## Véase también

- [[infrastructure-os]] — los nodos de sustrato de cómputo que `os-network-admin` gobierna
- [[os-family-overview]] — la familia de ocho SO y cómo encaja cada miembro
- [[diode-standard]] — el protocolo que rige el flujo de comandos unidireccional a través de la flota
- [[service-slm]] — el modelo de lenguaje semántico local que traduce los comandos
- [[machine-based-auth]] — los pares de claves fiduciarias y el registro de emparejamientos que gestiona `os-network-admin`
- [[deployment-patterns]] — las seis configuraciones de flota canónicas
