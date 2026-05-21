---
schema: foundry-doc-v1
title: "Registros de Lenguaje Editorial"
slug: editorial-language-registers
short_description: "Las tres wikis de PointSav atienden audiencias distintas en registros de lenguaje distintos: tono institucional Bloomberg y FT para lectores corporativos y de proyectos, tono técnico Stripe y Cloudflare para ingenieros de documentación, y prosa de especificación RIBA para sitios de implementación especializada. Las reglas de retiro de vocabulario rigen traducción consistente entre registros."
category: reference
status: stable
bcsc_class: no-disclosure-implication
last_edited: 2026-05-21
editor: pointsav-engineering
language: es
paired_with: editorial-language-registers.md
---

Los tres wikis de PointSav se dirigen a tres audiencias primarias distintas. Cada audiencia tiene diferente nivel de alfabetización financiera y técnica, diferentes razones para leer y diferentes expectativas de vocabulario. Este artículo define los tres registros, explica quién es cada audiencia y establece las reglas de vocabulario que rigen los tres wikis.

## El estándar editorial

Cinco reglas, reconciliadas y ratificadas por el operador el 2026-05-21, son el estándar editorial detrás de cada registro definido aquí. Los registros siguientes especializan estas reglas para una audiencia concreta; nunca las relajan. Donde una regla de registro y una regla siguiente parezcan entrar en conflicto, prevalece la regla siguiente.

1. **La longitud de la oración se presupuesta según su función.** Una oración de desarrollo — la que desarrolla un mecanismo o un argumento dentro de una sección del cuerpo — llega a unas 45 palabras como máximo. Una oración de divulgación — el encabezado, una afirmación de cumplimiento, una declaración regulatoria — llega a 25 palabras como máximo. Varíe el ritmo: cada párrafo incluye al menos una oración corta y declarativa.
2. **Los verbos activos describen el mecanismo como hecho presente.** Use la voz activa para describir cómo funciona algo ahora. No la use para afirmar como hecho consumado una afirmación prospectiva — la capacidad, el cronograma o el resultado aún no real conserva `planificado`, `previsto`, `puede` u `objetivo`. No atribuya intención ni emoción humana a un sistema. No hay prohibición de `es`, `son` o `era`.
3. **La analogía es un techo, no una cuota.** Una analogía es opcional. Donde se use, manténgase en una como máximo por cada 300 palabras.
4. **El encabezado es el núcleo informativo; el arco Franklin ordena el cuerpo.** El encabezado Bloomberg de cuatro párrafos lleva la noticia en aproximadamente el primer 10% del artículo. El arco Franklin — Crisis, luego Búsqueda, luego Avance — rige solo el orden de las secciones del cuerpo.
5. **Se rechaza el registro de marketing SaaS.** El contenido público no adopta la voz promocional de una página de producto de software. Los nombres en clave internos se mantienen internos.

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

El lector primario es un ingeniero o diseñador. El lector secundario —cada vez más importante— es un lector institucional emergente: el comité tecnológico de un banco, un responsable entrante en una family office, o un desarrollador senior de una firma del Top-400 que evalúa si la plataforma merece respaldo financiero.

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
