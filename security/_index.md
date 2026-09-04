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
last_edited: 2026-09-04
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
- [[capability-based-security|Capability-based security]] — Capability-based security grants each component an unforgeable, scoped token it must present to act, replacing ambient privilege. One software layer implements it today; kernel-level enforcement is planned.
- [[machine-based-auth|Machine-based authorization]] — Access is granted to a device's key rather than to a person's password. A short-code pairing ceremony binds an SSH key fingerprint to a user record after operator approval, with no password stored anywhere.
- [[personnel-permissions|Personnel and permissions]] — Four permission tiers, P1 through P4, are implemented as a typed enumeration and served over an HTTP endpoint that reads a workspace configuration file. That file currently declares no contributors, so the endpoint resolves nothing for any real user.
- [[identity-ledger-schema-design|Identity ledger schema design]] — Three record types — Person, Anchor, Claim — separate who is known from how they were observed and what was asserted. Identity is a UUIDv5 of a lowercased email, so the same input always yields the same identifier.
- [[verification-surveyor|Verification surveyor]] — A command-line tool that requires a person to confirm each extracted identity against external evidence before it is promoted from a queue to a verified record, throttled to ten confirmations per day.
<!-- END AUTO-GENERATED -->

## Cryptographic verification {#group-count-2}

How a reader independently checks that a record hasn't been altered.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: cryptographic-verification -->
- [[crypto-attestation|Cryptographic payload attestation]] — Cryptographic payload attestation lets a reader recompute a hash of published content and compare it against a published value. Unwired, cosmetic prototypes exist in a few release templates; the knowledge wiki does not offer it.
- [[cryptographic-ledgers|Cryptographic ledgers]] — An append-only log where each entry's hash covers the one before it, closed by Ed25519-signed checkpoints and anchored monthly in a public transparency log. Implemented as a linear chain, one flat file per tenant.
<!-- END AUTO-GENERATED -->

## Isolation boundaries {#group-count-3}

What contains a compromise once one occurs. Thin relative to the category's own scope — see the
[[ppn-tenant-vm-isolation|tenant isolation]] and [[service-vm-tenant|VM tenant]] articles in
[Where It Runs](/category/infrastructure) for the commercially load-bearing case, which isn't yet
cross-referenced from here.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: isolation-boundaries -->
- [[sel4-capability-topology|seL4 capability topology]] — In an seL4 system the security policy is the shape of the capability graph established at boot, not a runtime policy layer. First-party work is nine bare-metal test binaries; no platform service runs on seL4.
- [[diode-standard|Diode standard]] — The Diode Standard is the design rule that command and data flow in one direction only, from authority to subject. Several real mechanisms follow it; no component enforces it as a named standard.
- [[genesis-protocol|Genesis protocol]] — The Genesis Protocol is the designed fleet-bootstrapping sequence for os-infrastructure nodes: ship with no prior configuration, boot on any network, and reach a secure, claimable state with no control-plane contact required.
<!-- END AUTO-GENERATED -->

## Data handling and privacy {#group-count-1}

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: data-handling-and-privacy -->
- [[data-sovereignty-telemetry|Data sovereignty and zero-state telemetry]] — Zero-state telemetry is the intended posture of measuring site usage without retaining identifying data. The pipeline running today writes full unmasked IP addresses to a plaintext file for up to a year; masking is not implemented.
<!-- END AUTO-GENERATED -->

## Supply-chain controls {#group-count-2}

Keeping code honest from a contributor's machine to production.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: supply-chain-controls -->
- [[five-stage-supply-chain|Five-stage supply chain]] — The path from a contributor's commit to a customer deployment crosses three repository tiers and two organisations, gated by a heavily guarded promotion script. There is no pull request and no second-party review.
- [[pre-commit-defense-in-depth|Pre-commit defense in depth]] — Four independent git hooks run before a commit is recorded: a helper-only gate, a data-path block, a staged-content secret and size scan, and an author-identity check. Every bypass is logged.
<!-- END AUTO-GENERATED -->

Several articles linked here describe planned, not-yet-built mechanisms and are hedged in
their own text. This page is an orientation, not a compliance attestation.

## See also

- [How It's Built](/architecture/) — how the platform is put together
- [Governance and Standards](/governance/) — what was decided and why it is compliant
- [Where It Runs](/infrastructure/) — the deployed storage and ledger infrastructure these mechanisms protect
