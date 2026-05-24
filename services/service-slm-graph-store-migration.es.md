---
schema: foundry-doc-v1
title: "Migración del almacén de grafos de service-slm"
slug: service-slm-graph-store-migration
category: services
type: concept
quality: pre-build
status: pre-build
audience: vendor-public
bcsc_class: current-fact
language_protocol: PROSE-TOPIC
last_edited: 2026-05-24
editor: pointsav-engineering
paired_with: service-slm-graph-store-migration.md
short_description: "service-slm migró su almacén de grafos de LadybugDB a SQLite para nodos de flota e integra una reconstrucción nocturna del DataGraph que procesa el corpus de datos del operador a través de Doorman hacia el grafo de propiedades utilizado para la inyección de contexto en inferencia."
cites: []
---

Cada noche, `jennifer-datagraph-rebuild.sh` procesa el corpus de datos
del operador y escribe las entidades nombradas extraídas en un grafo
de propiedades almacenado en LadybugDB. Este grafo de propiedades — el
DataGraph del despliegue — es la capa de entidades que service-content utiliza
para inyectar contexto de negocio estructurado en las solicitudes de
inferencia. La reconstrucción se ejecuta como Fase 1 de la ventana nocturna
de Elastic Compute #1, antes de que la fase de entrenamiento reclame la GPU. El
DataGraph del despliegue está activo, con un archivo LadybugDB de 11 MB
actualmente operativo en service-content.

## Qué contiene el DataGraph

El DataGraph del despliegue es un grafo de propiedades de entidades de negocio
nombradas extraídas del corpus de datos del despliegue del operador. El grafo
contiene cinco clasificaciones de entidades: Persona (personal, contactos,
contrapartes), Empresa (proveedores, clientes, organizaciones asociadas),
Proyecto (compromisos activos e históricos), Cuenta (cuentas financieras y
referencias de libro mayor) y Ubicación (oficinas, instalaciones y direcciones
operativas). Estas entidades se extraen de tres flujos de documentos: archivos
markdown de transcripciones de reuniones del directorio de activos del
minutebook, archivos YAML y markdown de investigación del directorio de
service-agents, y registros JSON de fuentes de contactos del directorio de
service-people.

## Qué hace la reconstrucción nocturna

Para cada documento no procesado, el script de reconstrucción llama a
`POST :9080/v1/chat/completions` a través del endpoint Doorman, pasando el
texto del documento con una restricción de gramática JSON Schema. El modelo de
lenguaje — OLMo 3 32B Think ejecutándose en Elastic Compute #1 mediante vLLM — devuelve
un arreglo JSON estructurado de objetos de entidades. Cada objeto incluye el
nombre de la entidad, la clasificación, la puntuación de confianza y vectores
opcionales de rol, ubicación y contacto. Luego, el script llama a
`POST :9081/v1/graph/mutate` en service-content para escribir esas entidades
en LadybugDB. La sonda de salud al final del ciclo consulta service-content
para obtener el conteo actual de entidades y escribe un archivo JSON resumen
en `$FOUNDRY_ROOT/data/datagraph-health.json`.

El script procesa tres lotes de documentos por ejecución: el árbol completo de
activos del minutebook, el árbol completo de service-agents y los 50 archivos
JSON de service-people más recientes no procesados. Un retardo aleatorio entre
documentos (de 0,3 a 1,5 segundos) evita que Doorman reciba una ráfaga de
solicitudes que podría interferir con el inicio de la fase de entrenamiento.

## El principio de paridad de enrutamiento

El script `jennifer-datagraph-rebuild.sh` llama únicamente a los mismos dos
endpoints REST API que cualquier operador o miembro de la comunidad que ejecute
service-slm y service-content llamaría desde su propia automatización:

- `POST :9080/v1/chat/completions` — extracción de entidades a través de Doorman
- `POST :9081/v1/graph/mutate` — escritura de entidades a través de service-content

No existe un acceso directo mediante observador de archivos, sin desvío interno
gRPC ni escritura directa en la base de datos. Esta es una decisión de diseño
deliberada. Si el script de reconstrucción falla, el fallo indica un defecto
real en service-slm o service-content que también afectaría a cualquier
operador o cliente que utilice la misma superficie de API. La reconstrucción
nocturna funciona como una prueba de integración completa que se ejecuta contra
servicios en producción con datos en producción cada noche. Los fallos son
explícitos y accionables de inmediato, en lugar de estar ocultos en una ruta
interna que los usuarios reales nunca ejercerían.

## Idempotencia

El script rastrea los documentos procesados mediante un registro local en
`$FOUNDRY_ROOT/data/datagraph-processed.txt`. Cada documento se identifica
mediante un hash de su contenido de archivo, prefijado con una etiqueta de
origen (`mk-` para minutebook, `ag-` para service-agents, `sp-` para
service-people). Antes de procesar cualquier documento, el script verifica si
su identificador aparece en el registro. Si está presente, el documento se
omite. Después de una llamada exitosa a `graph/mutate`, el identificador se
agrega al registro. Este mecanismo garantiza que los documentos no sean
reprocesados en múltiples ejecuciones nocturnas, incluso si el mismo contenido
está presente en los directorios de origen.

El registro es de solo adición y no se poda automáticamente. Si service-content
se reinicia y el grafo se reconstruye desde cero, el registro puede borrarse
para forzar una re-extracción completa en la próxima ejecución nocturna.

## Inyección de contexto del grafo

El DataGraph del despliegue no es un almacén de referencia estático.
service-content lo consulta antes de cada solicitud de inferencia. Cuando
Doorman recibe una solicitud de completación de un operador o aplicación,
service-content recupera las entidades relevantes al contexto de la solicitud
— basándose en el ID de módulo, la clasificación de entidades y los umbrales
de confianza — y las inyecta en el mensaje de sistema como un bloque de
contexto de entidades estructurado. El modelo de lenguaje recibe contexto de
negocio estructurado (quiénes son las personas relevantes, qué proyectos están
activos, qué empresas son contrapartes) sin que esos datos estructurados crucen
el límite del modelo externo. El grafo permanece dentro del límite del
despliegue; solo el contexto en prosa inyectado lo abandona.

## Estado actual y criterio de validación

El DataGraph del despliegue está activo. Tres ejecuciones nocturnas consecutivas
que reporten estado HEALTHY — definido como un delta de conteo de entidades no
negativo y un ciclo exitoso de ida y vuelta en los endpoints de extracción y
mutación — son el criterio previsto antes de que el patrón DataGraph se extienda
a contextos operativos más amplios. Ese criterio aún no se ha alcanzado; el
pipeline de reconstrucción se encuentra en su período operativo inicial.

## Véase también

- [[elastic-compute-lora-training-pipeline]] — la Fase 2 de la misma ventana nocturna (entrenamiento de adaptador LoRA)
- [[service-slm]] — el servicio que orquesta el pipeline nocturno completo
