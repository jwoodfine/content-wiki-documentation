---
schema: foundry-doc-v1
title: "Sistemas"
slug: _index.es
lang: es
category: systems
type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: _index.md
---

PointSav construye ocho sistemas operativos de propósito específico que comparten un sustrato común de seL4 y Rust. Cada uno hace un trabajo, no contiene funciones que no necesita, y se comunica a través de una disciplina de protocolo Diode común. El resultado es una familia que puede auditarse componente por componente, actualizarse de forma independiente y desplegarse en cualquier configuración sin acoplamiento inesperado entre sistemas.

[[os-family-overview]] es el punto de entrada para los lectores nuevos en la familia. Explica el sustrato común, el modelo de capacidades que hereda cada SO y la regla Diode que rige su comunicación.

## La capa de archivo

Los sistemas de gestión de registros fundamentales en la base de cada despliegue.

- [[totebox-os]] — La capa de archivo: un vault de nivel de kernel aislado por entidad, que almacena registros como archivos planos inertes sin operación de eliminación, expuestos únicamente a través del Diode.
- [[totebox-archive]] — Una máquina virtual micro-autónoma y libremente transferible que persiste datos institucionales como archivos planos inmutables.
- [[totebox-orchestration]] — Cómo se coordinan las instancias Totebox en un despliegue de flota; programación, límites de aislamiento y rutas de actualización.

## Superficies del operador

Los sistemas a través de los cuales un operador humano interactúa con la plataforma.

- [[console-os]] — La superficie orientada al ser humano: un Libro de Comandos que se conecta a un Totebox y renderiza su estado a través de una interfaz controlada por teclado y teclas F.
- [[os-workplace]] — El sistema operativo de escritorio gratuito: un escritorio soberano nativo en Rust que se empareja con un archivo Totebox y sirve como puerta de entrada al producto comercial.
- [[os-orchestration]] — El Agregador de Flota para carteras de múltiples entidades: un operador ve, consulta y comanda muchos archivos Totebox a la vez.

## Control de red e infraestructura

Los sistemas que gestionan el tejido de red y el cómputo subyacente.

- [[infrastructure-os]] — El sustrato de cómputo que aloja los sistemas operativos PointSav en hardware on-premises, arrendado y en la nube; arranca flotas aisladas a través del Protocolo Génesis.
- [[os-network-admin]] — El plano de control de una flota PointSav: gestiona el registro de emparejamiento, las reglas Diode y la política de enrutamiento de malla.
- [[os-privategit]] — Alojamiento Git privado para control de versiones soberano dentro de una flota.

## Publicación y medios

- [[mediakit-os]] — El SO orientado al público: aloja el sitio web de marketing de una empresa, el wiki interno y la sala de prensa de cumplimiento en un único dispositivo soberano propiedad de la empresa.

## Véase también

- [Arquitectura](/architecture/) — arquitectura transversal de la plataforma y el modelo de tres anillos
- [Servicios](/services/) — los servicios autónomos que se ejecutan dentro y a través de los sistemas operativos
- [Infraestructura](/infrastructure/) — topología de despliegue de flota y entorno operativo en la nube
