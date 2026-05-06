---
schema: foundry-doc-v1
title: "service-fs"
slug: service-fs-data-lake
category: services
type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
cites: []
---

`service-fs` is the foundational storage layer for the PointSav GIS platform. It implements a data lake model where raw geospatial points ingested from open geospatial sources are stored in a durable, modular file system for downstream analytical processing.

## Data Ingestion and Storage

The service maintains a unified filesystem structure with separate landing zones for retail and civic infrastructure data.

- **Retail landing:** raw commercial operator records ingested from open geospatial registries (OpenStreetMap, Overture Maps Foundation).
- **Civic landing:** raw civic and institutional facility records from the same open sources.

### Architectural Role

As the stateful layer of the platform, `service-fs` is responsible for data persistence. It is designed to be independent of the analytical software — if the GIS orchestration layer is re-provisioned, the core data assets remain intact within this layer. The clean separation between data persistence and analytical logic is a core design invariant.

## Unikernel Implementation

In production, `service-fs` is deployed as a low-overhead unikernel. It provides a restricted API for the `service-business` and `service-places` intelligence layers to read raw data and write back processed results, enforcing clean separation between storage and analysis concerns.

## See Also

- [[service-business-clustering]]
- [[service-places-filtering]]
- [[app-orchestration-gis]]

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
