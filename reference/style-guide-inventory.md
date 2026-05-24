---
schema: foundry-doc-v1
title: "Style guide — inventory"
slug: style-guide-inventory
category: reference
type: topic
quality: complete
short_description: "Editorial standards for inventory documents (PROSE genre) in the platform: table discipline, classification vocabulary, state enumeration, and when an inventory is the right artifact over a registry or brief."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-24
editor: pointsav-engineering
cites: []
paired_with: style-guide-inventory.es.md
---

> An inventory is a timestamped count of what exists, what state it is in, and what type it is. It is not a plan and not a log.

An **inventory** (PROSE genre) is a point-in-time enumeration of items in a defined scope, organised to support classification and action. It differs from a registry (which is authoritative and updated continuously) and from a brief (which carries analysis and recommendation). An inventory is read; a registry is queried. This article is the human-facing standard; the machine-readable counterpart lives in `service-disclosure/templates/inventory.toml`.

## When to use this template

Use an inventory when:

- A count is needed to understand the size of a migration, cleanup, or audit task.
- Items need to be classified and the classification itself is the deliverable.
- A snapshot is required before a structural change so the before-state is recorded.

Do not use an inventory as a living document. Inventories are snapshots — they carry a date, go stale, and are superseded by a new inventory when the scope changes materially. A living record belongs in a registry or a cleanup log.

## Structure

The template requires three sections:

| Section | Purpose |
|---|---|
| **Opening** | One paragraph: what scope was inventoried, as of what date, and what the count reveals at high level. |
| **Inventory table** | The enumeration. Columns: `Item` (canonical name), `State` (closed enum), `Type` (closed enum), `Notes` (short, max one clause). |
| **Summary** | Counts by state and type. Totals. May include a "next action" pointer if the inventory is the input to a migration or audit. |

An optional **Classification vocabulary** section follows the table when the State and Type enumerations are not self-evident. Define each value in one phrase.

## Inventory table discipline

- One row per item. No merged cells.
- `State` values come from a closed enum per domain (for example, `open | closed | deferred` for cleanup items; `active | dormant | archived` for projects).
- `Type` values come from the relevant taxonomy (Nomenclature Matrix entity types, genre families, etc.).
- Notes column: one clause maximum. If more than one clause is needed, the item requires its own entry in the cleanup log or brief.

## Register and tone

Factual. No interpretation in the table — the rows are observations, not recommendations. The opening paragraph may describe what the pattern suggests; the table itself does not.

Dates are ISO 8601. Canonical names from the Nomenclature Matrix throughout. No prose in the table beyond the Notes column.

## See also

- [[style-guide-readme|Style Guide — README]]
- [[style-guide-memo|Style Guide — Memo]]
- [[language-protocol-substrate|Language Protocol Substrate]]
