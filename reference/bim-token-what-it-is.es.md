---
schema: foundry-doc-v1
title: "Qué es un BIM Token"
slug: bim-token-what-it-is
language: es
category: reference
type: topic
quality: core
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-06
editor: pointsav-engineering
cites: []
paired_with: bim-token-what-it-is.md
---

El modelado de información de construcción (BIM, por sus siglas en inglés) produce representaciones digitales detalladas de estructuras, pero no previene violaciones normativas. Un modelo puede ser geométricamente completo y estar correctamente clasificado según el esquema IFC y seguir conteniendo elementos que incumplen la normativa de construcción, no alcanzan los umbrales de rendimiento climático o entran en conflicto con la regulación jurisdiccional — fallas que solo se descubren cuando un verificador posterior al diseño las detecta. Un BIM Token aborda este problema antes de que ocurra: codifica la decisión sobre un elemento constructivo como una unidad de especificación composable y reutilizable que pre-limita el espacio de diseño en lugar de auditar un modelo terminado.

## Definición

Un BIM Token es una unidad de especificación del entorno construido — el equivalente estructural de un token de sistema de diseño de software. Donde un token de sistema de diseño codifica una decisión de diseño (un color, una unidad de espaciado, una receta de componente) como un valor reutilizable y referenciable que todas las superficies deben respetar, un BIM Token codifica una decisión sobre un elemento constructivo en tres ejes simultáneos:

1. **Qué ES el elemento** — su clase de entidad IFC, su referencia de clasificación Uniclass 2015, su URI de identidad en bSDD y las plantillas de conjuntos de propiedades aplicables.
2. **Qué DEBE cumplir** — los requisitos normativos impuestos por su jurisdicción, expresados como superposiciones jurisdiccionales (archivos de restricción IDS 1.0 y fragmentos de exclusión geométrica IFC).
3. **Cómo DEBE comportarse** — los requisitos de rendimiento energético, térmico, estructural y acústico impuestos por su zona climática, expresados como parámetros tabulados referenciados a ASHRAE y normas nacionales equivalentes.

Colocar un BIM Token en un modelo significa colocar simultáneamente el elemento, su envolvente normativa y su umbral de rendimiento climático. Las violaciones son geométricamente imposibles por construcción, en lugar de descubrirse en la revisión posterior al diseño.

## La tesis del pre-condicionamiento

Dos décadas de herramientas BIM se han construido sobre un supuesto de validación posterior: diseñar libremente y luego comprobar. Las plataformas de validación comerciales ejecutan reglas sobre modelos terminados y generan informes de incumplimiento. El sistema CORENET X de Singapur — el sistema gubernamental de validación BIM más avanzado en producción — opera bajo este mismo principio.

El enfoque de pre-condicionamiento invierte esta lógica. Si los únicos elementos disponibles para un diseñador son BIM Tokens, y cada token ya codifica las restricciones normativas y de rendimiento aplicables a su tipo en una jurisdicción y zona climática determinadas, el informe de conformidad es estructuralmente innecesario. El modelo no puede ser no conforme porque las configuraciones no conformes no pueden colocarse.

Esta es una afirmación composicional, no de validación. La distinción importa porque los validadores generan informes que requieren corrección humana. Un sistema de composición que aplica restricciones en el momento de colocación no tiene infracciones que reportar.

## Tres capas

Un BIM Token tiene tres capas. Las tres son datos incorporados en el token. Ninguna es una opción seleccionable en tiempo de ejecución.

- **Capa 1 — Especificación:** la identidad permanente del token (clase IFC, referencia Uniclass 2015, URI bSDD, descripción y conjuntos de propiedades aplicables).
- **Capa 2 — Normativa:** una tabla de superposiciones jurisdiccionales registradas, mostrando todos los requisitos de todas las jurisdicciones registradas simultáneamente.
- **Capa 3 — Zona climática:** una tabla de requisitos de rendimiento por zona climática, alineada con ASHRAE 90.1, el Código Nacional de Construcción de Canadá y las normas EN ISO 52000 de la UE.

La regla de composición es: `valor_efectivo = max(requisito_normativo, requisito_climático)`. Los fragmentos de exclusión geométrica IFC anulan incondicionalmente cualquier restricción numérica.

## Forma de implementación

Los BIM Tokens se almacenan en formato JSON del Grupo de Comunidad de Tokens de Diseño del W3C (DTCG), extendido con tipos de tokens específicos para el sector AEC. El mecanismo estándar de alias DTCG permite la composición entre tokens: un token de conjunto de muro cortina puede referenciar sus tokens de unidad de acristalamiento, perfil de parteluz y rotura de puente térmico.

El formato legible por máquina permite la integración con cualquier herramienta BIM compatible con DTCG, el versionado independiente de las superposiciones normativas, y la operación sin conexión — requisito indispensable para proyectos con restricciones ITAR, soberanía GDPR y obras en sitios remotos.

## Véase también

- [[bim-token-three-layers]]
- [[building-design-system-bim]]
- [[city-code-as-composable-geometry]]
- [[flat-file-bim-leapfrog]]
- [[bim-token-taxonomy]]

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™ y Totebox Archive™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos titulares.*
