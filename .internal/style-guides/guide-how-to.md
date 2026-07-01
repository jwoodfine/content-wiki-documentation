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
real-world goal. The second reader is the future operator running this same procedure at 3 a.m.
under load — which is why every step is unambiguous and every outcome is verifiable. Structure
the document around the task, not around the system's internals.

## 2. The shape

The operational skeleton, in order:

- **Prerequisites** — the explicit starting state and required access. If none, say "None."
- **Purpose** — one sentence naming the goal this procedure achieves.
- **Procedure** — numbered steps, imperative voice, one action per step.
- **Expected outcome** — a single verifiable fact that is true when the procedure succeeds.
- **Verification** — concrete checks with expected output, not a feeling of confidence.
- **Rollback** — the failure mode, its diagnostic, and the corrective steps; or a stated
  guarantee that the procedure is idempotent or the change irreversible.

**Orientation and first-run variant.** Some guides are learning-oriented rather than
task-oriented — a first-run walk-through that shows a reader around a system they have not used
yet. These are Diátaxis tutorials; they live here because the covering set has no separate
tutorial register. An orientation guide keeps Prerequisites and numbered steps, but where a task
how-to carries formal Expected outcome / Verification / Rollback, an orientation guide folds
confirmation inline ("you should now see the status bar at the top of the screen") and may omit
Rollback, because a read-only walk-through changes no state to reverse. Only that outcome/
verification/rollback formality relaxes; every other rule below still holds. (Added 2026-07-01
after a first-run guide scored as non-compliant against the task skeleton — see the calibration
report.)

## 3. Opening

A how-to leads with Purpose, then Prerequisites — the reader must know in the first two lines
whether this is the right procedure and whether they can run it now.

Purpose is one sentence: the goal, in the reader's terms, phrased as the result they want.
Prerequisites follow immediately and are explicit — access, state, tools, and any procedure
that must have run first. Never leave a prerequisite implied; a missing one is discovered
halfway through, with the system half-changed.

The isolation test for a how-to: a reader who reads only Purpose and Prerequisites can decide,
correctly, whether to proceed or to go elsewhere. If they cannot, the opening has failed.

## 4. Paragraph and sentence rhythm

Terser than house-core. Steps average roughly 14 words; the ceiling is about 24. A step that
runs longer is carrying two actions — split it into two numbered steps.

Steps are imperative and lead with the verb: "Stop the service," not "The service should now be
stopped." Prose between steps is rare and short — a how-to is mostly a numbered list, not an
essay with commands attached.

## 5. Headings and scannability

The six skeleton names from §2 are the fixed headings: Prerequisites, Purpose, Procedure,
Expected outcome, Verification, Rollback. Use them verbatim so a reader who knows one runbook
knows them all.

The Procedure is a numbered list — order is load-bearing, so numbers, not bullets. Steps may
fork on real conditions with an explicit branch: "If the queue is drained, continue to step 5;
if not, repeat step 3." Verification checks are best as a short table or a fenced command with
its expected output beside it. Callouts carry only a genuine hazard ("this step is
irreversible"), never emphasis.

## 6. Voice and tone

The move a how-to turns on is the imperative step with a named object and a verifiable result.

> Restart the gateway; confirm it returns to `active` within 30 seconds.

That single line names the action, the object, and the observable result. Verification carries
its own discipline: never "verify the service is healthy." Name the check and the value that
proves health — a status string, an exit code, a row count, an HTTP code. A check the reader
cannot compare against an expected value is not a check.

Rollback names the failure, not just the reversal. State the failure mode ("if the migration
aborts mid-run"), the diagnostic that confirms it (what to look at), and the corrective steps —
or state plainly that the procedure is idempotent and safe to re-run, or that the change is
irreversible and forward-only.

## 7. Code and examples

A how-to may carry command and code blocks — the operator runs them, so they belong in the
steps. Fence each block, keep it to the command the step performs, and show expected output
where a verification depends on it.

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

**Monolithic step with embedded rationale → step plus a link.**

> Weaker: Rotate the key here rather than at the node, because the gateway is the single
> custody point and node-level rotation would create divergent key state across the fleet, so
> run the rotation from the gateway.
> Stronger: Rotate the key from the gateway (not the node). See [[gateway-key-custody]] for why.

*Moved the reasoning to the reference article and left the step as an action; the operator gets
the move, the rationale stays canonical and linked.*

**Unconditional step that should fork → explicit branch.**

> Weaker: Drain the queue and apply the migration.
> Stronger: If the queue is non-empty, drain it (step 3) before continuing. If already drained,
> apply the migration (step 5).

*Reflected the two real states the operator can be in; the reader stays on the path to the goal
instead of guessing.*

## 9. Pre-publish checklist

- Does the opening let a reader decide, from Purpose and Prerequisites alone, whether to
  proceed?
- Are prerequisites explicit, with "None" stated when there are none?
- Is every step imperative, single-action, and under the length ceiling?
- Does every verification name a concrete check and its expected output?
- Does Rollback name the failure mode and its fix, or state idempotent/irreversible?
- Does every architectural "why" link to a reference article rather than explain inline?
- Do conditional steps fork explicitly where the real world forks?
- Are the title and slug free of a leading article (*the/a/an*), sentence-case / lowercase-kebab, and matched to each other? (see [[house-core]] §Capitalization)
