---
schema: foundry-doc-v1
title: "Aprendizaje Fundamentado en Grafos de Conocimiento"
slug: knowledge-graph-grounded-apprenticeship.es
category: architecture
type: topic
quality: published
short_description: "El Portero consulta el grafo de conocimiento por inquilino antes de cada solicitud de inferencia, produciendo tuplas de entrenamiento donde el grafo y el adaptador del modelo co-evolucionan."
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: knowledge-graph-grounded-apprenticeship.md
---

El **Aprendizaje Fundamentado en Grafos de Conocimiento** es el patrón por el cual el Portero (`service-slm`) consulta el grafo de conocimiento por inquilino en `service-content` antes de despachar cualquier solicitud de inferencia sustantiva. El contexto de fundamentación — un subgrafo de entidades y relaciones relevantes para la consulta — se suministra al modelo junto con la solicitud. La tupla de entrenamiento resultante contiene tanto el contexto del grafo como la respuesta del modelo, lo que significa que el grafo de conocimiento y el adaptador por inquilino mejoran juntos con el tiempo. Esta reclamación codifica el punto doctrinal #44.

## Fundamentación previa a la inferencia

Antes de despachar una solicitud a cualquier nivel de cómputo, el Portero llama a la herramienta de consulta de grafo de `service-content` para ensamblar un subgrafo de dos saltos alrededor de los términos de la consulta. Este subgrafo se presenta como un prefijo estructurado en el prompt del sistema del modelo, incluyendo entidades relevantes, sus relaciones y sus clasificaciones de dominio y tema.

Cuando una consulta no tiene contexto de grafo relevante — por ejemplo, una pregunta genérica de administración del sistema — el Portero procede sin fundamentación y la tupla de entrenamiento se marca como no fundamentada. El modelo aprende así que algunas preguntas no requieren contexto de grafo.

## Mutación del grafo post-inferencia

Cuando la respuesta del modelo incluye salidas estructuradas y el veredicto del operador acepta la respuesta, el Portero puede proponer mutaciones del grafo derivadas de la respuesta — nuevas entidades, nuevas relaciones o propiedades actualizadas. `service-content` aplica los cambios atómicamente, por inquilino, y el registro de auditoría registra el evento de mutación.

El bucle se cierra: las entidades descubiertas durante una interacción de inferencia se convierten en contexto de fundamentación para la siguiente. El grafo de conocimiento crece a través del uso.

## Aislamiento por inquilino

El identificador de módulo que determina el alcance de cada grafo también aísla el contexto de entrenamiento. El grafo y el corpus de entrenamiento de un inquilino no pueden ser accedidos por otro inquilino ni utilizados para entrenar el adaptador de otro inquilino. Los límites son estructurales, no de política.

## Métricas de calidad basadas en coherencia con el grafo

Una respuesta del modelo puede evaluarse contra el grafo en tres dimensiones: la tasa de citación (qué fracción de las entidades nombradas en la respuesta existen en el grafo), la precisión de las relaciones (qué fracción de las relaciones declaradas coinciden con aristas del grafo) y la tasa de alucinación (qué fracción de las entidades nombradas no están presentes en el grafo). Una tasa de alucinación elevada es el principal modo de fallo; las respuestas por encima de un umbral son candidatas para rechazo o refinamiento.

## Dependencia de la Disciplina de Límite Único

Este patrón depende de la [[single-boundary-compute-discipline]]. Si la inferencia puede evitar el Portero, también evita la fundamentación del grafo. Sin cumplimiento de límite único, el aprendizaje fundamentado en grafos de conocimiento no puede garantizarse estructuralmente.

## Véase También

- [[single-boundary-compute-discipline]] — requisito previo estructural
- [[seed-taxonomy-as-smb-bootstrap]] — la taxonomía por inquilino que siembra el grafo de conocimiento utilizado para la fundamentación
- [[mcp-substrate-protocol]] — las herramientas MCP `graph_query` y `graph_mutate`

---

## Procedencia

Resumen de adaptación estratégica del archivo fuente `convention-knowledge-graph-grounded-apprenticeship.md` (refinado el 30 de abril de 2026).

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*
