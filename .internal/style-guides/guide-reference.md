---
schema: foundry-doc-v1
title: "Reference guide — encyclopedic reference and explanation"
slug: guide-reference
category: internal
type: reference
content_type: reference
quality: complete
status: active
audience: contributor
bcsc_class: public-disclosure-safe
governs: [PROSE-TOPIC, PROSE-ARCHITECTURE, PROSE-RESEARCH, PROSE-TEXT, PROSE-README, PROSE-INVENTORY, changelog, DESIGN-RESEARCH]
last_edited: 2026-07-01
editor: pointsav-engineering
---

> The register guide for encyclopedic reference and explanation — the information-oriented
> prose a reader consults to look something up or reads to understand how a thing works.
> Builds on [[house-core]] and states only the reference specialization. Where this guide is
> silent, the house core governs.

## 1. Purpose and audience

A reader comes to this prose with a question, not a task. Reference is consulted, not read:
the reader arrives, takes the fact, and leaves, so the writing must be a firm platform —
certain, consistent, and free of doubt. Explanation is the same register read at leisure: it
develops *why* a thing works the way it does, and it earns room to make connections and weigh
alternatives, but it never tips into advocacy or procedure. Both halves share one discipline:
describe the subject; do not instruct, and do not sell. A reader who wants steps follows a
link to a how-to.

The primary reader is anyone consulting the platform's own record — an engineer, a reviewer,
an analyst. A second reader looks over their shoulder: a machine indexing the corpus for
retrieval, which rewards the same front-loaded, predictable structure the human scanner does.
If a definition is plain and unmemorable, it is probably right.

See [[guide-journal]] for JOURNAL manuscripts.

## 2. The shape

Most articles follow one order: **lead → context → the mechanism, section by section → limits
and relations → references.** The lead defines and situates; each body section develops one
part of the mechanism; the close names what the thing is *not* and links to what it connects
to. The "is not" section is load-bearing — a reference article that never draws its boundary
invites the scope creep it exists to prevent.

### Mirror the subject, standardize the type

Section order follows the subject's own structure — a service article walks its interfaces in
the order the system exposes them, not in the order they were designed. And every article of
the same type shares one skeleton: when all service articles carry the same sections in the
same order, a reader who has used one can navigate all of them without relearning the map.
Consistency across siblings is a feature of reference, not a constraint on it.

### Fixed shapes by artifact type

- **ARCHITECTURE** carries fixed sections in order: *position* (where it sits), *public
  surface* (what it exposes), *module layout* (how it decomposes), and *what this is not*
  (the boundary that prevents scope creep).
- **README** is orientation: a one-paragraph definition of the thing, how to enter it, and
  where to go next — the shortest article that still passes the isolation test.
- **INVENTORY and changelog** are structured records: the table or dated list *is* the
  payload, and prose is only its wrapper (§5).
- **RESEARCH / TEXT / DESIGN-RESEARCH** are explanation-forward. Each still opens with the
  claim, not the journey to it, and each stays *about* its subject — if the title would not
  survive an implicit "About …" prefix, the piece has drifted from explanation into
  something else.

## 3. Opening

Lead with a one-sentence definition, then establish significance — the house lead rule
([[house-core]] §Opening and the lead), applied at its tightest. The first sentence says what
the subject *is*, directly: "a write-once ledger is an append-only store whose records cannot
be altered after commit." Never route the definition through the word itself — "X refers to"
and "X is a term for" define the label instead of the thing, and the reader came for the
thing. And do not overload that first sentence with everything notable about the subject;
one clean predicate, then let the next sentences carry the stakes.

The isolation test for reference is exact: lift the lead out, and a reader who sees nothing
else must be able to state what the subject is and where it fits. A lead that opens on
history, motivation, or a narrative hook has buried its definition — front-load it. Reference
never teases: the most important fact appears first and is developed after, not hinted at and
revealed.

For an INVENTORY or changelog, the lead says what the record covers and how it is ordered;
the entries follow.

### Short description

Every reference article carries a curated `short_description` in frontmatter: one sentence,
roughly 120 to 180 characters, that a search result or category listing shows beside the
title. Write it keyword-first with no leading article, like a heading — the same casing and
filing discipline as [[house-core]] §Capitalization. It complements the title rather than
repeating it: state what distinguishes the subject, not a second copy of its name.
The Spanish pair carries its own, under the same rules.

> **Weaker:** "The article about how the platform's append-only ledger works."
> **Stronger:** "Append-only audit store whose committed records cannot be altered; anchors
> the platform's verifiable history."

## 4. Paragraph and sentence rhythm

House rhythm applies ([[house-core]] §Paragraph and sentence rhythm); the reference delta is
that facts of record dominate this register. A definition, a compliance claim, or a
structural invariant is a sentence the reader will rely on verbatim, so hold it to the house
fact-of-record target — and remember it is a target, not a gate: a claim that needs
twenty-eight words to be true takes twenty-eight.

The strongest section opener in this register is the definitional one-liner — a single
short paragraph that states the term, then a longer paragraph that develops it. Explanation
may run a slightly longer thread than pure reference while it develops a single mechanism,
but the moment the idea changes, the paragraph ends.

## 5. Headings and scannability

The house density band applies unchanged ([[house-core]] §Headings and scannability). The
reference delta is what the headings *say*: name each heading after the part of the mechanism
its section describes — "Heartbeat ingestion," "Placement algorithm," "Failure modes" — so the
heading skeleton reads as the subject's own anatomy. A reader scanning only the left margin
should come away with the structure of the thing.

### Structured records — the table is the payload

INVENTORY rows, changelog entries, a module map, options compared against criteria: this is
genuinely structured content, and here the table or dated list is the article's payload, not
an illustration of it. The prose wrapper does exactly three jobs — says what the record
covers, how it is ordered, and how to read the columns — and then stands aside. Keep column
sets identical across sibling records so a reader can compare them, and keep every row's
first cell a keyword, exactly as headings are.

The boundary runs both ways. Prose chopped into bullets to look scannable has stopped
explaining and started inventorying; a record narrated as paragraphs has hidden its data in
running text. Match the structure to the content, and commit to it.

## 6. Voice and tone

Neutral, exact, active. The register turns on the **neutral factual clause** — a statement a
reader can verify against the system, naming the actor and the consequence, carrying no
adjective the fact has not earned:

> The resolver rejects an unknown slug and renders it as a red link.

Every word of that sentence is checkable, which is why it is authoritative. Reference tone is
austere on purpose: certainty is the product, and an intensifier spends credibility that the
verifiable claim had already banked. State the specific number, the named mechanism, the
checkable property, and let significance follow from the fact.

Explanation admits perspective where reference does not — it may weigh a design against its
alternatives and say why the trade went the way it did. It does so in the same neutral
clause: "the design accepts slower writes to keep reads lock-free" weighs a trade-off as a
fact; "the elegant design wisely avoids locks" grades it. When a term of art appears, link to
its article at first mention rather than re-defining it in place. A capability not yet true
carries *planned* or *intended*; it is never asserted as done.

## 7. Code and examples

Explanatory prose is light on inline code. A mechanism is explained in words first; code
appears only when the words genuinely need it, introduced by a sentence that says what it
shows, and kept to the minimum that makes the point. An example in reference *illustrates
the description* — it shows the shape of a thing without sliding into instruction.

The reference-versus-how-to line is the rule here: if a reader would copy and execute the
block, it belongs in a how-to, and this article links to it. What stays inline is the short,
illustrative fragment — a schema shape, a signature, a one-line invariant — that clarifies
the idea without becoming a procedure.

## 8. Worked examples

**Buried lead to front-loaded definition.**

> *Before:* Deployment records refer to a concept that emerged after years of teams
> struggling with brittle scripts and manual handoffs.
> *After:* A deployment record is a versioned description of one running instance. It lets an
> operator recreate, audit, or retire that instance from a single file.

Annotation: "refers to a concept" defined the label, and the history buried the subject; the
definition now leads and the lead survives in isolation.

**Editorial to neutral factual clause.**

> *Before:* Impressively, the ledger never loses a write — a truly remarkable guarantee.
> *After:* The ledger is write-once: an appended entry is never modified or deleted.

Annotation: the judgment words are dropped and the guarantee becomes a property the reader
can check — which is what makes it authoritative.

**Narrated record to table payload.**

> *Before:* The fleet currently includes the controller, which listens on its own port and
> handles placement, as well as the host agent, which polls hardware, and also a tenant
> proxy that enforces quotas.
> *After:* Three services make up the fleet:
>
> | Service | Role |
> |---|---|
> | Fleet controller | Ingests heartbeats; advises placement |
> | Host agent | Polls node hardware; reports upward |
> | Tenant proxy | Authenticates callers; enforces quotas |

Annotation: three parallel facts escape the comma chain into a record the eye compares in one
pass; the prose shrinks to a one-line wrapper.

## 9. Pre-publish checklist

- Does the lead define the subject in its first sentence — no "refers to" — and survive the
  isolation test?
- Does the `short_description` distinguish the subject in one keyword-first sentence of about
  120 to 180 characters, with its Spanish pair?
- Does the section order mirror the subject's own structure, and does every heading name the
  mechanism its section describes?
- Is every claim a neutral factual clause — actor named, consequence stated, no adjective the
  fact has not earned?
- Does every term of art link once, at first mention, instead of being re-defined in place?
- Is inline code a short illustrative fragment, with anything a reader would execute linked
  to a how-to?
- For a structured record, is the table or list the payload, the prose only its wrapper, and
  the column set consistent with sibling records?
- Do the title, headings, slug, and short description follow the casing and leading-article
  rules in [[house-core]] §Capitalization?
