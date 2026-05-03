---
schema: foundry-doc-v1
title: "Style Guide — INVENTORY"
slug: style-guide-inventory
category: reference
type: topic
quality: core
short_description: "Editorial standards for INVENTORY.md files in Foundry fleet-deployment repos and aggregator directories, covering required sections, the table-first discipline, and the operational register."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: style-guide-inventory.es.md
---

> An `INVENTORY.md` catalogs contained sub-artefacts in a scannable table — a summary count followed by one row per item, with prose kept outside the table cells.

An **INVENTORY.md** is a catalog document. It is the answer to
the question "what is in this directory?" rather than "what
does this project do?" — that answer belongs in the README.
Inventory files are common in fleet-deployment repos
(`woodfine-fleet-deployment`, `pointsav-fleet-deployment`) and
in aggregator directories that contain multiple deployment
instances, named artefacts, or registered items. The
machine-readable counterpart lives in
`service-disclosure/templates/inventory.toml`.

## When to use this template

Use the inventory template when a directory contains a
collection of named sub-artefacts that a maintainer needs to
survey at a glance. Common cases:

- A fleet-deployment catalog directory containing multiple
  deployment subfolders — the inventory names each subfolder,
  its state, and its tenant.
- A deployment instance containing multiple registered items
  such as loaded templates, active configurations, or staged
  data files.
- An aggregator at a repo root that collects items from multiple
  contributing sources.

Do not use an inventory file as a substitute for a README or
an `ARCHITECTURE.md`. An inventory answers "what is here"; it
does not answer "why this exists" or "how it is organised".

## Frontmatter fields

`INVENTORY.md` files do not carry YAML frontmatter. The
template describes a plain Markdown file. No citation-substrate
fields are required.

## Structure

The template requires two sections:

| Section | Purpose |
|---|---|
| **Summary** | A short prose block and a count rollup. States the total number of items, their breakdown by state or type, and any notable conditions. Two to four sentences. |
| **Catalog** | One Markdown table row per artefact. Each row names the item, its state, its tenant or owner, and any brief notes needed for the reader to act. |

The Catalog table is the primary content. Column names depend on
the artefact type but always include the canonical item name and
its current state. Do not crowd the table with prose
explanations; notes columns should be short phrases, not
sentences.

Prose explanation belongs outside the table: in the Summary, or
in a brief paragraph between the Summary and the Catalog when
there is context that applies to multiple rows.

## Register and tone

The register is operational. Sentence-length budget: mean around
sixteen words, maximum around twenty-eight, applied to the prose
sections. Table cells are shorter: five to ten words per cell,
enough to be clear, not a sentence.

Canonical names from the Nomenclature Matrix are used in the
Name column. No paraphrases; no legacy prefixes. State values
come from the defined state vocabulary for the artefact type:
for deployment instances, the state vocabulary is
`active`, `dormant`, `decommissioned`; for projects, it follows
the project-lifecycle vocabulary at `~/Foundry/CLAUDE.md` §9.

The banned-vocabulary list applies. An inventory table cell that
says "robust configuration" says nothing. Name the specific
configuration state or version.

## Example

```markdown
## Summary

This deployment catalog contains 4 registered deployment
subfolders: 2 active, 1 dormant, 1 pending provisioning.
All four target the Woodfine Management tenant.

## Catalog

| Deployment name | State | Tenant | Notes |
|---|---|---|---|
| cluster-totebox-corporate-1 | active | woodfine | Serving production traffic |
| cluster-totebox-property-1 | active | woodfine | Read-only access until Q3 |
| media-knowledge-documentation-1 | dormant | woodfine | Awaiting DNS cutover |
| route-network-admin-1 | pending | woodfine | Instance directory created; not provisioned |
```

## See also

- [[style-guide-changelog|Style Guide — CHANGELOG]]
- [[style-guide-readme|Style Guide — README]]
- [[style-guide-architecture|Style Guide — ARCHITECTURE]]

## References
