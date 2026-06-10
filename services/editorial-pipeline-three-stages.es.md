---
schema: foundry-doc-v1
title: "El Proceso Editorial en Tres Etapas"
slug: editorial-pipeline-three-stages
category: services
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-06-10
editor: pointsav-engineering
paired_with: editorial-pipeline-three-stages.md
---

`service-proofreader` procesa cada solicitud `/v1/proofread` a través de tres etapas discretas ejecutadas en secuencia. Cada etapa es verificable de forma independiente y dispone de un camino de degradación definido cuando su dependencia no está disponible. El orden va de lo más económico a lo más costoso: las comprobaciones deterministas baratas se ejecutan primero para que la inferencia costosa nunca reciba entradas que una pasada de reglas ya podría haber resuelto.

## Por Qué Tres Etapas, en Este Orden

Tres principios guían el orden.

*Disciplina de costos.* La Etapa 1 es determinista y se completa en tiempo por debajo del milisegundo para cualquier longitud de entrada. La Etapa 2 llama a un servicio lingüístico alojado localmente. La Etapa 3 enruta a través de la capa de inferencia hacia un nivel de cómputo que puede implicar capacidad de GPU o una API externa. Si la Etapa 1 detecta una violación de vocabulario prohibido suficientemente grave, el procesamiento se detiene y retorna antes de que cualquier pasada lingüística sea apropiada. La inferencia costosa nunca recibe entradas que las etapas anteriores ya habrían manejado.

*Corrección.* La Etapa 2 aplica cientos de reglas gramaticales y de estilo con salida consistente. Cuando la Etapa 3 recibe el documento, el conjunto de hallazgos de la Etapa 2 está integrado en el prompt como contexto editorial. El modelo de inferencia encuentra el documento con los errores mecánicos conocidos ya anotados, en lugar de descubrirlos de forma inconsistente en cada pasada.

*Auditabilidad.* Cada etapa emite un conjunto estructurado de hallazgos verificable de forma independiente. La respuesta completa del proceso incluye hallazgos de las tres etapas, cada uno atribuido a su fuente.

## Etapa 1 — Análisis de Vocabulario Prohibido

La Etapa 1 analiza el texto de entrada contra las listas de vocabulario del espacio de trabajo, compiladas por familia de protocolo lingüístico: las familias PROSE, COMMS, LEGAL y TRANSLATE llevan conjuntos de términos distintos apropiados para sus géneros registrados.

Una coincidencia produce un hallazgo con severidad `Banned`, un intervalo de caracteres que identifica el término marcado y una sugerencia de reemplazo extraída de la entrada de la lista de vocabulario. La Etapa 1 solo marca hallazgos — no reescribe el documento en silencio. Una coincidencia de vocabulario prohibido requiere que un humano comprenda y aplique la sustitución correcta; la reescritura automatizada omitiría esa comprensión.

La Etapa 1 no tiene dependencias externas. Se ejecuta contra un conjunto de términos en memoria y se completa independientemente de la disponibilidad de los servicios de Etapa 2 o Etapa 3.

## Etapa 2 — Pasada Mecánica de LanguageTool

La Etapa 2 llama a LanguageTool 6.6, que se ejecuta como un servicio HTTP compañero co-ubicado con el proceso. LanguageTool aplica reglas de ortografía, gramática y estilo — categorías demasiado numerosas para enumerarlas como una lista de vocabulario estática.

El proceso normaliza la respuesta de LanguageTool al tipo interno `Finding` utilizado en las tres etapas. Cada coincidencia de regla de LanguageTool se mapea a un hallazgo con severidad `Mechanical` y un intervalo de caracteres. El paso de normalización aísla el proceso de los cambios en el esquema de respuesta de LanguageTool.

Los hallazgos de la Etapa 2 se serializan como un bloque de anotación JSON estructurado incrustado en el prompt para la Etapa 3. El bloque de anotación forma parte del registro de solicitud firmado — los hallazgos que recibió la Etapa 3 son recuperables a posteriori.

## Etapa 3 — Pasada Generativa

La Etapa 3 enruta el documento y el conjunto de hallazgos de la Etapa 2 a la capa de inferencia. El servicio de enrutamiento selecciona un nivel de cómputo según la forma de la solicitud y las restricciones de presupuesto aplicables: el Nivel A es un modelo cuantizado de 7B alojado localmente, el Nivel B es un modelo de 32B disponible mediante capacidad de GPU en múltiples nubes, y el Nivel C enruta a una API de inferencia externa. El prompt del sistema incluye el bloque de anotación de la Etapa 2 para que el modelo lea los hallazgos mecánicos como contexto editorial.

El resultado de la Etapa 3 es una reescritura completa del texto de entrada. Los hallazgos de la Etapa 3 llevan severidad `Generative` y representan sugerencias por intervalo derivadas de la pasada de inferencia, más allá del alcance de las reglas mecánicas de la Etapa 2.

## Niveles de Severidad en el Protocolo

La respuesta de `/v1/proofread` lleva un arreglo `findings` donde cada entrada tiene un campo `severity`:

| Severidad | Fuente | Significado |
|---|---|---|
| `Banned` | Etapa 1 | El término aparece en la lista de vocabulario aplicable; requiere sustitución humana |
| `Mechanical` | Etapa 2 | Coincidencia de regla de gramática, ortografía o estilo de la pasada mecánica |
| `Generative` | Etapa 3 | Sugerencia por intervalo de la pasada de inferencia editorial |

Los llamadores usan la severidad para conducir las decisiones de interfaz. Los hallazgos `Banned` pueden justificar una presentación prominente antes de que cualquier trabajo editorial sea apropiado; los hallazgos `Mechanical` pueden colapsarse por defecto en un panel de revisión.

## Veredicto del Operador y el Ciclo de Aprendizaje

Después de revisar la reescritura de la Etapa 3, el operador registra un veredicto mediante `/v1/verdict`: `accepted` (la reescritura se adopta tal como está), `rejected` (el operador revierte al original) o `edited` (el operador ha realizado más cambios y envía el texto final).

El veredicto cierra el ciclo al contribuir al corpus que informa el comportamiento futuro del modelo. La tupla de entrada original, reescritura del proceso y disposición del operador forma un par de calidad de entrenamiento. Cuando el operador edita en lugar de aceptar o rechazar, el texto editado es el ejemplo positivo y la reescritura sin editar es el negativo. El corpus acumula preferencias editoriales reales a lo largo de los veredictos.

## Degradación Controlada

Cada etapa tiene un comportamiento definido cuando su dependencia no está disponible.

Si el servicio LanguageTool de la Etapa 2 no está disponible, el proceso continúa a la Etapa 3 con un conjunto de hallazgos mecánicos vacío. La respuesta incluye un indicador de que la pasada mecánica no se ejecutó.

Si la Etapa 3 no puede alcanzar ningún nivel de cómputo dentro del tiempo de espera configurado, el proceso retorna únicamente los hallazgos de las Etapas 1 y 2, con `generative_pass: false` en la respuesta. Ningún camino de degradación omite silenciosamente los hallazgos disponibles de las etapas que sí se ejecutaron.

## Véase También

- [[language-protocol-substrate]] — las definiciones de familia de género y las listas de vocabulario por familia que utiliza la Etapa 1
- [[customer-tier-catalog-pattern]] — el modelo de despliegue para la instancia del servicio de revisión
- [[soft-slm-tiered-gateway]] — la capa de enrutamiento de inferencia a través de la cual despacha la Etapa 3
