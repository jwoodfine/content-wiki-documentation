---
schema: foundry-doc-v1
title: "Proofreader console"
slug: radical-proofreader-ui
category: applications
type: app
content_type: topic
quality: complete
index_group: knowledge-and-editorial-applications
short_description: "Terminal content cartridge for the service-proofreader pipeline — operators submit text, review findings, and record a binary accept/reject verdict that feeds the apprenticeship corpus."
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-09-05
editor: pointsav-engineering
cites: []
references: []
paired_with: radical-proofreader-ui.es.md
---

The **proofreader console**, `app-console-content`, is the F4 content cartridge in
[[os-console]] — a terminal interface, not a web application. Operators use it to
submit text to the `service-proofreader` pipeline, review the structured findings and rewrite
it returns, and record a verdict that feeds the platform's [[apprenticeship-substrate|apprenticeship learning corpus]].

## Verdict recording and the apprenticeship loop

After the pipeline returns its findings and rewrite, the operator reviews them from the
terminal and records a verdict with a single keystroke: **accept** the rewrite, or **reject**
it and keep the original. Each verdict posts the request, the tenant, and the disposition back
to the pipeline as a typed event. There is no third "edit and resubmit" disposition — the
choice is binary.

The console surfaces the platform's data-handling commitment at the point of text submission.
The no-train-on-tenant-text guarantee is a structural property of the corpus write path, not a
runtime configuration flag: an operator's submitted text and the resulting rewrite are written
to that tenant's deployment instance directory and cannot be co-mingled with other tenants'
records. The corpus written under one tenant's deployment instance is the training substrate
for that tenant's adapted model, not for any other account's model.

The guarantee is made explicit in the submission interface because operators require confidence
before submitting sensitive editorial material. The console surfaces it as a disclosure notice
— permanent, not dismissible — adjacent to the text submission area.

## See also

- [[editorial-pipeline-three-stages]] — the three-stage pipeline the console interfaces with
- [[language-protocol-substrate]] — the genre family classification the console's finding
  display reflects
- [[customer-tier-catalog-pattern]] — how the proofreader deployment instance is provisioned
