---
schema: foundry-doc-v1
type: topic
slug: service-egress
short_description: "El servicio de soberanía de datos que transfiere físicamente cargas útiles almacenadas en la nube al almacenamiento en frío local, ejecutando protocolos de flujo que eliminan retención de datos del lado del proveedor y dependencia de almacenamiento en la nube."
title: "Servicio de egreso"
category: services
language: es
paired_with: service-egress.md
status: stub
last_edited: 2026-05-07
editor: pointsav-engineering
---

[[service-fs-architecture|`service-egress`]] es el motor de soberanía de datos que transfiere físicamente las cargas almacenadas en la nube al almacenamiento local en frío, ejecutando el protocolo de flujo que elimina la retención de datos del proveedor y la dependencia de la continuidad del almacenamiento en nube. Las cargas transferidas se escriben en el [[worm-ledger-design|libro mayor WORM]] por inquilino gestionado por [[service-fs-architecture]], donde se convierten en registros de solo adición. El servicio trabaja junto a [[service-email]] para garantizar que cada mensaje ingestado de un buzón en la nube tenga una copia local permanente antes de que se limpie la fuente en la nube. Consulte la [[sovereign-airlock-doctrine|exclusa soberana]] para conocer el principio arquitectónico que rige la dirección del flujo de datos.
