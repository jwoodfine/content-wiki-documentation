---
schema: foundry-doc-v1
title: "Distribución Linux Ligera"
slug: lightweight-linux-distribution
category: reference
type: topic
content_type: topic
quality: complete
status: active
audience: customer-woodfine
bcsc_class: current-fact
language_protocol: TRANSLATE-ES
last_edited: 2026-07-31
editor: woodfine-editorial
short_description: "Distribución Linux diseñada para usar mucha menos RAM y capacidad de procesador que las distribuciones completas, apta para hardware limitado, embebido o heredado."
paired_with: lightweight-linux-distribution.md
tags:
  - domain:documentation
  - source:jennifer-cluster
  - batch:iteration-2
source_refs:
  - 10d76ed910fc7f26661a61d75019fc9a8ca52b47037443d73d2bbe924ade6cca
thesis_alignment: "Las distribuciones Linux ligeras son el sustrato para los appliances de software y las implementaciones de sistemas embebidos; comprender sus principios de diseño informa la arquitectura de imágenes de SO mínimas orientadas a appliances."
keynote: false
---

Una distribución Linux ligera es un sistema operativo basado en Linux diseñado para utilizar significativamente menos RAM y capacidad de procesador que las distribuciones Linux completas. La característica definitoria es la eficiencia de recursos: la distribución es capaz de ejecutarse en hardware con memoria limitada, velocidad de CPU restringida, o ambas.

## Ligereza como medida relativa

El concepto de distribución ligera no es absoluto sino relativo. Lo que constituye "ligero" depende de la generación de hardware considerada y de la carga de trabajo servida. Las distribuciones completas contemporáneas como Ubuntu con el entorno de escritorio Unity requieren aproximadamente 2 GB de RAM para funcionar cómodamente; las distribuciones ligeras pueden operar con tan solo 46 MB (Tiny Core Linux) o 24 MB (SliTaz) de RAM para uso interactivo de escritorio, y las distribuciones embebidas como OpenWrt requieren solo 32 MB de RAM para operación sin interfaz gráfica.

## El entorno de escritorio como factor principal de peso

El entorno de escritorio — la capa de interfaz gráfica de usuario que proporciona gestión de ventanas, barras de tareas, gestores de archivos y configuración del sistema — es el determinante más importante del consumo de recursos de una distribución Linux. Reemplazar un entorno completo como GNOME con una alternativa ligera como LXQt (utilizado por Lubuntu), Xfce (utilizado por Xubuntu) o el gestor de ventanas Openbox por sí solo puede reducir los requisitos de memoria de 2 GB a 128 MB o menos.

Esta observación tiene dos consecuencias prácticas. En primer lugar, una distribución que es "pesada" con un entorno de escritorio puede ser "ligera" con otro: Lubuntu 10.10, usando el escritorio LXDE, requería solo 128 MB de RAM y un procesador Pentium II, mientras que Ubuntu 10.10 con el shell Unity requería un procesador de doble núcleo a 2 GHz y 2 GB de RAM. En segundo lugar, muchas distribuciones ligeras se distinguen no por innovaciones únicas en el kernel o la gestión de paquetes, sino por su elección de entorno de escritorio y su conjunto de paquetes predeterminado.

## Distribuciones ligeras destacadas

**Alpine Linux** (2010) — Distribución de seguridad orientada a la ligereza que utiliza musl libc y BusyBox. Requiere 128 MB de RAM; su imagen de contenedor Docker es de aproximadamente 8 MB. Ampliamente utilizada como base para imágenes de contenedores.

**Tiny Core Linux** (2009) — Entre las distribuciones Linux funcionales más pequeñas, Tiny Core requiere tan solo 46 MB de RAM. Tres variantes: Core (11 MB, solo línea de comandos), TinyCore (16 MB, GUI mínima con FLTK) y CorePlus (106 MB, instalador completo).

**SliTaz** (2008) — Distribución Linux portátil con una imagen de disco de 50 MB que opera con 24 MB de RAM. Una variante llamada Tiny SliTaz (2016) requiere solo 4 MB de RAM.

**Puppy Linux** (2003) — Familia de distribuciones diseñadas para ejecutarse completamente desde RAM tras el arranque, usando el gestor de ventanas JWM. Requiere aproximadamente 256 MB de RAM.

**OpenWrt** (2004) — Distribución Linux para dispositivos de red embebidos, particularmente enrutadores domésticos. Requiere 32 MB de RAM y cabe en una imagen flash de 6 MB. Sin interfaz gráfica, gestionado mediante interfaz web o SSH.

**Alpine Linux, antiX, CRUX, Damn Small Linux, Gentoo** (32 MB, la instalación funcional más ligera), GoboLinux, LXLE, Nanolinux (64 MB de RAM, imagen de 19 MB, 2015), Porteus (36 MB de RAM, 260 MB, portátil), Salix OS, Slax, TurnKey Linux, VectorLinux Light, Void Linux y Zenwalk se encuentran entre las distribuciones que cubren todo el espectro de escenarios de implementación ligera.

### Variantes basadas en Ubuntu y de propósito especial

**Lubuntu** (LXQt, basado en Ubuntu) y **Xubuntu** (Xfce, basado en Ubuntu) son variantes ligeras de la distribución Ubuntu principal que mantienen la gestión de paquetes APT y los repositorios de software de Ubuntu, reduciendo los requisitos de hardware a aproximadamente 916 MB (Lubuntu) y 1 GB (Xubuntu) de RAM respectivamente.

**Lightweight Portable Security** (2011) — Distribución desarrollada por el Departamento de Defensa de EE. UU. para operaciones seguras en hardware no confiable. Basada en Arch Linux; imagen de aproximadamente 390 MB. Solo arranque en vivo; no almacena datos de sesión localmente.

**TurnKey Linux** (2008) — Biblioteca de appliances Linux específicos por aplicación, basados en Debian, cada uno preconfigurado como servidor sin interfaz gráfica. Requiere 256 MB de RAM; la imagen base es de 212 MB. Utilizado para el despliegue rápido de servidores.

## Categorías de implementación

Las distribuciones Linux ligeras se implementan en cuatro categorías principales:

**Computación de escritorio en hardware heredado.** Organizaciones e individuos con equipos más antiguos — laptops y escritorios fabricados antes de 2010 — usan distribuciones ligeras para extender la vida útil del hardware disponible.

**Sistemas operativos en vivo.** Las distribuciones ligeras se usan como entornos de arranque en vivo en USB o CD para operaciones de rescate, navegación sensible a la privacidad y acceso seguro a sistemas no confiables.

**Dispositivos embebidos y de red.** Distribuciones como OpenWrt se dirigen a enrutadores, conmutadores y otros dispositivos de red donde la RAM se mide en megabytes y el almacenamiento en kilobytes.

**Imágenes base para servidores y appliances.** Las distribuciones mínimas — en particular Alpine Linux — se usan como imágenes base para despliegues de contenedores y appliances de software, donde el tamaño total de la imagen afecta directamente la velocidad de despliegue y los costos de almacenamiento.

---

*citas: [[just-enough-operating-system]], [[virtual-appliance]], [[computer-appliance]]*
