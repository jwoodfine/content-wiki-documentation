---
schema: foundry-doc-v1
title: "Security overview"
slug: security-overview
category: governance
type: topic
quality: complete
short_description: "The platform's security posture: capability-based hardware isolation, the Diode unidirectional command-flow standard, the Doorman AI boundary, the WORM audit ledger, and how each property is enforced by architecture rather than by policy controls that can be misconfigured."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
editor: pointsav-engineering
cites: []
paired_with: security-overview.es.md
---

The PointSav platform enforces security through architecture. Capability-based isolation, unidirectional command flow, a WORM ledger that makes record modification structurally impossible, and a single AI boundary that logs every call to the per-tenant audit ledger — these properties hold because the architecture makes violation impossible, not because a policy prohibits it and an administrator might misconfigure that prohibition.

The Doorman service holds every external API key and logs every AI inference call. No AI request reaches an external model without passing through this boundary, and no boundary call goes unrecorded. An operator who wants to audit every AI interaction reads the ledger; the record exists whether or not the operator intended to log it, because the logging is not optional.

The Diode standard imposes a unidirectional command-flow discipline across the entire fleet. Traffic moves from authority to subject and never the reverse. A node that receives a command cannot initiate a command to the node that sent it. Lateral movement attacks require the routing logic that the Diode removes.

A security officer can verify that AI has not touched the authoritative record without trusting the vendor's claims. The three-ring architecture provides the answer architecturally: Ring 1 and Ring 2 have no import, no dependency, and no runtime call that reaches Ring 3. The code can be inspected; the isolation is in the structure, not the policy.

## Tenant isolation

The platform enforces tenant isolation at three layers:

**Kernel-level at Ring 1.** Each tenant's Ring 1 boundary services run as separate processes with separate storage roots. There is no code path from one tenant's Ring 1 data to another's. The [[totebox-os|ToteboxOS]] enforces this at the kernel level: capability-based security means no component can reach another's resources without holding a cryptographic capability token that was explicitly granted at provisioning time.

**Namespace isolation at Ring 2.** Ring 2 services are multi-tenant via `moduleId`. One process handles requests for all tenants, but each tenant's knowledge graph and search index are isolated behind their `moduleId` namespace at every read and write path. A query for tenant A cannot return records for tenant B.

**Single-boundary AI isolation at Ring 3.** [[service-slm]] is the sole Ring 3 service. Every AI request passes through the Doorman, which sanitises outbound data, routes among three compute tiers, and writes an audit row at the customer's local ledger before any external call is made. No other service in the platform makes external AI calls.

## The Doorman boundary

The Doorman is the single point through which all AI inference flows. It enforces five properties:

**No key lives outside the Doorman.** API keys for external AI vendors are held exclusively at the Doorman. No other process in the platform holds or can request these keys. A breach of any non-Doorman service cannot expose external API keys.

**Every call is logged before it is made.** The Doorman writes an audit row to the customer's local ledger before dispatching the external call. A call that fails at the network layer still has a ledger entry. The external gateway writes a second audit row simultaneously — two-ledger, per-call coverage that does not depend on the success of the call.

**Outbound data is sanitised.** The Doorman inspects every outbound payload before it leaves the customer's network. Structured data subject to the platform's data-classification rules is stripped at this boundary before the request is dispatched.

**Inbound responses are contained.** The response from an external model returns to the Doorman and is not directly exposed to Ring 2 or Ring 1 services. The Doorman routes the response to the requesting application.

**Tier routing is audited.** The customer can see in their local ledger exactly which compute tier handled each request: local (Tier A), GPU burst (Tier B), or external API (Tier C). This tier-level record is the basis for per-token billing attribution and for regulatory evidence of data localisation.

## The WORM ledger

Every Ring 1 service writes to a Write-Once-Read-Many ledger. The ledger has no delete operation and no overwrite operation — these functions do not exist in the storage engine. Modification is structurally impossible rather than policy-prohibited.

The ledger is tile-based and hash-chained: each tile contains the hash of the previous tile. Any modification to any tile breaks the hash chain and is detectable by any verifier without access to the platform's own systems. The `[[fs-anchor-emitter]]` service generates signed checkpoints of the ledger at hourly cadence and prepares them for external anchoring to the Sigstore Rekor public transparency log on a monthly schedule — independent, external proof-of-state that does not depend on the vendor's continued operation.

The WORM ledger structure satisfies SEC Rule 17a-4(f), eIDAS qualified electronic records preservation, and SOC 2 — by structural guarantee, not by policy attestation that can be amended.

## The Diode standard

The Diode standard is the foundational network security topology of the PointSav fleet. Commands flow from authority (os-orchestration, os-console) to subject (Totebox archives, services) and never the reverse.

A Totebox archive that receives a command from os-console cannot initiate a command back to os-console. The routing logic that would allow this does not exist in the communication stack. This removes the lateral movement attack surface: an attacker who compromises a Totebox archive cannot use that position to issue commands to the orchestration layer or to peer archives.

Commands transmit as 16-byte binary packets across the WireGuard mesh. The compact binary format eliminates the command-injection attack surface that text-based command protocols carry.

## Capability-based access control

The platform uses capability-based security rather than access-control lists or role-based access control. A software component can communicate with another only if it holds a cryptographic capability token explicitly granted at provisioning time. There is no ambient authority — a component that has not been explicitly granted a capability cannot acquire it by any runtime mechanism.

A compromised component cannot escalate its own privileges. It can do only what its capability set allows, and its capability set was fixed at provisioning. A Ring 1 service that is compromised cannot reach Ring 2 resources it was not provisioned to access.

[[machine-based-auth]] extends this model to operator authentication: the cryptographic pairing between an operator's hardware device and the orchestration node is the permission. Username and password structures are not used for platform access.

## Supply chain security

Code reaches production deployments through a five-stage supply chain with a double-blind air-gap. Contributors work in staging environments that have no access to production credentials or production data. The double-blind design means a contributor cannot see production data, and production systems cannot be reached from a contributor's working environment. The five-stage supply chain is documented at [[five-stage-supply-chain]].

## What a security audit covers

A security audit of the platform can verify the following directly from the ledger and the codebase:

| Audit question | Source of evidence |
|---|---|
| Did AI write to the authoritative record? | Ring 3 codebase: no write path to Ring 1/2 storage exists |
| Which AI calls were made and when? | Per-tenant audit ledger: every Doorman call logged |
| Has any ledger record been modified? | Hash chain: break is detectable without trusting the platform |
| What entered Ring 1 and when? | Ring 1 WORM ledger: every ingest event recorded |
| What left the platform and when? | [[service-egress|service-egress]] audit entries in the ledger |

What the audit cannot find — because it does not exist — is an AI write path to Ring 1 or Ring 2 storage. The architecture has no such path.

## See also

- [[three-ring-architecture]] — the three-ring model and why AI is structurally optional
- [[diode-standard]] — the unidirectional command-flow discipline in full
- [[doorman-protocol]] — the Doorman AI boundary service and its routing logic
- [[capability-based-security]] — the capability-based isolation model at the OS layer
- [[worm-ledger-design]] — the WORM ledger structure and its compliance properties
- [[machine-based-auth]] — machine-based authorization for operator identity
- [[architecture-decisions]] — the twelve binding decisions, including ADR-07 (no AI on structured data), ADR-10 (F12 mandatory checkpoint), ADR-19 (no automated AI publishing)
- [[five-stage-supply-chain]] — the double-blind supply chain
- [[procurement-overview]] — procurement terms and commercial structure for regulated buyers
