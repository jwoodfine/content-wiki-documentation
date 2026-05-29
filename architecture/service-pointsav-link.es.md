---
schema: foundry-doc-v1
title: "service-pointsav-link"
slug: service-pointsav-link
short_description: "service-pointsav-link es el adaptador hot-pluggable que conecta un nodo Sujeto os-* a una flota de PointSav, con un estado predeterminado de no instalado y un modo de fallo de desconexión limpia."
category: architecture
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: service-pointsav-link.md
language: es
---

`service-pointsav-link` es el adaptador hot-pluggable que conecta un nodo Sujeto [[os-family-overview|`os-*`]] a una flota de [[pointsav-overview|PointSav]]. Es el único código responsable de traducir los comandos de autoridad — emitidos por [[os-network-admin|`os-network-admin`]] y entregados a través del [[ppn-command-protocol|Protocolo de Comandos de la PPN]] — en operaciones ejecutables por el Sujeto. Su propiedad más importante es su estado predeterminado: no está instalado.

## Las cuatro propiedades

| Propiedad | Comportamiento |
|---|---|
| Estado predeterminado | No instalado; el Sujeto no tiene concepto de llamar a casa |
| Estado activado | Conectado en caliente por el operador con un único comando; pone el Sujeto bajo gestión de flota |
| Modo de fallo | Si el adaptador falla, el enlace se corta de forma limpia; el Sujeto continúa ejecutándose de forma independiente |
| Ruta de código | La política Diodo vive dentro del adaptador, no en el kernel del SO |

## Estado predeterminado: sin capacidad de llamar a casa

Un nodo [[infrastructure-os|`os-infrastructure`]] recién arrancado no tiene `service-pointsav-link` instalado. Esto no es una elección de configuración — es una invariante arquitectónica. El sistema operativo Sujeto no contiene código que le permita iniciar contacto con ninguna autoridad.

Esta propiedad se aplica a toda la [[os-family-overview|familia `os-*`]]. Poner un nodo bajo gestión es siempre una acción explícita del operador, nunca automática.

## Activación: conectar el adaptador en caliente

Un operador activa `service-pointsav-link` en un Sujeto con un único comando emitido desde [[os-network-admin|`os-network-admin`]]. La secuencia de activación instala el paquete `pointsav-protocol`, registra el par de claves fiduciarias del nodo en el [[pairing-as-permission|registro de emparejamiento]] de la flota como entrada de Sujeto, y abre el único canal de comandos entrantes del adaptador.

## Modo de fallo: desconexión limpia

Si `service-pointsav-link` falla o se desinstala deliberadamente, el Sujeto no falla. Continúa ejecutando sus cargas de trabajo como si la gestión de flota nunca hubiera estado presente. Esto garantiza que un fallo del plano de control sea una pérdida de observabilidad, no una interrupción del servicio.

## El Estándar Universal

`service-pointsav-link` no es una característica de un sistema operativo específico. El mismo paquete `pointsav-protocol`, con diferentes vinculaciones de política, es el adaptador entre cualquier par de instancias de SO de [[pointsav-overview|PointSav]] que necesiten comunicarse.

## Véase también

- [[diode-standard]] — la jerarquía de autoridad y las reglas de tráfico que el adaptador aplica
- [[ppn-command-protocol]] — el formato de cable binario de 16 bytes que recibe el adaptador
- [[genesis-protocol]] — la fase de aprovisionamiento que precede a la activación del adaptador
- [[machine-based-auth]] — los pares de claves fiduciarias que autentican el canal de comandos del adaptador
