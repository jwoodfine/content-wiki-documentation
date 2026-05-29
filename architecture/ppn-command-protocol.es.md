---
schema: foundry-doc-v1
title: "El Protocolo de Comandos de la PPN"
slug: ppn-command-protocol
short_description: "El Protocolo de Comandos de la PPN es el formato de cable binario de 16 bytes utilizado por os-network-admin para emitir comandos a los nodos os-infrastructure a través de la malla WireGuard, sin intermediario central ni sobrecarga de sesión."
category: architecture
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: ppn-command-protocol.md
language: es
---

El Protocolo de Comandos de la PPN es el formato de cable utilizado por el plano de control [[os-network-admin|`os-network-admin`]] para emitir comandos a los nodos [[infrastructure-os|`os-infrastructure`]] a través de la [[pointsav-private-network|Red Privada]] de [[pointsav-overview|PointSav]]. Transmite comandos de flota como paquetes binarios de 16 bytes difundidos por UDP en el puerto 8090 sobre la malla WireGuard — sin intermediario central, sin cola y sin ningún servicio de terceros en el camino.

## Restricciones de diseño

Tres requisitos configuraron el protocolo. Sin intermediario: el protocolo de comandos elimina completamente al intermediario. Sin texto plano: el protocolo funciona exclusivamente sobre la malla WireGuard, donde el protocolo Noise IK de WireGuard autentica cada par. Sin verbosidad: los comandos tienen 16 bytes y no hay negociación de sesión ni sobrecarga de encuadre.

## El formato del paquete

Cada comando tiene exactamente 16 bytes. Los dos primeros bytes constituyen el código de operación: un byte que identifica la clase de operación y un byte que identifica el nodo de destino. Los 14 bytes restantes transportan la carga útil específica de la operación.

## La secuencia de despacho

1. El administrador escribe la intención en lenguaje natural en el terminal F8.
2. [[service-slm|`service-slm`]] ejecutándose localmente en el nodo [[os-network-admin|`os-network-admin`]] analiza la oración y produce el código de operación de dos bytes.
3. `service-udp` construye el paquete completo de 16 bytes y lo difunde en la malla WireGuard por UDP en el puerto 8090.
4. Cada nodo de la flota recibe el paquete simultáneamente. Solo el nodo cuya dirección coincide con el byte de destino actúa; todos los demás descartan.

## Relación con el Estándar Diodo

El Protocolo de Comandos de la PPN es la implementación en cable de la categoría de control descendente del [[diode-standard|Estándar Diodo]]. Fluye de la autoridad ([[os-network-admin|`os-network-admin`]]) al sujeto ([[infrastructure-os|`os-infrastructure`]]) y nunca al revés. No existe una ruta de comandos ascendente en el protocolo.

## Véase también

- [[sovereign-mesh]] — la superposición WireGuard sobre la que funciona el protocolo
- [[diode-standard]] — la jerarquía de autoridad y las reglas de tráfico que el protocolo implementa
- [[genesis-protocol]] — cómo los nodos se unen a la malla antes de poder recibir comandos
- [[service-pointsav-link]] — el adaptador hot-pluggable que recibe y ejecuta comandos en los nodos Sujeto
