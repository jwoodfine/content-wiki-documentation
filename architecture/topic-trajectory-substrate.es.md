---
schema: foundry-doc-v1
title: "El Sustrato de Trayectoria"
slug: topic-trajectory-substrate.es
category: architecture
type: topic
quality: published
short_description: "El mecanismo mediante el cual la plataforma PointSav captura su propio trabajo en producción como material de entrenamiento: tres tipos de corpus ortogonales, una biblioteca de adaptadores versionados y un álgebra de composición que permiten al sustrato mejorarse a sí mismo a partir de la actividad operativa real, sin mezclar datos del proveedor, datos de clientes ni registros entre inquilinos."
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: topic-trajectory-substrate.md
---

Foundry captura el trabajo que realiza como material de entrenamiento. Con el tiempo, el sustrato da forma al sustrato.

Este es el Sustrato de Trayectoria: un conjunto de mecanismos de captura, tipos de corpus, tipos de adaptadores y reglas de separación que permiten a la plataforma mejorar su sustrato de IA a partir de la actividad productiva real. La mejora ocurre sin mezclar datos del proveedor y del cliente, sin cruzar fronteras entre inquilinos y sin requerir un esfuerzo separado de anotación o etiquetado de datos.

## Los tres corpus ortogonales

**El corpus constitucional** captura la relación entre cláusulas doctrinales, roles y alcance operativo. Su alcance es universal — aplica a todo despliegue. El adaptador que produce es el adaptador constitucional, cargado por el Doorman en cada solicitud.

**El corpus de ingeniería** captura las trayectorias de sesión del constructor de la plataforma, los commits de código y las enmiendas doctrinales. Su alcance es el proveedor. El adaptador que produce refleja el juicio acumulado del trabajo de desarrollo de la plataforma.

**El corpus de tiempo de ejecución por inquilino** captura lo que fluye a través de los servicios Ring 1 de un cliente: registros que llegan, deltas del grafo de conocimiento que produce el pipeline, patrones de uso del operador. Su alcance es estrictamente por cliente. Vive dentro de la instancia ToteboxOS del cliente. El espacio de trabajo del proveedor nunca recibe registros de tiempo de ejecución de inquilinos a menos que el cliente haya optado explícitamente por el mercado federado.

Los tres corpus nunca se cruzan en tiempo de entrenamiento. Esta es privacidad estructural por infraestructura: la separación se aplica por la ubicación de escritura de los archivos, no por documentos de política.

## Mecanismos de captura

Cuatro operaciones de captura se ejecutan en segundo plano durante el uso normal de la plataforma: captura de edición (tras cada commit en ramas activas), captura de trayectoria de sesión (al final de una sesión de trabajo), captura doctrinal (en actualizaciones de versión de doctrina) y captura de retroalimentación (cuando un operador rechaza un resultado o solicita una revisión).

La captura de retroalimentación registra la tripleta de salida rechazada, salida corregida y etiqueta de violación doctrinal. Estas tripletas alimentan el entrenamiento DPO en el adaptador correspondiente, produciendo aprendizaje de antipatrones con granularidad por cluster, por rol y por colaborador.

## La biblioteca de adaptadores

El entrenamiento de los corpus capturados produce una biblioteca de adaptadores LoRA — modificaciones de peso ligeras que desplazan el comportamiento de un modelo base en una dirección específica. Los adaptadores están versionados y firmados; cada versión incorpora la versión de doctrina contra la que fue entrenada.

La composición en tiempo de solicitud sigue un álgebra fija: el modelo base más el adaptador constitucional (siempre cargado), más el adaptador de ingeniería para trabajo de construcción de plataforma, más el adaptador de inquilino para trabajo de voz del cliente, más el adaptador de rol que corresponde al rol de la sesión solicitante, más el adaptador de cluster para el proyecto activo.

## Procedencia y re-derivabilidad

Cada registro del corpus lleva una cabecera de procedencia estructurada: tipo de tupla, versión de doctrina en el momento de la captura, identificador de inquilino, identificador de cluster, rol, alcance, clase de redacción, clase de evidencia, commit fuente e identificador de sesión. La combinación hace que cada versión de adaptador sea re-derivable desde sus registros fuente, y que cualquier registro fuente pueda responder: ¿en qué versiones de adaptadores se usó este registro para entrenamiento?

## Ver también

- [[topic-apprenticeship-substrate]] — el cuarto tipo de corpus (aprendizaje asistido) que trabaja junto al Sustrato de Trayectoria
- [[compounding-doorman]] — el Doorman que lee la biblioteca de adaptadores y aplica el álgebra de composición en tiempo de solicitud
- [[topic-llm-substrate-decision]] — el modelo base OLMo 3 que todos los adaptadores modifican

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*
