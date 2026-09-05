---
schema: foundry-doc-v1
title: "Plan de operacionalización de service-slm"
slug: service-slm-operationalization-plan
category: reference
type: topic
content_type: topic
quality: complete
short_description: El plan estratégico y operativo para hacer la transición desde llamadas a modelos de lenguaje externos hacia un sustrato de modelo de lenguaje pequeño por inquilino que se mejora mediante un bucle de retroalimentación compuesto.
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: service-slm-operationalization-plan.md
---


El plan de operacionalización de [[service-slm]] describe el camino previsto desde un estado inicial — en el que las llamadas a modelos de lenguaje externos grandes gestionan sustancialmente todo el trabajo asistido por inteligencia artificial — hacia un estado objetivo en el que un [[compounding-substrate|sustrato de modelo de lenguaje pequeño]] por inquilino contribuye en paralelo con las llamadas externas, acumula un corpus de entrenamiento a partir de sus propios resultados y correcciones, y desplaza progresivamente el nivel externo de mayor costo en los tipos de tareas que el sustrato ha dominado.

Esta es una trayectoria de varios años, no un evento de despliegue único. El plan está ratificado como guía operativa que dirige el trabajo entre clústeres a lo largo de múltiples hitos de ingeniería.

## El estado objetivo

El objetivo estratégico es un sustrato editorial y de [[apprenticeship-substrate|aprendizaje]] por inquilino donde cada commit se convierte en material para el corpus de entrenamiento, los [[adapter-composition|pesos de adaptadores]] por inquilino se componen con el modelo base abierto en el momento de la inferencia, y el sustrato mejora monótonamente porque dos bucles de retroalimentación se cierran simultáneamente. El primer bucle captura la señal de corrección estructural — si el sustrato produjo un resultado que el portal editorial aceptó — y la incorpora al entrenamiento continuo. El segundo bucle captura la señal de oficio — si un colaborador creativo editó el resultado publicado, y cómo — y la incorpora como una capa de entrenamiento de preferencia sobre la capa estructural.

Cuando ambos bucles están operando, cada tipo de tarea que el sustrato maneja con una tasa de aceptación suficientemente alta es candidato a promoción: de requerir revisión sénior en cada resultado, a requerir solo verificaciones puntuales, a operar de forma autónoma dentro de su límite de tarea. Cada paso de promoción reduce el costo por tarea en llamadas a modelos externos. El costo semanal de modelos externos tiende hacia un piso que comprende solo el trabajo de coordinación y ratificación que irreduciblemente requiere el modelo de mayor capacidad.

La razón estructural por la que este camino no es replicable por despliegues multiinquilino de propósito general es que los bucles de retroalimentación se cierran por inquilino. Un colaborador creativo que edita contenido para el despliegue de un cliente produce pares de preferencia que entrenan un adaptador específico de la voz de ese cliente. Los despliegues multiinquilino producen retroalimentación que promedia entre todos los clientes y no mejora el sustrato de ningún cliente en particular.

## Los tres niveles de cómputo

El sustrato enruta el trabajo asistido por inteligencia artificial a través de tres niveles de cómputo según la forma de la tarea, los requisitos de latencia y el presupuesto de costo.

**Nivel A — Local.** Un modelo de pesos abiertos más pequeño ejecutándose en la máquina virtual de trabajo bajo inferencia de CPU. Este es el respaldo siempre disponible: sin dependencia externa, sin costo por llamada, latencia predecible. Adecuado para tareas donde los requisitos de calidad son modestos o donde la forma de la tarea ya ha sido dominada por el sustrato mediante entrenamiento continuo.

**Nivel B — Ráfaga.** Un modelo de razonamiento de pesos abiertos más grande — el nivel de 32 mil millones de parámetros de la misma familia OLMo que el modelo local — en cómputo GPU preferencial aprovisionado bajo demanda. Este nivel es eficiente en costo para cargas de trabajo que toleran tiempos de inicio en frío de sesenta a ciento veinte segundos, aceptable para tuberías editoriales asíncronas pero no para flujos de trabajo interactivos síncronos. El modelo de precios preferencial reduce el costo en aproximadamente un sesenta por ciento comparado con el cómputo bajo demanda para el mismo hardware.

**Nivel C — API externa.** Proveedores de modelos de lenguaje externos alcanzados vía HTTPS. Este nivel se reserva para tareas de precisión estrecha — fundamentación de citas, construcción inicial de grafos de conocimiento a partir de un corpus, generación de salida estructurada cuando el modelo local no puede cumplir el umbral de conformidad del esquema, y desambiguación de entidades en casos de alta ambigüedad. El servicio [[compounding-doorman|Doorman]] es el único componente que guarda claves de API externas; todas las llamadas del Nivel C se enrutan a través de él y se registran en el [[worm-ledger-architecture|libro de auditoría]] por inquilino.

La decisión de enrutamiento la toma el Doorman según la forma de la solicitud y los límites de presupuesto por inquilino. Los llamantes no eligen un nivel; describen lo que necesitan, y el Doorman enruta en consecuencia.

## El mecanismo de autocorrección

El término "autocorrección" describe una propiedad del bucle de retroalimentación, no un proceso correctivo aplicado a errores específicos. Cuando el sustrato produce un resultado que el portal editorial acepta, la aceptación se registra. Cuando el portal lo rechaza, el rechazo y la versión corregida también se registran. Ambas señales alimentan el corpus de entrenamiento. Un tipo de tarea que comienza con una tasa de aceptación baja mejora a lo largo de ciclos de entrenamiento sucesivos a medida que el sustrato aprende de sus rechazos. El sistema es autocorrectivo a nivel del corpus, no a nivel de cada resultado individual.

Esta propiedad tiene una implicación práctica para la gestión de calidad: un resultado de calidad algo menor por parte de un modelo menos capaz hoy es aceptable si la señal de rechazo alimenta un corpus de entrenamiento que produce un modelo mejor mañana. El costo de un resultado imperfecto a tasas aceptables es la inversión en entrenamiento; el retorno es un sustrato que requiere progresivamente menos corrección.

## Marco de entrenamiento LoRA

El [[yo-yo-lora-training-pipeline|entrenamiento de adaptadores]] usa la pila de Hugging Face `peft`/`trl`/`transformers` — `LoraConfig` y `SFTTrainer` — no un marco de entrenamiento de terceros. El volumen actual de pares (cientos bajos) se sitúa por debajo del piso estable para el entrenamiento por pares de preferencia. El ajuste fino supervisado sobre pares de verdad fundamental de un solo lado es, en su lugar, la vía de entrenamiento principal. Existen tanto un script de SFT como un script de entrenamiento de preferencia, que comparten el mismo rango LoRA para que un cambio futuro no requiera un nuevo formato de adaptador. Un adaptador por inquilino se entrena con rango 16 (alpha 32), cargado en float16 en lugar de 4 bits, en una GPU L4 con 24 gigabytes de memoria — la carga completa en float16 cabe en el margen de la L4, mientras que una carga cuantizada no cabría. El modelo base es el modelo de pesos abiertos de nivel local de la plataforma, no el modelo de ráfaga más grande. El controlador de entrenamiento se parametriza por la ruta de corpus específica del inquilino y la ruta de salida del adaptador, de modo que el mismo controlador maneja a todos los inquilinos proporcionando distintas rutas de entrada y salida.

La cadencia de entrenamiento prevista es trimestral, sincronizada con el momento en que el corpus de cada inquilino ha acumulado volumen suficiente para producir una señal significativa. Una ejecución de entrenamiento inicial cuesta aproximadamente entre diez y veinte dólares estadounidenses en cómputo de GPU, según la clase de instancia y la duración de la ventana planificadas.

## Despliegue del corpus

Los datos de entrenamiento por inquilino viven en instancias de despliegue en lugar de a nivel de espacio de trabajo. Esto mantiene los datos del inquilino estructuralmente separados: una instancia de despliegue guarda el corpus, los pesos de adaptador y el libro de auditoría del inquilino PointSav; una segunda instancia guarda lo mismo para el inquilino Woodfine. La entrada del catálogo en el repositorio de despliegue de flota describe para qué sirve una instancia de tubería de entrenamiento; la instancia numerada lleva el estado real por inquilino.

## Véase también

- [[tier-c-key-wiring]] — La forma operativa de gestión de claves API del Nivel C externo
- [[apprenticeship-substrate]] — el pipeline de aprendizaje que acumula el corpus de entrenamiento
- [[compounding-doorman]] — el Portero que enruta entre los tres niveles de cómputo
- [[yo-yo-lora-training-pipeline]] — el pipeline nocturno de entrenamiento LoRA en la GPU de ráfaga
- [[trajectory-substrate]] — el mecanismo que convierte el trabajo operativo en tuplas de entrenamiento
