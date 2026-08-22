---
schema: foundry-doc-v1
title: "Genesis protocol"
slug: genesis-protocol
short_description: "El Genesis Protocol es la secuencia diseñada de arranque de flota para nodos os-infrastructure: enviarse sin configuración previa, arrancar en cualquier red y alcanzar un estado seguro y reclamable sin necesitar contacto con el plano de control."
category: security
index_group: isolation-boundaries
type: topic
content_type: topic
status: stable
bcsc_class: public-disclosure-safe
language: es
language_protocol: TRANSLATE-ES
paired_with: genesis-protocol.md
last_edited: 2026-08-22
editor: pointsav-engineering
---

El Genesis Protocol es la secuencia diseñada de arranque para un nodo `os-infrastructure`. Permite que un nodo se envíe a cualquier ubicación, se encienda sin configuración previa ni conexión a un plano de control, y alcance un estado seguro y reclamable que espera a un administrador en lugar de buscarlo. El protocolo invierte el orden habitual: en vez de que el plano de control exista antes de que el cómputo pueda unirse a él, el cómputo existe primero y espera a ser encontrado.

Un nodo enviado así no necesita aprovisionamiento previo y no expone nada a la red mientras espera. Un administrador puede reclamar cincuenta nodos enviados a cincuenta ubicaciones cuando esté listo, días o meses después, sin tocar ninguno de ellos mientras tanto.

## Cómo funciona

La secuencia completa está diseñada y documentada en la pila de red del nodo, pero aún no es operativa — el trabajo del controlador de red del que depende todavía no está listo. Una vez construida, funcionará en cinco etapas:

1. **Descubrimiento.** El nodo busca un servidor de emparejamiento en la red local (una consulta mDNS), y recurre a una dirección de retransmisión preconfigurada si nadie responde dentro de la ventana de descubrimiento. Si no encuentra ninguno, espera — este es el estado esperado para un nodo que aguarda ser reclamado, no un fallo.
2. **Saludo.** Si un servidor de emparejamiento responde, el nodo envía un fotograma de saludo por UDP que lleva un código corto de 8 caracteres (Crockford base32).
3. **Intercambio de claves.** Un intercambio de claves autenticado por contraseña CPace (RFC 9382) sigue al saludo. La clave de sesión resultante deriva una cadena corta de autenticación de 5 bytes, mostrada en el framebuffer del nodo.
4. **Ceremonia.** El nodo registra una solicitud de reclamación ante el servicio de emparejamiento y sondea el resultado — hasta diez minutos — mientras un administrador revisa el código y aprueba o deniega desde su propia consola.
5. **Reclamación.** Al aprobarse, el nodo recibe su configuración de malla y se une a la [[sovereign-mesh|red privada]], siguiendo la misma ceremonia de incorporación que ejecuta [[os-network-admin]] del lado del administrador.

**Nada de lo anterior está activo todavía.** Cada paso del código actual es un marcador de posición explícito: el descubrimiento de pares siempre reporta "no encontrado," el envío del saludo siempre reporta fallo, y la cadena de estado del propio crate es "skeleton — controlador NIC pendiente." Esto describe el mecanismo previsto una vez completado el trabajo del controlador de red, no el comportamiento actual del nodo.

## Por qué importa la secuenciación

La gestión convencional de flotas exige que el plano de control exista, esté enrutado y listo antes de que un nodo pueda unirse — un problema de coordinación cuando el hardware llega a un sitio antes de que la capa de gestión esté lista, o al revés. El Genesis Protocol elimina esa dependencia: el nodo no necesita que la flota exista todavía, solo que eventualmente lo encuentre.

## Relación con la autorización basada en máquina

Una vez construido, una reclamación exitosa será el punto de entrada a la [[machine-based-auth|autorización basada en máquina]]: la aprobación de la ceremonia de incorporación es lo que registra por primera vez al nodo en el sistema de emparejamiento de la flota, el mismo mecanismo que rige toda autenticación posterior.

## Véase también

- [[os-infrastructure-ppn-node]] — el nodo que ejecuta el Genesis Protocol en el primer arranque
- [[os-network-admin]] — el plano de control que ejecuta el lado de reclamación/aprobación de la ceremonia
- [[sovereign-mesh]] — la superposición de red privada a la que se une un nodo tras una reclamación exitosa
- [[machine-based-auth]] — el sistema de autenticación al que entra un nodo reclamado
