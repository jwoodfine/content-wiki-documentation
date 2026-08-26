---
schema: foundry-doc-v1
title: "Sistema de Diseño de la Construcción"
slug: building-design-system
language: es
category: architecture
index_group: location-intelligence-and-domain
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-26
editor: pointsav-engineering
short_description: "Una capa de coordinación planificada para el entorno construido: una biblioteca canónica y legible por máquina de especificaciones de elementos de construcción que las superficies de autoría BIM independientes consumen por referencia, de la misma manera que un sistema de diseño de software mantiene consistentes a equipos de producto independientes."
cites: [ifc-4-3, uniclass-2015, bsdd-v1]
paired_with: building-design-system.md
---

Los principales sistemas de diseño de software resuelven un problema de coordinación a escala: cuando equipos independientes construyen interfaces en paralelo, la consistencia se rompe a menos que las decisiones de diseño se codifiquen en una capa compartida que cada superficie consume por referencia. No ha existido un equivalente para el entorno construido. La producción de Modelado de Información de la Construcción (BIM) se coordina mediante estándares compartidos (IFC, Uniclass, bSDD) y herramientas de autoría compartidas, pero no ha existido una capa de especificación común — ninguna biblioteca canónica y legible por máquina de especificaciones de elementos de construcción que las superficies de autoría independientes consuman por referencia. El Sistema de Diseño de la Construcción está pensado para llenar ese vacío.

**Por qué importa:** sin esta capa, cada superficie de autoría BIM vuelve a derivar los mismos requisitos de código y desempeño de forma independiente, y dos superficies que trabajan en el mismo edificio pueden desalinearse sin que ninguna esté equivocada en sus propios términos.

## Por qué el espacio ha estado vacío

Tres factores estructurales lo han mantenido vacío. Las herramientas de autoría BIM propietarias han almacenado históricamente las especificaciones de elementos en formatos ligados a una sola herramienta, no diseñados para transportar datos regulatorios normativos entre herramientas. IFC es un formato de intercambio neutral — expresa lo que contiene un modelo, no lo que exige una especificación — por lo que nunca fue diseñado para ser, por sí solo, un sistema de diseño. Y la pila más amplia de estándares del entorno construido evolucionó en paralelo entre jurisdicciones, sin un solo estándar que proporcionara una capa de especificación componible que enlazara a los demás.

**Por qué importa:** cada factor es una razón por la que ningún proveedor por sí solo llenó antes este vacío, no una razón por la que no pueda llenarse — los estándares sobre los que se compondría ya son abiertos y ya están maduros (véase [[flat-file-bim-leapfrog]]).

## De qué está hecho

El Sistema de Diseño de la Construcción se organiza en dos capas: una biblioteca de [[bim-object-specification|categorías primitivas de Objeto BIM]] — las unidades de especificación para elementos espaciales, elementos físicos, materiales, sistemas y más — y un conjunto de [[aec-interface-conventions|componentes de interfaz compartidos]] sobre los que puede construir cualquier superficie con capacidad BIM. Juntos están pensados para dar a las superficies de autoría independientes un vocabulario común en torno al cual coordinarse, sin que un profesional que se mueve entre ellas necesite aprender una interfaz nueva cada vez.

## Un archivo propio, no un servicio alojado

El Sistema de Diseño de la Construcción no está planificado como un servicio alojado — es un conjunto de archivos en un repositorio git que una organización clona y extiende con sus propios datos específicos de jurisdicción y de sitio. Este es el mismo modelo de soberanía que sustenta [[asset-anchored-bim-vault|el archivo BIM de archivos planos]] en un sentido más amplio. No se requiere que nada regrese a un proveedor central para que una organización siga usando su propia copia.

**Por qué importa:** la capa de coordinación es una conveniencia en tiempo de diseño, no una dependencia en tiempo de ejecución — un cliente que deja de pagar soporte conserva cada archivo que hace funcionar su propio archivo BIM.

## Dónde vive la especificación

El catálogo completo de categorías de objetos, la biblioteca de componentes de interfaz y el estado actual de implementación se mantienen directamente en [bim.woodfinegroup.com](https://bim.woodfinegroup.com), el despliegue de referencia cuya arquitectura describe este artículo.

## Véase también

- [[bim-object-specification]] — las categorías primitivas de Objeto BIM y la estructura de composición de tres capas
- [[aec-interface-conventions]] — el vocabulario de interfaz compartido sobre el que este sistema de diseño construye sus propios componentes
- [[asset-anchored-bim-vault]] — la estructura de archivo que este sistema de diseño está pensado para organizar
- [[flat-file-bim-leapfrog]] — las restricciones arquitectónicas sobre las que se construye todo el sustrato BIM
