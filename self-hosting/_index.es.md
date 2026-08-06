---
schema: foundry-doc-v1
title: "Autoalojamiento"
slug: self-hosting-index
category: self-hosting
type: topic
content_type: topic
index_type: thematic
index_scope: self-hosting
quality: complete
short_description: "Ejecutar la plataforma en infraestructura propia: iniciar las imágenes de aparato seL4, desplegar el motor wiki y conectar la inferencia local."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-04
editor: pointsav-engineering
paired_with: _index.md
---

**El autoalojamiento** significa ejecutar componentes de la plataforma en infraestructura que usted controla, en lugar de una instancia alojada — iniciar las imágenes de aparato seL4 publicadas, levantar el motor wiki sobre su propio contenido y conectar la puerta de enlace de inferencia a su propio hardware. Cada componente aquí se degrada con elegancia en lugar de negarse a iniciar: un despliegue con una sola pieza funcionando sigue siendo un despliegue válido y útil.

<!-- START-HERE-HIGHLIGHT: el motor lee este bloque para la tarjeta "empezar aquí"
     (reutiliza el componente cluster-card--start-here existente). No añadir más de una. -->

**Empiece aquí:** [[self-host-a-deployment|Autoalojar un despliegue]] — inicia las dos imágenes de aparato seL4 independientes (`os-totebox`, `app-orchestration-slm`) sobre las que se ejecuta todo lo demás en esta categoría.

<!-- END-START-HERE-HIGHLIGHT -->

## Poner la plataforma en marcha

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: getting-the-platform-running -->
- [[self-host-a-deployment|Autoalojar un despliegue]] — inicie las imágenes de aparato `os-totebox` y `app-orchestration-slm` bajo QEMU
- [[deploy-knowledge-instance|Desplegar una instancia de conocimiento]] — sirva una wiki de documentación, proyectos o corporativa desde una ruta de contenido local
<!-- END AUTO-GENERATED -->

## Conectar la inferencia

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: wiring-up-inference -->
- [[configure-doorman|Configurar la puerta de enlace Doorman]] — defina los extremos de Nivel A/B/C mediante variables de entorno, sin archivo de configuración
- [[run-local-slm-inference|Ejecutar inferencia SLM local]] — inicie el modelo local y envíe una solicitud a través de Doorman
<!-- END AUTO-GENERATED -->

Cada guía tiene sus propios prerrequisitos, pasos de verificación y procedimiento de
reversión; esta página no los repite. La operación cotidiana de un despliegue en marcha
está en [Cómo lo opera](/category/how-to).

## Véase también

- [Cómo lo opera](/category/how-to) — las guías operativas cotidianas restantes
- [Dónde se ejecuta](/category/infrastructure) — la arquitectura sobre la que se despliegan estas guías
- [Seguridad y confianza](/category/security) — el modelo de identidad y permisos en el que participan los despliegues autoalojados
