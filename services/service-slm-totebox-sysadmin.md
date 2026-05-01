---
schema: foundry-doc-v1
title: "service-slm as Totebox Sysadmin and Support Centre"
slug: service-slm-totebox-sysadmin
category: services
type: topic
quality: core
short_description: "How service-slm becomes the operational assistant and support centre for Totebox Archive and Totebox Orchestration deployments — the training strategy, the ten operational task families, and the four-stage pipeline from corpus capture to per-tenant LoRA adapters."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
  - olmo3-allenai
  - federated-lora-2502-05087
  - lorax-predibase
  - s-lora-2024
  - constitutional-ai-2212-08073
  - vllm-multi-lora
  - ni-51-102
  - osc-sn-51-721
paired_with: service-slm-totebox-sysadmin.es.md
---

`service-slm` — the Compounding Doorman at Ring 3 of the platform — is designed to become the operational assistant and support centre for Totebox Archive and Totebox Orchestration deployments. This article describes the strategy: the operational task families a sysadmin handles, why service-slm is structurally suited to handle them, the corpus shape required to train it, and the four stages that take a deployment from initial capture to a per-tenant LoRA adapter running in production.

The premise is grounded in present state, not projection. The Doorman is operational. The apprenticeship corpus pipeline is wired. The substrate is configured to learn. What remains is to direct it at the operational work that matters most.

## The ten Totebox operational task families

A survey of the GUIDE files across the three Totebox deployment clusters — personnel, corporate, and property — yields a clear taxonomy of the day-to-day scenarios a Totebox sysadmin encounters. These ten families cover roughly 95 percent of the operational scenarios present in the existing guides. They define what service-slm needs to learn.

| Task family | Example surfaces | Common error states |
|---|---|---|
| **Node provisioning** | 9-step physical sequence: power, boot drive, MBA handshake, isolated container mount, Diode Standard, terminal lock | Boot-drive cryptographic mismatch; MBA handshake failure; Diode reverse-flow violation |
| **Ingress operations** | MSFT Graph harvester, First Derivative emission, spool-daemon watchdog | Auth tokens expired; Outlook target folders missing; spool-daemon not monitoring `maildir/new/` |
| **Sovereign data extraction (DARP)** | `tool-extract-content.sh`, `tool-extract-people.sh` | Cloud-side temp file not destroyed; SSH credentials missing; partial flatten step |
| **Cold-storage egress** | Quarterly rsync to attached secure drive; JSON-to-CSV ledger extraction | Drive not mounted; rsync permission denied; partial transfer; integrity mismatch |
| **SLM execution review** | Inspect `knowledge-graph/` drafts vs `verified-ledger/` finalised records | Drafts not advancing; AI extraction mismatch with Domain Glossaries |
| **Sovereign search operations** | Tantivy index, boolean query at command terminal, DARP extraction by encrypted volume | Index not regenerating; query parser rejecting valid boolean; index drift |
| **Identity and capability operations** | Tenant ID, Client ID, Secret Value — Zero-Touch Parser locks keys at 600 permissions; per-node MBA handshake | Keys in Git history; permission drift on `.env`; MBA registration desync |
| **Adapter injection validation** | Drop adapter into `private-adapters/`; volume cap at 75–100 ops/cycle; read-only service-people query | Adapter writing to local store; volume cap exceeded; service-people write attempt |
| **Audit-trail reconciliation** | Cross-check per-tenant audit ledger against WORM Immutable Ledger; verify signed verdict events; resolve anchor timestamps | Audit row missing for an apprentice diff; verdict signature fails verification; anchor lag |
| **Schema-conforming data import** | Imports following canonical Glossary CSV; Archetype + Chart-of-Accounts + Domain mapping at ingress | Term not in canonical Term_EN; Domain mismatch; YAML structural-tag failure |

## Why service-slm rather than an external API for these tasks

Four structural properties make these workloads suited to service-slm over third-party inference APIs:

**Sovereignty.** Every task family above touches tenant data — personnel records, corporate ledgers, real-property archives, audit trails. Routing these to an external service for routine sysadmin operations breaks the data-sovereignty guarantee at Doctrine §IV.b. service-slm running locally inside the customer's Doorman boundary is the only architecture where the data never leaves the customer-controlled substrate.

**Latency.** Sysadmin work is high-frequency and low-latency in character. Diagnosing a stalled spool-daemon, reconciling an audit-row mismatch, or walking through a 9-step provisioning sequence requires a responsive assistant. Tier B (OLMo 3.1 32B Think on A100 80GB) delivers approximately 100–150 tokens per second at modest batch sizes [olmo3-allenai]. A Tier C external-API round-trip adds 5–15 seconds per call including network and provider queuing. On a multi-step provisioning walkthrough, that latency difference is material.

**Cost at volume.** The planned amortised cost of Tier B on a preemptible A100 with idle-shutdown lands near $0.0001 per typical sysadmin request once the instance is shared across multiple customer deployments. Tier C equivalents at full prompt context exceed $0.05 per request. At sustained operational volumes — thousands of sysadmin queries per day across an active fleet — the differential compounds. [ni-51-102] [osc-sn-51-721] *Forward-looking cost figures reflect planned substrate economics; actual costs may differ based on model, provider pricing, and prompt size.*

**Personalisation.** Per-tenant LoRA adapters trained on each customer's specific operational patterns — the actual error states they encounter, the command shapes they prefer, the glossary terms they use — make service-slm a more accurate assistant for that customer than a generic inference service can be at any scale. The structural basis for this is that the customer's data and interaction history stay within the customer's substrate, available for training, without any sharing or external transmission.

**Continuous availability.** Tier A (local CPU model) operates during Tier B cold starts, spot preemption windows, or network-isolated periods. The Brief Queue Substrate keeps corpus capture continuous across all three failure modes. The training signal is never lost.

## The corpus shape: ten new task-type registrations

The apprenticeship corpus accumulates at `data/training-corpus/apprenticeship/<task-type>/<tenant>/`. For Totebox sysadmin work, ten new task-types should be registered in the promotion ledger via signed `task-type-add` events per `conventions/apprenticeship-substrate.md` §6. The proposed registrations correspond directly to the ten task families above:

| task_type | Trigger | Input shape | Output shape | Verdict criteria |
|---|---|---|---|---|
| `node-provision` | Operator runs provisioning and asks for step confirmation or failure diagnosis | Step number + terminal output + MBA state | Diagnosis + next-step instruction citing the guide | Step matches authoritative guide; no fabricated commands |
| `ingress-diagnose` | Spool-daemon stall or auth failure | systemd status + last 50 log lines + credentials presence (redacted) | Root cause + remediation command sequence | Cause matches operator-confirmed root cause; commands syntactically valid |
| `darp-extract` | `tool-extract-*.sh` failure or partial result | Script invocation + exit code + cloud-temp-file post-state | Cleanup commands + retry sequence | Zero cloud-temp residue after cleanup; retry preserves DARP guarantees |
| `cold-storage-sync` | rsync integrity mismatch | rsync invocation + output + drive UUID | Verification + repair sequence | Verification matches checksum manifest; no data loss |
| `slm-execution-review` | `knowledge-graph/` vs `verified-ledger/` divergence | Draft entity + verified entity + Domain Glossary | Diff explanation + advancement recommendation | Recommendation aligns with canonical Term_EN |
| `sovereign-search-debug` | Tantivy index drift or parser rejection | Boolean query + index state + last Forge run timestamp | Diagnosis + index regeneration command | Regeneration succeeds without losing prior index |
| `identity-cap-handshake` | MBA handshake failure | Hardware fingerprint + MBA state + per-node `.env` | Step-by-step recovery preserving Zero-Touch Parser invariants | Recovery preserves MBA registration; no key leakage; 600 permissions maintained |
| `adapter-injection-validate` | Operator drops new private adapter | Adapter source + placement + volume-cap declaration | Pass or fail with specific structural-rule citations | Adapter passes Diode Standard; volume cap declared; no service-people writes |
| `audit-row-reconcile` | Audit ledger row missing for a known brief | brief_id + commit SHA + ledger range | Trace locating the missing row + repair sequence | Repair preserves WORM append-only invariant |
| `schema-import-validate` | CSV or JSON import fails the deterministic parser | Source row + Glossary Term_EN + expected Archetype | Reformatted row + structural-tag YAML | Term_EN is canonical; Archetype correct; YAML passes lexical grammar |

Each new task-type starts at `review` stage. Promotion to `spot-check` requires at least 50 verdicts at a rate of 0.85 or higher.

## The four-stage training pipeline

**Stage 1 — Capture.** Every shadow brief lands a corpus tuple at `stage_at_capture: review`, `verdict: null`. Capture is automatic on every commit's post-commit hook via the Brief Queue Substrate. No operator action; no additional compute. This stage is operational.

**Stage 2 — Promote via signed verdict.** A senior identity — Master, Root, or operator at the chat surface — reviews captured tuples and signs verdicts using `ssh-keygen -Y sign -n apprenticeship-verdict-v1`. Verdict outcomes: Approve, Refine (producing a DPO pair), Reject, or Defer to Tier C. A weekly batch at session end is the sustainable cadence; per-commit signing does not scale. Signing is local cryptographic operation: zero compute cost. Verification uses the `identity/allowed_signers` file.

**Stage 3 — Per-cluster LoRA training cycle.** When a task-type's corpus crosses 50 verdict-signed tuples, the trainer is triggered. Initial cycle runs CPU-only on the workspace VM (zero cost; informs Phase 1 scope). Production cycles move to Tier B once the Yo-Yo GPU instance is provisioned (planned cost: $1–3 per training run, hours of wall time) [olmo3-allenai]. LoRA rank 16–32, targeting attention and feed-forward layers. The trained adapter lands at `data/adapters/<task-type>-<cluster>-<tenant>-v0.1.lora` and is SSH-signed before deployment. *Training timeline and cost projections are planned targets, subject to corpus accumulation rate, hardware availability, and operator review. [ni-51-102] [osc-sn-51-721]*

**Stage 4 — Multi-adapter composition at request time.** The Doorman composes up to three adapters per request: `base ⊕ engineering-pointsav ⊕ cluster-<name>` or `base ⊕ apprenticeship-pointsav ⊕ tenant-<name>`. Tier B vLLM Multi-LoRA serves the composition [vllm-multi-lora] [s-lora-2024] [lorax-predibase]. Every request's audit-ledger entry records the composed adapter set, making the influence of each adapter traceable.

Stage 5 — continued pretraining into a PointSav-OLMo base — is a long-horizon trajectory planned for workspace v0.5.0, contingent on corpus accumulation crossing 50–100B tokens across all tenants. This is an intended capability; actual timeline depends on corpus growth rate and operational conditions [olmo3-allenai]. [ni-51-102] [osc-sn-51-721]

## Customer product tiers

The service-slm-as-sysadmin capability is available across three customer tiers, each with a distinct deployment and cost shape:

**Tier 1 — Single-Totebox SMB.** OLMo 3 7B Q4 running on the customer's appliance (8–12 GB consumer GPU or 8 GB CPU laptop). The Doorman handles routine sysadmin queries from the ten task families. Tier C external API access remains for cases the local model defers. Sovereignty: complete — no data flow to vendor infrastructure for routine operations.

**Tier 2 — Multi-Totebox customer.** Tier 1 plus access to vendor-hosted Tier B (OLMo 3.1 32B Think) for harder queries. Per-tenant LoRA adapters trained on the customer's own corpus deploy on Tier B. Pricing: per-token at PointSav rates, planned to be structurally below the $95,000–$590,000 annual floors that gate comparable closed-source SMB offerings. *Planned pricing is intended to be structurally favourable relative to those alternatives; actual pricing is not yet set and is subject to operator decision before any commercial offer.* [ni-51-102] [osc-sn-51-721]

**Tier 3 — PointSav-LLM specialist product.** A vendor-hosted model trained on Foundry's aggregated multi-tenant corpus plus curated public corpus; a specialist in Totebox Archive operation, PointSav conventions, and the ten task families. L1 AI resolution of a planned 80–90 percent of customer queries autonomously; L2 human-in-the-loop escalation; L3 engineering for rare complex cases. Each L2 response feeds back as DPO training signal. *Tier 3 deployment timeline is planned for v0.5.0 (Q1 2027 per current roadmap); actual timing is subject to corpus accumulation rate and operator decision. [ni-51-102] [osc-sn-51-721]*

## See Also

- [[service-slm]] — the service that implements this capability; Ring 3 Doorman specification
- [[compounding-doorman]] — the operational pattern the Doorman implements; why it compounds
- [[apprenticeship-substrate]] — the corpus capture and verdict-signing pipeline that feeds Stage 1 and Stage 2
- [[brief-queue-substrate]] — the durable queue that keeps corpus capture continuous across compute-tier transitions

## References

1. OLMo 3 tech report, AI2. Token throughput and fine-tuning recipe. [olmo3-allenai]
2. vLLM Multi-LoRA documentation — serving multiple LoRA adapters per request. [vllm-multi-lora]
3. S-LoRA — scalable LoRA serving reference. [s-lora-2024]
4. LoRAX — multi-LoRA serving infrastructure (Predibase). [lorax-predibase]
5. Federated LoRA framework. [federated-lora-2502-05087]
6. `conventions/apprenticeship-substrate.md` — brief/attempt/verdict format; promotion ledger; per-task-type stage transitions.
7. `conventions/compounding-substrate.md` — five structural properties; multi-tier compute routing.
8. NI 51-102, Continuous Disclosure Obligations (BCSC). [ni-51-102]
9. OSC Staff Notice 51-721, Forward-Looking Information Disclosure. [osc-sn-51-721]

---

## Provenance

Source material: workspace-root draft `topic-service-slm-as-totebox-sysadmin.md` (authored 2026-04-29 at workspace v0.1.80). Background corpus: ten GUIDE files surveyed in cluster-totebox-personnel for operational ground truth; conventions `apprenticeship-substrate.md` and `compounding-substrate.md`; trainer-scoping document (commit `562baa0`) for engineering-side alignment. Refinement disciplines applied: no body H1; structural-positioning discipline (vendor-by-name contrast removed; structural market-gap framing retained); BCSC forward-looking adapter (cost projections, Tier 2 pricing, Tier 3 timeline, and Phase 3 training cycle all labelled with planned/intended/may framing per ni-51-102 / osc-sn-51-721); banned-vocabulary pass (no substitutions required); Open Questions section from source (§7) omitted from published TOPIC — those are internal research items, not public doctrine; Provenance footer BCSC-scrubbed.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
