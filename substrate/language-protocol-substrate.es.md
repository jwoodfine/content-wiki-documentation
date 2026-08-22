---
schema: foundry-doc-v1
title: "Sustrato de protocolo de lenguaje"
slug: language-protocol-substrate
lang: es
paired_with: language-protocol-substrate.md
category: substrate
type: topic
content_type: topic
quality: complete
index_group: core-named-substrates
short_description: "El mecanismo de enrutamiento que transporta el registro, tipo de documento y destino declarados de un borrador entre archivos — un campo de portada, una tabla de enrutamiento y una convención de buzón, no un sistema de adaptadores de IA."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-22
editor: pointsav-engineering
cites:
 - ni-51-102
 - osc-sn-51-721
---

Cada borrador que se mueve por la plataforma PointSav — un artículo de wiki, un README, una corrección legal, una traducción — declara de antemano su registro, tipo de documento y destino, en lugar de que estos se infieran después. Esa declaración es el sustrato de protocolo de lenguaje: un campo de portada, una tabla de enrutamiento y una convención de buzón, no un sistema de IA.

El sustrato tiene dos capas reales y separadas. La **capa de enrutamiento** es genuinamente operativa: cada borrador lleva un valor `language_protocol`, una tabla a nivel de espacio de trabajo mapea ese valor al archivo que lo posee, y un mensaje de buzón recoge el traspaso automáticamente. La **capa de registro y esquema** vive como datos, no como código — qué debe contener un documento PROSE o LEGAL, y qué palabras no puede usar. Archivos YAML en `pointsav-design-system` (un registro por wiki, una lista de vocabulario prohibido por wiki, un esquema por tipo de contenido) definen esas reglas; un script de linting las verifica antes de publicar. No existe una "taxonomía de adaptadores en cuatro familias" unificada, ningún adaptador LoRA compuesto por petición, ni un único crate de Rust que posea esquema, plantillas y validación juntos.

## Los cuatro valores de protocolo — reales, y cómo enrutan realmente

`PROSE-*`, `COMMS-*`, `LEGAL-*` y `TRANSLATE-*` son valores reales de `language_protocol`. Dos archivos gateway poseen el enrutamiento: `project-editorial` recibe PROSE/COMMS/LEGAL/TRANSLATE, `project-design` recibe DESIGN-*. Un borrador se marca con la portada `foundry-draft-v1` (protocolo, destino, campo de enrutamiento), y una convención de prefijo de mensaje de buzón lleva la intención de enrutamiento al archivo propietario automáticamente.

Lo que no es real: un sistema de IA que compone un modelo base con un adaptador de "voz de marca" y un adaptador por protocolo al momento de la inferencia. Tampoco existe un crate de Rust compartido que produzca "dieciocho plantillas de género" y "ocho términos prohibidos transversales." El contenido de registro y esquema que realmente gobierna cada protocolo son actualmente 3 esquemas de tipo de contenido (TOPIC, GUIDE, JOURNAL) y una lista de vocabulario prohibido por wiki — no una taxonomía única de dieciocho plantillas.

## Dónde vive realmente el contenido de registro y esquema

`pointsav-design-system/tokens/linguistic/` contiene un archivo de registro por wiki y una lista de vocabulario prohibido por wiki, cada término con su reemplazo aprobado en lenguaje llano. `pointsav-design-system/tokens/content-schema/` contiene el esquema de portada y estructura de cada tipo de contenido. `project-editorial` es el custodio de contenido de este subárbol de tokens; aplicar cambios pasa por la puerta de confirmación mecánica de `project-design`.

`editorial-lint.py` (de `project-editorial`) lee estos archivos de tokens directamente y verifica la estructura y el vocabulario de un borrador contra ellos antes de que pueda confirmarse. Es un script de linting que corre al momento de confirmar, no un adaptador de inferencia ni un servicio que otro componente invoca por petición.

## `service-proofreader` — un servicio real, desplegado por separado

`service-proofreader` es un servicio real de asistencia de escritura interactiva en ejecución (`local-proofreader.service`, puerto 9092) — pero no es un crate dentro de `pointsav-monorepo`, ni una pata de una división en cuatro servicios junto a `service-content`/`service-slm`. Es su propio despliegue, alcanzable desde la [[radical-proofreader-ui|consola de revisión]], y despacha su paso generativo a través del Doorman como cualquier otro llamador de inferencia.

## Véase también

- [[customer-hostability]]
- [[anti-homogenization-discipline]]
- [[apprenticeship-substrate]]
- [[citation-substrate]]
