---
schema: foundry-doc-v1
title: "Registros de Lenguaje Editorial"
slug: editorial-language-registers
category: reference
status: stable
bcsc_class: no-disclosure-implication
last_edited: 2026-05-08
editor: pointsav-engineering
language: es
paired_with: editorial-language-registers.md
---

Los tres wikis de PointSav se dirigen a tres audiencias primarias distintas. Cada audiencia tiene diferente nivel de alfabetización financiera y técnica, diferentes razones para leer y diferentes expectativas de vocabulario. Este artículo define los tres registros, explica quién es cada audiencia y establece las reglas de vocabulario que rigen los tres wikis.

## Mapa de audiencias

| Wiki | Audiencia primaria | Registro |
|---|---|---|
| `content-wiki-corporate` | Banqueros, family offices, inversores institucionales | Bloomberg / FT / Economist |
| `content-wiki-projects` | Top-400 firmas promotoras, arquitectos comerciales, gestores de programas de construcción | Bloomberg / FT / Economist |
| `content-wiki-documentation` | Ingenieros de software, diseñadores, desarrolladores de plataforma | Stripe / Cloudflare + capa de accesibilidad corporativa |
| `bim.woodfinegroup.com` | Arquitectos, ingenieros, funcionarios de código de construcción | Especificación RIBA / IFC |
| `gis.woodfinegroup.com` | Analistas GIS, gestores de programas de co-ubicación | Especificación técnica |
| `design.pointsav.com` | Contribuidores al sistema de diseño | Especificación de diseño (DTCG) |

Los wikis corporativo y de proyectos comparten registro porque comparten audiencia primaria. La materia cambia —gobierno corporativo y estructura de capital versus programas de desarrollo inmobiliario y mercados de co-ubicación—, pero el marco de evaluación financiera del lector no cambia.

## Registro 1 — Bloomberg / FT / Economist

**Aplica a:** `content-wiki-corporate` y `content-wiki-projects`

El lector es un tomador de decisiones institucional con alfabetización financiera. Lee para tomar decisiones de asignación de capital o para evaluar la estructura y los patrocinadores de la plataforma.

**Reglas principales:**
- Extensión de oración: objetivo de 14–18 palabras; límite máximo de 25
- Estructura del párrafo inicial: la consecuencia primero — el hecho más importante para un asignador de capital va en la primera oración
- Voz: activa. La voz pasiva oculta la responsabilidad y se percibe como evasión.
- Números: siempre específicos. "7 dólares al mes" en lugar de "bajo costo."
- Jerga: traducir todo en el primer uso. Los términos internos de la plataforma no aparecen sin un equivalente en lenguaje llano inmediatamente antes.
- Bloques de código: nunca.

## Registro 2 — Stripe / Cloudflare + capa de accesibilidad corporativa

**Aplica a:** `content-wiki-documentation`

El lector primario es un ingeniero o diseñador. El lector secundario —cada vez más importante— es un lector institucional de nueva generación: el comité tecnológico de un banco, el responsable de una siguiente generación en una family office, o un desarrollador senior de una firma del Top-400 que evalúa si la plataforma merece respaldo financiero.

**Reglas principales:**
- Estructura por sección: Concepto → Por qué importa (una oración, consecuencia primero, sin jerga) → Cómo funciona → Código → Casos límite
- La oración "por qué importa" debe ser comprensible para el lector institucional que escanea los encabezados de sección
- Bloques de código: reales y ejecutables.
- Términos de plataforma: definir una vez en lenguaje llano, luego usar el término.

## Registro 3 — Especificación RIBA / IFC

**Aplica a:** sitios especializados únicamente — `bim.woodfinegroup.com`, `gis.woodfinegroup.com`, `design.pointsav.com`

El lenguaje de especificación prescriptiva (deberá / no deberá para requisitos, medidas con unidades, distinción normativa vs. informativa) es el registro correcto para los sitios especializados. No aparece en los tres wikis principales, porque el lenguaje de "deberá" resulta agresivo para un asignador de capital y la especificación señala "documento de cumplimiento", no "plataforma creíble."

## Retiro de vocabulario

| Retirar | Reemplazar con |
|---|---|
| Substrate | la capa de datos / el código de la plataforma / la base de seguridad |
| Doctrine | principio arquitectónico / decisión de diseño / política de ingeniería |
| Compounding | agregación de señal de entrenamiento / mejora del modelo en el tiempo |
| Leapfrog | diseñado para superar / previsto para reemplazar / planificado para [fecha] |
| Doorman | pasarela de control de acceso / enrutador de solicitudes de IA |
| Ring 1 / Ring 2 / Ring 3 | nivel de archivo / nivel de datos / pasarela de inferencia |
| Totebox | archivo de propiedades / bóveda de datos |
| Yo-Yo pool | instancias GPU bajo demanda / nodos de inferencia efímeros |
| Sovereign (adjetivo) | verificable de forma independiente / controlado por el operador |
| LadybugDB | base de datos de grafos de propiedades / el almacén del DataGraph |

## Véase también

- [[editorial-philosophy]] — el modelo Wikipedia y el propósito de aprendizaje que comparten todos los registros
- [[style-guide-topic]] — estructura de artículos y convenciones del patrón Wikipedia
- [[glossary-documentation]] — definiciones canónicas de términos
