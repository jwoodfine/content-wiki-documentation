---
schema: foundry-doc-v1
title: "El Flujo de Conocimiento: Ciclo de Entrenamiento y DataGraph Ontológico"
slug: flow-quality-architecture
category: architecture
type: concept
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: planned
language_protocol: TRANSLATE-ES
last_edited: 2026-06-28
editor: editorial
short_description: "El flujo de conocimiento del Totebox convierte prosa en dos activos duraderos: un DataGraph ontológico de entidades y adaptadores LoRA que especializan un modelo de lenguaje local. Dos preguntas de calidad determinan si el flujo vale su costo: ¿produce el ciclo de entrenamiento adaptadores que mejoran el modelo de forma medible, y es el DataGraph una ontología precisa y bien resuelta?"
paired_with: flow-quality-architecture.md
cites: []
---

El flujo de conocimiento del Totebox convierte prosa en dos activos duraderos: un **DataGraph ontológico** de entidades y **adaptadores LoRA** que especializan un modelo de lenguaje local. Ambos los sirven `service-slm` (el Doorman) y `service-content` (el DataGraph).

```
prosa ─▶ service-extraction ─▶ CORPUS_*.json
      ─▶ service-content ──▶ GLiNER Nivel 0 (~150ms) ─▶ tramos de entidades
                         └──▶ OLMo Nivel A  (30–137s) ─▶ alternativa si Nivel 0 vacío
                         └──▶ GPU Nivel B   (enriquecimiento) ─▶ vectores rol/ubicación
                         └──▶ grafo LadybugDB
      ◀── el Doorman consulta el grafo por contexto antes de cada inferencia ◀──
corpus de entrenamiento (tuplas de commits + pares de enriquecimiento Nivel-A-vs-B)
      ─▶ TRL SFT / DPO ─▶ adaptador PEFT
```

Dos preguntas de calidad determinan si el flujo vale su costo: ¿produce el **ciclo de entrenamiento** adaptadores que mejoran el modelo de forma medible, y es el **DataGraph** una ontología precisa y bien resuelta en lugar de un montón de fragmentos?

## Cómo se cierra el ciclo (estado previsto)

Un ciclo de entrenamiento sano es un circuito cerrado: corpus → SFT → DPO on-policy → una **compuerta de evaluación** que compara el nuevo adaptador con el vigente sobre un conjunto dorado fijo y versionado → promoción solo ante una mejora medida → el adaptador promovido **servido** en la ruta de inferencia → su comportamiento capturado de vuelta al corpus. La norma de referencia para cada etapa está bien establecida: los adaptadores se acoplan a todas las proyecciones lineales del modelo base y el acoplamiento se verifica tras la construcción; las tasas de aprendizaje superan en un orden de magnitud al ajuste completo; el entrenamiento por preferencias solo corre por encima de un umbral de pares limpios y diversos; y no se promueve ningún adaptador que una sonda base-contra-adaptador no pueda distinguir del modelo base.

## Cómo es coherente la ontología (estado previsto)

Un DataGraph coherente resuelve entidades en cuatro etapas — agrupamiento, similitud, clustering y canonicalización — respaldadas por una tabla de alias para que las variantes superficiales ("Woodfine Management Corp.", "Woodfine Capital Projects") colapsen en una única identidad canónica. Los hechos llevan procedencia (documento fuente, nivel del extractor, confianza, marca de tiempo); los hechos en conflicto se reconcilian en lugar de sobrescribirse; las relaciones son aristas tipadas de una ontología cerrada y direccional; y se conserva el historial para poder leer cualquier hecho "a fecha de" un momento dado.

## Estado objetivo (planificado)

El objetivo previsto, adoptado de forma incremental, son dos ciclos co-evolutivos detrás de un único Doorman, compartiendo un modelo base fijo en hardware soberano.

**El ciclo del DataGraph** está previsto que avance de un grafo de propiedades a uno ontológico sofisticado: una ontología formal versionada (OWL 2 RL) cuyos axiomas permitan a un razonador *derivar* aristas que el extractor nunca escribió; validación SHACL como compuerta de escritura; completado de enlaces por embeddings e inductivo que proponga aristas *candidatas* con puntuación para revisión (nunca auto-publicadas); respuesta a consultas lógicas multi-salto sobre el grafo incompleto; una capa de comunidades para recuperación temática; y una capa de auto-ontologización para que el esquema crezca desde el corpus — todo detrás de un trait `GraphStore`, con procedencia bitemporal para que cualquier hecho sea reproducible "a fecha de".

**El ciclo de entrenamiento** está previsto que corra de forma continua en lugar de por lotes ocasionales: el modelo servido generaría sus propios pares de preferencia on-policy, un objetivo sin modelo de referencia mantendría asequible el entrenamiento perpetuo, una compuerta de evaluación sería la única vía a la promoción, y un adaptador promovido se intercambiaría en caliente en la ruta de inferencia mientras el anterior quedaría en una ranura de reversión — con el entrenamiento programado en el tiempo ocioso del servicio para no privar a las solicitudes interactivas. Un registro de base fijaría un único linaje de modelo base en entrenamiento, política de referencia y servicio, de modo que un adaptador entrenado siempre fuera servible.

Los dos ciclos están previstos para unificarse: el grafo aportaría señal de entrenamiento y el modelo entrenado mejoraría la extracción — un sistema que se auto-alimenta. La ruta por fases y las decisiones que requiere se registran en el brief del plan de construcción del flujo. Este tema describe la arquitectura; el procedimiento operativo se cubre en la guía complementaria.
