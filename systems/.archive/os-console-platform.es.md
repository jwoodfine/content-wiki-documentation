---
schema: foundry-doc-v1
title: "Plataforma os-console y arquitectura de cartuchos"
slug: os-console-platform
aliases:
  - os-console-platform
short_description: "os-console es un único binario en Rust con arquitectura de cartuchos que proporciona acceso nativo por teclado a los flujos de trabajo del Archivo Totebox mediante módulos navegados con teclas de función."
category: systems
type: topic
content_type: topic
status: archived
archived: 2026-07-31
archived_reason: "Fragmentación de contenido genuina con console-os.md y os-console-architecture.md — los tres describían el mismo producto (os-console) en profundidades técnicas superpuestas, con inconsistencias reales. Fusionado en un artículo canónico único, systems/os-console.md."
superseded_by: os-console
bcsc_class: public-disclosure-safe
last_edited: 2026-07-31
editor: pointsav-engineering
paired_with: os-console-platform.md
language: es
---

`os-console` es la interfaz de consola nativa de teclado de Woodfine — un único binario en Rust que proporciona acceso directo al [[totebox-archive|Archivo Totebox]], flujos de trabajo editoriales, registros de gobernanza y gestión de infraestructura desde una terminal. Se conecta a los servicios `os-*` de backend mediante [[machine-based-auth|autorización basada en máquinas]] y opera completamente sin conexión cuando los servicios de backend no están disponibles.

> **Dirección planificada.** Está prevista una reconstrucción para evolucionar os-console hacia un escritorio de entrada dual nativo del equipo anfitrión: varios cartuchos visibles simultáneamente, compatibilidad completa con ratón con paridad de teclado garantizada, una capa de movimiento y gráficos cinematográficos, y una superficie de visibilidad de capacidades en tiempo real. La arquitectura canónica y el programa de ingeniería se encuentran en `BRIEF-os-console-rebuild-2030.md`. Las descripciones a continuación reflejan la consola actual (según construida); las capacidades prospectivas están marcadas como planificadas o previstas.

## El binario

`os-console` es el artefacto desplegable: un binario, un proceso, todos los cartuchos compilados en él. Se ejecuta como una aplicación nativa en el sistema operativo anfitrión. Las plataformas de destino incluyen Linux Mint en el iMac de escritorio local y macOS 13 o posterior en estaciones de trabajo ejecutivas. Un modo de servidor SSH opcional, compilado con el indicador `--features ssh-server`, permite el acceso remoto a través del puerto 2222. La dirección planificada es el despliegue nativo en el equipo anfitrión, conectando a un Archivo Totebox remoto a través de internet mediante [[machine-based-auth|autorización basada en máquinas]].

## El chasis base: app-console-keys

`app-console-keys` es el chasis base siempre instalado dentro de `os-console`. Su relación con `os-console` es análoga a la que [[service-fs-architecture|`service-fs`]] tiene con `os-totebox`: es el componente mínimo requerido que debe estar presente; todo lo demás es opcional.

`app-console-keys` proporciona el rasgo `Cartridge` (la interfaz que todos los cartuchos implementan), el marco de navegación por teclas de función, la barra de estado que muestra el estado de la conexión de [[machine-based-auth|autorización basada en máquinas]] y la identidad de sesión, el cliente de autorización y la configuración basada en perfiles.

**Nota de nomenclatura:** "keys" en `app-console-keys` se refiere a teclas de función — F-keys. No se refiere a claves criptográficas. La autorización basada en máquinas es implementada por `system-gateway-mba`, un crate separado.

## Cartuchos

Cada crate `app-console-*` es un crate de biblioteca que implementa el rasgo `Cartridge`. Los cartuchos se compilan directamente en `os-console` — no se cargan dinámicamente ni se lanzan como subprocesos. Un cartucho que no está instalado tiene su ranura de tecla de función atenuada en la tira de pestañas.

Los cartuchos son opcionales excepto `app-console-keys` y `app-console-input` (F12). Una instalación que incluya únicamente `app-console-content` (F4) y `app-console-input` (F12) es un despliegue de os-console completo y válido para trabajo editorial.

## Mapa de teclas de función

La consola presenta doce ranuras direccionables mediante teclas de función. F12 está fijada como El Ancla — la [[input-machine|Máquina de Entrada]] — y nunca se mueve. El artículo [[console-os|os-console]] describe el diseño y contexto de despliegue del producto más amplio.

| Tecla F | Cartucho | Dominio |
|---|---|---|
| F1 | `app-console-help` | Panel de ayuda |
| F2 | `app-console-people` | Identidad y contactos |
| F3 | `app-console-email` | Comunicaciones |
| F4 | `app-console-content` | Editorial — corrección, redacción, verificación |
| F5 | `app-console-minutebook` | Gobernanza — actas, resoluciones |
| F6 | `app-console-bookkeeper` | Libro mayor financiero |
| F7 | `app-console-bim` | Gestión de información de construcción |
| F8 | `app-console-gis` | Información geográfica |
| F9 | `app-console-slm` | Gestión de IA y mercado de adaptadores |
| F10 | `app-console-mesh` | Gestión de malla de red |
| F11 | `app-console-system` | Estado de salud en vivo de los servicios `os-*` y estado de emparejamiento |
| F12 | `app-console-input` | El Ancla — Máquina de Entrada (SYS-ADR-10) |

## La barra de estado

La barra de estado de `app-console-keys` siempre es visible en la parte inferior de la consola y proporciona al operador un panorama situacional en tiempo real:

```
operador@woodfine | MBA LINK ACTIVE | F4: Content | Tier A | 00:04:23
```

El componente de identidad muestra el nombre de usuario y el inquilino establecidos durante la ceremonia de emparejamiento. El estado de autorización muestra `MBA LINK ACTIVE`, `MBA LINK INACTIVE <motivo>` o `MBA LINK PENDING`. El nombre de la ranura del cartucho activo, el nivel de SLM en uso (A para local, B para ráfaga en la nube, C para API de frontera) y la duración de la sesión completan la barra.

## Conectividad de autorización

`app-console-keys` mantiene conexiones salientes con los servicios `os-*` emparejados. Cada emparejamiento es independiente: la consola puede estar activa con `os-totebox` e inactiva con `os-privategit` simultáneamente.

Cuando el enlace de autorización está inactivo, os-console opera en modo solo local. El contenido almacenado en caché local permanece accesible. Las solicitudes a los servicios de backend `service-proofreader`, `service-input` y `service-content` fallan de manera controlada en lugar de bloquearse.

## Renderizado de PDF

`os-console` admite el renderizado de PDF dentro de la terminal mediante la biblioteca `pdfium-render` — bindings de Rust sobre pdfium de Chromium. Las páginas del PDF se renderizan como mapas de bits RGB y se muestran usando el protocolo gráfico Kitty como ruta principal, con Sixel como alternativa y un error para las terminales que no admiten ninguno de los dos. Esto es renderizado de píxeles, no extracción de texto.

## Ubicación en la Arquitectura de Tres Anillos

`os-console` es un cliente de la [[three-ring-architecture|Arquitectura de Tres Anillos]], no un anillo en sí mismo. Se conecta a los servicios del Anillo 1 a través de la capa de autorización — `service-input` vía F12, [[service-people|`service-people`]] vía F2, [[service-email|`service-email`]] vía F3, y `service-fs`; a los servicios del Anillo 2, incluyendo [[service-content|`service-content`]] y [[service-search|`service-search`]]; y al servicio del Anillo 3 [[service-slm|`service-slm`]] vía [[compounding-doorman|Doorman]] en `http://localhost:8011`. `os-console` es la interfaz humana mediante la cual un operador instruye a los anillos.

## Véase también

- [[console-os]] — descripción arquitectónica general de os-console como Libro Mayor de Comandos
- [[machine-based-auth]] — el mecanismo de autorización que utiliza os-console
- [[input-machine]] — El Ancla; puerta de ingesta obligatoria en F12
- [[three-ring-architecture]] — la arquitectura de anillos a la que se conecta os-console
- [[os-family-overview]] — la familia de ocho SO y cómo encaja os-console
- [[compounding-doorman]] — el límite de auditoría Doorman para el acceso a service-slm
