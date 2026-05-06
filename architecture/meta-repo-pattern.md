---
schema: foundry-doc-v1
title: "The Meta-Repo Pattern"
slug: meta-repo-pattern
category: architecture
type: topic
quality: published
short_description: A lightweight repository sitting above project code that provides agents with shared context without coupling git histories — the structural pattern that organises the Foundry workspace and its per-project cluster directories.
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: meta-repo-pattern.es.md
---

A **meta-repo** is a repository that sits above project code, provides shared context — rules, doctrine, identity, tooling — to every project below it, and keeps project histories independent. No Git histories are coupled; each project retains its own `.git/` directory and its own release cycle. The meta-repo enables coherent multi-agent workflows by giving every session the context it needs to navigate many projects without that context living in any one of them.

The Foundry workspace implements this pattern. The workspace directory is the meta-repo. It holds the constitutional charter, the operational guide, shared conventions, the citation registry, the identity store, shared tooling scripts, and the overall project-clone manifest. Every engineering repository below the workspace has its own independent `.git/`.

## Three layers

The Foundry workspace has three structural layers:

```
~/Foundry/                              ← meta-repo (workspace tier)
   ├── DOCTRINE.md                          shared context
   ├── CLAUDE.md                            shared rules
   ├── conventions/                         shared conventions
   ├── citations.yaml                       shared citation registry
   ├── identity/                            shared identity store
   ├── bin/                                 shared tooling
   │
   ├── vendor/<repo>/                   ← upstream repos (engineering tier)
   ├── customer/<repo>/                     each with independent .git/
   │
   └── clones/<cluster>/                ← sub-meta-repos (cluster tier)
       ├── .claude/manifest.md              cluster-level shared context
       ├── .claude/inbox.md / outbox.md     cluster-level mailbox
       └── <sub-clone-1>/                   independent .git/
           <sub-clone-2>/                   independent .git/
```

The cluster directory is itself a meta-repo: a parent containing one or more sub-clones, each with its own `.git/`, sharing context through the cluster manifest and the cluster mailbox. Single-clone clusters are the N=1 case. Multi-clone clusters allow a single Task session to make coordinated changes across multiple repositories in one session.

## The only hard rule

The constraint that makes the pattern work is the `.git/index` race: two sessions writing to the same `.git/index` race and can corrupt each other's staged changes. Two sessions in different `.git/` directories do not race.

Therefore:
- One Master session per workspace meta-repo
- One Root session per upstream repository
- One Task session per cluster directory, writing to one sub-clone's `.git/index` at a time

Multiple Task sessions across different clusters are safe because each cluster's sub-clones have their own `.git/`. A Task session writing to multiple sub-clones of one cluster serially is also safe — they are separate `.git/` directories.

## Session roles and scope

The meta-repo pattern maps directly to the three Claude session roles:

**Master** — operates in the workspace meta-repo. Writes workspace-level documents, the identity store, workspace tool scripts, and the project-clone manifest. Maintains the workspace Git repository and creates new cluster directories. Does not write feature code inside any cluster clone.

**Root** — operates in an upstream repository root. Writes that repository's CLAUDE.md, project registry, cleanup log, and GUIDE files. Maintains the main branch of that specific repository. Does not operate at workspace level.

**Task** — operates in a per-project cluster directory under `clones/`. Writes feature code on the cluster's declared sub-clones, per-project CLAUDE.md and NEXT.md files, the cluster mailbox, and commits on the cluster's feature branch. Also owns deployment provisioning for deployment instances associated with its cluster. Does not write workspace-level or upstream-repo-level files.

The role is determined by the directory a session starts in. It is not chosen or reassigned mid-session.

## Cluster manifest schema

Every cluster directory carries a manifest at `.claude/manifest.md` declaring the cluster name, branch, state, the list of sub-clones with their upstream repos, and the four-leg tetrad (vendor, customer, deployment, and wiki TOPIC contributions) required by Doctrine claim #37.

```yaml
---
schema: foundry-cluster-manifest-v1
cluster_name: project-example
cluster_branch: cluster/project-example
created: 2026-04-26
state: active
clones:
  - repo: pointsav-monorepo
    role: primary
    path: pointsav-monorepo/
    upstream: vendor/pointsav-monorepo
---
```

Master creates the cluster directory and manifest. Task occupies it. Master never edits feature code inside a clone; Task never edits the workspace-level manifest.

## Why the pattern is the right shape

The meta-repo preserves the Action Matrix roles at every layer. No layer is collapsed and no layer is bypassed. Work that belongs at the engineering tier stays there; workspace governance stays in the workspace. The handoff pattern handles cross-repo file moves without requiring a session to hold simultaneous write access to two independent `.git/` directories.

For clusters that work across multiple repositories — for example, a cluster whose vendor leg is in the monorepo and whose customer leg is in a fleet-deployment catalog — the multi-clone variant allows one Task session to commit to both repositories serially without the concurrency hazard of two independent Git sessions.

## See Also

- [[compounding-doorman]] — the inference boundary that Task sessions route through when querying the SLM
- [[apprenticeship-substrate]] — how Task session commits feed the training corpus
- [[knowledge-commons]] — the public-side artifacts the workspace meta-repo publishes per Doctrine MINOR bump

## References

1. Meta-Repo Pattern — 2026 industry vocabulary; Mars meta-repo precedent.
2. Augment Code 2026 Multi-Agent Workspace Guide.

---

## Provenance

Source material: `conventions/meta-repo-pattern.md` (ratified 2026-04-26, doctrine v0.0.2). Disciplines applied: no body H1; structural positioning; BCSC framing not required (no forward-looking commercial claims); banned-vocabulary pass; workspace-internal file paths adapted to be general where internal context is not needed for understanding.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
