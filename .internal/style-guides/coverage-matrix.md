---
schema: foundry-doc-v1
title: "Coverage matrix — every prose artifact maps to one guide"
slug: coverage-matrix
category: internal
type: reference
content_type: reference
quality: complete
status: active
audience: contributor
bcsc_class: public-disclosure-safe
last_edited: 2026-07-01
editor: pointsav-engineering
---

> Proves the style-guide set covers every prose-bearing artifact type in the workspace with the
> fewest guides. Source of truth for the taxonomy: `conventions/artifact-classification.yaml`
> (and `artifact-registry.md`). Each prose artifact maps to exactly one register guide. The
> three house profiles are audience specializations of the reference guide, not extra registers.

## Covering set — five register guides

| Guide | Register / Diátaxis type | Governs (artifact types) |
|---|---|---|
| **reference** | Encyclopedic reference + explanation; neutral | PROSE-TOPIC, PROSE-ARCHITECTURE, PROSE-RESEARCH, PROSE-TEXT, PROSE-README, PROSE-INVENTORY, changelog, DESIGN-RESEARCH |
| **how-to** | Operational / procedural; Diátaxis how-to | PROSE-GUIDE, RUNBOOK, PROSE-DIRECTIVE |
| **communications** | Institutional communications | COMMS-ANNOUNCEMENT, COMMS-PRESS, COMMS-CORPORATE, COMMS-EMAIL, COMMS-NOTES, PROSE-MEMO, chat, ticket-comment |
| **legal** | Plain-language legal / governance | LEGAL-MANIFEST, LEGAL-DISCLAIMER, LEGAL-CORRECTIONS, contract, CLA, terms, policy, license-explainer |
| **journal** | Academic prose; peer-reviewed / self-published complete-idea papers | JOURNAL |

Three **house profiles** — `documentation`, `corporate`, `projects` — specialize the reference
guide for each wiki's audience and subject. They govern the wiki TOPIC/GUIDE/ARCHITECTURE work
and point back to the reference and how-to guides for craft.

## Full artifact enumeration (from artifact-classification.yaml)

| Artifact type | Prose? | Assigned guide |
|---|---|---|
| PROSE-TOPIC (TOPIC-) | yes | reference (+ wiki house profile) |
| PROSE-ARCHITECTURE | yes | reference (+ documentation profile) |
| PROSE-GUIDE (GUIDE-) | yes | how-to (+ documentation profile) |
| RUNBOOK- | yes | how-to |
| PROSE-DIRECTIVE | yes | how-to |
| PROSE-RESEARCH | yes | reference |
| PROSE-TEXT (TEXT-) | yes | reference |
| PROSE-README | yes | reference |
| PROSE-INVENTORY | yes | reference |
| PROSE-MEMO | yes | communications |
| changelog | yes | reference |
| COMMS-ANNOUNCEMENT / -PRESS / -CORPORATE / -EMAIL / -NOTES | yes | communications |
| chat, ticket-comment | yes | communications |
| JOURNAL- | yes | journal |
| LEGAL-MANIFEST / -DISCLAIMER / -CORRECTIONS | yes | legal |
| contract, CLA, terms, policy, license-explainer | yes | legal |
| TRANSLATE-ES | yes | governed by the source artifact's guide + the bilingual-adaptation note in house-core |
| DESIGN-RESEARCH | yes | reference |
| DESIGN-COMPONENT | microcopy only | out of scope — UI/ARIA text owned by project-design accessibility docs |
| DESIGN-TOKEN-* / DESIGN-WIREFRAME / ASSET | no | out of scope — visual/binary |
| BIM- | yes, but foreign gateway | adopts the reference guide; owned by project-bim (bim.woodfinegroup.com) |
| LICENSE- | standard text | out of scope as authored prose — canonical licence files; the *explanation* of a licence is `license-explainer` → legal |
| CODE-, SOFT-, DATA-, SCRIPT-, CONFIG- | no | out of scope — code / data / binary |
| CONVENTION-, DOCTRINE-AMENDMENT- | yes, governance prose | adopt the reference guide's craft; owned by Command Session (workspace docs), not published |

## Gaps and decisions

- **No prose artifact type is left ungoverned.** Every `yes` row maps to exactly one guide.
- **JOURNAL is its own register — reversal, 2026-07-01.** The earlier decision kept JOURNAL
  inside the reference guide as an academic-variant section to hold the set minimal; that is
  reversed as of 2026-07-01, because a JOURNAL is a distinct kind — a complete idea argued end
  to end for an external venue, not a lookup artifact. Its extra discipline (literature review,
  external submission, natural-person authors) still lives in
  `conventions/journal-artifact-discipline.md`, which the journal guide points to.
- **TRANSLATE-ES** is not a register — a translated artifact follows its source artifact's guide
  plus the shared bilingual-adaptation note, so it needs no guide of its own.
- **CONVENTION / DOCTRINE-AMENDMENT** are governance prose owned by the Command Session; they
  adopt the reference guide's craft but are not part of the published bundle set.
