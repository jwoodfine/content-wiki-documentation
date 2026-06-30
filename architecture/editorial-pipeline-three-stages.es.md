---
title: "La canalización editorial de tres etapas"
slug: editorial-pipeline-three-stages
category: architecture
last_edited: 2026-06-29
editor: pointsav-engineering
status: stable
---

La **canalización editorial de tres etapas** es la secuencia de procesamiento que
`service-proofreader` aplica a cada solicitud `/v1/proofread`. Cada etapa es independiente,
tiene una forma de entrada definida y produce un conjunto estructurado de hallazgos. Las etapas
se ejecutan en orden: primero reglas deterministas baratas, luego análisis gramatical mecánico
y finalmente reescritura generativa. La racionalidad de disciplina de costes es directa: la
Etapa 1 termina la solicitud anticipadamente ante infracciones claras; los hallazgos mecánicos
de la Etapa 2 se incorporan al indicador de la Etapa 3, evitando que el modelo redescubra
errores que el paso de reglas ya catalogó.

## Por qué tres etapas, en este orden

El orden refleja tres perfiles distintos de coste y fiabilidad. La Etapa 1 es determinista y
no tiene dependencia externa; se completa en tiempo de submilisegundo y no puede fallar por
infraestructura. La Etapa 2 llama a una instancia de LanguageTool desplegada localmente y
puede degradarse sin error si ese servicio no está disponible. La Etapa 3 enruta a través del
Doorman hacia uno de tres niveles de cómputo y es la única etapa sujeta a variación de latencia
y coste.

Cada etapa produce un conjunto de hallazgos verificable de forma independiente. Un operador que
revise una respuesta `/v1/proofread` puede atribuir cada señal a la etapa que la produjo: un
acierto de vocabulario prohibido de la Etapa 1 tiene una autoridad diferente a una sugerencia
de estilo de la Etapa 3.

## Etapa 1 — Análisis de vocabulario prohibido (determinista, basado en reglas)

La Etapa 1 es un análisis de texto puro contra las listas de vocabulario prohibido. Se definen
cuatro familias de género — PROSE, COMMS, LEGAL y TRANSLATE — cada una con su propia lista de
términos no permitidos, vocabulario de marketing de productos de IA y frases de cobertura
vagas. Una coincidencia produce una señal `Severity::Banned` con el tramo coincidente, la
familia que activó la coincidencia y una sugerencia de reemplazo cuando existe. La Etapa 1
solo señala; nunca reescribe.

## Etapa 2 — Paso mecánico de LanguageTool 6.6 (compañero Docker)

La Etapa 2 llama a la API HTTP de LanguageTool 6.6 que se ejecuta como servicio compañero
Docker coubicado con el binario del corrector. LanguageTool maneja ortografía, gramática,
puntuación y reglas de estilo demasiado numerosas para enumerarlas como lista estática. La
respuesta se normaliza: cada coincidencia de regla de LanguageTool se mapea al tipo interno
`Finding` del corrector, se le asigna `Severity::Mechanical` y se anota con el tramo
coincidente, el identificador de regla y el reemplazo sugerido. El conjunto completo de
hallazgos de la Etapa 2 se serializa a JSON para el consumo de la Etapa 3.

## Etapa 3 — Paso generativo del Doorman (service-SLM via Niveles A/B/C)

La Etapa 3 enruta a través del Doorman (service-slm) hacia uno de tres niveles de cómputo:
Nivel A (OLMo 3 7B Q4 ejecutándose localmente), Nivel B (OLMo 3.1 32B en ráfaga de GPU en la
nube) o Nivel C (punto de conexión de API externo). El Doorman selecciona el nivel según la
forma de la solicitud, la profundidad de la cola y el límite de presupuesto configurado. La
salida es una reescritura completa del texto.

## Cómo los hallazgos de la Etapa 2 fluyen hacia la Etapa 3 como JSON en línea

El conjunto de hallazgos de la Etapa 2 se incorpora directamente en el indicador del Doorman
de la Etapa 3 como un bloque de anotación JSON estructurado. Cada entrada en el bloque incluye
los desplazamientos del tramo coincidente, el ID de regla de LanguageTool, el reemplazo
sugerido y el discriminante `Severity::Mechanical`. La incorporación en línea se prefiere sobre
un punto de conexión de inyección de contexto separado porque mantiene la entrada de la Etapa 3
autocontenida y auditable.

## Severidad por señal en el hilo

La respuesta `/v1/proofread` lleva un array `findings`. Cada entrada tiene un discriminante
`severity`: `Banned` (Etapa 1), `Mechanical` (Etapa 2) o `Generative` (Etapa 3, reservado).
Los llamadores usan la severidad para tomar decisiones de interfaz: los hallazgos `Banned`
resaltan automáticamente y bloquean el envío; los hallazgos `Mechanical` se muestran en línea
pero son contraíbles.

## El veredicto del operador cierra el ciclo de aprendizaje

Después de revisar la reescritura de la Etapa 3, el operador registra una de tres disposiciones
mediante `/v1/verdict`: `accepted`, `rejected` o `edited` (con el texto final de su elección).
El veredicto y los textos asociados forman una tupla de par de eventos —
`draft-created` → `draft-refined` → `creative-edited` — que alimenta el corpus de aprendizaje
para el refinamiento continuo del modelo.

## Cuando las etapas se degradan de forma controlada

Si el compañero Docker de LanguageTool de la Etapa 2 no está disponible, la canalización
continúa hacia la Etapa 3 con un conjunto de hallazgos mecánicos vacío; los metadatos de la
respuesta llevan `mechanical_pass: false`. Si el Doorman de la Etapa 3 no puede alcanzar
ningún nivel de cómputo dentro del tiempo de espera configurado, la canalización devuelve
solo los hallazgos de las Etapas 1 y 2, con `generative_pass: false`. En ambos casos
degradados, la respuesta sigue siendo válida.

## Véase también

- [[language-protocol-substrate]] — las cuatro familias de género y las listas de vocabulario
  de las que se nutre la Etapa 1; artículo complementario
- [[customer-tier-catalog-pattern]] — cómo se provisiona la instancia de despliegue del
  corrector para ejecutar esta canalización; artículo complementario
