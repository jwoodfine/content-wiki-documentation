---
schema: foundry-doc-v1
title: "La consola del corrector"
slug: radical-proofreader-ui
category: applications
type: app
content_type: topic
quality: complete
short_description: "La interfaz web orientada al operador para la canalización editorial service-proofreader, que implementa una arquitectura de tokens de diseño de dos niveles para la adaptación de marca del inquilino y una herramienta de destilación en Rust puro que convierte pares de eventos del corpus de aprendizaje en conjuntos de datos de entrenamiento para service-slm."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-06-30
editor: pointsav-engineering
cites: []
references: []
paired_with: radical-proofreader-ui.md
---

La **consola del corrector** es la interfaz web orientada al operador para la canalización
editorial `service-proofreader`. Los operadores utilizan la consola para enviar texto para
análisis por etapas, revisar hallazgos estructurados, aplicar o rechazar reescrituras
sugeridas y registrar disposiciones de veredicto que alimentan el corpus de aprendizaje de
la plataforma. La consola está implementada como una aplicación HTML renderizada en el servidor
sin dependencia de marcos de trabajo JavaScript del lado del cliente.

## Arquitectura de tokens de diseño

La consola implementa una arquitectura de tokens de diseño de dos niveles que desacopla el
lenguaje visual de la plataforma de la identidad de marca de cualquier inquilino específico.
El primer nivel consiste en tokens genéricos — variables CSS de referencia, primitivas de
espaciado y escalas tipográficas — distribuidos desde el repositorio `pointsav-design-system`.
Estos tokens establecen el vocabulario estructural de la interfaz: diseño de cuadrícula,
tamaño de componentes, colores de estado para los niveles de gravedad de hallazgos y jerarquía
tipográfica para la visualización de hallazgos de tres niveles (Prohibido, Mecánico, Generativo).

El segundo nivel consiste en tokens de anulación del inquilino procedentes del repositorio de
activos multimedia del inquilino. Estos tokens llevan decisiones de marca — tipografías, paleta
de colores y activos de logotipo — que adaptan la interfaz a la identidad visual del inquilino
sin modificar el código fuente de la consola. Los dos niveles se aplican en secuencia en el
momento del renderizado: los tokens genéricos establecen los valores predeterminados; los tokens
de anulación del inquilino sustituyen valores donde la marca lo requiere.

Esta estratificación permite que la misma base de código de la consola sirva a múltiples
inquilinos bajo identidades de marca distintas. Un despliegue sin archivo de anulación del
inquilino recurre completamente al nivel genérico.

## La garantía de no entrenamiento con texto del inquilino

La consola expone el compromiso de manejo de datos de la plataforma en el punto de envío de
texto. La garantía de no entrenamiento con texto del inquilino es una propiedad estructural de
la ruta de escritura del corpus: el texto enviado por un operador y la reescritura resultante
se escriben en el directorio de instancia de despliegue de ese inquilino y no pueden mezclarse
con los registros de otros inquilinos.

La garantía se hace explícita en la interfaz de envío porque los operadores requieren confianza
antes de enviar material editorial sensible. La consola la muestra como un aviso de divulgación
— permanente, no descartable — adyacente al área de envío de texto.

## Registro de veredictos y el ciclo de aprendizaje

Después de que la canalización de tres etapas produce sus hallazgos y la reescritura completa
del texto, el operador interactúa con la consola a través de una interfaz de veredicto. La
interfaz presenta simultáneamente el texto original, la reescritura de la Etapa 3 y el
conjunto de hallazgos anotados. Están disponibles tres controles de disposición: Aceptar (tomar
la reescritura tal cual), Rechazar (descartar la reescritura y conservar el original) o Editar
(enviar una versión modificada manualmente como texto final).

El veredicto enviado desencadena una escritura `/v1/verdict` que registra la entrada, la
salida elegida y la disposición del operador como una tupla de par de eventos tipificada. Los
veredictos aceptados y editados son la señal de entrenamiento más valiosa. Los veredictos
rechazados se conservan como ejemplos negativos para la canalización de Optimización de
Preferencias Directas de la Etapa 1.

## Implementación en Rust y destilación del corpus

La canalización de entrenamiento de la plataforma está implementada en Rust en lugar de un
lenguaje de scripting. La herramienta de destilación procesa los registros de eventos JSONL
sin procesar escritos por el punto de conexión de veredicto para extraer pares de
entrada/salida verificados basados en las disposiciones del operador. La herramienta garantiza
la seguridad de tipos al analizar el esquema de par de eventos — `draft-created`,
`draft-refined`, `creative-edited` — y produce un archivo `training_dataset.jsonl` en el
formato consumido por `service-slm` para el ajuste fino LoRA.

La implementación en Rust unifica el ecosistema de herramientas operativas: una sola invocación
`cargo run` reemplaza una canalización de scripts de shell y pasos de preprocesamiento en
Python. También elimina una clase de errores de análisis que pueden surgir cuando el esquema de
par de eventos evoluciona — los cambios de esquema requieren actualizar las definiciones de tipo
en Rust, que el compilador impone en tiempo de compilación.

## Véase también

- [[editorial-pipeline-three-stages]] — la canalización de tres etapas con la que interactúa
  la consola
- [[language-protocol-substrate]] — la clasificación de familia de género que refleja la
  visualización de hallazgos de la consola
- [[customer-tier-catalog-pattern]] — cómo se provisiona la instancia de despliegue del
  corrector
