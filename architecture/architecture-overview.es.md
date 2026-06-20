---
schema: foundry-doc-v1
title: "Descripción General de Arquitectura — Plataforma PointSav"
slug: architecture-overview
category: architecture
type: concept
content_type: topic
quality: stub
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: TRANSLATE-ES
last_edited: 2026-06-20
editor: pointsav-engineering
paired_with: architecture-overview.md
short_description: "Mapa de las principales superficies arquitectónicas de la plataforma PointSav: sustrato de cómputo, distribución de software, inteligencia GIS y el pipeline editorial."
cites: []
---

La plataforma PointSav está compuesta de varias superficies arquitectónicas que operan de forma independiente pero comparten un sustrato común. Este artículo sirve como mapa hacia los artículos de arquitectura detallados.

## Sustrato de cómputo — Red Privada de PointSav (PPN)

La PPN es el pool de recursos VM multi-inquilino que forma el piso de ejecución de la plataforma. Es una pila de tres servicios (controlador de flota, agente de host, proxy de inquilino) sobre una malla WireGuard.

- [[ppn-small-business-compute|Cómputo PPN para pequeñas empresas]] — descripción del producto y pila de tres nodos
- [[ppn-vm-resource-pool|Arquitectura del Pool de Recursos VM PPN]] — algoritmo de colocación, agente de host, broker de inferencia
- [[ppn-tenant-vm-isolation|Aislamiento de VMs por Inquilino en PPN]] — aislamiento de espacio de nombres, tokens portadores, auditoría WORM

## Distribución de software

El software comercial construido sobre la plataforma se distribuye mediante un pipeline de binarios firmados con verificación de licencia en la instalación y en tiempo de ejecución.

- [[software-distribution-substrate|Sustrato de Distribución de Software]] — firma de binarios, tokens de licencia Ed25519, servidor Git privado

## Inteligencia de localización y GIS

La plataforma de orquestación GIS produce datos comerciales de clústeres de co-ubicación para los arquetipos PRO, VWH y PKS.

- Descripción General de Datos — capas de datos y pipeline de teselas GIS
- Nomenclatura de Niveles de Co-ubicación — vocabulario T1/T2/T3

## Consola OS y superficies de escritorio

La Consola OS es la interfaz de terminal para la gestión de la plataforma. Las aplicaciones de superficie Workplace están dirigidas a profesionales del sector AEC.

- [[os-console-architecture|Arquitectura de la Consola OS]] — modelo de cartuchos, superficie Ratatui, panel de estado de Doorman

*Este artículo es un resumen provisional. El contenido completo está previsto para una sesión futura.*
