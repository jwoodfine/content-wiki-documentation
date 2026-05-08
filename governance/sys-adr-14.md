---
schema: foundry-doc-v1
type: topic
slug: sys-adr-14
title: "SYS-ADR-14: UI and API Port Separation at Proxy Layer"
category: governance
language: en
paired_with: sys-adr-14.es.md
status: stub
last_edited: 2026-05-07
editor: pointsav-engineering
---

Architecture decision record establishing separate proxy routes for static UI assets (served from an edge web server) and live API commands (routed through the WireGuard mesh to the Rust backend), eliminating the Rust binary as a static file server.
