---
schema: foundry-doc-v1
title: "El Sistema de Diseño de la Construcción"
slug: building-design-system-bim
language: es
category: architecture
type: topic
quality: core
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-06
editor: pointsav-engineering
cites: []
paired_with: building-design-system-bim.md
---

Los grandes sistemas de diseño de software resuelven un problema de coordinación a escala: cuando equipos independientes crean superficies de interfaz de forma paralela, la consistencia se rompe a menos que las decisiones de diseño estén codificadas en una capa compartida de tokens, recetas de componentes y patrones de interacción que todas las superficies deben consumir. No existe un sistema equivalente para el entorno construido. La producción BIM se coordina a través de normas compartidas (IFC, Uniclass, bSDD) y herramientas de autoría compartidas, pero no existe una capa de tokens común — ninguna biblioteca canónica y legible por máquina de especificaciones de elementos del entorno construido que las superficies de autoría consuman por referencia. Una investigación encargada en abril de 2026 analizó el estado del arte disponible y encontró ese espacio vacío. El Sistema de Diseño de la Construcción está concebido para llenarlo.

## Por qué el espacio está vacío

Tres factores estructurales mantuvieron vacío ese espacio.

**Dominio de herramientas de autoría propietarias.** Las herramientas BIM dominantes han almacenado históricamente las especificaciones de elementos en formatos de objetos propietarios. Estos formatos contienen geometría, comportamiento paramétrico y algunos metadatos, pero están bloqueados por formato, no son interoperables entre herramientas y no están diseñados para llevar datos normativos. Sirven como biblioteca de elementos para una sola herramienta, no como capa de especificación compartida entre herramientas.

**IFC como formato de intercambio, no de especificación.** IFC 4.3 (ISO 16739-1:2024) es un formato de intercambio neutro — expresa lo que contiene un modelo, no lo que requiere una especificación de token. El mecanismo de conjuntos de propiedades IFC proporciona plantillas para valores de propiedad pero no lleva lógica de aplicación, jerarquía de restricciones ni mapeo jurisdiccional.

**Fragmentación de normas.** La pila de normas del entorno construido — IFC, Uniclass, Omniclass, MasterFormat, CoClass, NBS, bSDD — evolucionó en paralelo entre jurisdicciones. Ninguna proporciona una capa de especificación composable análoga al DTCG.

El Sistema de Diseño de la Construcción usa cada una de estas normas en su función adecuada: IFC como jerarquía de tipos de entidad, Uniclass 2015 como base de clasificación, bSDD como identidad semántica e IDS 1.0 como expresión de restricciones. DTCG proporciona el formato contenedor y el mecanismo de alias.

## Las ocho categorías de primitivos de tokens

La capa de tokens está organizada en ocho categorías de primitivos, cada una correspondiente a un grupo de tipos de entidades IFC 4.3:

1. **Espacial** — jerarquía `IfcSpatialElement`: sitio, edificio, planta, espacio, zona.
2. **Elementos** — jerarquía `IfcBuiltElement`: muros, losas, vigas, columnas, puertas, ventanas, escaleras, rampas. Los tokens de elementos llevan la especificación completa de tres capas porque son los objetos primarios de restricción normativa.
3. **Sistemas** — jerarquía `IfcDistributionElement`: mecánico, eléctrico, fontanería, protección contra incendios, HVAC.
4. **Materiales** — especificaciones `IfcMaterial` e `IfcMaterialLayer`, incluyendo conductividad térmica, grado estructural y clasificación de reacción al fuego.
5. **Conjuntos** — composiciones `IfcElementAssembly`: un token de conjunto de muro cortina referencia sus tokens de componentes mediante el mecanismo de alias DTCG.
6. **Rendimiento** — plantillas `IfcPropertySet` para especificaciones de rendimiento transversales: puentes térmicos, permeabilidad al aire, índices de aislamiento acústico.
7. **Identidad y Códigos** — tablas de mapeo entre identificadores de BIM Tokens y sistemas de clasificación externos: Uniclass 2015, Omniclass Tabla 23, referencias de sección NBS, Masterformat 2018.
8. **Zonas climáticas** — tablas de parámetros de rendimiento por identificador de zona climática (ASHRAE 90.1, NBC canadiense, EN ISO 52000).

## El modelo de bóveda soberana

El Sistema de Diseño de la Construcción no es un servicio alojado externamente. Es un conjunto de archivos JSON en un repositorio git — la bóveda de tokens BIM. Las organizaciones que operan la plataforma clonan el repositorio de la bóveda, lo extienden con sus propias superposiciones normativas y datos de zona climática, y configuran su instancia local de `app-orchestration-bim` para leer desde su copia local.

La capa de proveedor (`pointsav-design-system`) mantiene los primitivos de tokens universales, las recetas de componentes y los archivos de investigación. Las bóvedas de capa de cliente extienden la capa del proveedor con adiciones jurisdiccionales y específicas de programa. Las instancias de despliegue leen desde la bóveda del cliente. Ningún dato fluye hacia arriba: proveedor → cliente → despliegue únicamente.

## Véase también

- [[bim-token-what-it-is]]
- [[bim-token-three-layers]]
- [[design-system-substrate]]
- [[flat-file-bim-leapfrog]]
- [[bim-token-taxonomy]]

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™ y Totebox Archive™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos titulares.*
