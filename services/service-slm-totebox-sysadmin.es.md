---
schema: foundry-doc-v1
title: "service-slm como Administrador y Centro de Soporte Totebox"
slug: service-slm-totebox-sysadmin.es
category: services
type: topic
quality: core
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
paired_with: service-slm-totebox-sysadmin.md
---

## Adaptación estratégica — service-slm como administrador Totebox

`service-slm` — el Doorman Compuesto en el Anillo 3 de la plataforma — está diseñado para convertirse en el asistente operativo y centro de soporte para los despliegues de Totebox Archive y Totebox Orchestration. Este artículo describe la estrategia: las diez familias de tareas operativas que maneja un administrador, por qué service-slm es estructuralmente adecuado para ellas, y los cuatro etapas que llevan un despliegue desde la captura inicial del corpus hasta un adaptador LoRA por tenant en producción.

## Las diez familias de tareas operativas

Un análisis de los archivos GUIDE en los tres clusters de despliegue Totebox — personal, corporativo y propiedad — produce una taxonomía clara de los escenarios del día a día que un administrador Totebox encuentra. Estas diez familias cubren aproximadamente el 95 por ciento de los escenarios operativos presentes en las guías existentes.

Las familias incluyen: aprovisionamiento de nodos (secuencia física de 9 pasos con verificación criptográfica), diagnóstico de operaciones de ingesta (daemon de spool, autenticación MSFT Graph, errores de glosario de dominio), extracción soberana de datos (DARP), sincronización de almacenamiento en frío, revisión de ejecución del modelo de lenguaje, operaciones de búsqueda soberana, operaciones de identidad y capacidad (protocolo MBA), validación de inyección de adaptadores, reconciliación de pistas de auditoría, e importación de datos conformes al esquema.

Estas diez familias de tareas se convierten en los tipos de tareas nombrados para el registro de aprendizaje de service-slm.

## Por qué service-slm y no una API externa

Cuatro propiedades estructurales hacen que estas cargas de trabajo sean idóneas para service-slm:

**Soberanía.** Cada familia de tareas toca datos del tenant — registros de personal, libros mayores corporativos, archivos de bienes raíces, pistas de auditoría. Enviar estos datos a un servicio externo para operaciones rutinarias de administración rompe la garantía de soberanía de datos en la Doctrina §IV.b. service-slm ejecutándose localmente dentro del límite del Doorman del cliente es la única arquitectura donde los datos nunca salen del sustrato controlado por el cliente.

**Latencia.** El trabajo de administración es de alta frecuencia y baja latencia. El Nivel B (OLMo 3.1 32B Think en GPU A100) entrega aproximadamente 100–150 tokens por segundo. Una llamada de API externa añade 5–15 segundos por llamada incluyendo red y cola del proveedor. En una secuencia de aprovisionamiento de varios pasos, esa diferencia de latencia es material.

**Coste a escala.** El coste amortizado planificado del Nivel B en una instancia preemptible con apagado por inactividad es muy inferior a los equivalentes de API del Nivel C al coste de contexto completo del prompt. A volúmenes operativos sostenidos — miles de consultas de administración por día en una flota activa — el diferencial se compone. *Las proyecciones de coste son objetivos planificados; los costes reales pueden diferir según el modelo, los precios del proveedor y el tamaño del prompt.* [ni-51-102] [osc-sn-51-721]

**Personalización.** Los adaptadores LoRA por tenant, entrenados en los patrones operativos específicos de cada cliente, hacen que service-slm sea un asistente más preciso para ese cliente que cualquier servicio de inferencia genérico.

## Las cuatro etapas del entrenamiento

**Etapa 1 — Captura.** Cada brief de sombra genera una tupla del corpus automáticamente en cada post-commit hook a través del Sustrato de Cola de Briefs. Esta etapa está operativa.

**Etapa 2 — Promover mediante veredicto firmado.** Una identidad senior revisa las tuplas capturadas y firma veredictos criptográficamente. Los veredictos producen pares DPO para el entrenamiento por preferencias. El ritmo sostenible es un lote semanal al final de la sesión.

**Etapa 3 — Ciclo de entrenamiento LoRA por cluster.** Cuando el corpus de un tipo de tarea supera 50 tuplas con veredicto firmado, se activa el entrenador. El ciclo inicial se ejecuta en CPU en el servidor del espacio de trabajo (coste cero). Los ciclos de producción se mueven al Nivel B una vez aprovisionada la instancia de GPU Yo-Yo (planificado). *Los objetivos de cronograma y coste están sujetos a la tasa de acumulación del corpus, disponibilidad de hardware y revisión del operador.* [ni-51-102] [osc-sn-51-721]

**Etapa 4 — Composición multi-adaptador en tiempo de solicitud.** El Doorman compone hasta tres adaptadores por solicitud. Cada entrada del libro mayor de auditoría registra el conjunto de adaptadores compuesto, haciendo trazable la influencia de cada uno.

## Niveles de producto para el cliente

El capability evoluciona a través de tres niveles de cliente. El Nivel 1 es una pyme con un solo Totebox ejecutando el modelo local (soberanía completa, coste solo de hardware). El Nivel 2 añade acceso al Nivel B alojado por el proveedor con adaptadores LoRA por tenant. El Nivel 3 es el producto especialista PointSav-LLM entrenado en el corpus multi-tenant agregado. *El cronograma de despliegue del Nivel 3 y los precios del Nivel 2 son objetivos planificados, sujetos a decisión del operador y condiciones operativas.* [ni-51-102] [osc-sn-51-721]

La especificación técnica completa, incluyendo la tabla de tipos de tarea, el corpus y la cadena de entrenamiento, está disponible en inglés en el artículo principal.

## Véase también

- [[service-slm]] — el servicio que implementa esta capacidad; especificación del Doorman del Anillo 3
- [[compounding-doorman]] — el patrón operativo del Doorman y por qué se compone con el tiempo
- [[apprenticeship-substrate]] — la cadena de captura del corpus y firma de veredictos
- [[brief-queue-substrate]] — la cola durable que mantiene continua la captura del corpus

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
