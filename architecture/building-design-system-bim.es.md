---
schema: foundry-doc-v1
title: "El sistema de diseño de la construcción"
slug: building-design-system-bim
short_description: "Una plataforma de sistema de diseño para el entorno construido organizada en ocho categorías primitivas de BIM Objects y diez componentes universales de interfaz AEC, proporcionando vocabulario de especificación compartido para que superficies de autoría independientes se coordinen sin introducir nuevas superficies de aprendizaje."
language: es
category: architecture
type: topic
content_type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-17
editor: pointsav-engineering
cites: [ifc-4-3, uniclass-2015, bsdd-v1, ids-1-0, dtcg-w3c]
paired_with: building-design-system-bim.md
---

Los grandes [[design-system-substrate|sistemas de diseño]] de software resuelven un problema de coordinación a escala: cuando equipos independientes crean superficies de interfaz de forma paralela, la consistencia se rompe a menos que las decisiones de diseño estén codificadas en una capa compartida de tokens, recetas de componentes y patrones de interacción que todas las superficies deben consumir. No existe un sistema equivalente para el entorno construido. La producción BIM se coordina a través de normas compartidas (IFC, Uniclass, bSDD) y herramientas de autoría compartidas, pero no existe una capa de Objetos BIM común — ninguna biblioteca canónica y legible por máquina de especificaciones de elementos del entorno construido que las superficies de autoría consuman por referencia. Una investigación encargada en abril de 2026 analizó el estado del arte disponible y encontró ese espacio vacío. El Sistema de Diseño de la Construcción está concebido para llenarlo. Se compone de ocho [[bim-objects-substrate|categorías primitivas de Objetos BIM]] y diez [[aec-interface-conventions|componentes universales de interfaz AEC]].

## Por qué el espacio está vacío

Tres factores estructurales mantuvieron vacío ese espacio.

**Dominio de herramientas de autoría propietarias.** Las herramientas BIM dominantes han almacenado históricamente las especificaciones de elementos en formatos de objetos propietarios. Estos formatos contienen geometría, comportamiento paramétrico y algunos metadatos, pero están bloqueados por formato, no son interoperables entre herramientas y no están diseñados para llevar datos normativos. Sirven como biblioteca de elementos para una sola herramienta, no como capa de especificación compartida entre herramientas.

**IFC como formato de intercambio, no de especificación.** IFC 4.3 (ISO 16739-1:2024) es un formato de intercambio neutro — expresa lo que contiene un modelo, no lo que requiere una especificación de token. El mecanismo de conjuntos de propiedades IFC proporciona plantillas para valores de propiedad pero no lleva lógica de aplicación, jerarquía de restricciones ni mapeo jurisdiccional.

**Fragmentación de normas.** La pila de normas del entorno construido — IFC, Uniclass, Omniclass, MasterFormat, CoClass, NBS, bSDD — evolucionó en paralelo entre jurisdicciones. Ninguna proporciona una capa de especificación composable análoga al DTCG.

El Sistema de Diseño de la Construcción usa cada una de estas normas en su función adecuada: IFC como jerarquía de tipos de entidad, Uniclass 2015 como base de clasificación, bSDD como identidad semántica e IDS 1.0 como expresión de restricciones. DTCG proporciona el formato contenedor y el mecanismo de alias.

## Las ocho categorías de Objetos BIM primitivos

La capa de Objetos BIM está organizada en ocho categorías de primitivos, cada una correspondiente a un grupo de tipos de entidades IFC 4.3:

1. **Espacial** — jerarquía `IfcSpatialElement`: sitio, edificio, planta, espacio, zona.
2. **Elementos** — jerarquía `IfcBuiltElement`: muros, losas, vigas, columnas, puertas, ventanas, escaleras, rampas. Los Objetos BIM de elementos llevan la especificación completa de tres capas porque son los objetos primarios de restricción normativa.
3. **Sistemas** — jerarquía `IfcDistributionElement`: mecánico, eléctrico, fontanería, protección contra incendios, HVAC.
4. **Materiales** — especificaciones `IfcMaterial` e `IfcMaterialLayer`, incluyendo conductividad térmica, grado estructural y clasificación de reacción al fuego.
5. **Conjuntos** — composiciones `IfcElementAssembly`: un Objeto BIM de conjunto de muro cortina referencia sus Objetos BIM de componentes mediante el mecanismo de alias DTCG.
6. **Rendimiento** — plantillas `IfcPropertySet` para especificaciones de rendimiento transversales: puentes térmicos, permeabilidad al aire, índices de aislamiento acústico.
7. **Identidad y Códigos** — tablas de mapeo entre identificadores de Objetos BIM y sistemas de clasificación externos: Uniclass 2015, Omniclass Tabla 23, referencias de sección NBS, Masterformat 2018.
8. **Zonas climáticas** — tablas de parámetros de rendimiento por identificador de zona climática (ASHRAE 90.1, NBC canadiense, EN ISO 52000).

## El modelo de bóveda soberana

El Sistema de Diseño de la Construcción no es un servicio alojado externamente. Es un conjunto de archivos JSON en un repositorio git — la [[asset-anchored-bim-vault|bóveda de Objetos BIM]]. Las organizaciones que operan la plataforma clonan el repositorio de la bóveda, lo extienden con sus propias superposiciones normativas y datos de zona climática, y configuran su instancia local de `app-orchestration-bim` para leer desde su copia local.

La capa de proveedor (`pointsav-design-system`) mantiene los Objetos BIM primitivos universales, las recetas de componentes y los archivos de investigación. Las bóvedas de capa de cliente extienden la capa del proveedor con adiciones jurisdiccionales y específicas de programa. Las instancias de despliegue leen desde la bóveda del cliente. Ningún dato fluye hacia arriba: [[five-stage-supply-chain|proveedor → cliente → despliegue]] únicamente.

## Véase también

- [[bim-objects-what-they-are]]
- [[bim-objects-three-layers]]
- [[bim-objects-substrate]]
- [[flat-file-bim-leapfrog]]
