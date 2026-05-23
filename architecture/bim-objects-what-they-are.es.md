---
schema: foundry-doc-v1
title: "Objetos BIM — Qué son"
slug: bim-objects-what-they-are
short_description: "Los BIM Objects son unidades de especificación del entorno construido componibles que codifican el tipo de elemento, requisitos regulatorios por jurisdicción y requisitos de desempeño de zona climática, preconstriñendo el espacio de diseño para que las configuraciones no conformes no puedan colocarse."
language: es
category: architecture
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-17
editor: pointsav-engineering
cites: [ifc-4-3, uniclass-2015, bsdd-v1, ids-1-0, dtcg-w3c]
paired_with: bim-objects-what-they-are.md
---

El Modelado de Información para la Construcción produce representaciones digitales detalladas de estructuras. En su forma estándar, no previene infracciones. Un modelo puede estar geométricamente completo, con materiales especificados y clasificado por tipo de entidad IFC, y aún así contener elementos que no cumplen con el código, violan los requisitos de desempeño climático o entran en conflicto con regulaciones jurisdiccionales — descubrimientos que sólo se hacen cuando un verificador posterior al diseño se ejecuta. Un Objeto BIM aborda esto desde el principio. Codifica una decisión sobre un elemento del entorno construido como una unidad de especificación composable y reasignable que pre-restringe el espacio de diseño en lugar de auditar un modelo completado.

## Definición

Un Objeto BIM es una unidad de especificación composable para el entorno construido — el equivalente estructural de un Token del Sistema de Diseño. Donde un Token del Sistema de Diseño codifica una decisión de diseño (un color, una unidad de espaciado, una receta de componente) como un valor reutilizable y reasignable que todas las superficies conformes deben respetar, un Objeto BIM codifica una decisión sobre un elemento del entorno construido en tres ejes simultáneos:

1. **Lo que el elemento ES** — su clase de entidad IFC, clasificación Uniclass 2015, URI de identidad bSDD, y plantillas de conjuntos de propiedades aplicables.
2. **Lo que DEBE satisfacer** — los requisitos regulatorios impuestos por su jurisdicción, expresados como superposiciones jurisdiccionales (archivos de restricción IDS 1.0 y fragmentos geométricos de exclusión IFC).
3. **Cómo DEBE desempeñarse** — los requisitos de energía, térmicos, estructurales y acústicos impuestos por su zona climática, expresados como parámetros de desempeño tabulares vinculados a ASHRAE y normas nacionales equivalentes.

Al colocar un Objeto BIM en un modelo se colocan simultáneamente el elemento, su envolvente regulatoria y su piso de desempeño climático. Las infracciones son geométricamente imposibles por construcción, en lugar de ser descubiertas en la revisión posterior al diseño.

## Lo que un Objeto BIM NO Es

La precisión requiere distinguir el Objeto BIM de cuatro estructuras a las que se asemeja superficialmente.

**No es un tipo de entidad IFC.** IFC 4.3 (ISO 16739-1:2024) define `IfcWall`, `IfcSlab`, `IfcBeam` y aproximadamente 900 otras clases de esquema. Un tipo de entidad IFC es una clase de esquema — define la forma que deben tener los datos de un registro de muro. No lleva valores de restricción, requisitos específicos de jurisdicción ni parámetros de desempeño. Un Objeto BIM usa la clase de entidad IFC como ancla de identidad, pero agrega las tres capas de restricción que la clase de esquema no puede contener.

**No es una Familia de Revit.** Una Familia de Revit es geometría parametrizada para una herramienta de autoría, almacenada en un formato binario propietario y vinculada a un proveedor. No lleva datos regulatorios normativos, mapeo de jurisdicción ni especificación de desempeño de zona climática. Un Objeto BIM es JSON simple (formato W3C DTCG), neutro respecto a las herramientas y legible por máquinas por cualquier consumidor conforme.

**No es una hoja de cálculo COBie.** COBie (Construction Operations Building Information Exchange) es captura de datos posterior al hecho — datos de gestión de instalaciones extraídos de un modelo después de que el diseño está completo. Documenta lo que se construyó. Un Objeto BIM restringe lo que puede colocarse.

**No es un Conjunto de Propiedades IFC.** Un Conjunto de Propiedades IFC (`Pset_WallCommon`, etc.) es una plantilla para valores sin lógica de aplicación, jerarquía de restricciones ni mapeo de jurisdicción. Registra propiedades; no las hace cumplir. Un Objeto BIM incluye definiciones de conjuntos de propiedades aplicables, pero agrega las capas de aplicación regulatoria y de zona climática que los conjuntos de propiedades no pueden expresar.

**No es un archivo de modelo BIM.** Un modelo IFC es una instancia geométrica para un proyecto específico. Un Objeto BIM es una especificación reutilizable — una plantilla que genera instancias geométricas conformes cuando se instancia.

## La Tesis de Pre-Restricción

Dos décadas de herramientas BIM se han construido sobre un supuesto de validación primero: diseñar libremente y luego verificar. Solibri, Archistar y plataformas similares ejecutan reglas contra modelos completados e informan infracciones. Singapore CORENET X — el sistema de presentación BIM gubernamental más avanzado en producción — opera bajo el mismo principio. Presentar un modelo; recibir un informe de cumplimiento.

El enfoque de pre-restricción invierte esto. Si los únicos elementos disponibles para un diseñador son Objetos BIM, y cada Objeto BIM ya codifica las restricciones regulatorias y de desempeño aplicables a su tipo en una jurisdicción y zona climática dadas, entonces el informe de cumplimiento es estructuralmente innecesario. El modelo no puede ser no conforme porque las configuraciones no conformes no pueden colocarse.

Esta es una afirmación composicional, no una afirmación de validación. La distinción importa porque los validadores generan informes que requieren remediación humana. Un sistema de composición que aplica restricciones en el momento de la colocación no tiene infracciones que informar.

## Tres Capas

Un Objeto BIM tiene tres capas. Las tres son datos integrados en el objeto. Ni Regulación ni Zona Climática son opciones seleccionables por el usuario en tiempo de ejecución — son datos de referencia mostrados como tablas de consulta estáticas, exactamente como una hoja de datos de estándar técnico muestra múltiples filas de jurisdicción simultáneamente.

**Capa 1 — Especificación.** La clase de entidad IFC (por ejemplo, `IfcWall`), referencia de clasificación Uniclass 2015 (por ejemplo, `Ss_20_05_30_75`), URI de concepto bSDD, descripción en lenguaje llano y plantillas de conjuntos de propiedades aplicables. Esta capa es la identidad permanente del Objeto BIM.

**Capa 2 — Regulación.** Una tabla de superposiciones jurisdiccionales registradas. Cada fila es una superposición: jurisdicción, estándar, tipo de restricción, valor requerido, autoridad fuente y ruta de archivo IDS 1.0. Cuando una superposición incluye un fragmento de exclusión geométrica IFC, ese fragmento tiene precedencia incondicional sobre cualquier restricción numérica.

**Capa 3 — Zona Climática.** Una tabla de requisitos de desempeño de zona climática registrados. Cada fila es una zona registrada: identificador de zona (alineado con ASHRAE 90.1 o equivalente nacional), parámetro de desempeño, valor requerido, unidad y estándar fuente. Cuando una fila de zona climática entra en conflicto con una fila de Regulación para el mismo parámetro, se aplica el valor más restrictivo.

**Regla de composición:** `effective_value = max(regulation_requirement, climate_zone_requirement)` donde ambos expresan límites inferiores. Los fragmentos de exclusión geométrica anulan las restricciones numéricas incondicionalmente.

## Forma de Implementación

Los Objetos BIM se almacenan como JSON en formato W3C Design Token Community Group (DTCG), extendido con tipos de objeto específicos para BIM. El campo `$type` se extiende más allá del conjunto central DTCG para incluir `bim-element`, `bim-material`, `bim-assembly` y tipos específicos de AEC relacionados. El mecanismo de alias DTCG estándar (`{token.reference}`) se preserva, permitiendo que los Objetos BIM se referencien entre sí composicionalmente.

El formato legible por máquinas permite:
- Integración de herramientas: cualquier herramienta de autoría BIM con un analizador DTCG puede consumir Objetos BIM sin desarrollo de complementos propietarios.
- Control de versiones regulatorias: las superposiciones jurisdiccionales tienen versiones independientes de la capa de especificación.
- Operación sin conexión: una bóveda completa de Objetos BIM es un directorio de archivos JSON, clonable via git y consultable sin acceso a la red.

## Relación con el Sistema de Diseño

El sistema de Objetos BIM es paralelo a la estructura de un sistema de diseño de software. Donde IBM Carbon o un sistema similar proporciona una capa primitiva de tokens, una capa de recetas de componentes y una capa de extensiones específicas por superficie, la plataforma de Objetos BIM proporciona una capa primitiva de objetos (las 8 categorías de objetos DTCG ancladas a IFC 4.3), una capa de componentes AEC universal y extensiones específicas por superficie por tipo de programa del entorno construido.

La analogía es estructural, no metafórica. Ambos sistemas abordan el mismo problema: aplicar coherencia entre superficies de autoría independientes codificando decisiones como unidades reutilizables, reasignables y versionables con especificaciones de restricciones legibles por máquinas.

## Véase también

- [[bim-objects-three-layers]] — cómo se estructuran las tres capas de composición (Especificación, Regulación, Zona Climática)
- [[bim-objects-substrate]] — las ocho categorías de Objetos BIM primitivos y sus anclas de entidades IFC
- [[building-design-system-bim]] — el Sistema de Diseño de la Construcción para el entorno construido
- [[flat-file-bim-leapfrog]] — el sustrato de archivo plano que hace posible la composición pre-restringida
