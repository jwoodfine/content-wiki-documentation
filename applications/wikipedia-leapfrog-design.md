---
schema: foundry-doc-v1
title: "Wikipedia leapfrog design — muscle memory and 5% headroom"
slug: wikipedia-leapfrog-design
short_description: "What the app-mediakit-knowledge wiki engine inherits from Wikipedia, what it adds beyond it, and what the 5% leapfrog headroom means for readers and engineers."
category: applications
type: topic
content_type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: wikipedia-leapfrog-design.es.md
cites: [ni-51-102, osc-sn-51-721]
---

# Wikipedia leapfrog design — muscle memory and 5% headroom

The [[app-mediakit-knowledge]] wiki engine inherits 95% of its chrome from Wikipedia's established layout conventions. The remaining 5% is leapfrog headroom: additions that no Wikipedia reader has encountered, shipped as additive features so the baseline reading experience is undisturbed. This article explains why each design choice was made and what the structural contract with two different audiences looks like.

---

## The muscle-memory contract

### Why Wikipedia patterns are the market-entry mechanism

Wikipedia has approximately two billion monthly readers. Those readers have developed navigational reflexes over two decades of exposure to a specific chrome — the location of tabs, the structure of article sections, the visual language of footnotes and hatnotes, the collapsible left-rail table of contents. These reflexes are not brand loyalty; they are motor programs.

A new knowledge-publication substrate faces a structural choice. It can differentiate its chrome from Wikipedia, forcing readers to learn new navigational motor programs before they can work efficiently. Or it can adopt the same chrome, accepting brief initial confusion in exchange for zero onboarding friction.

The substrate adopts the second path, with one qualification: the adoption is principled, not superficial. A principled adoption identifies the exact set of patterns that carry the muscle memory and holds them inviolable.

### The 95% / 5% allocation

95% of the chrome is the Wikipedia muscle-memory inventory, held inviolable across all phases. 5% is the leapfrog headroom — additions that are additive rather than replacements, so the baseline experience is undisturbed for readers who do not attend to the additions.

The Vector 2022 skin — Wikipedia's current production skin — provides the template. A 2025 study found the Vector 2022 redesign drove pageviews up 1.25% and internal link clicks up 1.06 million monthly, with no significant disruption, by following additive discipline: nothing was removed from the existing experience. The substrate follows the same discipline.

### What was kept

The eighteen sacred patterns catalogued in the engine's UX design specification include: the Article / Talk tab pair at the top-left of the title row; Read / Edit / View history tabs at the top-right; per-section edit pencils on every heading; end-of-article ordering (See also, Notes, References, Further reading, External links, Categories); hatnotes for disambiguation; the bolded subject plus copula lead sentence; a collapsible left-rail table of contents that follows the reader on scroll; the language switcher next to the title; footnote conventions using bracketed superscripts with back-arrow reference lists; infobox right-rail capability; blue unvisited / purple visited / red missing-target link colours; body typography at 17 px minimum with line-height 1.5 or greater and a 45–75 character line length; the centre-top search placeholder; and mobile chrome with a hamburger button and sections collapsed by default.

---

## What was added beyond Wikipedia

Five additions ship beyond the Wikipedia inventory. Each is additive — no existing Wikipedia muscle-memory pattern is removed or altered.

### Citation badges

Next to every inline citation reference, the chrome renders a small badge in the C2PA Content Credentials (CR) pin glyph convention. The badge defaults to neutral grey. This follows the lesson of the TLS padlock: in May 2023, Chrome removed the green padlock because 89% of users misread the positive state as "this site is trustworthy" rather than "the connection is encrypted." A positive-state signal that is ubiquitous becomes noise. Citation badges follow the same calibration: neutral grey for all-verified, amber for source drift, red for a missing or hash-mismatched citation, blue for forward-looking information. The verified-green state appears only when a reader explicitly toggles the "show all verified marks" density setting.

This addition does not interfere with footnote conventions. The badge appears at clause end, next to — not replacing — the existing `[n]` footnote superscript.

### Forward-looking information banner

Articles whose frontmatter sets `forward_looking: true` render a cautionary banner in reading view. The banner is the reading-surface expression of [[compliance-and-continuous-disclosure|continuous-disclosure requirements]] under [ni-51-102] and [osc-sn-51-721]: forward-looking information must be labelled, carry a stated reasonable basis, and include material assumptions and cautionary language. The banner appears below the article title in reading view, distinct in colour from the body, and does not interfere with the hatnote or lead sentence.

### Disclosure class field

Articles carry a `disclosure_class` field in frontmatter with three values: `narrative`, `financial`, `governance`. In the current phase this field is invisible to readers — it appears in the JSON-LD structured data in the rendered article's `<head>` block. A planned linter will check that articles classified as financial carry an iXBRL block and that articles with `forward_looking: true` carry the required cautionary language patterns.

### IVC masthead band placeholder

A single horizontal strip below the title row. In the current phase this band renders placeholder text indicating that verification is not yet available. A planned future phase is intended to fill the band with a live verification summary: the count of claims in the article, the count verified, and the time since the last drift check. The band's structural location is established now so the template is not restructured when the verification machinery ships.

### Reader density toggle

A preference control with three states: Off, Exceptions only (default), All. The setting persists across sessions. In the default state, neutral grey marks are rendered at low visual weight and coloured exception marks (amber, red, blue) are prominent. The All state renders verified-green marks alongside exception marks, for readers who want the full verification picture. The Off state provides the pure Wikipedia reading experience.

---

## Deliberate visual-identity divergence

The substrate adopts Wikipedia's ergonomic patterns — where tabs, tables of contents, and headings are located — while diverging at every point where divergence does not cost ergonomic familiarity.

Colour, typeface, logo, and wordmark are brand assets, not navigational affordances. These are the points of deliberate divergence. The PointSav house colour palette applies to all chrome elements: tab bar background, active state indicators, sidebar background, and footer band.

Link colours honour the blue / purple / red visited-state convention, because this convention is navigational, not brand — readers have learned to interpret link colour state across every browser that uses default link colours. The specific blue, purple, and red are in the PointSav house palette, not Wikipedia's exact values.

Body typography follows the same values as Vector 2022 because those values are correct, not because Wikipedia specified them. The 17 px body size, 1.5 or greater line-height, and 45–75 character line length derive from decades of typographic research into reading comfort. Wikipedia adopted them for the same reason.

A reader who arrives at documentation.pointsav.com and has spent years reading Wikipedia navigates immediately. They do not mistake the site for Wikipedia. The visual identity is distinct; the navigational identity is familiar.

---

## Why both audiences feel at home

A financial-community reader arrives via a link to a specific article. They see a title, article and talk tabs at the top left, read and edit and view history tabs at the top right. A bolded subject line opens the article body. A hatnote cross-references related articles. Footnotes appear inline and resolve at the bottom of the article. They have never visited this site before; they navigate without friction because they have navigated this structure thousands of times on Wikipedia.

An engineering reader has the same navigational experience, and also notices the JSON-LD `TechArticle` profile in the page source, the stable URL slug corresponding to a Markdown filename in a Git repository, and the `/feed.atom` endpoint advertised in the page header. Both readers are at home without having learned a new paradigm.

---

## Forward reference — the 5% leapfrog headroom

The following items are intended or planned for later phases. No specific delivery dates are stated. Material changes to the delivery plan would be recorded in the engineering phase plan documents and the workspace changelog, in accordance with [ni-51-102] continuous-disclosure obligations.

**Per-claim cryptographic verification badges** (planned): the inline badge system described above, intended to be wired to a content-addressed federation layer in a future phase. The masthead band placeholder and reader density toggle ship as structural locations now; the machinery intended to fill them is planned for a later phase.

**Real-time collaborative editing** (opt-in): the CRDT implementation ships behind a `--enable-collab` flag. Intended for trusted multi-user deployments where multiple authors edit the same article simultaneously with shared cursor awareness. Git remains canonical; the CRDT is intended as session-ephemeral state that serialises to a commit on explicit save.

**Mobile editor**: a mobile-first edit surface is intended for a later phase. The current editor is desktop-first.

**Citation-graph navigation**: intended affordances for navigating "what this article cites" and "what cites this article", planned for after the redb wikilink graph ships.

**Semantic browse**: "articles like this" and "concepts adjacent to this" surfaced from the citation graph, not from an inference model in the read path. Intended as a complement to category browse.

---

## See also

- [[app-mediakit-knowledge]] — the wiki engine that implements this leapfrog design
- [[knowledge-wiki-home-page-design]] — the home page design intent and Wikipedia conventions applied
- [[source-of-truth-inversion]] — the canonical/view/ephemeral pattern that underpins the engine's editorial posture
- [[substrate-native-compatibility]] — the rationale for the substrate-native API surface over a MediaWiki shim
