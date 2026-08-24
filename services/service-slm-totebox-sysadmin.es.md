---
schema: foundry-doc-v1
title: "SLM como sysadmin de Totebox — el plan"
slug: service-slm-totebox-sysadmin
category: services
type: topic
content_type: topic
quality: complete
index_group: ring-3-ai-gateway
short_description: "Una dirección planificada para service-slm: usar su canalización real y ya operativa de captura-y-veredicto para construir un asistente sysadmin de Totebox — la taxonomía de tareas específica y las herramientas descritas aquí aún no están construidas."
status: active
bcsc_class: forward-looking
language_protocol: PROSE-TOPIC
last_edited: 2026-08-24
editor: pointsav-engineering
cites:
 - olmo3-allenai
 - federated-lora-2502-05087
 - lorax-predibase
 - s-lora-2024
 - constitutional-ai-2212-08073
 - vllm-multi-lora
 - ni-51-102
 - np-51-201
paired_with: service-slm-totebox-sysadmin.md
---

Se pretende que [[service-slm]] se convierta en el asistente operativo de los despliegues
[[totebox-os|Totebox]] — una IA que ayude a un operador a diagnosticar y resolver problemas
cotidianos de sysadmin en lugar de exigirle buscar en la documentación o escalar a
ingeniería. Esta es una dirección planificada, no una función distribuida: lo que es real hoy
es el sustrato de entrenamiento subyacente; lo que está planificado es dirigirlo
específicamente al trabajo de sysadmin.

## Lo que es real hoy

La [[apprenticeship-substrate|canalización de aprendizaje]] sobre la que se construiría este
plan es real y operativa. Captura una tupla de corpus para cualquier tipo de tarea etiquetado
en `stage_at_capture: review`, `verdict: null`, en cada commit relevante — automático, sin
acción del operador. Una identidad senior revisa posteriormente las tuplas capturadas y firma
un veredicto (aprobar, refinar, rechazar o diferir) usando una firma SSH verificada contra el
registro de firmantes del espacio de trabajo. Este mecanismo de captura-y-firma-de-veredicto
es genérico — ya se ejecuta hoy para tipos de tarea de ingeniería, no de sysadmin — y los
adaptadores LoRA por inquilino compuestos en tiempo de solicitud por el Doorman son una
capacidad real y funcional.

**Lo que no es real hoy**: ningún tipo de tarea de sysadmin se ha registrado en esta
canalización. La taxonomía específica a continuación, y las herramientas que nombra, son una
propuesta de cómo esa capacidad podría extenderse al trabajo de sysadmin — no un inventario de
lo que existe.

## La taxonomía de tareas propuesta

Un relevamiento de las guías operativas en los clústeres de despliegue de Totebox sugiere
aproximadamente diez categorías recurrentes de trabajo de sysadmin con las que un asistente
entrenado podría ayudar: aprovisionamiento de nodos, diagnóstico de canalización de ingreso,
extracción soberana de datos, egreso a almacenamiento en frío, revisión de registros
redactados por IA contra los verificados, operaciones de índice de búsqueda, operaciones de
identidad y emparejamiento, validación de despliegue de adaptadores, reconciliación de rastro
de auditoría, e importación de datos conforme a esquema. Cada una necesitaría su propio tipo
de tarea registrado en la canalización anterior, con su propio corpus de interacciones reales
del operador, antes de que pudiera entrenarse un adaptador para ella.

## Por qué service-slm en lugar de una API externa, si se construye

El razonamiento para mantener este trabajo local en lugar de enrutarlo a una API de terceros
aplica independientemente de si la taxonomía específica anterior es lo que finalmente se
distribuye: cada una de estas categorías de tareas toca datos de inquilinos — registros de
personal, libros mayores corporativos, archivos de propiedades, rastros de auditoría — y
enrutar esos datos a un servicio externo para operaciones rutinarias de sysadmin rompería la
garantía de soberanía de datos de la plataforma. Un modelo ejecutándose dentro del límite
propio del Doorman del cliente es la arquitectura donde los datos nunca salen de la
infraestructura propia del cliente. Los adaptadores LoRA por inquilino, una vez entrenados con
el corpus operativo propio de un cliente, también harían al asistente más preciso para ese
cliente específicamente que lo que podría lograr un servicio genérico — el historial de
interacción propio del cliente permanece dentro de su propio sustrato, disponible para
entrenamiento, sin transmisión externa.

## Costo y cronograma

Cualquier cifra de costo o cronograma para esta capacidad — costo por solicitud a escala,
costo de ejecución de entrenamiento, umbrales de promoción de adaptadores — son objetivos
planificados pendientes de datos operativos reales, no cifras medidas. [ni-51-102]
[np-51-201]

## Véase también

- [[service-slm]] — el servicio que implementaría esta capacidad
- [[compounding-doorman]] — el patrón operativo que implementa el Doorman
- [[apprenticeship-substrate]] — la canalización real de captura y firma de veredicto sobre la que se construye este plan
- [[brief-queue-substrate]] — la cola durable que mantiene la captura de corpus continua a través de transiciones de nivel de cómputo
- [[pointsav-llm]] — el producto comercial especialista relacionado, planificado por separado
