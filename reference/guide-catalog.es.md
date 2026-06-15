---
schema: foundry-doc-v1
title: "Índice de Guías para Desarrolladores"
slug: guide-catalog
category: reference
type: topic
content_type: topic
status: stable
language_protocol: TRANSLATE-ES
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: guide-catalog.md
aliases:
  - developer-guide-index
---

El Índice de Guías para Desarrolladores enumera las guías prácticas de la plataforma PointSav, organizadas por área de interés del desarrollador. Cada guía cubre una tarea específica que un desarrollador realiza al construir con la plataforma o desplegarla. Para la arquitectura subyacente en la que se basa cada guía, siga los enlaces a los artículos dentro de cada guía.

Los manuales operativos internos para el despliegue de flota Woodfine no se incluyen aquí — son documentos operativos para aprovisionamiento y mantenimiento, no guías públicas para desarrolladores.

## Primeros pasos

Estas guías cubren los primeros pasos para un desarrollador nuevo en la plataforma: configurar el conjunto de herramientas, autenticar un dispositivo y abrir una sesión de trabajo.

- [[pair-a-new-device]] — registra un nuevo dispositivo y asígnale un nivel de emparejamiento (INPUT, USER o INTERFACE)
- [[install-toolchain]] — instala el compilador de Rust y el asistente de confirmación del nivel de preparación en una VM del espacio de trabajo
- [[open-first-totebox-session]] — abre una sesión de trabajo en un Archivo Totebox y navega por el ciclo de vida de la sesión
- [[explore-the-console]] — recorre el diseño de tres zonas de la TUI, la barra de estado y las ranuras de teclas de función por primera vez

## Trabajar en la consola

Estas guías cubren la interfaz de terminal de la plataforma y sus ranuras de Cartucho integradas.

- [[navigate-console-tui]] — definiciones de campos de la barra de estado, cambio de tecla de función, atajos de teclado universales
- [[use-f-key-model]] — asignaciones de ranuras predeterminadas, modelo de compilación de Cartucho, Email / SLM / Máquina de Entrada
- [[read-the-command-ledger]] — ver entradas del libro mayor WORM desde la pestaña LEDGER de F12, comprender tipos de entrada, exportar a formato C2SP
- [[run-first-slm-query]] — enviar un prompt de inferencia en F9 y leer el panel de salud del Doorman

## Registros y almacenamiento

Estas guías cubren el libro mayor de auditoría WORM y las operaciones con datos de entidades.

- [[read-write-totebox-archives]] — protocolo de lectura al inicio de sesión, flujo de confirmación, preparación de borradores, buzón entre archivos
- [[verify-worm-ledger]] — confirmar la integridad de la cadena de hash mediante SHA-256 y validar contra un punto de control Sigstore firmado
- [[query-the-datagraph]] — buscar entidades nombradas mediante consulta en texto plano, navegar relaciones, gestionar interrupciones del Nivel A
- [[export-structured-data]] — cuatro rutas de exportación por caso de uso: DataGraph, Markdown wiki, GeoJSON, tiles del libro mayor

## Autorización de máquinas

Estas guías cubren el emparejamiento criptográfico de dispositivos que controla el acceso a la plataforma.

- [[pair-a-new-device]] — el flujo de registro principal; los cuatro tipos de emparejamiento (ADMIN, INPUT, USER, INTERFACE)
- [[enroll-ppn-node]] — registrar un nodo de cómputo PPN con el controlador de flota y verificar el primer latido
- [[issue-capability-token]] — generar un token Ed25519 con alcance para un dispositivo o servicio
- [[rotate-keys]] — reemplazar un par de claves y su token mediante la secuencia de rotación en tres fases
- [[authenticate-binary-downloads]] — verificar y descargar binarios firmados desde el punto de distribución privado

Para el modelo de autorización que sustenta todas estas operaciones, consulta [[machine-based-auth]] y [[pairing-as-permission]].

## Escala multi-entidad

Estas guías cubren la operación de la plataforma a través de múltiples tenants, usuarios y nodos de flota.

- [[configure-tenant-namespace]] — registrar un espacio de nombres de tenant, establecer límites de cuota, verificar el aislamiento y emitir la credencial raíz
- [[scale-user-tiers]] — promover usuarios entre los niveles READ / USER / INPUT y actualizar masivamente un equipo
- [[add-a-fleet-node]] — inscribir un segundo nodo PPN en una flota en funcionamiento sin interrumpir los nodos existentes

## Integración y datos

Estas guías cubren el consumo de datos de la plataforma y la conexión de aplicaciones externas.

- [[build-a-colocation-map]] — autentícate contra la API de tiles SIG y renderiza marcadores de clústeres con color por nivel en MapLibre
- [[connect-osm-data-pipeline]] — escribir un YAML de ingestión de cadena, ejecutar el script de ingestión contra la API de Overpass y reconstruir la capa de clústeres
- [[federate-archives-via-content-mounts]] — declara un montaje de contenido secundario en `knowledge.toml` y accede a artículos federados entre instancias
- [[use-knowledge-mounts]] — añadir un repositorio de contenido secundario a una instancia wiki en ejecución y verificar el aislamiento de slugs

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
