---
schema: foundry-doc-v1
title: "The System Substrate Architecture"
slug: system-substrate-doctrine
category: architecture
type: topic
quality: published
short_description: The kernel-level architecture beneath every PointSav service — a customer-rooted capability ledger that is the audit log, a two-bottoms sovereign OS strategy, and three mechanisms for time-bound capabilities, reproducible verification, and boot-anywhere recovery.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites:
  - sec-17a-4-f
  - eidas-qualified-preservation
  - rfc-3161
  - opentimestamps
  - constitutional-ai-2212-08073
  - olmo3-allenai
paired_with: system-substrate-doctrine.es.md
---

The **System Substrate Architecture** defines the layer beneath every PointSav operating system, service, and application — the kernel, the capability model, the audit ledger, and the ownership-transfer ceremony that together constitute a cryptographically sovereign deployment.

Two core structural properties drive the architecture. **The Capability Ledger Substrate**: the running system's capability state IS the append-only {{gli|WORM}} ledger; the kernel consults the ledger before honoring any invocation; the deployment is derived from the ledger. **The Two-Bottoms Sovereign Substrate**: the same binaries run on either a formally verified kernel ({{gli|seL4}} today, with a future no-std Rust moonshot-kernel) or a sovereignty-grade compatibility kernel (NetBSD with Veriexec and offline-reproducible builds), depending on hardware constraints and required assurance level.

## Cryptographic State Composition

No production system in 2026 bundles source, formal verification proofs, capability graph, audit ledger, and signing keys under a single transparency-log root with an ownership-transfer ceremony. The cryptographic primitives are mature individually — {{gli|C2SP}} `signed-note` supports witness cosigning, {{gli|C2SP}} `tlog-tiles` provides the {{gli|WORM}} substrate, {{gli|seL4}} delivers kernel-mediated capability invocation, CHERIoT 1.0 silicon shipped commercially in March 2026. What is new is their composition into a single deployable artefact.

Existing approaches root attestation in the vendor's keys (cloud providers), the state (national digital-identity stacks), or the chip vendor (secure enclave silicon). In each case, the attested proof is proof of the vendor's controls, not proof of the customer's controls. The Foundry composition inverts this: every attestation chain terminates at the customer's own apex signing key.

## Immutable Capability Ledger

Every kernel-mediated capability invocation, grant, revocation, and transition emits a signed entry to a customer-rooted Merkle log. Before the kernel honors any capability invocation, it consults the ledger for the current revocation status, the time-bound expiry, and the validity of the apex root.

**The deployment IS the ledger.** To boot a Foundry deployment is to replay the ledger from genesis forward. To shut down is to append a shutdown entry. To upgrade is to append a version-bump entry. To rotate keys is to append a rotation entry. The deployment state at any point in time is the deterministic application of all ledger entries up to that point. An auditor with the ledger and the source can reconstruct any historical state.

The customer's apex signing key is held by the customer — in their TPM, in an HSM they own and operate, or as a paper-printed seed for air-gapped recovery. No Foundry service, no provider, no chip vendor sits between the customer and the ledger root.

## Apex Cosigning and Ownership Transfer

Ownership transfer is a single signed ledger entry. The previous apex appends a revocation entry releasing the deployment to a new apex. The new apex cosigns the next checkpoint root via the {{gli|C2SP}} `signed-note` multi-signature primitive. From that checkpoint forward, only the new apex's signature is required. The deployment continues running without state migration, downtime, or vendor involvement.

The new apex inherits the entire ledger history, all capability state, all audit records, and all formal verification proofs. The previous apex retains only the immutable historical record that they were the apex from genesis to the rotation entry.

This mechanism is intended to address M&A integration, divestiture, customer breakout, and operator succession — all handled by the same apex-rotation ceremony.

## Operational Recovery Mechanisms

**Mechanism A — Time-Bound Capabilities.** A capability carries an expiry timestamp and a witness public key. The kernel refuses to honor the capability past expiry unless a signed witness record is presented whose hash appears in the current capability log Merkle root. Extending a capability requires a fresh witness signature AND an appearance in the public log. The witness key belongs to the customer; every authorization extension is logged and customer-cosigned.

Verification cost is linear in federation cardinality. On server-class hardware (n2-class x86), a single-signature Ed25519 verify takes approximately 3.4 ms; a cache hit on the most recent capability takes approximately 8 ns. Cache is structurally non-optional in any production deployment.

**Mechanism B — Reproducible Verification On Customer Metal.** Every release ships Isabelle/HOL theorem files for the formally verified {{gli|seL4}} portion, Rust ownership traces for the system layer, a reproducible-build graph anchored to a public transparency log, and a source manifest signed via Sigstore Cosign and witness-cosigned by the customer's apex. Spot-check verification (signature verification, cached intermediate proofs, reproducible-build replay) is intended to complete in under 60 minutes on a commodity laptop. Full Isabelle/HOL replay is optional and may take hours to days.

**Mechanism C — Boot-Anywhere Capability Recovery.** The customer's full operational identity reconstructs from a paper-printed seed plus the public transparency-log state. The seed encodes the apex private key (BIP-39 or printable base32), the ledger anchor reference, and optionally pre-trusted witness federation public keys — the whole fitting on a single index card or A4 sheet. No vendor portal, no cloud round-trip, no HSM is required for recovery. The system boots on borrowed hardware (NetBSD compat-bottom) and replays the ledger from genesis using the reconstituted apex.

## Dual-Kernel Execution Environments

| Bottom | Role | Kernel |
|---|---|---|
| Native | Highest-assurance, regulated, cyberphysical | {{gli|seL4}} (AArch64-first; 15.0.0 as of March 2026) → planned moonshot-kernel (no-std Rust) |
| Compat | Sovereignty-grade, boot-anywhere commodity hardware | NetBSD with Veriexec + offline-reproducible `build.sh` + rump kernels |

NetBSD is chosen specifically for BSD 2-clause transferability, Veriexec's mirror of {{gli|seL4}}'s verified-image-only-boot invariant, `build.sh` offline reproducibility (rebuild the entire OS from a USB-archived snapshot), rump kernels enabling the same driver code in user space and embedded contexts, 57 official hardware ports, and an independent foundation with no hyperscaler entanglement.

The same `os-*` binaries run on either bottom via a thin shim. Linux is not in the architecture; it remains available as an unsupported community-tier fallback for hardware neither bottom covers but is not in the trust chain and not in any PointSav deployment guide.

AArch64 is the primary hardware target. RISC-V64 has more complete formal verification but commodity hardware remains significantly weaker in 2026. x86_64 has functional correctness on {{gli|seL4}} without information-flow or binary correctness proofs; it is used for development hosts and the NetBSD compat-bottom but not for the {{gli|seL4}} native bottom.

## Honest Capability Boundaries

The substrate does not claim to own what it does not own. Silicon, microcode, and most boot firmware (Boot Guard, ME, PSP) are vendor-controlled. On a curated short-list of Coreboot-compatible boards or OpenPOWER hardware, the bootloader is controllable. The substrate owns the kernel, the system layer, the application layer, the capability ledger, the identity and audit trail, the build provenance, and the formal verification artifacts.

## Phased Rollout Architecture

Phase 0 workspace hygiene for the `project-system` cluster is pending. Phase 1A — a capability-ledger primitive prototype binding {{gli|C2SP}} signed-note multi-signature checkpoints to capability invocation — is planned work. Phase 1B — the `moonshot-toolkit` Rust CLI for orchestrating {{gli|seL4}} builds with a reproducible-build harness — is planned foundational work. NetBSD compat-bottom prototype, TOPIC and GUIDE drafting, and the minimal moonshot-kernel capability subset are subsequent phases.

## See Also

- [[worm-ledger-architecture]] — the {{gli|WORM}} substrate primitive ({{gli|C2SP}} tlog-tiles + signed-note) that the Capability Ledger extends
- [[compounding-doorman]] — the inference boundary that operates above the system substrate
- [[disclosure-substrate]] — the disclosure-record substrate that sits above this layer

## References

1. SEC Rule 17a-4(f) — electronic records preservation requirements.
2. eIDAS Regulation — qualified electronic signatures and trust services.
3. RFC 3161 — Time-Stamp Protocol.
4. OpenTimestamps — Bitcoin-anchored timestamping.
5. Constitutional AI: Harmlessness from AI Feedback, Bai et al., arXiv 2212.08073.
6. OLMo 3 — Allen Institute for AI, Apache 2.0.

---

## Provenance

Source material: ratified 2026-04-26. Disciplines applied: no body H1; structural positioning (competitor attestation products removed by competitive comparison; architectural contrast retained structurally); BCSC forward-looking framing on moonshot-kernel, {{gli|seL4}} SMP verification target, Phase 1A-1B implementation (planned/intended/target); banned-vocabulary pass; workspace-internal cluster paths and author attribution stripped.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
