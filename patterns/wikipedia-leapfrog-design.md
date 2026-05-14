---
schema: foundry-doc-v1
title: "Wikipedia Leapfrog Design"
slug: wikipedia-leapfrog-design
category: patterns
type: topic
quality: complete
short_description: "The design narrative behind app-mediakit-knowledge's chrome — what was kept from Wikipedia, what was added beyond it, the deliberate visual-identity divergence, and what the 5% leapfrog headroom means for both readers and engineers — built on a 95%/5% muscle-memory contract that adopts Wikipedia's load-bearing patterns and extends only where the substrate has structural advantage."
status: active
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
last_edited: 2026-05-14
editor: pointsav-engineering
paired_with: wikipedia-leapfrog-design.es.md
cites:
  - ni-51-102
  - osc-sn-51-721
references:
  - id: 1
    text: "Vector 2022 — Wikipedia skin documentation."
    url: "https://en.wikipedia.org/wiki/Wikipedia:Vector_2022"
  - id: 2
    text: "Krämer, J. et al. Measuring the Impact of Wikipedia's Vector 2022 Skin. MDPI Informatics 2025."
    url: "https://www.mdpi.com/2227-9709/12/3/97"
  - id: 3
    text: "Chromium Blog — An update on the lock icon. May 2023."
    url: "https://blog.chromium.org/2023/05/an-update-on-lock-icon.html"
  - id: 4
    text: "BBC Verify — editorial verification initiative."
    url: "https://en.wikipedia.org/wiki/BBC_Verify"
---

The design narrative behind `app-mediakit-knowledge`'s chrome: what was kept from Wikipedia, what was added beyond Wikipedia, the deliberate visual-identity divergence, and what the 5% leapfrog headroom means for both readers and engineers. The chrome inventory lives at [[app-mediakit-knowledge]] §4 — what the chrome contains. This article explains why each choice was made, and what the structural contract with two different audiences looks like. The contract is 95%/5%: the substrate adopts Wikipedia's load-bearing patterns wholesale and extends only where it has structural advantage Wikipedia's volunteer-governance model cannot reach.

## The muscle-memory contract

### Why Wikipedia patterns are the substrate's market-entry mechanism

Wikipedia has approximately two billion monthly readers. Those readers have developed navigational reflexes over two decades of exposure to a specific chrome — the location of tabs, the structure of article sections, the visual language of footnotes and hatnotes, the left-rail table of contents. These reflexes are not brand loyalty; they are motor programs. A reader of any Wikipedia article navigates without thinking about navigation.

When a new knowledge-publication substrate enters this environment, it faces a structural choice. It can differentiate its chrome from Wikipedia — building a visual identity distinct enough that readers know immediately they are looking at something new. The cost of that choice is that readers must learn new navigational motor programs before they can work efficiently. Or it can adopt the same chrome, accepting that some readers will briefly experience it as a Wikipedia instance, in exchange for zero onboarding friction.

The substrate's choice is the second path, with one important qualification: the adoption must be principled, not superficial. A superficial copy fails the first time a reader looks for an affordance that the original had but the copy omitted. A principled adoption identifies the exact set of patterns that carry the muscle memory and holds them inviolable.

### The 95%/5% contract

`UX-DESIGN.md §3` names the structural allocation: 95% of the chrome is the Wikipedia muscle-memory inventory, held inviolable across all phases; 5% is the leapfrog headroom — additions that no Wikipedia reader has encountered, shipped as additive rather than replacements, so the baseline experience is undisturbed for readers who do not attend to the additions.

The Vector 2022 skin — Wikipedia's current production skin — provides the template.[^1] The Vector 2022 redesign process was deliberate about additive discipline: the community RfC showed 165 oppose, 153 support, yet the deployment proceeded because the close found rough consensus that nothing had been removed from the existing experience. A subsequent MDPI 2025 study found the redesign drove pageviews up 1.25% and internal link clicks up 1.06 million monthly, with no significant external referral disruption.[^2] The data supports additive. The substrate follows the same discipline.

### What was kept — the Phase 1 / Phase 1.1 split

The eighteen sacred patterns catalogued in `UX-DESIGN.md §1` are the inventory. The engineering delivery splits across two phases:

**Phase 1 (shipped)** covers items where the muscle memory is expressed in render output rather than chrome structure: footnote convention (item 4, bracketed superscript plus back-arrow reference list), infobox right-rail capability (item 7), link colours (item 10, blue unvisited / purple visited / red missing target), body typography (item 11, serif stack, body at minimum 17px, line-height 1.5 or greater, 45–75 character line length), centre-top search placeholder (item 13), and mobile chrome (item 16, hamburger left, sections collapsed by default, infobox stacked under lead).

**Phase 1.1 (additive over Phase 1)** covers the chrome elements that require structural additions to the template layer — the items a reader interacts with by clicking rather than by reading:

- Article / Talk tab pair (item 1), positioned at the top-left of the title row
- Read / Edit / View history tabs (item 2), positioned at the top-right of the title row, in that order
- Per-section `[edit]` pencils (item 3), right-floated on every heading
- End-of-article ordering (item 5): See also, Notes, References, Further reading, External links, Categories — the Wikipedia Manual of Style Layout sequence, because readers have learned to find citations at the bottom and that expectation should be met
- Hatnote (item 6), italic and indented, at the top of the article body above the infobox in source order, for disambiguation and cross-references
- Lead first-sentence convention (item 8), bolded subject plus copula plus one-line definition — the pattern that lets a reader identify the subject of any article within two seconds of arriving
- "From PointSav Knowledge" tagline (item 9), rendered under the article title in the Vector 2022 tagline element
- Collapsible left-rail table of contents (item 12), following the reader on scroll — the biggest visible structural change from Vector 2022, retained because it increased internal link clicks
- Language switcher (item 14), as a button next to the title, not buried in the sidebar — the Vector 2022 placement that reduced the friction of switching to the Spanish sibling
- Footer convention (item 15): categories, licence notice, About / Contact links

Phase 1.1 also ships two IVC chrome placeholders — visual surfaces that carry no machinery in Phase 1.1 but establish the structural location that Phase 7 is planned to fill.

## What was added beyond Wikipedia

Five additions ship beyond the Wikipedia inventory. Each is additive — no existing Wikipedia muscle-memory pattern is removed or altered. The additions appear at locations and in visual registers that do not interfere with the base reading experience. A reader who never attends to any of them receives the Wikipedia experience they expected.

### Citation badges

Next to every inline `[citation-id]` reference, the chrome renders a small badge in the C2PA "CR" pin glyph convention. The C2PA Content Credentials mark is shipping in Adobe's Content Authenticity application and on consumer devices; it carries growing visual literacy without requiring the substrate to invent a new symbol.

The default colour is neutral grey. This is the critical design decision, taken directly from the TLS padlock lesson: Chrome removed the green padlock in May 2023 because 89% of users misread the positive state as "this site is trustworthy" rather than "the connection is encrypted."[^3] When a positive-state signal is ubiquitous, it becomes noise; only the exception deserves colour. Citation badges follow the same calibration: neutral grey for all-verified, amber for source drift, red for a missing or hash-mismatched citation, blue for forward-looking information. The positive state (verified green) appears only when the reader has explicitly toggled the "show all verified marks" density setting.

This addition does not interfere with footnote conventions (item 4 in the inventory). The badge appears at clause end, next to — not replacing — the existing `[n]` footnote superscript. A reader who ignores badges reads footnotes exactly as before.

### FLI banner pattern

Articles whose frontmatter sets `forward_looking: true` render a cautionary banner in reading view. In authoring view, the SAA editor renders a blue squiggle on forward-looking statements that lack the frontmatter flag, prompting the author to add it.

The banner is sourced from BCSC continuous-disclosure posture: NI 51-102 and OSC Staff Notice 51-721 require that forward-looking information be labelled, carry a stated reasonable basis, and include material assumptions and cautionary language. The banner is the reading-surface expression of that requirement. An article about planned or intended future capability that sets `forward_looking: true` carries the banner as structural transparency, not as an editorial judgment.

This addition appears as a visual band immediately below the article title in reading view, distinct in colour from the body, with a formulaic cautionary sentence. It does not interfere with the hatnote (item 6) or the lead first-sentence (item 8), both of which appear below the banner in source order.

### BCSC disclosure_class field

Articles carry a `disclosure_class` field in frontmatter with three enumeration values: `narrative`, `financial`, `governance`. In the current phase this field is invisible to readers — it is expressed in the JSON-LD structured data in every rendered article's `<head>` block, where structured data parsers can consume it, but it does not appear as visible chrome.

Starting in Phase 8, a frontmatter linter is planned to check that articles classified `disclosure_class: financial` carry an iXBRL block, that articles with `forward_looking: true` carry the cautionary language patterns, and that any third-party governance claims appear with documented `cites:` resolution. The field is invisible today and consequential at Phase 8. It does not interfere with any Wikipedia muscle-memory pattern because it has no visible reading-surface expression until the Phase 8 linter activates.

### IVC masthead band placeholder

A single horizontal strip at the top of every article, below the title row. In Phase 1.1 this band renders placeholder text indicating that verification is not yet available. Phase 7 is planned to fill the band with a live verification summary line: the count of claims in the article, the count verified, and the time since the last drift check.

The structural logic follows the same pattern as BBC Verify's branded byline approach — a single line in the page chrome that gives the reader an at-a-glance trust signal without distributing per-claim marks throughout the prose.[^4] The masthead band is the location where the positive verification state lives, reserving the inline badge colours for exceptions only. That structural split — positive signal in the chrome band, exception signals inline — is the design that makes the IVC system legible without becoming visual noise.

The Phase 1.1 placeholder band occupies the location now so that the template is not restructured at Phase 7. Phase 7 replaces the placeholder text with live data; the band's position, size, and colour register are not intended to change.

### Reader density toggle

A preference with three states: Off, Exceptions only (default), All. The setting persists across sessions. In Phase 1.1 the preference is stored but has no effect on the chrome because the IVC machinery (Phase 7) does not yet exist.

- **Off** — no IVC marks in the chrome; the pure Wikipedia reading experience for readers who do not want the verification layer
- **Exceptions only (default)** — neutral grey marks rendered at low visual weight; coloured exception marks prominent
- **All** — verified-green marks rendered alongside exception marks; for auditors, regulators, and power readers who want the full verification picture

The default is Exceptions only — the operationalisation of the TLS padlock lesson at the substrate layer: the baseline reading experience suppresses the positive signal, showing only deviations from the expected verified state. This addition appears in the user preferences interface and does not interfere with any reading-surface Wikipedia pattern.

## The deliberate visual-identity divergence

### Muscle memory, not literal mimicry

The substrate's adoption of Wikipedia chrome is principled, not imitative. The principle: inherit the ergonomic substrate of the muscle memory; diverge visually at every point where divergence does not cost ergonomic familiarity.

The ergonomic substrate is the spatial and typographic structure that trained two decades of navigational reflexes: where the tabs are, where the table of contents is, where headings fall, how footnotes are numbered. A reader navigates by these structural landmarks. Changing their position costs the muscle memory; leaving their position unchanged preserves it.

Colour, typeface, logo, wordmark — these are brand assets, not navigational affordances. A reader does not navigate to a footnote by its colour. A reader does not find the table of contents by recognising a wordmark. These elements are the points of deliberate divergence.

### What is tracked from Vector 2022

The substrate tracks Vector 2022's typography and spacing discipline because these are ergonomic, not brand:

- Body text at minimum 17px (Wikipedia moved from 14px in 2023; the MDPI study found this contributed to the pageview gain)
- Line-height 1.5 or greater for body paragraphs
- 45 to 75 character line length — the decades-old typographic consensus for comfortable sustained reading, consistent with the Bringhurst tradition and the Nielsen Norman Group research on reading comfort
- Serif / sans-serif choice appropriate to the content register

These numbers are not Wikipedia's inventions. They derive from decades of typographic research. Wikipedia adopted them because they are correct. The substrate adopts them for the same reason.

Vector 2022's content-column width (approximately 960 px maximum) is tracked because it reflects the same character-count reasoning at typical screen sizes. The substrate does not reproduce Vector 2022's exact pixel values as a deference to Wikipedia; it uses values that satisfy the same typographic criteria.

### What is deliberately divergent

The PointSav house colour palette applies to all chrome elements: tab bar background, active-state indicator, link underline colour, section heading colour, sidebar background, footer band. These are the visual surfaces a reader sees as colour, not as structure. The colour is distinctly not Wikipedia grey and Wikipedia blue.

Link colours honour the blue / purple / red visited-state convention (item 10 in the muscle-memory inventory), because this convention is navigational, not brand — readers have learned to interpret link colour state across every browser and every website that uses default link colours. The specific blue, purple, and red are in the PointSav house palette, not Wikipedia's exact hex values.

No Wikimedia logo. No Wikipedia wordmark. No Vector 2022 stylesheet is linked or loaded. The chrome is implemented in the substrate's own CSS bundle, which satisfies the same typographic and spatial criteria as Vector 2022 because those criteria are correct.

A reader who arrives at `documentation.pointsav.com` and has spent years reading Wikipedia will immediately know how to navigate. They will not mistake the site for Wikipedia. The visual identity is distinct; the navigational identity is familiar.

## Why both audiences feel at home

### The financial-community reader

A reader arriving from the financial community — an analyst, an investor, a regulatory observer — arrives at `documentation.pointsav.com` via a link to a specific article. They see a title, a tagline, article and talk tabs at the top left, read and edit and view history tabs at the top right. A bolded subject line opens the article body. A hatnote above the lead paragraph cross-references related articles. Footnotes appear inline and resolve at the bottom of the article. Categories appear in a footer band.

They have never visited this site before. They have not been given a tutorial. They navigate without friction because they have navigated this structure thousands of times on Wikipedia.

The IVC masthead band is present — in Phase 1.1 it indicates that verification is not yet available; Phase 7 is planned to replace it with a claim-count verification summary. This reader understands what a news organisation's branded verification label looks like. They do not need to understand what IVC means technically to form an intuition that the site takes sourcing seriously.

The `disclosure_class` field is invisible to this reader in Phase 1.1. When the Phase 8 linter activates, articles classified as financial or governance are intended to carry structural markers that this reader's professional context has trained them to recognise: iXBRL for financial-statement content, forward-looking-information banners for content that describes plans rather than facts.

### The engineering reader

The same reader with an engineering background arrives at the same article and has the same navigational experience. They also notice things the financial-community reader may not attend to.

In the article's page source, `<script type="application/ld+json">` carries a Schema.org `TechArticle` profile. The article URL slug is stable and corresponds to a Markdown filename in a Git repository. The `/feed.atom` endpoint is advertised in the page header. An `/llms.txt` file at the site root maps the corpus structure for machine crawler ingestion.

In Phase 4, when the MCP server is planned to be live, the engineering reader can point any MCP-compatible agent at the wiki's MCP manifest and interact with the corpus programmatically — searching topics, fetching revisions, proposing edits, navigating backlinks — all through the same structured interface that the substrate is intended to expose natively.

In the edit surface, the engineering reader sees `[[wikilink]]` syntax, the same as Wikipedia's convention. They see a CodeMirror 6 editor they already recognise from comparable tooling. They see the substrate squiggle lint markers that cite the rule they are enforcing.

Both readers are at home. Neither had to learn a new paradigm.

## Forward reference — the 5% leapfrog headroom

The 5% leapfrog headroom enumerated in `UX-DESIGN.md §3` covers capability additions that no surveyed knowledge-publication system ships as of 2026. Each item below is *intended* or *planned* for later phases; no specific timelines are stated.

**Per-claim cryptographic verification badges** (IVC, Phase 7 planned) — the inline badge system described above, wired to the Phase 7 content-addressed federation seam. The masthead band placeholder and reader density toggle ship as structural locations in Phase 1.1; the machinery intended to fill them is planned for Phase 7.

**Real-time collaborative editing** (Phase 2 Step 7, opt-in) — the `y-codemirror.next` and Yjs CRDT implementation behind `--enable-collab`. *Intended* for trusted multi-user deployments where multiple authors edit the same article simultaneously with shared cursor awareness. Git remains canonical; the CRDT is *intended* as session-ephemeral state that serialises to a commit on explicit save.

**Mobile editor** — a mobile-first edit surface is *intended* for a later phase. The current editor is desktop-first; a mobile edit surface represents the largest unmet-need gap relative to Wikipedia, where the substantial majority of mobile sessions involve zero edits.

**Citation-graph navigation** — *intended* affordances for navigating "what this article cites" and "what cites this article", powered by the content-addressed citation registry. *Intended* to land after the Phase 4 redb wikilink graph ships.

**Semantic browse** — "articles like this" and "concepts adjacent to this" surfaced from the citation graph, not from an LLM in the read path. *Intended* as a complement to category browse. The read path is designed to be deterministic; AI is structurally optional in the outermost ring of the three-ring architecture, not embedded in the rendering path.

All items above are *intended* or *planned*. They carry no specific delivery dates. Material changes to the delivery plan would be recorded in the engineering phase plan documents and the workspace changelog.

## See also

- [[app-mediakit-knowledge]] — the engine architecture; chrome inventory at §4; compatibility surface rationale
- [[source-of-truth-inversion]] — the canonical / view / ephemeral pattern that makes Git the disclosure record
- [[substrate-native-compatibility]] — the substrate-native API surface and its rationale
- [[article-shell-leapfrog]] — the five article-shell primitives beyond Wikipedia
- [[knowledge-wiki-home-page-design]] — the home-page design intent and two-audience contract
