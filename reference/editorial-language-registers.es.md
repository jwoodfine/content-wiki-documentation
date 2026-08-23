---
schema: foundry-doc-v1
content_type: topic
title: "Registros de lenguaje editorial"
slug: editorial-language-registers
short_description: "Tres registros de lenguaje que ajustan las wikis de PointSav a sus audiencias: prensa financiera, plataforma de desarrolladores y especificación regulatoria."
category: reference
status: stable
bcsc_class: no-disclosure-implication
last_edited: 2026-08-22
editor: pointsav-engineering
language: es
paired_with: editorial-language-registers.md
---

Los tres wikis de PointSav se dirigen a tres audiencias primarias distintas. Cada audiencia tiene diferente nivel de alfabetización financiera y técnica, diferentes razones para leer y diferentes expectativas de vocabulario. Este artículo es una visión general, orientada al lector, de los tres registros; las normas de redacción detalladas y autoritativas que los sustentan se mantienen como el conjunto de guías de estilo editorial de la organización, la única fuente de verdad a la que remite cualquier otra nota sobre voz o registro. El [[language-protocol-substrate|sustrato de protocolo de lenguaje]] hace cumplir estas reglas estructuralmente en el momento de la captura.

## El estándar editorial

Cinco reglas, reconciliadas y ratificadas por el operador el 2026-05-21, son el estándar editorial detrás de cada registro definido aquí. Los registros siguientes especializan estas reglas para una audiencia concreta; nunca las relajan. Donde una regla de registro y una regla siguiente parezcan entrar en conflicto, prevalece la regla siguiente.

1. **La longitud de la oración se presupuesta según su función.** Una oración de desarrollo — la que desarrolla un mecanismo o un argumento dentro de una sección del cuerpo — llega a unas 45 palabras como máximo. Una oración de divulgación — el encabezado, una afirmación de cumplimiento, una declaración regulatoria — llega a 25 palabras como máximo. Varíe el ritmo: cada párrafo incluye al menos una oración corta y declarativa.
2. **Los verbos activos describen el mecanismo como hecho presente.** Use la voz activa para describir cómo funciona algo ahora. No la use para afirmar como hecho consumado una afirmación prospectiva — la capacidad, el cronograma o el resultado aún no real conserva `planificado`, `previsto`, `puede` u `objetivo`. No atribuya intención ni emoción humana a un sistema. No hay prohibición de `es`, `son` o `era`.
3. **La analogía es un techo, no una cuota.** Una analogía es opcional. Donde se use, manténgase en una como máximo por cada 300 palabras.
4. **El encabezado es el núcleo informativo; el arco Franklin ordena el cuerpo.** El encabezado de cuatro párrafos lleva la noticia en aproximadamente el primer 10% del artículo. El arco Franklin — Crisis, luego Búsqueda, luego Avance — rige solo el orden de las secciones del cuerpo.
5. **Se rechaza el registro de marketing SaaS.** El contenido público no adopta la voz promocional de una página de producto de software. Los nombres en clave internos se mantienen internos.

## Qué es un registro

Un registro de lenguaje es la combinación de estructura de oración, vocabulario, profundidad y tono apropiada para una audiencia específica en un contexto específico. Un informe financiero usa un registro distinto al de una especificación técnica. El periodismo financiero institucional usa un registro distinto al de un código de construcción. La documentación de plataforma para desarrolladores usa un registro distinto a ambos. Los wikis de PointSav se escriben en tres registros distintos — uno por audiencia — aplicados de forma consistente en cada artículo.

El registro no es una preferencia de estilo. Es la diferencia entre un lector que comprende lo que vino a aprender y un lector que se rinde y cierra la pestaña.

## Mapa de audiencias

| Wiki | Audiencia primaria | Audiencia secundaria | Registro |
|---|---|---|---|
| `media-knowledge-corporate` | Banqueros, family offices, inversores institucionales | Directivos de nivel C, asesores corporativos | Registro institucional de prensa financiera |
| `media-knowledge-projects` | Top-400 firmas promotoras, arquitectos comerciales, gestores de programas de construcción | Los mismos inversores institucionales, leyendo sobre la materia de proyectos | Registro institucional de prensa financiera |
| `media-knowledge-documentation` | Ingenieros de software, diseñadores gráficos, desarrolladores de plataforma | Lectores institucionales emergentes que evalúan la credibilidad técnica | Registro de plataforma de desarrolladores + capa de accesibilidad corporativa |
| `bim.woodfinegroup.com` | Arquitectos, ingenieros, funcionarios de código de construcción | — | Registro de especificación regulatoria |
| `gis.woodfinegroup.com` | Analistas GIS, gestores de programas de co-ubicación | — | Especificación técnica |
| `design.pointsav.com` | Contribuidores al sistema de diseño, autores de componentes | — | Especificación de diseño (DTCG, API de componentes) |

Los wikis corporativo y de proyectos comparten registro porque comparten audiencia primaria. La materia cambia —gobierno corporativo y estructura de capital versus programas de desarrollo inmobiliario y mercados de co-ubicación—, pero el marco de evaluación financiera del lector no cambia.

## Registro 1 — Registro institucional de prensa financiera

**Aplica a:** `media-knowledge-corporate` y `media-knowledge-projects`

El lector es un tomador de decisiones institucional con alfabetización financiera. Lee para tomar decisiones de asignación de capital o para evaluar la estructura y los patrocinadores de la plataforma.

**Reglas principales:**
- Extensión de oración: objetivo de 14–18 palabras; límite máximo de 25
- Estructura del párrafo inicial: la consecuencia primero — el hecho más importante para un asignador de capital va en la primera oración
- Voz: activa. La voz pasiva oculta la responsabilidad y se percibe como evasión.
- Números: siempre específicos. "7 dólares al mes" en lugar de "bajo costo." "Mercados de desarrollo Top-400" en lugar de "mercados importantes."
- Jerga: traducir todo en el primer uso. Los términos internos de la plataforma no aparecen sin un equivalente en lenguaje llano inmediatamente antes.
- Bloques de código: nunca. El lector corporativo y de proyectos no necesita ver comandos de terminal.
- Citas: investigación financiera, presentaciones regulatorias, informes de la industria, datos de mercado
- Evitar: matizaciones académicas, sustantivos abstractos, afirmaciones de marketing dramáticas, metáforas internas de la plataforma

### Ejemplos de consecuencia primero

**Patrón de consecuencia primero:**

*"El marco Direct-Hold elimina el fondo agrupado. Cada propiedad es su propia unidad legal y financiera."*

*"Cada sitio de desarrollo de co-ubicación se suscribe como un evento de capital independiente. Woodfine no agrupa el desempeño entre sitios — la convergencia en un nodo se valida de forma independiente antes de comprometer capital."*

Mismo lector, mismo registro, distinta materia.

## Registro 2 — Registro de plataforma de desarrolladores + capa de accesibilidad corporativa

**Aplica a:** `media-knowledge-documentation`

El lector primario es un ingeniero o diseñador. El lector secundario —cada vez más importante— es un lector institucional emergente: el comité tecnológico de un banco, un responsable entrante en una family office, o un desarrollador senior de una firma del Top-400 que evalúa si la plataforma merece respaldo financiero.

**Reglas principales:**
- Estructura por sección: Concepto → Por qué importa (una oración, consecuencia primero, sin jerga) → Cómo funciona → Código → Casos límite
- La oración "por qué importa" debe ser comprensible por sí sola para el lector institucional que escanea los encabezados de sección — es la capa de accesibilidad corporativa
- Bloques de código: reales y ejecutables; si se abrevian, marcar con `# ...`
- Jerga técnica (gRPC, systemd, JSON, async): usar con libertad — no hace falta explicarla
- Términos de plataforma: definir una vez en lenguaje llano, luego usar el término.
- Tono: entre pares, seguro, directo — de ingeniero a ingeniero
- Evitar: sobreexplicar lo básico (HTTP, SSH, git), descripciones de arquitectura vagas, ejemplos incompletos

### La capa de accesibilidad en la práctica

**Patrón de la capa de accesibilidad:**

*"**[[service-slm|service-slm]]** enruta cada solicitud de IA al nivel de cómputo más económico que cumple el plazo, sin que quien la origina especifique el nivel. Primero inferencia local (5 s), luego ráfaga en la nube (10 s), por último API externa (30 s). Una solicitud que se resuelve localmente nunca sale de la infraestructura del cliente — y nunca aparece en un estado de cuenta de facturación en la nube."*

La última oración es la capa de accesibilidad corporativa. Un lector institucional que escanea encabezados de sección obtiene: "puede ejecutarse localmente, y usted no paga nada cuando lo hace."

## Registro 3 — Registro de especificación regulatoria

**Aplica a:** sitios especializados únicamente — `bim.woodfinegroup.com`, `gis.woodfinegroup.com`, `design.pointsav.com`

El lenguaje de especificación prescriptiva (deberá / no deberá para requisitos, medidas con unidades, distinción normativa vs. informativa, citas de normas, en la tradición de los códigos de construcción y los organismos de normas de interoperabilidad) es el registro correcto para los sitios especializados. No aparece en los tres wikis principales porque la audiencia de esos wikis es el tomador de decisiones institucional, no el ingeniero de cumplimiento. El lenguaje de "deberá" resulta agresivo para un asignador de capital, y el lenguaje de especificación señala "documento de cumplimiento", no "plataforma creíble."

### Remitir a los sitios especializados

**Los sitios especializados como destino de referencias cruzadas:**

Cuando un artículo de un wiki principal hace referencia a un tema que requiere especificación prescriptiva, enlazar al sitio especializado correspondiente:

- *"Para las especificaciones completas de tokens de zona climática y los mapeos IFC, véase `bim.woodfinegroup.com`."*
- *"Para la metodología de puntuación de co-ubicación y los criterios de zonificación, véase `gis.woodfinegroup.com`."*
- *"Para los esquemas de tokens de diseño y las especificaciones de componentes, véase `design.pointsav.com`."*

Estos sitios son destinos de referencia canónicos, de la misma manera que los artículos de Wikipedia enlazan a normas técnicas — el artículo principal es legible para una audiencia general; el sitio especializado es donde se va a construir o verificar.

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
| Compounding Substrate | la plataforma (primer uso); enlazar al artículo de arquitectura |
| Apprenticeship Substrate | la canalización de aprendizaje / el sistema de entrenamiento |
| LadybugDB | base de datos de grafos de propiedades / el almacén del DataGraph |

**Regla:** los términos retirados pueden aparecer en artículos de arquitectura y de servicios del wiki de documentación cuando se están definiendo explícitamente. No deben aparecer en el wiki corporativo, el wiki de proyectos o el contenido de GUIDE sin una traducción en lenguaje llano inmediatamente antes.

## Véase también

- [[editorial-philosophy]] — el modelo Wikipedia y el propósito de aprendizaje que comparten todos los registros
- [[glossary-documentation]] — definiciones canónicas de términos
