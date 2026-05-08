---
schema: foundry-doc-v1
type: topic
slug: sys-adr-14
title: "SYS-ADR-14: Separación de Puertos de Interfaz y API en la Capa de Proxy"
category: governance
language: es
paired_with: sys-adr-14.md
status: stub
last_edited: 2026-05-07
editor: pointsav-engineering
---

Registro de decisión arquitectónica que establece rutas de proxy separadas para activos de interfaz estáticos (servidos desde un servidor web perimetral) y comandos de API en tiempo real (enrutados a través de la malla WireGuard al backend en Rust).
