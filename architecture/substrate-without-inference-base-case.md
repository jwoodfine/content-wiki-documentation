---
schema: foundry-doc-v1
title: "Substrate Without Inference — The Base Case"
slug: substrate-without-inference-base-case
category: architecture
type: topic
quality: published
short_description: "The Totebox Archive remains fully operational and freely transferable even when no AI inference tier is available; the deterministic substrate is the load-bearing foundation."
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: substrate-without-inference-base-case.es.md
---

The **Substrate-Without-Inference Base Case** establishes that the Totebox Archive must remain fully operational and freely transferable even when `service-slm` cannot run any inference. AI inference is value-add. The deterministic substrate — the file ledger, the knowledge graph, the extraction pipeline, and the editorial services — is load-bearing. This distinction is encoded in Doctrine claim #54.

## What the base case requires

When all three compute tiers (local specialist, GPU burst, and external API) are simultaneously unavailable, the following must hold:

The WORM file ledger (`service-fs`) is operational: ingest, query, and checkpoint all work. The knowledge runtime (`service-content`) is operational: graph queries, vector search, and temporal queries work, with mutations from non-AI paths only. The input service, extraction service (at the deterministic parsing layer), egress service, people service, and email service are all operational. The Doorman is bound and listening, returning 503 to inference endpoints while keeping health and contract endpoints always responsive. The operator TUI operates in deterministic-only mode.

When marketplace and settlement services are enabled, those are also operational in the base case. Transactions may proceed without AI-assisted grounding; audit and consent records are still enforced.

## What the base case does not require

It is not required that all three tiers be simultaneously unavailable to activate this mode. The base case is simply that at least one tier is down. If even one tier is available, AI-assisted operations resume normally. The deterministic-only mode activates only when every tier has failed simultaneously.

## TUI in deterministic-only mode

When the operator TUI detects that no inference tier is available, it enters deterministic-only mode. The status bar shows that AI is disabled. Natural-language chat input is unavailable. Slash commands that depend on AI — verdict capture, brief submission, adapter listing — gracefully return no-ops or unavailability notices.

Deterministic slash commands remain fully operational: status and health queries, audit ledger queries, knowledge graph queries, keyword search, export, and the ownership transfer preparation flow.

## Transfer of ownership

The "freely transferable" property is more than a philosophical statement. It is implemented through a structured transfer flow. The operator runs a transfer preparation command to produce a self-contained, cryptographically signed bundle: the per-tenant graph snapshot, the audit ledger, the trained adapter weights, the seed taxonomy, the pack manifest, and the tenant configuration. The bundle is signed by the operator's identity key and the integrity is anchored to a public transparency log.

The receiving party imports the bundle into a fresh Totebox. Deterministic operations work immediately on the imported state. AI-assisted operations become available once the new operator configures the compute tier.

## Why this matters commercially

The freely transferable property distinguishes a sovereign asset from a service subscription. When a business is sold, the new owner imports the Totebox bundle and has the complete operational history available immediately — the knowledge graph, the audit ledger, and the workflow vocabulary — without re-subscribing to any platform or engaging migration consultants.

When a business dissolves or splits, each party receives their share of the graph as a portable, cryptographically-signed artefact. When the acquiring party in a corporate transaction imports the bundle, patient or client records, audit history, and operational patterns are available immediately with verifiable provenance.

If Foundry itself ceases operations, the customer continues operating their Totebox indefinitely. The deterministic substrate works without Foundry. The customer loses the ability to receive new vertical packs and to transact on Foundry's marketplace, but their existing operations do not pause.

## Implementation requirement

The base case constrains every service implementation. Every service must have a deterministic baseline that operates without AI. AI-enhanced operations are documented as requiring the AI tier and gracefully degrading when it is unavailable. Regression in the deterministic baseline — any service that fails when all tiers are down — is a doctrine-level signal that a load-bearing function has been made to depend on AI.

## See Also

- [[tier-zero-customer-side-sovereign-specialist]] — the Tier 0 deployment that this base case guarantees
- [[customer-owned-graph-ip]] — the ownership right that the transfer flow exercises
- [[single-boundary-compute-discipline]] — the Doorman's behavior in the base case (503 from inference endpoints; health endpoints always responsive)

## References

1. Doctrine claim #54 — Substrate-Without-Inference Base Case (ratified v0.1.0).
2. Doctrine claim #16 — Three-Ring Architecture; Ring 3 is structurally optional.
3. Doctrine claim #34 — Two-Bottoms Sovereign Substrate; sovereignty without vendor dependency.
4. Sigstore Rekor transparency log — cryptographic anchoring for transfer bundle integrity.

---

## Provenance

Source: `convention-substrate-without-inference-base-case.md` (refined 2026-04-30). Workspace-internal file paths and open questions removed. Transfer flow and marketplace references carry "intended" framing where Phase 5 implementation is pending. BCSC continuous-disclosure posture applied.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
