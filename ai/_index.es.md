---
schema: foundry-doc-v1
title: "Cómo se usa y se contiene la IA"
slug: ai-index
category: ai
type: topic
content_type: topic
quality: complete
short_description: "Dónde se sitúa la IA y dónde no se le permite intervenir: el límite que mantiene a la IA alejada del registro autoritativo, el enrutamiento entre modelos, y los modelos pequeños del lado del cliente diseñados para aprender el propio entorno de un cliente. El núcleo funciona completamente sin ella."
index_type: thematic
index_scope: ai
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-24
editor: pointsav-engineering
paired_with: _index.md
---

La categoría **ai** recoge dónde se sitúa la IA en la plataforma y dónde no se le permite intervenir. Abarca el límite que mantiene a la IA alejada del registro autoritativo, el enrutamiento entre modelos, y los modelos pequeños del lado del cliente diseñados para aprender el propio entorno de un cliente. El núcleo determinista funciona completamente sin IA.

Esta es la puerta de entrada a la afirmación arquitectónica más distintiva de la plataforma — la IA se usa, y se contiene — y para los ingenieros que buscan una pieza específica de la pila de IA: el límite de inferencia, el enrutamiento soberano, el programa de modelos por niveles de proveedor, y las canalizaciones de entrenamiento que lo producen.

<!-- START-HERE-HIGHLIGHT: el motor lee este bloque para la tarjeta "empezar aquí"
     (reutiliza el componente cluster-card--start-here existente). No añadir más de una. -->

**"El núcleo funciona completamente sin ella"** es la afirmación central de esta categoría, y el artículo que la sustenta — [[substrate-without-inference-base-case]] — vive en [Componentes básicos](/category/substrate), no aquí. Léalo primero si está evaluando la afirmación de contención en sí misma; todo lo demás la asume.

<!-- END-START-HERE-HIGHLIGHT -->

## El límite del Doorman

La única puerta por la que se enruta cada llamada de inferencia — ningún servicio posee sus propias credenciales de IA ni realiza una llamada saliente directa.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: the-doorman-boundary -->
- [[doorman-protocol|Protocolo Doorman]] — el único límite de solicitudes de IA: enrutamiento de tres niveles, el libro de auditoría, la disciplina `moduleId`
- [[sovereign-ai-routing|Enrutamiento de IA y la esclusa lingüística]] — la disciplina de sanitizar-al-salir / rehidratar-al-entrar aplicada en ese límite antes de que cualquier dato llegue a un modelo externo
- [[decode-time-constraints|Restricciones en tiempo de decodificación]] — reglas gramaticales aplicadas en cada paso de token, que hacen matemáticamente imposible producir vocabulario prohibido o salidas inválidas
- [[slm-stack-architecture|Arquitectura de la pila Rust de SLM]] — el grafo de dependencias Rust y la arquitectura binaria detrás de `service-slm`, el crate que implementa el Doorman
<!-- END AUTO-GENERATED -->

## Niveles de cómputo

Dónde se ejecuta realmente la inferencia, y el modelo especializado de proveedor hacia el que apunta el nivel superior.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: compute-tiers -->
- [[zero-container-inference|Inferencia sin contenedores]] — el patrón de despliegue planeado para el Nivel B de GPU: binarios nativos bajo systemd, temporizadores de apagado por inactividad en lugar de un runtime de contenedores
- [[pointsav-llm|PointSav-LLM]] — el modelo especializado de proveedor planeado para el Nivel 3, aún no operativo; prospectivo en su totalidad
<!-- END AUTO-GENERATED -->

## Extracción de entidades y el bucle de entrenamiento

Cómo la plataforma convierte el uso en señal de entrenamiento — el mecanismo detrás de "la plataforma aprende de cómo se usa."

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: entity-extraction-and-training-loop -->
- [[tiered-entity-extraction-architecture|Arquitectura de extracción de entidades por niveles]] — la canalización de extracción de tres niveles por documento: detección extractiva GLiNER, respaldo generativo OLMo, enriquecimiento por GPU
- [[elastic-compute-lora-training-pipeline|Canalización nocturna de entrenamiento LoRA de Elastic Compute #1]] — el trabajo nocturno de dos fases que reconstruye el DataGraph y entrena los pesos del adaptador
- [[learning-datagraph-architecture|DataGraph de aprendizaje]] — las cuatro vías de captura de señal de entrenamiento: captura de trayectoria, cola de aprendizaje, pares DPO editoriales, destilación de correcciones
- [[flow-quality-architecture|Flujo de conocimiento: bucle de entrenamiento y DataGraph ontológico]] — el marco de calidad que pregunta si el bucle de entrenamiento y el DataGraph realmente funcionan, no solo si se ejecutan
<!-- END AUTO-GENERATED -->

## Véase también

- [Cómo Está Construido](/architecture/) — la construcción de tres anillos que hace estructural este límite
- [Componentes básicos](/substrate/) — conceptos de mecanismo relacionados con la IA, incluyendo el artículo de opcionalidad de IA mencionado arriba
- [Servicios de la plataforma](/services/) — las páginas por servicio, incluyendo el propio servicio de IA
