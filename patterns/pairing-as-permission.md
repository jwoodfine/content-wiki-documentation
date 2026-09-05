---
schema: foundry-doc-v1
title: "Pairing as permission"
slug: pairing-as-permission
category: patterns
type: topic
content_type: topic
quality: complete
index_group: sovereignty-and-infrastructure-patterns
short_description: "The Object Capability access-control principle — a cryptographic pairing is the permission, and its absence means no pathway exists to ask for one — as embodied in the platform's machine-based node admission."
status: active
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
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

Pairing as permission is the access-control principle behind the platform's [[machine-based-auth|machine-based node admission]]: a cryptographic pairing between two nodes is the permission, and the absence of a pairing makes the connection structurally impossible — not access-denied, but no pathway to even ask. There is no central access-control list checked at request time, and no role lookup on the connection path. **A node that has never completed a pairing ceremony cannot be instructed by anything, because nothing has a way to reach it.** That safety property holds even if every other layer of the system has a bug. The model is the formally proven Object Capability pattern, deployed in production at Fuchsia OS, seL4, and WireGuard.

## The core principle

In most access-control systems, a request arrives, the system looks up whether the requester has permission, and either allows or rejects it. The lookup requires a central authority — a database, a role-policy store, a permission table.

Pairing as permission eliminates the lookup. Two nodes communicate only if a cryptographic pairing has already been established between them. If no pairing exists, no connection exists and no request is made. The question "does this node have permission to reach that node?" has a structural answer: check whether a pairing exists. If not, no pathway exists to ask in the first place.

This is the Object Capability Model — a formally proven security pattern first described by Mark S. Miller in *Capability Myths Demolished* (2003).[^1] The central axiom: **connectivity begets connectivity.** Object A can send a message to B only if A holds a reference to B. The reference is the capability. Without the reference, the connection is structurally impossible.

## Node admission by pairing ceremony

The platform's real embodiment of this principle is machine-based node admission: a new node completes a pairing ceremony against an approval service before it can join the network at all, rather than joining first and being granted or denied specific permissions afterward. Until that ceremony completes and is approved, the node has no pathway into the network to request anything — there is nothing to deny, because there is no connection to deny it on.

This is a narrower, concrete instance of the general principle above, not the whole of it — the platform does not yet implement capability-based access control at every layer described by the formal Object Capability literature. What exists today is pairing-gated network admission at the node level; broader per-resource capability delegation, of the kind Fuchsia or seL4 implement throughout their respective systems, is a design direction this principle points toward, not a claim about what is built everywhere already.

## Why this is stronger than role tables

Role-based and access-list systems share a structural vulnerability: the **confused deputy problem**. A trusted intermediary — a process holding elevated permissions — can be tricked into performing an action on behalf of a less-trusted caller, using its own permissions to do something the caller could not do directly. The vulnerability is structural: it is present in any system where authority is looked up from a table at request time, regardless of how carefully that table is maintained.

In the Object Capability Model, this vulnerability is an architectural invariant rather than a bug to guard against. A holder cannot use what it was never given a reference to — there is no lookup step for a bug to corrupt.

## Production implementations

This is not a theoretical model. It is deployed at scale in production systems outside this platform.

**Fuchsia OS** (Google) implements capability-based access control at the operating-system level. Every component must have capabilities explicitly routed to it through the component topology. A component that has not been given a capability route is structurally unreachable — not access-denied, but no pathway. Fuchsia runs on every Google Nest Hub model.[^2]

**seL4 microkernel** has a machine-checked formal proof of capability confinement: a process cannot access a resource it was not explicitly given a capability for. The proof covers both integrity (data cannot be modified without authority) and authority confinement (authority cannot exceed what was delegated). seL4 is the gold standard for formally verified security models.[^3]

**WireGuard** implements the same pattern at the network layer. The `AllowedIPs` table is the capability table — a node with no entry for a destination cannot send packets to it. Access control is structural to the routing, not a check performed at transmission time.

## See also

- [[machine-based-auth]] — the real pairing-ceremony mechanism that embodies this principle today
- [[personnel-permissions]] — the platform's separate, tier-based authorization model for personnel access, distinct from this node-level capability model
- [[compounding-substrate]] — the broader architecture this access model operates within
- [[three-ring-architecture]] — the ring boundary model this principle reinforces at the node level
- [[pair-a-new-device]] — step-by-step guide: register a device through the pairing ceremony
