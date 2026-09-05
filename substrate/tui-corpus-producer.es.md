---
schema: foundry-doc-v1
title: "TUI como productora de corpus"
slug: tui-corpus-producer
category: substrate
type: topic
content_type: topic
quality: complete
index_group: small-language-model-stack
short_description: "Cada interacción del operador con service-slm a través de la interfaz de terminal es una contribución curada al corpus de entrenamiento del adaptador por inquilino."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
editor: pointsav-engineering
cites: []
references:
  - id: 1
    text: "Rafailov, R. et al. 'Direct Preference Optimization: Your Language Model is Secretly a Reward Model.' NeurIPS, 2023."
    url: "https://arxiv.org/abs/2305.18290"
  - id: 2
    text: "Zhou, C. et al. 'LIMA: Less Is More for Alignment.' NeurIPS, 2023."
    url: "https://arxiv.org/abs/2305.11206"
paired_with: tui-corpus-producer.md
---


El patrón **TUI como Productora de Corpus** es la intención de diseño de que la interacción del operador por terminal con el [[compounding-doorman|Portero]] se convierta en fuente primaria de datos de entrenamiento de alta calidad para el [[adapter-composition|adaptador del modelo]] por inquilino. No existe un único componente de terminal `slm-cli` — la app de consola que hoy monitorea al Portero (`app-console-slm`) es un panel de salud y conteo de entidades, sin superficie de chat ni de captura de veredicto propia. La vía de captura de veredicto que sí existe hoy, `POST /v1/verdict`, la invoca la consola del corrector de estilo, no una interfaz de chat de SLM de propósito general. El patrón que describe este artículo — cualquier interacción de terminal alimentando un corpus de entrenamiento mediante un veredicto firmado — es la dirección prevista de la plataforma, no una TUI generalizada ya entregada.

## Por qué las interacciones de terminal producen datos de alta calidad

Las interacciones de administración de sistemas e infraestructura tienen tres propiedades que las distinguen de los datos de entrenamiento generales:

**Verdad fundamental verificable.** Cuando un operador sigue el consejo de la IA — ejecutando un comando sugerido, aplicando un cambio de configuración propuesto — el sistema se recupera o no lo hace. No existe ninguna demora para saber si la respuesta fue correcta. Esta propiedad de retroalimentación inmediata es exclusiva de los dominios operacionales.

**Dominio acotado.** Las operaciones de archivo, las convenciones del sistema y el vocabulario de flujo de trabajo específico del cliente forman un conjunto acotado de comandos y modos de fallo. Los modelos se entrenan más eficientemente sobre dominios acotados que sobre corpus generales.

**Retroalimentación de expertos en el dominio.** El operador que emite un veredicto es la persona que sabe si la respuesta fue correcta, no un anotador distante del trabajo real. La literatura publicada sobre aprendizaje por refuerzo a partir de retroalimentación humana reporta consistentemente que las tuplas de interacción firmadas con veredicto entrenan un orden de magnitud más eficientemente que las tuplas sin veredicto. [^1]

## El mecanismo de veredicto

El endpoint de veredicto que existe hoy (`POST /v1/verdict`) es binario: aceptar la respuesta, o rechazarla y quedarse con la alternativa. No hay una tercera disposición de "refinar en línea" en el mecanismo entregado, aunque sería una extensión de diseño natural. Un veredicto binario de aceptar/rechazar basta para producir un par de entrenamiento de optimización de preferencia directa — la respuesta aceptada y la rechazada para el mismo prompt — sin necesitar una escala graduada. Si una interacción no produce ningún veredicto, no se ha confirmado que exista hoy una vía de captura para el ajuste fino supervisado sin veredicto.

## Propiedad del adaptador por inquilino

El corpus producido por los operadores de un cliente entrena el adaptador de ese cliente, no un adaptador general. Por la convención [[customer-owned-graph-ip]], los pesos del adaptador entrenado son propiedad del cliente. La plataforma distribuye la arquitectura del modelo y el pipeline de entrenamiento; el cliente retiene el adaptador resultante.

## Disciplina de captura de veredicto

Ciertas sesiones de terminal no deben contribuir al corpus de entrenamiento: las sesiones de prueba iniciadas con una bandera de no-corpus, las sesiones interrumpidas por niveles no disponibles antes de completarse, y las sesiones en modo de depuración de nivel forzado se registran en el [[worm-ledger-architecture|registro de auditoría]] pero se excluyen de los datos de entrenamiento normales.

## Véase También

- [[single-boundary-compute-discipline]] — la TUI nunca llama a los niveles de inferencia directamente
- [[customer-owned-graph-ip]] — los pesos del adaptador por inquilino son propiedad del cliente
- [[knowledge-graph-grounded-apprenticeship]] — las tuplas de entrenamiento llevan contexto de grafo cuando el Portero fundamenta la solicitud
