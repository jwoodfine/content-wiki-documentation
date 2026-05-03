---
schema: foundry-doc-v1
title: "Project Tetrad Discipline"
slug: project-tetrad-discipline
category: reference
type: topic
quality: published
short_description: The four-leg structural rule every project cluster must satisfy — vendor code, customer runbook, deployment instance, and wiki TOPIC contribution.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: project-tetrad-discipline.es.md
---

Every active project cluster in the PointSav engineering framework must satisfy four structural requirements before a milestone is ratified. These four requirements — known collectively as the Project Tetrad Discipline — ensure that each cluster produces vendor-tier source code, customer-facing operational runbooks, a working deployment instance, and a public knowledge contribution to the documentation wiki. Clusters that omit any leg silently fail ratification regardless of how complete the other three are.

## Origin

The Tetrad was introduced in Doctrine version 0.0.10 as an upgrade to the earlier Project Triad Discipline, which required three legs — vendor, customer, and deployment. The Triad ensured that clusters shipped complete software products: code without runbooks, runbooks without code, and either without a tested runtime were all made structurally impossible. The Tetrad extends this same forcing function to public knowledge accumulation by adding a fourth mandatory leg.

Without a knowledge leg, TOPIC contributions to the documentation wiki accumulate incidentally rather than as a structural consequence of every milestone. The Reverse-Funnel Editorial Pattern — the editorial pipeline that processes raw drafts into published wiki content — is starved of bulk input when knowledge production is optional. The Tetrad closes this gap by making a wiki TOPIC contribution path as mandatory as shipping code.

## The four legs

**Vendor leg.** At least one engineering sub-clone drawn from a vendor-tier canonical repository. This is where source code lives. Task-layer session commits land here on the cluster's feature branch and advance toward the canonical repository through the staging-tier promotion path.

**Customer leg.** At least one operational runbook contribution path to a fleet-deployment catalog subfolder. Runbooks describe how to install, configure, operate, and recover the deployment. They are written for the operator role rather than the software engineer, and they advance the catalog entry that corresponds to the cluster's deployment shape.

**Deployment leg.** At least one numbered runtime instance under the deployment instances directory. The instance carries a manifest declaring its tenant, purpose, source version, and current state. Runtime state is local-only and never published to a version-control remote. This is where the cluster's vendor and customer legs are actually run end-to-end against real conditions.

**Wiki leg.** At least one TOPIC contribution path to the documentation wiki. Task sessions stage draft TOPIC files in their cluster's drafts-outbound directory. The project-language editorial gateway sweeps those drafts, refines them to the required register — Bloomberg-standard prose, BCSC-compliant forward-looking framing, resolved citation identifiers, and bilingual pairs — and routes refined output to the content-wiki-documentation repository for publication.

## Declaring the tetrad

Each cluster's manifest file carries a `tetrad:` field with at least one entry under each leg. Legs that are not yet active are declared `leg-pending` with a concrete plan and a target date. A leg may not be silently absent. The distinction between `leg-pending` and absent is the difference between a planned commitment and an oversight.

## Master ratification

The workspace's Master-layer session ratifies milestone work by checking all four legs. A milestone passes ratification when: each leg is declared in the manifest; each leg is either active, completed, or `leg-pending` with a concrete plan; and the current milestone's commits include contributions to at least three of the four legs. Deployment-only milestones and editorial-sweep milestones are each permitted to contribute to a subset, but no leg may be silently omitted from the manifest.

## Relationship to earlier conventions

The Tetrad supersedes the Project Triad Discipline for all clusters created or upgraded after Doctrine version 0.0.10. Clusters that predate the Tetrad carry a `triad:` field and receive a broadcast to their inbox asking them to amend the manifest and add an initial wiki-leg entry. Prior milestones ratified under the Triad remain valid; Tetrad discipline applies from the upgrade commit forward.

## Why the wiki leg compounds

The three-leg Triad ensured that each cluster shipped functional software. The Tetrad additionally ensures that each cluster produces a public record of what it built and why. When the editorial pipeline is operational, these records feed a continued-pretraining corpus that makes the substrate progressively sharper at generating baseline drafts. Creative contributors then refine those published drafts, and their edits become the craft preference signal for the next training cycle. Each cluster milestone that satisfies the wiki leg contributes one iteration of this compounding loop.

## See also

- [[project-triad-discipline]] — The predecessor three-leg convention, now superseded for new work.
- [[reverse-funnel-editorial-pattern]] — The editorial pipeline that processes wiki-leg draft output.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
