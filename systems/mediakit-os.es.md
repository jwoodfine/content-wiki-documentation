---
schema: foundry-doc-v1
title: "os-mediakit — El dispositivo de cumplimiento soberano"
slug: mediakit-os
category: systems
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: mediakit-os.md
short_description: "os-mediakit es el sistema operativo de cara al público en la familia PointSav, que aloja el sitio web de marketing de una empresa, su wiki interna y su sala de prensa de cumplimiento en un único dispositivo soberano de propiedad completa."
cites: []
---

`os-mediakit` es el sistema operativo de cara al público en la familia PointSav. Aloja el sitio web de marketing de una empresa, su wiki interna y su sala de prensa de cumplimiento — tres cargas de trabajo que habitualmente viven en plataformas de terceros arrendadas y que desaparecen en el momento en que vence una suscripción. El operador objetivo es un Emisor Informante: una empresa con obligaciones de divulgación estatutaria que necesita prueba matemática de qué divulgó y exactamente cuándo. `os-mediakit` está construido sobre una base FreeBSD reforzada y distribuye tres superficies de aplicación como cargas de trabajo aisladas. Este artículo cubre las tres superficies, la justificación del licenciamiento FreeBSD, el Libro Mayor de Cumplimiento, el adaptador Diodo y los dos modos de despliegue.

## Las tres superficies de aplicación

`os-mediakit` aloja tres superficies en un único dispositivo. Cada carga de trabajo se ejecuta como una instancia aislada para que una consulta intensiva a la base de datos en la wiki no pueda inducir latencia en la página de inicio:

| Superficie | Motor | Rol |
|---|---|---|
| `app-mediakit-marketing` | Motor de sitio estático con capa de caché en Rust | Páginas públicas y páginas de relaciones con inversores |
| `app-mediakit-knowledge` | Motor de wiki Markdown con almacenamiento conforme al contrato de contenido | Wiki corporativa, wiki de proyectos, wiki de documentación |
| `app-mediakit-distribution` | Motor de feeds de cumplimiento basado en envío | Comunicados de prensa, presentaciones regulatorias, comentarios ejecutivos |

## Por qué FreeBSD

La elección del SO base es deliberada. La licencia BSD de FreeBSD permite a PointSav tomar el código, modificarlo, mantener cerradas las modificaciones y distribuir una distribución propietaria sin obligación de abrir esas modificaciones. El resultado es un camino legalmente limpio hacia un dispositivo de cumplimiento propietario.

La hoja de ruta prevista para el sustrato es una metamorfosis de cuatro fases:

| Fase | Forma | Estado |
|---|---|---|
| 1 | Host FreeBSD reforzado con las tres aplicaciones ejecutándose en jaulas | Inicial |
| 2 | NanoBSD — una variante reducida de solo lectura | Previsto |
| 3 | Núcleo personalizado con renderizado en lenguaje interpretado reemplazado por Rust | Previsto |
| 4 | Unikernel — SO y aplicación fusionados en un único binario | Previsto |

## El Libro Mayor de Cumplimiento

La capacidad distintiva es `app-mediakit-distribution`. Las plataformas convencionales de relaciones con inversores obtienen datos de servicios de distribución de noticias después del hecho y los sirven como páginas estáticas. `os-mediakit` invierte el flujo:

1. Un comunicado de prensa se redacta dentro de `os-totebox` y se firma criptográficamente.
2. `os-totebox` envía el contenido firmado a `os-mediakit-distribution` en el momento de la publicación.
3. `os-mediakit` archiva el contenido firmado, la marca de tiempo y la firma criptográfica antes de publicar.
4. El sitio web se actualiza en el momento de la publicación. El registro firmado permanece en `os-mediakit` de forma permanente.

El resultado es prueba matemática de qué se divulgó y exactamente cuándo. La empresa no pierde su archivo cuando termina una suscripción — la empresa posee el dispositivo.

## La conexión Diodo

`os-mediakit` está orientado a internet público. `os-totebox` no lo está. Los dos se conectan únicamente a través de un adaptador unidireccional (`service-pointsav-link`, previsto) que permite que los comandos y el contenido fluyan desde el Totebox interno al MediaKit público, pero nunca a la inversa. Un plugin comprometido en la superficie de marketing no puede alcanzar el Totebox corporativo, porque el código para hacerlo está ausente del adaptador.

El adaptador es un paquete instalado por separado. Los operadores que no necesitan gestión de flota pueden ejecutar `os-mediakit` sin ningún adaptador; el SO no tiene capacidad para comunicarse con sistemas externos.

## Autónomo o federado

`os-mediakit` se despliega en dos configuraciones:

| Configuración | Caso de uso | Interfaz |
|---|---|---|
| Autónomo | Un trabajador independiente o PYME que aloja uno o dos sitios públicos | TUI local accesible por SSH |
| Federado | Un operador comercial que gestiona muchos sitios desde una flota centralizada | El TUI local se convierte en monitor de estado; el control pasa a `os-orchestration` |

Ambas configuraciones utilizan el mismo binario de `os-mediakit`. La transición es un único comando: instalar el paquete adaptador, realizar un apretón de manos de emparejamiento único y la instancia MediaKit se une a la flota.

## Véase también

- [[os-family-overview]] — la familia de ocho SO y cómo encaja os-mediakit
- [[totebox-os]] — la bóveda interna que envía contenido firmado a os-mediakit
- [[diode-standard]] — el adaptador unidireccional que separa la superficie pública de la bóveda privada
- [[app-mediakit-knowledge]] — la superficie de wiki de documentación
- [[compliance-and-continuous-disclosure]] — postura BCSC y obligaciones de divulgación continua
- [[deployment-patterns]] — cómo os-mediakit aparece en cada configuración de despliegue canónica
