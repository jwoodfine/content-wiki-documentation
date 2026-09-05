---
schema: foundry-doc-v1
title: "Cómo Lo Operas"
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
last_edited: 2026-09-04
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
- [[install-toolchain|Instalar el conjunto de herramientas de desarrollo]] — Instala el conjunto de herramientas Rust fijado con rustup, ejecuta una compilación y pruebas base, y verifica el asistente de commits y la clave SSH de firma necesarios antes de trabajar en un archivo del monorepo.
- [[open-first-totebox-session|Abrir tu primera sesión Totebox]] — Abre una primera sesión Totebox en un único archivo: lea el manifiesto, revise su bandeja de entrada, entienda qué puede y no puede escribir la sesión, y complete el barrido de cierre antes de cerrar.
- [[explore-the-console|Explorar la consola]] — Orienta a un operador de primera vez en os-console — la barra de estado, el panel F9 de la pasarela de inferencia y el punto de control obligatorio F12 que escribe en el libro mayor WORM.
<!-- END AUTO-GENERATED -->

## Trabajar en la consola

Usa la interfaz de terminal de la plataforma y sus Cartuchos integrados.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: working-in-the-console -->
- [[navigate-console-tui|Navegar la TUI de la consola]] — Navega os-console por teclado — la barra de teclas de función arriba, los campos reales de la barra de estado abajo, y el cambio de ranuras sin perder estado.
- [[use-f-key-model|Usar el modelo de teclas de función]] — Trabaja con el modelo de cartuchos de tecla de función de os-console — correo en F3, el panel SLM de solo monitoreo en F9, la Máquina de Entrada basada en archivos en F12 — donde cada cartucho compilado posee el renderizado y la entrada de su ranura.
- [[read-the-command-ledger|Leer el libro mayor de comandos]] — Lee el libro mayor WORM de solo anexado a través de la API HTTP real de service-fs — paginando entradas con un cursor y obteniendo un punto de control firmado — ya que no existe ninguna interfaz de navegación del libro mayor en la consola.
- [[run-first-slm-query|Ejecutar tu primera consulta SLM]] — Envía una primera solicitud de inferencia directamente a Doorman por HTTP — la ruta real, ya que la ranura F9 de la consola es un panel de monitoreo sin ninguna interfaz de consulta.
<!-- END AUTO-GENERATED -->

## Registros y almacenamiento

Trabaja con el libro mayor de auditoría WORM y los datos de entidades.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: records-and-storage -->
- [[read-write-totebox-archives|Leer y escribir en archivos Totebox]] — Lee el estado de un archivo Totebox al inicio de sesión — bandeja de entrada, contexto de sesión, git status, NEXT.md — y registra cambios mediante el flujo de commit de nivel staging.
- [[verify-worm-ledger|Verificar una entrada del libro mayor WORM]] — Verifica entradas del libro mayor WORM contra un punto de control obtenido a través de la API HTTP real de service-fs, usando un conjunto de herramientas SHA-256 estándar — no existe ni se necesita ninguna CLI ni herramienta propietaria.
- [[query-the-datagraph|Consultar el DataGraph]] — Consulta el DataGraph para obtener el estado actual de entidades con las herramientas MCP reales query_datagraph y get_entity_context, y maneja la indisponibilidad del DataGraph como su propia señal, separada de los niveles de inferencia de Doorman.
- [[export-structured-data|Exportar datos estructurados]] — Exporta datos de la plataforma por tres rutas reales — registros de entidades del DataGraph a través de herramientas MCP, Markdown wiki leído directamente de git, y entradas de libro mayor paginadas a través de la API HTTP de service-fs.
<!-- END AUTO-GENERATED -->

## Escala multi-entidad

Gestiona múltiples tenants, usuarios y nodos de flota.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: multi-entity-scale -->
- [[configure-tenant-namespace|Configurar un espacio de nombres de tenant]] — Configura un espacio de nombres de tenant en service-vm-tenant mediante variables de entorno y un reinicio — el mecanismo real basado en configuración, ya que no existe ninguna API de registro de tenants en tiempo de ejecución.
- [[scale-user-tiers|Escalar el acceso de usuarios]] — Otorga tokens de capacidad con alcance de rol a nuevos usuarios a medida que un equipo crece, usando la API real de emparejamiento de service-content — no existe una operación de promoción/degradación ni de revocación masiva, ya que no existe ningún mecanismo de revocación.
- [[add-a-fleet-node|Añadir un nodo a una flota en funcionamiento]] — Añade un segundo nodo a una flota PPN ya en funcionamiento usando la configuración real por variables de entorno de service-vm-host — el mismo mecanismo que el primer nodo, ya que nada cambia en la inscripción una vez que existe una flota.
<!-- END AUTO-GENERATED -->

## Integración y datos

Conecta tuberías de datos externas y crea aplicaciones de inteligencia de ubicación.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: integration-and-data -->
- [[build-a-colocation-map|Construir un mapa de co-ubicación]] — Renderiza marcadores de clúster de co-ubicación coloreados por nivel en MapLibre GL cargando un archivo PMTiles directamente — la arquitectura real de archivo plano, ya que no existe ninguna API REST de clústeres con token bearer.
- [[connect-osm-data-pipeline|Conectarse al pipeline de datos OSM]] — Ingiere una nueva cadena minorista o de servicios desde OpenStreetMap usando el script real ingest-osm.py y los diccionarios CATEGORIES/BRAND_FILL de taxonomy.py, y luego reconstruye los tiles de clúster servibles.
- [[federate-archives-via-content-mounts|Federar archivos mediante montajes de contenido]] — Federa los artículos de una segunda instancia de conocimiento en una instancia en ejecución mediante una entrada [[mount]] en knowledge.toml — un espacio de nombres plano y combinado sin aislamiento, no un esquema de federación con prefijo de URL.
- [[use-knowledge-mounts|Usar montajes de conocimiento declarativos]] — Añade un repositorio de contenido secundario a una instancia de conocimiento en ejecución mediante una entrada [[mount]] en knowledge.toml — al mismo espacio de nombres de slugs plano que el primario, ya que no existe ningún aislamiento por prefijo de URL.
<!-- END AUTO-GENERATED -->

El emparejamiento de dispositivos, los tokens de capacidad y la inscripción de flota ahora tienen su propia categoría — véase [Autorización de Máquinas](/category/machine-authorization). El despliegue autoalojado ahora tiene su propia categoría — véase [Autoalojamiento](/category/self-hosting).

## Herramientas financieras y de construcción

Ejecute las herramientas de dominio de la plataforma — el libro mayor de costes, cronograma y calidad de construcción y sus herramientas hermanas de contabilidad y nóminas. Todas son herramientas de línea de comandos; ninguna tiene hoy una pantalla de consola.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: financial-construction-tools -->
- [[generate-a-construction-cost-estimate|Generar un informe de estimación de costes de construcción]] — Ejecuta el binario de informes de construcción sobre un directorio de datos CSV para producir informes de costes y de cronograma en HTML y PDF, con registros de conciliación y validación — la única interfaz existente, ya que la herramienta no tiene pantalla de consola ni analiza argumento alguno de línea de comandos.
- [[generate-a-financial-statement-package|Generar un paquete de estados financieros]] — Ejecuta el binario de estados para un ejercicio y un período concretos y produce un paquete consolidado en HTML y PDF, recalculado desde los CSV de asientos en cada ejecución — la herramienta se niega a representar antes que publicar una cifra que no cuadra.
- [[generate-a-payroll-register|Generar un registro de nóminas]] — Ejecuta el binario de nóminas para agregar las horas de mano de obra presupuestadas por división en un registro HTML y PDF — un informe estrecho que no calcula salario bruto, ni frecuencia de pago, ni remisión, y que imprime una raya en lugar de una cifra allí donde no la tiene.
<!-- END AUTO-GENERATED -->

## Véase también

- [[architecture-index|Arquitectura]] — arquitectura transversal de la plataforma
- [[patterns-index|Patrones]] — patrones de diseño nombrados utilizados en toda la plataforma
- [[totebox-session]] — qué es una sesión Totebox y qué puede hacer
- [[machine-based-auth]] — cómo funciona la autorización basada en máquinas
- [Autorización de Máquinas](/category/machine-authorization) — emparejamiento de dispositivos, tokens de capacidad, inscripción de flota y autenticación de descargas de binarios
- [Autoalojamiento](/category/self-hosting) — desplegar componentes de la plataforma en tu propia infraestructura
