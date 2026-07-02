---
schema: foundry-doc-v1
title: "How-to guide — operational and procedural writing"
slug: guide-how-to
category: internal
type: reference
content_type: reference
quality: complete
status: active
audience: contributor
bcsc_class: public-disclosure-safe
governs: [PROSE-GUIDE, RUNBOOK, PROSE-DIRECTIVE]
last_edited: 2026-07-01
editor: pointsav-engineering
---

> The register guide for operational writing — guides, runbooks, and directives that take a
> competent reader from a starting state to a finished task. Builds on [[house-core]]; restates
> nothing there. If a point is not covered here, house-core governs.

## 1. Purpose and audience

A how-to serves a reader who already knows the domain and now has a job to do. The reader is
mid-task: a system is in front of them, a goal is defined, and they need the steps that get
them from here to done. They are not learning fundamentals — a how-to is not a tutorial and
never stops to teach what the role already assumes.

This is the Diátaxis how-to register: task-oriented, addressed to a practitioner pursuing a
real-world goal. Practical usability beats completeness
— the guide serves the reader's goal, not the tool's feature list. The second reader is the
future operator running this same procedure at 3 a.m. under load — which is why every step is
unambiguous and every outcome is verifiable. Structure the document around the task, not
around the system's internals.

## 2. The shape

The operational skeleton, in order:

- **Prerequisites** — the explicit starting state: access, tools, state, prior procedures.
  If none, say "None."
- **Purpose** — one sentence naming the goal, plus a rough time estimate.
- **Procedure** — numbered steps, imperative voice, one action per step.
- **Expected outcome** — a single verifiable fact that is true when the procedure succeeds.
- **Verification** — concrete checks with expected output, not a feeling of confidence.
- **Rollback** — the failure mode, its diagnostic, and the corrective steps; or a stated
  guarantee that the procedure is idempotent or the change irreversible.
- **Next steps** — where the reader goes once done: the natural follow-on procedure, or the
  reference article for the system just changed.

The first six are the fixed core; Next steps closes the document so the finished reader is
routed, not stranded. Document one method — the primary one. An alternative approach earns a
single line and a link, never a parallel procedure; two full paths through one guide means the
operator must first decide which guide they are reading.

**Orientation and first-run variant.** Some guides are learning-oriented rather than
task-oriented — a first-run walk-through that shows a reader around a system they have not used
yet. These are Diátaxis tutorials; they live here because the covering set has no separate
tutorial register. An orientation guide keeps Prerequisites, numbered steps, and
Next steps — the bridge from first run to real tasks — but where a task how-to carries formal
Expected outcome / Verification / Rollback, an orientation guide folds confirmation inline
("you should now see the status bar at the top of the screen") and may omit Rollback, because a
read-only walk-through changes no state to reverse. Only that outcome/verification/rollback
formality relaxes; every other rule below still holds. (Added 2026-07-01 after a first-run
guide scored as non-compliant against the task skeleton — see the calibration report.)

## 3. Opening

A how-to opens with its decision pair — Purpose and Prerequisites. Within the first screen the
reader learns three things: whether this is the right procedure, whether they can run it now,
and roughly what it will cost them in time.

Purpose is one sentence, the goal phrased in the reader's terms as the result they want, plus
the estimate: "Rotate the fleet signing keys — about ten minutes, most of it waiting on
propagation." The estimate is a round, honest number, and it separates work from waiting — an
operator plans differently around two minutes of typing than around a twenty-minute
propagation window, and a wait a step silently triggers is a wait the operator will misread as
a failure. If the duration cannot be estimated, the procedure is not yet understood well
enough to publish.

Prerequisites follow immediately as a scannable list of checkable items — access, state,
tools, and any procedure that must have run first — each one the reader can confirm before
starting, with the check named where it is not obvious. Never leave a prerequisite implied; a
missing one is discovered halfway through, with the system half-changed.

The isolation test for a how-to: a reader who reads only Purpose and Prerequisites can decide,
correctly, whether to proceed, defer, or go elsewhere. If they cannot, the opening has failed.

### Short description

Frontmatter carries a `short_description` of roughly 120–180 characters — keyword-first, no
leading article, stating the task and its outcome. It is what search results and catalog
listings display, so it obeys the same scan discipline as the title. The Spanish pair carries
its own `short_description` under the same rules: same length band, no leading article.

## 4. Paragraph and sentence rhythm

Terser than house-core. Steps average roughly 14 words; the ceiling is about 24. A step that
runs longer is carrying two actions — split it into two numbered steps.

Steps are imperative and lead with the verb: "Stop the service," not "The service should now be
stopped." Two orderings within the step follow the reader's own sequence:

- **Location before action.** The reader must be in the right place before they act: "In the
  fleet console, open **Nodes**," not "Open **Nodes** in the fleet console."
- **Goal before action, when conditional.** A conditional step states the goal first so the
  reader can match it to their situation before acting: "To skip re-indexing, pass
  `--no-index`."

A step may carry its immediate result in the same breath — "Restart the unit. The status
column reads `active` within 30 seconds." — so the reader knows what confirms the step before
moving on. Prose between steps is rare and short — a how-to is mostly a numbered list, not an
essay with commands attached.

## 5. Headings and scannability

The skeleton names from §2 are the fixed headings — Prerequisites, Purpose, Procedure,
Expected outcome, Verification, Rollback, Next steps. Use them verbatim so a reader who knows
one runbook knows them all.

### Title leads with the verb

A how-to title is the task, and the task is a verb: "Rotate keys," not "Key rotation" and not
"How to rotate keys." This is the house keyword-first rule applied to this register — in a
task document the verb *is* the keyword, and a catalog of guides scanned down the left margin
reads as a list of things the reader can do. A "How to" prefix files every guide under H and
wastes the scan position. Sibling guides in a catalog stay parallel: "Rotate keys," "Revoke a
node," "Restore from snapshot." The no-leading-article and sentence-case rules from
[[house-core]] hold unchanged; the slug matches (`rotate-keys`).

### Procedure structure

The Procedure is a numbered list — order is load-bearing, so numbers, not bullets. A
single-action procedure takes one bullet instead of a numbered list of one. Mark a skippable
step by opening it with "Optional:". Steps may fork on real conditions with an explicit
branch: "If the queue is drained, continue to step 5; if not, repeat step 3." A procedure that
outgrows a screen is usually two procedures — split it into stages under `###` subheadings,
each stage ending at a state the operator can verify before continuing. Verification checks
are best as a short table or a fenced command with its expected output beside it.

### Callouts

Three labels, each with one job: **Note** for an aside the reader may safely skip, **Tip** for
a better move the reader may take, **Warning** for a genuine hazard — data loss,
irreversibility, cost. A callout earns its box by being out-of-band; prose the step needs is
part of the step, and a callout used for emphasis is a step that was not written clearly
enough. Place a Warning immediately before the step it protects, never after. Three to five
callouts per guide is the ceiling and most guides need one or two — callouts in a row stop
being visible, and a reader trained to skip boxes skips the one that mattered.

## 6. Voice and tone

The move a how-to turns on is the imperative step with a named object and a verifiable result.

> Restart the gateway; confirm it returns to `active` within 30 seconds.

That single line names the action, the object, and the observable result. Introduce a command
by what it accomplishes, not by the act of running it: "Deploy the gateway:" followed by the
block, never "Run the following command:". Verification carries its own discipline: never
"verify the service is healthy." Name the check and the value that proves health — a status
string, an exit code, a row count, an HTTP code. A check the reader cannot compare against an
expected value is not a check.

Rollback names the failure, not just the reversal. State the failure mode ("if the migration
aborts mid-run"), the diagnostic that confirms it (what to look at), and the corrective steps —
or state plainly that the procedure is idempotent and safe to re-run, or that the change is
irreversible and forward-only.

Next steps routes the finished reader in one or two lines: the procedure this one unlocks, or
the reference article for the system just changed. It is a signpost, not a summary — the
reader already knows what they did.

## 7. Code and examples

A how-to may carry command and code blocks — the operator runs them, so they belong in the
steps. Every fenced block carries its language tag (```` ```bash ````, ```` ```toml ````,
```` ```rust ````; expected output takes ```` ```json ```` or ```` ```text ````) so the
renderer highlights it and a machine reader knows what it is holding. Keep each block
copy-runnable: the command itself, one per block, no prompt decoration. Name placeholders for
what the reader substitutes and say where the value comes from:

```bash
foundryctl node revoke <node-id>   # node-id: first column of `foundryctl node list`
```

Show expected output wherever a verification depends on it, in its own tagged block beside the
command.

Architectural rationale does not belong inline. The "why" — why this order, why this component
holds this responsibility — lives in a reference or explanation article, linked once. A how-to
carries the steps; the explanation carries the reasoning. When a step needs its rationale,
point to it: "See [[gateway-key-custody]] for why the gateway holds every key; this guide
covers the rotation procedure." This keeps the procedure runnable and the reasoning in one
canonical place rather than re-explained in every guide that touches it.

## 8. Worked examples

**Vague verification → concrete check with expected output.**

> Weaker: After restarting, verify the service is healthy.
> Stronger: After restarting, run `curl -s localhost:9203/healthz`; expect `{"status":"ok"}`.

*Named the check and the value that proves success; "healthy" is unverifiable, a status string
is not.*

**Noun title and buried duration → imperative title and estimate up front.**

> Weaker: Title: "Signing-key rotation." Purpose: This guide describes the rotation process
> for fleet signing keys. Note that propagation may take some time.
> Stronger: Title: "Rotate fleet signing keys." Purpose: Rotate the fleet signing keys —
> about ten minutes, eight of them waiting on propagation.

*Led the title with the verb and put the honest time cost in the first line; the reader can
now decide, schedule, and stop misreading the wait as a failure.*

**Callout as emphasis → prose in the step; callout kept for the hazard.**

> Weaker: **Note:** it is very important to drain the queue first. **Note:** draining uses
> the drain subcommand. **Warning:** remember to check the queue afterwards.
> Stronger: Drain the queue: `foundryctl queue drain`. The count reaches 0 within a minute.
> **Warning:** step 4 deletes the snapshot; there is no undo past this point.

*Folded the ordinary instructions into the step where they belong and spent the one callout on
the genuine hazard — a box is only visible when boxes are rare.*

## 9. Pre-publish checklist

- Does the title lead with an imperative verb, do title and slug drop the leading article, and
  does `short_description` state the task keyword-first in ~120–180 characters, with its
  Spanish pair? (see [[house-core]] §Capitalization)
- Can a reader decide to proceed from Purpose and Prerequisites alone — with a rough time
  estimate in Purpose and "None" stated when there are no prerequisites?
- Is every step imperative, single-action, under the length ceiling, placed after its
  location, and forked explicitly where the real world forks?
- Does every fenced block carry a language tag and stay copy-runnable, with placeholders named
  for what the reader substitutes?
- Does every verification name a concrete check and its expected output?
- Does Rollback name the failure mode and its fix, or state idempotent/irreversible?
- Does each callout carry a genuine hazard or aside — at most a handful, with any Warning
  placed before the step it protects?
- Does every architectural "why" link to a reference article rather than explain inline, and
  does Next steps route the finished reader to a real destination?
