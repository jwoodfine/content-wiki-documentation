---
schema: foundry-doc-v1
title: "Sistemas Operativos"
slug: systems-index
short_description: "Los sistemas operativos de propósito específico que comparten un sustrato seL4 y Rust común — Totebox, Console, Workplace, Orchestration, Infrastructure, Network Admin, MediaKit y PrivateGit — cada uno realizando un trabajo, sin características que no necesita, y comunicándose a través de una disciplina de protocolo común basada en Diode."
lang: es
category: systems
type: topic
content_type: topic
quality: complete
index_type: thematic
index_scope: systems
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-09-04
editor: pointsav-engineering
paired_with: _index.md
---

PointSav construye una familia de sistemas operativos de propósito específico que comparten un sustrato común de seL4 y Rust. Cada uno hace un trabajo, no contiene funciones que no necesita, y se comunica a través de una disciplina de protocolo Diode común. El resultado es una familia que puede auditarse componente por componente, actualizarse de forma independiente y desplegarse en cualquier configuración sin acoplamiento inesperado entre sistemas.

<!-- START-HERE-HIGHLIGHT: el motor lee este bloque para la tarjeta "empezar aquí"
     (reutiliza el componente cluster-card--start-here existente). No añadir más de una. -->

**Empiece aquí:** [[os-family-overview|Visión general de la familia de SO]] — el punto de entrada para los lectores nuevos en la familia; explica el sustrato común, el modelo de [[capability-based-security|seguridad basada en capacidades]] que hereda cada SO, el [[diode-standard|estándar Diode]] que rige cómo se comunican y el [[sel4-microkernel-substrate|sustrato del microkernel seL4]] que los ancla a todos.

<!-- END-START-HERE-HIGHLIGHT -->

## La capa de archivo

Los sistemas centrales de mantenimiento de registros en la base de cada despliegue — donde vive el registro canónico y cómo se coordina a través de una flota.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: the-archive-layer -->
- [[totebox-os]] — os-totebox es la capa de archivo de la familia PointSav — una bóveda aislada por entidad, que almacena registros como archivos planos inertes sin operación de borrado y los expone únicamente a través del Diodo bajo comando de os-console u os-orchestration. Su vía de producción aloja un invitado Linux bajo el micronúcleo seL4; existen otras formas de host para compatibilidad y desarrollo local.
- [[totebox-orchestration|Orquestación Totebox]] — Totebox Orchestration describe la capa de coordinación que administra múltiples contenedores de archivo de datos Totebox, manteniendo motores de ejecución de software aislados de libros mayores corporativos pasivos en implementaciones.
- [[vm-architecture|Arquitectura VM-*]] — La plataforma PointSav organiza sus despliegues en tiempo de ejecución en cinco tipos de máquinas virtuales — VM-Totebox, VM-MediaKit, VM-Orchestration, VM-PrivateGit y VM-Infrastructure — cada uno correspondiendo exactamente a un binario fuente os-*.
- [[scaling-coordinated-development-totebox-archives|Escalar el desarrollo coordinado en múltiples Totebox Archives]] — Cuellos de botella de coordinación más allá de veinte archivos — serialización de publicaciones, latencia de mensajes, carga del operador y aislamiento por proceso.
- [[os-totebox-sovereign-archive|os-totebox: la bóveda soberana de datos WORM]] — os-totebox está diseñado para convertirse en un sistema operativo de Tipo I sobre hardware físico, construido sobre el micronúcleo seL4 formalmente verificado — el estado final previsto, no el software que se ejecuta hoy.
- [[os-totebox-service-pd-model|Cómo los service-* se convierten en dominios de protección seL4]] — Explica cómo os-totebox está diseñado para asignar binarios de servicio Rust a dominios de protección seL4 — la pila planificada de siete PDs, trabajo de la Fase H1 de la hoja de ruta, no el binario que se ejecuta hoy.
<!-- END AUTO-GENERATED -->

## Superficies del operador

Los sistemas a través de los cuales un operador humano interactúa con la plataforma — controlados por teclado, estructurados por teclas F y construidos en torno a la memoria muscular en lugar de la descubribilidad.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: operator-surfaces -->
- [[os-console]] — os-console es la superficie de cara al operador de la plataforma PointSav — un Libro Mayor de Comandos, en un único binario nativo de teclado, que se conecta a un Totebox y aloja cartuchos TUI independientes mediante un chasis unificado.
- [[os-console-totebox-browser]] — os-console-totebox-browser se ha incorporado a la sección propia de os-console 'Por qué este diseño: la analogía del navegador' — este artículo es ahora un breve puntero, no un análisis independiente.
- [[input-machine|Máquina de entrada]] — La Máquina de Entrada es la puerta obligatoria de incorporación de documentos en os-console, asignada permanentemente a F12 y respaldada por service-input en el Archivo Totebox.
- [[os-workplace]] — os-workplace es el nivel de escritorio gratuito previsto en la familia PointSav — hoy, un conjunto creciente de aplicaciones independientes en Rust y Tauri que el operador ejecuta en su propio equipo, incorporándose a la red como un par WireGuard station-*; la puerta de entrada prevista a la línea comercial.
- [[os-orchestration]] — os-orchestration es el sistema operativo de nivel comercial que permite a un único operador ver, consultar y comandar muchos archivos Totebox a la vez — el Agregador de Flota para portafolios multi-entidad y despliegues empresariales.
<!-- END AUTO-GENERATED -->

## Control de red e infraestructura

Los sistemas que gestionan el tejido de red, la ruta de arranque y el sustrato de cómputo subyacente.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: network-control-and-infrastructure -->
- [[os-network-admin]] — os-network-admin es el plano de control de una Red Privada PointSav — proporciona enrutamiento de malla WireGuard, la superficie de ceremonia de unión de nodos y la aplicación del Diode Standard, sin poseer ninguna autoridad criptográfica del nivel de archivo.
- [[os-privategit]] — La capa de sistema operativo que aloja la infraestructura Git privada que sustenta el espacio de trabajo de desarrollo, flujo de commit de nivel de staging y repositorios de fuente canónica para todos los repos de ingeniería de PointSav.
- [[app-privategit-workbench|Workbench de navegador]] — El editor de archivos basado en navegador incluido en os-privategit: una interfaz de tres columnas para trabajar con archivos sin una sesión de terminal.
- [[os-infrastructure-ppn-node|os-infrastructure: sistema operativo de nodo PPN]] — os-infrastructure es la capa del sistema operativo para los nodos de la Red Privada PointSav — su único propósito es configurar, operar y mantener un nodo PPN: gestionar túneles WireGuard, alojar máquinas virtuales y exponer el plano de control del operador.
<!-- END AUTO-GENERATED -->

## Publicación y medios

El SO orientado al público que aloja la superficie de marketing de la empresa, el wiki interno y la sala de prensa de cumplimiento en un único dispositivo soberano.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: publishing-and-media -->
- [[os-mediakit]] — El nivel web público de la familia de SO PointSav — os-mediakit posee TLS, el ciclo de vida systemd y el acceso a datos mediado por la puerta de enlace; app-mediakit-knowledge/marketing/distribution poseen la lógica de dominio. Ubuntu 24.04 hoy; el estado final previsto es una VM seL4 por instancia de despliegue, no un dispositivo combinado único.
<!-- END AUTO-GENERATED -->

## Véase también

- [Cómo Está Construido](/architecture/) — arquitectura transversal de la plataforma y el modelo de tres anillos
- [Servicios de la Plataforma](/services/) — los servicios autónomos que se ejecutan dentro y a través de los sistemas operativos
- [Dónde Se Ejecuta](/infrastructure/) — topología de despliegue de flota y entorno operativo en la nube
- [Bloques de Construcción](/substrate/) — las disciplinas de sustrato y las primitivas del microkernel que hereda la familia de SO
