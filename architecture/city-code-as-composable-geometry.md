---
schema: foundry-doc-v1
title: "City Code as Composable Geometry"
slug: city-code-as-composable-geometry
category: architecture
type: topic
quality: core
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-06
editor: pointsav-engineering
cites: [ifc-4-3, ids-1-0, bsdd-v1]
paired_with: city-code-as-composable-geometry.es.md
---

Every building code compliance tool in production follows the same architecture: a completed design model is submitted to a rules engine, which generates a violation report, which a human must review and remediate before resubmission. This post-design validation model has been the industry standard for twenty years. It produces a structural tension between design iteration speed and compliance verification. The more thorough the rules engine, the longer each review cycle. A different architecture is possible: if regulatory requirements are encoded directly into the elements available to a designer — not as rules applied to a finished model but as geometric and numeric constraints embedded in the element specification — then non-compliant configurations cannot be placed. This is the City Code as Composable Geometry model, and it is the architectural claim underlying the BIM Token platform (Doctrine claim #41, 2026).

## The Validation-First Paradigm

Post-design validation tools operate on a common pattern:

1. A designer authors a model in an IFC-capable authoring tool.
2. The model is exported to IFC format and submitted to a validation service.
3. The validation service applies a ruleset — encoded in proprietary rule languages, IDS 1.0 constraint files, or platform-specific scripting — and produces a report listing violations.
4. A human reviews the report, returns to the authoring tool, makes corrections, and resubmits.

This cycle repeats until the model passes. Most authoring tools enforce nothing at placement time: any element may be placed anywhere until the external validator objects.

The consequences are operational. Design teams budget iteration time for compliance review. On complex projects, regulatory review cycles add weeks to design phases. The validator is a gating function that sits outside the design environment and communicates asynchronously with it.

## Prior Art Survey

Research conducted in April 2026 identified four categories of prior art, all in the validation-first quadrant.

**IDS 1.0 (Information Delivery Specification).** buildingSMART's IDS standard encodes property constraints in XML. An IDS file declares what a valid model contains — it is a validation language, not a constraint on element palettes. IDS files are inputs to validators, not constraints applied during design.

**bSDD (buildingSMART Data Dictionary).** The bSDD provides semantic identity for element types across jurisdictions and tools. It does not encode regulatory constraints or climate zone performance requirements. A bSDD URI is an identity anchor, not a constraint specification.

**Post-design validation platforms.** Commercial BIM validation platforms operate post-design. Their rules engines can check geometry, topology, property values, and spatial relationships — but they operate as audit tools on submitted models. Non-compliant models pass through authoring environments without objection until submission.

**Singapore CORENET X.** The most advanced government BIM submission system in public production. CORENET X accepts IFC models submitted for building permit applications and runs automated code compliance checks against Singapore's regulatory requirements. It remains a validator: models are authored freely, submitted to CORENET X, and returned with violation reports. The 2024 implementation adds real-time guidance in some authoring tool plugins, narrowing but not closing the gap between validation-first and composition-first. It is jurisdiction-specific and not available as a neutral platform for other jurisdictions.

**Assessment.** All identified prior art occupies the validation-first quadrant. The compositional-first quadrant — encoding constraints into element specifications before authoring — has no established prior art in public production as of 2026.

## The Compositional Mechanism

City Code as Composable Geometry operates through a three-layer technical mechanism.

**Layer 1: Semantic identity via bSDD.** Every BIM Token carries a bSDD concept URI identifying its element type in a jurisdiction-neutral, tool-neutral reference. This URI is the stable identity that allows Regulation and Climate Zone overlays to reference the same element type regardless of IFC version drift.

**Layer 2: Regulatory constraint via IDS 1.0.** Each registered jurisdictional overlay for a BIM Token includes an IDS 1.0 constraint file. The IDS file encodes numeric and property constraints: maximum U-values, minimum structural ratings, fire resistance class requirements, accessibility clearances. When a BIM Token is placed in a model, its registered IDS constraints are part of its specification — the authoring environment receives these as element requirements at placement time, not as post-placement rules.

**Layer 3: Exclusion geometry via IFC fragment.** Where a regulatory requirement has geometric expression — a fire compartment boundary that an element must not cross, a setback from a property line, an accessibility envelope that must remain clear — the jurisdictional overlay includes an IFC fragment: a solid geometry encoded in IFC format that defines the excluded or required space. This fragment is associated with the token and resolves at placement time. It cannot be overridden by numeric constraints.

The composition of these three layers is what makes the geometry "encode" the code. The regulatory constraint is not stored in a separate validation database checked after authoring. It is stored in the token specification and instantiated with the element.

## Geometric Exclusion in Detail

The IFC fragment mechanism addresses the class of regulatory requirements that numeric constraints cannot express.

Consider a fire compartment wall in a multi-storey building. The requirement is not simply "this wall must have fire resistance class REI 90." It is also "this wall must form a continuous plane from floor slab to ceiling slab with no penetrations except those covered by appropriately rated closure devices." The second requirement is topological and geometric: the wall must occupy a specific spatial relationship to surrounding elements.

An IDS numeric constraint can express REI 90. It cannot express the topological continuity requirement. An IFC geometric exclusion fragment can: it encodes the spatial volume that the fire compartment boundary must occupy and the adjacent spatial volumes that must be filled by conforming construction. Authoring tools that consume the fragment can display the required geometry as a design guide and flag deviations in real time.

This is qualitatively different from post-design validation. The designer sees the required spatial configuration during authoring, not after submission.

## Structural Constraints on Centralised Approaches

Research identified three structural reasons why centralised cloud approaches cannot replicate the City Code as Composable Geometry model for all deployment contexts.

**Regulatory data sovereignty.** Jurisdictional regulatory data is public law. Encoding it as a service hosted on a commercial cloud platform creates procurement and sovereignty concerns for non-US jurisdictions under EU data residency requirements, GDPR restrictions, and equivalent national frameworks. A neutral platform that cities and national governments can self-host or have hosted under national cloud frameworks is structurally required for broad adoption.

**Offline-first requirement.** Construction sites frequently operate without reliable network connectivity. ITAR-restricted projects, remote sites, and many public infrastructure projects require the constraint data to be available offline. A cloud-dependent validation service cannot serve these use cases. A BIM Token vault cloned via git and stored locally is available offline unconditionally.

**Commercial platform neutrality.** Cities and national governments issuing regulatory requirements need to publish them to all conformant BIM platforms, not to specific commercial vendors. Publishing code requirements to a neutral, open-format JSON standard (W3C DTCG with BIM extensions) and distributing them via public git repositories is analogous to publishing building codes as PDF — neutral, reproducible, and vendor-independent.

## Implementation Stages

The City Code as Composable Geometry model is implemented progressively.

**Stage 1 (current, planned for v0.0.3):** BIM Token vault with Specification layer complete. Regulation layer skeleton present with first overlay set: British Columbia residential (RS-1 zoning) — selected because Woodfine Management Corp. operates in BC and is the reference customer. Climate Zone layer populated with BC temperate-coastal zone (ASHRAE 5C equivalent) performance parameters.

**Stage 2 (intended, v0.1.x):** IDS 1.0 constraint file generation. For each registered Regulation overlay, a conformant IDS 1.0 file is generated from the token data and published alongside the DTCG JSON. This enables existing IDS-aware validators to consume PointSav-authored constraint specifications.

**Stage 3 (intended, future):** Authoring tool integration. A plugin or API surface that delivers BIM Token constraints to IFC-capable authoring tools at placement time, not at submission time. The authoring tool receives the element palette constrained to conformant tokens for the project's jurisdiction and climate zone.

## See Also

- [[bim-token-what-it-is]]
- [[bim-token-three-layers]]
- [[flat-file-bim-leapfrog]]
- [[open-bim-regulatory-acceptance]]
- [[leapfrog-2030-architecture]]

## References

- IFC 4.3 (ISO 16739-1:2024) — buildingSMART International
- IDS 1.0 (Information Delivery Specification) — buildingSMART International
- buildingSMART Data Dictionary (bSDD) — buildingSMART International
- Singapore CORENET X — Building and Construction Authority, Singapore
- DOCTRINE.md claim #41 — City Code as Composable Geometry

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
