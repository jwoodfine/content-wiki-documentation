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
last_edited: 2026-05-19
editor: pointsav-engineering
paired_with: _index.md
---

La categoría **patrones** recoge patrones de diseño nombrados realizados a través de la plataforma. Un patrón en esta categoría es una forma recurrente — aplicada en la capa editorial, de interfaz o de coordinación — que resuelve un problema estructural de una manera que otras partes de la plataforma reutilizan.

Los patrones se diferencian de los sustratos: un sustrato es un mecanismo portante del que depende la plataforma (y que se compone con el tiempo); un patrón es una decisión de diseño que puede aplicarse o no. Los patrones se diferencian de la arquitectura: un artículo de arquitectura describe cómo se compone un sistema específico; un patrón describe una forma que se repite en sistemas.

## Por dónde empezar

Lea primero [[source-of-truth-inversion]] y [[pairing-as-permission]] — son los patrones portantes sobre los que se construyen los demás.

## Patrones de soberanía e infraestructura

Los compromisos estructurales que definen qué es y qué no es un despliegue de PointSav.

- [[source-of-truth-inversion]] — Designa una capa como canónica (firmada, confirmada), una segunda como vista reconstruida de forma determinista, y una tercera como efímera de sesión; elimina clases enteras de errores de sincronización y pérdida de datos.
- [[pairing-as-permission]] — Un emparejamiento criptográfico entre dos nodos es el permiso; la ausencia de emparejamiento hace que la conexión sea estructuralmente imposible — no acceso denegado, sino ninguna ruta.
- [[zero-container-runtime]] — Cada despliegue se ejecuta como un binario Linux bajo systemd en una máquina virtual o host bare-metal estándar; sin entorno de ejecución de contenedores, sin orquestador de contenedores, sin plataforma de tiempo de ejecución gestionada.
- [[zero-execution-routing]] — Las capas de presentación aplican un mandato de cero ejecución: enrutamiento bilingüe mediante determinismo estructural y elementos interactivos mediante máquinas de estado CSS nativas, eliminando JavaScript del lado del cliente para la manipulación central del DOM.
- [[customer-first-ordering]] — Un proveedor de software que construye algo que un cliente instalará debe construirlo en el mismo orden en que el cliente lo instalará, sobre el mismo sustrato que el cliente utilizará.

## Despliegue y configuración

- [[deployment-patterns]] — Las seis configuraciones canónicas en las que se despliega el sustrato de PointSav — cada una construida sobre las mismas cinco primitivas y superficie de SO, con el Plan de Cuentas y la superficie de cumplimiento adaptados por segmento.

## Colaboración y flujo de trabajo editorial

- [[collab-via-passthrough-relay]] — El patrón de retransmisión de paso directo no mantiene estado del documento en el servidor y reenvía actualizaciones CRDT directamente entre clientes, manteniendo el árbol git canónico como único registro autoritativo en todo momento.
- [[model-tier-discipline]] — Enrutamiento del trabajo al nivel de modelo de IA apropiado — reflexión profunda, implementación o mecánico — para adecuar la capacidad del modelo a la forma del trabajo y controlar el coste de inferencia.

## Interfaz y experiencia de usuario

- [[knowledge-wiki-leapfrog-architecture]] — El diseño del motor app-mediakit-knowledge: elementos de interfaz con forma de Wikipedia sobre archivos Markdown git planos, con verificación de citaciones, procedencia del rastro de investigación e integración de IA en la edición como capa de diferenciación.
- [[location-intelligence-ux]] — La filosofía de diseño Conclusión Primero de Inteligencia de Ubicación: conclusiones de nivel ordenadas en lugar de puntos de datos individuales, para que los usuarios vean los nodos comerciales más defendibles a zoom nacional antes de profundizar en operadores individuales.

## Véase también

- [Sustrato](/substrate/) — mecanismos fundamentales sobre los que se construyen los patrones
- [Arquitectura](/architecture/) — arquitectura concreta de la plataforma
