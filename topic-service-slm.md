---
schema: foundry-doc-v1
title: "service-slm: Linguistic Air-Lock"
slug: topic-service-slm
category: services
type: topic
quality: complete
short_description: "service-slm is the Doorman service — the single network boundary that holds API keys, routes AI inference across three compute tiers, and writes an immutable per-tenant audit record of every external call."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: topic-service-slm.es.md
---

# service-slm: Linguistic Air-Lock

> service-slm is the Doorman service — the single network boundary that holds API keys, routes AI inference across three compute tiers, and writes an immutable per-tenant audit record of every external call.

**service-slm**, also called the Doorman, is the Ring 3 optional-intelligence boundary in the PointSav three-ring architecture. It is the only service that holds API keys for external AI providers. Every AI inference request from any other service routes through the Doorman, which selects among three compute tiers — Tier A local OLMo on the workspace VM, Tier B Yo-Yo GPU burst on multi-cloud, and Tier C external API calls to Anthropic, Google, or OpenAI — based on request shape and tenant budget caps. The Doorman enforces sanitise-outbound and rehydrate-inbound discipline so that customer-identifying details do not reach external providers in raw form. It writes a signed audit entry to the per-tenant ledger on every call, whether internal or external.

## Overview

The Doorman acts as the air-lock for unstructured text entering the knowledge pipeline. Raw text arriving from Ring 1 services — emails, PDFs, form submissions — passes through service-slm before any structured facts are written to the knowledge graph. The service applies a Small Language Model to extract verifiable facts, formats them as clean Markdown, and closes the AI processing window before data continues downstream to Ring 2. This containment is the implementation of SYS-ADR-07: structured data never routes through AI.

## Ring and Role

service-slm occupies **Ring 3 — Optional Intelligence** in the three-ring compounding-substrate architecture. Ring 3 is structurally optional: Ring 1 boundary ingest and Ring 2 knowledge and processing operate without it. When Ring 3 is active, the Doorman mediates all AI calls on behalf of any ring, applying per-tenant configuration and routing policy.

The three compute tiers the Doorman routes across:

| Tier | Compute | When used |
|---|---|---|
| Tier A — Local | OLMo 3 7B Q4 on workspace VM (CPU) | High-volume, low-latency, budget-sensitive requests |
| Tier B — Yo-Yo | OLMo 3.1 32B Think on multi-cloud GPU burst (GCP Cloud Run / RunPod / Modal) | Requests that require larger model capacity |
| Tier C — External API | Anthropic Claude / Google Gemini / OpenAI | Narrow precision tasks: citation grounding, initial graph build |

Customers do not choose the tier. Request shape and budget caps determine routing automatically.

## Architecture

The Doorman enforces three invariants at every call boundary:

1. **Key custody.** No other service holds provider API keys. The Doorman is the exclusive key holder. A compromise of any Ring 1 or Ring 2 service does not expose provider keys.
2. **Audit logging.** Every call — including Tier A local calls — writes a signed record to the per-tenant audit ledger at `~/Foundry/data/audit-ledger/<tenant>/<YYYY-MM>.jsonl`. The record captures the request shape, tier selected, token count, and response hash.
3. **Sanitise-outbound / rehydrate-inbound.** Before any request leaves the workspace, the Doorman strips customer-identifying details per the per-tenant sanitisation policy. The response is rehydrated with the stripped context before returning to the caller.

The service listens on `127.0.0.1:9080` and speaks an OpenAI-compatible HTTP API, allowing any Ring 2 service to address it without bespoke integration.

## Configuration

The Doorman is deployed as a systemd unit (`infrastructure/local-doorman/`) on the workspace VM. Key configuration fields:

- Per-tenant budget caps (monthly token limits per tier)
- Sanitisation policy (field list stripped before outbound calls)
- Routing thresholds (conditions under which a request escalates from Tier A to Tier B or C)
- Audit ledger path and rotation schedule

See `infrastructure/local-doorman/` for the live systemd unit and `conventions/apprenticeship-substrate.md` for the routing-inversion (apprenticeship) configuration that runs on top of this service.

## See Also

- [[topic-service-extraction]]
- [[topic-service-search]]
- [[topic-apprenticeship-substrate]]
- [[topic-language-protocol-substrate]]
- [[topic-trajectory-substrate]]

## References

- DOCTRINE.md §XI — Three-ring architecture and three-tier compute routing
- `conventions/apprenticeship-substrate.md` — routing inversion and verdict-signed training
- `infrastructure/local-doorman/` — systemd unit (live since workspace v0.1.13)
- SYS-ADR-07 — structured data never routes through AI

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.