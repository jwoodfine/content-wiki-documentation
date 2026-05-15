---
schema: foundry-doc-v1
title: "Architecture Decisions"
slug: architecture-decisions
category: governance
type: governance
quality: complete
short_description: "Twelve binding architecture decisions — recorded commitments that govern how the PointSav platform is built and constrain all future engineering work on data handling, human oversight, system separation, and deployment custody."
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: architecture-decisions.es.md
---

Architecture decisions are recorded commitments — choices made deliberately, for stated reasons, that bind all future engineering on the platform. Unlike conventions, which describe how the team prefers to work, architecture decisions describe what the platform will not do regardless of convenience. Twelve decisions govern the PointSav platform as of the current release. Three of these — ADR-07, ADR-10, and ADR-19 — carry the heaviest regulatory weight: together they define the boundary between automated processing and human authority over the platform's permanent records. By the end of this article, a reader will understand the three decisions that most affect compliance posture, the decisions that govern structural separation, and the decisions that govern deployment custody.

## The three decisions that govern AI and human authority

These three decisions define where automated processing stops and human authority begins. They are the decisions an auditor, a procurement evaluator, or a technical due-diligence reviewer should read first.

**ADR-07 — Data must be classified before the AI boundary touches it.**
Every file that enters the platform is classified by type before any processing occurs. Structured data — spreadsheets, ledger entries, database exports, signed documents — routes to deterministic parsing engines that produce verifiable, repeatable output. Unstructured human text — correspondence, meeting notes, narrative reports — routes to the language model boundary. Nothing crosses the boundary unclassified. This prevents the platform from applying AI reasoning to records that should have deterministic, auditable treatment.

**ADR-10 — Every base-asset ledger entry requires a human checkpoint.**
The platform's F12 input interface is the mandatory human-in-the-loop checkpoint for all base-asset ledger commits. No automated process can write a verified record to long-term storage without a human confirming the routing decision at the F12 gate. The design mirrors the control structure of a regulated clearing house: the platform can process, classify, and propose — but the commit belongs to an authorised human.

**ADR-19 — No automated publishing to verified ledgers.**
Automated processes are prohibited from publishing to the long-term storage ledgers. All verified records are committed only through a human-authenticated action at the F12 interface. The decision closes the loop between ADR-07 (classify first) and ADR-10 (human checkpoint): the classification proposes, the checkpoint confirms, and the commit to the permanent record requires the operator's intentional action. There is no back-channel path through which the system can record a fact without a human in the sequence.

Together, these three decisions produce a record structure that satisfies the custody requirement common to regulated financial and property operations: the system generates structured proposals, humans authorise permanent records, and the audit trail captures both.

## The decisions that govern data structure and internal separation

**ADR-17 — Three tiers of data, one human-authenticated tier.**
The platform's data is modelled in three tiers. The first tier is raw base assets — original documents and records as received, treated as immutable. The second tier is a self-healing taxonomy index — the platform's classification of those assets, which can be updated as rules change without altering the underlying record. The third tier is synthesised output — reports, summaries, and structured extracts derived from the base assets. Only the base asset tier requires a human-authenticated commit per ADR-10. The taxonomy and synthesis layers can self-correct without further human action, because they derive their authority from the immutable tier underneath them.

**ADR-06 — Compliance ledger separated from the intelligence pool.**
The immutable compliance ledger — the service that handles inbound communications and regulated correspondence — is physically separated from the self-healing intelligence pool that the platform uses to classify and link documents. The separation prevents a common failure mode in retrieval pipelines: when the compliance record and the search index share a data layer, an index update can silently alter what the compliance record appears to contain. Physical separation eliminates that risk by construction.

**ADR-11 — Console chassis separated from execution cartridges.**
The operator console is divided into a presentation chassis — the UI shell that handles layout, navigation, and keyboard bindings — and a set of execution cartridges, each of which implements a specific console function. The chassis and cartridges can be deployed and updated independently. A change to the compliance-review cartridge does not require redeploying the presentation shell, and vice versa. This separation makes the console's individual functions auditable and replaceable without risk to the shell's stability.

**ADR-14 — Static assets and live commands use separate proxy routes.**
Static UI assets — the files a browser downloads once to render the console — are served from an edge web server optimised for caching and delivery. Live API commands — the instructions an operator sends to the platform — travel through an encrypted mesh network to the backend. The routes never mix. Eliminating the Rust backend as a static file server removes a class of latency and caching problems that would otherwise appear only under production load conditions.

## The decisions that govern custody and deployment

**ADR-13 — Cryptographic keys remain on the operator's hardware.**
The master routing node and its cryptographic keys reside on the operator's local machine as a Type-II virtual machine. They are not hosted in commercial cloud infrastructure. This decision reflects a specific custody principle: the entity that holds the signing keys for a regulated record set should be the regulated entity, not a third-party cloud provider. The deployment model is designed so that a customer can satisfy this requirement without managing bare-metal infrastructure.

**ADR-08 — systemd is a quarantined dependency.**
The systemd init system, required on current Debian cloud nodes, is formally classified as a quarantined component — a dependency the platform accepts temporarily while the microkernel replacement is planned. The decision is recorded so that future engineering work does not inadvertently deepen the dependency. Platform services that currently run under systemd are designed to be portable to the target microkernel without architectural rework.

## The decisions that govern operational integrity

**ADR-15 — Console pages are never cached.**
All operator console pages are served with cache-disabling headers and versioned fetch parameters. The decision eliminates a failure mode that appears in regulated operational tools: a browser presenting a stale cached state of the console while the underlying data has changed. An operator acting on a cached console view may take an action based on information that no longer reflects the platform's state. The platform prevents this by construction rather than by operator discipline.

**ADR-16 — Peer commands travel as unicast, not broadcast.**
Commands sent to peer nodes in the platform's mesh network travel as individual unicast deliveries — one command per node — rather than as a network broadcast. Native UDP broadcast is incompatible with the WireGuard encrypted mesh the platform uses for inter-node communication. The unicast loop preserves delivery guarantees without requiring a separate broadcast layer.

**ADR-18 — The operator console is a heads-up display.**
The operator console is designed as a heads-up display that bridges operators to the platform's derivative data architecture. Each function key maps to a distinct cartridge viewport — a bounded view of one part of the platform's data — rather than to a free-form interface. The design limits the surface area of each operator interaction, which reduces the categories of error an operator can introduce in a single session.

## See also

- [[doorman-protocol]] — the Doorman service that enforces ADR-07's data-classification boundary in production
- [[app-console-input]] — the F12 input gate that implements ADR-10's human checkpoint
- [[worm-ledger-design]] — the WORM ledger architecture that makes ADR-19's prohibition enforceable
- [[three-ring-architecture]] — the ring structure that ADR-06's separation reflects at the service layer
- [[disclosure-substrate]] — the architecture that produces the auditable record chain these decisions protect
