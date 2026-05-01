---
schema: foundry-doc-v1
title: "El Sustrato de Divulgación Continua"
slug: topic-disclosure-substrate.es
category: architecture
type: topic
quality: published
short_description: Un wiki de documentación que funciona simultáneamente como registro de divulgación continua del emisor, con procedencia criptográfica y adaptadores de exportación regulatoria por jurisdicción.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
  - sec-17a-4-f
  - ixbrl-esef
  - opentimestamps
  - rfc-3161
paired_with: topic-disclosure-substrate.md
---

El **Sustrato de Divulgación Continua** es el patrón arquitectónico mediante el cual un wiki de documentación de PointSav funciona simultáneamente como documentación operativa y como registro de divulgación autorizado del emisor. En lugar de mantener documentación interna, un sitio de relaciones con inversores gestionado por un proveedor externo y presentaciones estatutarias periódicas como tres cuerpos de texto separados, el sustrato los unifica en un único corpus Markdown que se renderiza en todos los formatos requeridos desde una sola fuente canónica.

## La inversión del modelo tradicional

Los emisores tradicionales mantienen registros superpuestos: un sistema de documentación interno, un sitio de relaciones con inversores en infraestructura de un proveedor, y presentaciones periódicas a reguladores nacionales. Estos tres cuerpos de texto frecuentemente son inconsistentes, se mantienen en ciclos de actualización diferentes y se alojan en proveedores cuya jurisdicción puede no coincidir con la del emisor.

El Sustrato de Divulgación Continua invierte este patrón. Un conjunto de archivos TOPIC en Markdown, confirmados con procedencia firmada en un repositorio wiki alojado en la infraestructura propia del emisor, genera todos los resultados requeridos: HTML renderizado para lectores públicos, documentos iXBRL para presentaciones ESEF de la UE, paquetes de presentación para SEDAR+ en Canadá, envíos XBRL para EDGAR en los Estados Unidos, y equivalentes para otras jurisdicciones mediante adaptadores de exportación configurables. La misma fuente Markdown que un lector navega en el wiki público es el registro de divulgación.

## Procedencia criptográfica y disciplina de dos relojes

Cada TOPIC lleva dos capas de procedencia criptográfica. El SHA del commit de Git más la ruta del archivo forman una identidad de contenido estable y verificable. Los mecanismos de sellado de tiempo — OpenTimestamps anclado a Bitcoin y el protocolo RFC 3161 mediante una Autoridad de Sellado de Tiempo con reconocimiento legal formal — se aplican de forma redundante a cada confirmación en la rama del wiki.

Una disciplina de dos relojes distingue `published_at` (cuándo el wiki renderizó el estado del contenido) de `valid_at` (cuándo el hecho subyacente es válido). Esta distinción aborda la brecha estándar en la divulgación: el momento de publicación no equivale al momento de validez del hecho. Ambas marcas de tiempo se anclan de forma independiente.

## Adaptadores de exportación y postura jurisdiccional

Un adaptador de exportación configurable por superficie regulatoria transforma el corpus Markdown junto con las anotaciones de metadatos en el formato de presentación requerido por cada regulador — incluyendo adaptadores para SEC EDGAR, SEDAR+ canadiense, ESEF europeo, EDINET de Japón, DART de Corea y MAGNA de Israel.

Para jurisdicciones con repositorios estatutarios sólidos, el sustrato es el complemento de frescura continua a las presentaciones periódicas. Para jurisdicciones donde el repositorio estatutario es cerrado, propietario o inaccesible al público, el sustrato se convierte en el registro abierto canónico. El registro de divulgación vive en la infraestructura propia del emisor, bajo su propia jurisdicción, portable por construcción entre jurisdicciones.

## Estado de implementación

El motor del wiki (Rust, axum + comrak + maud) está operativo. Los adaptadores de exportación por jurisdicción, el módulo de extracción iXBRL, el sellado de tiempo criptográfico y el mecanismo de fundamentación de IA impuesto por el sustrato están planificados para un clúster dedicado `project-disclosure`. Cuando esté operativo, el sustrato será estructuralmente incapaz de publicar resultados de IA sin fundamentación — una propiedad necesaria para que el wiki funcione como registro de divulgación bajo escrutinio regulatorio.

## Véase también

- [[compounding-doorman]] — el límite de inferencia que hace cumplir la disciplina de sanitización de salida en cada llamada editorial asistida por IA
- [[knowledge-commons]] — la línea entre conocimiento público y servicios de pago
- [[topic-language-protocol-substrate]] — el proceso editorial que produce contenido TOPIC al registro requerido

## Referencias

1. NI 51-102 Obligaciones de Divulgación Continua — Administradores de Valores de Canadá.
2. Reglamento ESEF — Formato Electrónico Único Europeo, iXBRL.
3. OpenTimestamps — sellado de tiempo anclado a Bitcoin, código abierto.
4. RFC 3161 — Protocolo de Sellado de Tiempo PKI de Internet X.509.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Atribución 4.0 Internacional](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.