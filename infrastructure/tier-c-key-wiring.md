---
schema: foundry-doc-v1
title: "Tier C key wiring"
slug: tier-c-key-wiring
category: infrastructure
index_group: fleet-and-edge-deployment
type: topic
content_type: topic
quality: complete
short_description: "The operational procedure for managing external API keys in the Doorman service — where keys live, how they are provisioned, how they rotate, and how a breach is contained."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-24
editor: pointsav-engineering
cites: []
paired_with: tier-c-key-wiring.es.md
---

Tier C of the [[service-slm-operationalization-plan|PointSav compute routing architecture]] routes AI-assisted requests to external language model providers via HTTPS. The [[doorman-protocol|Doorman service]] is the only component in the framework that holds provider API keys. This document describes the operational form of Tier C key management: where keys are stored, how they are provisioned and rotated, how cost and usage are audited, and how a suspected compromise is contained.

The universal principle is that API keys live at the gateway only — never in application code, never in version-controlled files, and never in logs or audit records. This document is the operational counterpart to that principle.

## Where keys live

Provider API keys are held together in a single operator-managed environment file on the gateway host, loaded via one environment-file override applied to the whole Doorman unit — the supported providers' keys all live in that one file, not in separate per-provider drop-ins. Rotating one provider's key means editing that shared file and reloading the service; it isn't isolated from the other providers' configuration the way a true per-provider drop-in would be.

The environment file is owned by root and readable only by the service user running the Doorman. It is not tracked in any version-control repository, not included in any backup that publishes outside the host, and not present anywhere in Git history.

The Doorman binary reads keys from its environment at startup and holds them in process memory. Keys are never written to disk by the Doorman, never echoed in response bodies, and never included in log output at any log level. Audit-ledger entries record the provider name, not any portion of the key.

A future strengthening of this posture, planned for a later milestone, will replace the plaintext environment file with an encrypted file that the Doorman decrypts into its runtime environment using an operator-held decryption key that is never present on the host in plaintext. The current approach is the operational baseline until that milestone lands.

## Provisioning a key

Activating a new provider key requires operator presence for every step that touches the key value itself, following a documented internal runbook rather than an ad hoc process. In outline: the key is obtained from the provider's console, staged only through restricted-permission temporary handling, written into the shared environment file, and the service is reloaded and health-checked to confirm the new configuration took effect. A low-cost test call confirms the key routes correctly and produces the expected audit-ledger entry before the temporary handling artifacts are securely removed. The activation itself is recorded in an internal operational log — provider name, date, and a pointer to the corresponding audit-ledger entry — but the key value never appears in that record or in any commit message.

## Rotation

Quarterly rotation per provider is the default cadence, aligned with calendar quarters. The procedure generates a new key at the provider console while the old key remains active, replaces that provider's key line in the shared environment file, reloads the service, verifies operation, and retains the old key at the provider side for a short overlap window in case rollback is needed. A rotation event marker in the audit ledger delineates pre-rotation and post-rotation usage, supporting post-incident investigation.

Accelerated rotation is appropriate when a compromise is suspected (see the breach response section), when the provider mandates rotation on its own schedule, or when the operator chooses a more frequent cadence for a high-volume deployment.

## Per-provider operational specifics

The Doorman supports three external providers as of the initial deployment: Anthropic Claude reached via the Messages API, Google Gemini reached via the Generative Language API, and OpenAI reached via the Chat Completions API. Each provider has a distinct authentication convention — header-based for Anthropic and OpenAI, URL-parameter-based for Gemini — and each has provider-specific rate-limit semantics that the Doorman handles with exponential backoff and retry capping.

When a provider returns a server error, the Doorman falls back to Tier A local inference rather than returning an error to the caller. The caller receives a response flagged as degraded, and the audit-ledger entry records the fallback. Budget exhaustion is handled differently: a request that would exceed the per-tenant daily budget is rejected immediately rather than silently downgraded to local inference, because returning a budget-exceeded error is preferable to providing a degraded answer the caller did not ask for.

## Audit posture

Every Tier C call produces an audit-ledger entry recording the provider, the model, token counts, computed cost, latency, tenant identifier, call purpose, and success status. Calls are restricted to a fixed allowlist of permitted purposes — editorial and knowledge-graph work, not open-ended use — and any call outside that allowlist is rejected at the Doorman.

A recurring operator review aggregates prior-period usage by provider, flags cost spikes and success-rate anomalies, and verifies that provider-side billing agrees with ledger-side cost totals within a reasonable margin. Persistent divergence between provider billing and the ledger is an investigation trigger, not a tolerance.

## Breach response

A breach is any event that exposes a key value beyond the Doorman boundary: accidental logging, accidental commit to a repository, a panic stack trace that echoes environment variables, inclusion in a message record, or appearance in a transcript used as a reproduction step. The response sequence is fixed and the first step is non-negotiable: revoke the key at the provider console immediately, before cleaning up the source of the leak. Revocation makes the leaked key worthless and bounds any potential misuse window. The remaining steps — removing the compromised key from the shared environment file, provisioning a fresh key through the standard runbook, sweeping the audit ledger for anomalous activity between the leak timestamp and revocation timestamp, and logging the incident — follow in order.

The incident is recorded in an internal operational log, carrying the leak source, the revocation timestamp, audit-ledger sweep findings, and the root cause and corrective action. This recording discipline is part of the continuous-disclosure substrate: material operational events are recorded in signed, date-stamped commits that are suitable for review.

## See also

- [[service-slm-operationalization-plan]] — the broader compute routing architecture that defines the Tier A, B, and C structure
- [[doorman-protocol]] — the Doorman service architecture: routing, authentication, and audit posture
- [[machine-based-auth]] — the machine-based authorization layer that operates alongside key-based Tier C access
