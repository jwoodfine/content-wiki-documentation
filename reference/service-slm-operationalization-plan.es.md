---
schema: foundry-doc-v1
title: "Plan de Operacionalización de service-slm"
slug: service-slm-operationalization-plan.es
category: reference
type: topic
quality: published
short_description: El plan estratégico y operativo para hacer la transición desde llamadas a modelos de lenguaje externos hacia un sustrato de modelo de lenguaje pequeño por inquilino que se mejora mediante un bucle de retroalimentación compuesto.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: service-slm-operationalization-plan.md
---

El plan de operacionalización de service-slm describe el camino previsto desde un estado inicial — en el que las llamadas a modelos de lenguaje externos grandes gestionan sustancialmente todo el trabajo asistido por inteligencia artificial — hacia un estado objetivo en el que un sustrato de modelo de lenguaje pequeño por inquilino contribuye en paralelo con las llamadas externas, acumula un corpus de entrenamiento a partir de sus propios resultados y correcciones, y desplaza progresivamente el nivel externo de mayor costo en los tipos de tareas que el sustrato ha dominado.

## El estado objetivo

El objetivo estratégico es un sustrato editorial y de aprendizaje por inquilino donde cada commit se convierte en material para el corpus de entrenamiento, los pesos de adaptadores por inquilino se componen con el modelo base abierto en el momento de la inferencia, y el sustrato mejora monótonamente porque dos bucles de retroalimentación se cierran simultáneamente. El primer bucle captura la señal de corrección estructural. El segundo bucle captura la señal de oficio — si un colaborador creativo editó el resultado publicado — y la incorpora como una capa de entrenamiento de preferencia sobre la capa estructural.

## Los tres niveles de cómputo

El sustrato enruta el trabajo asistido por inteligencia artificial a través de tres niveles. El **Nivel A** es local: un modelo de pesos abiertos más pequeño ejecutándose en la máquina virtual de trabajo bajo inferencia de CPU, siempre disponible sin dependencia externa. El **Nivel B** es de ráfaga: un modelo de pesos abiertos más grande en cómputo GPU preferencial aprovisionado bajo demanda, adecuado para tuberías editoriales asíncronas que toleran un tiempo de inicio en frío de sesenta a ciento veinte segundos. El **Nivel C** es API externa: proveedores de modelos de lenguaje externos alcanzados vía HTTPS, reservado para tareas de precisión estrecha: fundamentación de citas, construcción inicial de grafos de conocimiento, generación de salida estructurada y desambiguación de entidades en casos de alta ambigüedad.

## El mecanismo de autocorrección

El sustrato es autocorrectivo a nivel de corpus. Cuando el portal editorial acepta un resultado del sustrato, la aceptación se registra. Cuando el portal lo rechaza, el rechazo y la versión corregida también se registran. Ambas señales alimentan el corpus de entrenamiento. Un tipo de tarea que comienza con una tasa de aceptación baja mejora a lo largo de ciclos de entrenamiento sucesivos. La consecuencia práctica es que un resultado de calidad algo menor a tasas aceptables hoy es aceptable si la señal de rechazo produce un modelo mejor mañana.

## Marco de entrenamiento LoRA y corpus por inquilino

El entrenamiento de adaptadores usa el marco Axolotl con el modelo OLMo 3.1 32B Think. Un adaptador por inquilino se entrena con adaptación de bajo rango. Los datos de entrenamiento por inquilino viven en instancias de despliegue separadas, una por inquilino, para mantener los datos de cada uno estructuralmente separados entre sí.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Con licencia [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*
