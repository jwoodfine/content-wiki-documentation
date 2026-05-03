---
schema: foundry-doc-v1
title: "Tier C Key Wiring"
slug: tier-c-key-wiring
category: reference
type: topic
quality: published
short_description: The operational procedure for managing external API keys in the Doorman service — where keys live, how they are provisioned, how they rotate, and how a breach is contained.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: tier-c-key-wiring.es.md
---

Tier C of the PointSav compute routing architecture routes AI-assisted requests to external language model providers via HTTPS. The Doorman service is the only component in the framework that holds provider API keys. This document describes the operational form of Tier C key management: where keys are stored, how they are provisioned and rotated, how cost and usage are audited, and how a suspected compromise is contained.

The universal principle is that API keys live at the gateway only — never in application code, never in version-controlled files, and never in logs or audit records. This document is the operational counterpart to that principle.

## Where keys live

Provider API keys are held in systemd unit drop-in files on the workspace virtual machine. The drop-in path follows the standard systemd pattern for extending a service unit without modifying the unit file itself. Each provider may have its own drop-in file, which makes per-provider rotation atomic: rotating the key for one provider does not require touching any other provider's configuration.

Drop-in files are owned by root and readable by the service user running the Doorman. They are not tracked in any version-control repository, not included in any backup that publishes outside the virtual machine, and not present anywhere in the Git history. The `.gitignore` at the workspace root does not need to mention them because they live outside the repository entirely.

The Doorman binary reads keys from its environment at startup and holds them in process memory. Keys are never written to disk by the Doorman, never echoed in response bodies, and never included in log output at any log level. Audit-ledger entries record the provider name, not any portion of the key.

A future strengthening of this posture, planned for a later milestone, will replace the plaintext drop-in with a sops-encrypted file that the Doorman decrypts into its runtime environment using an operator-held decryption key that is never present on the virtual machine in plaintext. The current systemd-tier approach is the operational baseline until that milestone lands.

## Provisioning a key

Activating a new provider key requires operator presence for the steps that touch the key value, and proceeds through an eight-step sequence. The operator obtains the key from the provider's console and copies it to a temporary file on the virtual machine. The temporary file is created with restricted permissions before the key value is written to it. The Doorman's systemd drop-in is then written using the key from the temporary file, the service is reloaded, and the health endpoint is queried to confirm the service has picked up the new configuration. A low-cost test call verifies that the key routes correctly and that an audit-ledger entry is produced with the expected fields. The operator then removes the temporary file using a secure deletion tool. The final step is a workspace changelog entry recording the activation event: provider name, date, and the reference to the first audit-ledger entry. The key value does not appear in the changelog entry or in any commit message.

## Rotation

Quarterly rotation per provider is the default cadence, aligned with calendar quarters. The procedure generates a new key at the provider console while the old key remains active, replaces the drop-in with the new key, reloads the service, verifies operation, and retains the old key at the provider side for a forty-eight-hour window in case rollback is needed. A rotation event marker in the audit ledger delineates pre-rotation and post-rotation usage, supporting post-incident investigation.

Accelerated rotation is appropriate when a compromise is suspected (see the breach response section), when the provider mandates rotation on its own schedule, or when the operator chooses a more frequent cadence for a high-volume deployment.

## Per-provider operational specifics

The Doorman supports three external providers as of the convention's ratification date: Anthropic Claude reached via the Messages API, Google Gemini reached via the Generative Language API, and OpenAI reached via the Chat Completions API. Each provider has a distinct authentication convention — header-based for Anthropic and OpenAI, URL-parameter-based for Gemini — and each has provider-specific rate-limit semantics that the Doorman handles with exponential backoff and retry capping.

When a provider returns a server error, the Doorman falls back to Tier A local inference rather than returning an error to the caller. The caller receives a response flagged as degraded, and the audit-ledger entry records the fallback. Budget exhaustion is handled differently: a request that would exceed the per-tenant daily budget is rejected immediately rather than silently downgraded to local inference, because returning a budget-exceeded error is preferable to providing a degraded answer the caller did not ask for.

## Audit posture

Every Tier C call produces an audit-ledger entry recording: provider name, model name, input and output token counts, computed USD cost, end-to-end latency, tenant identifier, call purpose, and success status. The four permitted call purposes are editorial refinement, citation grounding, entity disambiguation, and initial knowledge graph construction. Calls for purposes outside this allowlist are rejected at the Doorman.

Monthly review by the workspace Master-layer session aggregates prior-month usage by provider, flags cost spikes and success-rate anomalies, and verifies that provider-side billing agrees with ledger-side USD totals within a reasonable margin. Persistent divergence between provider billing and the ledger is an investigation trigger, not a tolerance.

## Breach response

A breach is any event that exposes a key value beyond the Doorman boundary: accidental logging, accidental commit to a repository, a panic stack trace that echoes environment variables, inclusion in an inbox or outbox message, or appearance in a chat transcript used as a reproduction step. The response sequence is fixed and the first step is non-negotiable: revoke the key at the provider console immediately, before cleaning up the source of the leak. Revocation makes the leaked key worthless and bounds any potential misuse window. The remaining steps — removing the drop-in, provisioning a fresh key through the standard eight-step runbook, sweeping the audit ledger for anomalous activity between the leak timestamp and revocation timestamp, and logging the incident — follow in order.

The incident log entry in the workspace cleanup log carries the leak source, the revocation timestamp, audit-ledger sweep findings, and the root cause and corrective action. This entry is part of the continuous-disclosure substrate: material operational events are recorded in signed, date-stamped commits that are suitable for review.

## See also

- [[service-slm-operationalization-plan]] — The broader compute routing architecture that defines the Tier A, B, and C structure.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
