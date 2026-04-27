---
schema: foundry-doc-v1
document_version: 0.1.0
title: "Compatibilidad nativa con el sustrato — por qué se eliminó el adaptador de la Action API"
slug: topic-substrate-native-compatibility
category: architecture
status: published
last_edited: 2026-04-27
editor: pointsav-engineering
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
lang: es
paired_with: topic-substrate-native-compatibility.md
cites:
  - ni-51-102
  - osc-sn-51-721
  - mediawiki-action-api
  - mediawiki-xml-dump
---

## Visión general

El motor de wiki de PointSav en `documentation.pointsav.com` adopta lo que la doctrina técnica interna denomina la postura *nativa con el sustrato*: la plataforma replica la compatibilidad estructural que un lector o integrador externo espera de MediaWiki — rutas `/wiki/{slug}`, sintaxis `[[wikilink]]`, importación de volcados XML — sin replicar la mimesis de interfaces internas, es decir, sin implementar la Action API de MediaWiki.

Esta decisión descansa en la reclamación #29 de la doctrina (Sustitución de Sustrato): cuando el sustrato reemplaza una plataforma existente, adopta las convenciones que ya son útiles y declina los contratos de interfaz que impondrían costes de mantenimiento y cumplimiento desproporcionados con respecto al beneficio obtenido.

## El ecosistema y sus dos componentes

El ecosistema MediaWiki es amplio: alrededor de 1.500 extensiones, cientos de miles de plantillas, el marco de automatización pywikibot, integración con Wikidata y el archivo de práctica operativa de Wikipedia y sus proyectos hermanos. Un motor wiki que prometa compatibilidad con MediaWiki hereda por referencia una parte de ese capital.

Sin embargo, ese capital tiene dos componentes con costes muy distintos.

El primer componente es la **compatibilidad estructural para lectores e integradores externos**: convenciones de URL, sintaxis de marcado, volcados XML de corpus. El sustrato las adopta porque son útiles y su mantenimiento es estable a lo largo de años.

El segundo componente es la **mimesis de interfaces internas**: endpoints de la Action API que extensiones y bots consumen. Cada endpoint replicado es un contrato que evoluciona con las versiones de MediaWiki, exige auditorías de seguridad independientes y amplía la superficie de divulgación continua que el sustrato asume ante inversores y contrapartes.

El sustrato participa plenamente en el primer componente y declina deliberadamente el segundo.

## Qué se conservó y qué se eliminó

Se conservaron cuatro superficies de compatibilidad de bajo coste: la ruta de importación de volcados XML (planificada; herramienta `import-mediawiki-xml` pendiente de implementación) `[mediawiki-xml-dump]`, las convenciones de URL `/wiki/{slug}`, la sintaxis de wikilinks `[[slug]]` y la sintaxis de notas al pie `[^1]` de CommonMark. Estas cuatro superficies no exigen ejecutar un analizador sintáctico de MediaWiki, una API de MediaWiki ni un marco de extensiones de MediaWiki.

Se eliminaron tres superficies de alto coste: el adaptador de la Action API `[mediawiki-action-api]` (eliminado del alcance en v0.1.14), las plantillas y funciones de analizador de MediaWiki, y el ecosistema pywikibot. En su lugar, el sustrato expone interfaces nativas — `GET /wiki/{slug}`, `POST /edit/{slug}`, `GET /sitemap.xml`, feeds Atom y JSON, búsqueda Tantivy — que cubren los mismos casos de uso sin comprometer al sustrato con el contrato de API de Wikipedia.

## Postura de divulgación como lente de compatibilidad

La razón más profunda de la postura nativa con el sustrato es que las decisiones sobre superficies de compatibilidad son, en el fondo, decisiones de divulgación continua. Toda interfaz que el sustrato expone públicamente constituye una obligación de divulgación bajo los marcos regulatorios aplicables `[ni-51-102]`. Lo que el sustrato no expone, no tiene que divulgar ni mantener como registro canónico.

Un adaptador de la Action API que devolviera `?action=query&prop=revisions` habría introducido un segundo registro canónico del historial de artículos paralelo al historial de Git — fuente primaria que ya existe y es verificable. Cualquier divergencia entre ambos registros habría sido un conflicto de divulgación. El sustrato declina el adaptador y mantiene Git como fuente única de verdad.

## El patrón se generaliza

La sustitución de sustrato se aplica más allá de MediaWiki: plataformas de distribución de divulgación financiera, CRM de clase Salesforce, registros corporativos de clase SAP, y almacenamiento SaaS de documentos. En cada caso el análisis sigue la misma lógica: qué obliga la interfaz de la plataforma existente al sustrato, y qué gana el sustrato a cambio. El sustrato conserva las superficies que puede fundamentar en divulgación; declina el resto.

La eliminación de la Action API de MediaWiki es el caso de estudio canónico. El patrón es estructuralmente determinante para la trayectoria más amplia del sustrato.

*Las afirmaciones con proyección futura en este documento — en particular respecto a la herramienta `import-mediawiki-xml` y al esquema de URL `verify://` — están sujetas a los factores de precaución aplicables bajo `[ni-51-102]` y `[osc-sn-51-721]`. La base razonable es el estado del sustrato operativo en v0.1.29.*
