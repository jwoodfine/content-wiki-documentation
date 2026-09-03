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
last_edited: 2026-08-06
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
- [[totebox-os]] — La capa de archivo: un vault aislado a nivel de kernel por entidad, que almacena registros como archivos planos inertes sin operación de eliminación, expuestos únicamente a través del Diode bajo comando de os-console u os-orchestration.
- [[totebox-orchestration|Orquestación Totebox]] — La capa de coordinación que gestiona múltiples contenedores de archivo de datos Totebox, manteniendo los motores de ejecución de software aislados de los libros corporativos pasivos a través de los despliegues.
- [[vm-architecture|Arquitectura VM-*]] — Los cinco tipos de VM nombrados (Totebox, MediaKit, Orchestration, PrivateGit, Infrastructure) y cómo cada uno corresponde exactamente a un binario fuente `os-*`.
- [[scaling-coordinated-development-totebox-archives|Escalar el desarrollo coordinado en múltiples Totebox Archives]] — Los cuellos de botella de coordinación que aparecen pasadas un par de docenas de archivos, y la trayectoria hacia el aislamiento de procesos por archivo.
- [[os-totebox-sovereign-archive|os-totebox: la bóveda soberana de datos WORM]] — El diseño final previsto de os-totebox como sistema operativo de Tipo I sobre seL4: la bóveda de datos WORM impuesta por un grafo de capacidades compilado, no por una política que un administrador pudiera anular.
- [[os-totebox-service-pd-model|Cómo los service-* se convierten en dominios de protección seL4]] — Cómo os-totebox está diseñado para asignar sus binarios de servicio Rust a siete Dominios de Protección seL4, con un confinamiento de capacidades que garantiza que un PD de service-slm comprometido nunca pueda alcanzar el PD de service-fs que retiene el almacenamiento.
<!-- END AUTO-GENERATED -->

## Superficies del operador

Los sistemas a través de los cuales un operador humano interactúa con la plataforma — controlados por teclado, estructurados por teclas F y construidos en torno a la memoria muscular en lugar de la descubribilidad.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: operator-surfaces -->
- [[os-console]] — La superficie orientada al ser humano: un Libro Mayor de Comandos y binario Rust único que se conecta a un Totebox y renderiza su estado a través de una interfaz controlada por teclado, basada en cartuchos y estructurada por teclas F.
- [[os-console-totebox-browser]] — El explicador de la analogía del navegador para la filosofía de diseño de os-console: cartuchos como pestañas, emparejamiento de máquinas como el almacén de certificados.
- [[input-machine|Máquina de entrada]] — La puerta de ingesta obligatoria de documentos en os-console, vinculada permanentemente a F12 y respaldada por `service-input` en el Archivo Totebox.
- [[os-workplace]] — El nivel de escritorio gratuito: una familia creciente de aplicaciones independientes en Rust y Tauri que se emparejan con un archivo Totebox y sirven como puerta de entrada de adopción a la línea de producto comercial.
- [[os-orchestration]] — El Agregador de Flota para carteras de múltiples entidades: un operador ve, consulta y comanda muchos archivos Totebox a la vez.
<!-- END AUTO-GENERATED -->

## Control de red e infraestructura

Los sistemas que gestionan el tejido de red, la ruta de arranque y el sustrato de cómputo subyacente.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: network-control-and-infrastructure -->
- [[os-network-admin]] — El plano de control de una flota: gestiona el registro de emparejamientos, las reglas Diode y la política de enrutamiento de malla; los comandos se transmiten como paquetes binarios de 16 bytes a través de la malla WireGuard.
- [[os-privategit]] — Alojamiento Git privado para control de versiones soberano dentro de una flota.
- [[app-privategit-workbench|Workbench de navegador]] — El editor de archivos basado en navegador incluido en os-privategit: una interfaz de tres columnas para trabajar con archivos sin una sesión de terminal.
- [[os-infrastructure-ppn-node|os-infrastructure: sistema operativo de nodo PPN]] — La capa de sistema operativo para los nodos PPN: gestiona túneles WireGuard, aloja las VMs invitadas de los demás servicios de la plataforma y ejecuta la ceremonia de incorporación del Protocolo Génesis.
<!-- END AUTO-GENERATED -->

## Publicación y medios

El SO orientado al público que aloja la superficie de marketing de la empresa, el wiki interno y la sala de prensa de cumplimiento en un único dispositivo soberano.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: publishing-and-media -->
- [[os-mediakit]] — La imagen del SO invitado para el nivel vm-mediakit, que aísla los wikis de conocimiento, los sitios de marketing, el corrector de pruebas y la orquestación BIM de los niveles de bóveda y orquestación. Ubuntu 24.04 hoy; una imagen seL4 Microkit es la forma prevista a largo plazo.
<!-- END AUTO-GENERATED -->

## Véase también

- [Cómo Está Construido](/architecture/) — arquitectura transversal de la plataforma y el modelo de tres anillos
- [Servicios de la Plataforma](/services/) — los servicios autónomos que se ejecutan dentro y a través de los sistemas operativos
- [Dónde Se Ejecuta](/infrastructure/) — topología de despliegue de flota y entorno operativo en la nube
- [Bloques de Construcción](/substrate/) — las disciplinas de sustrato y las primitivas del microkernel que hereda la familia de SO
