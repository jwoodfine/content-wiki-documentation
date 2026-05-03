---
schema: foundry-doc-v1
title: "Style Guide — GUIDE"
slug: topic-style-guide-guide
category: reference
type: topic
quality: core
short_description: "How to write a GUIDE file: the operational runbook format used inside Foundry deployment subfolders, covering required structure, voice, command formatting, and the distinction from TOPIC files."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: topic-style-guide-guide.es.md
---

# Style Guide — GUIDE

> A GUIDE file is the operational runbook format for Foundry deployment subfolders — how to run, configure, or recover from failure — and is distinct from a TOPIC, which explains what something is and why.

A **GUIDE** file (`guide-<subject>.md`) is an operational runbook —
how to run, configure, or recover from failure. It tells the
operator what to do, in order, with the commands they will copy
and paste. It is not an explanation of why something works; that
reasoning belongs in a TOPIC, covered in
[[topic-style-guide-topic|Style Guide — TOPIC]]. Every GUIDE
lives inside the deployment subfolder it operates; a GUIDE that
appears at a catalog root without a containing subfolder is
misplaced and must be moved.

## Where GUIDEs live

GUIDEs live inside the deployment subfolder they operate. There
are two tiers:

| Tier | Path shape | Purpose |
|---|---|---|
| **Catalog** | `customer/woodfine-fleet-deployment/<deployment-name>/GUIDE-*.md` | Defines how this deployment-name is operated. Every catalog entry that is operationally meaningful carries at least one. |
| **Instance** | `~/Foundry/deployments/<instance>/GUIDE-*.md` | Variation only when an instance has operationally significant deviations from its catalog GUIDE. |

A GUIDE at a fleet-deployment catalog *root* (no containing
deployment subfolder) is misplaced. The workspace
`~/Foundry/CLAUDE.md` §14 names this as drift; move into the
owning deployment subfolder.

## English only

GUIDE files are English-only. They are operational, not
public-facing — bilingual pairs add maintenance cost without
benefit, because the audience is operators with English working
proficiency. This is the asymmetry against TOPIC files, which
are always bilingual.

## Frontmatter is optional

GUIDEs do not declare citations in the citation-substrate sense
because they describe procedures rather than make claims. A
GUIDE may carry a brief frontmatter block declaring its
deployment-name and last-verified date, but it is not required
and the renderer does not depend on it.

```yaml
---
deployment: cluster-totebox-corporate
last_verified: 2026-04-27
---
```

The verification date is more meaningful than the edit date. A
GUIDE that has not been re-verified against the live deployment
in the last quarter is suspect; the date tells the operator
whether the procedure is fresh.

## Required structure

Every GUIDE has four sections:

1. **Purpose** — one sentence saying what this GUIDE accomplishes.
2. **Procedure** — numbered steps in imperative voice.
3. **Verification** — how the operator confirms each step worked.
4. **Recovery** — what to do if a step fails.

Sections that do not apply are not omitted. If the GUIDE
describes a procedure with no recovery path (because the
procedure is idempotent, for instance), the Recovery section
says so explicitly. Omission would be ambiguous; a stated
"no recovery needed; the operation is idempotent" is informative.

## Voice — terse imperative

GUIDEs use shorter sentences than TOPICs. Sentence-length
budget: mean around fourteen words, maximum around twenty-four.
Imperative voice — `run`, `confirm`, `restart`, `verify`. Active
voice always; passive voice in a runbook hides who or what is
doing the action, which matters when something fails.

The banned-vocabulary list applies. The list includes verbal
tics that survive in operational prose (`leverage`, `seamless`,
`robust`) — these have no place in a runbook because they
describe nothing the operator can verify.

## Commands are copy-pasteable

Every command in a GUIDE is in a fenced code block, alone on
its line, ready to copy and paste. Inline backtick code is for
referring to a command, not running it.

```sh
systemctl status local-doorman.service
```

Where a command takes arguments that the operator must
substitute, the placeholders are obvious — `<tenant-id>`,
`<instance-name>`, `<commit-sha>`. They are never `xxx`,
`YOUR_VALUE`, or `[insert here]`.

## Verification is concrete

Every step has a check the operator can run to confirm the step
worked. The check is a command with an expected output, not a
narrative. "Verify the service is healthy" is not a check;
"`systemctl is-active local-doorman.service` returns `active`"
is a check.

This rule applies to the procedure as a whole, not only to
individual steps. The Verification section at the bottom of the
GUIDE confirms the post-condition the GUIDE is meant to
establish.

## Recovery is concrete

When a step fails, the operator should know exactly what to
try next. Recovery instructions name the failure mode they
address, the diagnostic command that confirms the failure mode,
and the corrective procedure.

A GUIDE with vague recovery ("restart the service if it does
not work") is worse than no GUIDE — it suggests the operator
has options when in fact the procedure has not been thought
through. Better to write "no automatic recovery; escalate to
on-call" than to gesture at recovery without specifying it.

## What a GUIDE is not

A GUIDE is not a TOPIC. The reasoning, design intent, or
architectural background that motivates a procedure lives in a
TOPIC; the procedure itself lives in the GUIDE. A document that
mixes both is split.

A GUIDE is not a script. A script that the GUIDE invokes lives
in the project's `scripts/` directory; the GUIDE references it
by path. Embedding script logic in GUIDE prose duplicates
authority and rots when the script changes.

A GUIDE is not a public-facing artefact. Operational detail —
the SSH command shape, the systemd unit name, the on-call
escalation path — does not belong in TOPIC files served to a
public audience. It belongs in GUIDEs read by operators with
deployment access.

## See Also

- [[topic-style-guide-readme|Style Guide — README]]
- [[topic-style-guide-topic|Style Guide — TOPIC]]
- [[topic-language-protocol-substrate|Language Protocol Substrate]]
- [[topic-customer-hostability|Customer Hostability]]

## References
