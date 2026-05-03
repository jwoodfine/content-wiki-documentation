---
schema: foundry-topic-v1
status: published
last_edited: 2026-04-30
category: applications
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
cites:
  - ni-51-102
  - osc-sn-51-721
references:
  - vendor/pointsav-monorepo/app-mediakit-knowledge/docs/UX-DESIGN.md
  - vendor/pointsav-monorepo/app-mediakit-knowledge/ARCHITECTURE.md
  - https://en.wikipedia.org/wiki/Wikipedia:Vector_2022
  - https://www.mdpi.com/2227-9709/12/3/97
  - https://blog.chromium.org/2023/05/an-update-on-lock-icon.html
---

The design narrative behind `app-mediakit-knowledge`'s chrome: what was kept from Wikipedia, what was added beyond Wikipedia, the deliberate visual-identity divergence, and what the 5% leapfrog headroom means for both readers and engineers.

This TOPIC goes deeper than the chrome inventory at [[app-mediakit-knowledge]] §4. That TOPIC lists what the chrome contains; this TOPIC explains why each choice was made and what the structural contract with two different audiences looks like.

## The muscle-memory contract

### Why Wikipedia patterns are the substrate's market-entry mechanism

Wikipedia has approximately two billion monthly readers. Those readers have developed navigational reflexes over two decades of exposure to a specific chrome — the location of tabs, the structure of article sections, the visual language of footnotes and hatnotes, the left-rail table of contents. These reflexes are not brand loyalty; they are motor programs. A reader of any Wikipedia article navigates without thinking about navigation.

When a new knowledge-publication substrate enters this environment, it faces a structural choice: differentiate the chrome from Wikipedia — building a visual identity distinct enough that readers know immediately they are looking at something new — at the cost of requiring readers to learn new navigational motor programs before they can work efficiently. Or adopt the same chrome, accepting that some readers will briefly experience it as a Wikipedia instance, in exchange for zero onboarding friction.

The substrate's choice is the second path, with one important qualification: the adoption must be principled, not superficial. A superficial copy fails the first time a reader looks for an affordance that the original had but the copy omitted. A principled adoption identifies the exact set of patterns that carry the muscle memory and holds them inviolable.

### The 95%/5% contract

`UX-DESIGN.md §3` names the structural allocation: 95% of the chrome is the Wikipedia muscle-memory inventory, held inviolable across all phases; 5% is the leapfrog headroom — additions that no Wikipedia reader has encountered, shipped as additive rather than replacements, so the baseline experience is undisturbed for readers who do not attend to the additions.

The Vector 2022 skin — Wikipedia's current production skin — provides the template. The Vector 2022 redesign process was deliberate about additive discipline: the community RfC showed 165 oppose, 153 support, yet the deployment proceeded because the close found rough consensus that nothing had been removed from the existing experience. A subsequent MDPI 2025 study found the redesign drove pageviews up 1.25% and internal link clicks up 1.06 million monthly, with no significant external referral disruption. The data supports additive. The substrate follows the same discipline.

### What was kept — the Phase 1 / Phase 1.1 split

The eighteen sacred patterns catalogued in `UX-DESIGN.md §1` are the inventory. The engineering delivery splits across two phases:

**Phase 1 (shipped)** covers items where the muscle memory is expressed in render output rather than chrome structure: footnote convention (bracketed superscript plus back-arrow reference list), infobox right-rail capability, link colours (blue unvisited / purple visited / red missing target), body typography (serif stack, body at minimum 17px, line-height 1.5 or greater, 45–75 character line length), centre-top search placeholder, and mobile chrome (hamburger left, sections collapsed by default, infobox stacked under lead).

**Phase 1.1 (additive over Phase 1)** covers the chrome elements that require structural additions to the template layer — the items a reader interacts with by clicking rather than by reading:

- Article / Talk tab pair, positioned at the top-left of the title row
- Read / Edit / View history tabs, positioned at the top-right of the title row, in that order
- Per-section `[edit]` pencils, right-floated on every heading
- End-of-article ordering: See also, Notes, References, Further reading, External links, Categories — the Wikipedia Manual of Style Layout sequence
- Hatnote, italic and indented, at the top of the article body above the infobox in source order
- Lead first-sentence convention: bolded subject plus copula plus one-line definition
- "From PointSav Knowledge" tagline rendered under the article title
- Collapsible left-rail table of contents following the reader on scroll
- Language switcher, as a button next to the title
- Footer convention: categories, license notice, About / Contact links

Phase 1.1 also ships two IVC chrome placeholders — visual surfaces that carry no machinery in Phase 1.1 but establish the structural location that Phase 7 is planned to fill.

## What was added beyond Wikipedia

Five additions ship beyond the Wikipedia inventory. Each is additive — no existing Wikipedia muscle-memory pattern is removed or altered.

### Citation badges

Next to every inline `[citation-id]` reference, the chrome renders a small badge in the C2PA "CR" pin glyph convention. The default colour is neutral grey — the critical design decision, taken directly from the TLS padlock lesson: Chrome removed the green padlock in May 2023 because 89% of users misread the positive state as "this site is trustworthy" rather than "the connection is encrypted." When a positive-state signal is ubiquitous, it becomes noise; only the exception deserves colour. Citation badges follow the same calibration: neutral grey for all-verified, amber for source drift, red for a missing or hash-mismatched citation, blue for forward-looking information. The positive state (verified green) appears only when the reader has explicitly toggled the "show all verified marks" density setting.

This addition does not interfere with footnote conventions. The badge appears at clause end, next to — not replacing — the existing `[n]` footnote superscript.

### FLI banner pattern

Articles whose frontmatter sets `forward_looking: true` render a cautionary banner in reading view. In authoring view, the SAA editor renders a blue squiggle on forward-looking statements that lack the frontmatter flag, prompting the author to add it.

The banner is sourced from BCSC continuous-disclosure posture: NI 51-102 and OSC Staff Notice 51-721 require that forward-looking information be labelled, carry a stated reasonable basis, and include material assumptions and cautionary language. The banner is the reading-surface expression of that requirement.

### BCSC disclosure_class field

Articles carry a `disclosure_class` field in frontmatter with three enumeration values: `narrative`, `financial`, `governance`. In the current phase this field is invisible to readers — it is expressed in JSON-LD structured data in every rendered article's `<head>` block. Starting in Phase 8, a frontmatter linter is planned to check that articles classified `disclosure_class: financial` carry an iXBRL block, and that articles with `forward_looking: true` carry the cautionary language patterns.

### IVC masthead band placeholder

A single horizontal strip at the top of every article, below the title row. In Phase 1.1 this band renders placeholder text indicating that verification is not yet available. Phase 7 is planned to fill the band with a live verification summary line: the count of claims in the article, the count verified, and the time since the last drift check.

The structural logic follows the same pattern as BBC Verify's branded byline approach — a single line in the page chrome that gives the reader an at-a-glance trust signal without distributing per-claim marks throughout the prose. The masthead band is the location where the positive verification state lives, reserving the inline badge colours for exceptions only.

### Reader density toggle

A preference with three states: Off, Exceptions only (default), All. In Phase 1.1 the preference is stored but has no effect on the chrome because the IVC machinery (Phase 7) does not yet exist.

- **Off** — no IVC marks; the pure Wikipedia reading experience
- **Exceptions only (default)** — neutral grey marks rendered at low visual weight; coloured exception marks prominent
- **All** — verified-green marks rendered alongside exception marks; for auditors, regulators, and power readers who want the full verification picture

The default is Exceptions only — the operationalisation of the TLS padlock lesson: the baseline reading experience suppresses the positive signal, showing only deviations from the expected verified state.

## The deliberate visual-identity divergence

### Muscle memory, not literal mimicry

The substrate's adoption of Wikipedia chrome is principled, not imitative. The principle: inherit the ergonomic substrate of the muscle memory; diverge visually at every point where divergence does not cost ergonomic familiarity.

The ergonomic substrate is the spatial and typographic structure that trained two decades of navigational reflexes: where the tabs are, where the table of contents is, where headings fall, how footnotes are numbered. A reader navigates by these structural landmarks. Changing their position costs the muscle memory; leaving their position unchanged preserves it.

Colour, typeface, logo, wordmark — these are brand assets, not navigational affordances. These are the points of deliberate divergence.

### What is tracked from Vector 2022

The substrate tracks Vector 2022's typography and spacing discipline because these are ergonomic, not brand:

- Body text at minimum 17px (Wikipedia moved from 14px in 2023; the MDPI study found this contributed to the pageview gain)
- Line-height 1.5 or greater for body paragraphs
- 45 to 75 character line length — the typographic consensus for comfortable sustained reading
- Serif / sans-serif choice appropriate to the content register

These numbers are not Wikipedia's inventions. They derive from decades of typographic research. Wikipedia adopted them because they are correct. The substrate adopts them for the same reason.

### What is deliberately divergent

The PointSav house colour palette applies to all chrome elements: tab bar background, active-state indicator, link underline colour, section heading colour, sidebar background, footer band.

Link colours honour the blue / purple / red visited-state convention — because this convention is navigational, not brand. The specific blue, purple, and red are in the PointSav house palette, not Wikipedia's exact hex values.

No Wikimedia logo. No Wikipedia wordmark. No Vector 2022 stylesheet is linked or loaded. The chrome is implemented in the substrate's own CSS bundle, which satisfies the same typographic and spatial criteria as Vector 2022 because those criteria are correct.

A reader who arrives at `documentation.pointsav.com` and has spent years reading Wikipedia will immediately know how to navigate. They will not mistake the site for Wikipedia. The visual identity is distinct; the navigational identity is familiar.

## Why both audiences feel at home

**The financial-community reader** arrives via a link to a specific article. They see article and talk tabs, read and edit and view history tabs, a bolded subject line opening the article body, hatnotes cross-referencing related articles, footnotes resolving at the bottom, and categories in a footer band. They have never visited this site before. They navigate without friction because they have navigated this structure thousands of times on Wikipedia.

**The engineering reader** has the same navigational experience and also notices things the financial-community reader may not attend to. In the page source, `<script type="application/ld+json">` carries a Schema.org `TechArticle` profile. The article URL slug is stable and corresponds to a Markdown filename in a Git repository. The `/feed.atom` endpoint is advertised in the page header. An `/llms.txt` file at the site root maps the corpus structure for LLM crawler ingestion. The engineering reader also sees `[[wikilink]]` syntax in the editor, CodeMirror 6, and the substrate squiggle lint markers that cite the rule they are enforcing.

Both readers are at home. Neither had to learn a new paradigm.

## Forward reference — the 5% leapfrog headroom

The 5% leapfrog headroom enumerated in `UX-DESIGN.md §3` covers capability additions that no surveyed knowledge-publication system ships as of 2026. Each item below is *intended* or *planned* for later phases; no specific timelines are stated.

**Per-claim cryptographic verification badges** (IVC, Phase 7 planned) — the inline badge system wired to the Phase 7 content-addressed federation seam.

**Real-time collaborative editing** (Phase 2 Step 7, opt-in) — the `y-codemirror.next` and Yjs CRDT implementation behind `--enable-collab`. Git remains canonical; the CRDT is *intended* as session-ephemeral state that serialises to a commit on explicit save.

**Mobile editor** — a mobile-first edit surface is *intended* for a later phase. The current editor is desktop-first.

**Citation-graph navigation** — *intended* affordances for navigating "what this article cites" and "what cites this article", powered by the content-addressed citation registry. Intended to land after the Phase 4 redb wikilink graph ships.

**Semantic browse** — "articles like this" and "concepts adjacent to this" surfaced from the citation graph, not from an LLM in the read path. *Intended* as a complement to category browse.

All items above are *intended* or *planned*. They carry no specific delivery dates. Material changes to the delivery plan would be recorded in the engineering phase plan documents and the workspace changelog.

## See also

- [[app-mediakit-knowledge]] — the engine architecture; chrome inventory at §4; compatibility surface rationale
- [[source-of-truth-inversion]] — the canonical / view / ephemeral pattern that makes Git the disclosure record
- [[substrate-native-compatibility]] — the Action API drop rationale and the substrate-native API surface set
- [[article-shell-leapfrog]] — the five article-shell primitives beyond Wikipedia
- [[knowledge-wiki-home-page-design]] — the home-page design intent and two-audience contract

## Provenance

Authored 2026-04-28 by the project-knowledge cluster (brief 04) based on `UX-DESIGN.md`, `ARCHITECTURE.md`, and direct workspace-document consultation. Refined by project-language 2026-04-30.

Forward-looking statements about planned phases carry *intended* / *planned* / *may be competitive in* language per [ni-51-102] and [osc-sn-51-721] continuous-disclosure posture. No specific delivery dates are stated; material changes would be recorded in the engineering phase plan documents and the workspace changelog.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
