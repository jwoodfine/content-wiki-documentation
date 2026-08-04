---
schema: foundry-doc-v1
title: "Genesis protocol"
slug: genesis-protocol
short_description: "El Genesis Protocol es la secuencia de arranque de flota ejecutada por cada nodo os-infrastructure en el primer arranque, permitiendo que los nodos alcancen un estado seguro y reclamable sin ninguna configuración previa ni dependencia del plano de control."
category: security
index_group: isolation-boundaries
type: topic
content_type: topic
status: stable
bcsc_class: public-disclosure-safe
language: es
language_protocol: TRANSLATE-ES
paired_with: genesis-protocol.md
last_edited: 2026-07-28
editor: pointsav-engineering
---

El Genesis Protocol es la secuencia de arranque inicial de flota que utiliza cada nodo `os-infrastructure` en su primer arranque. Permite que un nodo se vuelva operativo en hardware aislado — sin configuración previa, sin conexión a ningún plano de control y sin conocimiento de la flota a la que eventualmente se unirá — y que permanezca en un estado seguro y reclamable hasta que un administrador esté listo para incorporarlo a la gestión. El protocolo invierte el supuesto convencional de que el plano de control debe existir antes de que se pueda añadir cómputo a él.

**Corrección mayor (2026-07-28):** la secuencia de cinco pasos a continuación no
coincide con lo que el crate `os-infrastructure` real hace o construye actualmente. Dos
cosas son ciertas a la vez, y ninguna coincide con este artículo: (1)
`os-infrastructure/src/main.rs`, `forge_iso.sh` y `build_iso/` están explícitamente
etiquetados como "Existing scaffold" / "andamiaje original de construcción de ISO" en el
propio `CLAUDE.md` del crate — se conservan solo hasta que `moonshot-toolkit build` los
reemplace de extremo a extremo (tarea #14). Ese código Rust de bajo nivel no depende de
seL4 y no genera ninguna clave a partir de entropía de hardware. (2) La ruta *actual* del
crate (Opción B — GRUB2 → microkernel seL4 → dominio de protección CAmkES VMM → VM
invitada Linux, según el mismo `CLAUDE.md`) aún no ha superado su propia prueba de
compuerta D7 de malla de tres nodos, y su pila de red real —
`system-network-interface/src/lib.rs` — tiene `scan_for_peers()`,
`send_genesis_handshake()` y `conduct_pairing_ceremony()` implementados como
stubs explícitos (`scan_for_peers` siempre devuelve `NotFound`;
`send_genesis_handshake` siempre devuelve `false`; `system_status()` reporta literalmente
`"skeleton (NIC driver pending)"`). No se encontró ningún concepto de "clave fiduciaria"/
"entropía de hardware", ninguna "interfaz WebSocket reforzada" ni ningún protocolo de
baliza de puerto de malla PPN con la forma descrita abajo en ninguna de las dependencias
reales del crate. El mecanismo real diseñado (aún no construido) es materialmente
distinto de la historia de cinco pasos de este artículo: un protocolo de saludo UDP
`GenesisHandshakeFrame` seguido de un intercambio de claves CPace PAKE (RFC 9382), con un
código SAS Crockford base32 de 8 caracteres mostrado en el framebuffer e introducido por
el operador en el panel F12 de `app-console-keys` — no una clave que el kernel seL4
verifica silenciosamente. **Marcado como una discrepancia arquitectónica de todo el
artículo, no como una edición puntual** — esto puede ser un documento de diseño temprano
anterior a la dirección de implementación real del crate, o ambos simplemente han
divergido. Se necesita confirmación de project-totebox sobre el diseño actual/previsto
real del Genesis Protocol antes de corregir o reescribir este artículo — este es
claramente un hallazgo de clase REESCRITURA según la rúbrica de disposición, no una
corrección puntual.

## El problema que resuelve

La gestión convencional de flotas requiere una dependencia de secuenciación: el plano de control debe estar configurado, la red debe estar enrutada y el nodo debe estar inscrito antes de que sea útil. Para un operador que envía hardware a una ubicación remota, esto crea un problema de coordinación — el hardware llega al sitio remoto antes de que la capa de gestión de flotas esté lista, o viceversa.

El Genesis Protocol elimina la dependencia de secuenciación. Un nodo puede enviarse a cualquier ubicación, arrancar en cualquier entorno de red y alcanzar un estado seguro y autónomo sin ningún aprovisionamiento previo. El administrador lo reclama cuando esté listo.

## Los cinco pasos

### 1 — Arranque ciego

En el primer arranque, el kernel seL4 genera un par de claves fiduciarias de Nivel 1 a partir de entropía de hardware. A continuación, el nodo entra en modo de arranque ciego: deliberadamente ignora DHCP y DNS, rechazando adquirir una dirección de red mediante mecanismos convencionales. Esto impide que el nodo sea alcanzado por, o se comunique con, cualquier infraestructura que no haya verificado previamente.

### 2 — Exploración

El nodo explora la red local en busca de una baliza `os-network-admin` en el puerto de malla PPN. La exploración utiliza la clave pública fiduciaria del nodo como identidad que presenta — de modo que solo una instancia legítima de `os-network-admin` que posea el material de clave administrativa correspondiente puede responder con autoridad.

### 3 — Bifurcación génesis

Si la exploración no encuentra ninguna baliza `os-network-admin` dentro de la ventana de exploración, el nodo forma una Red Privada de Uno. Sella todos los puertos externos excepto uno, un único punto de acceso reforzado. No intenta contactar ningún servicio externo. No falla. Espera.

Un nodo que ha realizado la bifurcación génesis está completamente operativo: tiene su par de claves, tiene un perímetro de red sellado y está esperando una reclamación. No es un nodo defectuoso — es un nodo preparado para la flota que aún no ha sido reclamado.

### 4 — Patrón de espera

El único punto de acceso abierto es una interfaz WebSocket reforzada. Solo acepta una clase de mensaje: una solicitud de reclamación administrativa que presente un par de claves fiduciarias válido. Cualquier otro intento de conexión se descarta silenciosamente. El nodo no emite ninguna información identificativa a la red; para un observador externo, el punto de acceso es opaco.

### 5 — Reclamación

Cuando un administrador arranca `os-network-admin` y presenta la clave fiduciaria administrativa, el punto de acceso en patrón de espera verifica la clave contra el par de claves almacenado localmente en el nodo. Si el par verifica:

1. El nodo se vincula a la flota, aceptando la instancia de `os-network-admin` como su autoridad
2. El nodo recibe su configuración WireGuard de malla y se une a la [[sovereign-mesh|malla soberana]]
3. El par de claves fiduciarias del nodo se registra en el registro de emparejamiento de `os-network-admin` como emparejamiento ADMIN
4. Los puertos externos sellados se abren de acuerdo con la política del Diode Standard de la flota

Si la clave no verifica, la reclamación se rechaza silenciosamente. El nodo permanece en su patrón de espera y no emite ninguna respuesta de error.

## Ensamblaje de flota diferido

El Genesis Protocol está diseñado para el caso en que el hardware se envía antes de que el administrador esté listo para gestionarlo. Un operador puede enviar cincuenta servidores a cincuenta ubicaciones remotas. Cada uno llega, arranca y forma una PPN de un solo nodo. Cuando el administrador esté listo — días, semanas o meses después — `os-network-admin` reclama los cincuenta en secuencia. Cada uno verifica la reclamación y se une a la flota. El operador nunca necesita tocar físicamente los nodos después del envío inicial.

Este patrón funciona porque el patrón de espera es indefinidamente estable. Un nodo en patrón de espera consume energía mínima, mantiene su perímetro sellado y no presenta ninguna superficie de ataque más allá del punto de acceso de reclamación reforzado.

## Relación con la autorización basada en máquina

El Genesis Protocol es la fase de aprovisionamiento de la [[machine-based-auth|autorización basada en máquina]]. El par de claves fiduciarias generado en el primer arranque se convierte en la entrada de emparejamiento ADMIN de ese nodo en el registro de emparejamiento de la flota. Tras la reclamación:

- El material de clave del nodo es la única base para toda la autenticación posterior — nunca se transmite ninguna contraseña
- El emparejamiento puede revocarse eliminando la entrada ADMIN del registro; el nodo se vuelve ingobernable por la flota (aunque continúa ejecutando sus cargas de trabajo de forma autónoma)
- La autoridad de clave fiduciaria administrativa reside físicamente con el administrador — nunca se delega a un servicio en la nube

## Véase también

- [[infrastructure-os]] — el sustrato de cómputo que ejecuta el Genesis Protocol en el primer arranque
- [[os-network-admin]] — el plano de control que ejecuta la secuencia de reclamación
- [[sovereign-mesh]] — la superposición WireGuard a la que se une el nodo tras una reclamación exitosa
- [[machine-based-auth]] — el sistema de pares de claves fiduciarias en el que se basa el protocolo
- [[diode-standard]] — la jerarquía de autoridad que rige la flota después de la reclamación
