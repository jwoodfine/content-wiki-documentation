---
schema: foundry-doc-v1
type: concept
slug: development-regions
short_description: "Development regions are geographic and jurisdictional zones that segment the platform's market data, regulatory context, and deployment topology. Each region defines a jurisdictional envelope, geographic boundary, and market data scope that governs co-location evaluation and compliance rule application."
title: "Development regions"
category: architecture
language: en
quality: complete
status: stable
bcsc_class: public-disclosure-safe
last_edited: 2026-05-13
editor: pointsav-engineering
paired_with: development-regions.es.md
cites: []
---

Development regions are the geographic and jurisdictional zones used by the [[pointsav-overview|PointSav]] platform to segment market data, regulatory context, and deployment topology. Each region defines a bounded envelope within which [[co-location-methodology|co-location candidates]] are evaluated, compliance postures are applied, and market intelligence accumulates. Regions are not delivery territories; they are analytical and operational boundaries that shape how the platform reasons about deployment decisions.

## Purpose

A platform serving customers across multiple jurisdictions cannot apply a single regulatory posture or a single set of market-data assumptions universally. A Canadian property-management customer operating under NI 51-102 continuous-disclosure obligations faces different data-residency requirements than a customer operating under equivalent US or European regimes. A co-location opportunity that satisfies Canadian jurisdictional constraints may not satisfy EU data-localization requirements, and vice versa.

Development regions encode this jurisdictional specificity at the architectural level. When an operator specifies a deployment requirement, they declare the target region. The platform's intelligence pipeline, the [[co-location-methodology]] scoring engine, and the compliance-posture validator all scope their outputs to that region's envelope.

## Region composition

Each development region is defined by three components:

**Jurisdictional envelope.** The set of legal and regulatory frameworks that apply within the region. For Canadian regions, this includes the applicable provincial securities regulator, the NI 51-102 continuous-disclosure framework, and any PIPEDA or CASL provisions relevant to data handling. The platform does not interpret these frameworks; it scopes data residency and disclosure tooling to the declared framework list.

**Geographic boundary.** The physical geography within which co-location facilities are considered. Geographic boundaries do not always align with jurisdictional ones — a Canadian regulatory envelope may encompass facilities in multiple provinces, each with distinct transit characteristics. The platform tracks both.

**Market data scope.** The data sources and market indices that feed the intelligence pipeline for the region. Real estate market data, economic indicators, and demographic signals are region-scoped because their informational content is jurisdictionally bounded. An index relevant to the British Columbia market is not structurally applicable to Alberta market decisions.

## Relationship to the co-location methodology

The [[co-location-methodology]] is the operational application of development-region definitions. When an operator initiates a site-selection process, they specify a development region; the co-location methodology then searches within that region's geographic boundary, applies its jurisdictional scoring rules, and returns a ranked candidate list scoped to that region.

Development regions are stable definitions that change infrequently — when a new regulatory framework comes into effect, when the platform expands to a new geography, or when a jurisdictional boundary changes. The co-location methodology is the runtime consumer of those definitions.

## Planned expansion

The development-regions model is intended to support expansion beyond Canada as the platform grows. New regions are added through a governed amendment process: the jurisdictional envelope, geographic boundary, and market-data scope must each be declared before the region is used in any deployment decision. Regions under definition are indicated as planned until all three components are formally specified.

## See also

- [[co-location-methodology]] — the scoring engine that operates within a declared development region
- [[leapfrog-2030-architecture]] — strategic architecture that shapes regional deployment decisions
- [[three-ring-architecture]] — platform substrate model within which regional deployments are provisioned
