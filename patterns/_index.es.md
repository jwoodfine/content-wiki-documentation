---
schema: foundry-doc-v1
title: "Patrones de diseño"
slug: patterns-index.es
category: patterns
type: topic
quality: complete
short_description: "La categoría de patrones recoge patrones de diseño nombrados realizados a través de la plataforma — el embudo editorial inverso, la inversión de la fuente de verdad, emparejamiento-como-permiso, el salto en la capa de artículo, el cromo de salto de Wikipedia — cada uno una forma recurrente aplicada en la capa editorial, de interfaz o de coordinación."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-09
editor: pointsav-engineering
paired_with: _index.md
---

La categoría **patrones** recoge patrones de diseño nombrados realizados a través de la plataforma. Un patrón en esta categoría es una forma recurrente — aplicada en la capa editorial, de interfaz o de coordinación — que resuelve un problema estructural de una manera que otras partes de la plataforma reutilizan.

Los patrones se diferencian de los sustratos: un sustrato es un mecanismo portante del que depende la plataforma (y que se compone con el tiempo); un patrón es una decisión de diseño que puede aplicarse o no. Los patrones se diferencian de la arquitectura: un artículo de arquitectura describe cómo se compone un sistema específico; un patrón describe una forma que se repite en sistemas.

## Orden de lectura

[[source-of-truth-inversion]] (la división canónico / vista / efímero) y [[pairing-as-permission]] (control de acceso basado en capacidades) son los patrones más fundamentales — léalos primero. [[reverse-funnel-editorial-pattern]] explica la canalización editorial utilizada para refinar borradores a escala. [[wikipedia-leapfrog-design]] y [[article-shell-leapfrog]] explican el contrato del cromo del wiki con la memoria muscular del lector. [[collab-via-passthrough-relay]] documenta el mecanismo de colaboración en tiempo real que no contiene estado del documento.

## Véase también

- [[substrate]] — mecanismos fundamentales sobre los que se construyen los patrones
- [[architecture]] — arquitectura concreta de la plataforma
