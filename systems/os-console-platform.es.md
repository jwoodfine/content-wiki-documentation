---
schema: foundry-doc-v1
title: "Plataforma os-console y arquitectura de cartuchos"
slug: os-console-platform
short_description: "os-console es un único binario en Rust con arquitectura de cartuchos que proporciona acceso nativo por teclado a los flujos de trabajo del Archivo Totebox mediante módulos navegados con teclas de función."
category: systems
type: topic
content_type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-06-23
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

## Mapa de teclas de función

La consola presenta doce ranuras direccionables mediante teclas de función. F12 está fijada como El Ancla — la [[input-machine|Máquina de Entrada]] — y nunca se mueve. El artículo [[console-os|os-console]] describe el diseño y contexto de despliegue del producto más amplio.

## La barra de estado

La barra de estado de `app-console-keys` siempre es visible en la parte inferior de la consola y proporciona al operador un panorama situacional en tiempo real:

```
operador@woodfine | MBA LINK ACTIVE | F4: Content | Tier A | 00:04:23
```

Cuando el enlace de autorización está inactivo, os-console opera en modo solo local. El contenido almacenado en caché local permanece accesible. Las solicitudes de servicios de backend fallan de manera controlada en lugar de bloquearse.

## Véase también

- [[console-os]] — descripción arquitectónica general de os-console como Libro Mayor de Comandos
- [[machine-based-auth]] — el mecanismo de autorización que utiliza os-console
- [[input-machine]] — El Ancla; puerta de ingesta obligatoria en F12
- [[three-ring-architecture]] — la arquitectura de anillos a la que se conecta os-console
- [[os-family-overview]] — la familia de ocho SO y cómo encaja os-console
- [[compounding-doorman]] — el límite de auditoría Doorman para el acceso a service-slm
