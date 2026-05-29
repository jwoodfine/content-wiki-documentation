---
schema: foundry-doc-v1
title: "El Protocolo Génesis"
slug: genesis-protocol
short_description: "El Protocolo Génesis es la secuencia de arranque de flota ejecutada por cada nodo os-infrastructure en el primer arranque, permitiendo que los nodos alcancen un estado seguro y reclamable sin ninguna configuración previa ni dependencia del plano de control."
category: architecture
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: genesis-protocol.md
language: es
---

El Protocolo Génesis es la secuencia de arranque de flota utilizada por cada nodo [[infrastructure-os|`os-infrastructure`]] en el primer arranque. Permite que un nodo se vuelva operacional en hardware aislado — sin configuración previa, sin conexión a ningún plano de control y sin conocimiento de la flota a la que eventualmente se unirá — y permanezca en un estado seguro y reclamable hasta que un administrador esté listo para ponerlo bajo gestión.

## El problema que resuelve

La gestión convencional de flotas requiere una dependencia de secuenciación: el plano de control debe estar configurado, la red debe estar enrutada y el nodo debe estar inscrito antes de que el nodo sea útil. El Protocolo Génesis elimina esta dependencia. Un nodo puede enviarse a cualquier ubicación, arrancar en cualquier entorno de red y alcanzar un estado seguro y autónomo sin ningún aprovisionamiento previo.

## Los cinco pasos

**1 — Arranque ciego.** En el primer arranque, el [[sel4-microkernel-substrate|kernel seL4]] genera un par de claves fiduciarias de Nivel 1 a partir de entropía de hardware. El nodo entra en modo de arranque ciego: ignora deliberadamente DHCP y DNS.

**2 — Exploración.** El nodo explora la red local en busca de una baliza de [[os-network-admin|`os-network-admin`]] en el puerto de malla.

**3 — Bifurcación Génesis.** Si la exploración no encuentra ninguna baliza de `os-network-admin` dentro del período de exploración, el nodo forma una [[pointsav-private-network|Red Privada]] de Uno. Sella todos los puertos externos excepto un único punto de acceso reforzado.

**4 — Patrón de espera.** El único punto de acceso abierto es una interfaz WebSocket reforzada que acepta únicamente solicitudes de reclamación administrativa que presenten un par de claves fiduciarias válido.

**5 — Reclamación.** Cuando un administrador arranca [[os-network-admin|`os-network-admin`]] y presenta la clave fiduciaria administrativa, el punto de acceso en patrón de espera verifica la clave. Si el par se verifica: el nodo se une a la flota; recibe su configuración de malla WireGuard y se une a la [[sovereign-mesh|malla soberana]]; su par de claves fiduciarias se registra en el [[pairing-as-permission|registro de emparejamiento]] de `os-network-admin` como emparejamiento ADMIN.

## Ensamblaje de flota diferido

El Protocolo Génesis está diseñado para el caso en que el hardware se envía antes de que el administrador esté listo para gestionarlo. Un operador puede enviar cincuenta servidores a cincuenta ubicaciones remotas. Cada uno llega, arranca y forma una Red Privada de Uno. Cuando el administrador esté listo — días, semanas o meses después — `os-network-admin` los reclama en secuencia. El operador nunca necesita volver a tocar físicamente los nodos después del envío inicial.

## Véase también

- [[infrastructure-os]] — el sustrato de cómputo que ejecuta el Protocolo Génesis en el primer arranque
- [[sovereign-mesh]] — la superposición WireGuard a la que el nodo se une tras una reclamación exitosa
- [[machine-based-auth]] — el sistema de par de claves fiduciarias en el que se basa el protocolo
- [[service-pointsav-link]] — el adaptador que pone el nodo bajo la gestión de la flota
