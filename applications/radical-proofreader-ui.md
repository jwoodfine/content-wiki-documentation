---
schema: foundry-doc-v1
title: "The Proofreader Console"
slug: radical-proofreader-ui
category: applications
type: app
content_type: topic
quality: complete
short_description: "The operator-facing web interface for the service-proofreader editorial pipeline, implementing a two-tier design token architecture for tenant brand adaptation and a pure-Rust distillation tool that converts apprenticeship corpus event-pairs into training datasets for service-slm."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-06-30
editor: pointsav-engineering
cites: []
references: []
paired_with: radical-proofreader-ui.es.md
---

The **proofreader console** is the operator-facing web interface for the `service-proofreader`
editorial pipeline. Operators use the console to submit text for staged analysis, review
structured findings, apply or reject suggested rewrites, and record verdict dispositions that
feed the platform's apprenticeship learning corpus. The console is implemented as a
server-rendered HTML application with no client-side JavaScript framework dependency; all
state transitions are handled at the server layer.

## Design token architecture

The console implements a two-tier design token architecture that decouples the platform's
visual language from any specific tenant's brand identity. The first tier consists of generic
tokens — baseline CSS variables, spacing primitives, and typographic scales — distributed
from the `pointsav-design-system` repository. These tokens establish the structural vocabulary
of the interface: grid layout, component sizing, state colours for finding severity levels, and
typographic hierarchy for the three-level finding display (Banned, Mechanical, Generative).

The second tier consists of tenant override tokens sourced from the tenant's media asset
repository. These tokens carry branding decisions — typography faces, colour palette
substitutions, and logo assets — that adapt the interface to the tenant's visual identity
without modifying the console's source code. The two tiers are applied in sequence at render
time: generic tokens establish defaults; tenant overrides substitute values where the brand
requires it. A deployment with no tenant override file falls back entirely to the generic tier,
producing a consistent baseline presentation.

This layering allows the same console codebase to serve multiple tenants under distinct brand
identities. A future `media-proofreader-pointsav` deployment would carry the vendor account's
own token overrides against the same generic substrate as the `media-proofreader-woodfinegroup`
deployment.

## The no-train-on-tenant-text guarantee

The console surfaces the platform's data-handling commitment at the point of text submission.
The no-train-on-tenant-text guarantee is a structural property of the corpus write path, not a
runtime configuration flag: an operator's submitted text and the resulting rewrite are written
to that tenant's deployment instance directory and cannot be co-mingled with other tenants'
records. The corpus written under one tenant's deployment instance is the training substrate
for that tenant's adapted model, not for any other account's model.

The guarantee is made explicit in the submission interface because operators require confidence
before submitting sensitive editorial material. The console surfaces it as a disclosure notice
— permanent, not dismissible — adjacent to the text submission area.

## Verdict recording and the apprenticeship loop

After the three-stage pipeline produces its findings and whole-text rewrite, the operator
interacts with the console through a verdict interface. The interface presents the original
text, the Stage-3 rewrite, and the annotated finding set simultaneously. Three disposition
controls are available: Accept (take the rewrite as-is), Reject (discard the rewrite and
retain the original), or Edit (submit a hand-modified version as the final text, with the
modification visible to the platform).

The submitted verdict triggers a `/v1/verdict` write that records the input, the chosen
output, and the operator's disposition as a typed event-pair tuple. Accepted and edited
verdicts are the highest-value training signal: they represent operator confirmation that a
specific rewrite direction was correct. Rejected verdicts are retained as negative examples
for the Stage-1 Direct Preference Optimisation pipeline. Together, these three disposition
types form the apprenticeship corpus that drives continued model refinement under the
reverse-funnel editorial pattern.

## Rust implementation and corpus distillation

The platform's training pipeline is implemented in Rust rather than a scripting language. The
distillation tool processes the raw JSONL event records written by the verdict endpoint to
extract verified input/output pairs based on operator dispositions. The tool enforces type
safety when parsing the event-pair schema — `draft-created`, `draft-refined`,
`creative-edited` — and produces a `training_dataset.jsonl` file in the format consumed by
`service-slm` for LoRA fine-tuning.

The Rust implementation unifies the operational tooling ecosystem: a single `cargo run`
invocation replaces a pipeline of shell scripts and Python preprocessing steps. It also
eliminates a class of parsing errors that can arise when the event-pair schema evolves —
schema changes require updating the Rust type definitions, which the compiler enforces at
build time rather than at runtime.

The distillation pass isolates operator-confirmed instruction/output pairs. These pairs are
the per-tenant adapter inputs for the student fine-tuning sequence, distinct from the broader
knowledge distillation run that involves the teacher model. The two training paths can run
independently or be integrated into a combined session depending on the corpus size and the
degree of adaptation desired.

## See also

- [[editorial-pipeline-three-stages]] — the three-stage pipeline the console interfaces with
- [[language-protocol-substrate]] — the genre family classification the console's finding
  display reflects
- [[customer-tier-catalog-pattern]] — how the proofreader deployment instance is provisioned
