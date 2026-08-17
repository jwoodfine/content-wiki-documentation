---
schema: foundry-doc-v1
title: "Grafo de aprendizaje — Cola de aprendizaje, pares DPO y captura de trayectorias"
slug: learning-datagraph-architecture
short_description: "Ciclo de entrenamiento que convierte interacciones del operador en señal de entrenamiento — captura de trayectorias, cola de aprendizaje y un canal real de destilación GLiNER→OLMo (no la vía DPO editorial que versiones anteriores de este artículo describían)."
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

- El sustrato acumula señal de entrenamiento mediante varios mecanismos distintos: captura de trayectorias al cierre de sesión, una cola de aprendizaje que se activa en cada confirmación, y un canal real de destilación GLiNER→OLMo — no la vía "DPO editorial de embudo inverso" que versiones anteriores de este artículo describían, la cual no tiene respaldo en el código.
- Toda la señal de entrenamiento pasa por el mismo límite auditable — [[doorman-protocol|Doorman]] — y aterriza en el ledger de solo adición. La verificación del alcance por inquilino de esta misma sesión (véase abajo) es un ejemplo real de ese límite siendo aplicado, no solo descrito.
- Las cifras específicas del corpus (número de tuplas, número de pares) no se repiten aquí — las únicas cifras verificadas de forma independiente en esta revisión están fechadas el 2026-04-29 y ya están desactualizadas (14 archivos de aprendizaje, un corpus de retroalimentación vacío); citar un número que suene más reciente sin una verificación reciente sería peor que no citar ninguno.
- `POST /v1/draft/generate` es real, está construido y en producción — `service-content/src/http.rs:352-479` (no las líneas `176-280` citadas antes), confirmado por lectura directa, no solo por el código de estado de una prueba en vivo. Su propio comentario de documentación lo llama "Tier C Drafting Pipeline" y hace proxy hacia **Claude Haiku 4.5** (`anthropic:claude-haiku-4-5-20251001`) — no Claude 3.5 Sonnet como afirmaba una corrección anterior. No existe ningún `service-content/CLAUDE.md` en ninguna parte del monorepo; esa cita fue fabricada junto con la afirmación sobre la versión del modelo.

## Mecanismos de señal de entrenamiento

**Captura de trayectorias.** Un hook de cierre de sesión se activa al final de cada sesión. El verdadero `capture-trajectory.sh` publica un resumen de sesión en texto libre envuelto en un esquema JSON de brief de aprendizaje (`brief_id`/`senior_role`/`task_type`/`body`) — no un conjunto fijo de campos de estado de rama/recuento de archivos/SHA como afirmaba texto anterior.

**Cola de aprendizaje.** Un hook post-commit dispara un brief "shadow" vía `POST /v1/shadow` para confirmaciones en 8 clústeres — el intervalo específico de "drenador de 15 minutos" de texto anterior no tiene respaldo en el código ni en `service-slm/docs/trainer-scoping.md`, la documentación real más cercana a este mecanismo. El modelo local en este bucle es **OLMo 3** (`OLMo-3-7B-Q4_K_M.gguf`, `slm-doorman/src/tier/local.rs`; también `olmo-3-1125-7b-q4` en `slm-core/src/apprenticeship.rs`) — no "OLMo-2 7B Q4"; no existe ninguna referencia a un modelo OLMo-2 en ninguna parte del código.

**El mecanismo DPO real es destilación GLiNER→OLMo, no pares editoriales de embudo inverso.** `service-content/src/lib.rs` (`write_gliner_olmo_dpo_pair`, alrededor de las líneas 279–282 y 659–690) muestra el verdadero canal DPO: GLiNER (extracción de Nivel 0, `:9085`) propone entidades, se le pide a OLMo 7B (Nivel A) que reproduzca o mejore la extracción, y la diferencia se convierte en un par DPO — una señal de calidad de extracción de entidades, no una señal de voz editorial proveniente de un canal "crudo → refinado → editado creativamente". No existe tal mecanismo de embudo inverso hacia pares DPO en el código; el texto anterior que describía uno no estaba fundamentado en el código base.

**Destilación de trayectorias negativas.** Un script de análisis de buzones lee las correcciones del operador de los mensajes archivados y emite señales de trayectoria negativa en el corpus de retroalimentación — no reverificado de forma independiente en esta revisión; se mantiene como se describía antes, sin reconfirmar.

## El bucle de entidades estructuradas, y el comportamiento de alcance por inquilino que realmente tiene

`POST /v1/draft/generate` efectivamente fundamenta la generación en entidades del grafo — consulta `state.graph.query_context` y un subgrafo de aristas inducido antes de llamar hacia afuera, lo cual coincide con la descripción de "fundamenta la generación en entidades del grafo". Lo que **no** hace: llamar a un planificador LoRA ni activar el cómputo GPU de Nivel B. Texto anterior afirmaba que "un planificador LoRA activa luego el cómputo GPU de Nivel B para el entrenamiento nocturno de adaptadores" en un paso posterior a este endpoint — no existe tal conexión en `draft_generate`; es una llamada síncrona de `/v1/audit/proxy` del Doorman hacia un modelo en la nube (Claude Haiku 4.5, véase arriba), punto final.

**No documentado antes en absoluto, a pesar de ser fundamental:** toda consulta al grafo que hace este endpoint está sujeta a la misma aplicación de aislamiento por inquilino descrita en [[doorman-protocol]] — `graph_query`/`graph_mutate` se limitan estrictamente al módulo propio del solicitante, sin fusión entre inquilinos, desde que la corrección se confirmó en producción el 2026-07-28. Un borrador de entidades estructuradas para un inquilino no puede fundamentarse en las entidades del grafo de otro inquilino. Esto importa exactamente por la razón de la reivindicación #48 de la DOCTRINA que [[doorman-protocol]] cubre con más detalle — la propiedad intelectual del grafo del cliente nunca se agrega entre inquilinos sin consentimiento explícito — y aplica aquí aunque el texto anterior de este artículo nunca lo haya mencionado.

El sustrato se acumula en dos direcciones en principio: estructuralmente (la densidad de citas y las cadenas de supersedencia se enriquecen con cada borrador) y generativamente (cada adaptador eleva el nivel del "crudo" para que el refinamiento comience más cerca de lo publicable) — la mitad generativa depende del canal de entrenamiento LoRA descrito en [[elastic-compute-lora-training-pipeline]], que este artículo no verifica por sí mismo.

## Véase también

- [[compounding-substrate]] — la disciplina de sustrato que esta arquitectura instancia
- [[service-slm]] — el servicio SLM local que ejecuta la inferencia del modelo en el bucle
- [[totebox-session]] — el modelo de sesión que la captura de trayectorias instrumenta al final de cada sesión
- [[mailbox-atomicity]] — la disciplina de escritura atómica que protege el ledger de auditoría de condiciones de carrera
