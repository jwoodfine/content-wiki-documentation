---
schema: foundry-doc-v1
title: "Guía de estilo: memo"
slug: style-guide-memo.es
short_description: "Estándares editoriales para memoranda internos (género PROSE-MEMO): disciplina de encabezado, orden de secciones, convención de recomendación primero y cuándo un memo es el artefacto adecuado."
category: reference
type: topic
content_type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-24
editor: pointsav-engineering
cites: []
paired_with: style-guide-memo.md
---

Un memo registra una decisión, análisis o recomendación dirigida a una audiencia nombrada. Es completo cuando el lector sabe qué se decidió y qué ocurre a continuación, sin necesidad de consultar ningún otro documento. Para la disciplina de registro y tono aplicada a todos los artefactos en prosa, véase [[editorial-language-registers|registros de lenguaje editorial]].

## Cuándo usar esta plantilla

Se usa un memo cuando una decisión ha sido tomada y debe comunicarse con el análisis que la respaldó, cuando una recomendación está lista para un tomador de decisiones nombrado y no puede entregarse en un solo párrafo, o cuando una pregunta compleja ha sido resuelta y la resolución debe quedar registrada. No se usa para debate en curso, estado de proyectos ni preguntas sin resolver.

## Estructura requerida

**Bloque de encabezado** (antes de cualquier sección):

```
To:   <destinatario>
From: <autor>
Date: <YYYY-MM-DD>
Re:   <asunto en una línea — específico y accionable>
```

Cinco secciones en orden:

1. **Summary** — la conclusión, expresada primero. Uno a tres oraciones. El lector que solo lea esta sección debe poder actuar sobre ella.
2. **Context** — los hechos necesarios para evaluar la recomendación. Solo lo que es relevante, no la historia completa.
3. **Analysis** — el razonamiento, estructurado en puntos numerados o párrafos cortos. Reconoce el contraargumento más sólido y explica por qué no fue decisivo.
4. **Recommendation** — la acción específica solicitada, con responsable y plazo. Un memo sin recomendación es un brief; reestructurar en consecuencia.
5. **Next steps** — acciones concretas de seguimiento con responsables y fechas.

## Registro

Prosa profesional, no legalismo. La recomendación va antes del análisis. El campo `Re:` debe ser específico y accionable. Promedio de veintidós palabras por oración; máximo cuarenta. Voz activa. Se aplica la lista de vocabulario prohibido.

## Véase también

- [[style-guide-topic|Guía de estilo — TOPIC]]
- [[language-protocol-substrate|Substrato del Protocolo de Lenguaje]]
