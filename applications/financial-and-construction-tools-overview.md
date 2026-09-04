---
schema: foundry-doc-v1
title: "The financial and construction tool family — a shared design across three products"
slug: financial-and-construction-tools-overview
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
paired_with: financial-and-construction-tools-overview.es.md
short_description: "How tool-accounting, tool-construction, and tool-payroll relate as one product family — a shared double-entry design, one-way data feeds between them, and a shared free/paid architecture boundary."
cites: []
---

[[tool-accounting]], [[tool-construction]], and [[tool-payroll]] are three separate products that share one design lineage rather than three independent tools that happen to sit near each other. This article covers what they share and how they connect; each tool's own article covers its own domain in depth.

## One double-entry design, three domains

All three tools are built on, or designed around, the same double-entry ledger discipline: every posting is a balanced entry, nothing is stored that can be derived from what is already recorded, and a full, tamper-evident history of every entry is kept rather than overwritten. `tool-accounting` applies this discipline to financial statements. `tool-construction` applies the identical discipline to physical construction quantities alongside dollars, in a two-ledger design (a production ledger for quantities, a cost ledger for dollars) built specifically because construction cost tracking needs both at once. `tool-payroll` is designed to apply the same underlying discipline to gross-to-net pay calculation and statutory remittance timing.

**Why it matters:** a shared design means a fix or an improvement to the underlying ledger mechanics is intended to benefit all three tools, not just one, and a developer or auditor who understands one tool's ledger model already understands the shape of the other two.

## How data moves between them — one-way feeds only

The three tools are designed to connect through one-way data bridges, never a shared table and never a value converted back to its source:

- **`tool-construction` → `tool-accounting`**: dollar cost, feeding the owner's financial statements as construction-in-progress.
- **`tool-construction` → `tool-payroll`**: hours and labour class, feeding payroll as timecards. This bridge is designed to run one way only — dollars come back only as ordinary payroll and payable postings into the construction cost ledger, through the same review path as any other source transaction, never as an automatic conversion of hours through a rate. That gap between an hours-times-rate estimate and real payroll dollars is a deliberate design feature, not an omission: it is the labour rate variance, and closing the loop automatically would destroy the very signal it exists to surface.

**Why it matters:** an owner or auditor evaluating these tools together does not need to reconcile numbers between them by hand — the one-way design means each tool's own ledger stays the authoritative source for its own domain, and every other tool receives it as a dated input, never as a shared mutable value.

## Shared free/paid architecture boundary

All three tools sit on the same underlying platform architecture: the archive substrate and the terminal that hosts them are free (Apache-2.0); cross-archive aggregation — the one capability an isolated archive genuinely cannot perform for itself — is the platform-wide paid boundary. Each of the three tools is designed as its own separate, additional commercial surface on top of that shared boundary, selling the domain engineering itself (the accounting engine, the construction ledger mechanics, the payroll calculation engine) rather than a markup on infrastructure that is already free to run.

## Licensing

`tool-accounting`, `tool-construction`, and `tool-payroll` are licensed under
AGPL-3.0-or-later. A separate PointSav-Commercial license is available as a paid
alternative for anyone who needs to distribute a modified version, or offer it as a
network service, without the copyleft obligation.

## Build status, side by side

| Tool | Real state today |
|---|---|
| `tool-accounting` | Furthest along: `tool-accounting-core` and `tool-typeset` are real, built, and verified end to end against a real historical fiscal year — journals, ledger, trial balance, and rendered statements. The consolidation fold, subsidiary journal data, and interim (quarterly) rendering are now real; non-wholly-owned consolidation, mid-year entry/exit, and opening balances remain unbuilt. |
| `tool-construction` | A real pilot CLI (`tool-construction-tco-26`) renders four real reports — a cost estimate, a critical-path schedule, a materials listing, and a monthly status report — against a registered pilot site's real work-package data. The dollar-side cost ledger, actual-cost reporting, and the working-day statutory-clock model remain unbuilt. |
| `tool-payroll` | One real report exists: a division-level Payroll Register aggregating the construction pilot's budgeted labour hours under a single, cited jurisdiction's wage-rules row (an explicit pilot scope, not platform coverage). Gross-to-net pay, pay frequency, and remittance computation remain design-only. |

**Why it matters:** the three tools are frequently discussed together because of their
shared design, but they are not at the same stage of readiness — each has at least one
real, running report today, but none is complete platform coverage, and nothing in any of
the three should be read as production-ready software.

## See also

- [[tool-accounting]]
- [[tool-construction]]
- [[tool-payroll]]
