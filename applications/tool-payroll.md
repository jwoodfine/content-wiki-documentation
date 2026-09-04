---
schema: foundry-doc-v1
title: "tool-payroll — jurisdiction-aware payroll and statutory remittance"
slug: tool-payroll
category: applications
type: tool
content_type: topic
quality: complete
index_group: financial-and-construction-tools
status: active
audience: vendor-public
bcsc_class: forward-looking
language_protocol: PROSE-TOPIC
last_edited: 2026-09-04
editor: pointsav-engineering
paired_with: tool-payroll.es.md
short_description: "A jurisdiction-aware payroll and statutory-remittance engine whose first real report — a division-level Payroll Register aggregating the construction pilot's budgeted labour hours under a cited single-jurisdiction wage-rules row — is built and running; gross-to-net pay, pay frequency, and remittance computation remain design-only."
cites: []
---

`tool-payroll` is a payroll engine in its earliest real build-out, designed to
handle the statutory side of paying a worker: how often a worker is paid, when
a computed pay date is legally permitted to fall, and how paying someone
relates to remitting statutory deductions to the correct authority. It is a
sibling product to [[tool-accounting]], not a feature of [[tool-construction]]
— cross-domain rather than construction-specific — and is intended to receive
timecards from both of those tools as one-way feeds.

**What exists today.** One real report exists, and only one. A pilot binary
crate — scaffolded alongside the construction toolchain's own pilot crates,
which is where the engine's development now lives — reads the budgeted labour
hours and crew assumptions the [[tool-construction]] pilot already maintains,
plus the one-row, single-jurisdiction wage-rules table described below, aggregates them into
division-level labour totals, and renders a Payroll Register (by Division) as
HTML and PDF through `tool-typeset`, the same shared renderer the sibling
engines use. It is a single command with no flags or arguments, and its tests
pass. The boundary is just as real: pay frequency, gross pay, and net pay are
computed nowhere — the register prints an em dash in those columns rather than
a fabricated number — and no timecard or payroll transaction has ever been
recorded. Everything else this article describes remains design.

---

## The problem it is designed to solve

A tradesperson who expects to be paid at the end of the day or the end of the
week, rather than on a standard biweekly cycle, is a real operational
requirement. Handling it correctly means keeping two facts that are easy to
conflate cleanly separate: how often a worker is paid, and how often the
employer must remit withheld statutory deductions to the tax authority. A
platform that quietly assumed these were the same clock would compute correct
paycheques and file incorrect remittances, or the reverse — the exact failure
mode this design exists to prevent.

**Why it matters:** an employer who pays trades daily does not, in most cases,
have to remit to the tax authority daily — but the platform still has to know
the difference, or it will eventually get one of the two wrong.

---

## The Payroll Register — the one real report

The engine's first shipped output is a single document: the Payroll Register
(by Division), a working schedule of budgeted labour — not a filed statement,
and not a pay run. The pilot binary reads three sets of plain files: the
construction pilot's own cost-code-to-division crosswalk and crew assumptions,
its real work-package data, and the wage-rules table below. It joins each cost
code to its construction-industry division, aggregates budgeted labour hours
and crew size per division, and renders the register as HTML and PDF.

Two properties are worth stating. First, the hours aggregation deliberately
mirrors, step for step, the logic the construction pilot's own monthly status
report uses for its man-hours figures — the same underlying numbers, computed
the same way, so the two documents can never silently diverge. The read is
file-based on purpose: no code dependency exists between the two pilot crates,
only files, matching the one-way feed discipline of the design. Second, the
register's Pay Frequency and Gross Pay columns print an em dash on every row,
and its own basis-of-preparation note says why: those numbers do not exist
anywhere — pay frequency has no designed data home yet, and gross-to-net
computation is explicitly out of scope — so the register states the gap
instead of showing a plausible figure. The same note prints the jurisdiction
facts the engine resolved from its wage-rules table: the wage-payment ceiling,
the day-counting basis, the remitting authority, and the
workers'-compensation authority, with the row's own source citation.

**Why it matters:** the first thing this engine shipped is its honest
boundary. A reader of the register gets real hours and real crew figures, a
printed statement of which columns are not yet real, and the cited wage-timing
rules that will eventually govern them — never an invented pay number.

**Edge cases:** crew size is optional per division — a division with no crew
assumption prints an em dash there too, never a zero, because a zero crew
would itself be a claim.

---

## Jurisdiction scope — one jurisdiction only, and explicitly a pilot

Every wage-timing and remittance figure lives as a cited row in a
jurisdiction-keyed table — `wage_payment_rules.csv`, now a real file the
running register loads — never a rule hardcoded into engine logic. As of this
writing, only **one jurisdiction row is populated and verified**, matching
the province where the pilot site sits (not named in public content). This
is explicitly a pilot scope, not platform coverage — every other
jurisdiction is a named, unpopulated gap, and an entity whose jurisdiction
has no row is intended to be a refused, visible gap rather than silently
defaulted to the populated row's numbers.

```
wage_payment_rules.csv — real; one populated, source-cited row

jurisdiction_code,max_pay_period_days,max_days_to_pay_after_period_end,
day_counting,remitting_authority,comp_authority,source_ref,effective_from

[jurisdiction],31,10,calendar,CRA,[jurisdiction] WCB,"[jurisdiction wage-payment
statute; federal remitter-type schedule; provincial workers'-compensation
premium mechanics]",
```

The citations ride in the row's own `source_ref` field, so the rule and its
source travel together — a reviewer never has to trust that a number in the
engine matches a rule somewhere else.

**Why it matters:** adding a second province, or a jurisdiction outside
Canada, is planned to mean adding one cited row to a table — not touching
engine code. Whether that plan holds in practice is untested, since no second
jurisdiction row exists yet.

---

## Two independent clocks: pay frequency and remittance frequency

Pay frequency — how often a worker is paid — is designed to be fully
decoupled from statutory remittance frequency, which is the single most
consequential distinction in this design. Pay frequency is intended to be
operator-configured per crew or employee: daily, weekly, bi-weekly, or
semi-monthly, with monthly as an outer bound in the pilot jurisdiction's
cited row rather than a distinct operator choice. Remittance frequency, by
contrast, is an
*employer*-level fact set by the tax authority from trailing withholding
volume — most employers remit monthly regardless of how often they pay staff,
and only the highest-volume employers are required to remit more often as
that volume rises.

The one documented exception: an employer whose trailing withholding volume
crosses a high threshold and who pays staff more than twice a month may be
required to remit on every payday. Short of that threshold, daily or weekly
pay to trades is not, on its own, expected to force daily or weekly
remittance.

**Why it matters:** an employer paying construction trades daily can, at
ordinary payroll sizes, still expect to remit to the tax authority on the
routine monthly schedule — the daily-pay expectation trades make of their
employer and the employer's remittance obligation are two different
questions with two different answers.

---

## The wage-payment ceiling

The pilot jurisdiction's cited rule sets a hard outer limit: a computed pay
date for a given pay period may fall no later than the jurisdiction's stated
number of days after the period ends — ten consecutive calendar days, in the
pilot jurisdiction's cited row. The design intends the engine to refuse, not
silently clamp, any configuration or manual pay-date entry that would
violate this ceiling once resolved from the entity's own jurisdiction row. A
pay run that would land outside the window is meant to surface as a named,
blocking error rather than a warning.

Today the ceiling is data, not enforcement: the running register resolves
the pilot jurisdiction's row and prints the ten-day figure into its own
notes, but no pay date is computed anywhere yet, so the
refuse-rather-than-clamp behavior remains design.

The pilot jurisdiction's own published construction-industry exceptions are
narrow: they cover only how vacation pay and general-holiday pay may be
timed, not a shorter or longer pay period, and not a different
payment-timing rule for trades or day labour generally. Trades are designed
to follow the identical ceiling as any other employee in that jurisdiction's
row — this finding is specific to the pilot jurisdiction and is not assumed
to generalize to any other.

**Why it matters:** a worker's legal right to be paid within a bounded
window after doing the work does not bend for the construction trades, at
least under the pilot jurisdiction's rule — the design treats that as a hard
constraint the engine enforces, not a preference it can override.

---

## Calendar days and working days are never the same clock

The pilot jurisdiction's wage-payment clock counts calendar days. A separate set of clocks,
already real and shipped in [[tool-construction]], counts *working* days
instead — governing holdback release and prompt-payment timing between
contracting parties. These are legally distinct regimes: one governs wages
owed to an employee under employment-standards law, the other governs
progress payments between contracting parties under contract law. The
governing construction-payment statute states directly that its own clocks do
not reduce or alter an employer's wage-payment obligations.

The design treats `day_counting` as its own field on the jurisdiction row —
`calendar` for the pilot jurisdiction's wage clock — rather than a hardcoded constant shared
with any working-day calendar tool-construction already maintains for its own
purposes. A rule that quietly borrowed one clock's day-counting for the other
would be treated as a real compliance defect, not a rounding difference.

**Why it matters:** two different legal deadlines can look like the same kind
of countdown and are not — mixing them up is exactly the class of bug this
design is structured to make structurally hard to write.

---

## Workers'-compensation reporting — a third, independent clock

Workers'-compensation assessable-earnings reporting and premium remittance is
designed as orthogonal to both of the clocks above. The pilot jurisdiction's cited
requirement is an annual payroll estimate plus periodic premium remittance —
monthly, quarterly, or annual, at the employer's choice below a payroll-size
threshold — to the provincial workers'-compensation board. That schedule
does not follow how often, or how quickly, an employer pays its workers.

The design models this as a `comp_authority` field per jurisdiction row —
the pilot jurisdiction's board is the one populated value today; equivalent
boards in other jurisdictions are named-but-unpopulated rows, not assumed to
share its specific mechanics.

**Why it matters:** a payroll platform can get wage timing and tax remittance
both right and still misreport workers'-compensation premiums if it assumes
that clock rides on either of the other two — the design keeps it separate on
purpose.

---

## Calendar and holiday logic

One concrete mechanic is in scope beyond the timing rules above: a computed
pay date that lands on a weekend or statutory holiday is intended to move to
the preceding business day, standard real-world payroll practice. That
requires a jurisdiction-keyed holiday calendar.

The design follows a pattern already established elsewhere on the platform. A
proposed, not-yet-built archive-resident scheduling service is intended to
eventually become the shared, canonical holiday-calendar source across
[[tool-construction]], `tool-payroll`, and [[tool-accounting]]. But
`tool-payroll`'s own holiday-calendar table is designed to work standalone in
flat-file mode first, with no build-time dependency on that shared service.
The convergence point is named as a future intention, not built now.

**Why it matters:** the design is structured so `tool-payroll` can run
correctly on its own, with a folder of data files and no other service
running, while still being able to plug into a shared calendar later without
a redesign.

---

## The bank-connectivity boundary

Whether `tool-payroll` — or anything in its surrounding platform — should
connect to a bank at all is answered narrowly and deliberately. The design
proposes a bounded, read-only ingestion component (working name
`service-bank-feed`, modelled on a real, already-shipped precedent elsewhere
in the platform for pulling data from one named external system) rather than
any broader banking connection. The name itself is a deliberate choice: a
component that could be read as managing a banking relationship was
considered and rejected in favor of one whose name states plainly that it
only pulls a read-only feed.

| Proposed to do | Explicitly out of scope |
|---|---|
| Pull read-only transaction data from one named external bank or aggregator, through a narrow, single-purpose connection | Reach any network endpoint beyond that one integration — no general internet access |
| Parse and normalize the feed into a structured record (date, amount, currency, counterparty, reference) — deterministic only | Classify or interpret a transaction's meaning — that stays a human or a separate classification step |
| Append the normalized record into the platform's append-only ledger | Edit or delete an existing ledger entry |
| Surface the raw, unclassified feed for human review | Auto-reconcile or auto-close a period without human review |
| Hold the minimum credential scope needed for one read-only connection | Initiate a payment, wire, transfer, or bill-pay, or write anything back to the bank |

No write-outward capability to a bank exists anywhere in the current design.
If payment initiation is ever pursued, the intended shape is a generated
payment-instruction file handed to a separately-licensed party — the
employer's own bank or a licensed payment processor — under a maker-checker
approval split, never money movement performed by `tool-payroll` itself.
That shape is named as the correct future direction; it is explicitly not
designed or built in the current pass.

**Why it matters:** the platform is designed so that nothing in this pipeline
can ever move money on its own — every dollar-moving step is planned to stay
in the hands of a separately licensed party, by design rather than by
accident.

---

## Relationship to tool-accounting and tool-construction

`tool-payroll` is designed with two intended feed sources landing in one
destination. [[tool-construction]]'s crew timecards are planned as one feed;
[[tool-accounting]] itself is planned to feed `tool-payroll` directly for an
operator's own non-construction staff, since the gross-to-net computation is
intended to be identical whether the employer is a construction operator or
any other kind of business. Both feeds are designed to land in
`tool-accounting`'s ledger the same way — as ordinary postings, one-way,
through the same review path as any other source transaction.

A precursor of the first feed is now real, and it is deliberately narrower
than the feed the design names: the Payroll Register reads the construction
pilot's *budgeted* work-package hours as plain files. A budget is an
estimate-stage figure; a timecard is an actuals record, and no timecard
exists anywhere in the pipeline yet — the same estimate-stage boundary the
construction engine itself states for its own ledger.

```
tool-construction (hours + labour class)  ──▶  tool-payroll   (feed 1)
tool-accounting (own staff hours)         ──▶  tool-payroll   (feed 2)
tool-payroll (computed dollars)           ──▶  tool-accounting  (ordinary postings)
tool-payroll (computed dollars)           ──▶  tool-construction  (cost ledger, one-way)
```

A cross-project cost aggregator that already exists for the accounting
platform is expected to need no direct connection to `tool-payroll` at all —
it aggregates each entity's already-posted accounting ledger, which already
carries whichever payroll dollars landed there regardless of which feed they
came from. That falls out of the one-way, feed-agnostic design rather than
requiring a separate integration.

Operator screens for timecard and pay-run approval are planned to extend an
existing bookkeeping terminal surface rather than create a new one. The
platform's terminal model favours extending a shared surface over adding a
dedicated screen per tool. This extension is proposed, not yet approved
by the surface's owner.

**Why it matters:** a construction crew and a law firm's own office staff are
intended to be paid through the identical engine — the only thing that
differs is which tool the hours came from.

---

## Licensing

`tool-payroll` is licensed under AGPL-3.0-or-later. AGPL-3.0-or-later is a copyleft
license: the source code is available to everyone, and any modified version — including
one operated as a network service — must be released under the same license if it is
distributed or made available over a network. A separate PointSav-Commercial license is
available as a paid alternative for anyone who needs to distribute a modified version, or
offer it as a network service, without that copyleft obligation.

---

## Status summary

| Component | Status |
|---|---|
| Payroll Register (by Division) — division-level budgeted-hours and crew aggregation, HTML + PDF | **Built and running** — the engine's first real report; a single command with no flags |
| Jurisdiction table (`wage_payment_rules.csv`) | Real — one populated, source-cited row (jurisdiction not named in public content), loaded by the running report. Every other jurisdiction is a named, unpopulated gap |
| Classification and integration contract with `tool-construction` | Locked as a design decision; a file-based read of the construction pilot's budgeted hours is real, but the timecard feed itself is not built |
| Pay-cadence and statutory-timing design (jurisdiction model, the two clocks, the wage-payment ceiling, calendar/working-day distinction, workers'-compensation reporting) | Designed and locked; enforcement not built — no pay date is computed anywhere yet |
| Gross-to-net computation itself (tax brackets, statutory deduction formulas) | Explicitly deferred; not designed |
| Engine and operator-facing crates | First pilot crate scaffolded and running, developed alongside the construction toolchain; a full engine crate does not exist |
| `service-bank-feed` | Proposed; ownership not yet confirmed; no formal proposal sent yet |
| Payment-file generation and maker-checker approval | Named as the intended future shape; not designed or built |
| Bookkeeping-terminal extension for pay-run and timecard approval | Proposed; requires sign-off from the surface's owner |

---

## See also

- [[tool-accounting]] — the sibling product `tool-payroll` is designed to extend; both are planned to share the identical gross-to-net engine regardless of which tool feeds it hours
- [[tool-construction]] — the tool whose crew timecards are designed as one of `tool-payroll`'s two intended feed sources, and whose pilot's budgeted hours the first real report already reads
