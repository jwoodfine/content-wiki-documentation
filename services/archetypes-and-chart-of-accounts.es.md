---
schema: foundry-doc-v1
title: "Arquetipos y plan de cuentas"
slug: archetypes-and-chart-of-accounts
category: services
type: concept
content_type: topic
quality: complete
index_group: ring-2-knowledge-and-processing
short_description: "El Plan de Cuentas y los once arquetipos son dos taxonomías de referencia que service-content carga en el grafo de conocimiento, dando a cada entidad clasificada una categoría estructural y una firma funcional."
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: archetypes-and-chart-of-accounts.md
references:
  - id: 1
    text: "Fundación IFRS, NIC 1 — Presentación de Estados Financieros, §54–76: Estado de Situación Financiera — requisitos de clasificación de partidas y subcuentas."
    url: "https://www.ifrs.org/issued-standards/list-of-standards/ias-1-presentation-of-financial-statements/"
  - id: 2
    text: "Organización Internacional del Trabajo, Clasificación Internacional Uniforme de Ocupaciones 2008 (CIUO-08): Marco Conceptual y Metodología. OIT, Ginebra, 2012."
    url: "https://www.ilo.org/public/english/bureau/stat/isco/docs/publication08.pdf"
---

El Plan de Cuentas y los once arquetipos son dos taxonomías de referencia que [[service-content]] mantiene como archivos CSV y carga en el grafo de conocimiento como entidades estáticas. Juntas dan a cada documento o entidad clasificada dos etiquetas independientes: dónde se ubica dentro de una estructura institucional y qué función desempeña. Un lector que solo necesita el vocabulario puede detenerse tras las dos tablas siguientes; quien quiera ver cómo la plataforma las usa realmente debe continuar hasta la sección del Verification Surveyor.

## Dos tablas de referencia, dos dimensiones

| Tabla | Forma real | Qué captura |
|---|---|---|
| Plan de Cuentas | `reference_number`, `category`, `type`, `gravity_keywords` — una lista plana de dos niveles, no una jerarquía profunda | Posición estructural: en qué categoría institucional se ubica (Personal, Compliance, Real Estate, Construction, entre otras) y qué tipo específico dentro de ella |
| Once Arquetipos | `id`, `name`, `signature`, `healing_trigger`, `gravity_keywords` — una fila por arquetipo | Función: qué hace una persona o entidad, independientemente de su título de puesto |

Una muestra real del Plan de Cuentas:

| Referencia | Categoría | Tipo |
|---|---|---|
| 1001 | Personal | Director |
| 2001 | Compliance | Counsel |
| 2002 | Compliance | Accounting |
| 3003 | Real Estate | Office Leasing |

El Plan es plano por diseño: una categoría y un tipo, nada más profundo. No existe una capa separada de "Dominio" o "Subdominio"; el campo de tipo lleva directamente ese nivel de especificidad.

## Los once arquetipos

Cada fila de arquetipo lleva un nombre y una firma breve. También lleva un "disparador de corrección" — el modo de falla contra el que se define el arquetipo:

| Arquetipo | Firma | Disparador de corrección |
|---|---|---|
| The Executive | Strategic Direction | Stagnation |
| The Guardian | Risk & Compliance | Breach |
| The Fiduciary | Resource Integrity | Leakage |
| The Architect | System Design | Complexity |
| The Engineer | Technical Execution | Friction |
| The Artisan | Creative Precision | Homogeneity |
| The Constructor | Physical Realization | Structural Gap |
| The Catalyst | Growth & Momentum | Inertia |
| The Envoy | External Synergy | Friction |
| The Steward | Asset Preservation | Degradation |
| The Sage | Knowledge & Vision | Ignorance |

Ambas tablas también llevan una columna `gravity_keywords` — una lista de términos asociados a la fila, separados por barras (las palabras clave de un Guardian incluyen "compliance," "counsel," "audit," "legal"). Esta columna existe hoy como vocabulario de referencia; ningún código de clasificación la compara automáticamente contra texto entrante todavía.

## Cómo llega la taxonomía al grafo de conocimiento

[[service-content]] expone una pequeña API administrativa que lee cada archivo CSV y carga sus filas en el grafo como entidades estáticas. Las once filas de arquetipos se cargan como `classification: "archetype"`, y las del Plan de Cuentas como `classification: "coa-profile"`, ambas etiquetadas con un módulo dedicado `__taxonomy__` para distinguirlas de las entidades extraídas de documentos reales. Recargar cualquiera de los dos archivos reemplaza el conjunto anterior de filas en lugar de añadirse a él.

## Dónde se aplica realmente la etiqueta de arquetipo

El único uso confirmado hoy de la taxonomía de arquetipos es la herramienta [[verification-surveyor|Verification Surveyor]]. Cuando un operador verifica manualmente la identidad de una entidad extraída, la herramienta le pide elegir uno de los once arquetipos del archivo de ontología y registra esa elección como una afirmación sobre la entidad, junto con la marca de tiempo de verificación y la URL de origen. Es una decisión humana tomada una vez por entidad durante la revisión — no una inferencia automática, ni un mecanismo que evalúe o puntúe el comportamiento continuo de una persona frente a su arquetipo. Las categorías del Plan de Cuentas no forman parte de este flujo; solo se aplica la selección de arquetipo.

## Véase también

- [[service-content]] — el servicio que posee ambos archivos CSV y los carga en el grafo de conocimiento
- [[verification-surveyor]] — la herramienta donde un operador aplica una etiqueta de arquetipo a una entidad verificada
- [[service-extraction]] — el motor de extracción que produce las entidades que revisa una sesión de Verification Surveyor
