---
schema: foundry-doc-v1
title: "Aislamiento de Máquinas Virtuales por Tenant en PPN"
slug: ppn-tenant-vm-isolation
category: architecture
type: concept
content_type: topic
quality: stub
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: TRANSLATE-ES
last_edited: 2026-06-15
editor: pointsav-engineering
paired_with: ppn-tenant-vm-isolation.md
es_status: stub
short_description: "El pool de recursos PPN separa las cargas de trabajo por tenant mediante aislamiento de espacio de nombres, aislamiento de proceso por VM y redes en modo usuario. El aislamiento a nivel de subred de red es un hito planificado."
cites: []
---

El pool de recursos de la Red Privada de PointSav (PPN) permite que múltiples tenants ejecuten máquinas virtuales en un conjunto compartido de nodos físicos y en la nube. Este artículo describe el modelo de aislamiento: qué separación se proporciona, qué no, y el camino planificado hacia un aislamiento más sólido a nivel de red.

Para la descripción completa en inglés, consulte [[ppn-tenant-vm-isolation|PPN Tenant VM Isolation]].
