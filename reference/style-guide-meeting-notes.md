---
schema: foundry-doc-v1
title: "Style guide — meeting notes"
slug: style-guide-meeting-notes
category: reference
type: topic
quality: complete
short_description: "Editorial standards for meeting notes in the platform (COMMS genre): header fields, agenda discipline, decisions-versus-notes distinction, and the action-items table format."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-24
editor: pointsav-engineering
cites: []
paired_with: style-guide-meeting-notes.es.md
---

> Meeting notes exist for the action items and the decisions. Everything else is archive material.

**Meeting notes** (COMMS genre) record what was decided and what happens next in a meeting. They are not a transcript. A reader who was absent reads the notes to learn the outcome and their obligations — not to reconstruct the conversation. This article is the human-facing standard; the machine-readable counterpart lives in `service-disclosure/templates/meeting-notes.toml`.

## When to use this template

Use meeting notes for any meeting that produces decisions or action items. Short informal check-ins that produce neither do not need notes — a chat message to the channel suffices. Notes are required when:

- A decision is made that affects scope, timeline, or ownership of work.
- An action item is assigned to a named person.
- A question is left open and needs to be tracked to resolution.

## Structure

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

## Register and tone

Decisions are phrased as completed facts: "Agreed: X will ship on 2026-07-01" rather than "We discussed shipping X." Action items use imperative form ("Write the draft proposal") and name a specific owner. "TBD" is acceptable for due dates; "someone" is not acceptable for owners.

The Notes section is prose-minimal. It exists for context, not for narrative — do not transcribe the discussion.

Sentence-length budget: mean around twenty words for prose sections. The Decisions and Action items sections use fragments where clarity permits.

## See also

- [[style-guide-ticket-comment|Style Guide — Ticket Comment]]
- [[style-guide-memo|Style Guide — Memo]]
- [[language-protocol-substrate|Language Protocol Substrate]]
