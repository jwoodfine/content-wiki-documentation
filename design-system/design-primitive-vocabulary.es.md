---
schema: foundry-doc-v1
title: "Sistema de diseño — Justificación del vocabulario primitivo"
slug: design-primitive-vocabulary
short_description: "Documenta los patrones estructurales preservados en la capa de tokens primitivos del sistema de diseño — escalas de color numéricas, aliasing semántico en capas, separación de tipo productivo versus expresivo, y escalas de espaciado numéricas — alineadas con convenciones de campo de 2018 a 2026 utilizando nomenclatura y valores específicos de PointSav."
category: design-system
type: reference
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: design-primitive-vocabulary.md
cites:
 - wcag-22
 - dtcg-spec
 - doctrine-38
---

La capa de tokens primitivos del [[design-system-substrate|sistema de diseño]] documenta qué patrones estructurales ha consolidado el campo desde 2018, cuáles preserva el sustrato de forma literal y cuáles reemplaza con vocabulario y valores originales de PointSav. La distinción es relevante para los profesionales que llegan de otros sistemas de diseño: los patrones estructurales compartidos generan reconocimiento inmediato; los nombres y valores originales de PointSav evitan cualquier conflicto de propiedad intelectual con los sistemas de los que se tomaron referencias. La justificación arquitectónica del sustrato está en [[design-philosophy|la filosofía del sistema de diseño]].

La capa de tokens primitivos del sustrato preserva cuatro patrones estructurales en los que el campo moderno de sistemas de diseño ha convergido (2018–2026): escalas de color numéricas, capas primitivo → semántico → componente, la división de tipografía productiva vs expresiva, y escalas de espaciado numéricas de ~12–15 pasos.

Estos patrones no son propiedad intelectual de ningún sistema de diseño en particular — son el vocabulario compartido del campo. Re-implementarlos es la elección arquitectónica correcta para cualquier sistema de diseño de 2026 que quiera que los profesionales lo adopten sin necesidad de re-aprender lo básico.

## Lo que el sustrato reemplazó

El sustrato utiliza vocabulario, valores hexadecimales, elecciones tipográficas y contenido originales de PointSav. Los nombres de las familias de color describen el rol en lugar de la familia cromática — los clientes que cambian su marca de azul a verde azulado no tienen que renombrar los tokens. Los valores hexadecimales son propios de PointSav, evitando entrelazamiento de IP. La tipografía canónica es Inter (código abierto, SIL OFL 1.1) en lugar de una tipografía asociada a una empresa específica — sin asociación de marca corporativa.

## Por qué importa la memoria muscular

Un diseñador o desarrollador que llega de cualquier entorno de sistema de diseño moderno reconoce los patrones estructurales del sustrato en segundos: escala de color numérica, capas DTCG, dos pistas tipográficas. Este reconocimiento es la rampa cognitiva de entrada. Es la mayor ventaja libre del sustrato — un profesional se adapta en días, no en semanas.

## Por qué importa el vocabulario

Un token nombrado por familia cromática con los valores exactos de un proveedor específico pone al sustrato a un litigio de marcas de distancia de un rediseño. Un token nombrado por rol con valores elegidos por PointSav, no.

## Véase también

- [[design-philosophy]] — las tres inversiones estructurales que motivan las decisiones de diseño del sustrato
- [[wiki-typography-system]] — la pila tipográfica IBM Plex construida sobre estas convenciones de tokens
- [[wiki-component-library]] — nueve componentes del wiki que consumen las capas de tokens descritas aquí
