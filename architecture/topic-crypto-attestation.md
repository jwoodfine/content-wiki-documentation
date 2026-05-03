---
schema: foundry-doc-v1
title: "Cryptographic Payload Attestation"
slug: topic-crypto-attestation
category: architecture
type: topic
quality: core
short_description: "Cryptographic payload attestation is the mechanism by which PointSav edge nodes dynamically prove the integrity of their published text content to any viewer, using client-side SHA-256 hashing so that any auditor can independently verify a disclosure has not been altered in transit."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: topic-crypto-attestation.es.md
---

# Cryptographic Payload Attestation

> Cryptographic payload attestation is the mechanism by which PointSav edge nodes dynamically prove the integrity of their published text content to any viewer, using client-side SHA-256 hashing so that any auditor can independently verify a disclosure has not been altered in transit.

**Cryptographic payload attestation** is the process by which PointSav public-facing edge nodes prove the integrity of their textual content to any viewer without requiring trust in the server delivering the content. To fulfill the platform's DARP (Direct, Auditable, Reproducible, Plain-text) requirements, all public-facing edge nodes dynamically compute and display a SHA-256 hash of their visible language content. Any institutional investor, auditor, or counterparty can independently copy the text, compute the hash locally using any SHA-256 tool, and confirm that the displayed hash matches — proving the content has not been altered between publication and the viewer's screen. The operation runs entirely in the browser, with no server involvement in the hash computation itself, which means the attestation is independent of whether the serving infrastructure is trustworthy.

## How It Works

The attestation mechanism uses the native browser `crypto.subtle.digest('SHA-256')` API:

1. **Extraction:** The JavaScript engine reads the current `innerText` of the visible language block (English or Spanish).
2. **Encoding:** The text is encoded into a `Uint8Array` using UTF-8 encoding.
3. **Hashing:** The encoded array is processed through SHA-256 via `crypto.subtle.digest`.
4. **Display:** The resulting hexadecimal string is injected live into the sidebar's metadata block, visible alongside the content it attests.

The computation happens at page render time and updates whenever the visible content changes. The hash displayed is always the hash of what the viewer is currently reading, not a cached value from a prior state.

## Security Posture

The attestation is zero-execution-server for the hash computation: the server delivers the JavaScript and the content, but the hash is computed by the browser using only local data. This means:

- A man-in-the-middle attacker who modified the content in transit would produce a hash mismatch that any viewer could detect.
- The serving infrastructure cannot silently substitute different content without breaking the displayed hash.
- Any viewer with a SHA-256 calculator can independently verify the attestation without tools provided by PointSav.

This satisfies the BCSC continuous-disclosure requirement that public disclosures be independently verifiable, and the ADR-07 requirement that the integrity chain for content be externally provable without access to internal infrastructure.

## Applications

Cryptographic payload attestation applies to:

- Public regulatory disclosures displayed on PointSav-operated edge nodes.
- Content wiki articles served at `documentation.pointsav.com` where integrity verification matters to institutional readers.
- Any content surface where a reader needs to confirm they are reading the published version and not an altered copy.

## Limitations

The attestation proves integrity at the moment of viewing — it does not prove the content was published at a specific time or that it has not been legitimately updated since a prior version. For time-stamped proof of prior content states, the WORM ledger architecture (`service-fs`) and monthly Rekor anchoring provide the complementary mechanism.

## See Also

- [[worm-ledger-architecture]]
- [[cryptographic-ledgers]]
- [[machine-based-auth]]
- [[compounding-substrate]]
- [[sovereign-ai-routing]]

## References

- `DOCTRINE.md §IX` — DARP (Direct, Auditable, Reproducible, Plain-text) posture
- `conventions/worm-ledger-design.md` — complementary WORM integrity mechanism for stored records
- `conventions/bcsc-disclosure-posture.md` — continuous-disclosure context; independently verifiable disclosures
