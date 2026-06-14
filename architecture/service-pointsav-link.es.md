---
schema: foundry-doc-v1
title: "service-pointsav-link"
slug: service-pointsav-link
short_description: "service-pointsav-link es el adaptador hot-pluggable que conecta un nodo Sujeto os-* a una flota PointSav, con un estado predeterminado de no instalado y un modo de fallo de separación limpia."
category: architecture
type: topic
content_type: topic
status: active
bcsc_class: public-disclosure-safe
language: es
language_protocol: TRANSLATE-ES
paired_with: service-pointsav-link.md
last_edited: 2026-05-30
editor: editorial
---

`service-pointsav-link` es el adaptador de conexión en caliente que conecta un nodo Sujeto `os-*` a una flota PointSav. Es el único código responsable de traducir los comandos de autoridad — emitidos por `os-network-admin` y entregados a través del [[ppn-command-protocol|PPN Command Protocol]] — en operaciones ejecutables por el Sujeto. El adaptador se distribuye como el paquete `pointsav-protocol`. Su propiedad más importante es su estado predeterminado: no está instalado. Un Sujeto sin `service-pointsav-link` no tiene ningún concepto de llamar a casa, recibir comandos o participar en la gestión de flota.

## Las cuatro propiedades

| Propiedad | Comportamiento |
|---|---|
| Estado predeterminado | No instalado; el Sujeto no tiene ningún concepto de llamar a casa |
| Estado activado | Conectado en caliente por el operador con un solo comando; pone al Sujeto bajo gestión de flota |
| Modo de fallo | Si el adaptador falla, el enlace se corta limpiamente; el Sujeto continúa ejecutándose de forma autónoma; la superficie de gestión de flota queda oscura |
| Ruta de código | La política del Diode Standard reside dentro del adaptador, no en el kernel del sistema operativo — la política puede actualizarse sin tocar el resto del sistema |

## Estado predeterminado: sin capacidad de llamar a casa

Un nodo `os-infrastructure` recién arrancado no tiene instalado `service-pointsav-link`. Esto no es una elección de configuración — es un invariante arquitectónico. El sistema operativo Sujeto no contiene ningún código que le permita iniciar contacto con ninguna autoridad. No hay cliente `ssh`, ni tabla de enrutamiento entre pares, ni iniciador RPC. El Sujeto es estructuralmente incapaz de llamar a casa.

Esta propiedad se cumple en toda la familia `os-*`. Cada Sujeto — `os-totebox`, `os-mediakit`, `os-privategit`, `os-infrastructure` y `os-network-admin` cuando actúa como Sujeto — comienza en un estado en el que la gestión de flota está ausente. Poner un nodo bajo gestión es siempre una acción explícita del operador, nunca automática.

## Activación: conectar el adaptador en caliente

Un operador activa `service-pointsav-link` en un Sujeto con un solo comando emitido desde `os-network-admin`. La secuencia de activación instala el paquete `pointsav-protocol`, registra el par de claves fiduciarias del nodo en el registro de emparejamiento de la flota como una entrada de Sujeto, y abre el único canal de comandos entrantes del adaptador.

Tras la activación, el Sujeto se vuelve direccionable por la difusión de comandos de la flota. El canal entrante del adaptador escucha en la malla PPN y acepta solo los paquetes cuyo código de operación está dentro del conjunto permitido definido por la política del [[diode-standard|Diode Standard]] de la flota. Todo el demás tráfico se descarta en el límite del adaptador.

## Modo de fallo: separación limpia

Si `service-pointsav-link` falla o se desinstala deliberadamente, el Sujeto no colapsa. Continúa ejecutando sus cargas de trabajo — sirviendo contenido, ejecutando cómputos, manteniendo su estado local — como si la gestión de flota nunca hubiera estado presente. La superficie de gestión de flota queda oscura: `os-network-admin` pierde visibilidad del Sujeto y no puede emitirle comandos. Pero los servicios propios del Sujeto no se ven afectados.

Este modo de fallo es por diseño. Un Sujeto que dependiera del adaptador para su operación normal estaría permanentemente acoplado al plano de control — cualquier interrupción del plano de control se propagaría a las cargas de trabajo del Sujeto. Al desacoplar la operación del Sujeto de la presencia del adaptador, `service-pointsav-link` garantiza que un fallo del plano de control sea una pérdida de observabilidad, no una interrupción del servicio.

## La política en el adaptador, no en el kernel

La política del [[diode-standard|Diode Standard]] — qué flujos de comandos están permitidos, qué operaciones se permiten desde qué autoridades, qué telemetría se emite — reside dentro de `service-pointsav-link`, no en el kernel del sistema operativo Sujeto. Esta separación tiene una consecuencia práctica: actualizar la política de flota requiere actualizar el adaptador, no reconstruir ni reiniciar el sistema operativo.

Una versión del sistema operativo Sujeto y una actualización de política del Diode Standard son despliegues independientes. Un operador puede endurecer o relajar la política de flota enviando una nueva versión del paquete `pointsav-protocol` a los Sujetos activos sin tocar ningún código del kernel.

## El estándar universal

`service-pointsav-link` no es una característica de un sistema operativo específico. El mismo paquete `pointsav-protocol`, con diferentes vinculaciones de política, es el adaptador entre cualquier par de instancias del sistema operativo PointSav que necesiten comunicarse. Un Sujeto `os-totebox` conectado a una Autoridad `os-console` utiliza la misma ruta de código del adaptador que un Sujeto `os-infrastructure` conectado a `os-network-admin`.

Este estándar uniforme es lo que hace auditable una flota compleja. Cada conexión tiene el mismo aspecto en la capa del protocolo. Un auditor que examine cualquier par de nodos conectados ve la misma forma del adaptador — el mismo comportamiento predeterminado desactivado, la misma secuencia de activación, la misma garantía de separación limpia.

## Véase también

- [[diode-standard]] — la jerarquía de autoridad y las reglas de tráfico que aplica el adaptador
- [[os-network-admin]] — la Autoridad que activa y ordena a los Sujetos a través del adaptador
- [[infrastructure-os]] — un Sujeto os-infrastructure que usa este adaptador para unirse a una flota
- [[ppn-command-protocol]] — el formato de cable binario de 16 bytes que recibe el adaptador
- [[machine-based-auth]] — los pares de claves fiduciarias que autentican el canal de comandos del adaptador
