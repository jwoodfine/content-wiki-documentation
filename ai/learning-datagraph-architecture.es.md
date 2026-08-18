---
schema: foundry-doc-v1
title: "Grafo de aprendizaje — Cola de aprendizaje, pares DPO y captura de trayectorias"
slug: learning-datagraph-architecture
short_description: "Ciclo de entrenamiento que convierte interacciones del operador en señal de entrenamiento — captura de trayectorias, una cola de aprendizaje y un canal de destilación GLiNER→OLMo que genera pares DPO de extracción de entidades."
language: es
category: ai
type: topic
content_type: topic
index_group: entity-extraction-and-the-training-loop
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-17
editor: pointsav-engineering
cites: []
paired_with: learning-datagraph-architecture.md

---

La plataforma construye un [[compounding-substrate|sustrato acumulativo]]: cada interacción del operador con una sesión de IA se convierte en una tupla de entrenamiento estructurada, enrutada a través de un único límite auditable ([[doorman-protocol|Doorman]]), capturada en un [[worm-ledger-architecture|ledger de solo adición]] y reincorporada al SLM local mediante ajuste fino periódico. El resultado es un entorno de desarrollo que aprende de cómo se usa — las sugerencias de código se acercan a los patrones que escribe este operador, las propuestas de borrador se alinean más con la voz editorial de esta casa, las extracciones de entidades se afinan a medida que el grafo se enriquece.

## Puntos clave

- El sustrato acumula señal de entrenamiento mediante varios mecanismos distintos: captura de trayectorias al cierre de sesión, una cola de aprendizaje que se activa en cada confirmación, y un canal de destilación GLiNER→OLMo que produce pares DPO de extracción de entidades.
- Toda la señal de entrenamiento pasa por el mismo límite auditable — [[doorman-protocol|Doorman]] — y aterriza en el ledger de solo adición. Las consultas al grafo que se hacen en este bucle están delimitadas por inquilino en ese mismo límite.
- Las cifras específicas del corpus (número de tuplas, número de pares) cambian con demasiada frecuencia para publicar aquí una cifra fiable.
- `POST /v1/draft/generate` es real, está construido y en producción. Su propio comentario de documentación lo llama "Tier C Drafting Pipeline" y hace proxy hacia **Claude Haiku 4.5**.

## Mecanismos de señal de entrenamiento

**Captura de trayectorias.** Un hook de cierre de sesión se activa al final de cada sesión y publica un resumen de sesión en texto libre envuelto en un esquema JSON de brief de aprendizaje (`brief_id`/`senior_role`/`task_type`/`body`).

**Cola de aprendizaje.** Un hook post-commit dispara un brief "shadow" para confirmaciones en 8 clústeres. El modelo local en este bucle es **OLMo 3**.

**El mecanismo DPO es destilación GLiNER→OLMo.** GLiNER (extracción de Nivel 0) propone entidades, se le pide a OLMo 7B (Nivel A) que reproduzca o mejore la extracción, y la diferencia se convierte en un par DPO — una señal de calidad de extracción de entidades, distinta de una señal de entrenamiento de voz editorial.

**Destilación de trayectorias negativas.** Un script de análisis de buzones lee las correcciones del operador de los mensajes archivados y emite señales de trayectoria negativa en el corpus de retroalimentación.

## El bucle de entidades estructuradas, y su comportamiento de alcance por inquilino

`POST /v1/draft/generate` fundamenta la generación en entidades del grafo — consulta el grafo y un subgrafo de aristas inducido antes de llamar hacia afuera. Lo que **no** hace: llamar a un planificador LoRA ni activar el cómputo GPU de Nivel B. Es una llamada síncrona de auditoría-proxy del Doorman hacia un modelo en la nube (Claude Haiku 4.5, véase arriba), punto final.

Toda consulta al grafo que hace este endpoint está sujeta a la misma aplicación de aislamiento por inquilino descrita en [[doorman-protocol]] — `graph_query`/`graph_mutate` se limitan estrictamente al módulo propio del solicitante, sin fusión entre inquilinos. Un borrador de entidades estructuradas para un inquilino no puede fundamentarse en las entidades del grafo de otro inquilino, de modo que la propiedad intelectual del grafo de un cliente nunca se agrega entre inquilinos sin consentimiento explícito.

El sustrato se acumula en dos direcciones en principio: estructuralmente (la densidad de citas y las cadenas de supersedencia se enriquecen con cada borrador) y generativamente (cada adaptador eleva el nivel del "crudo" para que el refinamiento comience más cerca de lo publicable) — la mitad generativa depende del canal de entrenamiento LoRA descrito en [[elastic-compute-lora-training-pipeline]].

## Véase también

- [[compounding-substrate]] — la disciplina de sustrato que esta arquitectura instancia
- [[service-slm]] — el servicio SLM local que ejecuta la inferencia del modelo en el bucle
- [[totebox-session]] — el modelo de sesión que la captura de trayectorias instrumenta al final de cada sesión
- [[mailbox-atomicity]] — la disciplina de escritura atómica que protege el ledger de auditoría de condiciones de carrera
