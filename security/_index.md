---
schema: foundry-doc-v1
title: "Security and Trust"
slug: security-index
category: security
type: topic
content_type: topic
index_type: thematic
index_scope: security
quality: complete
short_description: "How the platform is protected and how its records are verified: identity and permissions, cryptographic verification, isolation boundaries, how data is handled and kept private, and the supply-chain controls designed to keep code honest."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-04
editor: pointsav-engineering
paired_with: _index.es.md
---

**Security and trust** on this platform rests on one idea: every component holds a verified,
scoped credential it must present to act — not an inherited grant of trust. That discipline
shows up across five areas: who's known to the system and what they're allowed to do, how a
reader independently verifies a record hasn't been altered, what contains a compromise once
one occurs, how data is handled and kept private, and the controls that keep code honest from
a contributor's machine to production.

A diligence reader's real question is *can this be trusted?* An engineer's is usually
narrower — *how does capability-based access control actually work?* Both start below.

<!-- START-HERE-HIGHLIGHT: engine reads this block to render the single "start here" card
     (reuses the existing cluster-card--start-here component). Do not add more than one. -->
**Start here:** [[capability-based-security|Capability-based security]] — the access-control
model the whole category is named for: components hold verified cryptographic tokens instead of
ambient privilege. One software layer implements it today; kernel-level enforcement is planned.
<!-- END-START-HERE-HIGHLIGHT -->

## Identity and permissions {#group-count-5}

Who is known to the system, how a device proves it, and what it's allowed to do.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: identity-and-permissions -->
- [[capability-based-security|Capability-based security]] — the access-control model: components hold verified cryptographic tokens instead of ambient privilege
- [[machine-based-auth|Machine-based authorization]] — pairing hardware to hardware replaces passwords; the pairing itself is the permission
- [[personnel-permissions|Personnel and permissions]] — how contributor identity and the four permission tiers are expressed through pairings, not database roles
- [[identity-ledger-schema-design|Identity ledger schema design]] — the Person/Anchor/Claim record types behind Ring 1 identity resolution
- [[verification-surveyor|Verification surveyor]] — the human-in-the-loop checkpoint that confirms an extracted identity before it's committed
<!-- END AUTO-GENERATED -->

## Cryptographic verification {#group-count-2}

How a reader independently checks that a record hasn't been altered.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: cryptographic-verification -->
- [[crypto-attestation|Cryptographic payload attestation]] — client-side SHA-256 hashing that would let any viewer verify published content wasn't changed in transit; today it's an unwired, cosmetic pattern in a few templates, not a capability any shipped surface actually offers
- [[cryptographic-ledgers|Cryptographic ledgers]] — the immutable-state storage pattern: hash-chained entries, signed checkpoints, monthly Sigstore Rekor anchoring
<!-- END AUTO-GENERATED -->

## Isolation boundaries {#group-count-3}

What contains a compromise once one occurs. Thin relative to the category's own scope — see the
[[ppn-tenant-vm-isolation|tenant isolation]] and [[service-vm-tenant|VM tenant]] articles in
[[infrastructure|Where It Runs]] for the commercially load-bearing case, which isn't yet
cross-referenced from here.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: isolation-boundaries -->
- [[sel4-capability-topology|seL4 capability topology]] — why security in an seL4 system is the shape of the capability graph, not a policy layer
- [[diode-standard|Diode standard]] — the unidirectional authority-to-subject command flow that removes lateral movement by design
- [[genesis-protocol|Genesis protocol]] — the fleet-bootstrapping sequence a node runs at first boot to reach a secure, claimable state
<!-- END AUTO-GENERATED -->

## Data handling and privacy {#group-count-1}

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: data-handling-and-privacy -->
- [[data-sovereignty-telemetry|Data sovereignty and zero-state telemetry]] — the platform's only article on this clause today; retention, deletion, and encryption-at-rest have no dedicated article yet
<!-- END AUTO-GENERATED -->

## Supply-chain controls {#group-count-2}

Keeping code honest from a contributor's machine to production.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: supply-chain-controls -->
- [[five-stage-supply-chain|Five-stage supply chain]] — the contributor-to-customer promotion path, gated by a heavily guarded promotion script rather than a pull request, and the double-blind air-gap between contributor and customer
- [[pre-commit-defense-in-depth|Pre-commit defense in depth]] — the helper-only gate, secret-pattern scan, and size guard that run on every commit
<!-- END AUTO-GENERATED -->

Several articles linked here describe planned, not-yet-built mechanisms and are hedged in
their own text. This page is an orientation, not a compliance attestation.

## See also

- [Architecture](/architecture/) — how the platform is put together
- [Governance and Standards](/governance/) — what was decided and why it is compliant
- [Where It Runs](/infrastructure/) — the deployed storage and ledger infrastructure these mechanisms protect
