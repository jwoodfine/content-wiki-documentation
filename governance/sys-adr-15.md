---
schema: foundry-doc-v1
type: topic
slug: sys-adr-15
title: "SYS-ADR-15: Browser Cache Invalidation Protocol"
category: governance
language: en
paired_with: sys-adr-15.es.md
status: stub
last_edited: 2026-05-07
editor: pointsav-engineering
---

Architecture decision record requiring that all operator console pages be served with cache-disabling headers and versioned fetch parameters, eliminating stale browser-cached UI states that could cause routing errors.
