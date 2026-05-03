---
title: "service-slm as Totebox Sysadmin"
slug: topic-service-slm-totebox-sysadmin
category: architecture
status: stable
last_edited: 2026-04-30
editor: pointsav-engineering
quality: complete
references:
  - id: 1
    text: "Foundry Doctrine claim #32 — The Apprenticeship Substrate"
  - id: 2
    text: "OLMo 3 — Allen Institute for AI. allenai.org/blog/olmo3"
  - id: 3
    text: "NI 51-102 Continuous Disclosure Obligations — BCSC"
  - id: 4
    text: "OSC Staff Notice 51-721 Forward-Looking Information Disclosure"
---

`service-slm` — the Doorman — is the intended operational sysadmin and support centre for Totebox Archive and Totebox Orchestration deployments. This document scopes what the model needs to know, how that knowledge is captured from real operations, and the three-tier customer-facing product trajectory that results.[^3][^4]

The substrate is already configured to learn. The Doorman is operational. The apprenticeship corpus pipeline captures training signal from every commit across active clusters. What remains is to point the apprenticeship substrate at the ten operational task families that matter most for Totebox operations, register them formally, and let the loop close.

## The ten Totebox operational task families

Surveying operational guide files across active deployments yields a clear taxonomy of what a Totebox sysadmin handles day-to-day:

| Task family | What it covers |
|---|---|
| Node provisioning | Physical boot sequence: power, boot drive, MBA handshake, mount isolated container, Diode Standard, lock terminal |
| Ingress operations | Graph API harvester scheduling, synthesis loop monitoring, spool-daemon watchdog |
| Sovereign data extraction (DARP) | Knowledge-graph and verified-ledger extraction to local; cloud-temp-file destruction verification |
| Cold-storage egress | Quarterly rsync to attached secure drive; integrity verification |
| SLM execution oversight | Reviewing raw AI extractions (drafts) versus human-approved verified-ledger (finalized); advancement decisions |
| Sovereign search operations | Tantivy index maintenance; boolean query diagnosis; DARP extraction by encrypted volume copy |
| Identity and capability operations | Air-gapped tenant credentials; Zero-Touch Parser key management; per-node MBA handshake |
| Adapter injection | Per-tenant private-adapter placement; volume-cap validation; Diode Standard compliance check |
| Audit-trail reconciliation | Cross-checking per-tenant audit ledger against the WORM Immutable Ledger; Sigstore Rekor anchor verification |
| Schema-conforming data import | Glossary-canonical term validation; Archetype mapping; YAML structural-tag grammar conformance |

These ten families cover approximately 95% of the operational scenarios surfaced in existing deployment guides. They become the named task-types for service-slm apprenticeship registration.

## Why service-slm rather than an external API

Four structural properties make these workloads uniquely well-suited to the local Doorman:

**Sovereignty.** Tenant-private corpus stays inside the customer's Totebox. Every task family above touches tenant data. Sending routine sysadmin queries to an external API for processing is a structural sovereignty break that the Doorman architecture prevents by construction.

**Speed.** Tier A local inference (OLMo 3 7B Q4 on the customer's hardware) and Tier B Yo-Yo (OLMo 3.1 32B Think on cloud GPU burst) both respond in seconds. A ten-second-per-step latency on a nine-step provisioning walkthrough is the difference between a usable assistant and a frustrating one.

**Cost shape.** Tier B amortized cost at the planned Yo-Yo substrate price lands near $0.0001 per typical sysadmin request. External API equivalents exceed $0.05 per request once prompts include the tenant context that sysadmin work requires.

**Personalization.** Per-cluster LoRA adapters trained on the customer's own operational patterns — the actual error states they hit, the actual command shapes they prefer, the actual glossaries they use — make service-slm a far better assistant for that customer than a generic model can be. Per-tenant continued pretraining preserving tenant isolation is structurally impossible for shared multi-tenant services.

## Corpus shape — ten new task-types for apprenticeship registration

The apprenticeship corpus already accumulates at `data/training-corpus/apprenticeship/<task-type>/<tenant>/`. Ten new task-types should be registered via signed `task-type-add` events corresponding to the ten operational families above.[^1]

Example registration:

| task_type | Trigger | Input shape | Output shape |
|---|---|---|---|
| `node-provision` | Operator asks SLM to confirm a step or explain a failure | Step number + terminal output + MBA state | Diagnosis + next-step instruction citing the guide |
| `ingress-diagnose` | spool-daemon stall or auth failure | systemd status + last 50 log lines | Root cause + remediation command sequence |
| `audit-row-reconcile` | Audit ledger row missing for a known apprentice diff | brief_id + commit SHA + ledger range | Trace + repair sequence preserving WORM append-only invariant |

Each new task-type starts at `review` stage; promotion to `spot-check` requires ≥ 50 verdicts at ≥ 0.85 accept-rate, consistent with the standard Apprenticeship Substrate thresholds.

## Three-tier customer trajectory

The training pipeline produces a three-tier product trajectory:

**Tier 1 — Single-Totebox SMB customer.** OLMo 3 7B Q4 running locally on the customer's appliance. Doorman handles routine sysadmin queries from the ten task families. Tier C external API access remains for cases the local model defers. Sovereignty: complete.

**Tier 2 — Multi-Totebox customer (planned).** Same substrate plus a subscription to vendor-hosted Tier B Yo-Yo (32B Think) for harder queries. Per-cluster LoRA adapters trained on the customer's own task-type corpus deploy on Tier B. Pricing is intended to be structurally below comparable closed-source offerings. Forward-looking: subject to corpus accumulation rate and compute pricing at time of deployment.[^3][^4]

**Tier 3 — PointSav-LLM specialist product (planned).** Vendor-hosted PointSav-OLMo-N, continued-pretrained on Foundry's full multi-tenant aggregated corpus plus curated public corpus. Multi-tenant API specialist in Totebox Archive operation and the ten task families above. L1 (AI) resolves an intended 80–90% of customer queries autonomously; L2 (human-in-the-loop) handles escalations; each L2 response feeds back as DPO training signal, closing the apprenticeship loop on customer-service work itself. Deployment timeline and pricing are planned targets subject to corpus accumulation and compute availability; material assumptions and cautionary language apply per continuous-disclosure posture.[^3][^4]

## Training pipeline stages

**Stage 1 — Capture (operational).** Every shadow brief lands a corpus tuple automatically on every commit's post-commit hook. No operator action required beyond normal development work.

**Stage 2 — Promote via signed verdict.** A senior identity (Master, Root, or operator) reviews captured tuples and signs verdicts via SSH. Approve, Refine, Reject, or DeferTierC. Refine produces a DPO pair. Sustainable cadence: weekly batch at session end.

**Stage 3 — Per-cluster LoRA training cycle.** When a task-type's corpus crosses 50 verdict-signed tuples, the trainer runs. Initial proof-of-life cycle runs CPU-only on the workspace VM (zero cost); production cycle moves to Tier B Yo-Yo GPU once the compute substrate is operational.

**Stage 4 — Multi-adapter composition at request time.** The Doorman composes up to three adapters per request: `base ⊕ engineering-pointsav ⊕ cluster-<name>` or `base ⊕ apprenticeship-pointsav ⊕ tenant-<name>`. Audit-ledger entry records the composed adapter set per request.

**Stage 5 — Continued pretraining (PointSav-OLMo-N, planned).** Once corpus crosses sufficient token density across all tenants, AI2's published OLMo 3 recipe applies: midtraining, long-context extension, post-training fine-tuning. This is the Tier 3 product and is intended for the v0.5.0 milestone, subject to corpus accumulation.[^2][^3][^4]

## See Also

- [[topic-apprenticeship-substrate]] — the verdict-signed training mechanism
- [[topic-four-tier-slm-substrate]] — the four-tier model routing hierarchy
- [[topic-single-boundary-compute-discipline]] — the Doorman boundary discipline
- [[topic-trajectory-substrate]] — the corpus capture and separation rules

## References

[^1]: Foundry Doctrine claim #32 — The Apprenticeship Substrate
[^2]: OLMo 3 — Allen Institute for AI. allenai.org/blog/olmo3
[^3]: NI 51-102 Continuous Disclosure Obligations — BCSC
[^4]: OSC Staff Notice 51-721 Forward-Looking Information Disclosure

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.
