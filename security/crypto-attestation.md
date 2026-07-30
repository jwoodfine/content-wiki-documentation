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
bcsc_class: public-disclosure-safe
last_edited: 2026-07-30
editor: pointsav-engineering
cites: []
paired_with: crypto-attestation.es.md
---

**Major correction (2026-07-30):** this article describes a live client-side
attestation feature — a browser `crypto.subtle.digest('SHA-256')` call that hashes the
visible article text and displays it "live into the sidebar's metadata block." No such
code exists in the wiki engine (`app-mediakit-knowledge`): a corpus-wide grep for
`crypto.subtle`/`SHA-256`/`digest`/`attest` across every `.rs` and `.js` file in the
crate returns zero hits. `static/app.js` (358 lines) has no hashing logic at all. The
engine's real sidebar (`src/ui/layout.rs:653`, `fn sidebar(...)`) renders site
navigation, category links, and the table of contents — no metadata block, no hash
display. This is the same unbuilt-feature pattern already found and corrected this
session in `capability-based-security.md`, `diode-standard.md`, and `genesis-protocol.md`.
**Flagged as a whole-article architectural mismatch, not line-edited** — needs
project-totebox confirmation of whether client-side attestation is planned or was
simply never built, before this article is corrected or rewritten.

> Cryptographic payload attestation is the mechanism by which PointSav edge nodes dynamically prove the integrity of their published text content to any viewer, using client-side SHA-256 hashing so that any auditor can independently verify a disclosure has not been altered in transit.

**Cryptographic payload attestation** is the process by which [[pointsav-overview|PointSav]] public-facing edge nodes prove the integrity of their textual content to any viewer without requiring trust in the server delivering the content. To fulfill the platform's DARP (Direct, Auditable, Reproducible, Plain-text) requirements, all public-facing edge nodes dynamically compute and display a SHA-256 hash of their visible language content. Any institutional investor, auditor, or counterparty can independently copy the text, compute the hash locally using any SHA-256 tool, and confirm that the displayed hash matches — proving the content has not been altered between publication and the viewer's screen. The operation runs entirely in the browser, with no server involvement in the hash computation itself, which means the attestation is independent of whether the serving infrastructure is trustworthy. See also [[cryptographic-ledgers|cryptographic ledgers]] and [[zero-execution-routing|zero-execution routing]].

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
- Any viewer with a SHA-256 calculator can independently verify the attestation without tools provided by [[pointsav-overview|PointSav]].

This satisfies the BCSC continuous-disclosure requirement that public disclosures be independently verifiable, and the ADR-07 requirement that the integrity chain for content be externally provable without access to internal infrastructure.

## Applications

Cryptographic payload attestation applies to:

- Public regulatory disclosures displayed on [[pointsav-overview|PointSav]]-operated edge nodes.
- Content wiki articles served at `documentation.pointsav.com` where integrity verification matters to institutional readers.
- Any content surface where a reader needs to confirm they are reading the published version and not an altered copy.

## Limitations

The attestation proves integrity at the moment of viewing — it does not prove the content was published at a specific time or that it has not been legitimately updated since a prior version. For time-stamped proof of prior content states, the [[worm-ledger-architecture|WORM ledger architecture]] ([[service-fs-architecture|service-fs]]) and monthly Rekor anchoring provide the complementary mechanism.

## See also

- [[worm-ledger-architecture]]
- [[cryptographic-ledgers]]
- [[machine-based-auth]]
- [[compounding-substrate]]
- [[sovereign-ai-routing]]
