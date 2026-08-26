---
schema: foundry-doc-v1
title: "Building Design System"
slug: building-design-system
language: en
category: architecture
index_group: location-intelligence-and-domain
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-26
editor: pointsav-engineering
short_description: "A planned coordination layer for the built environment: a canonical, machine-readable library of building-element specifications that independent BIM authoring surfaces consume by reference, the way a software design system keeps independent product teams consistent."
cites: [ifc-4-3, uniclass-2015, bsdd-v1]
paired_with: building-design-system.es.md
---

Major software design systems solve a coordination problem at scale: when independent teams build interfaces in parallel, consistency breaks down unless design decisions are encoded in a shared layer that every surface consumes by reference. No equivalent has existed for the built environment. Building Information Modelling production is coordinated through shared standards (IFC, Uniclass, bSDD) and shared authoring tools, but there has been no common specification layer — no canonical, machine-readable library of building-element specifications that independent authoring surfaces consume by reference. The Building Design System is intended to fill that gap.

**Why it matters:** without this layer, every BIM authoring surface re-derives the same code and performance requirements independently, and two surfaces working on the same building can drift out of agreement without either one being wrong on its own terms.

## Why the space has been empty

Three structural factors have kept it empty. Proprietary BIM authoring tools have historically stored element specifications in formats locked to a single tool, not designed to carry normative regulatory data across tools. IFC is a neutral exchange format — it expresses what a model contains, not what a specification requires — so it was never designed to be a design system on its own. And the wider built-environment standards stack evolved in parallel across jurisdictions, with no single standard providing a composable specification layer that ties the others together.

**Why it matters:** each factor is a reason no single vendor filled this gap already, not a reason it can't be filled — the standards it would compose on top of are already open and already mature (see [[flat-file-bim-leapfrog]]).

## What it is made of

The Building Design System is organized into two layers: a library of [[bim-object-specification|BIM Object primitive categories]] — the specification units for spatial elements, physical elements, materials, systems, and more — and a set of [[aec-interface-conventions|shared interface components]] that any BIM-capable surface can build on. Together they are intended to give independent authoring surfaces a common vocabulary to coordinate around, without a practitioner moving between them needing to learn a new interface each time.

## An owned archive, not a hosted service

The Building Design System is not planned as a hosted service — it is a set of files in a git repository that an organization clones and extends with its own jurisdiction-specific and site-specific data. This is the same sovereignty model that underlies [[asset-anchored-bim-vault|the flat-file BIM archive]] more broadly. Nothing is required to flow back to a central vendor for an organization to keep using its own copy.

**Why it matters:** the coordination layer is a design-time convenience, not a runtime dependency — a customer that stops paying for support keeps every file that makes their BIM archive work.

## Where the specification lives

The full object category catalog, interface component library, and current implementation status are maintained directly at [bim.woodfinegroup.com](https://bim.woodfinegroup.com), the reference deployment this article describes the architecture of.

## See also

- [[bim-object-specification]] — the BIM Object primitive categories and three-layer composition structure
- [[aec-interface-conventions]] — the shared interface vocabulary the design system builds its own components on
- [[asset-anchored-bim-vault]] — the archive structure this design system is intended to organize
- [[flat-file-bim-leapfrog]] — the architectural constraints the whole BIM substrate is built on
