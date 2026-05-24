---
schema: foundry-doc-v1
title: "Guía de estilo: política"
slug: style-guide-policy.es
short_description: "Estándares editoriales para documentos de política (género LEGAL): disciplina de alcance, formato de reglas numeradas, cláusula de aplicación, cadencia de revisión y distinción entre política y ADR."
category: reference
type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-24
editor: pointsav-engineering
cites: []
paired_with: style-guide-policy.md
---

Una política establece qué se requiere, quién está obligado y qué ocurre cuando se viola la regla. Cada oración de una política es una regla o el soporte de una regla.

## Cuándo usar esta plantilla

Se usa una política cuando el comportamiento debe ser uniforme en un equipo, proyecto u organización, cuando la desviación tiene consecuencias reales que deben establecerse, y cuando la regla necesita una cadencia de revisión para no quedar obsoleta en silencio. No se escribe una política para una preferencia o guía; una guía lleva "preferido" o "recomendado" y no implica aplicación.

## Estructura requerida

Cinco secciones en orden:

1. **Scope** — a quién y qué aplica esta política. Roles, sistemas o contextos nombrados. Explícito sobre lo que no aplica.
2. **Policy** — las reglas, numeradas. Cada regla es una declaración completa y autónoma. La primera palabra es una obligación: "Todo X debe…", "Ningún Y puede…", "Todo Z está obligado a…".
3. **Enforcement** — qué ocurre cuando se viola una regla. Debe nombrar una consecuencia o un proceso, no un vago "será abordado."
4. **Review** — con qué frecuencia y por quién se revisa esta política. Mínimo anual.
5. **See also** — vínculos a los ADR, convenciones o leyes que esta política implementa o requiere.

## Registro

Legal-llano. Voz activa. Sin conjeturas: "debe" y "no puede" para requisitos. "Debería" y "se recomienda" no son lenguaje de política. Máximo veinticinco palabras por regla.

## Véase también

- [[sys-adr-07|SYS-ADR-07 — Sin IA en datos estructurados]]
- [[language-protocol-substrate|Substrato del Protocolo de Lenguaje]]
