---
schema: foundry-doc-v1
title: "Pipeline de borradores wiki por clúster"
slug: cluster-wiki-draft-pipeline.es
category: reference
type: topic
quality: published
short_description: El pipeline de espacio de trabajo que enruta borradores editoriales de todas las capas de contribuidores a través de una pasarela editorial hacia temas de documentación, runbooks de implementación y documentos de gobernanza publicados.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
paired_with: cluster-wiki-draft-pipeline.md
---

## Resumen estratégico

El pipeline de borradores wiki por clúster es el mecanismo estructurado que recopila borradores editoriales de toda la plataforma, aplica un pase editorial consistente y enruta el resultado refinado a la superficie publicada apropiada. Operacionaliza el Patrón Editorial de Embudo Inverso: el sustrato genera borradores estructurales; una pasarela editorial los refina para el registro; los Contribuidores Creativos editan la versión publicada al final del ciclo.

## Tres puertos de entrada

Los borradores editoriales se originan desde tres capas:

**Borradores a nivel de clúster** (mayor velocidad): un clúster de desarrollo produce borradores explicando lo que construyó y las decisiones arquitectónicas tomadas.

**Borradores a nivel de repositorio**: actualizaciones de README por repositorio, temas de arquitectura que abarcan múltiples proyectos dentro de un único código base.

**Borradores a nivel de espacio de trabajo**: temas transversales entre clústeres, documentos de gobernanza, texto de licencias y páginas de identidad de contribuidores.

## Lo que aplica la pasarela editorial

**Disciplina de registro.** El borrador crudo puede ser técnicamente preciso pero redactado conversacionalmente. La pasarela produce resultados en registro Bloomberg — preciso, económico, legible por un no especialista financieramente instruido.

**Disciplina de divulgación.** El campo `bcsc_class` del borrador determina qué reglas de divulgación aplican. Los borradores marcados como `forward-looking` reciben lenguaje planificado/previsto/puede, con base razonable declarada y supuestos materiales nombrados.

**Resolución de citas.** Las referencias URL en línea en el borrador crudo se resuelven a IDs de citación estables del registro.

**Generación bilingüe.** Los temas wiki publicados y los archivos README se producen como pares bilingües — la versión en español sigue un patrón de adaptación estratégica.

## Corpus de aprendizaje

Cada transición editorial emite un evento estructurado al corpus de aprendizaje: `draft-created`, `draft-refined` y `creative-edited`. Estos pares se acumulan como material de entrenamiento para la capacidad de inferencia local de la plataforma, generando dos pares de preferencia por ciclo de vida de borrador.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*
