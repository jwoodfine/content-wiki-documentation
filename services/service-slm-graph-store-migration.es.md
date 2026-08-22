---
schema: foundry-doc-v1
title: "Reconstrucción del almacén de grafos de service-slm"
slug: service-slm-graph-store-migration
category: services
index_group: ring-3-ai-gateway
type: concept
content_type: topic
quality: pre-build
status: pre-build
audience: vendor-public
bcsc_class: current-fact
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: service-slm-graph-store-migration.md
short_description: "El almacén de grafos de service-slm ejecuta una reconstrucción nocturna — la extracción de entidades vía Doorman escribe directamente en el grafo al completarse, sin paso de revisión humana en el propio script de reconstrucción."
cites: []
---

El almacén de grafos de [[service-slm]] es un grafo de propiedades en vivo de entidades
comerciales nombradas, extraídas cada noche del corpus de datos de un operador — la capa de
entidades que [[service-content]] usa para inyectar contexto comercial estructurado en las
solicitudes de inferencia sin enviar datos propietarios a un modelo externo. El grafo se
almacena en LadybugDB y se reconstruye cada noche mediante un script que se ejecuta como Fase
1 de la ventana de Cómputo Elástico, antes de que la fase de entrenamiento del modelo reclame
la GPU.

## Qué contiene el grafo

El grafo mantiene cinco clasificaciones de entidades: Persona (personal, contactos,
contrapartes), Empresa (proveedores, clientes, organizaciones socias), Proyecto
(compromisos activos e históricos), Cuenta (cuentas financieras y referencias de libro
mayor), y Ubicación (oficinas, sitios y direcciones operativas). Estas entidades se extraen
de tres flujos de documentos: archivos de transcripción de reuniones, material de
investigación y contexto, y registros de contacto de origen desde [[service-people]].

## Qué hace la reconstrucción nocturna

Por cada documento no procesado, el script de reconstrucción llama al endpoint de
finalización del [[doorman-protocol|Doorman]] con una restricción de gramática JSON Schema.
El modelo de lenguaje — ejecutándose en el nivel de ráfaga GPU vía vLLM — devuelve un arreglo
estructurado de objetos de entidad, cada uno con un nombre, clasificación, puntuación de
confianza, y campos opcionales de rol, ubicación y contacto. El script entonces escribe esas
entidades directamente en el grafo a través del endpoint de mutación de service-content. Una
verificación de salud al final de cada ciclo registra el conteo actual de entidades.

El script procesa todo el backlog de documentos no procesados en cada ejecución, con un
retraso aleatorizado entre solicitudes para que el Doorman nunca reciba una ráfaga que pudiera
interferir con el arranque propio de la fase de entrenamiento.

## La ruta de escritura no tiene paso de revisión propio

Este es el hecho que un lector que evalúa la postura de gobernanza de datos de la plataforma
necesita: la escritura del script de reconstrucción al grafo es incondicionada. Llama al mismo
endpoint de mutación que cualquier operador o miembro de la comunidad podría llamar desde su
propia automatización, y ese endpoint escribe de inmediato — no hay archivo de propuesta, ni
cola pendiente, ni visto bueno humano en ningún punto del flujo propio de este script. Existe
un punto de control de gobernanza de escritura separado en otra parte de service-content (una
ruta de captura-y-verificación para un sitio de llamada automatizado distinto, que requiere un
veredicto humano firmado antes de que una escritura se concrete), pero no cubre este endpoint
ni este script; el diseño propio del endpoint asume en cambio que cada quien lo llama provee
su propio control, y este script no provee ninguno.

## Idempotencia

El script rastrea los documentos procesados en un libro local de solo-anexado, identificado
por un hash del contenido de cada documento. Un documento ya presente en el libro se omite en
ejecuciones futuras. El libro no se depura automáticamente; limpiarlo fuerza una
re-extracción completa en la siguiente ejecución.

## Inyección de contexto del grafo

El grafo no es un almacén de referencia estático. service-content lo consulta antes de cada
solicitud de inferencia, recupera las entidades relevantes al contexto de la solicitud, y las
inyecta en el mensaje de sistema del modelo como contexto comercial estructurado — quiénes son
las personas relevantes, qué proyectos están activos, qué empresas son contrapartes — sin que
esos datos estructurados crucen el límite del modelo externo. El grafo en sí permanece dentro
del despliegue; solo el contexto en prosa inyectado sale de él.

## Estado actual

El grafo está en vivo hoy, con entidades extraídas reales sirviendo activamente solicitudes de
inferencia. Si este patrón está listo para extenderse a contextos operativos más grandes está
condicionado a un criterio de ejecuciones saludables consecutivas que aún no se ha cumplido —
la canalización sigue en su período operativo inicial.

## Véase también

- [[elastic-compute-lora-training-pipeline]] — Fase 2 de la misma ventana nocturna (entrenamiento de adaptador LoRA)
- [[service-slm]] — el servicio que orquesta la canalización nocturna completa
