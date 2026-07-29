---
schema: foundry-doc-v1
title: "Security and Trust"
slug: security-index
category: security
type: topic
content_type: topic
quality: complete
short_description: "How the platform is protected and how its records are verified: identity and permissions, cryptographic verification, isolation boundaries, how data is handled and kept private, and the supply-chain controls designed to keep code honest."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-07-28
editor: pointsav-engineering
paired_with: _index.es.md
---

The **security** category collects how the platform is protected and how its records are verified. It covers identity and permissions, cryptographic verification, isolation boundaries, how data is handled and kept private, and the supply-chain controls designed to keep code honest from contributor to production.

This is the platform's answer to the diligence reader's question — *can this be trusted?* — and the front door for engineers looking up a specific security mechanism: capability-based access control, machine-based authentication, attestation, cryptographic ledgers, and the trust-establishment bootstrap a device passes through before it joins a deployment.

## Identity and permissions

Who is known to the system, how a device proves it, and what it's allowed to do.

- [[capability-based-security|Capability-based security]] — the access-control model: components hold verified cryptographic tokens instead of ambient privilege
- [[machine-based-auth|Machine-based authorization]] — pairing hardware to hardware replaces passwords; the pairing itself is the permission
- [[personnel-permissions|Personnel and permissions]] — how contributor identity and the four permission tiers are expressed through pairings, not database roles
- [[identity-ledger-schema-design|Identity ledger schema design]] — the Person/Anchor/Claim record types behind Ring 1 identity resolution
- [[verification-surveyor|Verification surveyor]] — the human-in-the-loop checkpoint that confirms an extracted identity before it's committed

## Cryptographic verification

How a reader independently checks that a record hasn't been altered.

- [[crypto-attestation|Cryptographic payload attestation]] — client-side SHA-256 hashing so any viewer can verify published content wasn't changed in transit
- [[cryptographic-ledgers|Cryptographic ledgers]] — the immutable-state storage pattern: hash-chained entries, signed checkpoints, monthly Sigstore Rekor anchoring

## Isolation boundaries

What contains a compromise once one occurs. Thin relative to the category's own scope — see the [[ppn-tenant-vm-isolation|tenant isolation]] and [[service-vm-tenant|VM tenant]] articles in [[infrastructure|Where It Runs]] for the commercially load-bearing case, which isn't yet cross-referenced from here.

- [[sel4-capability-topology|seL4 capability topology]] — why security in an seL4 system is the shape of the capability graph, not a policy layer
- [[diode-standard|Diode standard]] — the unidirectional authority-to-subject command flow that removes lateral movement by design
- [[genesis-protocol|Genesis protocol]] — the fleet-bootstrapping sequence a node runs at first boot to reach a secure, claimable state

## Data handling and privacy

- [[data-sovereignty-telemetry|Data sovereignty and zero-state telemetry]] — the platform's only article on this clause today; retention, deletion, and encryption-at-rest have no dedicated article yet

## Supply-chain controls

Keeping code honest from a contributor's machine to production.

- [[five-stage-supply-chain|Five-stage sovereign supply chain]] — the fork → PR → squash-merge → mirror → deploy path, and the double-blind air-gap between contributor and customer
- [[pre-commit-defense-in-depth|Pre-commit defense in depth]] — the helper-only gate, secret-pattern scan, and size guard that run on every commit

## See also

- [Architecture](/architecture/) — how the platform is put together
- [Governance and Standards](/governance/) — what was decided and why it is compliant
- [Where It Runs](/infrastructure/) — the deployed storage and ledger infrastructure these mechanisms protect
