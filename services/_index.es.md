---
schema: foundry-doc-v1
title: "Servicios de la Plataforma"
slug: services-index
short_description: "Los servicios autónomos que implementan ingestión de límite Ring 1 y procesamiento de conocimiento determinista Ring 2 en la arquitectura de tres anillos de PointSav — agrupados por capa de anillo y función."
lang: es
category: services
type: topic
content_type: topic
quality: complete
index_type: thematic
index_scope: services
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-09-04
editor: pointsav-engineering
paired_with: _index.md
---

La arquitectura de tres anillos de PointSav asigna cada servicio a una capa con autoridad y dependencias definidas. Los servicios del Anillo 1 gestionan la ingesta por inquilino: cada uno acepta datos brutos de una fuente externa y los escribe en un libro durable. Los servicios del Anillo 2 proporcionan conocimiento y procesamiento determinista: leen del Anillo 1 y producen registros estructurados, grafos de conocimiento e índices de búsqueda. El Anillo 3 es un único servicio, service-slm, que lee del Anillo 2 y nunca escribe en él.

La plataforma funciona completamente a través de los Anillos 1 y 2 sin cómputo de IA — un despliegue puede excluir el Anillo 3 por completo, reduciendo la superficie de ataque y satisfaciendo los requisitos de aislamiento de red. Donde se incluye el Anillo 3, la pregunta de cumplimiento sobre si la IA ha tocado el registro autoritativo se responde de forma arquitectónica, no procedimental: los servicios del Anillo 2 pueden invocar al Anillo 3 para obtener propuestas de extracción o clasificación (la entrega de corpus de `service-extraction` a `service-content`, que llama al Doorman para la extracción de entidades restringida por gramática hacia el DataGraph, es una de esas vías), pero el Anillo 3 nunca escribe en el grafo de conocimiento, el libro mayor ni ningún almacén de registros estructurados. Toda propuesta aceptada entra al registro únicamente a través de una vía de escritura del Anillo 2 con un punto de control de aprobación humana.

<!-- START-HERE-HIGHLIGHT: el motor lee este bloque para la tarjeta "empezar aquí"
     (reutiliza el componente cluster-card--start-here existente). No añadir más de una. -->

**Empiece aquí:** [[service-fs]] — el servicio de sistema de archivos en el que escribe cada otro servicio del Anillo 1, y la base de la postura de auditoría WORM que asume el resto de esta categoría.

<!-- END-START-HERE-HIGHLIGHT -->

## Anillo 1 — Ingesta en el límite

Servicios de límite por inquilino. Cada uno se ejecuta como un proceso separado por inquilino y expone una interfaz de servidor de Protocolo de Contexto de Modelo.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: ring-1-boundary-ingest -->
- [[service-fs]] — El libro mayor inmutable Write-Once-Read-Many por inquilino que respalda cada registro escrito en la plataforma — una interfaz HTTP y MCP real e implementada sobre un registro de anexado encadenado por hash, con anclaje externo mensual a un registro público de transparencia.
- [[service-email]] — service-email extrae correo de un buzón de Microsoft Exchange vía EWS, escribe el mensaje en bruto en almacenamiento local y lo elimina del buzón de origen inmediatamente después de extraerlo — el buzón en la nube es un punto de tránsito, no una copia de registro.
- [[service-people]] — service-people es la superficie F2 en os-console — un servidor MCP sobre un libro de identidades de solo-anexado y respaldado por WORM, con tres herramientas: anexar, buscar y escanear correos por expresión regular.
- [[service-input]] — service-input migra por lotes material de referencia en markdown desde un archivo fuente hacia la canalización de ingesta de la plataforma, deduplicando por hash de contenido y validando contra el registro de libro mayor propio de cada archivo — con una herramienta complementaria que puntúa qué tan bien coincide la extracción posterior con ese libro mayor.
<!-- END AUTO-GENERATED -->

## Anillo 2 — Conocimiento y procesamiento

Servicios de procesamiento determinista. Cada uno lee del Anillo 1 y produce registros estructurados — ninguna varianza de IA entra en el registro autoritativo.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: ring-2-knowledge-and-processing -->
- [[service-extraction]] — service-extraction vigila un directorio en busca de cargas útiles JSON entrantes que llevan entidades clasificadas en el borde, escribe un registro de libro mayor por carga útil para el servicio objetivo, y puede puentear el mismo texto hacia la canalización de ingesta del DataGraph.
- [[service-content]] — service-content extrae entidades nombradas de cargas útiles en bruto mediante una canalización de modelos escalonada, las escribe en el grafo de conocimiento bajo un punto de control de revisión humana, y aloja las taxonomías de referencia de la plataforma.
- [[service-search]] — service-search es un servicio de búsqueda de texto completo Ring 2 diseñado pero no construido — un README describe un índice invertido basado en Tantivy, pero aún no existe código fuente.
- [[service-egress]] — service-egress comprime y fragmenta datos de correo locales para transferencia saliente, y solo elimina la fuente local una vez que una contraparte externa confirma la recepción con una prueba criptográfica — una válvula de liberación saliente, no una importación de la nube a local.
- [[archetypes-and-chart-of-accounts]] — El Plan de Cuentas y los once arquetipos son dos taxonomías de referencia que service-content carga en el grafo de conocimiento, dando a cada entidad clasificada una categoría estructural y una firma funcional.
<!-- END AUTO-GENERATED -->

## Anillo 3 — Puerta de IA

Un servicio abarca el Anillo 3. Lee del Anillo 2 y produce propuestas que un humano revisa; nunca escribe en el grafo de conocimiento ni en el libro.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: ring-3-ai-gateway -->
- [[service-slm]] — service-slm es la puerta de enlace de inferencia de IA de la plataforma — cada solicitud, local o remota, transita el límite de auditoría del Doorman y uno de tres niveles de cómputo antes de que se devuelva una respuesta.
- [[service-slm-yoyo-operational]] — Cómo operan el enrutador de inferencia de tres niveles de service-slm y la VM de ráfaga GPU Yo-Yo: el límite del Doorman, los niveles local y de ráfaga, la cola de aprendizaje, y el techo de costo por apagado en inactividad.
- [[service-slm-totebox-sysadmin]] — Una dirección planificada para service-slm: usar su canalización real y ya operativa de captura-y-veredicto para construir un asistente sysadmin de Totebox — la taxonomía de tareas específica y las herramientas descritas aquí aún no están construidas.
- [[service-slm-graph-store-migration]] — El almacén de grafos de service-slm ejecuta una reconstrucción nocturna — la extracción de entidades vía Doorman escribe directamente en el grafo al completarse, sin paso de revisión humana en el propio script de reconstrucción.
- [[yoyo-daily-enrichment-cycle]] — La ventana nocturna de dos fases en GPU que reconstruye el DataGraph y, una vez habilitada por completo, entrena pesos de adaptador para el modelo de lenguaje local — actualmente ejecutándose solo en modo DataGraph.
<!-- END AUTO-GENERATED -->

## Servicios especializados y de dominio

Servicios construidos para capacidades específicas de la plataforma.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: specialist-and-domain-services -->
- [[service-business-clustering]] — Un patrón espacial padre-hijo que convierte puntos minoristas en bruto en una entidad comercial por sitio físico, para que la canalización GIS razone sobre una ubicación una sola vez en lugar de una vez por cada inquilino colocalizado.
- [[service-places-filtering]] — Un paso de filtrado que conserva solo instituciones de nivel regional de los datos cívicos en bruto, para que los rankings de nivel GIS reflejen concentración institucional en lugar de cada clínica e instalación comunitaria.
- [[service-wallet-settlement]] — service-wallet es un libro mayor contable por inquilino planificado para ingresos de flujo inverso del mercado — aún no existe código; el diseño propone un libro firmado sin custodia en lugar de un riel de pago.
- [[message-courier]] — Un motor deliberadamente delgado que carga dinámicamente el script adaptador privado de un cliente y le entrega el control de ejecución — manteniendo cada detalle operativo de la lógica de automatización web de un cliente completamente fuera del código abierto.
- [[fs-anchor-emitter]] — Un binario de un solo uso que obtiene un punto de control firmado del libro mayor WORM desde service-fs, lo ancla en el registro público de transparencia Sigstore Rekor y escribe el resultado de vuelta — haciendo el estado del libro mayor auditable desde fuera de la plataforma.
- [[service-fs-data-lake]] — El lago de datos de la canalización GIS es su capa de almacenamiento fundamental — un almacén de archivos planos que guarda puntos geoespaciales sin procesar, disponible para cada paso descendente de la misma canalización. Distinto de service-fs, el libro mayor WORM separado de la plataforma.
- [[template-ledger]] — Mecanismo de distribución en service-email-template que sincroniza una copia autoritativa de cada plantilla aprobada con el correo del operador, eliminando la deriva de versiones.
- [[editorial-pipeline-three-stages]] — El contrato real, confirmado del lado cliente, de la canalización de corrección de la plataforma: un conjunto fijo de protocolos de idioma, una respuesta que informa qué nivel de cómputo se ejecutó y qué se degradó, y un veredicto humano binario que alimenta el corpus de entrenamiento.
- [[private-git-paid-customer-endpoint]] — El servidor de versiones binarias de software.pointsav.com verifica tokens de licencia Ed25519 y transmite binarios compilados — sin estado, sin registros de pago ni claves, con algunos productos servidos abiertamente sin verificación de licencia.
- [[service-pointsav-link]] — service-pointsav-link es un concepto de adaptador nombrado pero no construido para conectar un nodo os-* a una flota PointSav — no existe un paquete correspondiente en el monorepo hoy.
- [[service-vm-fleet]] — El controlador de flota mantiene una vista global de la capacidad de nodos en la malla WireGuard de la PPN y gestiona las decisiones de colocación de máquinas virtuales.
- [[service-vm-tenant]] — El proxy de inquilino aplica autenticación, aislamiento de espacio de nombres, límites de cuota y una pista de auditoría inmutable en el límite del cliente del pool de recursos VM de la PPN.
- [[poi-data-schema|Esquema de datos de puntos de interés]] — Las estructuras de registro de los datos de localización ingeridos de OpenStreetMap y de Overture Maps Foundation, normalizadas en un esquema JSONL unificado antes del análisis de agrupaciones. Los QID de Wikidata son el identificador principal de cadena, y un modelo padre-hijo resuelve los servicios auxiliares comarcados.
- [[regional-name-resolution-architecture|Arquitectura de resolución de nombres regionales]] — El motor de geocodificación inversa por capas y sin conexión que convierte las coordenadas de una agrupación en un nombre regional legible: sus conjuntos de límites, su orden de enrutamiento por país y el posprocesado que hace legibles los nombres en lengua de origen, sin ninguna llamada a API externa.
<!-- END AUTO-GENERATED -->

## Véase también

- [Sistemas Operativos](/systems/) — los sistemas operativos dentro de los cuales se ejecutan los servicios
- [Cómo Está Construido](/architecture/) — el modelo de tres anillos y los invariantes que rigen la interacción entre anillos
- [Dónde Se Ejecuta](/infrastructure/) — despliegue de flota y la capa física en la que se ejecutan los servicios
