---
schema: foundry-doc-v1
title: "tool-accounting — double-entry ledger and audit-ready financial statements"
slug: tool-accounting
category: applications
type: tool
content_type: topic
quality: complete
index_group: financial-and-construction-tools
status: active
audience: vendor-public
bcsc_class: forward-looking
language_protocol: PROSE-TOPIC
last_edited: 2026-09-01
editor: pointsav-engineering
paired_with: tool-accounting.es.md
short_description: "A flat-file, owner-held double-entry accounting engine producing audit-ready financial statements from plain-text journals; its core engine and PDF/HTML renderer are built and verified against real historical data, ahead of the rest of the platform's ledger tooling."
cites: []
---

`tool-accounting` is a double-entry accounting engine built to hold a group of related
entities' books as a plain-text, owner-held record rather than as rows in a hosted
database. It journals every transaction, folds those journals into a computed ledger and
trial balance, and renders audit-ready financial statements and narrative disclosure —
without requiring a server, a subscription, or a proprietary file format to read any of it
back later.

The problem it answers is durability and provability at the same time. It aims to leave
behind a set of books any computer can still read in twenty years, that nothing can
silently overwrite. A reviewing accountant should be able to walk from a statement figure
back to the entry that produced it — without taking anyone's word for the trail in
between.

---

## Design commitment: double-entry, computed and never stored

Every transaction posts as two effects of equal and opposite size on two different
accounts — a payment reduces cash and increases an expense by the identical amount, in one
entry. Because every account balance is built from many such paired effects that always
cancel, the sum of every balance across the ledger is provably zero at every instant. That
fact, checked mechanically at the moment an entry is posted, catches what a single running
total cannot: an unbalanced entry, a reference to an account that does not exist, an
amount posted to only one side.

**Why it matters:** an error in a double-entry ledger cannot hide the way it can in a
simple running total — the books either balance, or the engine refuses the entry that
broke them. That is what lets an owner trust a set of books nobody has audited yet.

`tool-accounting` never stores the ledger itself. The running balance of every account is
recomputed in full from the underlying journal entries every time a report runs, and the
result is never written back. A second, incrementally updated copy is a second thing that
can drift from the journal it was supposedly derived from; a ledger with no existence
apart from the entries it was just computed from cannot disagree with them.

```rust
pub struct Money {
    pub minor: i64,          // an exact integer count of minor units — never a float
    pub currency: Currency,  // carried explicitly on every amount
}
```

Money values are integers, never floating-point — an amount is parsed once from text into
an exact count of minor units and stays exact through every fold. A value entered with
more than two decimal places is refused outright rather than rounded, because float noise
introduced upstream is not a real amount.

**Edge cases:** every report run takes an explicit `run_date` from the caller — never the
system clock — so the same record, rendered the same way twice, produces byte-identical
output regardless of when or where it runs. A reporting period is always explicitly
disjoint (one quarter only) or cumulative (year-to-date); the engine never infers which
from context, and a cumulative label is rejected outright at the journal-entry level.

---

## The data model

Every entity's chart of accounts is a single flat file, not a table an operator can
silently extend by typing a new code into a transaction. An entry referencing an account
the chart does not contain fails to load — an invariant failure, not a new account created
by side effect. A small set of other master files carry the same discipline. Each is a single
source of truth for one category of fact, referenced by code rather than re-typed at the
point of use. Among them: an entity registry (jurisdiction, functional currency, reporting
framework, which periods are formally delivered), a counterparty registry, a period
registry, opening balances, and an exchange-rate table. A consolidation-membership table
rounds out the set, kept separate from both the chart and the entity registry.

**Why it matters:** a reviewer reading the chart of accounts sees the same open questions
the engine sees. An account whose sign convention is still undecided is excluded from
every computed statement and reported by name — never guessed at.

Every posted transaction is one row of a fixed seventeen-field schema. The fields cover
entity, account, fiscal year, disjoint quarter, and transaction date; counterparty
(tagged intercompany or external at entry time, never inferred later) and description; a
reference number and an optional pre-tax subtotal and tax amount; and currency, the
functional-currency amount, and an invoice reference. There is exactly one such schema.
The engine refuses to load a file whose structure has drifted from it.

```rust
pub struct JournalLine {
    pub entity_code: String,
    pub account_code: String,
    pub fiscal_year: u16,
    pub period: JournalPeriod,        // Q1 | Q2 | Q3 | Q4 — always disjoint
    pub txn_date: String,
    pub counterparty_type: String,    // "intercompany" | "external"
    pub amount: Money,                // the functional-currency amount
    // ...
}
```

**How it works, in flat-file mode:** journal files live as CSV under a plain git
repository with zero remotes — a directory `tool-accounting-core` reads in full once per
report run, never once per account. The filename itself carries the entity, account,
fiscal year, and quarter, duplicating what is already inside the file on purpose, so a
lint pass can cross-check a file's declared identity against its own rows.

---

## Consolidation and multi-entity structure

`tool-accounting` is built to hold more than one entity at once: a primary reporting
entity, a general partner or equivalent controlling entity excluded from its own
consolidation, and one or more wholly-owned subsidiaries consolidated into the group. Each
tier can carry a different reporting obligation, registered per entity rather than assumed
platform-wide. Combining related entities' books is not simple addition. An intercompany
transaction must be identified as such at the moment it is entered. An elimination
requires both sides of a transaction to tie to exactly the same figure before it is
removed. And every eliminating entry is itself an ordinary, reviewable journal entry —
never a spreadsheet adjustment invisible to anyone who did not build it.

**Why it matters:** a group's consolidated balance sheet should not simply add up what one
entity owes another and call it group debt — that double-counts an obligation which, from
outside the group, is no obligation at all. The engine refuses to eliminate a mismatched
pair rather than paper over the difference.

Ownership percentage is a general field on every consolidation-membership row from the
outset, even where every member today is wholly owned, so the equity logic needs no
structural rewrite if a partially owned entity is ever added.

---

## Audit-readiness posture

The design target is a record a reviewing accountant could reasonably accept as reliable
without independently re-performing it. Four properties do that work: output reproducible
from the same inputs; a population of entries that is tamper-evident once posted; an
opening balance independently re-derived rather than only asserted; and a mechanical path
from any statement figure back to the entries that produced it. **This is a design
posture, not a compliance certification of any kind** — a design that makes an audit more efficient to
perform is not the same claim as a design that has passed one.

**Why it matters:** an owner who has never engaged an auditor still gets a record held to
the same discipline an audit would demand of it. The standard does not wait for someone to
check the homework.

The engine refuses to render anything on an invariant failure — an unbalanced entry, a
reference to an account that was never declared, an unresolved opening-balance discrepancy
— rather than continuing past it with a warning. The one governed exception is a formally
logged reconciling item, itself required to close within two reporting periods or the run
fails outright.

---

## Where the record lives

`tool-accounting-core` runs against a plain directory of CSV files today — a real, running
mode, and a permanent one rather than a stage the platform intends to retire. A second
storage mode is planned but not yet built: appending the same records through
[[service-fs]]'s hash-chained, tamper-checked append log inside a [[totebox-archive]].
That mode would let a reviewing accountant verify not just that an entry's contents are
unaltered, but that the log it sits in has only ever been appended to since a prior
checkpoint they held. Both modes are intended to share every layer above the storage trait
itself, so which one an owner uses would change nothing about the engine's logic — only
where the bytes live.

**Why it matters:** an owner is never required to adopt a hosted platform to use the
ledger. The engine can be handed to an accountant as a folder on a laptop, and every figure
in a statement can be reproduced from it on that accountant's own machine.

---

## Build status

`tool-accounting-core` — the shared money, period, and journal-line types, the CSV parser,
and the chart, ledger, and trial-balance logic — is built and has been verified against
real historical annual data rather than synthetic fixtures, which surfaced and fixed real
data-entry defects in the process. `tool-typeset`, the zero-dependency PDF and HTML
renderer this engine shares with the platform's sibling construction tool, is built and
independently verified by extracting text back out of a rendered PDF and checking it
against the source structure. Together they have already run one full fiscal year's
complete pipeline — journals into a computed ledger, a trial balance folded from it,
rendered statements, and rendered narrative. That run was entered and rendered end to end
for a primary reporting entity and its general partner, and a second year is now in
progress.

**Why it matters:** an owner evaluating this platform is not being asked to take the
design on faith. The components that touch real dollar figures have already been checked
against a real year of real transactions, not designed on paper alone — which puts
`tool-accounting` further along than any comparable tool elsewhere in the platform's
ledger-and-statement family.

What is registered but not yet active: several wholly-owned subsidiary entities are
registered as consolidation members, with membership and ownership percentage recorded and
fully specified. But the consolidation math itself is not yet wired in, no journal data
exists yet for those subsidiaries, and interim (quarterly) statement rendering is
specified but not yet built. Opening balances are empty for every entity; current runs
treat an opening balance as an open item rather than assuming a figure, and dual
verification against a prior year's own closing balance is a locked design not yet
exercised in practice. The bookkeeping review terminal planned to confirm entries into the
ledger is scaffolded and active as a plugin surface, but it is not yet wired to live ledger
data — its current view renders placeholder figures. A cross-archive aggregation component
intended for a firm servicing many owners' books at once is referred to here under the
working name `app-orchestration-accounting`. **This is a proposed name and scope only —
not a name ratified anywhere else in the platform** — and nothing under that name exists
yet.

---

## Licensing

`tool-accounting` is licensed under AGPL-3.0-or-later. AGPL-3.0-or-later is a copyleft
license: the source code is available to everyone, and any modified version — including
one operated as a network service — must be released under the same license if it is
distributed or made available over a network. A separate PointSav-Commercial license is
available as a paid alternative for anyone who needs to distribute a modified version, or
offer it as a network service, without that copyleft obligation.

**Why it matters:** a lender or an owner's own engineer can read and audit the full source
before deciding whether to trust it — the code is not a black box behind a paywall.

---

## See also

- [[tool-construction]] — the sibling development-and-construction ledger tool, built on
  the same double-entry design and sharing this engine's renderer
- [[service-fs]] — the append-log storage substrate the planned archive storage mode is
  designed against
- [[totebox-archive]] — the owner-held archive an entity's records are intended to live
  inside
- [[service-input]] — parses and content-addresses a source document before it becomes a
  proposed journal entry
