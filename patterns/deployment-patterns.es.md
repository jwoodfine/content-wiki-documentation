---
schema: foundry-doc-v1
title: "deployment-patterns"
slug: deployment-patterns
category: patterns
type: concept
quality: complete
short_description: "Los patrones de despliegue describen las seis configuraciones canónicas en las que se despliega el sustrato PointSav — cada una basada en los mismos cinco primitivos y la misma superficie de SO, con el Plan de Cuentas y la superficie de cumplimiento adaptados por segmento."
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: deployment-patterns.md
references:
  - id: 1
    text: "Jackson, Cam. 'Micro Frontends.' martinfowler.com, 2019. El artículo técnico fundacional que describe el patrón arquitectónico de micro-frontends aplicado en la ingeniería web moderna."
    url: "https://martinfowler.com/articles/micro-frontends.html"
  - id: 2
    text: "The Open Group, Estándar TOGAF, 10.ª edición, 2022. Capítulo 20: Patrones de Arquitectura. Tratamiento canónico de configuraciones de despliegue reutilizables en arquitectura empresarial."
    url: "https://www.opengroup.org/togaf"
---

Los patrones de despliegue describen las seis configuraciones canónicas en las que se despliega el sustrato PointSav en diferentes contextos institucionales. Cada configuración se basa en los mismos cinco primitivos — Personas, Comunicaciones, Borradores, Registros, Dinero — y la misma superficie de [[console-os|Libro Mayor de Comandos]]; lo que cambia por configuración es el [[archetypes-and-chart-of-accounts|Plan de Cuentas]] y la superficie de cumplimiento. El sustrato no se bifurca entre segmentos; se adapta. Al finalizar este artículo, el lector comprenderá el posicionamiento de Compañero, las seis configuraciones canónicas y el modelo de aislamiento de micro-frontend que hace práctica la versión independiente en los seis.

## Cinco primitivos que abarcan todos los contextos institucionales [^2]

Cada contexto en el que operan los usuarios institucionales se asigna a las mismas cinco categorías primitivas de registros. Un profesional regulado que gestiona archivos de pacientes, un abogado litigante que gestiona la divulgación de casos y un hogar que gestiona declaraciones de impuestos mantienen documentos que caen exactamente en estas categorías:

| Primitivo | Qué cubre |
|---|---|
| Personas | Contactos, registros de personal, relaciones de identidad |
| Comunicaciones | Correo electrónico, correspondencia, registros de reuniones |
| Borradores | Trabajo en progreso — documentos bajo autoría activa |
| Registros | Documentos firmados, sellados o ejecutados |
| Dinero | Registros financieros, facturas, entradas del libro mayor |

El [[console-os|Libro Mayor de Comandos]] expone cada primitivo como una superficie de tecla F dedicada. El operador presiona una tecla; el chasis carga el plugin relevante; el plugin muestra los registros de ese primitivo dentro del contexto [[totebox-os|Totebox]] actual.

## Cómo la plataforma opera junto a las herramientas incumbentes

La plataforma se posiciona como un motor complementario, no como un reemplazo de las herramientas operativas existentes. Los clientes continúan usando las aplicaciones profesionales y de productividad que ya operan; el sustrato funciona en paralelo, enrutando los registros de esas aplicaciones hacia archivos [[totebox-os|Totebox]] soberanos.

| Categoría de herramienta incumbente | Lo que agrega el sustrato |
|---|---|
| Clientes de correo electrónico profesional | [[service-email\|service-email]] ingiere cada mensaje en un Maildir WORM; la copia en la nube puede rotar mientras la copia soberana permanece sellada |
| Aplicaciones de hojas de cálculo | La superficie de hoja de cálculo soberana prevista almacena modelos financieros ejecutados en el [[worm-ledger-design\|libro mayor WORM]] |
| Aplicaciones de procesamiento de texto | La superficie de procesamiento de texto soberana prevista usa Typst para salida con fidelidad de impresión |
| Plataformas de redes profesionales | Se prevé que [[service-people]] recopile datos de contacto verificados en el libro mayor de identidad del Totebox |
| Repositorios de documentos corporativos | service-minutebook sella criptográficamente los registros firmados contra el sustrato [[worm-ledger-design\|WORM]] |

El cliente no necesita abandonar ninguna herramienta funcional. El sustrato opera en segundo plano; el Libro Mayor de Comandos proporciona una vista soberana sobre los registros que producen las herramientas incumbentes.

## Seis configuraciones de despliegue canónicas

Las seis configuraciones representan familias de GUIDEs distintas en el catálogo de despliegue de flota. Cada una es una configuración, no un producto separado; el [[totebox-os]], el [[console-os|os-console]] y los servicios subyacentes son idénticos en las seis.

| Configuración | Registros principales | Adaptación del [[archetypes-and-chart-of-accounts\|Plan de Cuentas]] |
|---|---|---|
| Gestor de activos inmobiliarios | Documentos de arrendamiento, modelos BIM, comunicaciones con inquilinos, permisos | Anclajes en Bienes Raíces / Arrendamiento / Inquilinos / Municipios |
| Emisor de información pública | Comunicados de prensa, presentaciones regulatorias, actas de la junta | Anclajes en Relaciones con Inversores / Finanzas / Medios |
| Práctica médica o quirúrgica | Registros de pacientes, archivos de diagnóstico, facturación clínica | Anclajes en Cumplimiento y Administración Local |
| Bufete de abogados | Expedientes de casos, materiales de divulgación, escritos judiciales firmados | Ancla en Cumplimiento / Asesoría |
| Family office | Registros fiscales, documentos de sucesión, contratos del hogar | Anclajes adaptados en Personal y Administración Local |
| Hogar | Recibos, garantías, correspondencia familiar | Plan simplificado de un solo Perfil |

## Aislamiento de micro-frontend dentro del Libro Mayor de Comandos [^1]

El [[console-os|Libro Mayor de Comandos]] no es una aplicación HTML monolítica. Es un chasis vacío que carga pequeños plugins aislados bajo demanda. Cuando el operador presiona F2, el chasis solicita la vista `/app-console-people/`; cuando presiona F3, destruye esa vista y carga `/app-console-email/`.

| Propiedad de aislamiento | Efecto |
|---|---|
| Aislamiento matemático en disco | El plugin de Personas no puede leer el estado del plugin de Correo; ocupan árboles de directorio separados |
| Versión independiente | Una actualización del plugin de Contabilidad no requiere una actualización del plugin de Contenido |
| Eficiencia de ancho de banda | Solo el HTML, CSS y JS del plugin activo se carga; el resto permanece en disco |
| Sin dependencia externa | Sin CDN, sin biblioteca de UI de terceros, sin telemetría; los plugins se envían dentro del mismo binario que el chasis |

El modelo de aislamiento se deriva del patrón arquitectónico de micro-frontends[^1] aplicado con disciplina soberana: toda la superficie se envía como un único binario Rust, ningún plugin obtiene activos de un host externo, y ningún plugin puede observar el estado de otro plugin.

## Cómo las plantillas de despliegue se asignan al catálogo de flota

| Plantilla | Función | Estado |
|---|---|---|
| `vault-privategit-source-1` | Despliegue de control de fuentes interno; el espacio de trabajo es una instancia de esta plantilla | Activo |
| Gestión de activos inmobiliarios | El despliegue operativo de referencia para una empresa inmobiliaria | Planeado |
| Emisor de información | Un par de [[mediakit-os]] y [[totebox-os]] para divulgación de empresa pública | Planeado |

Las plantillas en la Capa de Exhibición corresponden a instancias numeradas en la Capa de Instancias — privadas para el operador, ignoradas por git en todos los repositorios públicos. Consulte [[three-layer-architecture]] para el modelo de tres capas.

## La cadencia de despliegue visible-primero

Los patrones de despliegue se lanzan con una cadencia de visible-primero: la URL resuelve y una superficie reconocible responde antes de que comience cualquier trabajo de pulido o endurecimiento. Un patrón que aún no ha sido aprovisionado como un despliegue funcional se describe en términos de planificación, no como infraestructura activa.

## Véase también

- [[three-layer-architecture]] — el modelo de tres capas Software / Exhibición / Instancias
- [[archetypes-and-chart-of-accounts]] — la taxonomía del Plan de Cuentas que se adapta por configuración
- [[console-os\|os-console]] — la superficie del Libro Mayor de Comandos común a las seis configuraciones
- [[totebox-os]] — el sistema operativo Totebox que aloja los archivos de cada configuración
- [[structural-positioning]] — los compromisos estructurales que se aplican uniformemente en las seis configuraciones
