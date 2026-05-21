---
schema: foundry-doc-v1
title: "Guía de estilo — TOPIC"
slug: style-guide-topic.es
short_description: "Estándares editoriales para archivos TOPIC en wikis de contenido: la apertura de cuatro párrafos Bloomberg, registro institucional 75/25, prueba de oración de CFO, regla de actores nombrados, voz, lenguaje orientado al futuro, disciplina de cita y la distinción de archivos GUIDE."
lang: es
category: reference
type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-21
editor: pointsav-engineering
paired_with: style-guide-topic.md
---

Un archivo TOPIC explica *qué es* algo — arquitectura, contexto o antecedentes de la plataforma que un lector nuevo necesita para orientarse. No describe cómo operar algo; eso corresponde a un archivo GUIDE.

Este artículo es en sí mismo un TOPIC y sigue la estructura que documenta.

## El estándar editorial

Estas cinco reglas son el estándar editorial ratificado para cada TOPIC. Fueron reconciliadas y ratificadas por el operador el 2026-05-21. Donde cualquier otra guía de este documento — o de [[editorial-language-registers]] — entre en conflicto con una regla siguiente, prevalece la regla.

1. **La longitud de la oración se presupuesta según su función.** Una oración de desarrollo — la que desarrolla un mecanismo o un argumento dentro de una sección del cuerpo — llega a unas 45 palabras como máximo. Una oración de divulgación — el encabezado, una afirmación de cumplimiento, una declaración regulatoria — llega a 25 palabras como máximo. Varíe el ritmo: cada párrafo incluye al menos una oración corta y declarativa.
2. **Los verbos activos describen el mecanismo como hecho presente.** Use la voz activa para describir cómo funciona algo ahora. No la use para afirmar como hecho consumado una afirmación prospectiva — la capacidad, el cronograma o el resultado aún no real conserva `planificado`, `previsto`, `puede` u `objetivo`. No atribuya intención ni emoción humana a un sistema. No hay prohibición de `es`, `son` o `era`.
3. **La analogía es un techo, no una cuota.** Una analogía es opcional. Donde se use, manténgase en una como máximo por cada 300 palabras.
4. **El encabezado es el núcleo informativo; el arco Franklin ordena el cuerpo.** El encabezado Bloomberg de cuatro párrafos lleva la noticia en aproximadamente el primer 10% del artículo. El arco Franklin — Crisis, luego Búsqueda, luego Avance — rige solo el orden de las secciones del cuerpo.
5. **Se rechaza el registro de marketing SaaS.** El contenido público no adopta la voz promocional de una página de producto de software. Los nombres en clave internos se mantienen internos y no aparecen en el texto público de un TOPIC.

## Dónde viven los TOPICs

| Wiki | Materia | Licencia |
|---|---|---|
| `content-wiki-documentation` | Documentación de la plataforma del proveedor | CC BY 4.0 (pública) |
| `content-wiki-corporate` | Principios corporativos del cliente | CC BY-ND 4.0 |
| `content-wiki-projects` | Narrativas de proyectos del cliente | CC BY-ND 4.0 |

Un TOPIC vive en la wiki cuya materia cubre. Cruzar estos límites en silencio es deriva; plantee la pregunta en lugar de elegir arbitrariamente.

## Pareja bilingüe obligatoria

Cada TOPIC se entrega como pareja: el archivo en inglés y una adaptación estratégica en español (`.es.md`). El archivo en español es adaptación estratégica, no traducción 1:1 — traduzca la orientación que necesita un lector hispanohablante; omita el detalle de implementación más profundo.

## Frontmatter requerido

Cada TOPIC declara sus metadatos en frontmatter YAML. La lista `cites` es obligatoria cuando el artículo hace afirmaciones que se resuelven en instrumentos regulatorios externos, documentos de investigación o especificaciones técnicas.

## Estructura del encabezado Bloomberg

Un TOPIC abre con un encabezado de cuatro párrafos de estilo Bloomberg. El modelo: el primer párrafo enuncia la propiedad estructural en una oración que satisfaría a un analista de Goldman Sachs leyendo en su teléfono. El segundo párrafo aporta un dato concreto o número que hace verificable el primero. El tercero explica el mecanismo. El cuarto declara por qué importa a un comprador regulado, un auditor o un gestor de riesgos.

| Párrafo | Contenido | Prueba |
|---|---|---|
| 1 — Qué + consecuencia | La propiedad estructural y su consecuencia de cumplimiento o riesgo | ¿Puede un analista leerlo en su teléfono y entender el punto? |
| 2 — Dato concreto | Un dato específico: métrica, fecha, decisión binaria | ¿Es verificable? ¿Hace falsificable el párrafo 1? |
| 3 — Mecanismo | Cómo funciona | ¿Es esta la descripción más simple y precisa del mecanismo? |
| 4 — Por qué importa | Consecuencia para el cumplimiento, la custodia o el riesgo | ¿Sabe un comprador regulado qué acción tomar? |

**Prueba del PDF independiente.** Imprima los párrafos 1–4 de forma aislada y entréguelos a un lector que no verá nada más. El mensaje esencial de cumplimiento o riesgo debe sobrevivir. Si no lo hace, revise el encabezado antes de cualquier otra edición.

## Voz — Bloomberg, no marketing

El estándar es prosa precisa y profesional comprensible para un lector financieramente competente sin formación técnica. Voz activa salvo que la voz pasiva aporte un significado técnico específico. La longitud de la oración sigue el estándar presupuestado arriba — oraciones de desarrollo hasta unas 45 palabras, prosa de divulgación hasta 25 — y cada párrafo incluye al menos una oración corta y declarativa.

La lista de vocabulario prohibido se aplica en su totalidad: `aprovechar`, `empoderar`, `próxima generación`, `líder del sector`, `sin fricciones`, `robusto`, `de vanguardia`.

**Actores y consecuencias nombrados.** Cada oración activa nombra quién hace qué y cuál es la consecuencia si no lo hace. "El Portero centraliza todas las claves API" nombra al actor. "Las claves API se gestionan centralmente" lo oculta. La voz pasiva es útil solo cuando el actor genuinamente no importa; en la mayoría de las oraciones de gobernanza, el actor es el punto.

**Prueba de la oración del director financiero.** Cada oración debe ser útil para un director financiero — alguien que entiende contratos, riesgo y regulación pero no lee código fuente. El detalle de ingeniería puro sin consecuencia empresarial pertenece más adelante en el artículo o en una nota al pie.

**Disciplina "¿y qué?"** Cada párrafo del cuerpo responde a la pregunta: *¿y qué significa esto para un comprador regulado o un ingeniero consciente del riesgo?*

## Registro institucional y de desarrollo: 75/25

Un TOPIC en `content-wiki-documentation` se dirige a dos audiencias simultáneamente: lectores institucionales (comunidad financiera, compradores regulados, responsables de cumplimiento, auditores) y lectores de desarrollo (ingenieros, arquitectos, integradores). El registro objetivo es 75% institucional, 25% de desarrollo.

En la práctica: escriba la afirmación estructural y su consecuencia de cumplimiento antes del detalle de implementación.

## Vocabulario de gobernanza interna

Las palabras **Doctrina** y **Convención** como vocabulario de gobernanza interna nunca aparecen en el cuerpo del texto de un TOPIC ni en los encabezados de sección. Un analista leyendo este wiki debe encontrar la idea subyacente en prosa institucional, no el nombre interno del mecanismo de gobernanza.

Escriba el principio, no la etiqueta:
- En lugar de "según la Doctrina, ninguna IA puede escribir en el grafo de conocimiento" → "ningún componente de IA escribe en el grafo de conocimiento; esa ruta es exclusivamente determinista"

## Lenguaje prospectivo con advertencia

Un TOPIC que describe capacidad, cronograma, resultado para el cliente o acuerdo de gobernanza futuros usa `planificado`, `previsto`, `puede` o `objetivo` — nunca futuro declarativo. Este es el requisito de divulgación continua de la BCSC por `[ni-51-102]` y la disciplina de información prospectiva de `[osc-sn-51-721]`.

## Citar cada afirmación no obvia

La disciplina es auditabilidad, no exhaustividad académica. Un revisor que lea el TOPIC dentro de cinco años debe poder rastrear cada afirmación no obvia hasta su fuente.

## Editar en el mismo archivo

Sin sufijos `_V2` / `_V3` — el historial de Git es el registro de versiones. Esta regla se aplica con todo su peso a los archivos TOPIC porque el renderizador del wiki sirve la versión más reciente confirmada.

## Qué no es un TOPIC

- No es un manual operativo. Las instrucciones operativas viven en archivos GUIDE dentro de la subcarpeta de despliegue que operan.
- No es material de marketing. La audiencia es colaboradores, clientes, reguladores e ingenieros — no compradores que necesitan ser persuadidos.
- No es material solo para uso interno. Lo interno vive en los directorios `.agent/` del espacio de trabajo o en instancias de despliegue, no en una wiki de contenido.

## Véase también

- [[style-guide-guide|Guía de estilo — GUIDE]]
- [[language-protocol-substrate|Sustrato de protocolo de lenguaje]]
- [[citation-substrate|Sustrato de citación]]
- [[anti-homogenization-discipline|Disciplina anti-homogenización]]
