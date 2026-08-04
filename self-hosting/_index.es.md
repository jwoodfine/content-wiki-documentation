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

**Empiece aquí:** [Autoalojar un despliegue](/es/wiki/self-host-a-deployment) — inicia las dos imágenes de aparato seL4 independientes (`os-totebox`, `app-orchestration-slm`) sobre las que se ejecuta todo lo demás en esta categoría.

<!-- END-START-HERE-HIGHLIGHT -->

## Poner la plataforma en marcha

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: getting-the-platform-running -->
- [Autoalojar un despliegue](/es/wiki/self-host-a-deployment) — inicie las imágenes de aparato `os-totebox` y `app-orchestration-slm` bajo QEMU
- [Desplegar una instancia de conocimiento](/es/wiki/deploy-knowledge-instance) — sirva una wiki de documentación, proyectos o corporativa desde una ruta de contenido local
<!-- END AUTO-GENERATED -->

## Conectar la inferencia

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: wiring-up-inference -->
- [Configurar la puerta de enlace Doorman](/es/wiki/configure-doorman) — defina los extremos de Nivel A/B/C mediante variables de entorno, sin archivo de configuración
- [Ejecutar inferencia SLM local](/es/wiki/run-local-slm-inference) — inicie el modelo local y envíe una solicitud a través de Doorman
<!-- END AUTO-GENERATED -->

## Lo que esto no es

Esta página no sustituye la lectura de las guías enlazadas — cada una tiene sus propios prerrequisitos, pasos de verificación y procedimiento de reversión que esta página no repite. No cubre la operación cotidiana de la plataforma una vez que un despliegue está en marcha (emparejar dispositivos, emitir tokens, escalar el acceso) — esas guías permanecen en [Cómo lo opera](/category/how-to) hasta que reciban el mismo tratamiento de categoría en una fase posterior.

## Véase también

- [Cómo lo opera](/category/how-to) — las guías operativas cotidianas restantes
- [Dónde se ejecuta](/category/infrastructure) — la arquitectura sobre la que se despliegan estas guías
- [Seguridad y confianza](/category/security) — el modelo de identidad y permisos en el que participan los despliegues autoalojados
