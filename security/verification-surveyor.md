---
title: "Verification surveyor"
slug: verification-surveyor
category: security
index_group: identity-and-permissions
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: current-fact
language_protocol: PROSE-TOPIC
last_edited: 2026-08-03
editor: pointsav-engineering
short_description: "A command-line tool that requires a person to confirm each extracted identity against external evidence before it is promoted from a queue to a verified record, throttled to ten confirmations per day."
paired_with: verification-surveyor.es.md
---

**The verification surveyor** is a command-line tool that requires a person to confirm each
machine-extracted identity against external evidence before it becomes a durable record. It sits
between a discovery queue of unverified fragments produced by automated extraction and a verified
ledger, and nothing crosses that boundary without a human decision recorded at the moment it is
made — enforced under a hard cap of ten verifications per operator per day.

Its purpose is to keep a specific kind of error out of the record. Automated extraction produces
plausible identities — a name and an email address appearing near a company and a job title in the
same document — and plausible is not the same as correct: an automated pipeline processing large
volumes of text will inevitably parse an "Unsubscribe" link as a name or lift a role title from a
footer rather than a biography. Once a wrong identity enters an append-only ledger it cannot be
quietly removed; it must be superseded, and everything derived from it must be revisited. The
surveyor makes the cost of that error fall on a person's attention for a few seconds rather than on
the record forever.

## How it works

The tool is a Python script of roughly 140 lines, invoked through a short shell wrapper. It reads
from a discovery queue directory, writes to a verified ledger directory, and consults an archetype
catalogue, all beneath a base path that defaults to a deployment location and is overridable by
environment variable.

For each queued fragment the operator is shown the extracted identity and asked a single question,
prompted verbatim as: *Paste Verified LinkedIn URL (or type 'reject' / 'skip')*. Critically, the
operator looks the individual up using *their own* browser and *their own* account on the external
directory — the platform never initiates the lookup itself, so no persistent foreign API token
needs to exist anywhere in the platform, no per-query cost accrues, and the platform is never
exposed to rate-limiting or address-blocking by the directory service, because from that service's
perspective the traffic is one human using their own account. The operator's answer determines one
of three outcomes.

**Skip** leaves the fragment untouched in the queue and moves on. This is the correct answer when
the operator cannot decide.

**Reject** deletes the fragment from the queue outright. Nothing is retained — no rejection record,
no tombstone. The fragment is treated as noise that should never have been queued, which still
gives the upstream extraction pipeline an implicit signal about the failure modes its patterns
produce, even without a retained audit trail of the rejection itself.

**A pasted URL** advances to a second prompt asking for an archetype identifier drawn from a fixed
catalogue of eleven professional archetypes (The Executive, The Guardian, The Fiduciary, and eight
others), loaded fresh from the platform's content ontology each session so classifications stay
consistent across operators and across time rather than being free-typed. An identifier not present
in the catalogue halts processing immediately rather than accepting an unclassified record. A valid
selection marks the record verified, attaches the supplied URL, the chosen archetype, and a
verification timestamp to its provenance, writes the enriched record to the verified ledger under
the same filename, removes the original from the queue, and increments the daily counter.

### What a queued fragment contains

The record the operator judges is deliberately thin: an identifier field, a display name, a claims
object holding an email address, a company, and a position, and a provenance object naming the
source file the fragment was extracted from. Nothing in it is authoritative — every field is a
machine's reading of a document, and the provenance entry exists so the operator can go back to
that document if the extracted values look wrong together.

Verification adds rather than replaces. The confirmed URL, the chosen archetype, and a verification
timestamp are attached alongside what was already there, and the status field is set to verified.
The original extracted values are not overwritten or discarded, so a later reviewer can see both
what was extracted and what a person concluded about it. The file keeps its original name as it
moves between directories, which is what makes the two directories readable as one pipeline rather
than two unrelated stores.

### The throttle as a quality mechanism

A hard limit of **ten verifications per operator per day** is enforced, tracked in a single-line
throttle file in the operator's home directory holding a date and a count; a stored date that no
longer matches today resets the count automatically. There is no lock, because it is a
single-operator local file rather than a shared resource.

The limit is a deliberate quality control, not a capacity constraint, aimed at a well-known failure
mode of human review: high-volume approval at speed decays into habitual confirmation, where the
reviewer's click becomes a reflex rather than a judgment. Capping the day at ten keeps each
verification a deliberate act, and it inverts the usual economics of data pipelines, where
throughput is the metric and review is the cost to minimise — here the review *is* the product, and
the cap is what makes the verified ledger's quality claim credible rather than nominal. Ten careful
confirmations a day compound to roughly 3,650 verified relationships per operator per year, with an
error rate the design argues should approach zero, because every record passed a fresh, unhurried
human check against a primary external source.

**The people component's own README states a different, contradicting figure.** It describes the
surveyor workflow as "restricted to 40-60 daily human verifications." Direct comparison against the
enforced code (`MAX_DAILY_VERIFICATIONS = 10`) and against the platform's user guide, which
independently states ten in both its prose and its pipeline diagram, confirms the README figure is
wrong and the code is authoritative — a cross-document inconsistency worth naming precisely rather
than silently reconciling, since the README continues to describe a mechanism that does not match
what runs.

## Where it lives, and where it does not

The script is part of the content console component (`app-console-content`), not the people
component (`service-people`) — a small correction with real consequences for anyone trying to find
it or reason about its dependencies. Describing the identity service as the surveyor's "owner"
overstates the coupling.

The discovery queue and verified-ledger directories sit under a people-component *path* in a
deployment layout, which is the source of the confusion, but the people component's own code never
touches them — searching that component's source for either directory name returns nothing.
Fragments are placed in the queue by two splitter programs belonging to the email service
(`email-splitter` and `sovereign-splinter`), which write plain files directly; the surveyor reads
them; nothing else in the platform participates. A whole-tree search confirmed a single copy of the
script and a single definition of its daily limit — there is no drifted duplicate elsewhere.

The result is two parallel systems sharing the word "identity" and a directory prefix without
sharing any code. One is the file-based queue described here. The other is the record model
described in [[identity-ledger-schema-design]], reached over an HTTP interface and persisted
through the file service. Treating them as one system leads to incorrect conclusions about both.

An earlier review pass on this subject wrongly concluded the surveyor mechanism did not exist,
having searched only the identity service's own source; that finding was retracted once the real
implementation was located in the content console. The standing lesson: a single-crate search is
not sufficient evidence that a described mechanism doesn't exist anywhere in the monorepo.

## No inference anywhere in the path

The verification step contains no artificial-intelligence component of any kind. The script makes
no network calls, imports no model or inference library, and its classification step is a manual
choice from a fixed catalogue. The people component's own source states the same rule for the
records it builds — extraction is pattern-matching only, with no inference in any construction
path. This matters because the surrounding platform does contain assistive tooling: the same
content console hosts an unrelated drafting feature that calls a language-model endpoint. The two
share a component but not a code path, and the verification flow is deliberately kept clear of it.

## What this is not

**This is not part of the people component.** The script lives in the content console. The people
component owns a different, HTTP-and-ledger-based identity model and does not read or write the
queue directories at all.

**This is not an automated verification service.** No API key, scraper, or integration connects the
platform to any external directory — if the operator does not personally look a record up, no
lookup happens.

**This is not an approval workflow.** There is no second reviewer, no escalation path, and no
record of rejections. One operator decides, and a rejected fragment is deleted rather than retained
for audit.

**A verified record is not an authenticated one.** The confirmation establishes that a person
matched an extracted fragment against a public professional profile they judged to be the same
individual. It is a considered human judgement, not proof of identity, and it inherits whatever
accuracy that external profile has.

**The throttle is not a security boundary.** It is a plain counter in a file in the operator's own
home directory, resettable by deleting it. It exists to protect decision quality, not to resist an
adversary.

**Ten per day is not a scaling plan.** At the enforced rate the mechanism verifies a few thousand
identities a year at most per operator. Any larger corpus requires more operators, not a higher cap
— anyone imagining thousands of verifications per week per operator has imagined a different, and
by this design's own argument, lower-quality system.

## See also

- [[identity-ledger-schema-design]] — the separate record model reached through the file service
- [[service-people]] — the component owning that model, and the one that does not own this tool
- [[adr-07-zero-ai-in-ring-1]] — the rule prohibiting inference in the archive tier's extraction path
- [[archetypes-and-chart-of-accounts]] — the classification catalogue the second prompt draws on
- [[tiered-entity-extraction-architecture]] — the extraction stages that fill the queue
- [[service-email]] — the component whose splitters write queued fragments
- [[machine-based-auth]]
