---
schema: foundry-topic-v1
title: "Compatibilidad nativa del sustrato — por qué se descartó el adaptador de Action API"
status: published
category: architecture
last_edited: 2026-04-30
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
language: es
companion: architecture/topic-substrate-native-compatibility.md
cites:
  - doctrine-claim-29
  - ni-51-102
---

## La elección

El wiki de ingeniería de PointSav en `documentation.pointsav.com` es un wiki nativo del sustrato. Acepta una importación única de XML de MediaWiki, sirve URLs con la forma familiar `/wiki/{slug}` de MediaWiki, acepta la sintaxis de Wikipedia con `[[wikilink]]` y `[^nota]`, y se detiene ahí. No implementa la Action API de MediaWiki, no soporta plantillas de MediaWiki, y no proporciona una superficie de escritura que imite los endpoints REST de MediaWiki.

Esta es la postura nativa del sustrato conforme a la reclamación #29 de Doctrine (Sustitución de Sustrato): cuando el sustrato sustituye el papel de una plataforma existente, replica la compatibilidad estructural — las superficies que un lector o integrador externo encuentra — sin replicar la imitación de interfaces — la forma de API que una integración de sistema interno consumiría. La distinción es fundamental.

## Por qué el foso del ecosistema es real pero costoso

El ecosistema de MediaWiki es real: aproximadamente 1.500 extensiones, cientos de miles de plantillas, un marco de bots maduro (pywikibot), integración con Wikidata, y una larga trayectoria operacional en Wikipedia, Wikiquote y numerosas instalaciones autohospedadas. Sin embargo, el foso tiene dos partes con costos muy diferentes.

La primera parte es la compatibilidad estructural para lectores e integradores: un lector que conoce el patrón de URL y el marcado de Wikipedia puede navegar y editar sin reentrenamiento. Esta parte es de bajo costo — el sustrato adopta convenciones porque son útiles, no como imitación.

La segunda parte es la imitación de interfaces de sistemas internos: extensiones que leen y escriben a través de la Action API, bots que se autentican contra el flujo de inicio de sesión de MediaWiki. Esta parte es de alto costo — cada endpoint de API imitado requiere mantenimiento frente a la evolución de MediaWiki, endurecimiento de seguridad, y auditoría de cumplimiento. El sustrato elige participar plenamente en la primera parte y declinar deliberadamente la segunda.

## Lo que se conservó y lo que se descartó

Se conservaron cuatro superficies de compatibilidad, todas en la categoría de bajo costo: la ruta de importación xml-dump, las convenciones de URL (`/wiki/{slug}`), la sintaxis de wikilinks (`[[slug]]`) y la sintaxis de notas al pie (`[^1]`). Estas cuatro superficies dan al wiki del sustrato el alcance del ecosistema de lectores e integradores que se espera de un despliegue de MediaWiki sustituido por el sustrato, sin requerir un analizador de MediaWiki, una API de MediaWiki ni un marco de extensiones de MediaWiki.

Se descartaron tres superficies de la categoría de alto costo: el adaptador de Action API (que habría multiplicado la superficie de auditoría de cumplimiento por un orden de magnitud), las plantillas y funciones de análisis de MediaWiki (que requerirían ejecutar un analizador de lenguaje Turing-completo en tiempo de renderizado), y el ecosistema de pywikibot (sustituido por las herramientas del espacio de trabajo existentes).

## La postura de divulgación como lente de compatibilidad

Las elecciones de superficie de compatibilidad del motor wiki son elecciones de divulgación continua encubiertas. Cada interfaz que el sustrato expone al público lo compromete con una obligación de divulgación conforme a [ni-51-102]. Lo que el sustrato no expone, no necesita divulgar.

Un adaptador de Action API que retornara el historial de revisiones habría creado un segundo registro canónico paralelo al historial git — cualquier divergencia sería un fallo de divulgación. El sustrato declina el adaptador y mantiene git como canónico. El mismo razonamiento se aplica al renderizado del lado del servidor y a la edición autenticada: el sustrato conserva las garantías del trajectory-substrate (reclamación #15 de Doctrine) al no replicar el flujo de autenticación de MediaWiki con menor proveniencia.

El patrón: cada interfaz que el sustrato no replica es una obligación que no asume.

## Véase también

- [[source-of-truth-inversion]] — La designación de capa de almacenamiento de la que depende este patrón.
- [[app-mediakit-knowledge]] — El motor wiki que este patrón gobierna.
- [[wikipedia-leapfrog-design]] — La intención de diseño del chrome del wiki.
- [[disclosure-substrate]] — La convención de divulgación continua y los casos de sustitución adicionales.

## Procedencia

Vista general estratégica en español elaborada por project-language el 2026-04-30. Basada en el borrador de project-knowledge (sesión 619abe3eff24497e, 2026-04-27). Por DOCTRINE.md §XII, esta vista general no es una traducción literal — adapta el concepto central para lectores en español.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
