---
schema: foundry-doc-v1
title: "Cryptographic payload attestation"
slug: crypto-attestation
category: security
type: topic
content_type: topic
quality: complete
short_description: "Mechanism by which PointSav edge nodes prove published text integrity to any viewer via client-side SHA-256 hashing, independently verifiable by any auditor."
status: active
bcsc_class: forward-looking
last_edited: 2026-07-30
editor: pointsav-engineering
cites: []
paired_with: crypto-attestation.es.md
---

**Correction — rehedged to planned/intended (2026-07-30):** this article originally
described a live client-side hash-attestation feature in unhedged present tense. No
such code exists: confirmed via both a single-crate check (`app-mediakit-knowledge`'s
`static/app.js` and `src/ui/layout.rs` — no hashing logic anywhere; the real sidebar
renders only nav/categories/TOC) and a broader cross-archive sweep for
`crypto.subtle.digest`/`SHA-256` (the only match anywhere in the fleet is an unrelated
save-integrity hash in `app-workplace-proforma`'s spreadsheet tool, not a wiki
attestation feature). Per operator direction, the body below is rewritten to present
this as planned/intended design, not current behavior.

> Cryptographic payload attestation is a mechanism by which PointSav intends its edge nodes to dynamically prove the integrity of their published text content to any viewer, using client-side SHA-256 hashing so that any auditor could independently verify a disclosure has not been altered in transit. This is a planned feature, not yet implemented.

**Cryptographic payload attestation**, once implemented, would be the process by which [[pointsav-overview|PointSav]] public-facing edge nodes prove the integrity of their textual content to any viewer without requiring trust in the server delivering the content. The design intent, per the platform's DARP (Direct, Auditable, Reproducible, Plain-text) requirements, is for public-facing edge nodes to dynamically compute and display a SHA-256 hash of their visible language content, so any institutional investor, auditor, or counterparty could independently copy the text, compute the hash locally, and confirm the displayed hash matches. **No such mechanism exists in the wiki engine (`app-mediakit-knowledge`) or anywhere else in the monorepo today.** See also [[cryptographic-ledgers|cryptographic ledgers]] and [[zero-execution-routing|zero-execution routing]].

## How it is intended to work

The design calls for the native browser `crypto.subtle.digest('SHA-256')` API to:

1. **Extraction:** read the current visible text of the language block (English or Spanish).
2. **Encoding:** encode the text into a `Uint8Array` using UTF-8.
3. **Hashing:** process the encoded array through SHA-256.
4. **Display:** inject the resulting hash live into a metadata block beside the content it attests.

None of this is implemented today — the wiki engine's static assets carry no hashing logic, and its real sidebar renders only navigation, categories, and the table of contents.

## Intended security posture

Once built, the attestation would be zero-execution-server for the hash computation — the server would deliver the JavaScript and content, but the hash would be computed by the browser using only local data. The intended effect: a man-in-the-middle attacker modifying content in transit would produce a detectable hash mismatch, and any viewer with a SHA-256 calculator could independently verify the attestation.

## Intended applications

Once implemented, cryptographic payload attestation is intended to apply to:

- Public regulatory disclosures displayed on [[pointsav-overview|PointSav]]-operated edge nodes.
- Content wiki articles served at `documentation.pointsav.com`.
- Any content surface where a reader needs to confirm they are reading the published version.

## Intended limitations

Even once built, the attestation would only prove integrity at the moment of viewing — it would not prove the content was published at a specific time or that it has not been legitimately updated since a prior version. Time-stamped proof of prior content states already exists independently of this planned feature, via the [[worm-ledger-architecture|WORM ledger architecture]] ([[service-fs-architecture|service-fs]]) and monthly Rekor anchoring — both real, verified mechanisms.

## See also

- [[worm-ledger-architecture]]
- [[cryptographic-ledgers]]
- [[machine-based-auth]]
- [[compounding-substrate]]
- [[sovereign-ai-routing]]
