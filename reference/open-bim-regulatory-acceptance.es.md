---
schema: foundry-doc-v1
title: "Open BIM y Aceptación Regulatoria"
slug: open-bim-regulatory-acceptance
language: es
category: reference
type: topic
quality: core
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-06
editor: pointsav-engineering
cites: [eupl-1-2]
paired_with: open-bim-regulatory-acceptance.md
---

El modelado de información de construcción (BIM) ya no es opcional en la contratación pública de la mayoría de las economías del G7. El gobierno federal de Estados Unidos exige entregas BIM en formato IFC para grandes proyectos de infraestructura y construcción desde 2007. La Unión Europea ha incorporado requisitos BIM en las directivas de contratación pública aplicadas en todos los estados miembros. El Reino Unido, Singapur, Noruega, Dinamarca, los Países Bajos y Australia han emitido mandatos nacionales o requisitos de política equivalentes. El panorama regulatorio del Open BIM está establecido. La pregunta abierta es qué plataformas pueden cumplir los requisitos de soberanía de datos asociados a estos mandatos.

## Qué es el Open BIM

El Open BIM, tal como lo define buildingSMART International, denota un enfoque de flujo de trabajo e intercambio de datos donde los datos del modelo se almacenan e intercambian en formatos abiertos neutros al proveedor (principalmente IFC, ISO 16739-1:2024), las clasificaciones y definiciones de propiedades referencian diccionarios abiertos (principalmente bSDD), las especificaciones de restricciones se expresan en lenguajes abiertos de restricción (principalmente IDS 1.0) y los datos de entrega se formatean según normas abiertas de gestión de instalaciones (principalmente COBie).

## Mandatos en Europa y América Latina

**España.** El Plan de Impulso de la Contratación Pública de Edificación BIM (PPRE 2022–2026) establece un mandato progresivo de BIM para contratos públicos de construcción, con objetivo de implementación completa en todas las obras públicas para 2026. IFC es el formato de intercambio especificado.

**Alemania.** El BMDV emitió una hoja de ruta BIM que exige el Open BIM en proyectos de infraestructura de transporte federal: objetivo de fase de diseño en 2020 y ciclo de vida completo en 2025.

**Italia.** El Decreto Legislativo 36/2023 exige BIM para contratos de obras públicas superiores a 15 millones de euros desde enero de 2023, con extensión a umbrales más bajos a lo largo de 2025.

**Reino Unido.** El mandato BIM de Nivel 2 para proyectos del sector público contratados centralmente lleva en vigor desde 2016. La BS EN ISO 19650 se adoptó como norma nacional del Reino Unido en 2019.

**Chile.** La Estrategia Nacional BIM 2023–2025 establece la adopción progresiva de BIM en obras públicas, posicionando a Chile como referencia regional.

**México, Colombia y Argentina** cuentan con iniciativas gubernamentales BIM en distintas fases de desarrollo, con mandatos de proyecto piloto en infraestructura pública.

## Soberanía de datos como requisito de contratación

Varios contextos de contratación pública imponen requisitos de soberanía de datos que efectivamente exigen plataformas BIM autoalojadas y con capacidad de operar sin conexión.

**GDPR.** Los datos de ocupación de edificios y los registros de gestión de instalaciones asociados a los gemelos digitales BIM pueden contener datos personales. El artículo 44 del GDPR prohíbe la transferencia de datos personales a jurisdicciones sin protección adecuada. Una plataforma BIM autoalojada que procesa datos dentro de la jurisdicción de la UE elimina la cuestión de la transferencia.

**Soberanía jurisdiccional.** Los datos regulatorios jurisdiccionales son derecho público. Publicarlos en un estándar JSON neutro y abierto (DTCG del W3C con extensiones BIM) y distribuirlos mediante repositorios git públicos es análogo a publicar códigos de construcción en PDF — neutro, reproducible e independiente de proveedores.

**Operación sin conexión.** Las obras frecuentemente operan sin conectividad de red fiable. Una bóveda de BIM Tokens clonada mediante git y almacenada localmente está disponible sin conexión de forma incondicional.

## ISO 19650 y el Entorno de Datos Común

ISO 19650 (Gestión de información usando BIM) define los requisitos para los procesos de gestión de información a lo largo del ciclo de vida del proyecto y para el Entorno de Datos Común (CDE). ISO 19650 Partes 1 y 2 son tecnológicamente neutras: un repositorio git satisface los requisitos del CDE de la ISO 19650 — contenedores de información, flujo de trabajo de emisión y recepción, registro de auditoría con control de revisiones y gestión de estados.

Esto significa que un proyecto BIM gestionado a través de una bóveda de tokens alojada en git opera dentro de un CDE conforme con ISO 19650, sin requerir una plataforma CDE creada específicamente para ese propósito. Esta es una ventaja de coste estructural para las pequeñas y medianas empresas del sector AEC.

## Licencia EUPL-1.2 y ventaja en licitaciones

La plataforma BIM de PointSav se publica bajo la Licencia Pública de la Unión Europea versión 1.2 (EUPL-1.2). Esta licencia está aprobada por la OSI (Open Source Initiative) y fue creada por la Comisión Europea para software producido por o para organismos públicos de la UE. Las autoridades contratantes de los estados miembros de la UE tienen una preferencia de política por el software con licencia EUPL-1.2 en la contratación pública.

## Véase también

- [[flat-file-bim-leapfrog]]
- [[city-code-as-composable-geometry]]
- [[bim-token-what-it-is]]
- [[bcsc-disclosure-posture]]
- [[leapfrog-2030-architecture]]

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™ y Totebox Archive™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos titulares.*
