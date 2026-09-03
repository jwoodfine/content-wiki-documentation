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
last_edited: 2026-08-22
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
- [[service-fs]] — El servicio de sistema de archivos: libro WORM de solo anexado, raíz de almacenamiento por inquilino, la base en la que escribe cada otro servicio del Anillo 1 — arquitectura, durabilidad y la postura de cumplimiento SEC 17a-4(f)/eIDAS/SOC 2 que habilita por construcción.
- [[service-email]] — Ingesta de correo electrónico: SMTP e IMAP, cargas útiles saneadas, Maildir de solo anexado en almacenamiento local en bloque.
- [[service-people]] — Libro de identidad: una superficie F2 de os-console que expone herramientas de anexado, búsqueda y escaneo de correo por expresión regular vía MCP, respaldada por un almacén que rechaza identidades en conflicto.
- [[service-input]] — Ingesta de documentos en el límite del Anillo 1: detecta el formato, enruta el contenido a analizadores específicos por formato y lo entrega a service-fs para su escritura en el libro WORM.
<!-- END AUTO-GENERATED -->

## Anillo 2 — Conocimiento y procesamiento

Servicios de procesamiento determinista. Cada uno lee del Anillo 1 y produce registros estructurados — ninguna varianza de IA entra en el registro autoritativo.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: ring-2-knowledge-and-processing -->
- [[service-extraction]] — El controlador central de tráfico del Anillo 2: elimina el formato propietario, construye Paquetes de Entidades, asigna IDs de transacción, enruta a servicios deterministas o a service-slm.
- [[service-content]] — El Motor de Gravedad: lee cargas útiles brutas de un Totebox, las ejecuta contra una taxonomía institucional, genera los documentos estructurados que publica una organización.
- [[service-search]] — Búsqueda de texto completo sobre Tantivy: un servicio de índice invertido diseñado pero no construido — hoy solo existe una descripción, sin código fuente.
- [[service-egress]] — Válvula de liberación física: los registros estructurados salen de la plataforma únicamente a través de este servicio.
- [[archetypes-and-chart-of-accounts]] — La taxonomía institucional: once arquetipos y un Plan de Cuentas que clasifican al personal y los documentos por posición estructural y rol funcional.
<!-- END AUTO-GENERATED -->

## Anillo 3 — Puerta de IA

Un servicio abarca el Anillo 3. Lee del Anillo 2 y produce propuestas que un humano revisa; nunca escribe en el grafo de conocimiento ni en el libro.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: ring-3-ai-gateway -->
- [[service-slm]] — El Portero: enrutamiento de IA entre niveles de cómputo local, de ráfaga y externo; libro de auditoría en cada llamada; todas las claves API retenidas en este límite.
- [[service-slm-yoyo-operational]] — Estado operativo de service-slm y la VM de ráfaga GPU Yo-Yo: configuración de Nivel A/B, cola de borradores de aprendizaje, techo de coste por apagado inactivo.
- [[service-slm-totebox-sysadmin]] — Una dirección planificada para service-slm como asistente sysadmin de Totebox, construida sobre la canalización real y ya operativa de entrenamiento por aprendizaje — la taxonomía de tareas específica es propuesta, aún no registrada.
- [[service-slm-graph-store-migration]] — El grafo de propiedades activo del DataGraph: reconstrucción nocturna en LadybugDB mediante extracción de entidades restringida por gramática a través del Doorman, escribiendo directamente sin paso de revisión propio.
- [[yoyo-daily-enrichment-cycle]] — La ventana diaria de lote de la VM de ráfaga GPU Yo-Yo: dos fases, reconstrucción del DataGraph y (una vez habilitado por completo) entrenamiento de adaptador — el entrenamiento se ejecuta actualmente en modo solo-marcador.
<!-- END AUTO-GENERATED -->

## Servicios especializados y de dominio

Servicios construidos para capacidades específicas de la plataforma.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: specialist-and-domain-services -->
- [[service-business-clustering]] — Convierte datos minoristas brutos en clústeres comerciales: esquema espacial padre-hijo, una entidad comercial por sitio.
- [[service-places-filtering]] — Filtra la infraestructura cívica e institucional para retener solo las instalaciones de grado regional en las clasificaciones GIS.
- [[service-wallet-settlement]] — Cartera y liquidación de pagos directos: un diseño de libro contable por inquilino planificado, aún no construido.
- [[message-courier]] — Motor de automatización web sin interfaz que conecta libros de identidad internos con portales web externos.
- [[fs-anchor-emitter]] — Puntos de control firmados del libro WORM a cadencia horaria, anclados a Sigstore Rekor mensualmente para auditabilidad externa.
- [[service-fs-data-lake]] — Data lake de archivos planos para el pipeline GIS: puntos geoespaciales brutos de fuentes abiertas, sin paso ETL.
- [[template-ledger]] — Distribuye plantillas de correo electrónico aprobadas al entorno de correo del operador; elimina la desviación de versiones entre el diseño de plantillas y la ejecución.
- [[editorial-pipeline-three-stages]] — Proceso de corrección en tres etapas ordenadas por costo: escaneo determinista de vocabulario prohibido, pasada mecánica con LanguageTool y una reescritura generativa enrutada a través de la capa de inferencia.
- [[private-git-paid-customer-endpoint]] — El servidor de versiones binarias detrás de software.pointsav.com: verifica tokens de licencia Ed25519 y transmite binarios compilados, sin almacenar registros de pago ni claves de firma.
- [[service-pointsav-link]] — Un concepto de diseño nombrado pero no construido para un adaptador de conexión a flota; no existe ningún paquete correspondiente en el monorepo hoy.
- [[service-vm-fleet]] — El servicio de colocación y registro del pool de recursos VM de la PPN: algoritmo de colocación de dos pasadas y estado de nodos impulsado por heartbeats.
- [[service-vm-tenant]] — El proxy de inquilino orientado al cliente del pool de recursos VM de la PPN: autenticación, aislamiento de espacio de nombres, aplicación de cuotas y una pista de auditoría inmutable.
- [[poi-data-schema|Esquema de datos de puntos de interés]] — Las estructuras de registro de los datos de localización ingeridos de OpenStreetMap y de Overture Maps Foundation, normalizadas en un esquema JSONL unificado antes del análisis de agrupaciones.
- [[regional-name-resolution-architecture|Arquitectura de resolución de nombres regionales]] — El motor de geocodificación inversa por capas y sin conexión que convierte las coordenadas de una agrupación en un nombre regional legible, sin ninguna llamada a API externa.
<!-- END AUTO-GENERATED -->

## Véase también

- [Sistemas Operativos](/systems/) — los sistemas operativos dentro de los cuales se ejecutan los servicios
- [Cómo Está Construido](/architecture/) — el modelo de tres anillos y los invariantes que rigen la interacción entre anillos
- [Dónde Se Ejecuta](/infrastructure/) — despliegue de flota y la capa física en la que se ejecutan los servicios
