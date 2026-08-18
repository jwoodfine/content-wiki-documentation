---
schema: foundry-doc-v1
title: "Flujo de conocimiento: ciclo de entrenamiento y DataGraph ontológico"
slug: flow-quality-architecture
category: ai
type: concept
content_type: topic
quality: complete
index_group: entity-extraction-and-the-training-loop
status: active
audience: vendor-public
bcsc_class: planned
language_protocol: TRANSLATE-ES
last_edited: 2026-08-17
editor: editorial
short_description: "Marco de calidad del flujo de conocimiento Totebox: si los adaptadores LoRA mejoran el modelo de forma medible y si el DataGraph es una ontología precisa y bien resuelta."
paired_with: flow-quality-architecture.md
cites: []

---

El flujo de conocimiento del Totebox convierte prosa en dos activos duraderos: un **[[ontological-datagraph|DataGraph ontológico]]** de entidades y **adaptadores LoRA** que especializan un modelo de lenguaje local. Ambos los sirven `service-slm` (el [[doorman-protocol|Doorman]]) y `service-content` (el DataGraph).

```
prosa ─▶ service-extraction ─▶ CORPUS_*.json
      ─▶ service-content ──▶ GLiNER Nivel 0 (rápido — sin cifra publicada; cualitativamente "~150x más rápido que OLMo") ─▶ tramos de entidades
                         └──▶ OLMo Nivel A  (alternativa, latencia no publicada) ─▶ alternativa de extracción (Nivel 0 inalcanzable) + tarea asíncrona de entrenamiento
                         └──▶ GPU Nivel B   (enriquecimiento) ─▶ vectores rol/ubicación
                         └──▶ grafo LadybugDB
      ◀── el Doorman consulta el grafo por contexto antes de cada inferencia ◀──
corpus de entrenamiento (tuplas de commits + pares de enriquecimiento Nivel-A-vs-B)
      ─▶ TRL SFT / DPO ─▶ adaptador PEFT
```

La ruta de éxito del Nivel 0 encola un `TierAJob` para una pasada asíncrona de *entrenamiento* del Nivel A. La generación de pares DPO ocurre después, más adelante en la cadena, no en esta cola.

Dos preguntas de calidad determinan si el flujo vale su costo: ¿produce el **ciclo de entrenamiento** adaptadores que mejoran el modelo de forma medible, y es el **DataGraph** una ontología precisa y bien resuelta en lugar de un montón de fragmentos?

## Cómo se cierra el ciclo (estado previsto)

Un ciclo de entrenamiento sano es un circuito cerrado: corpus → SFT → DPO on-policy → una compuerta de evaluación → promoción solo ante una mejora medida → el adaptador promovido **servido** en la ruta de inferencia → su comportamiento capturado de vuelta al corpus. Varias etapas son reales y confirmadas: los adaptadores se acoplan a todas las proyecciones lineales del modelo base y el acoplamiento se verifica tras la construcción (una comprobación de fallo-cerrado sobre la lista exacta de módulos objetivo, en los scripts de entrenamiento SFT y DPO); las tasas de aprendizaje superan en un orden de magnitud al ajuste completo (2e-4 frente a un valor por defecto declarado de 2e-5 para ajuste completo); el entrenamiento por preferencias solo corre por encima de un umbral de pares limpios y diversos (una constante real `CLEAN_PAIR_FLOOR = 3000`, más compuertas de calidad por par); y no se promueve ningún adaptador que una sonda base-contra-adaptador no pueda distinguir del modelo base (un script real de compuerta de despliegue implementa exactamente esta comprobación).

La compuerta de evaluación no compara el nuevo adaptador con un adaptador vigente sobre un conjunto dorado fijo y versionado — no existe tal comparación ni tal conjunto dorado. La compuerta puntúa las propias completions del adaptador contra un umbral fijo de tasa de aprobación — corrección de diff-parse / git-apply / formato de sobre — sobre un 10% de retención barajado aleatoriamente, dividido de nuevo en cada ejecución.

## Cómo es coherente la ontología (estado previsto)

Se prevé que un DataGraph coherente resuelva entidades mediante etapas de agrupamiento, similitud y canonicalización, para que las variantes superficiales ("MCorp", "Woodfine Capital Projects") colapsen en una única identidad canónica. Lo que está construido hoy es más limitado: la resolución de entidades implementa tres etapas, no cuatro — agrupamiento → similitud → bandas de decisión (auto-fusión / revisión / nuevo) — sin ninguna etapa de clustering. La tabla de alias que respaldaría la canonicalización explícitamente aún no está implementada; el propio comentario del módulo la describe como "una migración aditiva aplicada por separado". La resolución de entidades hoy es pura y sin efectos secundarios, todavía no respaldada por el mecanismo de alias que describe esta sección.

Los hechos llevan procedencia parcial: existe un campo real `confidence` y un campo real `source_doc` en cada entidad del grafo, con `source_doc` de tipo primero-en-escribir-gana — pero no existe ningún campo `extractor_tier`, así que la procedencia todavía no captura qué nivel (GLiNER, OLMo o GPU) produjo un hecho dado. El manejo de conflictos es mixto, no uniformemente "reconciliado en lugar de sobrescrito": los campos vectoriales usan una fusión de nuevo-gana-si-está-presente y `source_doc` es primero-en-escribir-gana, pero `confidence` se sobrescribe incondicionalmente en cada escritura — el campo pensado más directamente para señalar confianza es precisamente el que no se reconcilia en absoluto. Las relaciones sí son genuinamente aristas tipadas y direccionales de una ontología cerrada (un vocabulario real de tipos de relación cargado desde un archivo CSV) — esta parte es precisa tal como se describe.

El historial a fecha — poder leer cualquier hecho "a fecha de" un momento dado — no está construido. Está planificado; véase Estado objetivo, más abajo.

## Estado objetivo (planificado)

El objetivo previsto, adoptado de forma incremental, son dos ciclos co-evolutivos detrás de un único Doorman, compartiendo un modelo base fijo en hardware soberano.

**El ciclo del DataGraph** está previsto que avance de un grafo de propiedades a uno ontológico sofisticado: una ontología formal versionada (OWL 2 RL) cuyos axiomas permitan a un razonador *derivar* aristas que el extractor nunca escribió; validación SHACL como compuerta de escritura; completado de enlaces por embeddings e inductivo que proponga aristas *candidatas* con puntuación para revisión (nunca auto-publicadas); respuesta a consultas lógicas multi-salto sobre el grafo incompleto; una capa de comunidades para recuperación temática; y una capa de auto-ontologización para que el esquema crezca desde el corpus — todo detrás de un trait `GraphStore`, con procedencia bitemporal para que cualquier hecho sea reproducible "a fecha de".

**El ciclo de entrenamiento** está previsto que corra de forma continua en lugar de por lotes ocasionales: el modelo servido generaría sus propios pares de preferencia on-policy, un objetivo sin modelo de referencia mantendría asequible el entrenamiento perpetuo, una compuerta de evaluación sería la única vía a la promoción, y un adaptador promovido se intercambiaría en caliente en la ruta de inferencia mientras el anterior quedaría en una ranura de reversión — con el entrenamiento programado en el tiempo ocioso del servicio para no privar a las solicitudes interactivas. Un registro de base fijaría un único linaje de modelo base en entrenamiento, política de referencia y servicio, de modo que un adaptador entrenado siempre fuera servible.

Los dos ciclos están previstos para unificarse: el grafo aportaría señal de entrenamiento y el modelo entrenado mejoraría la extracción — un sistema que se auto-alimenta. La ruta por fases y las decisiones que requiere se registran en el brief del plan de construcción del flujo. Este tema describe la arquitectura; el procedimiento operativo se cubre en la guía complementaria.
