---
schema: foundry-doc-v1
title: "Aprendizaje fundamentado en grafos de conocimiento"
slug: knowledge-graph-grounded-apprenticeship
category: substrate
type: topic
content_type: topic
quality: complete
index_group: the-compounding-doorman-and-ai-boundary
short_description: "El Portero busca entidades coincidentes en el grafo de conocimiento por inquilino antes de despachar una solicitud, fundamentando la respuesta del modelo en hechos que el grafo ya contiene."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-22
editor: pointsav-engineering
cites: []
references:
  - id: 1
    text: "Edge, D. et al. 'From Local to Global: A Graph RAG Approach to Query-Focused Summarization.' arXiv:2404.16130, 2024."
    url: "https://arxiv.org/abs/2404.16130"
paired_with: knowledge-graph-grounded-apprenticeship.md
---


La **fundamentación en el grafo de conocimiento** es el patrón por el cual el [[compounding-doorman|Portero]] ([[service-slm]]) consulta el grafo de conocimiento por inquilino en [[service-content]] antes de despachar una solicitud a un nivel de cómputo. Las entidades coincidentes se anteponen al prompt del sistema del modelo como contexto factual, aisladas por inquilino mediante el identificador de módulo — el adaptador de Woodfine nunca ve el contexto del grafo de PointSav, ni viceversa.

Este patrón extiende el [[apprenticeship-substrate|sustrato de aprendizaje]] con una capa de fundamentación por grafo.

## Fundamentación previa a la inferencia

Antes de despachar una solicitud, el Portero extrae las palabras de cuatro o más caracteres del mensaje más reciente del usuario y consulta a [[service-content]] por entidades cuyo nombre coincide como subcadena con esas palabras, prefiriendo los candidatos más largos y específicos primero. Una entidad coincidente aporta su clasificación (Persona, Empresa, Proyecto, Cuenta o Ubicación) y, si se conocen, su rol, ubicación y datos de contacto — la consulta por defecto avanza un salto desde las entidades encontradas, no un recorrido más amplio. Los resultados se anteponen como un mensaje de sistema que el modelo ve junto con la consulta del usuario.

La búsqueda no es crítica: si `service-content` no está disponible o ninguna entidad coincide, la solicitud continúa sin modificar. Una pregunta genérica de administración del sistema, sin entidades relevantes en su texto, simplemente no recibe fundamentación — es el caso esperado y común, no un fallo.

## Sin escritura automática al grafo desde la inferencia

Nada en la ruta de enrutamiento o manejo de veredictos del Portero escribe de vuelta al grafo. El endpoint de mutación que expone [[service-content]] (`POST /v1/graph/mutate`) existe, pero su único invocador real es una herramienta operada por humanos — `graph-committer.py` de project-editorial, que exige que un operador revise una propuesta almacenada y confirme explícitamente antes de escribir nada. Una ruta separada, no relacionada, sí escribe entidades sin revisión humana por elemento: un trabajo de extracción nocturno que, cuando está habilitado, captura entidades extraídas automáticamente para su aprobación por lote posterior. Véase [[nightly-datagraph-rebuild]] para el comportamiento real de ese mecanismo y su brecha de gobernanza actualmente abierta. Ninguna de las dos rutas se activa por el veredicto de una solicitud de inferencia.

## Aislamiento por inquilino

El identificador de módulo que determina el alcance de cada grafo también aísla el contexto de entrenamiento. El grafo de un inquilino no puede ser accedido por otro inquilino. Los límites son estructurales, no de política.

## Métricas de calidad basadas en coherencia con el grafo

Una respuesta del modelo puede evaluarse contra el grafo en tres dimensiones, independientemente de si el grafo mismo cambia. La tasa de citación mide qué fracción de las entidades nombradas en la respuesta existen en el grafo. La precisión de las relaciones mide qué fracción de las relaciones declaradas coinciden con las aristas ya registradas. La tasa de alucinación mide qué fracción de las entidades nombradas no están presentes en el grafo — es el principal modo de fallo; las respuestas por encima de un umbral son candidatas para rechazo o refinamiento. [^1]

## Dependencia de la disciplina de límite único

La fundamentación depende de la [[single-boundary-compute-discipline]]. Si la inferencia puede evitar al Portero, también evita la fundamentación del grafo por completo — una solicitud que rodea al Portero no recibe contexto de entidades ni medición de tasa de citación. Sin cumplimiento de límite único, la fundamentación no puede garantizarse para cada solicitud.

## Véase también

- [[single-boundary-compute-discipline]] — requisito previo estructural; la fundamentación ocurre en el límite del Portero
- [[seed-taxonomy-as-smb-bootstrap]] — la taxonomía por inquilino que siembra el grafo de conocimiento utilizado para la fundamentación
- [[mcp-substrate-protocol]] — las herramientas MCP mediante las cuales el Portero interactúa con `service-content`
- [[nightly-datagraph-rebuild]] — la ruta separada, no relacionada, que sí escribe nuevas entidades al grafo
