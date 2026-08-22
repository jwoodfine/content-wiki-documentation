---
schema: foundry-doc-v1
title: "bim-and-real-property-surfaces"
slug: bim-and-real-property-surfaces
category: applications
type: concept
content_type: topic
quality: complete
index_group: domain-applications
short_description: "Cómo PointSav trata el Modelado de Información de Construcción como un dominio operativo distinto — un sistema de diseño de nivel cliente separado, una ubicación real en el Plan de Cuentas y superficies de consola específicas de BIM aún en fase de investigación."
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
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

BIM y superficies de bienes raíces describe cómo la plataforma PointSav trata el Modelado de Información de Construcción (BIM) como un dominio operativo distinto en los despliegues de clientes del sector inmobiliario. Los componentes, tokens y primitivas geoespaciales de BIM residen en un sistema de diseño de nivel cliente separado (`woodfine-bim-library`), distinto del vendor `pointsav-design-system` — este artículo resume los puntos de integración; el contenido detallado de BIM está en `woodfine-bim-library`. Al finalizar este artículo, el lector comprenderá la separación de los dos sistemas de diseño, la ubicación real de los colaboradores BIM en el [[archetypes-and-chart-of-accounts|Plan de Cuentas]], y el estado actual (fase de investigación) de las superficies de consola específicas de BIM.

## Dos sistemas de diseño, deliberadamente separados

La aclaración estructural más importante: PointSav opera dos sistemas de diseño distintos, no uno con una subsección BIM.

| Sistema de diseño | Repositorio | Audiencia | Dominio |
|---|---|---|---|
| `pointsav-design-system` | `github.com/pointsav` (vendor) | Colaboradores de PointSav y operadores de flota | Sustrato de UI y UX para [[os-console]], [[os-workplace]] y toda la familia de SO vendor |
| `woodfine-bim-library` | `github.com/woodfine` (cliente) | Arquitectos, ingenieros, operadores inmobiliarios | Tokens BIM, componentes IFC[^2], primitivas visuales geoespaciales, sistema de diseño inmobiliario |

Los dos sistemas comparten metodología de autoría — un esquema común de metadatos estructurados, [[six-tier-sovereignty-matrix|estructura de soberanía de seis niveles]], nomenclatura estricta en minúsculas con guiones — pero no comparten contenido. La separación es estructural: BIM concierne a los bienes raíces; el sistema de diseño del vendor concierne a las superficies del sistema operativo. El contenido o los tokens específicos de los flujos de trabajo BIM pertenecen a `woodfine-bim-library`, nunca a `pointsav-design-system`.

El despliegue público previsto para `woodfine-bim-library` es `bim.woodfinegroup.com`. Las especificaciones completas de componentes BIM, definiciones de tokens y primitivas geoespaciales se mantienen allí.

## Sufijos de nombre de archivo por estado de documento

Los documentos fuente de bienes raíces en el corpus de trabajo de la plataforma llevan sufijos
de nombre de archivo como `_FIN` (final, compartido para aprobación o coordinación) y
`_JW`/`_EXE` (estados de borrador y ejecutado/firmado), una convención informal anterior a
cualquier herramienta de la plataforma. Formalizar esto como un sistema de estado legible por
máquina, mapeado a ISO 19650[^1] — con `service-bim` inspeccionando el sufijo y enrutando el
documento automáticamente — es una intención de diseño para la canalización de ingesta BIM, no
una capacidad construida hoy: `service-bim` existe solo como notas de investigación y diseño,
sin código de ingesta, validación o enrutamiento de auditoría entregado.

## Colaboradores BIM en el Plan de Cuentas

El [[archetypes-and-chart-of-accounts|Plan de Cuentas]] institucional tiene una entrada real
para el trabajo BIM: categoría **Soporte de TI**, tipo **BIM** (referencia `6010`), asociada
con palabras clave que incluyen `bim`, `building information modeling`, `digital twin`,
`revit` e `ifc`. Los colaboradores BIM están en la misma categoría que otros roles de
ejecución técnica, no bajo Cumplimiento o Bienes Raíces, donde aplican categorías distintas.

## Superficies de sistema operativo adyacentes a BIM

El trabajo de dominio BIM en [[os-console]] está en fase de investigación — existe un
documento de diseño (`app-console-bim`), no se ha entregado código. La forma prevista, según
esa investigación: una única terminal de enrutamiento y coordinación (`app-console-bim`)
distinta de una superficie de autoría (`app-workplace-bim`) — la separación coincide con la
distinción consola/estación de trabajo que ya existe en la plataforma, ver-y-vincular frente a
crear-y-editar. `app-console-bim` consultaría elementos, vincularía órdenes de trabajo y
crearía incidencias; no editaría geometría BIM. Para carteras que abarcan múltiples
propiedades, una capa de agregación sin estado (`app-orchestration-bim`) está prevista para
federar consultas entre archivos de propiedades en lugar de almacenar datos ella misma. La
dirección técnica actual del documento de investigación favorece la renderización IFC basada
en navegador (evaluando `xeokit-sdk` y `@thatopen/components`) sobre un kernel de geometría
Rust nativo — nada de esto está comprometido ni construido, y la dirección puede cambiar antes
de que comience la implementación.

## Véase también

- `woodfine-bim-library` — el sistema de diseño BIM de nivel cliente (mantenido por separado en `github.com/woodfine`)
- [[archetypes-and-chart-of-accounts]] — la taxonomía del Plan de Cuentas y los once arquetipos
- [[totebox-os]] — el sistema operativo Totebox en el que corren los archivos de bienes raíces
- [[app-console-input]] — la puerta de entrada general de ingesta de documentos de la plataforma
- [[service-content]] — el servicio de clasificación y taxonomía de documentos de la plataforma
- [[worm-ledger-design]] — el diseño del libro mayor de registro inmutable de la plataforma
