---
schema: foundry-doc-v1
title: "City code as composable geometry"
slug: city-code-as-composable-geometry
language: en
category: patterns
index_group: sovereignty-and-infrastructure-patterns
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-09-04
editor: pointsav-engineering
short_description: "A composition-first pattern that encodes regulatory requirements into element specifications as geometric and numeric constraints rather than applying them post-design, so a non-compliant configuration cannot be placed in the first place."
cites: [ifc-4-3, ids-1-0, bsdd-v1]
paired_with: city-code-as-composable-geometry.es.md
---

Every building-code compliance tool in production follows one architecture: a completed model is submitted to a rules engine, which emits a violation report, which a human reviews and remediates before resubmission. This post-design validation model has been the industry standard for twenty years, and it produces a structural tension — the more thorough the rules engine, the longer each review cycle.

A different architecture is possible. If regulatory requirements are encoded into the elements available to a designer — not as rules applied to a finished model, but as geometric and numeric constraints embedded in the element specification — then non-compliant configurations cannot be placed. This is the City Code as Composable Geometry pattern, and it is the architectural claim underlying the BIM Object library.

**Why it matters:** the cost of a code violation drops from weeks of rework to zero, because the violation never enters the model.

## The validation-first paradigm

Post-design validation tools share a common shape:

1. A designer authors a model in an IFC-capable authoring tool.
2. The model is exported to IFC and submitted to a validation service.
3. The service applies a ruleset — proprietary rule languages, IDS 1.0 constraint files, or platform scripting — and produces a report listing violations.
4. A human reviews the report, returns to the authoring tool, corrects, and resubmits.

The cycle repeats until the model passes. Most authoring tools enforce nothing at placement time: any element may go anywhere until an external validator objects.

The consequences are operational. Design teams budget iteration time for compliance review, and on complex projects regulatory review adds weeks to design phases. The validator is a gating function sitting outside the design environment, communicating with it asynchronously.

**Why it matters:** the delay is not a tooling defect anyone has failed to fix — it is inherent to checking after the fact rather than constraining beforehand.

## Prior art survey

Research conducted in April 2026 identified four categories of prior art, all in the validation-first quadrant.

**IDS 1.0 (Information Delivery Specification).** buildingSMART's IDS standard encodes property constraints in XML. An IDS file declares what a valid model contains — it is a validation language, not a constraint on element palettes. IDS files are inputs to validators, not constraints applied during authoring.

**bSDD (buildingSMART Data Dictionary).** bSDD provides semantic identity for element types across jurisdictions and tools. It does not encode regulatory constraints or climate-zone performance requirements. A bSDD URI is an identity anchor, not a constraint specification.

**Post-design validation platforms.** Commercial BIM validation platforms operate post-design. Their rules engines check geometry, topology, property values, and spatial relationships — as audit tools on submitted models. Non-compliant models pass through authoring environments without objection until submission.

**Singapore CORENET X.** The most advanced government BIM submission system in public production. It accepts IFC models for building-permit applications and runs automated code-compliance checks against Singapore's requirements. It remains a validator: models are authored freely, submitted, and returned with violation reports. The 2024 implementation adds real-time guidance in some authoring-tool plugins, narrowing but not closing the gap. It is jurisdiction-specific and not available as a neutral platform elsewhere.

**Assessment.** All identified prior art occupies the validation-first quadrant. The composition-first quadrant — encoding constraints into element specifications before authoring — has no established prior art in public production as of 2026.

## The compositional mechanism

The pattern operates through three layers.

**Layer 1 — semantic identity via bSDD.** Every BIM Object carries a bSDD concept URI identifying its element type in a jurisdiction-neutral, tool-neutral reference. This URI is the stable identity that lets Regulation and Climate Zone overlays reference the same element type regardless of IFC version drift.

**Layer 2 — regulatory constraint via IDS 1.0.** Each registered jurisdictional overlay includes an IDS 1.0 constraint file encoding numeric and property constraints: maximum U-values, minimum structural ratings, fire-resistance class requirements, accessibility clearances. When an object is placed, its registered IDS constraints are part of its specification — the authoring environment receives them as element requirements at placement time, not as post-placement rules.

**Layer 3 — exclusion geometry via IFC fragment.** Where a requirement has geometric expression — a fire-compartment boundary an element must not cross, a setback from a property line, an accessibility envelope that must stay clear — the overlay includes an IFC fragment: solid geometry in IFC format defining the excluded or required space. The fragment is associated with the object and resolves at placement time. It cannot be overridden by numeric constraints.

The composition of these three layers is what makes the geometry "encode" the code. The constraint is not held in a separate validation database consulted afterwards; it is held in the object specification and instantiated with the element.

**Why it matters:** because the constraint travels with the element, a jurisdiction's rules can change without anyone re-auditing existing models — the next placement simply picks up the current overlay.

## Geometric exclusion in detail

The IFC fragment mechanism addresses the class of requirements numeric constraints cannot express.

Consider a fire-compartment wall in a multi-storey building. The requirement is not simply "this wall must have fire-resistance class REI 90." It is also "this wall must form a continuous plane from floor slab to ceiling slab with no penetrations except those covered by appropriately rated closure devices." The second requirement is topological and geometric: the wall must occupy a specific spatial relationship to surrounding elements.

An IDS numeric constraint can express REI 90; it cannot express topological continuity. An IFC geometric exclusion fragment can — it encodes the spatial volume the boundary must occupy and the adjacent volumes that must be filled by conforming construction. Authoring tools consuming the fragment can display the required geometry as a design guide and flag deviations in real time.

**Why it matters:** the designer sees the required spatial configuration while designing, not after submitting. That is the qualitative difference between this pattern and validation.

## Structural constraints on centralised approaches

Three structural reasons prevent a centralised cloud service from replicating this pattern for all deployment contexts.

**Regulatory data sovereignty.** Jurisdictional regulatory data is public law. Encoding it as a service hosted on a commercial cloud creates procurement and sovereignty concerns for non-US jurisdictions under EU data-residency requirements, GDPR restrictions, and equivalent national frameworks. A neutral platform that cities and national governments can self-host, or have hosted under national cloud frameworks, is structurally required for broad adoption.

**Offline-first requirement.** Construction sites frequently operate without reliable connectivity. ITAR-restricted projects, remote sites, and many public infrastructure projects need constraint data available offline. A cloud-dependent validation service cannot serve these; an object vault cloned and stored locally is available offline unconditionally.

**Commercial platform neutrality.** Governments issuing regulatory requirements need to publish them to all conformant BIM platforms, not to specific vendors. Publishing code requirements to a neutral, open-format JSON standard (W3C DTCG with BIM extensions) and distributing them via public repositories is analogous to publishing building codes as PDF — neutral, reproducible, and vendor-independent.

## Implementation stages

The pattern is implemented progressively.

**Stage 1 (current, planned for v0.0.3).** Object vault with the Specification layer complete. Regulation layer skeleton present with a first overlay set: a representative jurisdiction's residential zoning code (RS-1-style zoning), illustrative rather than exhaustive. Climate Zone layer populated with that same jurisdiction's temperate-coastal (ASHRAE 5C equivalent) performance parameters.

**Stage 2 (intended, v0.1.x).** IDS 1.0 constraint-file generation. For each registered Regulation overlay, a conformant IDS 1.0 file is generated from the object data and published alongside the DTCG JSON, so existing IDS-aware validators can consume PointSav-authored constraint specifications.

**Stage 3 (intended, future).** Authoring-tool integration — a plugin or API surface delivering object constraints to IFC-capable authoring tools at placement time rather than at submission time, with the element palette constrained to conformant objects for the project's jurisdiction and climate zone.

## See also

- [[flat-file-bim-leapfrog]] — the offline-first, open-standards posture this depends on
- [[leapfrog-2030-architecture]] — the wider architectural programme
