---
schema: foundry-doc-v1
title: "Reconstrucción nocturna del grafo de datos"
slug: nightly-datagraph-rebuild
category: substrate
type: concept
content_type: topic
index_group: small-language-model-stack
status: stub
short_description: "El proceso programado que reconstruye el grafo de conocimiento de la plataforma cada noche. Existe un punto de control de aprobación humana para las entidades extraídas por IA, pero es opcional — un operador debe habilitarlo; por defecto, las escrituras automatizadas llegan al grafo sin revisión por elemento."
bcsc_class: public-disclosure-safe
lang: es
last_edited: 2026-08-24
editor: pointsav-engineering
paired_with: nightly-datagraph-rebuild.md
---

La reconstrucción nocturna del grafo de datos es el proceso programado que reconstruye el [[knowledge-graph-grounded-apprenticeship|grafo de conocimiento]] completo de la plataforma a partir de sus fuentes canónicas de archivos planos. Todas las relaciones consultables en el grafo — enlaces de entidades, [[service-extraction|resultados de extracción]], [[worm-ledger-architecture|entradas del libro de registros]] e índices de [[location-intelligence-substrate|inteligencia de ubicación]] — se derivan de las mismas entradas deterministas en cada ciclo. El resultado es una instantánea estable disponible para todos los consumidores de consultas al inicio de cada día operativo.

## Puntos clave

- El grafo se reconstruye a partir de fuentes de archivos planos cada noche, sin mantenimiento por mutación continua. Los consumidores leen una instantánea estable, no un grafo parcialmente construido en tiempo real.
- Cada ciclo de reconstrucción puede replicarse a partir de archivos planos archivados, ya que la instantánea del libro de registros WORM que cada ciclo lee es en sí misma inmutable.
- La extracción de entidades usa inferencia restringida por gramática a través del [[doorman-protocol|Doorman]] — esto es el Anillo 2 invocando al Anillo 3 para obtener una propuesta, no un paso determinista interno del Anillo 2. Existe un punto de control de captura-y-promoción exactamente para este caso — la salida de extracción puede retenerse para una aprobación firmada criptográficamente y revisada por un humano antes de convertirse en una escritura al grafo, en línea con el límite de [SYS-ADR-07](governance/architecture-decisions). Ese punto de control es opcional, no el valor por defecto: un operador debe habilitarlo explícitamente. Con la configuración por defecto, la salida de extracción se escribe en el grafo de inmediato, sin revisión por elemento. Véase [[three-ring-architecture|la Arquitectura de Tres Anillos]] para la regla general que este punto de control implementa cuando está habilitado.
- Cada ciclo acumula el anterior. Los registros recién comprometidos extienden el grafo; ningún registro se elimina. El mecanismo [[compounding-substrate]] hace que el grafo crezca con precisión de forma monotónica con el tiempo.

## Propósito

El patrón de reconstrucción garantiza que el substrato consultable refleje el estado comprometido del registro canónico, no la deriva acumulada en memoria. Cualquier ejecución individual puede replicarse a partir de los archivos planos archivados.

Las uniones basadas en esquemas contra la taxonomía canónica y los índices de inteligencia de ubicación son deterministas — sin coincidencia difusa. La extracción de entidades en sí no lo es: es inferencia restringida por gramática a través del Doorman, que produce un registro estructurado. Que un humano revise ese registro antes de que se convierta en una escritura al grafo depende de una configuración que controla el operador, desactivada por defecto — véase la nota de cumplimiento arriba. Es una brecha real y actualmente abierta entre la intención del límite de SYS-ADR-07 (la IA nunca escribe directamente en un almacén de registros estructurados) y la configuración por defecto de este proceso, que se está siguiendo por separado con Command.

## Etapas del proceso

El proceso de reconstrucción sigue una secuencia fija:

1. **Instantánea del libro de registros** — lee el estado comprometido actual de todos los segmentos del [[worm-ledger-design|libro de registros WORM]]. El libro es de solo adición; la instantánea es el historial completo hasta el momento de inicio programado.
2. **Paso de extracción** — [[service-extraction|service-extraction]] entrega el texto del corpus a [[service-content|service-content]], que invoca al Doorman para la extracción de entidades restringida por gramática, produciendo registros de entidades estructurados para personas, organizaciones, activos y eventos. Esta es una llamada del Anillo 2 al Anillo 3, no un paso determinista — si estos registros quedan pendientes de revisión humana o se escriben directamente al grafo depende de la configuración del operador descrita arriba.
3. **Uniones por esquema** — los registros de entidades se unen con la taxonomía canónica y los índices de inteligencia de ubicación mediante relaciones de clave foránea explícitas. No hay coincidencia difusa en esta etapa.
4. **Construcción del grafo** — los registros unidos se ensamblan en el substrato de grafo consultable consumido por [[service-content|service-content]] y la [[doorman-protocol|capa de inferencia Doorman]].
5. **Intercambio** — el grafo completado reemplaza la instantánea anterior de forma atómica. Los consumidores de consultas pasan a la nueva versión en la siguiente solicitud tras el intercambio.

## Posición en la pila de substratos

La reconstrucción nocturna se sitúa entre el [[worm-ledger-design|libro de registros WORM]] (que acumula escrituras de solo adición durante el día) y el nivel de consulta (que lee el grafo completado más recientemente). Los consumidores del grafo de conocimiento siempre leen una instantánea estable, no un grafo parcialmente construido.

El mecanismo [[compounding-substrate]] hace que cada ciclo de reconstrucción herede el grafo anterior completo y añada encima los registros recién comprometidos. La precisión se acumula con el tiempo: una entidad que apareció en tres registros del libro de registros hace dos años y en doce el mes pasado tiene un nodo de grafo más rico que una entidad recién registrada — sin ningún paso de curación manual.

## Véase también

- [[compounding-substrate]] — el mecanismo por el cual cada ciclo de reconstrucción acumula el conocimiento anterior
- [[worm-ledger-design]] — el libro de registros de solo adición que alimenta el proceso de reconstrucción
- [[service-extraction]] — el servicio de extracción que produce los registros de entidades consumidos por la reconstrucción
- [[service-content]] — el servicio de consultas que lee el grafo completado
- [[doorman-protocol]] — el cliente de la capa de inferencia que consulta el grafo para obtener contexto de entidades
