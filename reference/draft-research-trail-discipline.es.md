---
schema: foundry-doc-v1
title: "Disciplina de rastro de investigación en borradores"
slug: draft-research-trail-discipline.es
category: reference
type: topic
quality: published
short_description: El requisito de que cada borrador que entra en un pipeline editorial o de diseño lleve documentación estructurada de la investigación que lo informó y la investigación que debe realizar la siguiente etapa.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
paired_with: draft-research-trail-discipline.md
---

## Resumen estratégico

La disciplina de rastro de investigación en borradores requiere que cada borrador que entra en cualquier pipeline de publicación lleve dos formas de documentación de investigación: campos de metadatos estructurados que las máquinas pueden analizar, y una sección de cuerpo que la pasarela de refinamiento puede leer. Juntos crean un rastro desde el material fuente hasta la afirmación publicada que persiste a través de cada transición en el ciclo de vida de publicación.

## Dos superficies, un rastro

**Campos de metadatos** llevan cinco elementos requeridos: el recuento de fuentes de investigación consultadas, el recuento de fuentes que el autor sugiere que consulte la pasarela, el recuento de preguntas abiertas sin resolver, la categoría de procedencia de la investigación, y un indicador sobre si el rastro aparece en el cuerpo. Los cinco campos son obligatorios en cada borrador; los recuentos de cero son válidos para borradores triviales.

**Sección de cuerpo** lleva el rastro en prosa con tres subsecciones: Realizado (qué informó el borrador), Sugerido (qué debe consultar la pasarela) y Preguntas abiertas (elementos que el autor no pudo resolver).

## Lo que hace la pasarela con el rastro

En tiempo de refinamiento, la pasarela lee la subsección de sugeridos antes de componer el refinamiento. Consulta las fuentes nombradas donde el alcance lo permite. El resultado refinado lleva un pie de Procedencia derivado del rastro. La disciplina de divulgación aplica en la etapa del pie de Procedencia: los elementos de investigación prospectivos se eliminan de los pies de Procedencia de cara al público; las notas de contexto de sesión nunca aparecen en el resultado publicado.

## Disciplina sin burocracia

El mecanismo está diseñado para ser ligero en la práctica: hallazgos de una línea; la investigación detallada va en un archivo de investigación separado, referenciado una vez; los recuentos vacíos son válidos y transparentes; las preguntas abiertas que la pasarela no puede resolver se convierten en solicitudes de vuelta al contribuidor de origen.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*
