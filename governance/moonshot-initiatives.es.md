---
schema: foundry-doc-v1
title: "Iniciativas Moonshot"
slug: moonshot-initiatives
short_description: "Las iniciativas moonshot son programas de ingeniería activos que construyen reemplazos nativos para dependencias de terceros en cuarentena, con el objetivo de eliminar el bloqueo de proveedor y reducir la superficie de ataque externa de la plataforma a lo largo del tiempo."
category: governance
type: topic
quality: complete
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

## Áreas de iniciativa activas

Cada moonshot apunta a una clase de dependencia distinta. Las siguientes clases tienen iniciativas abiertas en la plataforma de ingeniería:

| Iniciativa | Dependencia objetivo | Justificación |
|---|---|---|
| `moonshot-database` | Motor de base de datos externo | Soberanía de datos; reemplazar el motor foráneo por un almacén embebido o de archivos planos formalmente verificado |
| `moonshot-gpu` | Servicios de inferencia GPU en la nube | Soberanía de inferencia; la capacidad GPU local elimina la dependencia de APIs de inferencia en la nube |
| `moonshot-hypervisor` | Capa de hipervisor externa | Soberanía de sustrato; un hipervisor verificado cierra la brecha entre el micronúcleo seL4 y el hardware de consumo |
| `moonshot-index` | Backends externos de búsqueda e indexación | Soberanía de búsqueda; un índice nativo de la plataforma elimina la dependencia de infraestructura de búsqueda de terceros |
| `moonshot-kernel` | Kernel Linux de consumo | Soberanía de kernel; el [[sel4-microkernel-substrate|micronúcleo formalmente verificado seL4]] reemplaza la dependencia de systemd/Linux en cuarentena registrada en [[architecture-decisions|ADR-08]] |
| `moonshot-network` | Plano de control de red externo | Soberanía de red; una malla nativa de WireGuard elimina la dependencia de servicios de red gestionados |
| `moonshot-protocol` | Protocolos de comunicación propietarios | Soberanía de protocolo; reemplazar protocolos propietarios por equivalentes abiertos y formalmente especificados |
| `moonshot-sel4-vmm` | Monitor de máquina virtual de consumo | Capa de verificación; un VMM nativo seL4 cierra el límite verificado bajo todos los sistemas operativos invitados |
| `moonshot-toolkit` | Herramientas externas de compilación e integración continua | Soberanía de compilación; un orquestador de compilación nativo en Rust reemplaza la dependencia de infraestructura CI externa |

El estado de finalización de cada iniciativa se registra en el libro contable de la [[sovereign-replacement-initiative|Iniciativa de Reemplazo Soberano]].

## Gobernanza

La Iniciativa de Reemplazo Soberano es el programa de gobernanza que coordina estos esfuerzos. Proporciona el marco para priorizar qué dependencias de terceros se apuntan, en qué secuencia, y qué criterios definen el éxito de cada iniciativa.

## Véase también

- [[sovereign-replacement-initiative]] — programa de gobernanza que coordina estos esfuerzos de ingeniería
- [[sel4-microkernel-substrate]] — el micronúcleo formalmente verificado al que apuntan moonshot-kernel y moonshot-sel4-vmm
- [[architecture-decisions]] — ADR-08 registra la cuarentena de systemd que moonshot-kernel está diseñado para cerrar
- [[ontological-governance]] — gobernanza de taxonomía que proporciona la nomenclatura para los componentes en cuarentena
- [[verification-surveyor]] — el agente de auditoría que rastrea el estado de finalización de cada iniciativa
