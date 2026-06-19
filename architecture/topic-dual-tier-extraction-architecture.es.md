---
schema: foundry-doc-v1
title: "Arquitectura de Extracción de Entidades en Dos Niveles"
slug: topic-dual-tier-extraction-architecture
category: architecture
type: concept
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: current-fact
language_protocol: TRANSLATE-ES
last_edited: 2026-06-19
editor: editorial
short_description: "La canalización de extracción de entidades de PointSav opera en dos niveles de inferencia en secuencia: el Nivel A en hardware de CPU local proporciona una extracción de referencia; el Nivel B en GPU ofrece un pase de mayor capacidad y registra la mejora como señal de entrenamiento."
paired_with: topic-dual-tier-extraction-architecture.md
cites: []
---

La canalización de extracción de entidades de PointSav opera en dos niveles de inferencia de forma secuencial sobre cada documento. El Nivel A proporciona una extracción de referencia en hardware de CPU local. El Nivel B aplica un pase de mayor capacidad mediante GPU cuando está disponible y registra la mejora como señal de entrenamiento para el refinamiento futuro del modelo.

## Nivel A — Inferencia local

El Nivel A enruta las cargas útiles de documentos a OLMo 7B, que se ejecuta en la CPU del VM de trabajo a través del punto de acceso `/v1/chat/completions` del Guardián. Un servicio de inferencia local dedicado mantiene este nivel disponible sin dependencias externas.

La extracción utiliza un indicador estructurado que limita al modelo a cinco clasificaciones de entidades: Persona, Empresa, Proyecto, Cuenta y Ubicación. Un filtro de clasificación a nivel de módulo en el servicio de extracción rechaza cualquier clasificación de salida fuera de este vocabulario antes de que el resultado llegue al almacén del grafo, previniendo la deriva taxonómica causada por salidas no controladas del modelo.

La clasificación de Ubicación lleva una definición restrictiva —un lugar geográfico nombrado específico o una dirección— con ejemplos negativos explícitos en el indicador del sistema que excluyen sustantivos espaciales genéricos. Los identificadores de licencia SPDX y otras cadenas técnicas se excluyen a nivel del indicador.

## Nivel B — Inferencia mediante GPU

El Nivel B enruta a través del punto de acceso `/v1/extract` del Guardián hacia OLMo 32B, ejecutándose en un nodo GPU L4. Cuando el circuito del Nivel B está cerrado y el nodo informa como activo, el Guardián reenvía la misma carga útil del documento para un segundo pase de extracción de mayor capacidad.

Los resultados del Nivel B se comparan con la referencia del Nivel A. El par se registra en el corpus de retroalimentación de OPD (Optimización de Preferencias Directas): la salida del Nivel B es la respuesta preferida y la salida del Nivel A es la respuesta rechazada. Este corpus se acumula durante las ejecuciones de extracción en vivo y está previsto para el ajuste fino futuro del modelo bajo el ciclo de entrenamiento Yo-Yo.

Un análisis de 32 pares de enriquecimiento de OPD producidos el 2026-06-14 encontró que el Nivel B extrajo más entidades que el Nivel A en el 78 % de los casos, menos en el 6 % e igual cantidad en el 16 %.

## Predicado de Retención de Vaciado

La cola de vaciado de aprendizaje del Guardián mantiene trabajos de entrenamiento pendientes. Cuando ambos niveles están disponibles, la extracción y el entrenamiento avanzan en paralelo. Un indicador de retención de vaciado puede pausar la cola de aprendizaje para evitar que la GPU reciba una cola agotada que haya sido procesada íntegramente por el Nivel A durante una interrupción de la GPU.

El predicado está diseñado para activarse automáticamente cuando el Nivel B ha estado fuera de línea por más tiempo que un umbral configurado. La implementación actual tiene una limitación conocida: no detecta la condición en que un nodo GPU informa `health_up: false` pero el circuito del Guardián permanece cerrado. Está previsto añadir un campo `down_for_secs` en la estructura de información del nivel para resolver esto.

## Comportamiento de Vaciado Cuando el Nivel B No Está Disponible

Cuando el Nivel A completa la extracción y el circuito del Nivel B está abierto, el documento se marca como procesado exitosamente y las entidades del Nivel A se escriben en el almacén del grafo. El documento no se reprocesará para un pase de enriquecimiento del Nivel B — el par de retroalimentación de OPD se omite de forma permanente para ese documento.

Para interrupciones breves de la GPU, este comportamiento es intencional. Para interrupciones prolongadas, el predicado de retención de vaciado está previsto para preservar documentos para el enriquecimiento futuro del Nivel B pausando la cola de aprendizaje antes de que el Nivel A procese todos los documentos pendientes.

## Almacén del Grafo

Las entidades extraídas por cualquiera de los dos niveles se escriben en LadybugDB. Las entidades se indexan por identificador de módulo y nombre de entidad; los duplicados dentro de un módulo se actualizan por inserción. El servicio de extracción registra los documentos procesados en un registro de procesamiento para evitar la reextracción al reiniciar el servicio.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
