---
schema: foundry-doc-v1
title: "Pipeline de borradores de diseño por clúster"
slug: cluster-design-draft-pipeline.es
category: reference
type: topic
quality: published
short_description: El pipeline de espacio de trabajo que enruta borradores de componentes de UI, investigación de diseño y cambios de tokens a través de una pasarela de sistema de diseño hacia el sustrato canónico.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites:
  - ni-51-102
paired_with: cluster-design-draft-pipeline.md
---

## Resumen estratégico

Cuando un clúster de desarrollo implementa una funcionalidad con interfaz de usuario, los componentes de UI que esa funcionalidad introduce necesitan aterrizar en un sustrato de sistema de diseño canónico — no como implementaciones locales aisladas que divergen silenciosamente con el tiempo. El pipeline de borradores de diseño por clúster es el mecanismo que enruta esas contribuciones desde donde se originan a través de una pasarela de sistema de diseño hacia el sustrato donde se vuelven reutilizables, legibles por máquinas y mantenidas consistentemente.

## Tres puertos de entrada, una pasarela de diseño

Los borradores se originan desde tres capas: nivel de clúster (una funcionalidad específica del producto), nivel de repositorio (contratos de diseño transversales), y nivel de espacio de trabajo (decisiones de lenguaje de diseño entre clústeres). Todos alimentan a la pasarela del sistema de diseño, que filtra por el campo `language_protocol` en los metadatos del borrador.

## Tres familias de borradores

**DESIGN-COMPONENT.** Un componente de UI — marcado HTML, variables CSS, roles ARIA y notas de interacción por teclado. La pasarela verifica alineación con el vocabulario primitivo de IBM Carbon (la capa base del sustrato), realiza verificaciones de accesibilidad WCAG 2.2 AA, empareja la receta del componente con un archivo de investigación legible por máquinas y activa una reconstrucción de exportaciones.

**DESIGN-RESEARCH.** Justificaciones de decisiones de diseño, reglas de voz de marca, pistas de consumo de IA — contribuciones que pertenecen al plano de respaldo de investigación del sustrato. Estos forman el contexto legible por máquinas que los agentes de IA consultan en tiempo de generación de código.

**DESIGN-TOKEN-CHANGE.** Adiciones o modificaciones propuestas al vocabulario de tokens almacenado en formato W3C Design Tokens Community Group. Los cambios de tokens requieren aprobación explícita de gobernanza antes de que la pasarela los procese, ya que se propagan a cada herramienta posterior.

## Corpus de aprendizaje

Cada transición a través del pipeline emite un evento estructurado al corpus de aprendizaje: `draft-created`, `draft-refined` y `creative-edited`. El primer par forma un ejemplo de entrenamiento de Etapa 1; el segundo par forma un ejemplo de Etapa 2 del diseñador creativo. El pipeline está diseñado como opt-in para clústeres sin superficies de usuario, pero es obligatorio cuando un clúster introduce nuevos elementos visuales.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*
