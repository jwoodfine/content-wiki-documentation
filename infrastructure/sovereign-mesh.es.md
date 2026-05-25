---
schema: foundry-doc-v1
type: topic
slug: sovereign-mesh
short_description: "La malla soberana es la superposición de red WireGuard a nivel de aplicación que conecta cada nodo de la flota de la Red Privada de PointSav, transportando comandos binarios firmados sin depender de un intermediario de mensajes centralizado."
title: "Malla soberana"
category: infrastructure
language: es
paired_with: sovereign-mesh.md
status: active
last_edited: 2026-05-25
editor: pointsav-engineering
---

La malla soberana es la superposición de red a nivel de aplicación que conecta cada nodo de la flota de la Red Privada de PointSav (PPN). Funciona sobre túneles criptográficos WireGuard en una interfaz dedicada `ppn0` y transporta comandos binarios firmados sin depender de un intermediario de mensajes centralizado. Cada nodo se comunica directamente con sus pares autorizados; la capa de malla aplica la misma jerarquía de autoridad que el [[diode-standard|Estándar Diodo]] como una propiedad estructural, no una opción de configuración.

## Topología en estrella

La malla utiliza una disposición en estrella. El nodo relé en la nube está en el centro y retransmite paquetes entre nodos radio que pueden no tener una ruta directa entre sí. La subred `10.50.0.0/24` es el rango de direcciones previsto para la PPN.

## Superposición WireGuard

Cada nodo levanta una interfaz WireGuard `ppn0` como parte de su secuencia de arranque. WireGuard proporciona acuerdo de claves mediante el protocolo Noise IK, cifrado e integridad mediante ChaCha20-Poly1305 por paquete, y alcanzabilidad de pares a través del relé en la nube como el único par con dirección estática.

## Protocolo de comandos

Todos los comandos de malla utilizan un formato de paquete binario de 16 bytes entregado por UDP en el puerto 8090. El flujo de comandos del operador al nodo de destino: la intención en lenguaje natural se introduce en el terminal F8 de `os-network-admin`; `service-slm` la traduce a un código de operación de 2 bytes; `service-udp` difunde el paquete de 16 bytes firmado sobre la malla WireGuard; el nodo de destino actúa mientras los demás descartan.

Los comandos fluyen en una sola dirección — desde `os-network-admin` hacia afuera — una restricción aplicada por `service-pointsav-link` en la capa de aplicación.

## Integración con el Protocolo Génesis

Un nodo de hardware se une a la malla a través del [[genesis-protocol|Protocolo Génesis]] en lugar del aprovisionamiento manual de WireGuard. Esto garantiza que ningún nodo se una a la malla sin un protocolo de autoridad verificado.

## Relación con el Estándar Diodo

El [[diode-standard|Estándar Diodo]] define tres categorías de tráfico de malla: comandos de autoridad, telemetría y sincronización entre nodos. Solo los comandos de autoridad utilizan el formato binario de 16 bytes en el puerto 8090.

## Véase también

- [[genesis-protocol]] — cómo los nodos se unen a la malla en el primer arranque
- [[ppn-command-protocol]] — el formato de cable binario de 16 bytes para comandos de flota
- [[service-pointsav-link]] — el adaptador que aplica la dirección del flujo de comandos
- [[diode-standard]] — jerarquía de autoridad y definiciones de categorías de tráfico
- [[sovereign-telemetry]] — la arquitectura de telemetría de estado cero que opera sobre la malla
