---
schema: foundry-doc-v1
title: "Pairing as permission"
slug: pairing-as-permission
category: patterns
type: topic
quality: complete
short_description: "PairingAsPermission is the Object Capability access-control model used in Totebox Orchestration: a cryptographic pairing between two nodes is the permission, and the absence of a pairing makes the connection structurally impossible — not access-denied, but no pathway."
status: active
bcsc_class: no-disclosure-implication
last_edited: 2026-05-15
editor: pointsav-engineering
cites: []
references:
 - id: 1
 text: "Miller, M. S. et al. 'Capability Myths Demolished.' SRL2003-02, Johns Hopkins University, 2003."
 url: "https://srl.cs.jhu.edu/pubs/SRL2003-02.pdf"
 - id: 2
 text: "Google. 'Fuchsia Component Framework: Capabilities overview.' Fuchsia.dev, 2024."
 url: "https://fuchsia.dev/fuchsia-src/concepts/components/v2/capabilities"
 - id: 3
 text: "seL4 Project. 'seL4: Formally Verified Microkernel.' The seL4 Foundation, 2024."
 url: "https://sel4.systems/"
paired_with: pairing-as-permission.es.md
---

PairingAsPermission is the access-control model used in Totebox Orchestration: a cryptographic pairing between two nodes is the permission, and the absence of a pairing makes the connection structurally impossible — not access-denied, but no pathway. There is no central access-control list, no permission lookup at request time, and no role table. The model is the formally proven Object Capability pattern, deployed in production at Fuchsia OS, seL4, and WireGuard. PairingAsPermission is canonical in the workspace; synonyms RBAC, ACL, and PermissionSystem are explicitly rejected.

This article describes the principle, the topology in Totebox Orchestration, the engineering risks, and the production reference implementations.

## The core principle

In most access-control systems, a request arrives, the system looks up whether the requester has permission, and either allows or rejects the request. The lookup requires a central authority: a database, a role-policy store, a permission table.

PairingAsPermission eliminates the lookup. Two nodes communicate only if a cryptographic pairing has been established between them. If no pairing exists, no connection exists and no request is made. The question "does this node have permission to reach that node?" has a structural answer: check whether a pairing exists. If not, no pathway exists to ask in the first place.

This is the Object Capability Model — a formally proven security pattern first described by Mark S. Miller in *Capability Myths Demolished* (2003). [^1] The central axiom: **connectivity begets connectivity.** Object A can send a message to B only if A holds a reference to B. The reference is the capability. Without the reference, the connection is structurally impossible — not access-denied, but no pathway.

## The topology in Totebox Orchestration

The Totebox Orchestration topology is:

- **Command** (the os-orchestration hub) is paired to: every Totebox Archive, both os-mediakit nodes, and both os-privategit nodes. The Command's pairing list is the de-facto topology map.
- **Per-project os-orchestration** instances are paired to: their own Totebox Archives only. A `project-bim` orchestration cannot reach `project-editorial` — no pairing exists.
- **Cross-project coordination** flows through the Command: `project-bim` sends a message to the Command; the Command, paired to both, fetches data or routes the request. No direct lateral connection is created between per-project orchestrations.

The permission map is the architecture diagram. There is no separate access-control document — the live pairing topology is the authoritative record.

## No central registry

There is no central registry recording who is paired to whom. This is deliberate.

The pairing state is distributed: it exists between the nodes themselves. Each node holds the public keys of its paired peers. The Command maintains `pairings.yaml` — a record of its active connections (endpoint, public key, module identifier, pairing date) — but this is the Command's operational record, not a central authority. If the Command loses its pairing list, the pairings can be re-established because each peer still holds the Command's public key and the Command still holds each peer's public key. The truth is distributed.

This mirrors Bitcoin's ownership model: there is no central bank recording who owns which coins. The ownership state is the blockchain — distributed, verifiable, requiring no authority. In PairingAsPermission, the pairing state is the topology. A new Totebox Archive declares itself via its `MANIFEST.md` (instance identity plus public key); the Command adds it to its active connections. The connection is the authorisation. No external authority approves or records it.

The design enables true distributed deployment: a Totebox Archive can reside on any cloud provider, any data centre, or a minimal compute node. The Command needs only the archive's endpoint and public key to establish a pairing.

## Why this is stronger than role tables

Role-based and access-list systems share a structural vulnerability: the **confused deputy problem**. A trusted intermediary — a process holding elevated permissions — can be tricked into performing an action on behalf of a less-trusted caller. The intermediary uses its own permissions to do something the caller could not do directly. The vulnerability is structural; it is present in any system where authority is looked up from a table at request time.

In the Object Capability Model, this vulnerability is an architectural invariant. A holder cannot use what it was never given a reference to. A per-project orchestration cannot instruct the Command to act on its behalf for a cross-project operation unless the per-project orchestration already holds the cross-project capability — which it does not. The Command validates per-caller scope on every request before acting. The validation is not an optional security layer; it is the definition of what the Command does.

## Production implementations

This is not a theoretical model. It is deployed at scale in production systems.

**Fuchsia OS** (Google) implements PairingAsPermission at the operating-system level. Every component must have capabilities explicitly routed to it through the component topology. A component that has not been given a capability route is structurally unreachable from the resource — not access-denied, but no pathway. Fuchsia runs on every Google Nest Hub model. [^2]

**seL4 microkernel** has a machine-checked formal proof of capability confinement: a process cannot access a resource it was not explicitly given a capability for. The proof covers integrity (data cannot be modified without authority) and authority confinement (authority cannot exceed what was delegated). seL4 is the gold standard for formally verified security models. [^3]

**WireGuard** implements the same pattern at the network layer. The `AllowedIPs` table is the capability table. A node with no entry for a destination cannot send packets to it. Access control is structural to the routing, not a check at transmission time.

## Three engineering risks and their defences

**Risk 1 — Confused deputy at the Command (high)**
A per-project orchestration sends the Command a message asking it to perform a cross-project operation. If the Command relays without validating the requester's scope, the requester has executed a capability it does not hold, using the Command as deputy.

Defence: the Command validates per-caller scope on every request. The planned `app-orchestration-command` implementation includes this check as the first operation in request handling. It is not optional.

**Risk 2 — Command as availability single point of failure (medium)**
If the Command is unavailable, cross-archive coordination is blocked.

Defence: per-project archives operate fully without the Command — they serve local resources and queue cross-archive requests for retry. No hard failure. Active-passive Command redundancy is a planned later-phase addition.

**Risk 3 — Multi-tenancy on shared physical nodes (medium)**
When multiple logical projects share a single Totebox Archive node, the Command holds capabilities for multiple tenants. If the Command uses the wrong capability token for a request, one tenant's data is accessible under another tenant's scope.

Defence: capability attenuation via separate module identifiers. The Command holds distinct `X-Module-ID` tokens per tenant. The shared archive enforces per-identifier partitions. The `service-slm` access-control gateway already implements this pattern — the Command must pass the correct module identifier for the requesting archive on every call, never its own.

## Implementation

The current implementation uses `system-mba-shim` — a transitional layer behind which conventional OAuth2 authentication sits. The `system-mba-shim` interface is the clean boundary: when the full PairingAsPermission cryptographic model (certificate-based peer-to-peer key exchange) replaces the OAuth2 layer, no calling code changes. The interface stays constant; the implementation behind it is upgraded in place.

The Six Orchestration Contracts include `pairing_attestation` as `SYS-CONTRACTS-01`, hardcoded into the operating-system kernel. It is not configurable.

## The Trustworthy System

PairingAsPermission is one layer of the Trustworthy System pattern: the architecture's attestable trustworthiness compounds over time. Every pairing event is an immutable ledger entry — the history of who was connected to what is append-only. Trustworthy System Attestation produces quarterly signed reports that extend the attestation chain. Apex permissions are co-signed. The pairing topology at any point in time is auditable from the Command's `pairings.yaml` plus the distributed `MANIFEST.md` files held by every paired peer.

Pairing is the permission. Topology is the audit.

## See also

- [[totebox-orchestration-development]]
- [[doorman-protocol]]
- [[compounding-substrate]]
- [[three-ring-architecture]]

