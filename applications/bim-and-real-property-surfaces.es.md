---
schema: foundry-doc-v1
title: "bim-and-real-property-surfaces"
slug: bim-and-real-property-surfaces
category: applications
type: concept
content_type: topic
quality: complete
short_description: "BIM y superficies de bienes raíces describe cómo PointSav trata el Modelado de Información de Construcción como un dominio operativo de primera clase, con herramientas de sistema de diseño dedicadas, disciplina de registro ISO 19650 y patrones de archivo Totebox."
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: bim-and-real-property-surfaces.md
references:
 - id: 1
 text: "Organización Internacional de Normalización, ISO 19650-1:2018 — Organización y digitalización de información sobre edificios y obras de ingeniería civil, incluido el modelado de información de construcción (BIM). Parte 1: Conceptos y principios."
 url: "https://www.iso.org/standard/68078.html"
 - id: 2
 text: "buildingSMART International, Industry Foundation Classes (IFC) — el estándar BIM abierto para el intercambio de datos de edificios."
 url: "https://www.buildingsmart.org/standards/bsi-standards/industry-foundation-classes/"
---

BIM y superficies de bienes raíces describe cómo la plataforma PointSav trata el Modelado de Información de Construcción (BIM) como un dominio operativo de primera clase en los despliegues de clientes del sector inmobiliario. La plataforma proporciona herramientas de sistema de diseño dedicadas, convenciones de registro ISO 19650[^1] y patrones de archivo [[totebox-os|Totebox]] para datos inmobiliarios. Los componentes, tokens y primitivas geoespaciales de BIM residen en un sistema de diseño de nivel cliente separado (`woodfine-design-bim`), distinto del vendor `pointsav-design-system` — este artículo resume los puntos de integración; el contenido detallado de BIM está en `woodfine-design-bim`. Al finalizar este artículo, el lector comprenderá la separación de los dos sistemas de diseño, la disciplina de sufijos ISO 19650 y la ubicación de los colaboradores BIM en el [[archetypes-and-chart-of-accounts|Plan de Cuentas]].

## Dos sistemas de diseño, deliberadamente separados

La aclaración estructural más importante: PointSav opera dos sistemas de diseño distintos, no uno con una subsección BIM.

| Sistema de diseño | Repositorio | Audiencia | Dominio |
|---|---|---|---|
| `pointsav-design-system` | `github.com/pointsav` (vendor) | Colaboradores de PointSav y operadores de flota | Sustrato de UI y UX para [[console-os|os-console]], [[os-workplace]] y toda la familia de SO vendor |
| `woodfine-design-bim` | `github.com/woodfine` (cliente) | Arquitectos, ingenieros, operadores inmobiliarios | Tokens BIM, componentes IFC[^2], primitivas visuales geoespaciales, sistema de diseño inmobiliario |

Los dos sistemas comparten metodología de autoría — un esquema común de metadatos estructurados, [[six-tier-sovereignty-matrix|estructura de soberanía de seis niveles]], nomenclatura estricta en minúsculas con guiones — pero no comparten contenido. La separación es estructural: BIM concierne a los bienes raíces; el sistema de diseño del vendor concierne a las superficies del sistema operativo. El contenido o los tokens específicos de los flujos de trabajo BIM pertenecen a `woodfine-design-bim`, nunca a `pointsav-design-system`.

El despliegue público previsto para `woodfine-design-bim` es `bim.woodfinegroup.com`. Las especificaciones completas de componentes BIM, definiciones de tokens y primitivas geoespaciales se mantienen allí.

## Disciplina de sufijos de registro ISO 19650

La gestión de documentos BIM opera bajo ISO 19650[^1], que define códigos explícitos de estado de documento para cada artefacto. El despliegue de PointSav adopta estos códigos como convenciones de sufijo de nombre de archivo para que las herramientas de auditoría puedan leer el estado del documento directamente del nombre del archivo.

| Sufijo | Estado ISO 19650 | Significado |
|---|---|---|
| `_JW` | S0 | Trabajo en curso — borrador, aún no compartido |
| `_FIN` | S4 | Final, compartido para aprobación o coordinación |
| `_PUB` | A0 | Publicado y aprobado para uso |
| `_EXE` | CR | Ejecutado o firmado — estado de registro o como construido |
| `_MCH` / `_DAT` | (coincide con el padre) | Versión legible por máquina del documento padre |

Las herramientas de auditoría leen el sufijo y enrutan en consecuencia. Un archivo `_PUB` está firmado y se trata como inmutable; un archivo `_JW` está en vuelo y no lleva estado verificado. Un archivo `_EXE` ha pasado la [[app-console-input|confirmación del operador F12]] e ingresa al archivo [[totebox-os|Totebox]] como un registro sellado bajo la [[worm-ledger-design|disciplina del libro mayor WORM]].

La disciplina de sufijos se aplica a cada artefacto BIM que ingresa al [[service-content|Motor de Gravedad]] — ya sea un dibujo, un modelo de coordinación, un permiso o un registro de arrendamiento. Esto hace que la postura de mantenimiento de registros sea coherente con la disciplina más amplia del [[worm-ledger-design|libro mayor WORM]] en toda la plataforma.

## Colaboradores BIM en el Plan de Cuentas

En el [[archetypes-and-chart-of-accounts|Plan de Cuentas]] institucional, los colaboradores del dominio BIM ocupan un conector estructural específico:

| Perfil | Dominio | Subdominio | Arquetipo ancla |
|---|---|---|---|
| Soporte de TI | Colaboradores | BIM | El Ingeniero |

Esta ubicación no es estética. Determina cómo [[service-people]] conecta a los colaboradores BIM cuando su producto de trabajo ingresa a [[service-content]]. Un modelador BIM, un coordinador BIM y un ingeniero estructural ocupan el mismo conector de arquetipo Ingeniero bajo Soporte de TI → Colaboradores → BIM, lo que significa que la plataforma aplica la misma clave de evaluación (`logic_efficiency`) y la misma lógica de enrutamiento de tareas a su producción.

Los colaboradores BIM son estructuralmente adyacentes a los trabajadores de DevOps, Redes, Bases de datos, Backend, GIS e IoT — todos posiciones de arquetipo Ingeniero bajo Soporte de TI. Esta adyacencia significa que el trabajo BIM hereda el mismo tratamiento computacional que otras disciplinas de datos y lógica.

## Superficies de sistema operativo adyacentes a BIM

Tres superficies de [[console-os|os-console]] están previstas para el trabajo de dominio BIM. Las tres son aspiracionales y llevan el lenguaje prospectivo apropiado.

| Superficie prevista | Función |
|---|---|
| `app-console-bim` | Visualización y revisión BIM de alta fidelidad; previsto para leer archivos IFC mediante una biblioteca Rust nativa para IFC; renderiza geometría B-rep mediante un kernel de geometría Rust |
| Variante GIS de `app-console-bim` | Superposición geoespacial y análisis mediante un conjunto de herramientas de caja blanca nativo de Rust; previsto para reemplazar las herramientas geoespaciales C++ heredadas |
| Consola de mapas de `app-console-bim` | Visualización espacial con un diseño de Consola basado en mapas |

La [[app-console-input|puerta de entrada F12]] gestiona la ingesta de documentos BIM — un operador arrastra un archivo IFC o un plano a F12, selecciona el destino en el Plan de Cuentas, confirma las entidades extraídas y el archivo ingresa al archivo Totebox con un sufijo ISO 19650 y un registro de auditoría con marca de tiempo.

## Véase también

- `woodfine-design-bim` — el sistema de diseño BIM de nivel cliente (mantenido por separado en `github.com/woodfine`)
- [[archetypes-and-chart-of-accounts]] — la taxonomía del Plan de Cuentas y los once arquetipos
- [[totebox-os]] — el sistema operativo Totebox que aloja los archivos de bienes raíces
- [[app-console-input]] — la puerta de entrada F12 a través de la cual los documentos BIM ingresan a la plataforma
- [[service-content]] — el Motor de Gravedad que clasifica y enruta los documentos BIM
- [[worm-ledger-design]] — el sustrato del libro mayor WORM que sella los registros inmobiliarios
