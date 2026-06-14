---
schema: foundry-doc-v1
title: "Guía de estilo: CLA"
slug: style-guide-cla.es
short_description: "Estándares editoriales para Acuerdos de Licencia de Contribuidor (género LEGAL-CLA): autoridad canónica del CLA, secciones requeridas, disciplina de licencia de patente y requisito de revisión de factory-release-engineering."
category: reference
type: topic
content_type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-24
editor: pointsav-engineering
cites: []
paired_with: style-guide-cla.md
---

Un CLA transfiere derechos específicos de propiedad intelectual de un contribuidor al proyecto. El texto canónico está gobernado por `factory-release-engineering`; esta plantilla es para redactar o explicar uno, no para ejecutarlo.

## Cuándo usar esta plantilla

Se usa cuando un proyecto de código abierto en `pointsav-monorepo` acepta contribuciones externas y necesita un marco de contribución, cuando los derechos de un contribuidor deben ser explícitos para satisfacer un requisito de licencia, o cuando se necesita una revisión de gobernanza de un CLA existente. El texto canónico del CLA es mantenido por `factory-release-engineering`: no redactar un CLA para ejecución sin [[style-guide-policy|revisión de gobernanza]].

## Estructura requerida

**Bloque de encabezado:**

```
Agreement:   Contributor License Agreement — <nombre del proyecto>
Contributor: <nombre legal completo o nombre de entidad>
```

Cinco secciones:

1. **Definitions** — tres términos definidos: Contribution (lo que el contribuidor envía), Project (a lo que contribuye), Contributor (quién acuerda). Definidos exactamente una vez.
2. **Grant of copyright license** — los derechos de autor específicos que el Contribuidor otorga al Proyecto. Mínimo: reproducir, preparar obras derivadas, exhibir públicamente, ejecutar públicamente, distribuir.
3. **Grant of patent license** — cualquier derecho de patente necesariamente infringido por la Contribución, con cláusula de terminación defensiva incluida.
4. **Representations** — las declaraciones del Contribuidor de que tiene derecho a realizar la Contribución. Deben ser concretas, no vagas.
5. **Scope** — qué cubre el acuerdo y qué no cubre explícitamente.

## Registro

Legal-llano. Los términos definidos se escriben en mayúscula. Las declaraciones en Representations deben ser precisas: las declaraciones vagas reducen la [[disclosure-substrate|aplicabilidad]] y crean ambigüedad.

## Véase también

- [[style-guide-contract|Guía de estilo — Contrato]]
- [[style-guide-license-explainer|Guía de estilo — Explicador de licencia]]
- [[language-protocol-substrate|Substrato del Protocolo de Lenguaje]]
