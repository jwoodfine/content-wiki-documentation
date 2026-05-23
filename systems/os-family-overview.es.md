---
schema: foundry-doc-v1
title: "La familia de SO — Ocho sistemas operativos, un sustrato"
slug: os-family-overview
category: systems
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: os-family-overview.md
short_description: "PointSav construye ocho sistemas operativos de propósito específico que comparten un sustrato común de seL4 y Rust. Cada uno hace un único trabajo, no contiene funciones que no necesita, y se comunica mediante una disciplina de protocolo Diodo común."
cites: []
---

PointSav construye ocho sistemas operativos de propósito específico que comparten un sustrato de micronúcleo seL4 común, una disciplina de lenguaje Rust común y un protocolo de comunicación basado en Diodo común. Cada SO hace un único trabajo y no contiene ninguna función que no necesita. La familia abarca desde un terminal de cara al operador hasta un dispositivo soberano en la nube, pero cada miembro compila desde el mismo núcleo y habla el mismo protocolo. Este artículo cubre los ocho miembros de la familia de SO, el sustrato que comparten, cómo se componen en despliegues y la disciplina Diodo que rige el flujo de comandos en todos ellos.

## Los ocho sistemas operativos

| SO | Rol | Operado por |
|---|---|---|
| `os-console` | Terminal humano universal — el Libro Mayor de Comandos | El operador en el teclado |
| `os-totebox` | Bóveda soberana y host de servicios — el archivo de datos | Una entidad (persona, corporación, propiedad) |
| `os-orchestration` | Agregador de flota — vista multi-archivo para operadores comerciales | Administrador empresarial |
| `os-infrastructure` | Sustrato de cómputo que aloja los demás | Administrador de flota |
| `os-network-admin` | Plano de control de red — enrutamiento, registro de emparejamientos, política de malla | Arquitecto de red |
| `os-mediakit` | Dispositivo web público — marketing, wiki, sala de prensa de cumplimiento | Emisor Informante o PYME |
| `os-privategit` | Hosting soberano de código fuente y diseño | PointSav interno y cliente |
| `os-workplace` | Escritorio soberano con aplicaciones nativas en Rust | Comunidad y cliente PYME |

## Por qué ocho, y no uno

Los sistemas operativos convencionales intentan serlo todo: contabilidad, correo electrónico, navegación segura, edición de video. El resultado es una gran superficie de ataque y una constante proliferación de funciones. PointSav invierte el modelo: cada SO es pequeño, de propósito único y reemplazable. Si un despliegue no necesita un agregador de flota, no incluye `os-orchestration`. Si no tiene un sitio web público, no incluye `os-mediakit`. Cada SO es una pieza de fontanería de precisión, no una plataforma.

## El sustrato compartido

Los ocho sistemas operativos comparten la misma capa fundacional:

| Capa | Componente | Propósito |
|---|---|---|
| Núcleo | [[sel4-microkernel-substrate|Micronúcleo seL4]] | Aislamiento de hardware verificado matemáticamente |
| Lenguaje | Rust (seguro en memoria; sin recolector de basura) | Todo el código `system-*`, `service-*` y `os-*`; C/C++ prohibido en L3 y superior |
| Controladores | sDDF (Marco de Controladores de Dispositivos seL4) | Acceso directo al hardware sin sobrecarga de tiempo de ejecución |
| Protocolo | Protocolo PointSav (PSP) | Protocolo binario basado en capacidades; tuneliza a través de TLS y VirtIO en el borde |
| Confianza | `service-pairing` | Emparejamientos criptográficos vinculados al hardware; sin nombres de usuario, sin contraseñas |
| Auditoría | Libro mayor de solo adición (previsto) | Registro de eventos inalterable que no puede ser desactivado por un administrador |
| Transferibilidad | Addendum Soberano (previsto) | La instancia en ejecución permanece como propiedad del operador en cualquier proveedor de nube |

## Cómo se componen en despliegues

El despliegue mínimo viable es un operador ejecutando `os-console`, conectado a un `os-totebox` alojado en la nube. La Consola es el teclado y la pantalla; el Totebox es la bóveda y el trabajador.

El despliegue más grande es cientos de instancias de `os-totebox` distribuidas entre nodos `os-infrastructure` en instalaciones propias, arrendadas y en la nube, gobernadas por un `os-network-admin` y agregadas a través de `os-orchestration` para la revisión ejecutiva. Ambos extremos utilizan los mismos binarios. La escala es una cuestión de configuración, no de bifurcación de código.

Las seis composiciones canónicas se cubren en detalle en [[deployment-patterns]].

## La disciplina Diodo

En los ocho, el flujo de comandos es unidireccional. `os-console` y `os-orchestration` pueden emitir comandos a los demás. Los demás emiten telemetría hacia arriba — nunca comandos en dirección inversa. Esta restricción se aplica a nivel del protocolo [[diode-standard|Diodo]], no por política. Una instancia comprometida de `os-mediakit` orientada al público no puede alcanzar un `os-totebox` corporativo porque el código para hacerlo está ausente del binario.

## Véase también

- [[console-os]] — el terminal Libro Mayor de Comandos; superficie de cara al operador
- [[totebox-os]] — la bóveda soberana y host de servicios
- [[os-orchestration]] — el agregador de flota para despliegues comerciales
- [[sel4-microkernel-substrate]] — el núcleo seL4 compartido y por qué PointSav lo adoptó
- [[diode-standard]] — el protocolo Diodo que rige el flujo de comandos unidireccional
- [[deployment-patterns]] — las seis configuraciones de despliegue canónicas
- [[six-tier-sovereignty-matrix]] — cómo la familia `os-*` encaja en el modelo de seis niveles más amplio
- [[machine-based-auth]] — emparejamiento vinculado al hardware en todos los miembros de la familia
