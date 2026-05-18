---
schema: foundry-doc-v1
title: "The property manager BIM gap"
slug: property-manager-bim-gap
short_description: "Fewer than 40 percent of facilities managers actively use the BIM models delivered at project handover, due to software cost, training requirements, and file format opacity. The Building Design System's FM-specific interface components provide read-only access to full-fidelity BIM data through searchable GUID lookups without requiring proprietary authoring tool licences."
category: architecture
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-17
editor: pointsav-engineering
cites: [ifc-4-3, iso-19650]
paired_with: property-manager-bim-gap.es.md
---

Building Information Models are authored by architects and structural engineers, delivered to contractors for construction, and then handed to property managers at practical completion. At that handover, the model's usefulness to the people who operate the building for the next 30 years depends entirely on whether the property manager has access to a BIM viewer, knows how to use it, and can afford to maintain the authoring-tool licence that produced the file.

In practice, most do not.

## What the Research Documents

The gap between BIM production and BIM consumption in facilities management is documented in peer-reviewed literature. A consistent finding across studies published between 2015 and 2024 is that fewer than 40 percent of facilities managers actively use the BIM models they receive at handover. The barriers cited most often are:

1. **Software cost.** Full-feature authoring licences are priced for design professionals. A facilities manager who only needs to look up a Pset value or file a BCF issue cannot justify the cost.

2. **Training requirement.** BIM authoring tools carry a significant learning curve. The interface is designed for model creation, not model consumption. A facilities manager who needs to locate a door's fire rating does not want to learn a coordinate system, a view matrix, and a family library to retrieve a single attribute.

3. **File format opacity.** IFC-SPF is plain text, but a 50 MB IFC file for a mid-size building is not navigable with a text editor. Without a viewer, the file is effectively inaccessible.

The result is what several researchers call the "BIM handover gap": a detailed digital model of the building exists, was paid for by the developer, and meets the contractual delivery requirement — and sits unused on a shared drive.

## How FM Platform Vendors Have Addressed It

Facilities management platforms — CAFM and CMMS software categories — have recognised this gap and begun building BIM viewer integrations. One documented example is a CAFM platform whose BIM integration imports model data at handover, links elements to maintenance schedules and work orders, and lets FM operators interact with the data through the CAFM interface rather than a BIM viewer.

This approach solves the viewer-cost and training-cost problems by translating BIM data into a form the CAFM platform already knows how to display. The trade-off is fidelity: the CAFM import is lossy. Pset values that the CAFM schema does not recognise are discarded. The geometric model is reduced to a floor-plan bitmap or a simple room list. The bidirectional link between FM work orders and the canonical IFC model is not maintained.

When the building is renovated — walls moved, systems upgraded — the CAFM database and the IFC model diverge and must be re-synchronised manually. In practice, this synchronisation rarely happens. The FM database reflects the building as it was delivered, not as it stands.

## The Gap This Platform Is Intended to Fill

The Building Design System's FM-specific interface components — `GuidSearch` and `AuditLog` — are designed for the facilities manager who needs read-only access to BIM model data without the cost or complexity of an authoring-tool licence.

`GuidSearch` is a search interface that takes an IFC GUID — the alphanumeric identifier stamped on every door, every wall, every HVAC component in a BIM model — and returns the element's Pset values, maintenance history, and open BCF issues. A facilities manager scanning a QR code attached to a piece of equipment, or reading a GUID from a work-order form, retrieves the building model data for that specific element without navigating a 3D viewport.

`AuditLog` is a time-ordered log of all changes to the vault: IFC model updates, BCF topic resolutions, work-order completions, and sensor-reading anomalies. For a facilities manager whose regulatory obligation is to demonstrate that a fire door was inspected, tested, and found compliant, the AuditLog is the audit trail.

Both components are intended to run on the [[asset-anchored-bim-vault]] — the same flat-file archive that the design and construction team used. There is no CAFM import, no schema translation, and no synchronisation gap. The FM operator reads the canonical model directly, at full Pset fidelity, through an interface designed for their workflow rather than for model creation.

## The Lease Register Convergence

The facilities management gap has a financial dimension that is less documented in the academic literature but is immediate for a property manager who is also a landlord. Lease register data — tenant names, lease terms, rent amounts, demising-wall coordinates — lives in a separate spreadsheet or lease management system, disconnected from the spatial model of the floor plate.

When a tenant changes use, or a demising wall is moved for a new tenant, the lease register, the FM work-order system, and the BIM model are three separate records of the same physical change. Each must be updated independently; none automatically propagates the change to the others.

The Woodfine vault's per-element YAML sidecars carry lease references alongside sensor readings and work-order history. A wall element's sidecar includes the tenant identifier and lease term for the space it bounds. When the lease changes, the sidecar is updated in the same git commit that records the model change. The three records become one.

This convergence is intended to be the most strategically consequential capability of the platform for a property manager who is also an asset owner: the building's spatial, operational, and financial identity in one portable archive that moves with the property deed.
