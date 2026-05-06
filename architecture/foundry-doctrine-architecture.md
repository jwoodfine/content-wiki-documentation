---
title: "Foundry Doctrine — Architectural Overview"
slug: foundry-doctrine-architecture
category: architecture
status: stable
bcsc_class: public-disclosure-safe
last_edited: 2026-04-30
editor: pointsav-engineering
quality: complete
references:
  - id: 1
    text: "NI 51-102 Continuous Disclosure Obligations — BCSC"
  - id: 2
    text: "OSC Staff Notice 51-721 Forward-Looking Information Disclosure"
  - id: 3
    text: "OLMo 3 — Allen Institute for AI. allenai.org/blog/olmo3"
  - id: 4
    text: "seL4 Microkernel — Data61/CSIRO. sel4.systems"
  - id: 5
    text: "Overture Maps Foundation. overturemaps.org"
---

Foundry Doctrine is the constitutional charter for the PointSav platform. It encodes the principles, commitments, and structural claims that govern every engineering, operational, and editorial decision across the workspace. The current release is v0.1.0 ALPHA, ratified 2026-04-30 under the `ps-administrator` signing identity.

## The Six Pillars

Foundry is built on six foundational commitments that take precedence over any specific design decision or engineering convenience:

**Plain text, flat file, open source.** Every artifact produced by the substrate — knowledge graphs, audit ledgers, documentation, configuration, training data — is plain text. No binary-only stores, no proprietary formats that require a running service to read.

**Sovereignty is structural, not procedural.** Customer data and compute stay inside the customer's boundary by construction. Firewall rules, bearer-token confinement, and WORM append-only ledgers enforce sovereignty at the infrastructure level; no policy document is load-bearing.

**Ring 3 is optional.** The AI inference ring (`service-slm` and the Yo-Yo compute substrate) is structurally optional. The deterministic substrate — knowledge graph, search, ingest, egress — functions completely when AI is disabled or unavailable. Optional Intelligence is a design constraint, not a marketing framing.

**Vendor → Customer → Deployments is the only flow.** Engineering source lives in `pointsav/*` canonical repos. Customer runbooks live in `woodfine/*`. Runtime instances are numbered and local-only. No reverse writes. No shortcuts through the layer boundary.

**Every session trains the model.** Every Task, Root, and Master session that produces output — diffs, briefs, editorial refinements, sysadmin interactions — generates a training tuple that accumulates in the apprenticeship corpus. The substrate sharpens monotonically with use.

**Human checkpoint at F12 is mandatory.** SYS-ADR-10 — the final human checkpoint before any state is committed to a verified ledger — is never bypassed. Automation serves the human; no automated path exists around F12.

## The Fifty-Two Leapfrog Claims

The doctrine enumerates 54 numbered structural claims that together constitute Foundry's competitive positioning relative to hyperscaler software-as-a-service. Each claim identifies a structural property of the Foundry substrate that hyperscaler economics or architecture structurally foreclose — not a feature advantage, but a property that cannot be replicated without changing the underlying business model.

Representative clusters from the full claim set:

**Sovereignty and data ownership (claims #1–#11, #48, #54).** The customer's knowledge graph is the customer's intellectual property. The per-tenant WORM ledger is customer-rooted. Export formats are open at day zero. The substrate runs fully — queries, audit, search, transfer of ownership — with no Foundry-side dependency. No hyperscaler SaaS can offer this without abandoning per-tenant hosting economics.

**Compounding substrate (claim #18).** Each unit of work — a commit, a session, an editorial pass, a training run — increases the capability of the next unit. Engineering work trains the engineering adapter; editorial work trains the language-protocol adapter; sysadmin interactions train the sysadmin adapter. The capability curve is monotonically increasing with work volume; the marginal cost of capability declines over time.

**Adapter composition algebra (claim #22).** At inference time the Doorman composes up to three adapters: `base ⊕ tenant ⊕ protocol`. The resulting inference is tuned simultaneously to the base model's general capability, the tenant's domain vocabulary and operational patterns, and the current request's genre requirements. Per-tenant continued pretraining (claim #15) deepens the tenant adapter monotonically as the corpus accumulates.

**Apprenticeship substrate (claim #32).** Code-shaped and prose-shaped work routes through the Doorman as a structured brief. The apprentice (local SLM) produces a candidate diff with cited reasoning. A senior identity issues a signed verdict. The (brief, attempt, verdict, final-diff) tuple lands in the apprenticeship corpus and feeds the next training cycle. Shadow routing on every commit exercises the apprentice continuously.

**Capability ledger substrate (claim #33).** Every kernel-mediated capability invocation emits a signed entry to a customer-rooted Merkle log. Revocation is a log entry. Ownership transfer is an apex-cosigning ceremony — no state migration, no service interruption. The deployment IS the ledger; the running system is the materialization of the ledger state.

**Two-bottoms sovereign substrate (claim #34).** The platform runs on two kernel bottoms: seL4 (native, formally verified, AArch64-first) and NetBSD (compatibility, BSD 2-clause, boot-anywhere). The same `os-*` binaries run on either bottom via a thin shim. The customer boots the same substrate on a leased laptop today and on a verified production appliance for regulated records tomorrow, without re-provisioning.

**Four-tier SLM ladder (claim #40).** Customers move through four product positions — Community (pure API gateway), Tier 1 (local 7B specialist), Tier 2 (vendor-hosted Yo-Yo 32B), Tier 3 (PointSav-LLM continued-pretrained specialist) — as their corpus accumulates and their compute appetite grows. The ladder is designed for breakout: every tier is customer-portable; no lock-in accrues at any rung.

**Reverse-flow substrate (claim #52).** The same Doorman gateway and audit ledger that enforce inbound discipline also enforce outbound commercial flows — data marketplace and ad exchange — as tenant-selectable, opt-in configurations. Monetization configuration is a contract decision, not an architectural rebuild.

## The Eight Cross-Industry Inventions

Beyond the structural claims, the doctrine draws on eight process inventions borrowed from established industries:

**Workspace Passport** (maritime) — every deployment carries a `MANIFEST.md` declaring origin, owner, and current state. **NOTAM** (aviation) — time-sensitive warnings read at every session start. **Recall Procedure** (pharmaceuticals) — defective vendor commits trigger recall notices into every downstream deployment inbox. **Bill of Lading** (shipping) — cross-realm handoffs generate append-only log entries. **Time-Vested Operation** (banking) — destructive operations post to `NEXT.md` with a vesting date; execution is blocked until the date passes. **Apprentice Mode** (aviation/medicine) — new model versions run in shadow mode; graduate after N approved actions. **Integrity Anchor** (notarization) — monthly workspace state hashes posted to Sigstore Rekor public transparency log. **Constitutional Convention** (IETF/constitutional amendment) — doctrine major-version bumps require 30-day public comment in `factory-release-engineering`.

## Workspace Structure

The workspace (`~/Foundry/`) is itself a deployment of the substrate — `vault-privategit-source-1`. Three tiers flow in one direction:

- `vendor/` — engineering source (`pointsav/*`) — GitHub-tracked
- `customer/` — guide catalog (`woodfine/*`) — GitHub-tracked
- `deployments/` — numbered runtime instances — local-only, gitignored

Three session roles operate the workspace: Master (workspace control plane, single at a time), Root (per engineering-repo plane, one per repo), Task (per project-cluster, multiple concurrent). The `.git/index` constraint — one session per index — is the hard race condition that determines this structure.

## Continuous Disclosure Posture

Every artifact written to the workspace — documentation, doctrine sections, commit messages, code comments — is treated as potentially reviewable under continuous-disclosure obligations. Forward-looking statements about future capability, timeline, or customer outcome carry "planned"/"intended"/"may" framing, a stated reasonable basis, cautionary language, and material assumptions. This is not a compliance statement; it is the operational practice that makes compliance a byproduct.[^1][^2]

## See Also

- [[compounding-substrate]] — the Compounding Substrate claim in detail
- [[three-ring-architecture]] — Ring 1, Ring 2, Ring 3 service composition
- [[single-boundary-compute-discipline]] — the Doorman as single boundary
- [[system-substrate-doctrine]] — the capability ledger and two-bottoms claims
- [[slm-stack-architecture]] — the Rust stack that implements the Doorman
- [[yoyo-compute-substrate]] — Tier B cloud GPU burst substrate

## References

[^1]: NI 51-102 Continuous Disclosure Obligations — BCSC
[^2]: OSC Staff Notice 51-721 Forward-Looking Information Disclosure

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.


---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
