---
title: "Identity ledger schema design"
slug: identity-ledger-schema-design
category: security
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: current-fact
language_protocol: PROSE-TOPIC
last_edited: 2026-08-03
editor: pointsav-engineering
short_description: "Three record types — Person, Anchor, Claim — separate who is known from how they were observed and what was asserted. Identity is a UUIDv5 of a lowercased email, so the same input always yields the same identifier."
paired_with: identity-ledger-schema-design.es.md
---

**The identity ledger schema** is the three-record model this platform uses to record who is known
to it: a **Person** record establishing that an identity exists, an **Anchor** record recording
where and when that identity was observed, and a **Claim** record asserting one attribute about it
with a stated confidence and source. Separating the three keeps a durable identity from being
overwritten every time a new document mentions it, and keeps a disputed attribute from
contaminating the identity it describes. Its defining design decision is that identity resolution
involves no inference of any kind: the primary identifier is derived arithmetically from an email
address, and observations are extracted by a fixed regular expression, never a model.

The separation solves a specific problem. A single mutable person row forces every new observation
to be either merged into the existing record or discarded, and merging is where identity systems
accumulate silent, unattributable error. Under this model an observation adds an Anchor, an
assertion adds a Claim, and neither alters the Person. Disagreement between sources becomes two
Claims with different sources rather than a lost prior value. Every structural claim in this
article has been verified directly against the current canonical source of the implementing
service, [[service-people|service-people]].

## The three records

**Person** carries seven fields: the derived `id`, a display `name`, the lowercase-normalised
`primary_email`, a list of `email_aliases` (also normalised on entry), an optional `organisation`,
and creation and update timestamps. The identifier is never caller-assigned — the only constructor
derives it from the email, so a Person whose `id` disagrees with its address cannot be built.

**Anchor** carries three fields: the `target_uuid` it points at, the observed address as
`anchor_source`, and a timestamp. An Anchor deliberately does not assert that the address belongs
to any named individual — it records only that the address was observed and what identifier
corresponds to it. Anchors are append-only; the system never modifies or retracts one.

**Claim** carries seven fields: a `claim_id` (a random UUIDv4, unique per observation — unlike the
derived identity UUID), the `target_uuid` it annotates, an `attribute` name and observed `value`, a
`confidence_score`, a `source_id` recording where the observation came from, and a timestamp. In
the sanctioned extraction path the confidence score is `1.0` for every Claim without exception,
because the only extraction method wired to it is a deterministic regular expression scanning for
email addresses; the field exists for possible future extraction methods, which would remain
subject to the no-inference boundary described below.

The asymmetry is the design. Person is the stable object; Anchor and Claim both point *at* a person
identifier and neither can modify it. Confidence lives on the Claim, where a contested assertion
belongs, and never on the Person.

### Deterministic identity

The person identifier is a version-5 UUID derived from the lowercased primary email address under
the standard DNS namespace:

```
id = UUIDv5(NAMESPACE_DNS, lowercase(primary_email))
```

The constructor lowercases before hashing, and a unit test asserts case-insensitivity explicitly.
The property this buys is reproducibility without coordination: the same email address yields the
same identifier on any machine, at any time, with no shared counter, no allocation service, and no
probabilistic matching — two components that have never communicated will independently arrive at
the same identifier for the same person, because *the derivation is the registry*, not a lookup
against it.

The two UUID versions in the schema divide labour deliberately. Identity uses version 5 — a
namespaced hash — precisely *because* it is deterministic: identity must be reproducible from the
address alone. Claims use version 4 — random — precisely because they must not be: each observation
is a distinct event, and two observations of the same attribute from the same source are two
records, not one.

The cost is equally definite and belongs alongside the benefit. Identity is bound to one email
address. A person whose primary address changes derives a different identifier until an operator
links the two via the alias list; the schema chooses that visible, auditable cost over silent
inference.

## The write path — and a second, unsanctioned one

The people component writes records to the file service over HTTP: a POST to a `/v1/append`
endpoint carrying an `X-Foundry-Module-ID` header, verified by reading the client directly and by
an end-to-end test that starts a real file-service daemon and asserts a record round-trips
faithfully. Storage on the far side is the hash-chained append-only log described in
[[cryptographic-ledgers]], so identity records inherit its tamper-evidence and its checkpoint and
anchoring properties.

That is the sanctioned path, and stating it plainly matters because it is not the only path in the
tree. A standalone mining tool, `tool-acs-miner`, defines byte-identical Anchor and Claim structures
of its own, derives identifiers with the identical `Uuid::new_v5` call (a test in `service-people`
itself pins agreement between the two implementations), and writes them with ordinary filesystem
calls directly to append-mode files under its own working directory — no HTTP call, no file
service, no hash chain. It also assigns confidence scores that vary by attribute type — `1.0` for
email, `0.9` for phone, `0.6` for a proper-noun match — unlike the sanctioned path's constant
`1.0`. Records written this way are outside the ledger's integrity guarantees entirely. No script
or component in the tree was found to invoke this tool, so whether it runs anywhere could not be
established; it is reported as present rather than as active.

The schema documentation adds a third description again: a JSON schema file and a component README
describe a considerably richer record — a structured `addresses` object holding emails, phone
numbers, and endpoints, a `roles` list, and a metadata block, under field names (`identity_id`,
`addresses.emails`, `addresses.phones`) that no code in the tree writes. That document describes an
intended model, not the implemented one, which remains the seven flat `Person` fields above.

## Conflict handling

The in-process store defines a typed error for conflicting identity, carrying the email address,
the identifier already bound to it, and the newly derived one. An append that would bind an
already-known email to a different identifier is refused rather than merged, and a test exercises
that refusal.

The refusal is real; a phrase sometimes used for it deserves qualification. The conflict is
surfaced as an error returned to the caller of the append operation — in the tool interface, as an
error string on the call. There is no operator inbox, review queue, or dedicated resolution
interface in code. The guarantee that holds is *no silent merge*: the write fails and the caller
learns why. The guarantee that does not hold today is that a person is systematically presented
with the conflict for adjudication — that remains a property of whatever calls the append
operation, not of the schema itself.

## The no-inference boundary and its governance citations

The schema is built so every operation is verifiable without model state. Email extraction is one
fixed, case-insensitive regular expression. Identifier derivation is the UUIDv5 algorithm — a hash
with a fixed namespace, deterministic by definition. Conflict detection is UUID equality — no fuzzy
matching, no embedding similarity, no tuned threshold. There are no model weights in the identity
service and no calls to any inference endpoint on the ingest path; the component's own source
states this directly.

Two distinct governance rules are frequently cited together here and are worth separating, since
conflating them misstates both. **SYS-ADR-07** prohibits routing structured data through an
inference model — it is the rule behind this zero-inference extraction path. **SYS-ADR-10** is the
separate rule requiring a mandatory human checkpoint at commit time; it governs human commitment to
a write, not the absence of a model in the pipeline. They are two rules governing two different
mechanisms, not one compound rule.

Planned extensions sit outside the no-inference boundary by design: a cross-tenant identity query
interface, and an optional similarity layer that may *suggest* candidate merges for operator review.
Both are intended for the platform's second ring; neither exists in the current implementation, and
under the platform's rules any inference-derived suggestion would require explicit operator action
before anything reached the first-ring ledger.

## What this is not

**This is not the queue-based verification flow.** The human-in-the-loop tool described in
[[verification-surveyor]] operates on per-transaction JSON files in a discovery queue and never
touches these record types or the file service. Two systems share the word "identity" and a
directory prefix and share no code.

**The implemented Person record is not the documented one.** The component's JSON schema and README
describe a richer record with structured addresses, roles, and metadata under field names nothing
writes. The implemented record is seven flat fields.

**Not every writer of these record shapes goes through the file service.** The standalone mining
tool writes identical structures directly to local append-only files, outside the hash chain. Any
claim that all identity records are covered by the ledger's integrity properties is true of the
sanctioned path and not of that one.

**Deterministic identity is not identity resolution.** The derivation guarantees that the same
email yields the same identifier. It does not decide whether two different email addresses belong
to the same person, and it will not conclude that two different addresses belong to the same
human — joining them requires a deliberate operator act on the alias list, never an automatic
merge. Treating anchor volume as a fact about an individual would also misread the schema: an
Anchor is not a claim about a person at all, only about an address's occurrence.

**Conflicts are not routed to a person.** They are refused and returned as an error to the caller.
The absence of a silent merge is the delivered property; systematic adjudication by a reviewer is
not implemented.

**Immutability is not a property of these records themselves.** It comes from the file service's
chained, checkpointed, read-only-on-write storage. Records written outside that path — as the
mining tool's are — have none of it.

## See also

- [[cryptographic-ledgers]] — the append-only chained storage the sanctioned write path uses
- [[worm-ledger-design]] — the write-once record model and its guarantees
- [[service-people]] — the component owning the Person, Anchor, and Claim types
- [[verification-surveyor]] — the separate human confirmation step for queued fragments
- [[machine-based-auth]]
- [[three-ring-architecture]] — the layered arrangement in which the archive tier sits
- [[tiered-entity-extraction-architecture]] — the extraction stages producing anchors and claims
