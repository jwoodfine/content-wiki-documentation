---
schema: foundry-doc-v1
title: "Convenciones de interfaz AEC"
slug: aec-interface-conventions
language: es
category: patterns
index_group: interface-and-user-experience
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-26
editor: pointsav-engineering
short_description: "Las herramientas de autoría BIM de toda la industria comparten un vocabulario de interfaz común — una jerarquía espacial, un panel de propiedades de elementos, una vista 3D y vistas guardadas — porque se construyen sobre el mismo modelo de datos IFC subyacente. La capa de interfaz planificada del Sistema de Diseño de la Construcción reutiliza ese vocabulario en lugar de inventar uno nuevo, y está pensada para extenderlo a los flujos de trabajo de gestión de instalaciones."
cites: [ifc-4-3]
paired_with: aec-interface-conventions.md
---

Toda plataforma de autoría BIM importante viene con las mismas cuatro convenciones de interfaz: un árbol de jerarquía para la estructura espacial, un panel de propiedades para los atributos de los elementos, una vista 3D y un navegador de vistas guardadas. Estas convenciones existen porque el modelo de datos subyacente — la jerarquía de entidades IFC — es el mismo sin importar qué herramienta lo autora. Un arquitecto o ingeniero que ha aprendido este vocabulario en una herramienta de autoría ya lo conoce en la siguiente.

**Por qué importa:** un profesional nunca tiene que volver a aprender cómo navegar un modelo solo porque cambió el software — el vocabulario es una propiedad del estándar, no de la interfaz de un proveedor particular.

## Por qué importa un vocabulario compartido

Los equipos de proyectos BIM trabajan habitualmente con varias herramientas de autoría en un mismo proyecto. El modelo del ingeniero estructural, el del arquitecto y el del ingeniero de MEP exportan cada uno al mismo formato abierto, y la coordinación ocurre en un visor común donde nadie trabaja en su entorno nativo de autoría. Una superficie de coordinación construida sobre este vocabulario compartido no introduce una curva de aprendizaje nueva encima de las herramientas que los profesionales ya usan.

## La capa de interfaz planificada del Sistema de Diseño de la Construcción

[[building-design-system|El Sistema de Diseño de la Construcción]] está planificado para construir sus propios componentes de interfaz sobre este mismo vocabulario compartido, de modo que un profesional que se mueve entre su herramienta de autoría y cualquier superficie BIM construida sobre la plataforma encuentre el mismo árbol, el mismo panel de propiedades y los mismos controles de vista. Esta capa aún no existe en código canónico.

**Por qué importa — curva de aprendizaje cero por diseño, no por accidente:** adoptar patrones de interfaz ya familiares de las herramientas de autoría AEC estándar de la industria significa que un profesional llega con una curva de aprendizaje cero en lugar de necesitar aprender las convenciones de una herramienta nueva antes de hacer trabajo real. Reflejar el vocabulario existente está pensado para que la atención se dirija a los verdaderos diferenciadores de la plataforma — el archivo de archivos planos descrito en [[asset-anchored-bim-vault]] — en lugar de a la navegación básica de la herramienta.

## Extensión hacia la gestión de instalaciones

Las herramientas BIM existentes se construyen principalmente para diseñadores, y la mayor parte del valor de un modelo se pierde una vez que llega a un gestor de instalaciones que nunca formó parte de su flujo de autoría. Esta capa de interfaz está pensada para extender el mismo vocabulario familiar al flujo de trabajo de gestión de instalaciones: vinculando el estado de mantenimiento a los elementos del edificio, conectando espacios con los registros de arrendamiento, y superponiendo datos de sensores en vivo sobre el modelo. La intención es convertir un modelo BIM de un artefacto de diseño-y-entrega en un registro operativo que un gestor de instalaciones realmente usa día a día, en lugar de un segundo sistema desconectado que hay que conciliar manualmente contra él.

## Dónde vive la especificación

El catálogo completo de componentes y el detalle de implementación detrás de esta capa de interfaz se mantienen directamente en [bim.woodfinegroup.com](https://bim.woodfinegroup.com).

## Véase también

- [[building-design-system]] — el Sistema de Diseño de la Construcción más amplio del que esta capa de interfaz forma parte
- [[bim-object-specification]] — el modelo de objetos subyacente que esta interfaz expone
- [[asset-anchored-bim-vault]] — la estructura de archivo de la que lee la extensión de gestión de instalaciones
