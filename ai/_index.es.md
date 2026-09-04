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
last_edited: 2026-09-04
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
- [[doorman-protocol|Protocolo Doorman]] — Doorman es el único límite de solicitud de IA a través del cual se enruta toda llamada de inferencia — conserva cada credencial de modelo externo y registra cada llamada en un libro mayor de auditoría inmutable.
- [[sovereign-ai-routing|Enrutamiento de IA y la esclusa lingüística]] — El enrutamiento de IA mantiene cada credencial de modelo externo y audita cada solicitud en una única frontera. No depura PII de los prompts, y el enrutamiento de Nivel C hacia modelos externos todavía no está en producción.
- [[decode-time-constraints|Restricciones en tiempo de decodificación]] — La técnica de decodificación restringida, y una línea clara entre esa técnica y lo que PointSav ha construido hoy: un linter asesor posterior a la generación, con el mecanismo basado en gramática planificado, no implementado.
- [[slm-stack-architecture|Arquitectura de la pila Rust de SLM]] — El grafo de dependencias Rust y la arquitectura de binarios de service-slm, el servicio Doorman que media cada llamada de inferencia en la plataforma PointSav.
<!-- END AUTO-GENERATED -->

## Niveles de cómputo

Dónde se ejecuta realmente la inferencia, y el modelo especializado de proveedor hacia el que apunta el nivel superior.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: compute-tiers -->
- [[zero-container-inference|Inferencia sin contenedores]] — Patrón de implementación GPU de Nivel B con binarios Linux nativos bajo systemd sobre una GPU L4, con la detección de inactividad ejecutándose desde el proceso del servidor Doorman en lugar de un temporizador en la propia VM de GPU.
- [[pointsav-llm|PointSav-LLM]] — El modelo de IA especialista planificado para el Nivel 3 del sistema de cuatro niveles SLM de PointSav, construido mediante entrenamiento continuo de OLMo 3 32B sobre el corpus federado de aprendizaje de la plataforma.
<!-- END AUTO-GENERATED -->

## Extracción de entidades y el bucle de entrenamiento

Cómo la plataforma convierte el uso en señal de entrenamiento — el mecanismo detrás de "la plataforma aprende de cómo se usa."

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: entity-extraction-and-training-loop -->
- [[tiered-entity-extraction-architecture|Arquitectura de extracción de entidades por niveles]] — La plataforma PointSav ejecuta tres niveles de extracción en secuencia sobre cada documento: el Nivel 0 proporciona detección extractiva rápida vía GLiNER; el Nivel A ofrece una alternativa generativa vía OLMo en CPU; el Nivel B aplica enriquecimiento en GPU y registra las mejoras como señal de entrenamiento.
- [[elastic-compute-lora-training-pipeline|Canalización nocturna de entrenamiento LoRA de Elastic Compute #1]] — Pipeline nocturno de dos fases en Elastic Compute #1 que reconstruye el DataGraph del despliegue y entrena pesos adaptadores LoRA para el modelo de lenguaje local.
- [[learning-datagraph-architecture|DataGraph de aprendizaje]] — Ciclo de entrenamiento que convierte interacciones del operador en señal de entrenamiento — captura de trayectorias, una cola de aprendizaje y un canal de destilación GLiNER→OLMo que genera pares DPO de extracción de entidades.
- [[flow-quality-architecture|Flujo de conocimiento: bucle de entrenamiento y DataGraph ontológico]] — Marco de calidad del flujo de conocimiento Totebox: si los adaptadores LoRA mejoran el modelo de forma medible y si el DataGraph es una ontología precisa y bien resuelta.
<!-- END AUTO-GENERATED -->

## Véase también

- [Cómo Está Construido](/architecture/) — la construcción de tres anillos que hace estructural este límite
- [Componentes básicos](/substrate/) — conceptos de mecanismo relacionados con la IA, incluyendo el artículo de opcionalidad de IA mencionado arriba
- [Servicios de la plataforma](/services/) — las páginas por servicio, incluyendo el propio servicio de IA
