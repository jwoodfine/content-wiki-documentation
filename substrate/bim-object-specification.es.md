---
schema: foundry-doc-v1
title: "Especificación de Objeto BIM"
slug: bim-object-specification
language: es
category: substrate
index_group: core-named-substrates
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-26
editor: pointsav-engineering
short_description: "La unidad de especificación reutilizable de elementos de construcción de la plataforma: un conjunto fijo de categorías primitivas ancladas a estándares abiertos (IFC, Uniclass, bSDD), cada una portando tres capas de información a la vez — qué es, qué exige su jurisdicción, y qué exige su clima."
cites: [ifc-4-3, uniclass-2015, bsdd-v1]
paired_with: bim-object-specification.md
---

El Modelado de Información de la Construcción (BIM) produce representaciones digitales detalladas de una estructura, pero un modelo BIM estándar no impide por sí mismo las infracciones de código — un modelo puede estar geométricamente completo y aun así incumplir los requisitos de una jurisdicción, descubierto solo cuando se ejecuta una verificación de cumplimiento después del hecho. Un **Objeto BIM** es el término de la plataforma para una especificación de elemento de construcción diseñada para portar sus requisitos de código y desempeño aplicables desde el momento en que se coloca, de modo que una infracción se detecta en el propio diseño en lugar de en una inspección posterior.

**Por qué importa:** el sustrato existe para hacer estructuralmente imposible colocar cierta clase de defecto, no solo para hacerla más fácil de detectar — la diferencia entre una unidad de especificación y una lista de verificación.

## Qué distingue a un Objeto BIM

Un Objeto BIM difiere de los bloques de construcción con los que podría confundirse. No es un tipo de entidad IFC en bruto (que define una forma de datos pero no porta requisitos específicos de jurisdicción). No es un formato de autoría de modelos propietario y atado a un proveedor. No son datos de gestión de instalaciones capturados después del hecho, una vez completado un modelo. Combina tres cosas a la vez: qué es el elemento, qué requisitos regulatorios debe satisfacer en su jurisdicción, y qué requisitos de desempeño debe cumplir para su zona climática — agrupados en una sola unidad de especificación reutilizable en lugar de verificarse por separado después del diseño.

## Categorías primitivas — el sustrato

Todo Objeto BIM pertenece a uno de un conjunto pequeño y fijo de categorías primitivas — elementos espaciales como sitios y plantas, elementos físicos como muros y puertas, materiales, ensamblajes, sistemas de construcción, umbrales de desempeño, requisitos de zona climática, y códigos de identidad. Agrupar los objetos de esta manera significa que una categoría le indica a un profesional qué tipo de cosa describe un objeto antes de abrir su especificación completa.

Cada categoría se ancla a los mismos estándares abiertos ya usados en toda la industria AEC: la jerarquía de entidades IFC para qué es un elemento, Uniclass 2015 para cómo se clasifica, y el Diccionario de Datos de buildingSMART (bSDD) para una definición estable e independiente de herramienta.

**Por qué importa:** anclarse a estándares abiertos en lugar de a un esquema propietario significa que el significado de un objeto no depende de que ninguna herramienta de autoría BIM en particular siga en el negocio — la especificación permanece legible y verificable durante el tiempo que el edificio permanezca en pie, y sin importar cuántos proveedores de software vengan y se vayan durante su vida.

## Tres capas de composición

Un Objeto BIM porta tres capas de información a la vez: Especificación, Regulación y Zona Climática. Ninguna de las tres es una elección que un diseñador haga en el momento del diseño. Un elemento de construcción tiene un tipo fijo, se ubica en una jurisdicción fija, y se desempeña en un clima fijo, de modo que el objeto refleja las tres como hechos sobre su contexto físico y no como preferencias del usuario.

| Capa | Qué porta |
|---|---|
| Especificación | La identidad permanente del objeto — qué tipo de elemento es, independientemente de dónde se construya |
| Regulación | Los requisitos legales específicos de la jurisdicción que aplican donde realmente se ubica el edificio |
| Zona Climática | Los requisitos de desempeño que se derivan del clima físico del edificio, tomados del código energético aplicable |

Regulación y Zona Climática se elaboran cada una como una tabla creciente de todo requisito registrado, en lugar de un solo valor, porque una jurisdicción o una zona climática es un hecho sobre el sitio, no un ajuste que elige un usuario. Los requisitos regulatorios varían por jurisdicción y cambian a medida que se actualizan los códigos; los requisitos de desempeño climático varían por zona y cambian a medida que se revisan los códigos energéticos. Mantener estas capas separadas, en lugar de plegarlas en un solo número, significa que cada aspecto puede rastrearse, sustentarse y actualizarse de forma independiente sin alterar los otros dos.

**Por qué importa — la regla de composición:** cuando un requisito regulatorio y un requisito de zona climática restringen a la vez la misma propiedad, prevalece el más estricto de los dos. Ambas capas expresan mínimos de desempeño, de modo que el requisito vinculante es siempre el que tenga el mínimo más alto — una regla directa de "prevalece lo más restrictivo", no una negociación.

## Dónde vive la especificación

El esquema completo a nivel de campo, la estructura de superposición por jurisdicción, el formato de entrega y el estado actual de implementación detrás de este sustrato se mantienen directamente en [bim.woodfinegroup.com](https://bim.woodfinegroup.com).

## Véase también

- [[building-design-system]] — la capa de coordinación de la que este sustrato es una de dos capas
- [[aec-interface-conventions]] — el vocabulario de interfaz compartido a través del cual una superficie con capacidad BIM expone este sustrato
- [[asset-anchored-bim-vault]] — el archivo que almacena cada Objeto BIM como un objeto direccionado por hash
- [[flat-file-bim-leapfrog]] — las restricciones arquitectónicas sobre las que se construye todo el sustrato BIM
