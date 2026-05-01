---
schema: foundry-doc-v1
title: "Wikipedia Structure — Reference for Contributors"
slug: wikipedia-structure
category: reference
type: reference
quality: core
short_description: "Wikipedia's article anatomy and Main Page panel structure, with adaptation guidance for documentation.pointsav.com contributors. Use as the style guide reference when writing or editing articles."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
paired_with: wikipedia-structure.es.md
---

Wikipedia's article structure is the most widely internalized documentation convention in the world. Readers who have used Wikipedia carry an unconscious model of where information lives on a page, what visual signals indicate quality, and how to navigate from article to article. `documentation.pointsav.com` adopts the same structural conventions so that readers arrive already knowing how to use it. This article describes Wikipedia's structural patterns and how each translates to PointSav documentation. Contributors should use it as the style guide reference for any article they write or edit. The goal is not imitation for its own sake: it is meeting readers where their existing expectations live.

## Wikipedia Main Page anatomy

Wikipedia's Main Page serves multiple reader intents simultaneously. Nine structural panels, each addressing a distinct need:

| Panel | Reader need served | PointSav equivalent |
|---|---|---|
| Welcome banner with article count | "What is this? Should I trust it?" | Article count + "PointSav platform documentation" tagline |
| Featured Article (image + 100–150 word excerpt) | "Show me what excellent coverage looks like" | Featured TOPIC (currently: `compounding-substrate`) |
| Did You Know... (9 bulleted quick facts) | "Surprise me; let me explore" | "Quick Facts" or "Tip of the week" panel — static markdown in iteration 1; panel engine support is an iteration-2 item |
| In the News (current events) | "Is this wiki current?" | "Latest Updates" — links to recent release notes or changelog entries; static markdown in iteration 1, panel automation is iteration 2 |
| On This Day (historical facts) | "What is the history here?" | "Milestones" — major product releases; iteration 3 |
| Featured Picture (large image + caption) | "Visual proof this is maintained" | Architecture diagram or system screenshot; iteration 2 |
| Other areas of Wikipedia (community links) | "Where do I ask questions?" | "Support" / "Discussions" / "Getting Started" links |
| Sister projects (Wiktionary, Commons, etc.) | "What else exists?" | Ecosystem links: GitHub, API docs, SDK repos |
| Language editions | "Is this available in my language?" | Bilingual toggle: English / Spanish (already implemented) |

**The principle underlying all nine panels**: every section on the Wikipedia Main Page carries a freshness signal. "Today's featured article," "In the news," "On this day" — the impression for readers is that the wiki is alive and maintained. A documentation home page without freshness signals reads as abandoned.

## Article anatomy

Every Wikipedia article follows the same structure in the same order. Readers learn it once, then apply it across every subsequent article without conscious thought.

### Pre-content elements (above the lead)

1. **Short description** (30–50 words below the title) — answers "Is this the right article?" in half a second. Example: "Cone geyser in Yellowstone National Park, Wyoming."

2. **Quality badge** (upper right) — Featured Article star (FA) or Good Article circle (GA). Readers learn to read these as trust signals: FA means professional publication quality. In PointSav documentation, the `quality:` frontmatter field already records Complete / Core / Stub for each article; visual badge rendering is project-knowledge engine scope.

3. **Hatnote** (italicized, indented, immediately below short description) — disambiguates. Standard forms:
   - "For other uses, see X (disambiguation)"
   - "Not to be confused with Y"
   - "X redirects here. For other uses, see Y"

   Use hatnotes wherever a reader might have arrived at the wrong article.

4. **Maintenance tags** — "[citation needed]", "[update needed]" — signal known article limitations transparently. For PointSav: "[needs examples]", "[beta — behaviour may change]".

5. **Infobox** (structured data panel, right side) — key facts in label-value pairs. Readers scan the infobox first, then read the lead. See "Infobox templates" below.

### Main content

6. **Lead section** (200–400 words) — the article in miniature. The lead must answer, in order: What is this? Why does it matter? When and where does it apply? What are the key facts a reader needs? Forty percent of Wikipedia readers read only the lead; write it as if it is the only section they will read. First sentence: bold the article title.

7. **Table of Contents** — auto-generated when four or more sections exist. Readers use the TOC as primary navigation; they jump to "Examples" or "Troubleshooting" rather than scrolling.

8. **Body sections** — named with simple parallel nouns (Overview / Configuration / Examples / Troubleshooting / Related Features). Avoid sections named with questions or vague labels ("Other information"). Maximum three levels of heading depth.

### Post-content elements

9. **See Also** (5–10 bulleted links to related articles) — enables serendipitous discovery and reveals integration relationships.

10. **References** ([1], [2], [3] numbered citations, full bibliography at bottom) — the primary quality signal readable to all audiences. Twenty or more citations reads as authoritative; five or fewer reads as unverified.

11. **External Links** — authoritative external sources only; not promotional links.

12. **Categories** (bottom footer) — enables browsing by topic rather than search. Every article carries two or three category tags; clicking a category shows all articles in that group.

## Infobox templates for PointSav documentation

Wikipedia uses different infobox schemas for different content types (person, location, organization, scientific concept). PointSav documentation uses three schemas. The code-block representation below is the iteration-1 form; actual template engine integration is a future scope item for project-knowledge.

**API endpoint infobox:**
```
HTTP method:        GET / POST / PUT / DELETE
Endpoint:           /api/v2/resource
Required params:    resource_id, timestamp
Response format:    JSON
Rate limit:         1,000 req/min
Authentication:     OAuth 2.0
Changelog:          [link to release notes]
```

**Feature infobox:**
```
Available in:       All Plans / Premium only
Release date:       YYYY-MM-DD
Status:             Stable / Beta / Deprecated
Replaces:           [link, if applicable]
Related features:   [links]
```

**Integration infobox:**
```
Partner:            [Name]
Sync frequency:     Real-time / Daily / Manual
Data synced:        [list]
Setup time:         N minutes
Support:            [contact]
```

## Quality grade system

Wikipedia uses seven quality tiers. PointSav documentation uses three, visible as coloured badges in the upper right of every article. The `quality:` frontmatter field is already in use across articles; visual badge rendering is project-knowledge engine scope.

| Badge | Criteria | Wikipedia equivalent |
|---|---|---|
| **Complete** (green) | 400+ word lead; full infobox; 5+ sections with examples; 10+ references; updated within 6 months | Featured Article (FA) |
| **Core** (blue) | 200+ word lead; key infobox fields; 3+ sections; 5+ references | Good Article (GA) |
| **Stub** (yellow) | Under 200 words; sparse or absent infobox; maintenance tags visible | Start / Stub class |

Readers do not need to read a badge to register it. The visual presence of a Complete badge (green, upper right) creates an impression of trustworthiness within the first five seconds on the page.

## Navigation muscle memory

Wikipedia trains readers to find things in consistent locations:

- **Left sidebar**: search, home link, browse by topic — navigation tools are always left; content is always right
- **Bold text on first mention**: first use of a key term is bolded and linked — readers learn that bold means "this is central; click to learn more"
- **See Also at bottom before References**: always in this order — readers who reach the bottom of an article find related reading before citations
- **Categories in footer**: below all other sections — the breadcrumb back to the category hierarchy

Consistent placement is more valuable than inventive placement. Once readers learn the pattern on one article, they navigate every subsequent article without effort.

## Three core insights

**Consistency creates trust.** Wikipedia's articles follow identical structure. Readers learn it once, then navigate every article using internalized muscle memory. A documentation wiki where each article is structured differently forces readers to re-learn on every page visit.

**Lead sections carry disproportionate weight.** Most documentation effort goes into the body. On Wikipedia, Featured Articles invest proportionally more effort in the lead than in any body section. The lead is the article in miniature: readers who only read the lead should understand the subject completely.

**Quality signals matter more than content completeness.** Readers assess article credibility in five seconds by scanning: badge presence, infobox fullness, image count, reference count, last-updated timestamp. They do not read the article to decide whether to trust it; they scan for signals that others have maintained it. A stub article with a visible Stub badge and maintenance tags reads as more trustworthy than an article with no badge at all — at least the stub is honest about its state.

## See Also

- [[style-guide-topic]] — how to apply Wikipedia structure when writing a TOPIC article
- [[style-guide-readme]] — how Wikipedia lead-section discipline applies to READMEs
- [[compounding-substrate]] — the featured article demonstrating Complete-quality Wikipedia structure
- [[apprenticeship-substrate]] — example of a Complete-quality TOPIC using Wikipedia anatomy

## References

1. Wikipedia Main Page — fetched live 2026-04-30. Full panel inventory and freshness-signal design.
2. Wikipedia Manual of Style/Lead section — formal lead-writing requirements; 200–400 words; must stand alone as a summary.
3. Wikipedia:Article structure — standard section order; heading hierarchy rules; accessibility requirements.
4. Wikipedia:Hatnote — disambiguation conventions; standard form templates.
5. Wikipedia:Content assessment — quality grade definitions (FA/GA/A/B/C/Start/Stub) and reader-perception mapping.
6. Wikipedia Special:Statistics — scale data (7.1M articles, 273K active editors).
7. Old Faithful article (Featured Article class) — concrete example of all structural elements applied to a single article.

## Provenance

Source material: Wikipedia Main Page; Wikipedia Manual of Style/Lead section; Wikipedia:Article structure; Wikipedia:Hatnote; Wikipedia:Content assessment; Wikipedia Special:Statistics; Old Faithful Featured Article. All fetched live 2026-04-30. Research conducted by web-fetch sub-agent. 7 sources consulted; 5 suggested for future review. Three open questions resolved inline: "Did You Know" and "Latest Updates" panels confirmed as static markdown in iteration 1 with panel engine support deferred to iteration 2; code-block infoboxes confirmed as the iteration-1 form with template engine integration as future project-knowledge scope; `quality:` frontmatter field confirmed as already in active use, with visual badge rendering identified as project-knowledge engine scope.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
