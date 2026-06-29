---
schema: foundry-doc-v1
title: "PPN: Arquitectura seL4 de Tres Caminos"
slug: ppn-three-path-architecture
category: architecture
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-06-29
editor: pointsav-engineering
paired_with: ppn-three-path-architecture.md
short_description: "Tres opciones de arquitectura seL4 secuenciales para nodos de infraestructura PPN: la Opción B se implementa primero (hipervisor seL4 + invitado Linux), la Opción C añade WireGuard como dominio de protección seL4, y la Opción A apunta a un entorno seL4 puro sin máquinas virtuales."
cites: []
---

La pila de nodos de la Red Privada PointSav está diseñada en torno al micronúcleo seL4. Tres opciones de arquitectura definen la hoja de ruta. Son secuenciales: la Opción B es el camino de desarrollo actual; la Opción C requiere que la Opción B se publique y permanezca estable; la Opción A requiere que la Opción C esté completa. Las tres se documentan juntas para que las decisiones tomadas en la Opción B no eliminen las opciones posteriores.

---

## Opción B — Hipervisor seL4 con invitado Linux

**Camino actual.**

seL4 funciona como hipervisor de Tipo 1 a EL2 (AArch64) o con VT-x (x86-64). El VMM CAmkES funciona como un dominio de protección seL4 y aloja una máquina virtual Linux (Debian 12). Todos los servicios PPN — WireGuard, gestión de flota, enrutamiento de inferencias — se ejecutan dentro del invitado Linux.

```
Hardware
└── Micronúcleo seL4 (EL2 / VT-x)
    └── VMM CAmkES [PD seL4]
        └── Invitado Linux (Debian 12)
            ├── Interfaz de malla WireGuard
            ├── service-vm-fleet
            ├── service-vm-host
            └── os-network-admin
```

**Qué proporciona seL4:** El núcleo está formalmente verificado. Ninguna máquina virtual invitada puede acceder a la capa del hipervisor, a la memoria de otro invitado ni a ningún objeto del núcleo seL4 sin una concesión explícita de capacidad seL4. En AArch64 EL2, la prueba de integridad (abril de 2025) extiende esto a una garantía verificada mecánicamente.

**Qué no proporciona seL4 en la Opción B:** El VMM CAmkES y el invitado Linux no están formalmente verificados. Un invitado Linux comprometido permanece confinado por la topología de capacidades de seL4, pero los servicios dentro del invitado son de confianza entre sí según el modelo de procesos normal de Linux.

**Cobertura de seguridad formal:**

| Arquitectura | Afirmación formal | Notas |
|---|---|---|
| AArch64 EL2 | Prueba de integridad seL4 (abril de 2025) | Afirmación de seguridad formal válida en el límite del hipervisor |
| x86-64 | Solo corrección funcional | Sin prueba de integridad formal; objetivo de desarrollo únicamente |

---

## Opción C — Dominios de protección seL4 poseen WireGuard

**Estado: previsto/con intención.** Requisito: la Opción B se publica y permanece estable durante seis meses o más.

Arquitectura híbrida. Los dominios de protección seL4 son propietarios de WireGuard y del plano de control de red PPN. Una máquina virtual Linux invitada aloja cargas de trabajo no críticas. El límite de seguridad es el dominio de protección WireGuard — la VM Linux no puede modificar las tablas de pares sin pasar por IPC seL4.

```
Micronúcleo seL4 (EL2 / VT-x)
├── PD: wireguard-control  [tabla de pares WireGuard, gestión CPace]
├── PD: ppn-gate           [aplicación de canales IPC seL4]
└── VMM CAmkES
    └── Invitado Linux (Doorman, flota, telemetría, multimedia)
```

Al mover la interfaz de malla WireGuard a un dominio de protección seL4, una VM Linux totalmente comprometida no puede acceder a las tablas de pares ni a la capacidad de añadir o eliminar nodos. Las solicitudes de adición de pares fluyen a través de IPC seL4 hacia el dominio wireguard-control, que valida cada solicitud de forma independiente.

Qué cambia respecto a la Opción B: la gestión WireGuard de `os-network-admin` se mueve de Linux a un PD seL4; el invitado Linux no tiene interfaz `wg0`; las solicitudes de adición de pares siguen el flujo VM Linux → IPC seL4 → PD wireguard-control → estado del núcleo.

---

## Opción A — Dominios de protección seL4 puros, sin máquinas virtuales

**Estado: previsto/con intención.** Requisito: la Opción C se publica y permanece estable.

Sin máquinas virtuales. Sin VMM. Cada servicio PPN es un dominio de protección seL4. WireGuard está portado a un PD seL4 sin capa de socket Linux. La gestión de flota y el enrutamiento de servicios son dominios de protección. Esto produce la base informática de confianza más pequeña posible.

```
Micronúcleo seL4 (EL2 — solo AArch64 para afirmaciones formales)
├── PD: wireguard     [criptografía WireGuard + tabla de pares, solo IPC seL4]
├── PD: fleet-tracker [service-vm-fleet, sin tokio, sin std net]
├── PD: doorman       [enrutamiento de inferencias, basado en IPC seL4]
└── PD: ppn-control   [os-network-admin, ceremonia CPace]
```

Eliminar el invitado Linux extrae el componente no verificado más grande de la pila. En AArch64 EL2 con la prueba de confidencialidad en curso a mediados de 2026, la Opción A apunta a las tres propiedades CIA en la capa del núcleo — la postura de seguridad más profunda de las tres opciones.

---

## Objetivos de arquitectura de Microkit 2.2.0

Microkit 2.2.0 — el marco recomendado por la Fundación seL4 para nuevos proyectos seL4 — admite estos objetivos de hardware:

| Objetivo | Arquitectura | Virtualización por hardware | Verificación |
|---|---|---|---|
| `aarch64` | AArch64 | No (solo EL2) | Prueba de integridad (abril de 2025) |
| `x86_64_generic` | x86-64 | No (software TCG) | Corrección funcional |
| `x86_64_generic_vtx` | x86-64 | Sí (VT-x/AMD-V) | Corrección funcional |

La compatibilidad con x86-64 se añadió en Microkit 2.1.0. Esta arquitectura es un objetivo de desarrollo y tiempo de ejecución válido, pero no cuenta con las pruebas de integridad o confidencialidad disponibles en AArch64.

---

## Resumen

| Opción | seL4 como | Linux | Base de cómputo de confianza | Verificación | Estado |
|---|---|---|---|---|---|
| B (actual) | Hipervisor | VM invitada | seL4 + VMM + Linux | Integridad AArch64 | Activo |
| C (previsto) | Hipervisor + PD WireGuard | VM invitada (limitada) | seL4 + VMM + PD WireGuard + Linux | Integridad AArch64 | Previsto/con intención |
| A (previsto) | SO (todos los componentes) | Ninguno | Solo seL4 | AArch64 todas CIA (en curso) | Previsto/con intención |

## Véase también

- [[sel4-capability-topology]] — base formal: cómo la topología de capacidades seL4 determina los perímetros de seguridad
- [[ppn-architecture-overview]] — cómo la capa del hipervisor seL4 encaja en la pila PPN de cuatro capas
- [[sovereign-mesh]] — la superposición WireGuard que se ejecuta dentro del invitado Linux (Opción B) o como un PD seL4 (Opciones C/A)
- [[os-products-distribution-model]] — formatos de artefactos en los que se distribuye os-infrastructure para su despliegue
