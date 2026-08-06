---
schema: foundry-doc-v1
title: "Guías para Desarrolladores"
slug: how-to
category: how-to
type: topic
content_type: topic
quality: complete
short_description: "Guías paso a paso para desarrolladores: configuración del entorno, navegación de la TUI de consola, operaciones del ledger WORM y escala multi-entidad de la plataforma PointSav. El emparejamiento de dispositivos y los tokens de capacidad ahora viven en Autorización de Máquinas; el despliegue autoalojado ahora vive en Autoalojamiento."
status: active
bcsc_class: public-disclosure-safe
language_protocol: TRANSLATE-ES
index_type: thematic
index_scope: how-to
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: _index.md
---

Guías paso a paso para construir con y sobre la plataforma PointSav. Cada guía aborda una tarea específica; síguelas de principio a fin y consulta los artículos de arquitectura relacionados cuando necesites la teoría subyacente.

Para los conceptos detrás de cada guía, comienza en [[architecture|Arquitectura]] o [[patterns-index|Patrones]]. Para una visión general de la arquitectura de la plataforma, consulta [[totebox-orchestration-development]].

<!-- START-HERE-HIGHLIGHT: el motor lee este bloque para la tarjeta "empezar aquí"
     (reutiliza el componente cluster-card--start-here existente). No añadir más de una. -->

**Empiece aquí:** [[install-toolchain|Instalar el conjunto de herramientas de desarrollo]] — el primer paso para cualquier nuevo colaborador, antes de abrir una sesión o explorar la consola.

<!-- END-START-HERE-HIGHLIGHT -->

## Primeros pasos

La base: instala el conjunto de herramientas y abre tu primera sesión.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: getting-started -->
- [[pair-a-new-device|Vincular un nuevo dispositivo]] — registra un dispositivo con el servidor de emparejamiento y logra que se apruebe en la red (ahora parte de [Autorización de Máquinas](/category/machine-authorization))
- [[install-toolchain|Instalar el conjunto de herramientas de desarrollo]] — configura Rust y el asistente de confirmación del nivel de preparación en una VM del espacio de trabajo
- [[open-first-totebox-session|Abrir tu primera sesión Totebox]] — navega a un archivo, lee tu bandeja de entrada y empieza a contribuir
- [[explore-the-console|Explorar la consola]] — recorre el diseño de tres zonas de la TUI, la barra de estado y las ranuras de teclas de función
<!-- END AUTO-GENERATED -->

## Trabajar en la consola

Usa la interfaz de terminal de la plataforma y sus Cartuchos integrados.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: working-in-the-console -->
- [[navigate-console-tui|Navegar la TUI de la consola]] — el diseño real de pantalla y los campos de la barra de estado
- [[use-f-key-model|Usar el modelo de teclas de función]] — qué hacen realmente F3, F9 y F12
- [[read-the-command-ledger|Leer el libro mayor de comandos]] — pagine entradas y obtenga un punto de control firmado a través de la API HTTP real de service-fs
- [[run-first-slm-query|Ejecutar tu primera consulta SLM]] — la ruta real hacia una primera solicitud de inferencia
<!-- END AUTO-GENERATED -->

## Registros y almacenamiento

Trabaja con el libro mayor de auditoría WORM y los datos de entidades.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: records-and-storage -->
- [[read-write-totebox-archives|Leer y escribir en archivos Totebox]] — protocolo de lectura al inicio de sesión, flujo de confirmación, preparación de borradores, buzón entre archivos
- [[verify-worm-ledger|Verificar una entrada del libro mayor WORM]] — verifique contra un punto de control obtenido, usando solo curl y SHA-256
- [[query-the-datagraph|Consultar el DataGraph]] — las herramientas reales query_datagraph/get_entity_context
- [[export-structured-data|Exportar datos estructurados]] — tres rutas de exportación reales: DataGraph, Markdown wiki, entradas del libro mayor
<!-- END AUTO-GENERATED -->

## Escala multi-entidad

Gestiona múltiples tenants, usuarios y nodos de flota.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: multi-entity-scale -->
- [[configure-tenant-namespace|Configurar un espacio de nombres de tenant]] — el aprovisionamiento real basado en configuración, ya que no existe ninguna API de registro
- [[scale-user-tiers|Escalar el acceso de usuarios]] — otorgue tokens con alcance de rol a medida que un equipo crece; no hay promoción/revocación
- [[add-a-fleet-node|Añadir un nodo a una flota en funcionamiento]] — inscribir un segundo nodo sin interrumpir las operaciones de la flota existente
<!-- END AUTO-GENERATED -->

## Integración y datos

Conecta tuberías de datos externas y crea aplicaciones de inteligencia de ubicación.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: integration-and-data -->
- [[build-a-colocation-map|Construir un mapa de co-ubicación]] — carga un archivo PMTiles directamente; no existe API REST ni clave de API
- [[connect-osm-data-pipeline|Conectarse al pipeline de datos OSM]] — el script real ingest-osm.py y el registro en taxonomy.py
- [[federate-archives-via-content-mounts|Federar archivos mediante montajes de contenido]] — monte el contenido de un segundo repositorio en una instancia en ejecución
- [[use-knowledge-mounts|Usar montajes de conocimiento declarativos]] — el esquema real de [[mount]] y su riesgo real de colisión de slugs sin mitigar
<!-- END AUTO-GENERATED -->

El emparejamiento de dispositivos, los tokens de capacidad y la inscripción de flota ahora tienen su propia categoría — véase [Autorización de Máquinas](/category/machine-authorization). El despliegue autoalojado ahora tiene su propia categoría — véase [Autoalojamiento](/category/self-hosting).

## Véase también

- [[architecture/_index|Arquitectura]] — arquitectura transversal de la plataforma
- [[patterns/_index|Patrones]] — patrones de diseño nombrados utilizados en toda la plataforma
- [[totebox-session]] — qué es una sesión Totebox y qué puede hacer
- [[machine-based-auth]] — cómo funciona la autorización basada en máquinas
- [Autorización de Máquinas](/category/machine-authorization) — emparejamiento de dispositivos, tokens de capacidad, inscripción de flota y autenticación de descargas de binarios
- [Autoalojamiento](/category/self-hosting) — desplegar componentes de la plataforma en tu propia infraestructura
