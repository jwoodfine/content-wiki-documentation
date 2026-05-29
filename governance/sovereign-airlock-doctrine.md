---
schema: foundry-doc-v1
title: "The sovereign airlock"
slug: sovereign-airlock-doctrine
category: governance
type: topic
quality: complete
short_description: "The sovereign airlock is the staged-commit protocol that enforces a hard separation between work-in-progress staging identities and canonical repository identities — two staging authors for all commits, two admin identities for canonical pushes, with no direct path between them."
status: active
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: sovereign-airlock-doctrine.es.md
---

The **sovereign airlock** is the commit and deployment protocol that enforces a structural separation between the identities that write work and the identities that publish it to canonical repositories. No commit author has direct push access to a canonical repository. No canonical push identity is a commit author. The two roles are cryptographically separate: a session that writes code cannot push without routing through the explicit Stage 6 promotion step, and the promotion step cannot be performed by the same identity that made the commit. This is not a policy enforced by tooling configuration — it is a structural impossibility, because the commit-author key and the push key are held by different identity directories.

## The four identities

The platform's identity store defines four named identities, each backed by a dedicated SSH key stored in an operator-controlled directory that no session can read or modify directly:

| Identity | Key | Role | Scope |
|---|---|---|---|
| `jwoodfine` | `id_jwoodfine` | Staging — Jennifer | All commits across engineering repos |
| `pwoodfine` | `id_pwoodfine` | Staging — Peter | All commits across engineering repos |
| `ps-administrator` | `id_pointsav-administrator` | Push-only | Canonical `pointsav` org on GitHub |
| `mcorp-administrator` | `id_woodfine-administrator` | Push-only | Canonical `woodfine` org on GitHub |

The staging identities (`jwoodfine`, `pwoodfine`) are used exclusively through the platform's commit tooling. Their keys are held in the operator-controlled identity store and are never elevated to push rights on canonical repositories. The admin identities hold push rights to canonical repositories but are never used as commit authors.

## The commit flow

Work moves through three tiers:

```
Staging tier (jwoodfine, pwoodfine commits)
       │
       │ Stage 6 promotion — operator-initiated, admin identity only
       ▼
Canonical vendor tier  (pointsav/* — push via ps-administrator SSH alias)
       │
       │ Release engineering governance
       ▼
Canonical customer tier  (woodfine/* — push via mcorp-administrator SSH alias)
```

The commit tooling alternates authorship between `jwoodfine` and `pwoodfine` on successive commits. The promotion step packages staged commits and pushes to the appropriate canonical remote using the admin identity's SSH alias. The admin identities' keys are configured for push authentication only; they do not appear as commit authors in the repository log.

## The structural guarantee

The airlock's guarantee is not "users are unlikely to push directly" but rather "direct pushing is structurally impossible from a staging session." A staging session that issues a push command targets the staging remote, not the canonical repository. Reaching the canonical repository requires the admin SSH alias, which requires the admin key, which requires the operator to explicitly initiate the Stage 6 promotion step.

This separation serves two functions for regulated operators. First, it makes the staging tier a genuine review boundary: promoted commits carry implicit sign-off that the operator reviewed the work before authorising the canonical push. Second, it keeps the commit history clean — every commit in the canonical repository was authored by a known staging identity, reviewed at a known point in time, and promoted by a deliberate operator action, consistent with the [[legal-and-ip-structure|squash-and-merge IP-transfer mechanic]].

## Key custody discipline

All four keys reside in the operator-controlled identity directory at permissions `0600`, accessible only to the system user that owns the workspace. Session tooling reads keys from this directory; no key is copied into a repository or exported to a session environment. A pre-commit hook blocks commits containing key material, enforcing the custody rule at the technical layer rather than the policy layer. The same boundary discipline extends to [[api-key-boundary-discipline|AI inference credentials]], which are held exclusively at the gateway and never at inference engines.

## See also

- [[pairing-as-permission]] — the cryptographic pairing pattern that governs which nodes can connect
- [[machine-based-auth]] — the platform's machine-based authentication protocol
- [[api-key-boundary-discipline]] — the same key-separation discipline applied to AI inference credentials
- [[legal-and-ip-structure]] — the IP-transfer mechanic that depends on this commit-flow separation
- [[single-boundary-compute-discipline]] — the AI inference boundary that the same key-separation discipline enforces at the model layer
