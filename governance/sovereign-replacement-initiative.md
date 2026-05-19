---
schema: foundry-doc-v1
title: "Sovereign replacement initiative"
slug: sovereign-replacement-initiative
category: governance
type: topic
quality: complete
short_description: "The Sovereign Replacement Initiative is the engineering governance program that tracks third-party dependencies, isolates them in quarantined component directories, and coordinates the active moonshot programs that build native replacements."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-19
editor: pointsav-engineering
cites: []
paired_with: sovereign-replacement-initiative.es.md
---


> The Sovereign Replacement Initiative is the formal program that records every foreign dependency in a structured ledger, enforces quarantine isolation until a native replacement is ready, and retires the dependency once the replacement reaches structural parity.

Any platform that has passed through a digital-transformation
phase inherits third-party architectural components it did not
design. Reliance on those components — proprietary cloud
authentication providers, foreign GPU drivers, commercial graph
APIs — creates a structural risk: if a third-party vendor changes
its terms of service or deprecates an API, the dependent platform
either adapts under pressure or halts. The **Sovereign Replacement
Initiative** is the platform's response to this class of risk. It is
a physical ledger of outstanding third-party dependencies and an
active engineering pipeline designed to eliminate them
systematically.

## Technical debt ledger

The initiative maintains a ledger that records each identified
third-party dependency alongside its isolation status and the
corresponding moonshot initiative, if one has been opened. The
ledger is a live document: entries are added when new dependencies
are identified and closed when a native replacement achieves
structural parity. Auditors and contributors can read the ledger
to see the platform's current external exposure.

## Quarantine protocol

Until a native replacement is available, a legacy component is
physically isolated into a quarantined component silo (for example,
`vendor-azure-auth` or `vendor-microsoft-graph`). These directories
are structural containers that restrict the foreign code to a
controlled capability boundary. The isolation prevents coupling from
spreading into adjacent platform layers while the replacement is
under development.

## Moonshot pipeline

For every quarantined dependency, the engineering team opens a
corresponding moonshot directory (for example, `moonshot-database`
or `moonshot-kernel`). These are active development efforts
targeting native, formally verifiable implementations. Once a
moonshot component achieves structural parity with its quarantined
counterpart, it replaces the isolated directory and the ledger
entry closes.

## Completion criteria

A ledger entry closes when the associated moonshot initiative achieves **structural parity** with the quarantined component it replaces. Structural parity has three conditions:

1. **Functional coverage.** The native implementation covers all platform use-cases currently served by the quarantined component.
2. **Physical supersession.** The quarantined `vendor-*` directory is deleted from the repository. No source references to the replaced component remain.
3. **Formal verification target.** For kernel-layer components, the native implementation satisfies the platform's formal verification requirement (seL4-compatible, memory-safe, no buffer overflow). For application-layer components, the platform's standard test coverage and audit-ledger integration requirements are met.

Until all three conditions are satisfied, the quarantine remains active and the ledger entry stays open.

## Relationship to ADR-08

[[architecture-decisions|Architecture Decision 8]] formally records the systemd init system as a quarantined dependency — the dependency the platform accepts while the `moonshot-kernel` initiative builds toward the seL4 microkernel replacement. The Sovereign Replacement Initiative is the governance mechanism that gives ADR-08 operational force: without the ledger, the quarantine is a statement of intent; with the ledger, it is a tracked commitment with a named completion path.

## Vendor and customer roles

The initiative operates across the vendor-customer structure:

- **Vendor (PointSav Digital Systems).** Maintains the ledger, engineers the native replacements, and owns the moonshot directories.
- **Customer (Woodfine Management Corp.).** Audits the pipeline to verify progress toward operational independence from legacy external providers.

## See also

- [[moonshot-initiatives|Moonshot Initiatives]]
- [[ontological-governance|Ontological Governance]]
- [[verification-surveyor|Verification Surveyor]]
- [[customer-hostability|Customer Hostability]]
