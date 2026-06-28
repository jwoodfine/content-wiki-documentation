---
schema: foundry-doc-v1
title: "Arquitectura de Extracción de Entidades por Niveles"
slug: topic-tiered-entity-extraction-architecture
category: architecture
type: concept
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: current-fact
language_protocol: TRANSLATE-ES
last_edited: 2026-06-28
editor: editorial
short_description: "La plataforma PointSav ejecuta tres niveles de extracción en secuencia sobre cada documento: el Nivel 0 proporciona detección extractiva rápida vía GLiNER; el Nivel A ofrece una alternativa generativa vía OLMo en CPU; el Nivel B aplica enriquecimiento en GPU y registra las mejoras como señal de entrenamiento."
paired_with: topic-tiered-entity-extraction-architecture.md
aliases:
  - topic-dual-tier-extraction-architecture
cites: []
---

La plataforma PointSav ejecuta tres niveles de extracción en secuencia sobre cada documento. El Nivel 0 proporciona detección extractiva rápida en CPU. El Nivel A ofrece una alternativa generativa cuando el Nivel 0 no está disponible. El Nivel B aplica un pase de enriquecimiento de mayor capacidad en GPU y registra las mejoras como señal de entrenamiento.

## Nivel 0 — Detección Extractiva (GLiNER)

El Nivel 0 envía los documentos a `service-gliner`, un microservicio de reconocimiento de entidades nombradas GLiNER que se ejecuta localmente en la VM. GLiNER es un modelo basado en el codificador BERT que lee un tramo de texto y devuelve los tramos de entidades con sus clasificaciones. Es puramente extractivo: sólo puede devolver tramos que aparecen literalmente en el texto de entrada y no puede generar ni inferir nombres que no estén presentes.

La latencia típica en CPU es de 130 a 208 milisegundos por documento, dos o tres órdenes de magnitud más rápido que la inferencia generativa.

Los documentos se truncan en un límite de oración cercano a los 2.000 caracteres antes de su envío. El codificador BERT opera con un contexto fijo de 512 tokens; el texto en el límite de 2.000 caracteres ocupa aproximadamente 480 tokens, dejando margen para las cadenas de descripción de etiquetas sin truncación. El contenido más allá de este límite no se envía al Nivel 0. La segmentación de artículos (planificada) abordará la recuperación de entidades en la segunda mitad de documentos largos.

Las etiquetas se expresan como descripciones en lenguaje natural. El identificador de dominio del documento selecciona el conjunto de etiquetas:

- `projects` — contenido de inversión inmobiliaria y propiedades comerciales. Reconoce Persona, Empresa, Proyecto (desarrollos, edificios, fondos), Ubicación y Cuenta.
- `corporate` — contenido organizacional general. Reconoce Persona, Empresa, Proyecto, Ubicación y Cuenta.
- `documentation` — contenido técnico y de ingeniería. Reconoce Persona, Empresa, Proyecto (proyectos de software), Ubicación y Cuenta.

Cuando el Nivel 0 devuelve una lista de entidades vacía, el flujo pasa al Nivel A. Una respuesta vacía de un servicio Nivel 0 bien funcionando es esperada y normal para archivos de datos estructurados, código fuente y otras entradas que no son prosa.

## Nivel A — Alternativa Generativa (OLMo)

El Nivel A envía los documentos a OLMo 7B ejecutándose en CPU a través del endpoint `/v1/chat/completions` del Doorman. El Nivel A se activa cuando el Nivel 0 es inalcanzable o devuelve una lista vacía de entidades.

La extracción utiliza un prompt estructurado que restringe el modelo a las mismas cinco clasificaciones de entidades que usa el Nivel 0. Cuando las restricciones gramaticales están habilitadas, el modelo se ve obligado a emitir JSON válido conforme al esquema de extracción, eliminando los rechazos por violación de esquema. La llamada de inferencia utiliza `temperature: 0.0` para producir resultados deterministas y `cache_prompt: true` para permitir la reutilización del caché KV entre llamadas consecutivas de extracción con el mismo prompt de sistema.

La latencia del Nivel A en CPU oscila entre 30 y 137 segundos por documento según la longitud del documento y la carga concurrente. Cuando la cola de aprendiz del Doorman está activa, los slots del Nivel A pueden estar ocupados y las llamadas de extracción interactivas se pondrán en cola.

## Nivel B — Enriquecimiento en GPU

El Nivel B enruta a través del endpoint `/v1/extract` del Doorman hacia un nodo de inferencia en GPU. Cuando el circuito del Nivel B está cerrado y el nodo reporta estado saludable, el Doorman reenvía el documento para un segundo pase de enriquecimiento de mayor capacidad.

Los resultados del Nivel B pasan por el mismo filtro de clasificación de entidades que los del Nivel 0 y Nivel A. Cuando el Nivel B tiene éxito estructuralmente pero todas las entidades devueltas fallan el filtro — una condición que surge cuando las restricciones gramaticales no están aplicadas en la ruta del Nivel B — el flujo aplica un comportamiento de rescate: utiliza el conjunto de entidades del Nivel 0 con una confianza reducida en lugar de escribir cero entidades en el grafo. El documento se marca para reintento de Nivel B para que una ejecución posterior pueda producir resultados enriquecidos cuando la aplicación de gramática esté disponible.

Los resultados del Nivel B y su referencia del Nivel A se registran como un par de retroalimentación DPO (Optimización por Preferencia Directa) para el ajuste fino futuro del modelo bajo el ciclo de entrenamiento Yo-Yo.

## Ruta de Escritura al Grafo

Las entidades producidas por el nivel que genera el resultado aceptado se escriben en LadybugDB. Las entidades se identifican por módulo y nombre; los duplicados dentro de un módulo se actualizan mediante upsert. Se emite un punto de control después de cada lote de escritura para garantizar que las entidades escritas por el hilo de drenaje sean inmediatamente visibles para las consultas HTTP de lectura, que se ejecutan en un contexto de tiempo de ejecución separado.

El servicio de extracción registra los documentos procesados en un libro de contabilidad JSONL para evitar la re-extracción al reiniciar el servicio.

## Contrapresión

Cuando el Doorman reporta una profundidad de cola que supera el umbral configurado y el Nivel 0 no está disponible, los documentos que caerían únicamente al Nivel A se difieren en lugar de procesarse. Esto evita que el retraso de documentos se marque permanentemente como procesado con baja calidad durante una interrupción del Nivel 0.

Los documentos para los que el Nivel 0 devuelve una lista de entidades no vacía siempre proceden al enriquecimiento del Nivel B independientemente de la profundidad de la cola.

## Resumen por Niveles

| Nivel | Servicio | Método | Latencia típica | Se activa cuando |
|---|---|---|---|---|
| 0 | service-gliner (GLiNER) | Detección extractiva | 130–208 ms | Por defecto — primera vía |
| A | service-slm (OLMo 7B CPU) | Completado generativo | 30–137 s | Nivel 0 no disponible o vacío |
| B | service-slm (nodo GPU) | Enriquecimiento generativo | 10–30 s | Circuito cerrado + nodo saludable |
