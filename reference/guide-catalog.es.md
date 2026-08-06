---
schema: foundry-doc-v1
title: "Índice de Guías para Desarrolladores"
slug: guide-catalog
short_description: "Índice de guías para desarrolladores de la plataforma PointSav — guías prácticas organizadas por tarea, desde la instalación de herramientas hasta el ciclo de sesión."
category: reference
type: topic
content_type: topic
status: stable
language_protocol: TRANSLATE-ES
last_edited: 2026-06-15
editor: pointsav-engineering
paired_with: guide-catalog.md
aliases:
  - developer-guide-index
---

> **Las guías operativas** para despliegues de plataforma se mantienen por separado en el catálogo de despliegue de flota Woodfine. Son documentos operativos para operadores del sistema y no se enumeran aquí.

El Índice de Guías para Desarrolladores enumera las guías prácticas de la plataforma PointSav, organizadas por área de interés del desarrollador. Cada guía cubre una tarea específica que un desarrollador realiza al construir con la plataforma o desplegarla. Para la arquitectura subyacente en la que se basa cada guía, siga los enlaces a los artículos dentro de cada guía.

Los manuales operativos internos para el despliegue de flota Woodfine no se incluyen aquí — son documentos operativos para aprovisionamiento y mantenimiento, no guías públicas para desarrolladores.

## Primeros pasos

Estas guías cubren los primeros pasos para un desarrollador nuevo en la plataforma: configurar el conjunto de herramientas, autenticar un dispositivo y abrir una sesión de trabajo.

- [[pair-a-new-device]] — registra un nuevo dispositivo con el servidor de emparejamiento y logra que se apruebe en la red
- [[install-toolchain]] — instala el compilador de Rust y el asistente de confirmación del nivel de preparación en una VM del espacio de trabajo
- [[open-first-totebox-session]] — abre una sesión de trabajo en un Archivo Totebox y navega por el ciclo de vida de la sesión
- [[explore-the-console]] — recorre el diseño de tres zonas de la TUI, la barra de estado y las ranuras de teclas de función por primera vez

## Trabajar en la consola

Estas guías cubren la interfaz de terminal de la plataforma y sus ranuras de Cartucho integradas.

- [[navigate-console-tui]] — el diseño real de pantalla y los campos de la barra de estado, y cómo cambiar de ranura sin perder estado
- [[use-f-key-model]] — qué hacen realmente F3, F9 y F12, corrigiendo dos comportamientos inventados
- [[read-the-command-ledger]] — pagine entradas del libro mayor y obtenga un punto de control firmado a través de la API HTTP real de service-fs
- [[run-first-slm-query]] — la ruta real hacia una primera solicitud de inferencia, ya que F9 no tiene ninguna interfaz de consulta

## Registros y almacenamiento

Estas guías cubren el libro mayor de auditoría WORM y las operaciones con datos de entidades.

- [[read-write-totebox-archives]] — protocolo de lectura al inicio de sesión, flujo de confirmación, preparación de borradores, buzón entre archivos
- [[verify-worm-ledger]] — verifique una entrada del libro mayor contra un punto de control obtenido, usando solo curl y SHA-256
- [[query-the-datagraph]] — las herramientas reales query_datagraph/get_entity_context, y por qué la disponibilidad del DataGraph no es un nivel de Doorman
- [[export-structured-data]] — las tres rutas de exportación reales, ya que una cuarta en una versión anterior de esta guía no existía

## Autorización de máquinas

Estas guías cubren los mecanismos de credenciales y admisión que determinan quién y qué
puede actuar sobre la plataforma — emparejamiento de dispositivos, tokens de capacidad
servicio a servicio, inscripción de nodos de flota y descargas de binarios firmadas. Son
mecanismos separados, no un solo sistema con nombres diferentes.

- [[pair-a-new-device]] — registra un dispositivo con el servidor de emparejamiento y logra que se apruebe en la malla WireGuard
- [[issue-capability-token]] — genera un token de capacidad firmado con Ed25519 y regístralo con un servicio par
- [[rotate-keys]] — reemplaza una credencial dentro de los límites reales de expiración de 24 horas del sistema; no existe mecanismo de revocación
- [[enroll-ppn-node]] — inicia el agente de latido por nodo y confírmalo en el controlador de la flota
- [[authenticate-binary-downloads]] — confirma un pedido y sigue la ruta de descarga firmada de una versión

Para el modelo de autorización que sustenta todas estas operaciones, consulta [[machine-based-auth]] y [[pairing-as-permission]].

## Escala multi-entidad

Estas guías cubren la operación de la plataforma a través de múltiples tenants, usuarios y nodos de flota.

- [[configure-tenant-namespace]] — el aprovisionamiento real basado en configuración en service-vm-tenant, ya que no existe ninguna API de registro
- [[scale-user-tiers]] — otorgue tokens con alcance de rol a medida que un equipo crece; no hay promoción/revocación, solo tokens nuevos
- [[add-a-fleet-node]] — inscribir un segundo nodo PPN en una flota en funcionamiento sin interrumpir los nodos existentes

## Integración y datos

Estas guías cubren el consumo de datos de la plataforma y la conexión de aplicaciones externas.

- [[build-a-colocation-map]] — carga un archivo PMTiles directamente en MapLibre; no existe API REST ni clave de API
- [[connect-osm-data-pipeline]] — ejecute el script real ingest-osm.py y registre una cadena en taxonomy.py
- [[federate-archives-via-content-mounts]] — monte el contenido de un segundo repositorio en una instancia en ejecución
- [[use-knowledge-mounts]] — el esquema real de [[mount]], y el riesgo real (un espacio de nombres compartido y plano, no aislado por montaje)

## Autoalojamiento

Estas guías cubren el despliegue y la ejecución de componentes de la plataforma en infraestructura controlada por el operador.

- [[self-host-a-deployment]] — aprovisiona una instancia de despliegue nombrada, inicia la pasarela y conéctala a la plataforma central
- [[configure-doorman]] — configurar las direcciones de nivel superior, los umbrales del interruptor de circuito y verificar el punto de conexión de salud
- [[deploy-knowledge-instance]] — compilar e iniciar `app-mediakit-knowledge` apuntando a una ruta de repositorio de contenido local
- [[run-local-slm-inference]] — iniciar el servicio SLM local, verificar el Nivel B de Doorman y enviar solicitudes de inferencia desde la consola o la API

## Véase también

- [[machine-based-auth]] — el modelo de autorización por hardware que sustenta todo el acceso a la plataforma
- [[totebox-orchestration-development]] — el modelo de orquestación de sesiones que rige el uso de los Archivos Totebox
- [[app-mediakit-knowledge]] — el motor wiki que sirve esta instancia de documentación
