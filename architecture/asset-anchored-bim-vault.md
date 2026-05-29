---
schema: foundry-doc-v1
title: "The asset-anchored BIM vault"
slug: asset-anchored-bim-vault
short_description: "A building's authoritative digital record structured as plain-text and standardized-binary files in a git-versioned directory, qualifying as an ISO 19650-conforming Common Data Environment that travels with the property deed."
category: architecture
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-17
editor: pointsav-engineering
cites: [ifc-4-3, iso-19650, ids-1-0]
paired_with: asset-anchored-bim-vault.es.md
---

A building's authoritative digital record is a directory of plain-text and standardised-binary files that live on the owner's storage, travel with the property deed when ownership changes hands, and remain readable without a proprietary software licence for as long as the underlying open standards are maintained. This article describes the vault layout, the versioning layer that gives the archive git-grade traceability, and the [[open-bim-regulatory-acceptance|ISO 19650]] qualification that makes a [[flat-file-bim-leapfrog|flat-file git repository]] a conforming Common Data Environment.

## The Vault Layout

The canonical vault for a Woodfine property archive is structured as follows:

```
vault/
├── ifc/             # Authoritative IFC-SPF files (ISO 16739-1:2024)
├── elements/        # Per-element YAML sidecars (Pset_* + sensor + work-order)
├── bcf/             # BCF 3.0 per-topic directories (XML + PNG; unzipped)
├── ids/             # IDS 1.0 validation contracts (per-jurisdiction overlay)
├── materials/       # Material database (flat files; service-materials input)
├── codes/           # Building codes as composable geometry overlays
│                    #   (bsdd-*.json + *.ids + *.ifc fragments per jurisdiction)
├── geometry/        # glTF 2.0 + CityJSONSeq (regenerable caches; not canonical)
├── drawings/        # SVG 2D drawings (regenerable; IFC GUIDs in SVG element IDs)
├── objects/<hash>.json  # Hash-addressed object store
└── refs/            # Git-style ref pointers (branches, tags, HEADs)
```

The `.ifc` files are the sole authoritative spatial and semantic state of the building. Every other directory either validates the IFC state, enriches it with non-geometric data, or caches a derivative representation that can be regenerated from the canonical source.

## The IFC-SPF File as Canonical Archive

IFC-SPF is the STEP Physical File encoding of IFC, specified in ISO 10303-21. It is a line-oriented clear-text format: a person with a text editor can read an IFC-SPF file. A Unix diff of two IFC-SPF files shows exactly which entities changed between model versions.

The format has been in production since IFC 1.0 in 1996. IFC 4.3, published as ISO 16739-1:2024, is the current revision. The standard's governance model — maintained by buildingSMART International, ratified by ISO — provides the longest credible shelf life of any building data format in use today.

## Per-Element YAML Sidecars

Each IFC element that carries non-geometric operational data has a corresponding YAML sidecar in `vault/elements/`. The sidecar filename is the IFC GUID of the element, which is stable across model revisions.

The sidecar can carry:

- **Pset overrides** — non-geometric property values not captured in the IFC authoring session
- **Sensor readings** — timestamped records from an MQTT broker (temperature, CO₂, occupancy) written as append-only log entries
- **Work orders** — references to maintenance tasks, inspection records, and repair history by work-order ID
- **Lease references** — tenant identifier and lease term, linking the spatial element to the lease register

Because the sidecar is a plain YAML file in the same git repository as the IFC file, every change to sensor data or work-order history is a git commit. The building's operational history is version-controlled alongside its geometry.

## The Hash-Addressed Object Store

The `vault/objects/` directory implements a hash-addressed object store. Each object is a JSON file whose filename is the SHA-256 hash of its content. `vault/refs/` holds named pointers — branches, tags, and HEAD — that resolve to specific object hashes.

This architecture gives the vault git-like content-addressable semantics independently of the git repository that wraps it. The result is a [[merkle-proofs-as-substrate-primitive|Merkle DAG]]: the root hash of a model state is cryptographically bound to every element it contains.

The Merkle structure provides two structural benefits:

1. **Audit trail integrity.** A claimed historical state of the model can be verified against the root hash without trusting the server that stored it.
2. **Efficient delta transfer.** When two parties synchronise vaults, only the objects whose hashes differ need to transfer.

## ISO 19650 Qualification

[[open-bim-regulatory-acceptance|ISO 19650]] defines a Common Data Environment (CDE) as a system for collecting, managing, and disseminating information in structured containers. The standard is technology-neutral.

A git repository hosting a vault directory qualifies as a CDE under ISO 19650 with the following mapping:

| ISO 19650 concept | Git + vault implementation |
|---|---|
| Information container | IFC file or YAML sidecar |
| Container UID | Git object hash or IFC GUID |
| Status | Branch name (`work-in-progress`, `shared`, `published`) |
| Revision | Git commit hash |
| Classification | Directory path + YAML header |
| Change history | `git log --follow <filename>` |
| CDE workflow states | Git branch merge / pull-request workflow |

A local git repository on an air-gapped workstation satisfies ISO 19650 as fully as a hosted platform. This makes the vault architecture appropriate for ITAR defence projects, EU Data Act jurisdictions, and HIPAA-governed healthcare facilities.

## Vendor-Obsolescence Survivability

Buildings are typically designed to stand for 50 to 100 years. The software tools used to author BIM models typically change format with every major release and become unreadable by competing tools within a decade.

The vault architecture addresses this asymmetry in two ways. First, the canonical formats — IFC-SPF, BCF 3.0, IDS 1.0, YAML — are ISO-governed open standards or widely adopted plain-text formats. Any competent engineer can write a reader for IFC-SPF from the ISO specification without access to proprietary SDKs. Second, the regenerable derivatives — glTF visualisation caches, SVG 2D drawings — are explicitly marked as non-canonical. If the tool that generated them disappears, the canonical IFC file remains and any IFC-to-glTF or IFC-to-SVG converter can regenerate them. The architecture is consistent with the [[flat-file-bim-leapfrog|flat-file BIM leapfrog]] design.

## The Archive Travels with the Land

A physical property asset transfers with a title deed. The Woodfine vault is intended to be bundled with that transfer: the same git repository that holds the IFC archive, the lease register references, and the operational history accompanies the property when ownership changes hands.

No cloud platform can make this guarantee. A multi-tenant SaaS platform holds the digital twin on behalf of the current tenant; when that tenant's subscription lapses or the vendor discontinues the product, the data requires explicit export — and export formats are invariably lossy relative to the native platform representation.

A flat-file vault is the owner's property in the same sense that the physical building is the owner's property: unconditionally, transferrably, and without ongoing vendor permission.
