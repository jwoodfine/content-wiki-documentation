---
schema: foundry-doc-v1
document_version: 0.1.0
title: "documentation.pointsav.com entra en operación (2026-04-27)"
slug: topic-documentation-pointsav-com-launch-2026-04-27
category: milestones
status: published
last_edited: 2026-04-27
editor: pointsav-engineering
audience: vendor-public
bcsc_class: current-fact
language_protocol: PROSE-TOPIC
lang: es
paired_with: topic-documentation-pointsav-com-launch-2026-04-27.md
cites:
  - ni-51-102
  - osc-sn-51-721
---

## Resumen estratégico

El 27 de abril de 2026, a las 16:25 UTC, `https://documentation.pointsav.com` entró en operación pública con TLS bajo la versión de workspace v0.1.29. El sitio sirve el wiki de ingeniería de PointSav — `app-mediakit-knowledge` — sobre un certificado Let's Encrypt válido hasta el 26 de julio de 2026, con renovación automática habilitada mediante certbot.

## La plataforma de servicio

La infraestructura es convencional: Linux, nginx, systemd y Let's Encrypt. El binario compilado en Rust se instala en `/usr/local/bin/app-mediakit-knowledge`, se ejecuta como usuario sin privilegios en el puerto de loopback 9090, y el vhost de nginx expone los puertos 80 (redireccionamiento HTTP→HTTPS y desafíos ACME) y 443 (TLS terminado). La configuración del servicio systemd está versionada como Infraestructura-como-Código en `~/Foundry/infrastructure/local-knowledge/local-knowledge.service`.

El lanzamiento expuso una brecha operacional no detectada previamente: el firewall de sistema operativo (`ufw`) sólo permitía el puerto 22/tcp, a pesar de que el firewall de GCP ya autorizaba los puertos 80 y 443. La corrección se integró en v0.1.29 —`configure-ubuntu-foundry.sh` ahora incluye esas reglas— para que futuras provisiones de VM hereden la configuración completa.

## Contenido actual y postura BCSC

El dominio sirve hoy cuatro páginas TOPIC de marcador de posición (`/wiki/welcome`, `/wiki/sample-article`, `/wiki/sample-forward-looking`, `/wiki/sample-citations`), redactadas específicamente para cumplir con la postura de divulgación continua que exige NI 51-102 desde el primer carácter `[ni-51-102]`. El corpus heredado de más de 30 TOPICs se retiene en espera de un paso editorial del cluster project-language; su publicación constituirá un único evento de cambio material en lugar de múltiples eventos separados.

Esta decisión es deliberada: cuatro archivos BCSC-limpios habilitan la evaluación de la interfaz de usuario en la URL pública sin que el calendario de limpieza editorial bloquee el lanzamiento técnico.

## Perspectivas futuras

Las siguientes afirmaciones son *planificadas*, no *comprometidas*. Aplica lenguaje cautelar conforme a `[ni-51-102]` y `[osc-sn-51-721]`; la base razonable es la trayectoria de los clusters project-knowledge y project-language a 2026-04-27. Los supuestos materiales incluyen la disponibilidad continua del VM, la ratificación del pipeline editorial del cluster project-language y la autorización del operador para la revisión BP1 de la Fase 4 del motor wiki.

El motor wiki *prevé* desarrollarse en fases posteriores: Fase 4 (commit vía git2, historial mediante gix, grafo de wikilinks en redb, servidor MCP vía rmcp), Fase 5 (gestión de imágenes y activos), Fase 6 (configuración por tenant para wikis del Cliente), Fase 7 (federación y recuperación por contenido-direccionado) y Fase 8 (linter que incorpora invariantes de clase de divulgación en verificaciones en tiempo de compilación). El cluster project-language *planea* refinar el corpus heredado en un paso editorial separado, tras lo cual `--content-dir` *podrá* apuntar al árbol de contenido ratificado. Estos planes *pueden* modificarse en función de decisiones del operador, requisitos del cliente o cambios en la doctrina del sustrato.
