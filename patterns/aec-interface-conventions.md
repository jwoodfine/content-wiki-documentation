---
schema: foundry-doc-v1
title: "AEC interface conventions"
slug: aec-interface-conventions
language: en
category: patterns
index_group: interface-and-user-experience
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-26
editor: pointsav-engineering
short_description: "BIM authoring tools across the industry share a common interface vocabulary — a spatial hierarchy, an element properties panel, a 3D viewport, and saved views — because they build on the same underlying IFC data model. The Building Design System's planned interface layer reuses this vocabulary rather than inventing a new one, and is intended to extend it into facility-management workflows."
cites: [ifc-4-3]
paired_with: aec-interface-conventions.es.md
---

Every major BIM authoring platform ships with the same four interface conventions: a hierarchy tree for the spatial structure, a properties panel for element attributes, a 3D viewport, and a saved-view navigator. These conventions exist because the underlying data model — the IFC entity hierarchy — is the same regardless of which tool authors it. An architect or engineer who has learned this vocabulary in one authoring tool already knows it in the next.

**Why it matters:** a practitioner never has to relearn how to navigate a model just because the software changed — the vocabulary is a property of the standard, not of any one vendor's interface.

## Why a shared vocabulary matters

BIM project teams routinely work across several authoring tools on a single project. The structural engineer's model, the architect's model, and the MEP engineer's model each export to the same open format, and coordination happens in a common viewer where no one is working in their native authoring environment. A coordination surface built on this shared vocabulary does not introduce a new learning curve on top of the tools practitioners already use.

## The Building Design System's planned interface layer

[[building-design-system|The Building Design System]] is planned to build its own interface components on this same shared vocabulary, so a practitioner moving between their authoring tool and any BIM surface built on the platform finds the same tree, the same properties panel, and the same viewport controls. This layer does not exist in canonical code yet.

**Why it matters — zero learning curve by design, not by accident:** adopting interface patterns already familiar from industry-standard AEC authoring tools means a practitioner arrives with a zero learning curve rather than needing to learn a new tool's conventions before doing any real work. Mirroring the existing vocabulary is intended to let attention go to the platform's actual differentiators — the flat-file archive described in [[asset-anchored-bim-vault]] — rather than to basic tool navigation.

## Extending into facility management

Existing BIM tools are built primarily for designers, and most of a model's value is lost once it reaches a facility manager who was never part of its authoring workflow. This interface layer is intended to extend the same familiar vocabulary into the facility-management workflow: linking maintenance status to building elements, connecting spaces to lease records, and layering live sensor data onto the model. The intent is to turn a BIM model from a design-and-handoff artifact into an operating record a facility manager actually uses day to day, rather than a second, disconnected system that has to be reconciled against it by hand.

## Where the specification lives

The full component catalog and implementation detail behind this interface layer are maintained directly at [bim.woodfinegroup.com](https://bim.woodfinegroup.com).

## See also

- [[building-design-system]] — the broader Building Design System this interface layer is part of
- [[bim-object-specification]] — the underlying object model this interface exposes
- [[asset-anchored-bim-vault]] — the archive structure the facility-management extension reads from
