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
last_edited: 2026-08-30
editor: pointsav-engineering
paired_with: tool-construction.es.md
short_description: "A flat-file, owner-held ledger for construction cost, schedule, and quality control, built on the same double-entry discipline as tool-accounting; scaffolded and compiling but with no pipeline logic written yet."
cites: []
---

`tool-construction` is a flat-file, owner-held ledger for construction cost, schedule, and quality control, built on the same double-entry discipline as the sibling accounting engine, [[tool-accounting]]. It is designed to serve three audiences at once: an implementation reference for developers building the platform out (including developers with no construction background), a technical overview for evaluating the business the software supports, and a decision document for a contractor or property owner evaluating adoption.

**What exists today.** `tool-construction-core` and `tool-construction-pro-01` are real Cargo workspace members that compile cleanly, but they are empty skeletons — no pipeline logic has been written yet. One real pilot construction site is registered, with its source documents cited by hash, but zero ledger entries exist. The ledger mechanism itself is fully designed, including two independent adversarial design reviews, but none of that design has been implemented in code.

---

## The problem it is designed to solve

Construction cost control breaks a project into a **cost code** — a numbered work-breakdown structure identifying one kind of work on one project, such as cast-in-place concrete or structural steel erection. Every cost is further split by **cost type** — labour, materials, equipment, and subcontract — because the four behave differently enough that combining them destroys the information an overrun would otherwise reveal.

Underneath the cost code sits the **work package**: a defined piece of physical work carrying two numbers whose relationship is the foundation of the design — a **quantity** (obtained by measuring the drawings) and a **unit factor** (the labour hours to install one unit of that quantity). The quantity sets the labour budget; the quantity actually installed later earns that budget down. Hours worked never draw anything down on their own — they are what the drawdown is measured against.

**Why it matters:** getting this direction backwards is one of the most common real errors in job costing, and it is the specific failure this design is built to prevent structurally rather than by convention.

---

## Earned Value Management and backflush costing

Spending and progress are not the same thing — a project that has spent 60% of its budget may be 30% or 80% complete. The design uses **Earned Value Management**, tracking Planned Value, Earned Value, and Actual Cost as three numbers in the same unit, so that cost efficiency and schedule adherence become leading indicators rather than something only visible after the fact. The design specifically guards against a known failure mode: if earned value were derived from hours spent rather than independently observed installed quantity, the measurement would compare a quantity with itself and could never report a problem — so independently reported installed quantity is treated as mandatory, not optional.

Material consumption is designed around **backflush costing**: rather than tracking every physical movement of material on site, the system is designed to record what was produced and calculate backward what must have been consumed, using a known factor, leaving only the difference against a periodic physical count to investigate. The design specifies that this must be driven by quantity installed, never by hours worked — driving it by hours would let a slow crew appear to have consumed more material than a wall actually contains, confounding a labour signal with a material signal.

**Why it matters:** both mechanisms are designed to turn day-to-day field reporting into an early warning about cost and schedule problems, months before a financial statement would show the same thing.

---

## The ledger design

The design specifies two separate ledgers, denominated differently on purpose. The **production ledger** is designed to hold physical quantities — hours, cubic metres, tonnes. The **cost ledger** is designed to hold dollars, fed only by real payroll and accounts-payable postings, never by converting the production ledger's quantities through a rate. A lump-sum subcontractor's obligation is a function of the contract and the percentage certified complete, not of the hours their own crew worked — two ledgers are designed to keep that case honest, rather than forcing an invented dollar figure or an hours-based approximation.

The two ledgers are designed as named projections of one journal, not separate books — an approach with production precedent (SAP's own Material Ledger was eventually folded into a single Universal Journal). Within that one journal, the design specifies that different kinds of quantity — hours and cubic metres, for example — are never summed together; an entry posting in more than one unit is designed to be checked unit by unit, with each unit's side required to balance independently.

**Why it matters:** the design is intended to let one real-world event, such as a day's work reported, post correctly across several different units at once in a single atomic entry, without ever forcing incompatible quantities into one number.

---

## Holdback, the lien period, and statutory clocks

Construction contracts are subject to statutory holdback (retainage) — a defined percentage of every certified payment withheld by the owner, released once a lien period during which unpaid suppliers can register a claim against the building expires with no claims registered. The design accounts for three consequences this creates: holdback applies against a certified payment application as a whole, not just against subcontract work; different kinds of work carry different lien periods, so parties on the same project become releasable on different dates; and the relevant statutory clocks run in working days, not calendar days, making a correct working-day calendar a legal requirement of the software rather than a scheduling convenience.

---

## Product topology and the free/paid boundary

`tool-construction` is designed as one component in a larger family: the construction ledger itself; the sibling accounting engine, [[tool-accounting]], which is designed to receive a one-way feed of dollar cost from it; `tool-typeset`, a zero-dependency document renderer shared with the accounting engine; and the proposed [[tool-payroll]] engine, which is designed to receive a one-way feed of hours and labour class from the construction ledger as timecards.

The platform's archive substrate and terminal are free (Apache-2.0); cross-archive aggregation is the paid boundary that applies platform-wide. `tool-construction` is designed as a separate, second commercial surface on top of that — what would be sold is the domain engineering itself (the quality-scoring schema, the earned-value mathematics, the ledger mechanism), not a markup on infrastructure that is already free.

The platform's distribution rules classify `tool-*` components as internal operator tooling not distributed as a standalone product by default, with exceptions granted individually — `tool-wallet` is the one existing precedent. **No distribution exception is currently recorded for `tool-construction`.**

## Licensing

`tool-construction` is licensed under FSL-1.1-ALv2.

---

## What is not yet built

Nothing described above as "designed" has pipeline logic written. Specifically not yet built: the ledger engine itself (postings, materials, labour, equipment, subcontracts, change orders, holdback); the archive storage adapter that would let a construction archive persist ledger data through the platform's own record store; a dedicated construction-domain archive (none has been provisioned); the sale-transition access-transfer mechanism; and the two proposed terminal screens (a ledger table view and a work-package/quality panel), neither of which has been granted a build slot on the platform's fixed twelve-function-key terminal.

Open design questions that remain genuinely unresolved include where the engine executes in a multi-archive case, whether individual-performance scoring belongs inside this system or stays a separate concern, whether quality sign-offs need cryptographic signing given their potential legal weight in a defect claim, and what triggers and authorizes the sale-transition access transfer described above and interfaces with a real legal closing process.

## See also

- [[tool-accounting]] — the sibling accounting engine that receives a one-way cost feed from this ledger
- [[tool-payroll]] — the proposed payroll engine that receives a one-way timecard feed from this ledger
