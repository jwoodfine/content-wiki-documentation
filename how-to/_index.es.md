---
schema: foundry-doc-v1
title: "Guías para Desarrolladores"
slug: how-to
category: how-to
type: topic
content_type: topic
quality: complete
short_description: "Guías paso a paso para desarrolladores: emparejamiento de dispositivos, configuración del entorno, navegación de la TUI de consola, operaciones del ledger WORM y despliegue autohospedado de la plataforma PointSav."
status: active
bcsc_class: public-disclosure-safe
language_protocol: TRANSLATE-ES
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: _index.md
---

Guías paso a paso para construir con y sobre la plataforma PointSav. Cada guía aborda una tarea específica; síguelas de principio a fin y consulta los artículos de arquitectura relacionados cuando necesites la teoría subyacente.

Para los conceptos detrás de cada guía, comienza en [[architecture|Arquitectura]] o [[patterns-index|Patrones]]. Para una visión general de la arquitectura de la plataforma, consulta [[totebox-orchestration-development]].

## Primeros pasos

La base: autentica tu dispositivo, instala el conjunto de herramientas y abre tu primera sesión.

- [[pair-a-new-device|Vincular un nuevo dispositivo]] — registra un dispositivo con el servidor de emparejamiento y logra que se apruebe en la red (ahora parte de [Autorización de Máquinas](/category/machine-authorization))
- [[install-toolchain|Instalar el conjunto de herramientas de desarrollo]] — configura Rust y el asistente de confirmación del nivel de preparación en una VM del espacio de trabajo
- [[open-first-totebox-session|Abrir tu primera sesión Totebox]] — navega a un archivo, lee tu bandeja de entrada y empieza a contribuir
- [[explore-the-console|Explorar la consola]] — recorre el diseño de tres zonas de la TUI, la barra de estado y las ranuras de teclas de función

## Trabajar en la consola

Usa la interfaz de terminal de la plataforma y sus Cartuchos integrados.

- [[navigate-console-tui|Navegar la TUI de la consola]] — el diseño real de pantalla y los campos de la barra de estado
- [[use-f-key-model|Usar el modelo de teclas de función]] — qué hacen realmente F3, F9 y F12
- [[read-the-command-ledger|Leer el libro mayor de comandos]] — pagine entradas y obtenga un punto de control firmado a través de la API HTTP real de service-fs
- [[run-first-slm-query|Ejecutar tu primera consulta SLM]] — la ruta real hacia una primera solicitud de inferencia

## Registros y almacenamiento

Trabaja con el libro mayor de auditoría WORM y los datos de entidades.

- [[read-write-totebox-archives|Leer y escribir en archivos Totebox]] — protocolo de lectura al inicio de sesión, flujo de confirmación, preparación de borradores, buzón entre archivos
- [[verify-worm-ledger|Verificar una entrada del libro mayor WORM]] — confirmar la integridad de la cadena de hash y validar contra un punto de control Sigstore firmado
- [[query-the-datagraph|Consultar el DataGraph]] — buscar entidades nombradas, navegar relaciones, manejar interrupciones del Nivel A
- [[export-structured-data|Exportar datos estructurados]] — cuatro rutas de exportación: DataGraph, Markdown wiki, GeoJSON, tiles del libro mayor

## Escala multi-entidad

Gestiona múltiples tenants, usuarios y nodos de flota.

- [[configure-tenant-namespace|Configurar un espacio de nombres de tenant]] — registrar un tenant, establecer cuotas, verificar el aislamiento, emitir la credencial raíz
- [[scale-user-tiers|Escalar los niveles de acceso de usuario]] — promover usuarios entre los niveles READ / USER / INPUT y actualizar masivamente un equipo
- [[add-a-fleet-node|Añadir un nodo a una flota en funcionamiento]] — inscribir un segundo nodo sin interrumpir las operaciones de la flota existente

## Integración y datos

Conecta tuberías de datos externas y crea aplicaciones de inteligencia de ubicación.

- [[build-a-colocation-map|Construir un mapa de co-ubicación]] — consulta la API del motor GIS y renderiza una capa de clústeres con MapLibre
- [[connect-osm-data-pipeline|Conectarse al pipeline de datos OSM]] — escribir un YAML de ingestión de cadena, ejecutar el script de ingestión y reconstruir la capa de clusters
- [[federate-archives-via-content-mounts|Federar archivos mediante montajes de contenido]] — monta contenido wiki de un archivo en una segunda instancia usando montajes TOML declarativos
- [[use-knowledge-mounts|Usar montajes de conocimiento declarativos]] — añadir un repositorio de contenido secundario a una instancia wiki en ejecución a través de knowledge.toml

## Autoalojamiento

Despliega la plataforma en tu propia infraestructura.

- [[self-host-a-deployment|Autoalojar un despliegue]] — provisiona un archivo Totebox en un nodo de cómputo compatible
- [[configure-doorman|Configurar el gateway Doorman]] — establecer las direcciones de nivel superior, los umbrales del interruptor de circuito y verificar el endpoint de salud
- [[deploy-knowledge-instance|Desplegar una instancia de conocimiento]] — compilar e iniciar app-mediakit-knowledge apuntando a un repositorio de contenido local
- [[run-local-slm-inference|Ejecutar inferencia SLM local]] — iniciar el servicio SLM, verificar el Nivel B de Doorman y enviar solicitudes de inferencia desde la consola o la API

## Véase también

- [[architecture/_index|Arquitectura]] — arquitectura transversal de la plataforma
- [[patterns/_index|Patrones]] — patrones de diseño nombrados utilizados en toda la plataforma
- [[totebox-session]] — qué es una sesión Totebox y qué puede hacer
- [[machine-based-auth]] — cómo funciona la autorización basada en máquinas
- [Autorización de Máquinas](/category/machine-authorization) — emparejamiento de dispositivos, tokens de capacidad, inscripción de flota y autenticación de descargas de binarios
- [Autoalojamiento](/category/self-hosting) — desplegar componentes de la plataforma en tu propia infraestructura
