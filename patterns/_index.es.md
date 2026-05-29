---
schema: foundry-doc-v1
title: "Patrones de diseño"
slug: patterns-index.es
category: patterns
type: topic
quality: complete
short_description: "La categoría de patrones recoge patrones de diseño nombrados realizados a través de la plataforma — inversión de la fuente de verdad, emparejamiento-como-permiso, runtime sin contenedores, enrutamiento sin ejecución, orden cliente-primero, disciplina de niveles de modelo, patrones de despliegue, el relevo de paso directo, la arquitectura de salto del wiki de conocimiento y la experiencia de inteligencia de ubicación — cada uno una forma recurrente aplicada en la capa editorial, de interfaz o de coordinación."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-29
editor: pointsav-engineering
paired_with: _index.md
---

La categoría **patrones** recoge patrones de diseño nombrados realizados a través de la plataforma. Un patrón en esta categoría es una forma recurrente — aplicada en la capa editorial, de interfaz o de coordinación — que resuelve un problema estructural de una manera que otras partes de la plataforma reutilizan. Los patrones se diferencian de los sustratos: un sustrato es un mecanismo portante del que depende la plataforma (y que se compone con el tiempo); un patrón es una decisión de diseño que puede aplicarse o no. Los patrones se diferencian de la arquitectura: un artículo de arquitectura describe cómo se compone un sistema específico; un patrón describe una forma que se repite en sistemas.

Los patrones de esta colección se sitúan sobre el [[compounding-substrate|sustrato compuesto]] y la [[three-ring-architecture|arquitectura de tres anillos]] — describen cómo la plataforma expresa esos fundamentos en formas recurrentes y nombradas.

## Por dónde empezar

Lea primero [[source-of-truth-inversion|inversión de la fuente de verdad]] y [[pairing-as-permission|emparejamiento-como-permiso]] — son los patrones portantes sobre los que se construyen los demás.

## Patrones de soberanía e infraestructura

Los compromisos estructurales que definen qué es y qué no es un despliegue de PointSav.

- [[source-of-truth-inversion|Inversión de la fuente de verdad]] — Designa una capa como canónica (firmada, confirmada), una segunda como vista reconstruida de forma determinista, y una tercera como efímera de sesión; elimina clases enteras de errores de sincronización y pérdida de datos.
- [[pairing-as-permission|Emparejamiento-como-permiso]] — Un emparejamiento criptográfico entre dos nodos es el permiso; la ausencia de emparejamiento hace que la conexión sea estructuralmente imposible — no acceso denegado, sino ninguna ruta.
- [[zero-container-runtime|Runtime sin contenedores]] — Cada despliegue se ejecuta como un binario Linux bajo systemd en una máquina virtual o host bare-metal estándar; sin entorno de ejecución de contenedores, sin orquestador de contenedores, sin plataforma de tiempo de ejecución gestionada.
- [[zero-execution-routing|Enrutamiento sin ejecución]] — Las capas de presentación aplican un mandato de cero ejecución: enrutamiento bilingüe mediante determinismo estructural y elementos interactivos mediante máquinas de estado CSS nativas, eliminando JavaScript del lado del cliente para la manipulación central del DOM.
- [[customer-first-ordering|Orden cliente-primero]] — Un proveedor de software que construye algo que un cliente instalará debe construirlo en el mismo orden en que el cliente lo instalará, sobre el mismo sustrato que el cliente utilizará.
- [[customer-hostability|Alojabilidad por el cliente]] — El compromiso arquitectónico de que cada artefacto se ejecute en el propio hardware del cliente, contra las propias claves del cliente, con el propio libro de auditoría del cliente.

## Despliegue y configuración

Las configuraciones canónicas en las que se envía el sustrato y las disciplinas que mantienen los despliegues componibles.

- [[deployment-patterns|Patrones de despliegue]] — Las seis configuraciones canónicas en las que se despliega el sustrato de PointSav — cada una construida sobre las mismas cinco primitivas y superficie de SO, con el Plan de Cuentas y la superficie de cumplimiento adaptados por segmento.
- [[three-layer-architecture|Arquitectura de tres capas]] — Cómo los entregables PointSav se mueven a través de las capas SOFTWARE, SHOWCASE e INSTANCE con un flujo estricto unidireccional de proveedor a cliente.
- [[3-layer-stack|Pila de tres capas]] — La descomposición de infraestructura en tres capas: capacidad de cómputo bruta, ejecución de plataforma aislada y acceso seguro del operador.

## Colaboración y flujo de trabajo editorial

Patrones que gobiernan cómo múltiples sesiones, múltiples motores y múltiples humanos colaboran sin corromper el registro canónico.

- [[collab-via-passthrough-relay|Colaboración por relevo de paso directo]] — El patrón de retransmisión de paso directo no mantiene estado del documento en el servidor y reenvía actualizaciones CRDT directamente entre clientes, manteniendo el árbol git canónico como único registro autoritativo en todo momento.
- [[model-tier-discipline|Disciplina de niveles de modelo]] — Enrutamiento del trabajo al nivel de modelo de IA apropiado — reflexión profunda, implementación o mecánico — para adecuar la capacidad del modelo a la forma del trabajo y controlar el coste de inferencia.
- [[multi-engine-session-coordination|Coordinación de sesiones multimotor]] — Cómo múltiples motores de IA coordinan sobre el mismo espacio de trabajo sin competir por el `.git/index` ni por el estado de sesión del otro.
- [[mailbox-atomicity|Atomicidad de buzón]] — La primitiva atómica de buzón que mantiene consistentes los traspasos entrada/salida entre sesiones bajo escrituras concurrentes.

## Interfaz y experiencia de usuario

Patrones que se repiten en el cromo orientado al operador — el wiki, la superficie de inteligencia de ubicación, la familia de escritorio.

- [[knowledge-wiki-leapfrog-architecture|Arquitectura de salto del wiki de conocimiento]] — El diseño del motor wiki: elementos de interfaz con forma de Wikipedia sobre archivos Markdown git planos, con verificación de citaciones, procedencia del rastro de investigación e integración de IA en la edición como capa de diferenciación.
- [[location-intelligence-ux|Experiencia de inteligencia de ubicación]] — La filosofía de diseño Conclusión Primero: conclusiones de nivel ordenadas en lugar de puntos de datos individuales, para que los usuarios vean los nodos comerciales más defendibles a zoom nacional antes de profundizar en operadores individuales.
- [[wikipedia-leapfrog-design|Diseño de salto sobre Wikipedia]] — Qué hereda el motor wiki de Wikipedia, qué añade más allá y qué significa el margen de salto del cinco por ciento.

## Véase también

- [Sustrato](/substrate/) — mecanismos fundamentales sobre los que se construyen los patrones
- [Arquitectura](/architecture/) — arquitectura concreta de la plataforma
- [Aplicaciones](/applications/) — aplicaciones orientadas al operador que componen estos patrones
- [Sistemas](/systems/) — los sistemas operativos en los que se realizan los patrones
