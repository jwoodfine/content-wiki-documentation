---
schema: foundry-doc-v1
title: "Communications guide — announcements, correspondence, and notes"
slug: guide-communications
category: internal
type: reference
content_type: reference
quality: complete
status: active
audience: contributor
bcsc_class: public-disclosure-safe
governs: [COMMS-ANNOUNCEMENT, COMMS-PRESS, COMMS-CORPORATE, COMMS-EMAIL, COMMS-NOTES, PROSE-MEMO, chat, ticket-comment]
last_edited: 2026-07-01
editor: pointsav-engineering
---

> The register guide for institutional communications — announcements, press releases,
> memos, correspondence, meeting notes, chat, and ticket comments. Builds on [[house-core]];
> restates nothing there. One register runs the whole formality range: the reader gets the
> consequence first, whatever the container. What scales from a press release down to a
> one-line chat message is formality — never the register.

## 1. Purpose and audience

A communication moves a decision, a fact, or a request from the writer to a reader who will
act on it. The reader is busy and reading to answer one question: what happened, or what do I
need to do? Everything in the message serves that question or is cut.

The register is institutional: precise, professional, consequence-first — the opposite of
marketing. The second reader is the one this message is forwarded to without its context;
write so the point survives the forward. The third is the reader who relies on the message
under disclosure rules: what is not yet true is framed as not yet true, in every genre down
to chat.

## 2. The shape

Every genre here is an inverted pyramid: the most important sentence first, then detail in
strictly descending order of importance. The test is the cut — remove the last paragraph,
then the one above it, and what remains is still true, complete, and actionable. A message
that fails the cut has its point sitting too low.

One spine, scaled per genre:

- **Subject up top** — the reader knows the topic before the first sentence.
- **Point in the first line** — the decision, the fact, or the ask.
- **Support in descending importance** — context and specifics, most consequential first.
- **Ask or next step** — who does what by when, or "no action needed" stated plainly.

Per-genre deltas:

- **Announcement / press** — headline in sentence case, keyword first; a dated lead that
  answers who, what, when, where, and why in one or two sentences; body in descending
  importance; a closing organization paragraph of at most 100 words, factual and in the
  third person, written so a republisher can lift it verbatim.
- **Memo** — the decision, then the rationale, then options considered in a line each, then
  who does what by when. One decision per memo; a second decision is a second memo.
- **Email** — one topic per message; the ask in the first two lines; everything below the
  fold is optional reading.
- **Meeting notes** — decisions, actions, open questions. Never a transcript.
- **Chat / ticket comment** — one point, actionable, no throat-clearing. A ticket comment
  records a state change: what was done, what was found, what happens next.

## 3. Opening

The conclusion opens; the background follows. A communication has no warm-up: the reader
learns the outcome, the decision, or the request before any context arrives — the
bottom-line-first convention institutional and military correspondence standards converged
on, because the reader is deciding, not browsing.

For an announcement, the lead is a dated statement of fact: what is true, as of when. For a
memo, sentence one is the decision. For an email, the subject carries the topic and the first
two lines carry the ask. For a note or a comment, the first clause is the whole point.

The isolation test here is the forward test. A reader who receives only the subject and the
first line — the exact view a preview pane or a hurried forward provides — knows what
happened and whether they must act. If the ask is below the fold, the opening has failed.

One calibrated exception: news with direct human consequence takes a single sentence of
framing before the point, so the point lands as information rather than alarm. One sentence.
The exception never grows into a warm-up.

## 4. Paragraph and sentence rhythm

External communications target 14 to 18 words a sentence — tighter than an explanation,
because a reader scanning for the ask should not wade through subordinate clauses. The
point-carrying sentence comes first and stays short.

Internal notes, chat, and ticket comments run shorter still — often a single sentence is the
whole message. Length signals importance, so do not pad a small message to look substantial,
and do not compress a consequential one to look casual.

## 5. Headings and scannability

Short genres carry no headings — an email, a chat message, a ticket comment are too small to
section. A memo or a longer announcement uses a few sentence-case headings: the decision, the
rationale, the actions.

### Subject line as the smallest heading

The subject line works harder than any heading: it is read in a truncating preview, sorted in
a crowded list, and searched months later. Keyword first, no leading article, roughly six to
ten words — preview panes cut the tail at around forty characters, so the words that identify
the message go first and filler goes nowhere. Where the genre allows, classify the message in
the first word: "Decision — provisioning moves to Thursday"; "Action by Thursday — approve
the window"; "FYI — search index rebuilt". The same rule governs a `short_description`
field wherever an artifact carries one: it is a subject line for an index, and every surface
that displays it truncates the tail, never the head.

### Meeting notes as structure

Meeting notes are structure, not prose: a short decisions list and an owner–action–date table
beat paragraphs a reader must mine for their name. Every action row names one owner — an
action with two owners has none — one verb, and one date. Publish notes while the decisions
are still warm, ideally the same day; notes that arrive a week late document a meeting nobody
remembers agreeing to.

## 6. Voice and tone

The move this register turns on is the consequence-first sentence: the reader learns the
result, then the reason.

> The provisioning window moves to Thursday; the migration needs one more validation pass.

Result first, cause second, no adjectives doing the work a fact should do. The institutional
tone is built from named facts and dates, not intensifiers — the positive alternative to hype
is always the specific, verifiable claim.

**Quote discipline.** A quote earns its place by carrying what a fact paragraph cannot: a
commitment, a judgment, a reason only its speaker can stand behind. Attribute every quote to
a named person or role, with the role stated at first reference, and let *said* do the
attribution — the neutral verb keeps the weight on the words. A quote that only adds
enthusiasm is replaced by the fact the enthusiasm was about.

**Forward-looking and disclosure posture.** Present facts go in the present tense. Anything
not yet true — a capability, a date, an outcome — carries *planned*, *intended*, *may*, or
*target*, with a reasonable basis. External announcements in regulated contexts carry the
cautionary framing the disclosure posture requires; see [[house-core]] for the base rule.
Never state a target as an accomplishment, and never give a system or the organization an
intent it does not have.

## 7. Code and examples

Communications generally carry no code. The exception is a ticket comment or a chat message
where a command is the clearest answer — fence it and keep it to the one command, with no
surrounding explanation the reader did not ask for. Longer procedures do not belong in a
message; link to the guide that carries them.

## 8. Worked examples

**Buried ask → subject and ask first.**

> Weaker: *Subject: Following up.* Following up on our earlier thread about the staging
> environment and the various validation steps we discussed, I wanted to circle back —
> could you approve the window?
> Stronger: *Subject: Action by Friday — approve Thursday provisioning window.* Please
> approve the Thursday provisioning window by end of day Friday. Context: the migration
> needs one more validation pass, which pushes us from Wednesday.

*The subject now classifies and identifies the message inside preview length; the ask and
its deadline are the first line; the context that was blocking the ask now supports it.*

**Hype and empty quote → dated fact and working quote.**

> Weaker: We're thrilled to unveil a game-changing platform that redefines what's possible.
> "This is a huge milestone for us," the team said.
> Stronger: On 1 July 2026 the organization released version 2 of the platform, adding
> federated search across all three content repositories. "Search was the most requested
> capability this year; version 2 closes it," said the platform lead.

*The feeling became a date and a named capability, and the quote now carries a fact and a
judgment its speaker owns, attributed to a role.*

**Meeting-notes transcript → decisions and owners.**

> Weaker: We talked for a while about the queue and then discussed whether to move the
> deadline, and there were a few opinions, and eventually it seemed like Thursday made sense.
> Stronger: Decision — provisioning moves to Thursday. Action — operator confirms the
> window by Wednesday noon. Reason — one more validation pass required.

*Kept the decision, one owner with one verb and one date, and the reason; dropped the
discussion a reader does not need to re-live.*

## 9. Pre-publish checklist

- Does the reader learn the point from the subject and first line alone — the forward test?
- Does the message survive the cut, paragraph by paragraph from the bottom?
- Is the ask — or "no action needed" — in the first lines, with one owner and a date?
- Does the subject or `short_description` lead with its keyword, fit a truncating preview,
  and carry no leading article (*the/a/an*)? (see [[house-core]] §Capitalization)
- Does every sentence carry a fact or a date, not an intensifier standing in for one?
- Is anything not yet true framed as planned, intended, may, or target?
- Does every quote carry a fact or a commitment, attributed to a named role?
- Do meeting notes record decisions and owner–action–date rows rather than the discussion?
