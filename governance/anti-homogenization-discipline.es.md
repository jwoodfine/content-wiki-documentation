---
schema: foundry-doc-v1
title: "Anti-Homogenization Discipline"
slug: anti-homogenization-discipline.es
category: governance
type: topic
quality: stub
short_description: "Anti-homogenization discipline is the architectural posture that resists AI writing assistants pulling contributors toward a single voice, by defaulting to flagging potential issues rather than silently rewriting text."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
  - ni-51-102
paired_with: anti-homogenization-discipline.md
---
# Disciplina anti-homogenización (resumen)

La mayoría de los asistentes de escritura con IA empujan
silenciosamente a sus usuarios hacia una voz única. Investigación
de Cornell (arXiv 2409.11360, 2024) encontró que las sugerencias
de IA empujan a escritores no occidentales hacia el registro
occidental con tasas más altas y con ganancias de productividad
más pequeñas, porque los escritores gastan tiempo adicional
corrigiendo la deriva de la IA hacia su voz auténtica. La
disciplina anti-homogenización de Foundry es la postura
arquitectónica que resiste esa deriva explícitamente.

## El problema

Un asistente entrenado centralmente sobre un corpus homogéneo
sugerirá, en promedio, ediciones que mueven el texto hacia el
centroide de ese corpus. Para usuarios cuya voz ya está en el
centroide, la IA es útil. Para usuarios cuya voz no está allí,
la IA es una fuerza constante que tira hacia la voz de otra
persona — usualmente la voz del hablante con mayor presencia
en los datos de entrenamiento.

## La disciplina — marcar, no reescribir

La acción editorial por defecto en Foundry es **marcar**, no
**reescribir**. Cuando el asistente identifica un problema
potencial, lo expone y propone una edición; no reescribe
silenciosamente el texto del usuario. La voz del usuario es la
autoridad, salvo delegación explícita de reescritura.

## Adaptadores por inquilino preservan la voz

El álgebra de composición de adaptadores de Foundry separa el
adaptador por inquilino del adaptador de protocolo. El
adaptador por inquilino entrena sobre el corpus del cliente
dentro de su sustrato y aprende su voz: las palabras que usa,
los ritmos de oración que prefiere, el registro por defecto.

Al componer en tiempo de petición, la salida refleja ambos:
las convenciones del género del protocolo y la voz del
inquilino. Un README escrito por Foundry dentro del sustrato
del Cliente A suena como el Cliente A; el mismo README dentro
del sustrato del Cliente B suena como el Cliente B.

## Pruebas operativas

Una nueva característica editorial satisface la disciplina si
cada edición automatizada se presenta como propuesta, el
adaptador por inquilino se compone con el adaptador de
protocolo en tiempo de petición, las tuplas firmadas
alimentan la pre-formación continuada del adaptador del
cliente (no de un adaptador compartido), y el cliente puede
auditar qué adaptadores estuvieron activos en cualquier
acción editorial.

## Véase también

- [Documento canónico en inglés](topic-anti-homogenization-discipline.md)
- [El sustrato de protocolo de lenguaje](topic-language-protocol-substrate.md)
- [Hospedaje por el cliente](topic-customer-hostability.md)


---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™ y Totebox Archive™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos titulares.*
