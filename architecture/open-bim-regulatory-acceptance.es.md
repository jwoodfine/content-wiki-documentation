---
schema: foundry-doc-v1
title: "BIM abierto y aceptación regulatoria"
slug: open-bim-regulatory-acceptance
short_description: "El modelado de información de construcción es obligatorio en la mayoría de las economías del G7 para contratación pública, con estándares abiertos — IFC 4.3, IDS 1.0, COBie — como requisito de entrega en lugar de formatos propietarios. Las plataformas BIM sin conexión y autohospedadas son el único tipo de arquitectura que satisface de forma nativa los requisitos de datos soberanos impuestos por ITAR, GDPR, HIPAA y marcos regulatorios equivalentes."
language: es
category: architecture
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-17
editor: pointsav-engineering
cites: [ifc-4-3, iso-19650, ids-1-0]
paired_with: open-bim-regulatory-acceptance.md
---

El Modelado de Información para la Construcción ya no es opcional en la contratación pública para la mayoría de las economías del G7. El gobierno federal de los Estados Unidos ha requerido entregables BIM en formato IFC para proyectos importantes de infraestructura y edificación desde 2007. La Unión Europea ha incorporado requisitos BIM en las directivas de contratación pública aplicadas en los estados miembros. El Reino Unido, Singapur, Noruega, Dinamarca, los Países Bajos y Australia han emitido mandatos nacionales o requisitos de política equivalentes. El panorama regulatorio para el BIM Abierto está definido. La pregunta abierta es qué plataformas pueden cumplir los requisitos de soberanía de datos adjuntos a estos mandatos. Véase [[flat-file-bim-leapfrog|el salto del BIM de archivo plano]] y [[asset-anchored-bim-vault|la bóveda BIM anclada al activo]].

## Definición de BIM Abierto

El BIM Abierto, según la definición de buildingSMART International, denota un enfoque de flujo de trabajo e intercambio de datos donde:

1. Los datos del modelo se almacenan e intercambian en formatos abiertos neutros respecto al proveedor, principalmente IFC (ISO 16739-1:2024).
2. Las definiciones de clasificación y propiedad referencian diccionarios abiertos, principalmente bSDD.
3. Las especificaciones de restricciones se expresan en lenguajes de restricción abiertos, principalmente IDS 1.0.
4. Los datos de entrega se formatean según estándares abiertos de gestión de instalaciones, principalmente COBie.

## Mandatos Federales de los Estados Unidos

**Administración de Servicios Generales (GSA).** El Programa Nacional de BIM 3D-4D de la GSA requiere datos espaciales y de programa en formato IFC para proyectos por encima de umbrales definidos. Se requieren entregables COBie para la transferencia.

**Cuerpo de Ingenieros del Ejército de los EE. UU. (USACE).** El Plan de Acción BIM del USACE exige BIM para proyectos de construcción militar (MILCON) y obras civiles por encima de 5 millones de dólares.

**Departamento de Asuntos de Veteranos (VA) y Comando de Ingeniería de Instalaciones Navales (NAVFAC).** Ambas agencias han publicado normas BIM que requieren exportaciones IFC en hitos de diseño.

## Unión Europea

La Directiva de Contratación Pública de la UE de 2014 (Directiva 2014/24/UE) permite explícitamente a los estados miembros requerir herramientas BIM electrónicas para contratos de construcción financiados con fondos públicos.

**Alemania.** El Ministerio Federal de Asuntos Digitales y Transporte (BMDV) emitió una hoja de ruta BIM con objetivos para la infraestructura federal de transporte establecidos para 2020 (fase de diseño) y 2025 (ciclo de vida completo).

**Italia.** El Decreto Legislativo 36/2023 (el nuevo Código de Contratos Públicos) exige BIM para contratos de obras públicas superiores a 15 millones de euros desde enero de 2023.

**España.** El Plan de Impulso de la Contratación Pública de Edificación BIM (PPRE 2022-2026) establece un mandato progresivo que apunta a la implementación completa en todas las obras públicas para 2026.

**Dinamarca.** Dinamarca ha requerido BIM en proyectos de edificación financiados por el Estado por encima de DKK 5 millones desde 2013.

**Noruega.** Statsbygg ha requerido entregables de BIM Abierto desde 2016. El Manual BIM de Statsbygg especifica IFC 4.x y requisitos de LOD por fase de proyecto.

**Reino Unido.** El mandato de BIM Nivel 2 del Gobierno del Reino Unido para proyectos del sector público contratados centralmente ha estado vigente desde 2016. BS EN ISO 19650 fue adoptada como norma nacional del Reino Unido en 2019.

## Arquitectura Soberana de Datos como Requisito de Contratación

**ITAR (Reglamento sobre el Tráfico Internacional de Armas).** Los proyectos de construcción de defensa que involucran datos sensibles de instalaciones están sujetos a ITAR y EAR. Una plataforma de primer uso sin conexión, autohospedada, que nunca transmite datos del modelo fuera de la red de la instalación, es la única arquitectura que satisface los requisitos ITAR sin autorización de nube comercial.

**RGPD (Reglamento General de Protección de Datos).** Los datos de ocupación de edificios, datos de sensores y registros de gestión de instalaciones asociados con gemelos digitales BIM pueden contener datos personales. Una plataforma BIM autohospedada que procesa datos dentro de la jurisdicción de la UE elimina la pregunta de transferencia.

**HIPAA.** La construcción de instalaciones sanitarias genera datos BIM asociados con el flujo de pacientes y la programación del espacio clínico. Una plataforma autohospedada con controles de acceso alineados con la postura de seguridad de la instalación satisface estos requisitos.

## ISO 19650 y el Entorno de Datos Común

Un repositorio git satisface los requisitos del EDC de ISO 19650:

| Concepto ISO 19650 | Implementación Git |
|---|---|
| Contenedor de información | Archivo IFC o sidecar YAML |
| UID del contenedor | Hash de objeto Git o GUID IFC |
| Estado | Nombre de rama (`work-in-progress`, `shared`, `published`) |
| Revisión | Hash de confirmación Git |
| Historial de cambios | `git log --follow <filename>` |

## Licencia Apache 2.0 y Ventaja en Contratación

Los archivos de datos de Objetos BIM se publican bajo Apache 2.0, aprobado por la OSI, compatible con la contratación pública (FAR 12.212) y con uso comercial derivado sin requisitos de copyleft.
