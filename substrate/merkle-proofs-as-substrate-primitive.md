---
schema: foundry-doc-v1
title: "Merkle proofs as a substrate primitive"
slug: merkle-proofs-as-substrate-primitive
category: substrate
status: stub
bcsc_class: no-disclosure-implication
last_edited: 2026-04-28
editor: pointsav-engineering
cites:
 - rfc-9162
 - doctrine-claim-33
 - doctrine-claim-34
---

`system-core` ships two RFC 9162 Merkle proof primitives — inclusion proofs and consistency proofs — as the cryptographic floor of the Capability Ledger Substrate. Together with the C2SP signed-note checkpoint format they gate ledger apply-side validity and make capability state auditable without requiring consumer good behaviour.

## What Merkle proofs are

Hash trees commit to a sequence of leaves: each leaf is hashed with a 0x00 domain-separation prefix; each internal node hashes two children with a 0x01 prefix (RFC 9162 §2.1.1). The root hash commits to the entire sequence. Proof paths are logarithmic in tree size. Collision resistance of the underlying hash function is the sole security assumption. The important distinction: *committing to* a sequence (root hash) is not the same as *proving membership or extension* of that sequence (proof path).

## Two flavours: inclusion and consistency

Inclusion proofs (RFC 9162 §2.1.3) prove that a single leaf is present in a tree of a given size. Consistency proofs (RFC 9162 §2.1.4) prove that a tree of size N+k is a valid extension of a tree of size N. The two flavours answer different questions: "is this leaf in the log?" versus "is this newer log a continuation of the older one?" Different consumers need different proofs; the same hash tree supports both.

## Inclusion proofs in `system-core`

The `InclusionProof` struct and its `verify` method implement the RFC 9162 §2.1.3 tree-walking algorithm. The `rfc9162_leaf_hash` (0x00 prefix) and `rfc9162_internal_hash` (0x01 prefix) helpers are the only non-trivial primitives. Test coverage: 11 tests including a full verification grid over tree sizes 1–8. Typical verification cost: 10–20 microseconds for representative tree sizes (Phase 1A.4 benchmarks).

## Consistency proofs in `system-core`

The `ConsistencyProof` struct and its `verify` method seed both accumulators from `hashes[0]` and track `fn`/`sn` counters until both reach zero. Nine error variants distinguish structural failures from cryptographic failures. Edge cases handled explicitly: `old_size == 0` (per RFC 9162 vs RFC 6962), `old_size == new_size` (requires empty proof), and power-of-two boundary transitions. Test coverage: 11 tests in `consistency_proof.rs`.

## Composed primitives on `SignedCheckpoint`

`SignedCheckpoint::verify_inclusion_proof` and `verify_consistency_proof` chain three steps in a single call: tree-size invariant check → signature verification → raw-proof verification. This composition is the kernel-facing API surface; raw `InclusionProof` and `ConsistencyProof` are building blocks and are not advertised directly. The `CheckpointInclusionError` and `CheckpointConsistencyError` taxonomies distinguish "checkpoint is malformed" from "proof is invalid" from "signer's public key is wrong".

## Consumer integration in `system-ledger`

The `LedgerConsumer` trait's `apply_witness_record` was promoted in Phase 1A.4 (commit 2b9ca9c, v0.1.x → v0.2.0 trait-signature change) from a trust-the-caller shortcut to an inclusion-proof-gated apply. The consult-capability hot path stays microsecond-fast via `CheckpointCache`; the apply side gains write-validity guarantees from Merkle inclusion proofs. The apex-handover ceremony requires inclusion-proof verification at handover height; strict-handover policies layer on top via `verify_apex_handover`.

## Why this matters as a substrate primitive

The Capability Ledger Substrate requires a customer-rooted Merkle log to make capability state auditable. The Two-Bottoms Sovereign Substrate requires that a deployment-as-cryptographic-artefact be inheritable across native (seL4) and compat (NetBSD) substrates without re-trusting the runtime. Merkle inclusion and consistency proofs are the cryptographic primitives that make both properties hold without requiring consumer good behaviour. The primitives run in `no_std`-compatible Rust, are kernel-consumption-eligible, and are reused across `system-core` consumers without per-consumer reimplementation.

## See also

- capability-ledger-substrate — the ledger the proofs protect
- [[worm-ledger-architecture]] — WORM ledger design that composes with checkpoint verification
- [[disclosure-substrate]] — how the ledger audit trail satisfies disclosure obligations

## References

- **RFC 9162** — Certificate Transparency Version 2.0. IETF, 2021. Defines the Merkle tree hash algorithm, inclusion proof, and consistency proof specifications used verbatim in `system-core`. https://datatracker.ietf.org/doc/html/rfc9162
- [[worm-ledger-design]] — WORM ledger design; `system-ledger` implements this.
