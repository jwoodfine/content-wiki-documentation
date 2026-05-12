---
schema: foundry-doc-v1
type: topic
slug: sys-adr-07
title: "SYS-ADR-07: Enrutamiento de Ingesta Determinista y Probabilística"
category: governance
language: es
paired_with: sys-adr-07.md
status: stub
last_edited: 2026-05-07
editor: pointsav-engineering
---

Registro de decisión arquitectónica que exige la clasificación del tipo de carga útil de todos los datos entrantes antes del procesamiento: los datos estructurados se dirigen a motores de análisis determinista y el texto humano no estructurado se dirige al límite del modelo de lenguaje.
