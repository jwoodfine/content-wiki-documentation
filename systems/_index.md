---
schema: foundry-doc-v1
title: "Systems — Category Landing"
slug: _index
category: systems
status: pre-build
last_edited: 2026-04-29
editor: pointsav-engineering
---

## Systems

This category covers the operating systems at the foundation layer of the PointSav platform. Each article describes one OS: its capability model, its role in tenant isolation, and how it composes with the services and applications that run on top of it.

The primary operating system is [[ToteboxOS]] — a formally verified capability-based OS built on seL4. Its design provides the tenant-isolation and cryptographic-attestation properties that the rest of the platform depends on. A second OS, the workplace operating environment, handles the employee-facing application surface. The orchestration layer connects them. Articles in this category are technical in register; readers should be comfortable with OS-level concepts, capability-based security, and hardware-level trust models.

## Articles in this category

- [[os-totebox]] — [[ToteboxOS]]: the seL4-based capability OS at the platform's foundation layer; formal verification, capability model, and tenant isolation.
- [[totebox-orchestration]] — How [[ToteboxOS]] instances are orchestrated across a fleet deployment; scheduling, isolation boundaries, and upgrade paths.

<!-- ENGINE: this list is editorial in iteration-1; iteration-2+
generates it from category-directory file listing once PL.7
chunked-migration moves articles into category subdirectories. -->

## See also

- [Wiki home](/)
- [Architecture](/architecture/)
- [Infrastructure](/infrastructure/)

<!-- EDITORIAL NOTE: PL.7 chunked normalization sweep will migrate
     root-prefixed TOPICs into this category subdirectory. Until
     migration lands, the existing root TOPICs render at their current
     URLs (topic-<slug>.md); this landing references them by current slug. -->
