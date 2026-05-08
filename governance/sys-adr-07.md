---
schema: foundry-doc-v1
type: topic
slug: sys-adr-07
title: "SYS-ADR-07: Deterministic and Probabilistic Ingestion Routing"
category: governance
language: en
paired_with: sys-adr-07.es.md
status: stub
last_edited: 2026-05-07
editor: pointsav-engineering
---

Architecture decision record requiring that all inbound data be classified by payload type before processing — structured data routes to deterministic parsing engines; unstructured human text routes to the language model boundary.
