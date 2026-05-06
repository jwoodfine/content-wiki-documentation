---
schema: foundry-doc-v1
title: "Guía de estilo: CHANGELOG"
slug: style-guide-changelog.es
category: reference
type: topic
quality: core
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: style-guide-changelog.md
---

Un `CHANGELOG.md` es el registro legible de la historia de
versiones de un proyecto. No es un registro de commits — ese
existe en Git. Es el resumen curado que un mantenedor escribe
para que los colaboradores comprendan qué cambió entre versiones
sin leer cada commit.

## Cuándo usar esta plantilla

Todo proyecto activo en `pointsav-monorepo` y todo repositorio
de ingeniería que publique versiones etiquetadas debe mantener
un `CHANGELOG.md`. El archivo se crea cuando la primera entrada
significativa se registra — no como marcador vacío.

## Estructura

Foundry sigue el formato keep-a-changelog ajustado a la regla
de versionado del espacio de trabajo (`CLAUDE.md` §7):

- Un **capítulo** por versión MAJOR
- Una **sección** por versión MINOR
- Una **línea** por PATCH (un commit aceptado)

La versión más reciente aparece al inicio del archivo. Cada
línea registra qué cambió y por qué, con el SHA corto del
commit. El quién y el cuándo viven en Git; el changelog no los
repite.

## Registro

Operacional. Oraciones declarativas breves en tiempo pasado.
Promedio de dieciséis palabras, máximo veintiocho. Cada
entrada explica el efecto del cambio para los consumidores,
no el detalle de implementación. Se aplica la lista de
vocabulario prohibido.

## Véase también

- [[style-guide-readme|Guía de estilo — README]]
- [[style-guide-architecture|Guía de estilo — ARCHITECTURE]]
- [[style-guide-inventory|Guía de estilo — INVENTORY]]


---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™ y Totebox Archive™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos titulares.*
