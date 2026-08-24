---
schema: foundry-doc-v1
title: "Protocolo de comandos PPN"
slug: ppn-command-protocol
short_description: "El PPN Command Protocol es el formato de cable binario de 16 bytes utilizado por app-network-admin para emitir comandos a los nodos os-infrastructure a través de la malla WireGuard, sin intermediario central ni sobrecarga de sesión."
category: infrastructure
index_group: network-and-telemetry
type: topic
content_type: topic
status: stable
bcsc_class: public-disclosure-safe
language: es
language_protocol: TRANSLATE-ES
paired_with: ppn-command-protocol.md
last_edited: 2026-08-24
editor: pointsav-engineering
---

El PPN Command Protocol es el formato de cable que `app-network-admin` utiliza para emitir comandos hacia los nodos `os-infrastructure` a través de la PointSav Private Network. Transmite comandos de flota como paquetes binarios de 16 bytes difundidos por UDP en el puerto 9206 sobre la malla WireGuard — sin intermediario central, sin cola y sin ningún servicio de terceros en el camino. Cada nodo de la flota recibe cada paquete simultáneamente; solo el nodo destinatario actúa.

Un crate aparte y más minimalista, `system-udp`, implementa un patrón de difusión relacionado pero distinto en el puerto UDP 8090, usando cargas JSON en lugar de este formato binario — los dos no son el mismo protocolo y no deben confundirse.

## Restricciones de diseño

El protocolo fue moldeado por tres requisitos que excluyen los enfoques convencionales:

**Sin intermediario.** Un intermediario de mensajes es un punto único de fallo y un problema de frontera de confianza — debe autenticarse, mantenerse y ser de confianza. El PPN Command Protocol elimina completamente al intermediario. El plano de control difunde; la malla entrega; el nodo decide.

**Sin texto en claro.** El protocolo se ejecuta exclusivamente sobre la malla WireGuard. El handshake IK del Noise Protocol de WireGuard autentica a cada par antes de que se entregue cualquier paquete. Un paquete de comandos nunca viaja por un enlace sin cifrar.

**Sin verbosidad.** Los comandos tienen 16 bytes. No hay negociación de sesión, ni handshake de reconocimiento, ni sobrecarga de enmarcado. En el nodo receptor, una lectura de 16 bytes coincide con una operación conocida o no lo hace.

## El formato del paquete

Cada comando tiene exactamente 16 bytes: un código de operación de 2 bytes, un identificador de nodo destino de 2 bytes, una marca de tiempo Unix de 4 bytes, y 8 bytes reservados en cero. No existe un campo de carga útil de longitud variable aparte — todo parámetro que el protocolo necesita hoy cabe en el formato fijo de código/destino/marca de tiempo. Hay tres operaciones definidas actualmente: PING, ISOLATE y PONG; cualquier otro código se trata como desconocido.

```
 0        2        4                 8                        16
 ┌────────┬────────┬─────────────────┬────────────────────────┐
 │ op (2) │dest.(2)│ marca tiempo (4)│  reservado, en cero (8) │
 └────────┴────────┴─────────────────┴────────────────────────┘
```

## La secuencia de despacho

1. El administrador escribe su intención en lenguaje natural en el terminal F8 — por ejemplo, instruyendo a la flota que aísle un nodo de borde específico.
2. `service-slm`, ejecutándose localmente, analiza la frase y produce el código de operación y el identificador del nodo destino.
3. `app-network-admin` construye el paquete completo de 16 bytes y lo difunde a través de la malla WireGuard en el puerto UDP 9206.
4. Cada nodo de la flota recibe el paquete simultáneamente. Solo el nodo cuya dirección coincide con el campo destino actúa; todos los demás descartan.

La capa de traducción es invisible en el límite del protocolo — la malla solo ve el comando binario, no la frase en lenguaje natural. `os-network-admin` en sí es un sondeador de aprobación de emparejamiento aparte y minimalista: vigila las solicitudes de unión de nodos pendientes y permite que un operador las apruebe, sin lógica de difusión de malla ni criptográfica propia. El flujo de traducción-autorización-difusión descrito arriba reside enteramente en `app-network-admin`.

## Por qué difusión simultánea

El modelo de difusión es deliberado. Un modelo de unidifusión requeriría que el plano de control mantuviera una tabla de enrutamiento con direcciones individuales para cada nodo, y requeriría sesiones TCP por nodo o reconocimientos. Ambos introducen estado que puede desincronizarse.

La difusión sobre una malla WireGuard elimina ambos problemas. Cada par recibe cada paquete. El nodo destinatario actúa; los demás descartan en la primera comparación de bytes. El plano de control no tiene estado de enrutamiento que mantener más allá de la lista de pares de la malla, que gestiona `app-network-admin`.

La restricción de seguridad está satisfecha por la propia malla: los no miembros no pueden recibir paquetes de la malla porque no poseen un handshake WireGuard válido con el hub.

## Relación con el Diode Standard

El PPN Command Protocol es la implementación en cable de la categoría de control descendente del [[diode-standard|Diode Standard]]. Fluye desde la autoridad (`app-network-admin`) hacia el sujeto (`os-infrastructure`) y nunca al revés. No existe un camino de comandos ascendente en el protocolo: el formato del paquete no contiene ninguna dirección de respuesta, ningún campo de reconocimiento y ningún mecanismo para que un nodo Sujeto inicie un paquete hacia la Autoridad.

La telemetría ascendente — logs, latidos, estado — viaja por un canal separado y estrictamente saneado. El canal de comandos y el canal de telemetría están desacoplados intencionalmente para que un fallo en uno no afecte al otro.

## Véase también

- `app-network-admin` — el crate de plano de control que produce y difunde los paquetes de comandos
- [[os-network-admin]] — el sondeador de aprobación de unión de nodos, un componente aparte; no el componente de difusión de malla
- [[os-infrastructure-ppn-node]] — los nodos de sustrato de cómputo que reciben y ejecutan los comandos
- [[diode-standard]] — la jerarquía de autoridad y las reglas de tráfico que implementa el protocolo
- [[sovereign-mesh]] — la superposición WireGuard sobre la que se ejecuta el protocolo
- [[service-slm]] — el enrutador semántico local que traduce la intención al código de operación de dos bytes
- [[machine-based-auth]] — los pares de claves fiduciarias que aseguran los pares de la malla
