---
schema: foundry-doc-v1
title: "Applications"
slug: applications-index
category: applications
type: topic
content_type: topic
quality: complete
short_description: "User-facing and internal applications built on the PointSav platform substrate — the wiki engine, marketing surface, GIS analytics engine, the browser developer workbench, the structured-input gate, and the design-intent articles that frame how those surfaces are composed."
index_type: thematic
index_scope: applications
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-09-04
editor: pointsav-engineering
paired_with: _index.es.md
---

Applications sit above the three-ring service layer. They consume deterministic data and optional AI output from the rings and present it through a defined interface. An application holds no canonical data — it is a view over the service layer, and can be re-provisioned without data loss by pointing a fresh instance at the immutable data underneath. The articles in this category cover both the named applications themselves and the design-intent material that explains how each surface is composed.

Each application here corresponds to an `app-*` directory in the monorepo and inherits the [[three-ring-architecture]] separation; none holds the authoritative record. Reader-facing chrome and design rationale articles are gathered alongside the application articles so that operators evaluating a surface can move from the engineering article to the design intent without leaving the category.

<!-- START-HERE-HIGHLIGHT: engine reads this block to render the single "start here" card
     (reuses the existing cluster-card--start-here component). Do not add more than one. -->

**Start here:** [[app-mediakit-knowledge]] — the wiki engine rendering the very documentation you're reading now, and the clearest example of this category's core pattern: an application as a throwaway view over canonical, git-committed data.

<!-- END-START-HERE-HIGHLIGHT -->

## Knowledge and editorial applications

The wiki engine, the marketing surface, and the design-intent articles that describe their reader-facing chrome.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: knowledge-and-editorial-applications -->
- [[app-mediakit-knowledge]] — Single-binary Rust wiki engine serving documentation.pointsav.com — a view over a markdown tree where git commits are canonical and the running binary is disposable.
- [[app-mediakit-marketing]] — app-mediakit-marketing is a Rust web server delivering marketing landing sites from typed page manifests — AI authors via MCP, a human approves before anything publishes. Serves home.woodfinegroup.com and home.pointsav.com.
- [[knowledge-wiki-home-page-design]] — How the documentation.pointsav.com home page inherits Wikipedia's structural conventions and extends them for engineering and financial-community readers.
- [[wikipedia-leapfrog-design]] — What the app-mediakit-knowledge wiki engine inherits from Wikipedia, what it adds beyond it, and what the 5% leapfrog headroom means for readers and engineers.
- [[documentation-pointsav-com-launch-2026-04-27]] — The April 2026 TLS launch of documentation.pointsav.com: serving stack, placeholder posture, BCSC disclosure rationale, and verification commands.
- [[radical-proofreader-ui]] — Terminal content cartridge for the service-proofreader pipeline — operators submit text, review findings, and record a binary accept/reject verdict that feeds the apprenticeship corpus.
<!-- END AUTO-GENERATED -->

## Location intelligence applications

The GIS analytics engine, the platform article that frames it alongside the rendering layer, and the user-experience design intent.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: location-intelligence-applications -->
- [[app-orchestration-gis]] — The Python data pipeline that produces the Woodfine co-location rankings and interactive map — cluster geometry rebuilt on a nightly schedule from source datasets, published as static map tiles.
- [[location-intelligence-platform]] — Customer-owned flat-file GIS application for retail cluster analysis and strategic site selection, pairing a nightly scoring pipeline with an interactive rendering layer.
- [[location-intelligence-ux]] — The Conclusion-First design philosophy: ranked tier conclusions rather than individual data points, so users see the most defensible commercial nodes at national zoom before drilling into individual operators.
<!-- END AUTO-GENERATED -->

## Input and developer surfaces

The structured-input gate that admits external files to a Totebox, and the browser workbench for working with archive files outside a terminal.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: input-and-developer-surfaces -->
- [[app-console-input]] — app-console-input is the F12 surface in os-console — a path, a confirm prompt, and a submission, through which raw external files enter a Totebox before being sealed into the verified ledger.
- [[app-privategit-workbench]] — Browser-based file editor in os-privategit presenting a three-column file tree, viewer, and editor for working across the cluster archive tree without a terminal.
- [[app-console-keys]] — app-console-keys is the always-installed base chassis of os-console, providing the Cartridge trait, F-key navigation strip, status bar, and auth client.
- [[app-console-email]] — app-console-email is the F3 communications cartridge for os-console, providing inbox listing, message reading, and compose-and-send via service-email.
- [[app-console-slm]] — Terminal console cartridge showing live AI inference infrastructure state — model health, the burst-GPU fleet, queue depth, and daily spend — read-only, with no controls of its own.
<!-- END AUTO-GENERATED -->

## Domain applications

Surfaces dedicated to a specific operational domain — Building Information Modelling and real-property workflows.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: domain-applications -->
- [[bim-and-real-property-surfaces]] — How PointSav treats Building Information Modelling as a distinct operational domain — a separate customer-tier design system, a real Chart of Accounts placement, and BIM-specific console surfaces still at the research stage.
<!-- END AUTO-GENERATED -->

Additional planned articles for this domain — design-system tooling for BIM, AEC interface conventions, and the gap between BIM authoring tools and property-manager workflows — are not yet written.

## Financial and construction tools

A family of owner-held ledger tools sharing one double-entry design: accounting, construction cost/schedule/quality control, and payroll. All three now have real, running code — tool-accounting's ledger engine, tool-construction's cost/schedule/reporting engine, and tool-payroll's first report — though the depth of what's built varies widely across the three.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: financial-and-construction-tools -->
- [[financial-and-construction-tools-overview]] — How tool-accounting, tool-construction, and tool-payroll relate as one product family — a shared double-entry design, one-way data feeds between them, and a shared free/paid architecture boundary.
- [[tool-accounting]] — A flat-file, owner-held double-entry accounting engine producing audit-ready financial statements from plain-text journals; its core engine and PDF/HTML renderer are built, verified against real historical multi-entity data, and driven by a real CLI toolchain of statement, ledger, narrative, and timeline report binaries — CLI-only, with no console surface yet.
- [[tool-construction]] — A flat-file, owner-held ledger for construction cost, schedule, and quality control, built on the same double-entry discipline as tool-accounting; the core engine now runs as a real CLI, posting a live pilot's estimates through all four cost-type chains — estimate-stage only, with no console surface yet.
- [[tool-payroll]] — A jurisdiction-aware payroll and statutory-remittance engine whose first real report — a division-level Payroll Register aggregating the construction pilot's budgeted labour hours under a cited single-jurisdiction wage-rules row — is built and running; gross-to-net pay, pay frequency, and remittance computation remain design-only.
<!-- END AUTO-GENERATED -->

## See also

- [Platform Services](/services/) — the service layer that applications build on
- [Operating Systems](/systems/) — the operating systems that host applications
- [How It's Built](/architecture/) — the three-ring model and the customer-ownership principles
- [Design and Brand](/design-system/) — the token and component vocabulary the application chrome inherits
