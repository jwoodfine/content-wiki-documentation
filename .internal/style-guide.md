---
schema: foundry-doc-v1
title: "Editorial style guide"
slug: style-guide
category: internal
type: reference
content_type: reference
quality: complete
short_description: "Consolidated internal reference for every editorial content type authored across the platform — TOPIC, GUIDE, ARCHITECTURE, and the internal-communication and legal-document genres (email, chat, meeting notes, contract, CLA, policy, README, terms of use, ticket comment, memo, license explainer, inventory, changelog). Not rendered on the public wiki; for contributors only."
status: active
audience: contributor-internal
bcsc_class: internal-only
last_edited: 2026-07-01
editor: pointsav-engineering
cites:
 - ni-51-102
 - osc-sn-51-721
paired_with: style-guide.es.md
---

> This document lives in `.internal/` and is not rendered by `app-mediakit-knowledge` — dotted directories are skipped by the content loader. It consolidates the sixteen former `reference/style-guide-*.md` articles into one contributor-facing standard. Content in this document is addressed to people authoring platform content, not to wiki readers.

## Topic

> A TOPIC file explains what something is — architecture, background, or platform context that a fresh reader needs to understand the platform — and is the counterpart of a GUIDE, which explains how to operate it.

A **TOPIC** file explains what something *is*. It is architecture, background — material a fresh reader needs to understand the platform. It is not how to operate something; that is a GUIDE file, covered in the **Guide** section below. This article is itself a TOPIC, and the structure it follows is the structure it documents.

### The editorial standard

These five rules are the ratified editorial standard for every TOPIC. They were reconciled and operator-ratified on 2026-05-21. Where any other guidance in this document — or in [[editorial-language-registers]] — conflicts with a rule below, the rule below governs.

1. **Sentence length is budgeted by sentence role.** An expansion sentence — one that develops a mechanism or an argument inside a body section — runs to about 45 words at most. A disclosure sentence — the lede, a compliance claim, a regulatory statement — runs to 25 words at most. Vary the rhythm: every paragraph carries at least one short declarative sentence, so the prose reads as an accordion rather than a monotone.
2. **Active verbs describe present-fact mechanism.** Use the active voice to describe how something works now. Do not use it to assert a forward-looking claim as accomplished fact — capability, timeline, or outcome that is not yet true keeps `planned`, `intended`, `may`, or `target` (see "Forward-looking statements" below). Do not give a system human intent or feeling. There is no ban on `is`, `are`, or `was`: a plain copula is correct when the sentence states a fact.
3. **Analogy is a ceiling, not a quota.** An analogy is optional. Where one is used, hold to at most one per 300 words. A TOPIC with no analogy is fully compliant; a TOPIC that reaches for an analogy in every paragraph is not.
4. **The lede is the nut graf; the Franklin arc orders the body.** The front-loaded four-paragraph lede carries the news in roughly the first 10% of the article. The Franklin arc — Crisis, then Quest, then Breakthrough — governs the order of body sections only. It never displaces the lede or delays the news.
5. **The SaaS-marketing register is rejected.** Public content does not adopt the promotional voice of a software-product landing page. Internal codenames — "Liquid Glass" among them — stay internal; they do not appear in public TOPIC text.

### Where TOPICs live

| Wiki | Subject | License |
|---|---|---|
| `content-wiki-documentation` | Vendor platform documentation | CC BY 4.0 (public) |
| `content-wiki-corporate` | Customer corporate principles | CC BY-ND 4.0 |
| `content-wiki-projects` | Customer project narratives | CC BY-ND 4.0 |

A TOPIC's home is the wiki whose subject matter it covers. A TOPIC about service architecture lives in `content-wiki-documentation`. A TOPIC about a customer's corporate principles lives in `content-wiki-corporate`. Crossing these boundaries silently is drift; surface the question rather than choosing arbitrarily.

### Bilingual pair required

Every TOPIC ships as a pair: the English file and a Spanish strategic adaptation (`.es.md`). The Spanish file is strategic adaptation, not 1:1 translation — translate the orientation a Spanish-reading audience needs; drop the deeper implementation detail.

A non-English-speaking contributor or reader should be able to locate themselves in the system without first decoding English-only material.

### Frontmatter is required

Every TOPIC declares its metadata in YAML frontmatter. The `cites` list is required when the article makes claims that resolve to external regulatory instruments, research papers, or technical specifications.

```yaml
---
schema: foundry-doc-v1
title: "Style Guide — TOPIC"
slug: style-guide-topic
category: reference
type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
editor: pointsav-engineering
cites:
 - ni-51-102
 - osc-sn-51-721
paired_with: style-guide-topic.es.md
---
```

Citation IDs resolve against the platform citation registry. Inline references in body prose use `[citation-id]` syntax. A new external reference is added to the registry first, then cited in the article.

### Front-loaded lede structure

A TOPIC opens with a front-loaded lede of four paragraphs. The model: the first paragraph states the structural property in one sentence that satisfies a financially literate institutional reader reading on their phone. The second paragraph supplies one concrete fact or number that makes the first paragraph verifiable. The third explains the mechanism. The fourth states why it matters for a regulated buyer, an auditor, or a risk manager.

| Paragraph | Content | Test |
|---|---|---|
| 1 — What + so-what | The structural property and its compliance or risk consequence | Can a financially literate institutional reader read this on their phone and understand the point? |
| 2 — Concrete fact | A specific datum: metric, date, binary decision | Is this verifiable? Does it make paragraph 1 falsifiable? |
| 3 — Mechanism | How it works | Is this the simplest accurate description of the mechanism? |
| 4 — Why it matters | Consequence for compliance, custody, or risk | Does a regulated buyer or auditor know what action to take from this? |

**Stand-alone PDF test.** Print paragraphs 1–4 in isolation and hand them to a reader who will see nothing else. The essential compliance or risk message must survive. If it does not, revise the lede before any other edit.

A reader who stops after the lede should leave with the news. This is the front-loaded shape. The reasoning, supporting citations, and trade-off discussion follow the lede; they do not precede it. Opening with mechanism and arriving at the consequence at the end is academic-paper shape — the wrong shape for a public platform wiki.

### Voice — institutional, not marketing

The standard is precise, professional prose understandable to a financially literate reader without a technical background. Active voice unless passive carries specific technical meaning. Sentence length follows the budgeted standard above — expansion sentences to about 45 words, disclosure prose to 25 — and every paragraph carries at least one short declarative sentence.

The banned-vocabulary list applies in full: `leverage`, `empower`, `next-generation`, `industry-leading`, `seamless`, `robust`, `cutting-edge`, `world-class`. These words carry no information. Their absence sharpens the prose; their presence dilutes it.

**Named actors and consequences.** Every active sentence names who does what and what the consequence is if they do not. "The Doorman holds every API key" names the actor. "API keys are managed centrally" hides who holds them and what happens if they are not held there. The passive construction is useful only when the actor genuinely does not matter; in most governance sentences, the actor is the point.

**CFO sentence test.** Every sentence must be useful to a chief financial officer — someone who understands contracts, risk, and regulation but does not read source code. Pure engineering detail without a business consequence belongs deeper in the article or in a footnote. "The storage engine appends to an immutable tile format" fails the test. "A record cannot be deleted or modified after it is written — the storage engine makes modification structurally impossible rather than policy-prohibited" passes it.

**"So what" discipline.** Every body paragraph answers the question: *so what for a regulated buyer or a risk-aware engineer?* A paragraph that describes a mechanism without stating its consequence for compliance, custody, cost, or risk should either have that consequence added or be collapsed into the paragraph that does.

### 75/25 institutional and developer register

A TOPIC in `content-wiki-documentation` is addressed to two audiences simultaneously: institutional readers (financial community, regulated buyers, compliance officers, auditors) and developer readers (engineers, architects, integrators). The target register is 75% institutional, 25% developer.

Institutional prose answers questions of the form: *does this satisfy my regulatory requirement? who owns this data? what happens if the vendor fails? what does the audit log look like?* Developer prose answers: *how does this work? what does the API look like? what are the edge cases?*

In practice: write the structural claim and its compliance consequence before the implementation detail. An article about the WORM ledger leads with "a record cannot be deleted or modified after it is written, satisfying SEC 17a-4(f) by structure" before it describes the tile format. An article about the Doorman leads with "no API key lives outside this boundary; every call is logged to the per-tenant audit ledger" before it describes the routing code.

### Internal governance vocabulary

The words **Doctrine** and **Convention** as internal governance vocabulary never appear in TOPIC body text or section headings. A financially literate institutional reader reading this wiki should encounter the underlying idea in institutional prose, not the internal name for the governance machinery.

Write the principle, not the label:

- Instead of "per Doctrine claim #7, no AI may write to the knowledge graph" → "no AI component writes to the knowledge graph; that path is exclusively deterministic"
- Instead of "this Convention establishes the commit-signing requirement" → "every commit must be signed with an SSH key verified against the platform's identity store"

Where the term is being defined as a first-class concept within the article — a TOPIC about constitutional amendment process, for example — use the term but immediately follow it with a plain-language translation.

### Forward-looking statements carry cautionary language

A TOPIC that describes future capability, timeline, customer outcome, or governance arrangement uses `planned`, `intended`, `may`, or `target` — never declarative-future. This is the BCSC continuous-disclosure posture per `[ni-51-102]` and the forward-looking discipline of `[osc-sn-51-721]`.

The Sovereign Data Foundation is referenced in planned and intended terms only. Treating it as a current equity holder or active governance body is a posture violation; future state is described as future state.

### Cite every non-obvious claim

A TOPIC that says "compose service-disclosure with service-content" cites neither — those are platform components and the reader can find them in the monorepo. A TOPIC that says "per the production AI literature, multi-LoRA composition above three adapters per request hits multi-task interference" needs a citation; the claim is non-obvious, the reader cannot verify it from the platform alone.

The discipline is not academic exhaustiveness. It is auditability. A reviewer reading the TOPIC five years from now should be able to follow each non-obvious claim back to its source.

### Edit in place

A TOPIC does not get a `_V2` or `_V3` suffix when revised. Edit the existing file; rely on Git history for prior versions. This applies with full weight to TOPIC files because the wiki renderer serves the latest committed version.

A TOPIC that has been substantially rewritten — new structural sections, removed claims, new citations — bumps `last_edited` in frontmatter. Routine wording polish does not require a frontmatter bump.

### What a TOPIC is not

A TOPIC is not a runbook. Operational instructions — "run this command, configure this setting, recover from this failure" — belong in GUIDE files inside the deployment subfolder they operate. A file that describes both is split.

A TOPIC is not a marketing piece. These wikis are public-facing in the sense that they are served at `documentation.pointsav.com`, but the audience is contributors, customers, regulators, and engineers — not buyers being persuaded.

A TOPIC is not internal-only material. Anything internal-only (in-flight cleanup, mailbox correspondence, deployment-specific notes) lives in the workspace's `.agent/` directories or deployment instances, not in a content wiki.

### See also

- **Guide** (below)
- [[language-protocol-substrate|Language Protocol Substrate]]
- [[citation-substrate|Citation Substrate]]
- [[anti-homogenization-discipline|Anti-Homogenization Discipline]]

## Guide

> A GUIDE file is the operational runbook format for platform deployment subfolders — how to run, configure, or recover from failure — and is distinct from a TOPIC, which explains what something is and why.

A **GUIDE** file (`guide-<subject>.md`) is an operational runbook — how to run, configure, or recover from failure. It tells the operator what to do, in order, with the commands they will copy and paste. It is not an explanation of why something works; that reasoning belongs in a TOPIC, covered in the **Topic** section above. Every GUIDE lives inside the deployment subfolder it operates; a GUIDE that appears at a catalog root without a containing subfolder is misplaced and must be moved.

### Where GUIDEs live

GUIDEs live inside the deployment subfolder they operate. There are two tiers:

| Tier | Path shape | Purpose |
|---|---|---|
| **Catalog** | `customer/woodfine-fleet-deployment/<deployment-name>/guide-*.md` | Defines how this deployment is operated. Every catalog entry that is operationally meaningful carries at least one. |
| **Instance** | `deployments/<instance>/guide-*.md` | Variation only when an instance has operationally significant deviations from its catalog GUIDE. |

A GUIDE at a fleet-deployment catalog root (no containing deployment subfolder) is misplaced. Move it into the owning deployment subfolder.

### English only

GUIDE files are English-only. They are operational, not public-facing — bilingual pairs add maintenance cost without benefit, because the audience is operators with English working proficiency. This is the asymmetry against TOPIC files, which are always bilingual.

### Frontmatter is optional

GUIDEs do not declare citations in the citation-substrate sense because they describe procedures rather than make claims. A GUIDE may carry a brief frontmatter block declaring its deployment name and last-verified date, but it is not required.

```yaml
---
deployment: cluster-totebox-corporate
last_verified: 2026-04-27
---
```

The verification date is more meaningful than the edit date. A GUIDE that has not been re-verified against the live deployment in the last quarter is suspect; the date tells the operator whether the procedure is fresh.

### Required structure

Every GUIDE has six sections, in this order:

1. **Prerequisites** — what the operator must have in place before starting: installed tools, access permissions, running services, environment variables, any prior GUIDE that must have been completed first.
2. **Purpose** — one sentence saying what this GUIDE accomplishes.
3. **Procedure** — numbered steps in imperative voice.
4. **Expected outcome** — the post-condition this GUIDE is intended to establish: what the system looks like when the procedure has succeeded. Stated as a verifiable fact, not a narrative ("The service reports `active (running)`" not "the service should be running").
5. **Verification** — the sequence of commands the operator runs to confirm the expected outcome holds. Each check specifies the command and the expected output.
6. **Rollback** — how to undo the procedure if verification fails or the procedure is interrupted. Name the failure mode, the diagnostic command, and the corrective steps. If the operation is idempotent or irreversible, say so explicitly — "this operation is idempotent; re-run the procedure" or "no rollback path; escalate to on-call before proceeding".

Sections that do not apply are not omitted — they explain why they do not apply. A Prerequisites section that lists nothing still says "No prerequisites; the procedure is self-contained." Omission would be ambiguous.

### Prerequisites are explicit

Prerequisites list everything the operator must have before the first numbered step. Items include: installed packages or binaries (a specific CLI available and on `$PATH`), access permissions (SSH key loaded, `sudo` rights, membership in a Unix group), running services (a specific systemd unit active), environment variables (`TENANT_ID` set), and any prior GUIDE that must have completed successfully (with a `[[slug]]` link to that GUIDE).

A Prerequisites section that lists nothing says explicitly: "No prerequisites; the procedure is self-contained." This tells the operator the GUIDE is safe to start without context.

### Voice — terse imperative

GUIDEs use shorter sentences than TOPICs. Sentence-length budget: mean around fourteen words, maximum around twenty-four. Imperative voice — `run`, `confirm`, `restart`, `verify`. Active voice always; passive voice in a runbook hides who or what is doing the action, which matters when something fails.

**Named actors.** Every step names the agent and the object: "the operator runs the following command" not "the following command is run." When a step changes state in a service or system, say what changes — "this writes a row to the per-tenant audit ledger" not "this completes the action." A step the operator cannot verify did not happen.

The banned-vocabulary list applies. The list includes verbal tics that survive in operational prose (`leverage`, `seamless`, `robust`) — these have no place in a runbook because they describe nothing the operator can verify.

### Commands are copy-pasteable

Every command in a GUIDE is in a fenced code block, alone on its line, ready to copy and paste. Inline backtick code is for referring to a command, not running it.

```sh
systemctl status local-doorman.service
```

Where a command takes arguments that the operator must substitute, the placeholders are obvious — `<tenant-id>`, `<instance-name>`, `<commit-sha>`. They are never `xxx`, `YOUR_VALUE`, or `[insert here]`.

### Verification is concrete

Every step has a check the operator can run to confirm the step worked. The check is a command with an expected output, not a narrative. "Verify the service is healthy" is not a check; "`systemctl is-active local-doorman.service` returns `active`" is a check.

This rule applies to the procedure as a whole, not only to individual steps. The Verification section at the bottom of the GUIDE confirms the post-condition the GUIDE is meant to establish.

### Rollback is concrete

When verification fails, the operator must know what to try next. Rollback instructions name the failure mode they address, the diagnostic command that confirms it, and the corrective steps.

A GUIDE with vague rollback ("restart the service if it does not work") is worse than no GUIDE — it suggests the operator has options when in fact the procedure has not been thought through. Better to write "no automatic rollback; escalate to on-call" than to gesture at recovery without specifying it.

Two special cases handled explicitly:

- **Idempotent procedure**: "This procedure is idempotent. If interrupted, re-run from step 1 — no partial state to clean up."
- **Irreversible procedure**: "This operation cannot be undone. Verify prerequisites and expected outcome before executing step N."

### What a GUIDE is not

A GUIDE is not a TOPIC. The reasoning, design intent, or architectural background that motivates a procedure lives in a TOPIC; the procedure itself lives in the GUIDE. A document that mixes both is split.

A GUIDE is not a script. A script that the GUIDE invokes lives in the project's `scripts/` directory; the GUIDE references it by path. Embedding script logic in GUIDE prose duplicates authority and rots when the script changes.

A GUIDE is not a public-facing artefact. Operational detail — the SSH command shape, the systemd unit name, the on-call escalation path — does not belong in TOPIC files served to a public audience. It belongs in GUIDEs read by operators with deployment access.

### See also

- **Topic** (above)
- [[language-protocol-substrate|Language Protocol Substrate]]
- [[customer-hostability|Customer Hostability]]

## Architecture

> An `ARCHITECTURE.md` at a project root explains where the project sits in the larger system, what it exposes, how its modules are organised, and — equally important — what it is not.

An **ARCHITECTURE.md** is the technical reference for a single project in `pointsav-monorepo`. It is written for an audience that already knows the platform's vocabulary and wants to understand one project's place in the system, its outward-facing interface, and the internal organisation of its code. It is not a tutorial and not a runbook. Companion files at the project root are governed by the [[root-files-discipline|root files discipline]]; this article covers one of them. The human-facing operational form; the machine-readable counterpart lives in `service-disclosure/templates/architecture.toml`.

### When to use this template

An `ARCHITECTURE.md` belongs at a project root whenever the project's design is complex enough that a contributor picking it up cold could not reconstruct its structure from the source files alone. Projects with more than two significant modules, a non-obvious layering decision, or a meaningful consumer contract with other parts of the system warrant an `ARCHITECTURE.md`.

Single-file utilities, thin adapters, and pure data directories do not warrant one. When in doubt, write a short version — four sections plus an annotated file tree is a complete `ARCHITECTURE.md`.

### Frontmatter fields

`ARCHITECTURE.md` files do not carry YAML frontmatter. The template describes a plain Markdown file with a section structure enforced by the per-genre validator in `service-disclosure`. No citation-substrate fields are required because the file is a project-root artefact, not a content-wiki article.

### Structure

The template requires four sections in this order:

| Section | Purpose |
|---|---|
| **Position** | Where this project sits in the larger system — which ring, which service family, which consumer-producer relationships. One or two paragraphs. Reference siblings by canonical Nomenclature Matrix name. |
| **Public surface** | The API, interface, or contract this project exposes to the rest of the codebase. List types, functions, or endpoints the consumer depends on. |
| **Module layout** | Annotated directory tree of the project's internal organisation. ASCII-art suffices. One phrase per leaf explaining its responsibility. |
| **What this is not** | Explicit non-goals. Name the things a reader might reasonably expect this project to do but that it does not. This section limits readers' interpretation and prevents feature-creep. |

Sections are separated by `##` headings and appear in the order above. Adding a fifth or sixth section is acceptable when the project has meaningfully distinct concerns (for example, a "Threading model" section for a concurrent service). Omitting a required section is not.

### Register and tone

The register is technical. Assume domain familiarity; do not explain the platform's general architecture in an `ARCHITECTURE.md` for a specific project — that belongs in a TOPIC in `content-wiki-documentation`.

Sentence-length budget: mean around eighteen words, maximum around thirty. Active voice. Diagrams for cross-component relationships are encouraged; ASCII-art trees suffice for module layout. Every canonical project or service name is used exactly as it appears in the Nomenclature Matrix — no paraphrases, no abbreviations.

The banned-vocabulary list applies. Technical writing that says `"robust"`, `"seamless"`, or `"leverage"` signals vagueness; an `ARCHITECTURE.md` should name the specific invariant, the specific interface, or the specific dependency.

### Example

```markdown
## Position

`service-disclosure` holds the schema substrate for the platform's
editorial work. It sits in Ring 2 alongside `service-content`
and is consumed at request time by `service-slm` (the Doorman)
to validate incoming protocol requests before routing.

## Public surface

- `Family` — four-variant enum identifying the adapter family.
- `GenreTemplate` — eighteen-variant enum; each maps to a
 `.toml` + `.md` pair under `templates/`.
- `validate_frontmatter(fm: &Frontmatter) -> Result<(), ValidationError>`

## Module layout

service-disclosure/
├── src/
│ ├── lib.rs # crate root; re-exports; BANNED_VOCABULARY
│ ├── genre.rs # Family + GenreTemplate
│ ├── frontmatter.rs # Frontmatter struct
│ └── validate.rs # validate_frontmatter + ValidationError
└── templates/ # 18 .toml + 18 .md pairs

## What this is not

- Not an inference engine. Prompt scaffolding lives in the
 template `.toml` files; the Doorman composes prompts at
 request time.
- Not a storage layer. Documents live in `service-content`.
```

### See also

- **Topic** (above)
- **Guide** (above)
- [[language-protocol-substrate|Language Protocol Substrate]]
- [[root-files-discipline]] — companion-file discipline that governs what belongs at a project root alongside ARCHITECTURE.md

## Email

> Every external email has one point. The reader knows what is wanted by the end of the first paragraph.

A **formal email** (COMMS-EMAIL genre) is any external or semi-formal communication sent to a recipient outside the Foundry workspace — a vendor, a regulator, a counterparty, or a collaborator. It differs from an inbox message in that it is addressed to a named recipient, carries a subject, and may be archived. This article is the human-facing standard; the machine-readable counterpart lives in `service-disclosure/templates/email.toml`.

### When to use this template

Use the email template for any communication that:

- Leaves the Foundry workspace (external recipient, external platform).
- Requires a written record (formal ask, vendor confirmation, regulatory contact).
- Is addressed to a specific person or role, not to a group channel.

Internal messages to the inbox or outbox use the inbox-message format from workspace §12. Slack or chat messages use the **Chat** template.

### Structure

The template requires a header and three body sections:

**Header** (before any body text):

```
To:      <recipient name and email, or role>
Subject: <specific subject — what this email is about, not "Update" or "Follow-up">
```

| Section | Purpose |
|---|---|
| **Opening** | One sentence: context and the ask, together. The recipient understands what is wanted without reading further. |
| **Body** | The detail the recipient needs to respond or act. One point per paragraph. No more than three paragraphs. |
| **Close** | The specific next step and who owns it. A concrete date where possible. Followed immediately by the signoff. |

### Register and tone

Professional, plain. Address the recipient by name or role in the opening where the relationship warrants it. Do not bury the ask in paragraph three.

Subject lines must be specific: "Request for NDA — MCorp / [Counterparty]" rather than "Partnership discussion." Ambiguous subjects delay responses and reduce traceability in archives.

Sentence-length budget: mean around twenty words, maximum thirty-five. Active voice. The [[editorial-language-registers|banned-vocabulary list]] applies: state the action directly rather than using marketing-register phrases.

When the recipient may be a current or prospective investor, forward-looking claims about the platform, products, or roadmap carry "planned / intended / may / target" language. This applies to all statements about future capability, timeline, or commercial outcome.

### See also

- **Chat** (below)
- **Memo** (below)
- [[language-protocol-substrate|Language Protocol Substrate]]

## Chat

> A chat message carries one point. If a second point is needed, send a second message.

A **chat message** (COMMS genre) is a short synchronous or near-synchronous communication sent to a team channel or direct recipient. It is addressed to people who are present or will be present soon. Chat is not a substitute for a memo, an **Email**, or a **Ticket comment** — each serves a different archival purpose. This article is the human-facing standard; the machine-readable counterpart lives in `service-disclosure/templates/chat.toml`.

### When to use this template

Use a chat message when:

- The communication is short, time-sensitive, and low-stakes.
- The recipient is on the same platform and likely to respond within the same working session.
- The message does not need to be formally archived or retrieved later.

If the content needs to be traceable, retrievable, or acted on by someone not currently present, use a ticket comment, email, or inbox message instead.

### Structure

**Header** (optional, for channel messages):

```
Channel: #<channel-name>   [or]   To: <@recipient>
```

Body: one point, three sentences maximum. If an ask is included, it is the last sentence and is phrased as a direct question.

```
<Context sentence — what is happening or what changed.>
<Detail sentence — the one thing the recipient needs to know.>
<Ask — optional: a direct question or request in one sentence.>
```

Do not include a signoff. Do not write a paragraph. Do not combine multiple topics in one message — send one message per point.

### Register and tone

Conversational but professional. Contractions are acceptable. Emoji are acceptable where they replace a word or carry genuine tonal meaning, not as decoration.

Abbreviations and internal terminology are fine for established team channels. For external-facing channels or recipients unfamiliar with platform vocabulary, spell out the first use.

One-line replies are preferred. If a paragraph is needed, the reply belongs in a ticket comment or email, not in chat.

### See also

- **Email** (above)
- **Ticket comment** (below)
- [[language-protocol-substrate|Language Protocol Substrate]]

## Meeting notes

> Meeting notes exist for the action items and the decisions. Everything else is archive material.

**Meeting notes** (COMMS genre) record what was decided and what happens next in a meeting. They are not a transcript. A reader who was absent reads the notes to learn the outcome and their obligations — not to reconstruct the conversation. For decisions that carry architectural weight, a [[architecture-decisions|formal ADR]] is the right artifact, not meeting notes. This article is the human-facing standard; the machine-readable counterpart lives in `service-disclosure/templates/meeting-notes.toml`.

### When to use this template

Use meeting notes for any meeting that produces decisions or action items. Short informal check-ins that produce neither do not need notes — a chat message to the channel suffices. Notes are required when:

- A decision is made that affects scope, timeline, or ownership of work.
- An action item is assigned to a named person.
- A question is left open and needs to be tracked to resolution.

### Structure

**Header block** (before any heading):

```
Meeting:   <descriptive title — not "Sync" or "Check-in">
Date:      <YYYY-MM-DD>
Attendees: <names or roles, comma-separated>
```

| Section | Purpose |
|---|---|
| **Agenda** | The topics listed going in. One item per line. Marked with ✓ if covered, — if deferred. |
| **Decisions** | A bulleted list of discrete decisions made. Each bullet names the decision and is self-contained — readable without the Notes context. |
| **Action items** | A table: `Owner` \| `Action` \| `Due`. One row per item. If no date was set, `Due` is `TBD` — not blank. |
| **Notes** | Optional. Context that supports the decisions or action items. This section is archive material — compress aggressively. Three sentences is usually sufficient; more than ten suggests a memo is warranted. |

### Register and tone

Decisions are phrased as completed facts: "Agreed: X will ship on 2026-07-01" rather than "We discussed shipping X." Action items use imperative form ("Write the draft proposal") and name a specific owner. "TBD" is acceptable for due dates; "someone" is not acceptable for owners.

The Notes section is prose-minimal. It exists for context, not for narrative — do not transcribe the discussion.

Sentence-length budget: mean around twenty words for prose sections. The Decisions and Action items sections use fragments where clarity permits.

### See also

- **Ticket comment** (below)
- **Memo** (below)
- [[language-protocol-substrate|Language Protocol Substrate]]

## Contract

> A contract names its parties, defines its terms, and states what each party is bound to do. Every clause is a commitment or a condition — nothing else.

A **contract** (LEGAL genre) is a formal agreement between two or more named parties that creates binding obligations. It is authored in the legal-plain register and reviewed by the responsible governance party before any party signs. This article is the human-facing standard; the machine-readable counterpart lives in `service-disclosure/templates/contract.toml`.

### When to use this template

Use the contract template when:

- A formal binding agreement is required between named parties.
- The obligations, term, and termination conditions need to be explicit and traceable.
- The agreement will be reviewed by `factory-release-engineering` governance before execution.

Informal operational agreements between team members or roles do not require a contract — a **Memo** or **Ticket comment** records them. Agreements that bind a legal entity (PointSav Digital Systems, MCorp, or a third party) require governance review before any signature.

### Structure

The template requires six sections in this order:

| Section | Purpose |
|---|---|
| **Parties** | The full legal names, registered addresses, and defined short names ("PointSav," "Vendor," "Contributor") of every party to the agreement. |
| **Effective date** | The date on which the agreement takes effect. If conditional on signature, state "the date of the last signature." |
| **Recitals** | Short "Whereas" clauses: the context and intent. Two to five recitals. Not obligations — context for interpretation. |
| **Definitions** | Each defined Term, stated once. Defined terms are capitalised throughout the contract after their first definition. |
| **Terms** | The substantive obligations: what each party must do, by when, and under what conditions. Numbered clauses. |
| **Term and termination** | The duration of the agreement, how it may be terminated, and what happens upon termination (survival clauses, obligations that persist). |

An optional **Signatures** block follows the last section. Its format is determined by the jurisdiction and signature method.

### Register and tone

Legal-plain. Defined terms are capitalised after their first definition. Active voice where possible: "Vendor shall deliver" rather than "Delivery shall be made by Vendor." No "herein," "aforementioned," or "notwithstanding" when plain alternatives exist. Every obligation names a subject and a deadline.

Every agreement that binds a legal entity routes through the system administrator (`open.source@pointsav.com`) for governance review before any signature is obtained. This rule applies without exception.

### See also

- **CLA** (below)
- **Policy** (below)
- **Terms** (below)
- [[language-protocol-substrate|Language Protocol Substrate]]

## CLA

> A CLA transfers specific intellectual property rights from a contributor to the project. The canonical text is governed by factory-release-engineering — this template is for drafting or explaining one, not for executing one.

A **Contributor License Agreement** (LEGAL-CLA genre) is an agreement between a project and a contributor that grants the project the rights it needs to use, modify, and redistribute the contributor's work. A CLA is not a copyright transfer — the contributor retains copyright and grants a [[disclosure-substrate|license]]. Every CLA executed under this platform routes through `factory-release-engineering` governance before it binds any party. This article is the human-facing standard; the machine-readable counterpart lives in `service-disclosure/templates/cla.toml`.

### When to use this template

Use this template when:

- An open-source project in `pointsav-monorepo` accepts external contributions and needs a contribution framework.
- A contributor's rights need to be explicit to satisfy a downstream licensing requirement.
- A governance review of an existing CLA is needed for comparison against the canonical text.

The canonical CLA text is maintained by `factory-release-engineering`. Do not draft a CLA for execution without routing it through **Policy** governance review.

### Structure

The template requires a header block and five sections:

**Header block** (before any heading):

```
Agreement:   Contributor License Agreement — <project name>
Contributor: <full legal name or entity name>
```

| Section | Purpose |
|---|---|
| **Definitions** | Three defined terms: Contribution (what the contributor submits), Project (what they contribute to), Contributor (who is agreeing). Defined exactly once. |
| **Grant of copyright license** | The specific copyright rights the Contributor grants the Project. Minimum: reproduce, prepare derivative works, publicly display, publicly perform, distribute. |
| **Grant of patent license** | Any patent rights the Contributor holds that are necessarily infringed by their Contribution, granted to the Project. Must include a defensive-termination clause: if the Contributor initiates patent litigation against the Project based on the Contribution, the patent license terminates. |
| **Representations** | The Contributor's representations that they have the right to make the Contribution — original authorship, employer consent where applicable, no conflicting agreements. Must be concrete, not vague ("I believe I have the right" is not sufficient). |
| **Scope** | What the agreement covers and what it explicitly does not — for example, that the Contributor retains copyright; that the agreement does not transfer moral rights in jurisdictions where these are inalienable. |

### Register and tone

Legal-plain. Defined terms are capitalised. Active voice where possible. Representations must be stated precisely — vague claims reduce enforceability and create ambiguity about what the Contributor actually represents.

### See also

- **Contract** (above)
- **License explainer** (below)
- **Terms** (below)
- [[language-protocol-substrate|Language Protocol Substrate]]

## Policy

> A policy states what is required, who is bound, and what happens when the rule is violated. Every sentence in a policy is either a rule or support for a rule.

A **policy** (LEGAL genre) is a binding statement of required behaviour within a defined scope. It differs from an ADR (which records a one-time architectural decision and its rationale — see [[architecture-decisions|Architecture Decision Records]]) and from a convention (which describes an agreed pattern). A policy names its rules, its enforcement mechanism, and its review cadence. This article is the human-facing standard; the machine-readable counterpart lives in `service-disclosure/templates/policy.toml`.

### When to use this template

Use a policy when:

- Behaviour must be uniform across a team, project, or organisation.
- Deviation has real consequences and those consequences need to be stated.
- The rule needs a review cadence so it does not silently go stale.

Do not write a policy for a preference or a guideline. A policy requires enforcement; a guideline carries the word "preferred" or "recommended" and does not.

### Structure

The template requires five sections in this order:

| Section | Purpose |
|---|---|
| **Scope** | Who and what this policy applies to. Named roles, systems, or contexts. Explicit about what it does not apply to. |
| **Policy** | The rules, numbered. Each rule is a complete, standalone statement. The first word is an obligation: "All X must…", "No Y may…", "Every Z is required to…". |
| **Enforcement** | What happens when a rule is violated. Must name a consequence or a process — not a vague "will be addressed." |
| **Review** | How often this policy is reviewed and by whom. Minimum annual. Policies in fast-moving domains review every six months. |
| **See also** | Links to the ADRs, conventions, or laws that this policy implements or is required by. |

### Register and tone

Legal-plain. Active voice. No hedges: a policy either requires something or it does not. "Should" and "encouraged" are not policy language — use "must" or "shall" for requirements, or move the statement to a convention.

Sentence-length budget: target under twenty-five words per rule. Numbered rules are paragraphs, not bullets — each stands alone. The Scope section must be precise enough that a new team member can determine, without asking, whether the policy binds them.

### See also

- [[architecture-decisions|SYS-ADR-07 — No AI on Structured Data]]
- **Architecture** (above)
- [[language-protocol-substrate|Language Protocol Substrate]]

## README

> A `README.md` is the first thing a collaborator or automated system reads when it enters a repository. It answers three questions in order: what is this, what do I need to know to use it, and where do I look next.

A **README** is the entry point for a repository or project directory. It is addressed to a reader who has no prior context — a new contributor, a review system, or an external collaborator encountering the repo for the first time. This article covers the human-facing standard; the machine-readable counterpart lives in `service-disclosure/templates/readme.toml`. The [[root-files-discipline|root files discipline]] governs which companion files may appear alongside the README at a repository root.

### When to use this template

Every repository root must carry a `README.md`. Projects inside a monorepo (`pointsav-monorepo/<prefix>-<name>/`) carry their own `README.md` at project root when the project is significant enough to be addressed independently. Thin adapters and single-file utilities do not require a separate project README — the repo-root README covers them.

Repositories with bilingual content (per workspace §6) also carry a `README.es.md` at the same level. Operational repos (internal tooling, deployment scaffolds) may defer the Spanish pair until a public-facing milestone.

### Structure

The template requires five sections in this order:

| Section | Purpose |
|---|---|
| **Opening** | One paragraph: what this repository or project is and who it is for. No headings before this paragraph — it appears immediately after any repo metadata. |
| **What this is** | What the repo contains or what the project does. Scope, not features. Two to four sentences. |
| **Layout** | An annotated directory tree or section listing. One phrase per entry. Describes structure, not behaviour. |
| **Using it** | The minimal sequence a new contributor needs to read, run, or build this repo's content. Prerequisites, then commands, then expected output. |
| **Where to look next** | A curated list of pointers to deeper documentation — ARCHITECTURE.md, CLAUDE.md, the relevant content-wiki TOPIC, the deployment guide. |

Optional sections (permitted at the end, after the required five): Contributing, Licence, Contact.

### Frontmatter fields

Repo-root `README.md` files carry no YAML frontmatter — they are plain Markdown for GitHub rendering. Project-root `README.md` files inside `pointsav-monorepo` also carry no frontmatter.

Content-wiki README-style articles (when a wiki article explains a README's design) use the standard `foundry-doc-v1` schema with `type: reference`.

### Register and tone

Plain English. Address the reader directly where helpful ("To build the crate, run…"). Avoid jargon that is not defined in the same document or available from a linked TOPIC. Mean sentence length around twenty words; nothing over forty.

The banned-vocabulary list applies. Do not use `"utilize"`, `"leverage"`, `"seamless"`, or `"robust"` in a README. State the actual behaviour, not the aspiration.

Bilingual pairs (`README.md` + `README.es.md`) are strategic adaptations, not translations. The Spanish version may restructure, shorten, or reframe for a different reader's context while carrying the same factual content.

### See also

- **Topic** (above)
- **Guide** (above)
- [[language-protocol-substrate|Language Protocol Substrate]]
- [[root-files-discipline]] — allowed companion files at a repository root

## Terms

> Terms of use state what a user may do with a service, what they may not do, and what the service owes them in return. Use constitutes acceptance.

**Terms of use** (LEGAL genre) are the binding rules that govern a user's access to and use of a service or site. They are published where users can read them before using the service — the opening clause makes clear that use of the service constitutes acceptance. Every terms-of-use document executed under this platform routes through `factory-release-engineering` governance for review before publication. This article is the human-facing standard; the machine-readable counterpart lives in `service-disclosure/templates/terms.toml`.

### When to use this template

Use terms of use when:

- A service or site is made available to users outside the Foundry workspace.
- The service's permitted and prohibited uses need to be on record.
- Liability limitations and warranty disclaimers need to be formally stated.

Internal tooling used only by workspace members does not require public terms of use — a **Policy** document covers internal-use obligations.

### Structure

The template requires an opening clause and five sections in this order:

**Opening clause** (before any heading): One sentence stating what service these terms govern and that use of the service constitutes acceptance of these terms.

| Section | Purpose |
|---|---|
| **Definitions** | Each defined Term, stated once. Capitalised after first definition. |
| **Acceptance** | How a user accepts the terms — by signing up, accessing the service, or clicking "I agree." What acceptance binds: the user to these terms; the service provider to the described service. |
| **Use of the service** | Permitted uses, prohibited uses, and the user's obligations (for example, account security, accurate registration). Numbered for traceability. |
| **Liability and disclaimers** | The warranty disclaimer and the limitation of liability. Must be in plain language: excessive legalese reduces enforceability. Standard formulations ("THE SERVICE IS PROVIDED 'AS IS'") may be used but must be followed by a plain-language equivalent. |
| **Changes to these terms** | How the terms may change, what constitutes notice to users, and the effective date of changes. |

Optional sections (at the end): Governing law and jurisdiction, Contact.

### Register and tone

Legal-plain. Active voice where possible. Every defined Term is capitalised on every use after its definition. Where the service touches investment or [[disclosure-substrate|disclosure]] material, forward-looking claims about service features or roadmap carry "planned / intended / may / target" language, in compliance with Canadian securities continuous-disclosure requirements.

### See also

- **Policy** (above)
- **Contract** (above)
- **CLA** (above)
- [[language-protocol-substrate|Language Protocol Substrate]]

## Ticket comment

> A ticket comment records a state change or a decision — not a thought. Every comment advances the ticket.

A **ticket comment** (COMMS genre) is a structured update on an issue, task, or work item. It is addressed to anyone who reads the ticket's history after the comment is posted. Unlike a **Chat message** (which is synchronous and ephemeral), a ticket comment is a permanent record and may be read months later by someone with no context from the thread. This article is the human-facing standard; the machine-readable counterpart lives in `service-disclosure/templates/ticket-comment.toml`.

### When to use this template

Write a ticket comment when:

- The status of the work has changed and stakeholders need to know.
- A decision was made that affects the ticket's scope, timeline, or owner.
- A blocker has been identified or resolved.
- An action was completed and the completion needs to be on record.

Do not comment to say you are working on the item — update the Status field instead. Do not post exploratory thoughts or half-formed questions as comments; draft them privately and post when the conclusion is clear.

### Structure

**Header block** (before any body text):

```
Ticket: <ticket-id or title>
Status: <new status — Open | In progress | Blocked | Review | Done>
```

| Section | Purpose |
|---|---|
| **What changed** | One to three sentences: the specific change in state, decision made, or fact established. Name the artifact, commit SHA, or decision explicitly. |
| **Next** | The concrete next step, with owner. A ticket comment with no "Next" is a dead end — the reader cannot act on it. If the ticket is Done, "Next" is "Closed." |

### Register and tone

Factual and brief. Past tense for what changed ("Committed X at hash Y"); present or future for next steps ("Owner: jw; due 2026-06-01"). No hedges — either the state changed or it did not.

Status field values are a closed set: `Open`, `In progress`, `Blocked`, `Review`, `Done`. No custom values.

Sentence-length budget: one to two sentences per section. If "What changed" needs more than three sentences, the change is complex enough to warrant a brief or a memo — reference it from the ticket comment rather than writing it inline.

### See also

- **Chat** (above)
- **Meeting notes** (above)
- [[language-protocol-substrate|Language Protocol Substrate]]

## Memo

> A memo records a decision, analysis, or recommendation addressed to a named audience. It is complete when the reader knows what was decided and what happens next — without reading anything else.

A **memo** (PROSE-MEMO genre) is an internal document addressed to a specific recipient for a specific decision or recommendation. It is not a status update, not a design document, and not a policy. A memo closes open questions; it does not catalogue them. For register and tone discipline applied to all prose artifacts, see [[editorial-language-registers]]. This article describes the human-facing standard; the machine-readable counterpart lives in `service-disclosure/templates/memo.toml`.

### When to use this template

Use a memo when:

- A decision has been reached and needs to be communicated with the analysis that led to it.
- A recommendation is ready for a named decision-maker and the recommendation cannot be delivered in a single paragraph.
- A complex cross-functional question is settled and the settlement needs to be on record.

Do not use a memo for ongoing discussion, for project status, or for questions that remain open. An open question belongs in an inbox message, a NEXT.md item, or a brief.

### Structure

The template requires a header block and five sections:

**Header block** (before any heading):

```
To:   <recipient name or role>
From: <author name or role>
Date: <YYYY-MM-DD>
Re:   <one-line subject — specific, actionable>
```

| Section | Purpose |
|---|---|
| **Summary** | The conclusion, stated first. One to three sentences: what was decided or recommended and the key constraint. The reader who reads only this section must be able to act on it. |
| **Context** | What precipitated the memo. The facts a recipient needs to evaluate the recommendation. Not the full history — only what is load-bearing. |
| **Analysis** | The reasoning. Structured as numbered points or short paragraphs. Acknowledges the strongest counterargument and explains why it was not decisive. |
| **Recommendation** | The specific action requested, with owner and timeline. A memo with no recommendation is a brief; restructure it accordingly. |
| **Next steps** | Concrete follow-on actions, owners, and dates. This is the section that gets executed. |

### Register and tone

Formal but plain. The register is professional prose, not legalese. State the recommendation before the analysis — readers at the recipient level do not need to reconstruct the conclusion from the evidence. The Subject (`Re:`) line must be specific: "Approve Q3 content freeze — 2026-08-15" rather than "Content freeze update."

Sentence-length budget: mean around twenty-two words, maximum forty. Active voice throughout the body. The Analysis section may use numbered points; the Recommendation and Next steps use imperative sentences.

The banned-vocabulary list applies. No `"leverage"`, `"facilitate"`, or `"synergize"` in professional correspondence — state the specific action directly.

### See also

- **Topic** (above)
- **Guide** (above)
- [[language-protocol-substrate|Language Protocol Substrate]]

## License explainer

> A license explainer translates a legal instrument into plain terms. It is not the license. If the explainer and the license conflict, the license wins.

A **license explainer** (PROSE genre) is a plain-language companion to a formal license document. It helps a reader understand what the license permits, requires, and forbids without having to parse legal text. An explainer is not legally binding — it is a reading aid. The binding text is always the formal license document linked from the explainer. For the governance layer that controls license propagation across repositories, see [[disclosure-substrate]]. This article is the human-facing standard; the machine-readable counterpart lives in `service-disclosure/templates/license-explainer.toml`.

### When to use this template

Write a license explainer when:

- A repository carries a license that affects contributors or consumers in non-obvious ways.
- The audience includes people who are not legal professionals.
- The license has conditions (attribution, share-alike, CLA requirement) that need to be understood to comply.

The explainer is not a substitute for legal review. For agreements that bind individuals or organisations to specific obligations, route through the responsible governance party (`factory-release-engineering` or the system administrator at `open.source@pointsav.com`) before publishing.

### Structure

The template requires five sections in this order:

| Section | Purpose |
|---|---|
| **Lede** | One to two sentences: what license this is and what it is designed to accomplish. No legal jargon. |
| **What it permits** | A bulleted list of what this license explicitly allows. Plain verbs: "Use commercially", "Modify the source", "Distribute copies". |
| **What it requires** | A bulleted list of conditions. Plain verbs: "Include the copyright notice", "State changes made", "Provide access to source". |
| **What it forbids** | A bulleted list of restrictions. Plain verbs: "Hold the author liable", "Use the trademark without permission". Omit this section if the license forbids nothing. |
| **Where binding text lives** | A direct link to the full formal license document and a statement that the formal text governs wherever the explainer and the formal text disagree. |

### Register and tone

Plain English. No "aforementioned," "notwithstanding," or "herein." The goal is comprehension, not impressiveness.

Sentence-length budget: mean around eighteen words, maximum thirty. Bullet items are imperative phrases beginning with a verb, not full sentences. The Lede may be two sentences maximum.

### See also

- **Policy** (above)
- **CLA** (above)
- [[language-protocol-substrate|Language Protocol Substrate]]

## Inventory

> An inventory is a timestamped count of what exists, what state it is in, and what type it is. It is not a plan and not a log.

An **inventory** (PROSE genre) is a point-in-time enumeration of items in a defined scope, organised to support classification and action. It differs from a registry (which is authoritative and updated continuously) and from a brief (which carries analysis and recommendation). An inventory is read; a registry is queried. For the [[citation-substrate|citation discipline]] that governs how inventories reference other documents, see the citation substrate. This article is the human-facing standard; the machine-readable counterpart lives in `service-disclosure/templates/inventory.toml`.

### When to use this template

Use an inventory when:

- A count is needed to understand the size of a migration, cleanup, or audit task.
- Items need to be classified and the classification itself is the deliverable.
- A snapshot is required before a structural change so the before-state is recorded.

Do not use an inventory as a living document. Inventories are snapshots — they carry a date, go stale, and are superseded by a new inventory when the scope changes materially. A living record belongs in a registry or a cleanup log.

### Structure

The template requires three sections:

| Section | Purpose |
|---|---|
| **Opening** | One paragraph: what scope was inventoried, as of what date, and what the count reveals at high level. |
| **Inventory table** | The enumeration. Columns: `Item` (canonical name), `State` (closed enum), `Type` (closed enum), `Notes` (short, max one clause). |
| **Summary** | Counts by state and type. Totals. May include a "next action" pointer if the inventory is the input to a migration or audit. |

An optional **Classification vocabulary** section follows the table when the State and Type enumerations are not self-evident. Define each value in one phrase.

### Inventory table discipline

- One row per item. No merged cells.
- `State` values come from a closed enum per domain (for example, `open | closed | deferred` for cleanup items; `active | dormant | archived` for projects).
- `Type` values come from the relevant taxonomy (Nomenclature Matrix entity types, genre families, etc.).
- Notes column: one clause maximum. If more than one clause is needed, the item requires its own entry in the cleanup log or brief.

### Register and tone

Factual. No interpretation in the table — the rows are observations, not recommendations. The opening paragraph may describe what the pattern suggests; the table itself does not.

Dates are ISO 8601. Canonical names from the Nomenclature Matrix throughout. No prose in the table beyond the Notes column.

### See also

- **README** (above)
- **Memo** (above)
- [[language-protocol-substrate|Language Protocol Substrate]]

## Changelog

> A changelog answers one question for every version: what changed, stated in one line, from the reader's point of view.

A **CHANGELOG.md** records meaningful changes to a repository at each version boundary. It is addressed to a reader who wants to know what a new version contains without reading a diff. A changelog is not a commit log — it selects, compresses, and reframes the commit history for a consumer who cares about impact, not implementation. The [[root-files-discipline|root files discipline]] governs when a CHANGELOG.md is required. This article is the human-facing standard; the machine-readable counterpart lives in `service-disclosure/templates/changelog.toml`.

### When to use this template

Every repository that carries version numbers uses a `CHANGELOG.md`. The file is created when the first meaningful entry exists — not as a placeholder. Repositories that do not version (pure content stores without a semantic version) may omit it; they track meaningful changes in `NEXT.md` or `cleanup-log.md`.

### Structure

The changelog is a flat list of version blocks, newest at the top:

```markdown
## M.m.P — YYYY-MM-DD

- <one-line entry, reader-facing>
- <one-line entry, reader-facing>

## M.m.P-1 — YYYY-MM-DD

- <one-line entry, reader-facing>
```

Each version block:

- Heading level `##`. Version number and ISO 8601 date on the same line.
- One bullet per meaningful change. Bullets are reader-facing: describe the effect, not the mechanism. "Adds X" rather than "Implemented the X module."
- Grouping labels (`### Added`, `### Fixed`, `### Changed`) are permitted when a version has more than five entries. Omit them when a version has five or fewer — grouping adds noise below that threshold.

### What counts as a changelog entry

Include:

- New capabilities available to consumers.
- Breaking changes to the public surface.
- Significant bug fixes with user-visible impact.
- Major structural changes (module split, rename).

Exclude:

- Internal refactors with no consumer-visible effect.
- Test additions or CI changes.
- Documentation-only commits (these are implicit in the version date).
- Version-bump commits (the heading captures this).

### Register and tone

Plain. Active voice, present tense: "Adds support for X", "Fixes the Y parsing failure." Not "We've added" or "This version includes." Not "Various improvements" — name what changed.

Sentence-length budget: one line per entry, target under twenty words. The date on the version heading uses ISO 8601 (`YYYY-MM-DD`). The version number follows the workspace versioning rule (MAJOR.MINOR.PATCH per workspace §7): PATCH increments per accepted commit; MINOR increments per feature milestone.

### See also

- **README** (above)
- **Architecture** (above)
- [[language-protocol-substrate|Language Protocol Substrate]]
