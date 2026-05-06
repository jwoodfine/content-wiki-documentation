---
schema: foundry-doc-v1
type: topic
slug: worm-ledger-architecture
title: "Sustrato del Ledger WORM: Arquitectura de Cuatro Capas"
audience: vendor-public
bcsc_class: current-fact
language: es
paired_with: worm-ledger-architecture.md
## Véase también

- [[worm-ledger-design]]
- [[worm-ledger-storage-architecture]]
- [[cryptographic-ledgers]]
- [[sel4-foundation]]

---


El servicio `service-fs` de Foundry proporciona el sustrato de almacenamiento inmutable de "escritura única y lectura múltiple" (WORM) para cada cliente. Esta arquitectura garantiza que todos los registros —desde identidades hasta comunicaciones— sean permanentes, imposibles de borrar y verificables criptográficamente.

## Arquitectura de Cuatro Capas

1.  **Capa 4 - Anclaje (Anchoring):** Se prevé el anclaje mensual de estados a la red pública Sigstore Rekor, proporcionando una prueba externa de integridad sin exponer datos privados.
2.  **Capa 3 - Protocolo de Red:** Comunicación actual mediante HTTP/JSON, con una transición planificada al protocolo MCP (Model Context Protocol).
3.  **Capa 2 - API del Ledger:** Un contrato en Rust que define las operaciones de escritura y lectura, independiente del sistema operativo subyacente.
4.  **Capa 1 - Almacenamiento de Teselas (Tiles):** Uso del estándar internacional **C2SP tlog-tiles** (RFC 9162 v2), asegurando que los datos sean legibles durante los próximos 100 años mediante herramientas estándar.

## Soberanía y Cumplimiento

Este diseño permite que Foundry funcione hoy como un demonio en Linux y, en el futuro, como un micro-kernel verificado (seL4) en dispositivos físicos (Totebox). Cumple nativamente con los requisitos de inmutabilidad de la SEC estadounidense y los estándares de preservación calificada eIDAS de la Unión Europea, devolviendo el control total del archivo histórico al propietario de los datos.


---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™ y Totebox Archive™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos titulares.*
