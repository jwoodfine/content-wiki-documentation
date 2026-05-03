---
schema: foundry-doc-v1
title: "Grafo de citaciones como sustrato"
slug: citation-substrate.es
category: reference
type: topic
quality: published
short_description: Cómo PointSav incorpora un grafo de citaciones legible por máquinas en cada cláusula doctrinal, convención y documento publicado como un elemento de sustrato de primera clase.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
paired_with: citation-substrate.md
---

## Resumen estratégico

El sustrato de citaciones hace de la trazabilidad de fuentes una propiedad estructural de la plataforma en lugar de un complemento editorial. Cada documento declara sus dependencias de citación en metadatos YAML legibles por máquinas, cada referencia en línea se resuelve contra un registro central, y un mecanismo de verificación mantiene el registro actualizado a medida que las fuentes cambian.

## Elementos fundamentales

**El registro central.** Un registro de citaciones a nivel de espacio de trabajo sirve como resolvedor canónico para todas las citaciones. Asigna un identificador estable a cada entrada — por ejemplo, `ni-51-102` para el Instrumento Nacional 51-102. Citar el ID en lugar de una URL directa significa que la URL puede cambiar en el registro sin afectar a todos los documentos que la referencian.

**Metadatos de documento.** Cada cláusula doctrinal, convención y documento público declara sus dependencias de citación en un campo `cites:` en el encabezado YAML. Las herramientas pueden validar que cada ID declarado existe en el registro y generar automáticamente una sección de Referencias al final de cada documento.

**Tres clases de procedencia.** Cada afirmación en el corpus lleva una de tres clases: primaria (observación original, inmutable), derivada (razonamiento sobre afirmaciones primarias, versionada) o citada (autoridad externa, verificada periódicamente). El campo `evidence_class` hace explícita la clase de procedencia y permite filtrado por máquinas.

**Custodia autocurativa.** Cuando la capacidad de inferencia local de la plataforma esté operativa, está previsto que ejecute pasadas nocturnas de higiene del conocimiento contra el grafo de citaciones — verificando URLs, detectando desviaciones de contenido y detectando documentos que citan la misma autoridad pero hacen afirmaciones divergentes. Estas pasadas están diseñadas como sugerencias, no como correcciones automáticas.

## Conexión con la postura de divulgación

El sustrato de citaciones es la forma operacional de un elemento de la postura de divulgación continua: las citaciones se comprometen junto con el texto que respaldan, son legibles por máquinas y auditables. Un auditor puede seguir la cadena de citación desde una afirmación publicada hasta su fuente sin depender de la caracterización que hace la organización publicadora de lo que dice la fuente.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*
