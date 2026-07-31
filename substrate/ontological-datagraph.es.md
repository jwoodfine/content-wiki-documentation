---
schema: foundry-doc-v1
title: "Grafo de conocimiento organizativo — memoria ontológica para operaciones empresariales"
slug: ontological-datagraph
category: substrate
type: topic
content_type: topic
quality: complete
short_description: "Grafo de conocimiento organizativo de personas, empresas, proyectos y relaciones — memoria semántica persistente para responder consultas de negocio sin releer documentos fuente."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-07-31
editor: pointsav-engineering
cites: []
references: []
paired_with: ontological-datagraph.md
---

# El grafo de conocimiento organizativo — memoria ontológica para operaciones empresariales

Un grafo de conocimiento organizativo almacena lo que una empresa sabe sobre sí misma:
quiénes son sus personas, empresas y proyectos; cómo se relacionan entre sí; qué
decisiones se han tomado y por quién; qué políticas rigen qué actividades. Esta
memoria estructurada está disponible para cada solicitud de inferencia de IA, inyectada
como contexto antes de que el modelo produzca su respuesta.

El grafo responde una clase de pregunta que una búsqueda de similitud vectorial no
puede responder: no solo "¿qué documentos mencionan a ACME Corp?" sino "¿qué es ACME
Corp, a quién conocemos allí, qué contrato rige nuestra relación, y qué decisiones
hemos tomado sobre sus facturas?" El recorrido sigue aristas. La respuesta emerge de
la estructura, no de la proximidad de palabras clave.

## Un grafo por nodo de despliegue

Un nodo de despliegue mantiene exactamente un grafo de conocimiento organizativo.
Todos los servicios que se ejecutan en ese nodo contribuyen entidades a este
almacén único, delimitadas por un identificador de módulo que mantiene los datos de
cada dominio aislados dentro de la misma base de datos física.

Este diseño permite el razonamiento entre dominios sin duplicación. Cuando un servicio
de contabilidad escribe "ACME Corp es un proveedor con condiciones de pago net-30" y
un [[service-extraction|servicio de extracción de documentos]] escribe "ACME Corp tiene sede en Toronto",
ambos hechos existen en el mismo grafo, adjuntos a la misma entidad.

## Qué pertenece al grafo

El grafo almacena hechos ontológicos: qué entidades existen, cómo se relacionan y qué
es verdad sobre ellas en un momento dado. No almacena registros transaccionales.

**En el grafo:**
- Una organización es un proveedor (entidad con atributo de relación).
- Un contrato existe entre dos partes con términos específicos.
- Una decisión fue tomada por una persona específica bajo una política concreta.
- Una propiedad es propiedad de una empresa con una clasificación específica.

**No en el grafo:**
- Líneas de factura individuales (son registros transaccionales; pertenecen al libro de contabilidad).
- Asientos contables (pertenecen al libro mayor).
- Texto de documento sin procesar (pertenece al almacén de documentos).

## Tipos de entidades

El grafo se configura mediante archivos de ontología cargados al inicio. Cada nodo
de despliegue puede definir clasificaciones de entidades apropiadas para su dominio
empresarial. Las clasificaciones base presentes en cada despliegue cubren los
primitivos organizativos fundamentales: Persona, Empresa, Proyecto, Cuenta y Ubicación.

Las clasificaciones adicionales se añaden a través de archivos CSV de ontología. Un
despacho de abogados podría añadir Caso, Regulación y Sentencia. Un administrador de
propiedades podría añadir Propiedad, Arrendamiento e Inquilino.

## Validez temporal

Cada hecho en el grafo lleva una marca de tiempo de creación. Los hechos sobre
entidades que cambian con el tiempo pueden ser reemplazados en lugar de sobrescritos.
El grafo conserva el hecho anterior con su ventana de validez.

## Recorrido multi-salto

El grafo está diseñado para el recorrido, no solo para la búsqueda. Un recorrido
sigue aristas desde una entidad hacia entidades conectadas.

**Ejemplo:** *¿Qué políticas rigen las decisiones de adquisición en este proyecto?*

1. Iniciar en la entidad Proyecto.
2. Seguir aristas `governed_by` hacia entidades Política.
3. Seguir aristas `defines_exceptions` desde cada Política hacia entidades Decisión.
4. Seguir aristas `approved_by` desde cada Decisión hacia entidades Persona.

El resultado: la cadena de gobierno completa, recuperada en una sola consulta
estructurada.

## Cómo entran las entidades al grafo

Las entidades entran al grafo a través de un [[service-extraction|pipeline de extracción]].
Documentos, correos electrónicos, notas de reuniones y otras fuentes en prosa llegan a
un directorio de entrada vigilado. El servicio de extracción lee cada fuente, envía el
texto al enrutador de inferencia para la extracción estructurada de entidades mediante
un esquema restringido por gramática, y escribe las entidades resultantes en el grafo a
través del endpoint de mutación del enrutador.

La calidad de la extracción depende del nivel de inferencia. El modelo compacto local
(Tier A) extrae entidades con menor confianza. El nodo GPU de ráfaga (Tier B) extrae con
mayor confianza, usando ventanas de contexto más amplias y restricciones de salida más
estrictas. La extracción de Tier A es útil para cobertura rápida; la extracción de Tier B
se usa para el registro organizativo canónico.

Cada extracción se registra con una referencia de fuente y una puntuación de confianza.
Las entidades extraídas de fuentes autoritativas (contratos ejecutados, documentos
presentados, registros oficiales) llevan mayor confianza que las extraídas de
correspondencia informal.

## Inyección de contexto en tiempo de inferencia

Antes de despachar cualquier solicitud, el [[soft-slm-tiered-gateway|enrutador de inferencia]] consulta el grafo
organizativo para obtener entidades relevantes para la solicitud actual. Las entidades
coincidentes se formatean como un bloque de contexto estructurado y se anteponen al
prompt del sistema. El modelo recibe este contexto de forma transparente.

## Privacidad y soberanía

El grafo de conocimiento organizativo contiene información empresarial sensible. El
grafo se ejecuta integrado dentro del nodo de despliegue. Su contenido nunca se envía
a un proveedor de inferencia externo como datos de entrenamiento.

La organización es propietaria del archivo de base de datos del grafo, las definiciones
de ontología, los datos de entidades y el historial de extracción. Estos activos son
portables: pueden respaldarse, migrarse y restaurarse sin dependencia de ningún
servicio de terceros.
