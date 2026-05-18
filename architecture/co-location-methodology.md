---
schema: foundry-doc-v1
type: concept
slug: co-location-methodology
short_description: "A structured approach for ranking hardware co-location candidates across jurisdictional, network, infrastructure, and cost dimensions, constrained first by regulatory requirements before other optimization occurs."
title: "Co-location methodology"
category: architecture
language: en
quality: complete
status: stable
bcsc_class: public-disclosure-safe
last_edited: 2026-05-13
editor: pointsav-engineering
paired_with: co-location-methodology.es.md
cites: []
---

The co-location methodology is the structured approach PointSav uses to score and rank physical co-location opportunities for customer deployments. It combines market data, regulatory context, and infrastructure characteristics drawn from the platform's intelligence pipeline and [[compounding-substrate]] to produce a ranked list of candidate sites for a given deployment requirement.

## What co-location means in this context

Co-location, in the PointSav deployment model, refers to placing customer-owned hardware in a third-party data centre facility rather than on a customer's own premises. The customer retains ownership of the hardware, the software stack, and the data; the facility provides power, cooling, physical security, and network transit.

The methodology addresses the site-selection step: given a deployment requirement — a ToteboxOS node, a MediaKit-class workload, or a GPU-capable inference tier — which facilities across which [[development-regions]] best satisfy the combination of latency, jurisdiction, compliance posture, and cost constraints?

## Scoring dimensions

**Jurisdictional fit.** Each co-location candidate is evaluated against the regulatory context of the customer's operating region. For Canadian customers under NI 51-102 or OSC SN 51-721 disclosure obligations, data residency within Canada is a baseline requirement. The methodology encodes jurisdiction-first scoring: a facility outside the required jurisdiction is excluded before other dimensions are evaluated.

**Network transit characteristics.** Latency to the customer's primary users and to the PointSav workspace endpoint is measured at candidate selection time. Facilities are scored on round-trip time, transit provider diversity, and the availability of a WireGuard-compatible BGP peering path to the customer's existing nodes.

**Infrastructure compatibility.** The physical power and cooling envelope of the facility is matched against the node class being placed. ToteboxOS nodes require modest, always-on power profiles; GPU-capable inference tiers require higher burst power and active cooling. Facilities that cannot accommodate the target node class are excluded.

**Cost structure.** Monthly colocation fees, cross-connect charges, and bandwidth commitments are normalized to a total cost of ownership over a 36-month horizon. The methodology does not optimize cost in isolation; it minimizes cost within the constraint set defined by the preceding dimensions.

## Integration with development regions

Co-location scoring operates within the [[development-regions]] taxonomy. A development region defines the geographic and jurisdictional envelope within which co-location candidates are considered. The methodology does not search globally; it searches within the region declared by the deployment requirement, then scores candidates within that region against the four dimensions above.

This scoped approach reflects the platform's deployment philosophy: sovereignty and regulatory compliance are architectural constraints, not post-selection considerations. Candidate sets are bounded before scoring begins.

## Intelligence pipeline role

The scoring computation draws on structured market data ingested by the platform's intelligence pipeline. Facility profiles — power ratings, transit providers, compliance certifications, pricing structures — are maintained as structured records in the [[three-ring-architecture]] Ring 1 data layer. The pipeline refreshes these records on a defined schedule; scores reflect the most recently ingested facility state.

Operator review is the final step. The intelligence pipeline produces a ranked candidate list; the operator selects from that list. The methodology does not automate site selection; it compresses the search space and makes the trade-offs explicit before the operator decides.

## See also

- [[development-regions]] — geographic and jurisdictional zone taxonomy
- [[three-ring-architecture]] — platform data and compute substrate model
- [[compounding-substrate]] — substrate mechanism that accumulates market intelligence over time
- [[leapfrog-2030-architecture]] — strategic architecture within which co-location decisions are made
