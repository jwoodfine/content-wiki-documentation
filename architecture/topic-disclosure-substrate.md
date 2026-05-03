---
schema: foundry-doc-v1
title: "The Disclosure Substrate"
slug: topic-disclosure-substrate
category: architecture
type: topic
quality: complete
short_description: "The Disclosure Substrate is the Foundry mechanism that makes a version-controlled Markdown wiki the primary continuous-disclosure record, combining signed authorship chains, cryptographic content hashes, and planned per-jurisdiction export adapters to produce regulator-compliant outputs from a single source."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
  - bcsc-continuous-disclosure
  - mondaq-ni-51-102-summary
  - sec-17a-4-f
  - eidas-qualified-preservation
  - etsi-ts-119-511
  - etsi-en-319-401
  - cen-ts-18170-2025
  - fca-ps-24-19
  - ixbrl-esef
  - esap-eu-2027
  - opentimestamps
  - rfc-3161
  - rfc-9162
  - sigstore-rekor-v2
  - c2sp-tlog-tiles
  - cloud-act-us
  - w3c-verifiable-credentials
  - vectara-hhem
  - c2pa
  - c3ai-acm-2025
  - computerweekly-sovereign-2026
paired_with: topic-disclosure-substrate.es.md
---

# The Disclosure Substrate

> The Disclosure Substrate is the Foundry mechanism that makes a version-controlled Markdown wiki the primary continuous-disclosure record, combining signed authorship chains, cryptographic content hashes, and planned per-jurisdiction export adapters to produce regulator-compliant outputs from a single source.

A documentation wiki can be designed so that it is not a description of a company's disclosures — it is the disclosure record. Every committed article carries a signed authorship chain, a cryptographic hash, and a timestamp anchored to an external ledger. Regulators and analysts read the same corpus that internal contributors write. The filing and the working document are the same artefact. That is **The Disclosure Substrate**. This article explains what it means structurally, how it differs from conventional investor relations practice, and what components make it operational.

## Overview

The Disclosure Substrate is a wiki engine, a version-controlled Markdown corpus, and a set of cryptographic and export adapters designed together so that the wiki is the primary continuous-disclosure record — not a supplement to a statutory filing, and not a mirror of a separately-maintained investor relations platform.

Under `[ni-51-102]` (NI 51-102 Continuous Disclosure Obligations), a reporting issuer is required to keep investors and the public continuously informed of material changes, forward-looking information, and annual and interim reports. The conventional implementation separates this into three bodies of text across three vendor stacks: internal documentation, an investor relations website, and statutory filings on SEDAR+ or EDGAR. Those three bodies are separately authored, often inconsistent, and difficult to audit against each other.

The substrate collapses the three into one: a single Markdown corpus under issuer infrastructure, rendered into reader-facing wiki pages, regulator-compliant export packages, and cryptographic proof-of-state artefacts — all from the same source.

## Ring and Role

The Disclosure Substrate spans all three rings and the workspace documentation layer. Ring 1 provides the inbound content stream (articles authored and committed by contributors). Ring 2 provides the search and knowledge-graph layer that indexes the corpus. Ring 3 provides the AI grounding layer (planned) that validates citations before publication. The cryptographic anchoring, export adapters, and the registry that validates every citation are workspace-layer infrastructure. The substrate is activated on every commit to the content-wiki repos.

## Architecture

### How the substrate operates

Every article (called a TOPIC) in the wiki carries YAML frontmatter declaring its title, slug, category, status, and — where the content is grounded in external material — its citation dependencies. Citations are resolved against a workspace-level registry; inline references use stable IDs (`[ni-51-102]`); the registry maps each ID to a title, URL, and optional clause reference. This is the citation-substrate layer per `conventions/citation-substrate.md`.

Every committed TOPIC acquires a stable cryptographic identity: a Git commit SHA plus file path, and a content hash. Both are exposed in the rendered HTML so that an external indexer or regulator fetcher can pin a specific content state.

Two timestamp mechanisms are planned for Phase 7 of the wiki engine (intended subject to the milestone schedule described in `conventions/disclosure-substrate.md` §6; actual delivery is subject to engineering capacity and milestone sequencing):

- **OpenTimestamps anchoring** `[opentimestamps]` — planned cryptographic anchoring of each commit to the Bitcoin blockchain. Bitcoin anchoring is free, open-source, and external to the issuer's infrastructure; it produces proof that a specific content state existed at a specific block height, without requiring trust in any single intermediary.
- **RFC 3161 timestamping** `[rfc-3161]` — planned formal timestamp tokens from a recognised Time-Stamp Authority. RFC 3161 tokens carry legal recognition in EU and most common-law jurisdictions. The planned use of both mechanisms provides cryptographic redundancy: one anchors to a decentralised ledger; the other provides the formally-recognised token a regulator or court can verify.

Two timestamp fields are planned per TOPIC — `published_at` (when the wiki rendered this content state) and `valid_at` (when the underlying fact the TOPIC asserts holds). The distinction matters for forward-looking information labelled under `[osc-sn-51-721]`: the publication date and the validity period of the information are separate facts that a disclosure record must be able to distinguish.

Material-change commits — those whose TOPIC edits constitute material changes under the `[bcsc-continuous-disclosure]` posture — are intended to emit a signed Disclosure-Diff artefact alongside the updated TOPIC. The Disclosure-Diff is a cryptographically signed diff of the change, not a derivative of the TOPIC; it is planned to be committed as a W3C Verifiable Credential `[w3c-verifiable-credentials]` alongside the affected article. This is forward-looking and subject to the cautionary factors in `[ni-51-102]` and `[osc-sn-51-721]`.

### Per-jurisdiction export adapters (planned)

A pluggable adapter layer is planned (intended, pending `project-disclosure` cluster scope; actual delivery subject to cluster activation and engineering sequencing) to transform the Markdown corpus into the submission format each regulatory surface requires:

| Adapter | Target surface |
|---|---|
| `export-sedar` | SEDAR+ — Canadian continuous-disclosure filings under `[ni-51-102]` |
| `export-edgar` | SEC EDGAR — US filings; XBRL-tagged under Exchange Act rules |
| `export-esef` | EU ESEF mandate — iXBRL `[ixbrl-esef]` annual reports; ESAP Phase 1 target July 2027 `[esap-eu-2027]` |
| `export-edinet` | Japan EDINET — FSA XBRL filings |
| `export-dart` | Korea DART — FSS XBRL filings |
| `export-magna` | Israel MAGNA — iXBRL filings |

Where a jurisdiction requires qualified electronic preservation — for example, EU `[eidas-qualified-preservation]` or ETSI `[etsi-ts-119-511]` and `[etsi-en-319-401]` long-term preservation standards — the planned adapters are designed to produce outputs that satisfy those preservation requirements by including the issuer's signing certificate chain and the RFC 3161 timestamp token in the submission package. The `[cen-ts-18170-2025]` standard on trusted digital preservation is the reference specification for this design.

The FCA PS24/19 `[fca-ps-24-19]` modernisation of the UK's National Storage Mechanism to an iXBRL-based system is incorporated into the planned `export-esef` adapter's scope, as UK-listed issuers following the post-Brexit iXBRL path use the same technical format as ESEF.

Each adapter is planned as a separable Rust crate. New jurisdictions are intended to be additive without changing the substrate's core. Forward-looking statements in this section depend on the material assumption that the `project-disclosure` cluster activates and that the XBRL taxonomy mapping work described in `conventions/disclosure-substrate.md` §3.4 completes before the adapters are required in production.

### Substrate Substitution applied to disclosure platforms

Conventional investor relations practice positions a separate IR platform between the issuer's internal documentation and public disclosure. Such platforms typically operate on third-party cloud infrastructure and serve the disclosure to investors from that infrastructure, with the legally-material record living at the vendor rather than under the issuer's own infrastructure.

Per Doctrine claim #29 (Substrate Substitution), the substrate's positioning is different: the wiki is the disclosure record, served directly under the issuer's own domain, signed under the issuer's own key, and anchored to external ledgers the issuer controls. There is no separate disclosure-distribution platform between the Markdown source and the reader.

What IR-platform services provide that the substrate does not — investor targeting, sell-side consensus aggregation, surveillance analytics — are composable via Ring 1 MCP adapters `[computerweekly-sovereign-2026]` as the substrate matures. The substrate replaces the substrate-of-record function; it composes with adjacent services that depend on multi-issuer panel data the substrate cannot replicate from a single deployment.

Vendor SaaS disclosure platforms running on US-headquartered infrastructure face a structural property worth naming: the CLOUD Act `[cloud-act-us]` extends US extraterritorial data-access authority over US-headquartered providers regardless of where customer data is stored. For an issuer in a jurisdiction where vendor jurisdiction matters — EU GDPR under the Schrems II posture, Health Canada residency mandates, Saudi Arabia's PDPL — the disclosure substrate's value is that the record lives under the issuer's own infrastructure, in the issuer's own jurisdiction, with the issuer holding the signing key. This is jurisdiction-portability by construction, not by policy agreement with a vendor.

### Substrate-enforced AI grounding (planned)

A disclosure substrate that permits AI-generated text to reach publication without verification produces a structural liability: if the AI hallucinated a fact, that fact is in the disclosure record. Vectara's HHEM `[vectara-hhem]` is a detection-only approach — identifying hallucinations after generation. The substrate's planned mechanism is refusal-to-render: a TOPIC whose proof-of-grounding chain does not verify does not reach the reader.

The planned mechanism (Phase 9 of the wiki engine; intended subject to the `project-disclosure` cluster reaching this milestone; subject to the cautionary factors in `[ni-51-102]` and `[osc-sn-51-721]`):

1. Every claim in an AI-drafted TOPIC must be paired with a citation ID resolvable in the citations registry.
2. Each citation's content hash must verify against the registry's stored hash.
3. An adversary-AI verdict pass (a separate model evaluation) confirms the claim is grounded in the cited source's actual content.
4. The verdict is signed as a W3C Verifiable Credential `[w3c-verifiable-credentials]` and committed in the same Git commit as the TOPIC.
5. The wiki renderer refuses to serve any TOPIC whose proof-of-grounding chain does not verify.

This mechanism does not depend on the model that authored the TOPIC being trustworthy. It depends only on the citation registry being accurate and the adversary-AI verdict being more conservative than the authoring model. The C2PA standard `[c2pa]` for content provenance and the ACM study on AI disclosure practices `[c3ai-acm-2025]` are the external reference points for the grounding discipline's design.

Material assumptions: the `project-disclosure` cluster activates; the constitutional-layer adapter from the `project-slm` cluster (Doctrine claim #31) is available before Phase 9 begins; the citation registry maintains content hashes as specified in `conventions/citation-substrate.md` §5.

## Configuration

Per `[ni-51-102]` continuous-disclosure language, the following items in this article are forward-looking:

- The planned per-jurisdiction export adapters depend on `project-disclosure` cluster activation and XBRL taxonomy mapping work. Actual delivery is subject to engineering sequencing and operator prioritisation.
- The planned Sigstore Rekor v2 monthly anchoring and RFC 3161 timestamping depend on the `fs-anchor-emitter` binary completing and on the IaC units in `infrastructure/local-fs-anchoring/` activating.
- The planned substrate-enforced AI grounding (Phase 9) depends on the constitutional-layer adapter from `project-slm` cluster and on `project-disclosure` reaching that phase.
- The planned Disclosure-Diff signed artefacts and Subscriber Proof-of-Receipt W3C VCs depend on Phase 8 completing before Phase 9.

Actual results may vary from the planned trajectory described above. All forward-looking statements depend on the material assumptions named in each section and are subject to operational reality, engineering capacity, and operator decisions on cluster prioritisation.

## See Also

- [[topic-compounding-substrate]]
- [[topic-substrate-native-compatibility]]
- [[topic-decode-time-constraints]]
- [[topic-canadian-simple-copyright]]
- [[topic-citation-substrate]]

## References

- `conventions/disclosure-substrate.md` — the operational convention
- `conventions/bcsc-disclosure-posture.md` — the FLI labelling rules
- DOCTRINE.md Claim #29 — Substrate Substitution
- `[ni-51-102]` — NI 51-102 Continuous Disclosure Obligations
- `[osc-sn-51-721]` — OSC Staff Notice 51-721 Forward-Looking Information Disclosure
- `[bcsc-continuous-disclosure]` — BCSC continuous disclosure guidance
- `[eidas-qualified-preservation]` — EU eIDAS qualified electronic preservation
- `[etsi-ts-119-511]` — ETSI TS 119 511 long-term preservation
- `[rfc-3161]` — RFC 3161 Internet X.509 PKI Time-Stamp Protocol
- `[rfc-9162]` — RFC 9162 Certificate Transparency Version 2.0
- `[sigstore-rekor-v2]` — Sigstore Rekor v2 transparency log
- `[c2sp-tlog-tiles]` — C2SP tlog-tiles format
- `[opentimestamps]` — OpenTimestamps anchoring
- `[cloud-act-us]` — US CLOUD Act (extraterritorial data access)
- `[w3c-verifiable-credentials]` — W3C Verifiable Credentials
- `[c2pa]` — Coalition for Content Provenance and Authenticity
- `[c3ai-acm-2025]` — ACM study on AI disclosure practices
