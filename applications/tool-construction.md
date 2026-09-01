---
schema: foundry-doc-v1
title: "tool-construction — construction cost, schedule, and quality ledger"
slug: tool-construction
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
paired_with: tool-construction.es.md
short_description: "A flat-file, owner-held ledger for construction cost, schedule, and quality control, built on the same double-entry discipline as tool-accounting; the core engine now runs as a real CLI, posting a live pilot's estimates through all four cost-type chains — estimate-stage only, with no console surface yet."
cites: []
---

`tool-construction` is a flat-file, owner-held ledger for construction cost, schedule, and quality control, built on the same double-entry discipline as the sibling accounting engine, [[tool-accounting]]. It is designed to serve three audiences at once: an implementation reference for developers building the platform out (including developers with no construction background), a technical overview for evaluating the business the software supports, and a decision document for a contractor or property owner evaluating adoption.

**What exists today.** The engine is real and running. `tool-construction-core` implements the quantity-side ledger in full — vector-valued journal entries, non-fungible units, and all four cost-type chains (labour, material, equipment, subcontract) — verified by golden-value tests that reproduce the architecture's own worked examples number for number. A pilot binary crate drives it as a command-line toolchain of five binaries that build a cost estimate bottom-up from work packages, compute a critical-path schedule, post the estimate into the ledger, and render reports as HTML and PDF. It runs against a real pilot: a live development project whose work packages are posted as real budget locks, with zero trial-balance identity failures. Two boundaries are just as real. The toolchain is CLI-only — no terminal or console surface exists, and none has been granted a build slot. And it is estimate-stage only: the ledger carries real estimates and budgets, not actuals, because no invoice, payment, or payroll record has entered the pipeline yet.

---

## The problem it solves

Construction cost control breaks a project into a **cost code** — a numbered work-breakdown structure identifying one kind of work on one project, such as cast-in-place concrete or structural steel erection. Every cost is further split by **cost type** — labour, materials, equipment, and subcontract — because the four behave differently enough that combining them destroys the information an overrun would otherwise reveal.

Underneath the cost code sits the **work package**: a defined piece of physical work carrying two numbers whose relationship is the foundation of the design — a **quantity** (obtained by measuring the drawings) and a **unit factor** (the labour hours to install one unit of that quantity). The quantity sets the labour budget; the quantity actually installed later earns that budget down. Hours worked never draw anything down on their own — they are what the drawdown is measured against.

**Why it matters:** getting this direction backwards is one of the most common real errors in job costing, and it is the specific failure the engine prevents structurally rather than by convention.

---

## Earned Value Management and backflush costing

Spending and progress are not the same thing — a project that has spent 60% of its budget may be 30% or 80% complete. The engine uses **Earned Value Management**, tracking Planned Value, Earned Value, and Actual Cost as three numbers in the same unit, so that cost efficiency and schedule adherence become leading indicators rather than something only visible after the fact. The design specifically guards against a known failure mode: if earned value were derived from hours spent rather than independently observed installed quantity, the measurement would compare a quantity with itself and could never report a problem — so independently reported installed quantity is treated as mandatory, not optional. The earned-value identities are enforced as trial-balance unit tests over the ledger fold, not computed by a separate formula that could drift from the postings.

Material consumption is built around **backflush costing**: rather than tracking every physical movement of material on site, the system records what was produced and calculates backward what must have been consumed, using a known factor, leaving only the difference against a periodic physical count to investigate. This is driven by quantity installed, never by hours worked — driving it by hours would let a slow crew appear to have consumed more material than a wall actually contains, confounding a labour signal with a material signal.

**Why it matters:** both mechanisms turn day-to-day field reporting into an early warning about cost and schedule problems, months before a financial statement would show the same thing. On the current pilot, this machinery is built and tested but not yet fed: no independent installed-quantity source exists for the project, so earned-value columns report nothing rather than a derived guess — see the reporting rule below.

---

## One journal, two projections

The engine keeps two ledgers, denominated differently on purpose. The **production ledger** holds physical quantities — hours, cubic metres, tonnes, schedule-of-values fractions. The **cost ledger** is designed to hold dollars, fed only by real payroll and accounts-payable postings, never by converting the production ledger's quantities through a rate. A lump-sum subcontractor's obligation is a function of the contract and the percentage certified complete, not of the hours their own crew worked — two ledgers keep that case honest, rather than forcing an invented dollar figure or an hours-based approximation. The quantity-side ledger is implemented in full; the dollar-side ledger is deliberately deferred until real payable and payroll data exists to feed it, rather than being built against invented figures.

The two ledgers are named projections of one journal, not separate books — an approach with production precedent (SAP's own Material Ledger was eventually folded into a single Universal Journal). Within that one journal, different kinds of quantity are never summed together. The unit type makes this a compile-and-runtime guarantee rather than a convention:

```rust
pub enum Unit {
    Labour(LabourClass),
    Material(MaterialSpec),
    Equipment(EquipmentSpec),
    Contract(ContractUnit),
}
```

A journal entry is vector-valued — one real-world event, such as a day's work reported, posts across several units at once in a single atomic entry — and the balance check runs componentwise, each unit's debits and credits required to balance independently. Adding across units is refused, not discouraged. Ledger state is never stored as a running total: every run folds the full journal fresh into account markings, so the trial-balance identities are re-proved from first entries on every execution.

**Why it matters:** the ledger cannot silently blend hours into cubic metres or either into dollars, and any corruption of state would fail loudly on the next fold instead of compounding quietly.

---

## The four cost-type chains

Each cost type carries its own chain of accounts and its own posting rules, because each fails differently. The labour and material chains implement the budget-lock and earn-down mechanics described above, including the firing precondition that gives the ledger its teeth: budget accounts hard-refuse an over-relief until a change order re-encumbers them, while stores accounts render and flag rather than block — the distinction between "this posting would overdraw an authorization" and "this posting reveals a variance worth investigating."

The **equipment chain** adds an operating-status dimension to every posting — operated, idle, standby, transport — following established industry job-costing practice rather than an invented taxonomy. Utilisation loss and productivity variance are then computed as pure filters over the same ledger fold, never as a separately derived formula, so the two components are structurally guaranteed to sum exactly to the chain's residual instead of needing a reconciling check.

The **subcontract chain** models a schedule-of-values line as a fraction-of-lump-sum unit and carries the certification and retainage mechanics through the ledger. It also enforces the one rule that is genuinely different from every other chain: the subcontract residual must close to **exactly zero**. Where every other chain's variance is a computed number to be explained, a subcontract closeout refuses on any non-zero residual until an explicitly authorized write-off is posted.

**Why it matters:** an over-claimed subcontract certification, an idle machine billed as productive, or work continuing past an exhausted change-order budget each surface as a refused or flagged posting at entry time — not as an anomaly someone might notice in a report weeks later.

---

## Whose ledger it is

A job-cost ledger only means something from one seat: the party actually performing the work is the only party that can observe labour hours, material consumption, and certification facts. The engine makes this explicit with a small set of party roles — performer, contracting owner, certifier, subcontractor, supplier — with exactly one performer per deployment, whose books the ledger is. Party identity attaches to a posting only where the posting's meaning genuinely depends on who asserted it (the subcontract certification chain); labour, material, and equipment postings are facts about the work, not about a relationship, and carry no party at all. A regression guard runs the same subcontract lifecycle twice, once with real party names and once with opaque identifiers, and asserts identical balances — mechanical proof that the ledger's arithmetic is independent of who the parties are.

On the current pilot, the performer is MCorp — the platform's reference customer, whose staff carry out the construction work and operate the pilot ledger. The development programme the project belongs to is Woodfine's; the ledger models the performing party's books, not the owner's.

**Why it matters:** the same five roles describe a general contractor with no holding structure at all just as well as they describe the pilot — the concrete test that the engine is generic domain software, not one company's internal tool with the names filed off.

---

## Reports, and the rule that a zero is a claim

The pilot toolchain renders its reports — a cost estimate, a critical-path schedule with a Gantt timeline, a materials listing, and a monthly project status report — as HTML and PDF through `tool-typeset`, the platform's shared zero-dependency document renderer, from a single compute layer per report. Every rendered PDF is verified visually, not just by build success — a discipline adopted after passing builds produced an unreadable timeline.

Two characteristics of the reporting are worth stating because they are unusual. First, the engine computes its outputs bottom-up from work-package primitives — the way a contractor's own estimating and scheduling software would — and then reconciles them against the pilot's independently prepared professional estimates and its known schedule dates, which serve as an answer key rather than as data the reports merely reformat. Second, the status report refuses to fabricate. Where no real measurement exists — an actual cost with no invoice behind it, a percent complete with no observed progress, an incident count with no safety register — the report prints an en dash, never a zero and never a projection dressed as an observation. A zero in an incident column would itself be a safety claim; a blank is the honest state of the data.

**Why it matters:** a report from this engine is either traceable to a real input or visibly empty — there is no third state, and that property is enforced by the compute layer, not by reviewer diligence.

---

## Holdback, the lien period, and statutory clocks

Construction contracts are subject to statutory holdback (retainage) — a defined percentage of every certified payment withheld by the owner, released once a lien period during which unpaid suppliers can register a claim against the building expires with no claims registered. The design accounts for three consequences this creates: holdback applies against a certified payment application as a whole, not just against subcontract work; different kinds of work carry different lien periods, so parties on the same project become releasable on different dates; and the relevant statutory clocks run in working days, not calendar days, making a correct working-day calendar a legal requirement of the software rather than a scheduling convenience. The subcontract chain's certification and retainage mechanics are built; the working-day calendar and statutory-clock model is the largest piece of this section still unimplemented, and it gates the payment-cycle reporting that would sit on top of it.

---

## Platform services

Three pieces of the engine's domain were deliberately built as standalone platform services rather than internal modules, so that later applications and reports can read the same data without going through this engine: `service-materials`, the canonical work-package store; `service-schedule`, the critical-path compute service; and `service-notify`, a domain-agnostic watcher that fires on deadlines and threshold breaches when a caller reports an observation. `tool-construction` consumes them as an ordinary HTTP client — the pilot's work packages live in `service-materials`, and the materials report is rendered from what the service returns, not from the file the engine loaded. Each service journals its state and rebuilds its index on restart. All three run locally today; production supervision wiring is deferred.

**Why it matters:** cost, schedule, and alerting data live behind service boundaries any future application can read, so the CLI engine is one consumer of the platform's data rather than its owner.

---

## Product topology and the free/paid boundary

`tool-construction` is one component in a larger family: the construction ledger itself; the sibling accounting engine, [[tool-accounting]], which is designed to receive a one-way feed of dollar cost from it; `tool-typeset`, the shared document renderer now doing the production rendering for both engines; and the proposed [[tool-payroll]] engine, which is designed to receive a one-way feed of hours and labour class from the construction ledger as timecards. Pilot-scoped sibling crates for the accounting and payroll engines are scaffolded alongside the construction pilot, but the cross-engine feeds themselves are not yet wired — the dollar-side and payroll integrations wait on the real actuals data described above.

The platform's archive substrate and terminal are free (Apache-2.0); cross-archive aggregation is the paid boundary that applies platform-wide. `tool-construction` is designed as a separate, second commercial surface on top of that — what would be sold is the domain engineering itself (the quality-scoring schema, the earned-value mathematics, the ledger mechanism), not a markup on infrastructure that is already free.

The platform's distribution rules classify `tool-*` components as internal operator tooling not distributed as a standalone product by default, with exceptions granted individually — `tool-wallet` is the one existing precedent. **No distribution exception is currently recorded for `tool-construction`.**

## Licensing

`tool-construction` is licensed under AGPL-3.0-or-later. AGPL-3.0-or-later is a copyleft license: the source code is available to everyone, and any modified version — including one operated as a network service — must be released under the same license if it is distributed or made available over a network. A separate PointSav-Commercial license is available as a paid alternative for anyone who needs to distribute a modified version, or offer it as a network service, without that copyleft obligation.

---

## What is not yet built

The boundaries stated at the top are worth restating precisely. Not yet built: the dollar-side cost ledger (payables, payroll postings, holdback dollars) and with it any actual-cost reporting — the pilot has no invoice, payment, or payroll document in its pipeline, and the engine reports that absence rather than modelling around it; an independent installed-quantity measurement source, which gates real earned-value reporting; the working-day calendar and statutory-clock model; the one-way feeds into [[tool-accounting]] and [[tool-payroll]]; the archive storage adapter that would persist ledger data through the platform's own record store; the sale-transition access-transfer mechanism; and any console or terminal surface — the two proposed screens (a ledger table view and a work-package/quality panel) remain without a build slot on the platform's fixed twelve-function-key terminal, and the toolchain is operated entirely from the command line.

Open design questions that remain genuinely unresolved include whether quality sign-offs need cryptographic signing given their potential legal weight in a defect claim, whether individual-performance scoring belongs inside this system or stays a separate concern, and what triggers and authorizes the sale-transition access transfer and interfaces with a real legal closing process.

## See also

- [[tool-accounting]] — the sibling accounting engine designed to receive a one-way cost feed from this ledger
- [[tool-payroll]] — the proposed payroll engine designed to receive a one-way timecard feed from this ledger
