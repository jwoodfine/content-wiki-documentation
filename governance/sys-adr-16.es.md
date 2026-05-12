---
schema: foundry-doc-v1
type: topic
slug: sys-adr-16
title: "SYS-ADR-16: Malla Unicast a Nivel de Aplicación sobre WireGuard"
category: governance
language: es
paired_with: sys-adr-16.md
status: stub
last_edited: 2026-05-07
editor: pointsav-engineering
---

Registro de decisión arquitectónica que reemplaza la difusión UDP nativa, incompatible con el enrutamiento de Capa 3 de WireGuard, con un bucle unicast a nivel de aplicación que entrega comandos a cada nodo par de forma individual.
