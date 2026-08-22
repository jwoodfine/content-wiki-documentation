---
schema: foundry-doc-v1
title: "Iniciativas Moonshot"
slug: moonshot-initiatives
short_description: "Las iniciativas moonshot son programas de ingeniería activos que construyen reemplazos nativos para dependencias de terceros en cuarentena, con el objetivo de eliminar el bloqueo de proveedor y reducir la superficie de ataque externa de la plataforma a lo largo del tiempo."
category: governance
type: topic
content_type: topic
quality: complete
index_group: engineering-sovereignty
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-19
editor: pointsav-engineering
paired_with: moonshot-initiatives.md
cites: []
---


Las iniciativas moonshot son programas de ingeniería activos que construyen reemplazos nativos para dependencias de terceros en cuarentena, con el objetivo de eliminar el bloqueo de proveedores y reducir la superficie de ataque externa de la plataforma a lo largo del tiempo.

## Qué son

La plataforma rastrea activamente la deuda de ingeniería de terceros en un libro contable estructurado. Los componentes arquitectónicos foráneos están contenidos en directorios aislados, denominados silos de componentes en cuarentena, hasta que una **iniciativa moonshot** entregue un reemplazo nativo.

Cada iniciativa moonshot es un esfuerzo de ingeniería distinto que apunta a una clase de dependencia. La finalización se define como paridad estructural con el componente que reemplaza, punto en el cual la implementación nativa suplanta físicamente el directorio en cuarentena.

## Por qué importa la cuarentena

La cuarentena no es una medida punitiva — es una postura arquitectónica. Un componente de terceros en cuarentena puede usarse operativamente mientras la iniciativa moonshot procede, pero su presencia está documentada como deuda de ingeniería activa. El libro contable hace la deuda visible; la visibilidad evita que se acumule silenciosamente.

## Áreas de iniciativa y estado real

Existen nueve directorios moonshot. Tres llevan ingeniería activa y sustancial hoy; los seis restantes son directorios nombrados con un esqueleto Cargo de 4 archivos y sin implementación todavía:

| Iniciativa | Dependencia objetivo | Estado |
|---|---|---|
| `moonshot-index` | Backends externos de búsqueda e indexación | Activa — un índice de trigrama funcional más una capa de búsqueda clasificada planificada, `std` puro, sin dependencia externa |
| `moonshot-sel4-vmm` | Monitor de máquina virtual de consumo | Activa — un tiempo de ejecución real de dominio de protección seL4 con varios binarios funcionales, incluida una llamada HTTP confirmada sobre DMA VirtIO-net |
| `moonshot-toolkit` | Herramientas externas de compilación e integración continua | Activa — un orquestador de compilación en Rust funcional que produce una imagen de sistema arrancable |
| `moonshot-database` | Motor de base de datos externo | Esqueleto — existen el directorio y el manifiesto Cargo, sin implementación |
| `moonshot-gpu` | Servicios de inferencia GPU en la nube | Esqueleto — existen el directorio y el manifiesto Cargo, sin implementación |
| `moonshot-hypervisor` | Capa de hipervisor externa | Esqueleto — existen el directorio y el manifiesto Cargo, sin implementación |
| `moonshot-kernel` | Kernel Linux de consumo | Esqueleto — existen el directorio y el manifiesto Cargo, sin implementación. El [[sel4-microkernel-substrate|micronúcleo formalmente verificado seL4]] es el reemplazo previsto para la dependencia de systemd/Linux en cuarentena registrada en [[architecture-decisions|ADR-08]], pero ese trabajo de reemplazo vive actualmente en `moonshot-sel4-vmm`, no aquí |
| `moonshot-network` | Plano de control de red externo | Esqueleto — existen el directorio y el manifiesto Cargo, sin implementación |
| `moonshot-protocol` | Protocolos de comunicación propietarios | Esqueleto — existen el directorio y el manifiesto Cargo, sin implementación |

El estado de finalización de cada iniciativa se registra en el libro contable de la [[sovereign-replacement-initiative|Iniciativa de Reemplazo Soberano]].

## Gobernanza

La Iniciativa de Reemplazo Soberano es el programa de gobernanza que coordina estos esfuerzos. Proporciona el marco para priorizar qué dependencias de terceros se apuntan, en qué secuencia, y qué criterios definen el éxito de cada iniciativa.

## Véase también

- [[sovereign-replacement-initiative]] — programa de gobernanza que coordina estos esfuerzos de ingeniería
- [[sel4-microkernel-substrate]] — el micronúcleo formalmente verificado al que apuntan moonshot-kernel y moonshot-sel4-vmm
- [[architecture-decisions]] — ADR-08 registra la cuarentena de systemd que moonshot-kernel está diseñado para cerrar
- [[ontological-governance]] — gobernanza de taxonomía que proporciona la nomenclatura para los componentes en cuarentena
- [[verification-surveyor]] — el agente de auditoría que rastrea el estado de finalización de cada iniciativa
