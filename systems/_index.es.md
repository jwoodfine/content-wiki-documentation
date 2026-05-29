---
schema: foundry-doc-v1
title: "Sistemas"
slug: _index.es
short_description: "Los sistemas operativos de propósito específico que comparten un sustrato seL4 y Rust común — Totebox, Console, Workplace, Orchestration, Infrastructure, Network Admin, MediaKit y PrivateGit — cada uno realizando un trabajo, sin características que no necesita, y comunicándose a través de una disciplina de protocolo común basada en Diode."
lang: es
category: systems
type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-29
editor: pointsav-engineering
paired_with: _index.md
---

PointSav construye una familia de sistemas operativos de propósito específico que comparten un sustrato común de seL4 y Rust. Cada uno hace un trabajo, no contiene funciones que no necesita, y se comunica a través de una disciplina de protocolo Diode común. El resultado es una familia que puede auditarse componente por componente, actualizarse de forma independiente y desplegarse en cualquier configuración sin acoplamiento inesperado entre sistemas.

[[os-family-overview|Visión general de la familia de SO]] es el punto de entrada para los lectores nuevos en la familia — explica el sustrato común, el modelo de [[capability-based-security|seguridad basada en capacidades]] que hereda cada SO, el [[diode-standard|estándar Diode]] que rige cómo se comunican y el [[sel4-microkernel-substrate|sustrato del microkernel seL4]] que los ancla a un kernel L1 formalmente verificado matemáticamente.

## La capa de archivo

Los sistemas centrales de mantenimiento de registros en la base de cada despliegue — donde vive el registro canónico y cómo se coordina a través de una flota.

- [[totebox-os]] — La capa de archivo: un vault aislado a nivel de kernel por entidad, que almacena registros como archivos planos inertes sin operación de eliminación, expuestos únicamente a través del Diode bajo comando de os-console u os-orchestration.
- [[totebox-archive|Archivo Totebox]] — Una máquina virtual micro-autónoma y libremente transferible que persiste datos institucionales como archivos planos inmutables.
- [[totebox-orchestration|Orquestación Totebox]] — La capa de coordinación que gestiona múltiples contenedores de archivo de datos Totebox, manteniendo los motores de ejecución de software aislados de los libros corporativos pasivos a través de los despliegues.

## Superficies del operador

Los sistemas a través de los cuales un operador humano interactúa con la plataforma — controlados por teclado, estructurados por teclas F y construidos en torno a la memoria muscular en lugar de la descubribilidad.

- [[console-os]] — La superficie orientada al ser humano: un Libro de Comandos que se conecta a un Totebox y renderiza su estado a través de una interfaz controlada por teclado y teclas F.
- [[os-console-platform|Plataforma os-console]] — El binario Rust que implementa os-console: arquitectura de cartuchos, módulos navegados por teclas F, acceso nativo por teclado a los flujos de trabajo del Archivo Totebox.
- [[input-machine|Máquina de entrada]] — La puerta de ingesta obligatoria de documentos en os-console, vinculada permanentemente a F12 y respaldada por `service-input` en el Archivo Totebox.
- [[os-workplace]] — El sistema operativo de escritorio gratuito: un escritorio soberano nativo en Rust que se empareja con un archivo Totebox y sirve como puerta de entrada de adopción a la línea de producto comercial.
- [[os-orchestration]] — El Agregador de Flota para carteras de múltiples entidades: un operador ve, consulta y comanda muchos archivos Totebox a la vez.

## Control de red e infraestructura

Los sistemas que gestionan el tejido de red, la ruta de arranque y el sustrato de cómputo subyacente.

- [[infrastructure-os]] — El sustrato de cómputo que aloja los sistemas operativos PointSav en hardware on-premises, arrendado y en la nube; arranca flotas aisladas a través del Protocolo Génesis.
- [[os-network-admin]] — El plano de control de una flota: gestiona el registro de emparejamientos, las reglas Diode y la política de enrutamiento de malla; los comandos se transmiten como paquetes binarios de 16 bytes a través de la malla WireGuard.
- [[os-privategit]] — Alojamiento Git privado para control de versiones soberano dentro de una flota.
- [[os-privategit-workbench|Workbench de os-privategit]] — El editor de archivos basado en navegador incluido en os-privategit: una interfaz de tres columnas para trabajar con archivos sin una sesión de terminal.

## Publicación y medios

El SO orientado al público que aloja la superficie de marketing de la empresa, el wiki interno y la sala de prensa de cumplimiento en un único dispositivo soberano.

- [[mediakit-os]] — El SO orientado al público: aloja el sitio web de marketing de una empresa, el wiki interno y la sala de prensa de cumplimiento en un único dispositivo soberano propiedad de la empresa.

## Véase también

- [Arquitectura](/architecture/) — arquitectura transversal de la plataforma y el modelo de tres anillos
- [Servicios](/services/) — los servicios autónomos que se ejecutan dentro y a través de los sistemas operativos
- [Infraestructura](/infrastructure/) — topología de despliegue de flota y entorno operativo en la nube
- [Sustrato](/substrate/) — las disciplinas de sustrato y las primitivas del microkernel que hereda la familia de SO
