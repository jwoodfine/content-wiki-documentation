---
schema: foundry-doc-v1
title: "Doctrina del sustrato del sistema"
slug: system-substrate-doctrine
category: substrate
type: topic
content_type: topic
quality: complete
index_group: cryptographic-and-microkernel-primitives
short_description: La arquitectura de nivel de kernel bajo cada servicio de PointSav — un registro de capacidades con raíz en el cliente, una estrategia de SO soberana de dos bases, y mecanismos para capacidades de tiempo limitado, verificación reproducible y recuperación universal.
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-07-31
editor: pointsav-engineering
cites:
 - sec-17a-4-f
 - eidas-qualified-preservation
 - rfc-3161
 - opentimestamps
paired_with: system-substrate-doctrine.md
---

La **Doctrina del Sustrato del Sistema** define la capa debajo de cada sistema operativo, servicio y aplicación de PointSav: el kernel, el modelo de capacidades, el [[worm-ledger-architecture|registro de auditoría]] y la ceremonia de transferencia de propiedad que juntos constituyen un despliegue criptográficamente soberano.

Dos afirmaciones principales impulsan la arquitectura. El **[[capability-ledger-substrate|Sustrato del Registro de Capacidades]]**: el estado de capacidades del sistema en ejecución ES el registro WORM de solo anexado; el kernel consulta el registro antes de honrar cualquier invocación; el despliegue se deriva del registro. El **Sustrato Soberano de Dos Bases**: los mismos binarios se ejecutan ya sea en un kernel formalmente verificado ([[sel4-microkernel-substrate|seL4]] hoy, con un futuro moonshot-kernel en Rust sin estándar) o en un kernel de compatibilidad de grado soberano (NetBSD con Veriexec y construcciones reproducibles sin conexión).

## La inversión del modelo de atestación

Los sistemas existentes anclan la atestación en las claves del proveedor: los proveedores de nube en sus propias raíces de confianza, los stacks nacionales de identidad digital en claves del estado, los enclaves seguros en claves del fabricante del chip. En cada caso, la prueba atestada es prueba de los controles del proveedor, no de los controles del cliente.

La arquitectura de la plataforma invierte esto: cada cadena de atestación termina en la clave de firma apex propia del [[customer-owned-graph-ip|cliente]]. La clave apex es sostenida por el cliente: en su TPM, en un HSM que él posee y opera, o como una semilla impresa en papel para recuperación con espacio de aire. Ningún servicio de la plataforma, ningún proveedor, ningún fabricante de chips se interpone entre el cliente y la raíz del registro.

## El Registro de Capacidades

Cada invocación de capacidad mediada por el kernel emite una entrada firmada a un registro [[merkle-proofs-as-substrate-primitive|Merkle]] con raíz en el cliente. El despliegue ES el registro: arrancar es reproducir el registro desde el génesis; apagar es añadir una entrada de apagado; actualizar es añadir una entrada de actualización de versión; rotar claves es añadir una entrada de rotación. El estado del despliegue en cualquier momento es la aplicación determinista de todas las entradas del registro hasta ese momento.

## Cosignatura Apex y transferencia de propiedad

La transferencia de propiedad es una única entrada firmada en el registro. El apex
anterior añade una entrada de revocación que libera el despliegue hacia un nuevo apex.
El nuevo apex cofirma la siguiente raíz de checkpoint mediante la primitiva de
multi-firma C2SP `signed-note` — el mismo mecanismo de
[[merkle-proofs-as-substrate-primitive|prueba Merkle]] usado en todo el registro. A
partir de ese checkpoint, solo se requiere la firma del nuevo apex. El despliegue
continúa ejecutándose sin migración de estado, sin tiempo de inactividad y sin
intervención del proveedor.

El nuevo apex hereda todo el historial del registro, todo el estado de capacidades,
todos los registros de auditoría y todas las pruebas de verificación formal. El apex
anterior conserva únicamente el registro histórico inmutable de que fue el apex desde
el génesis hasta la entrada de rotación.

Este mecanismo está pensado para cubrir integraciones de fusiones y adquisiciones,
desinversiones, la salida (breakout) de un cliente y la sucesión de operador — todas
gestionadas mediante la misma ceremonia de rotación de apex.

## Tres mecanismos

**Mecanismo A — Capacidades de Tiempo Limitado.** Una capacidad lleva una marca de tiempo de vencimiento y una clave pública de testigo. El kernel se niega a honrar la capacidad pasado el vencimiento a menos que se presente un registro de testigo firmado cuyo hash aparezca en la raíz Merkle del registro de capacidades actual. Extender una capacidad requiere una nueva firma de testigo Y una aparición en el registro público.

**Mecanismo B — Verificación Reproducible en Hardware del Cliente.** Cada versión incluye archivos de teoremas Isabelle/HOL para la parte de seL4 formalmente verificada, trazas de propiedad de Rust para la capa del sistema, y un grafo de construcción reproducible anclado a un registro de transparencia público. La verificación de inspección rápida está prevista para completarse en menos de 60 minutos en un portátil de uso comercial.

**Mecanismo C — Recuperación Universal de Capacidades.** La identidad operativa completa del cliente se reconstruye desde una semilla impresa en papel más el estado del registro de transparencia público. La semilla cabe en una tarjeta índice de tamaño estándar. No se requiere portal del proveedor, vuelta al cloud ni HSM para la recuperación.

## Las dos bases

El sustrato opera sobre dos bases: una base nativa de máxima seguridad (seL4 en AArch64, con moonshot-kernel previsto en Rust sin estándar) y una base de compatibilidad de grado soberano (NetBSD con Veriexec, `build.sh` reproducible sin conexión, y rump kernels). Los mismos binarios `os-*` se ejecutan en cualquiera de las dos bases mediante un delgado shim.

NetBSD se elige específicamente por su transferibilidad BSD de 2 cláusulas, Veriexec (análogo al arranque de solo imágenes verificadas de seL4), reproducibilidad sin conexión de `build.sh`, rump kernels para el puente IT/OT, 57 puertos de hardware oficiales, y una fundación independiente sin entrelazamiento con hiperscalares.

AArch64 es el objetivo de hardware principal. RISC-V64 cuenta con una verificación
formal más completa, pero el hardware comercial sigue siendo significativamente más
débil en 2026. x86_64 tiene corrección funcional en seL4 sin pruebas de corrección de
flujo de información ni de corrección binaria; se usa para hosts de desarrollo y la
base de compatibilidad NetBSD, pero no para la base nativa de seL4.

## Límites honestos de capacidad

El sustrato no pretende ser dueño de lo que no controla. El silicio, el microcódigo y
la mayor parte del firmware de arranque (Boot Guard, ME, PSP) están controlados por el
fabricante. En una lista corta y seleccionada de placas compatibles con Coreboot o
hardware OpenPOWER, el cargador de arranque sí es controlable. El sustrato es dueño del
kernel, la capa de sistema, la capa de aplicación, el registro de capacidades, el
rastro de identidad y auditoría, la procedencia de la construcción (*build
provenance*) y los artefactos de verificación formal.

## Arquitectura de implementación por fases

La higiene de espacio de trabajo de la Fase 0 para el clúster `project-system` está
pendiente. La Fase 1A — un prototipo de la primitiva de registro de capacidades que
vincula los checkpoints de multi-firma C2SP `signed-note` con la invocación de
capacidades — es trabajo planificado. La Fase 1B — el CLI de Rust `moonshot-toolkit`
para orquestar builds de seL4 con un arnés de construcción reproducible — es trabajo
fundacional planificado. El prototipo de la base de compatibilidad NetBSD, la
redacción de TOPIC y GUIDE, y el subconjunto mínimo de capacidades de
moonshot-kernel son fases posteriores.

## Véase también

- [[worm-ledger-architecture]] — el sustrato WORM primitivo que el Registro de Capacidades extiende
- [[compounding-doorman]] — el límite de inferencia que opera sobre el sustrato del sistema

## Referencias

1. Regla SEC 17a-4(f) — requisitos de preservación de registros electrónicos.
2. Reglamento eIDAS — firmas electrónicas cualificadas y servicios de confianza.
3. RFC 3161 — Protocolo de Sellado de Tiempo.
4. OpenTimestamps — sellado de tiempo anclado a Bitcoin.
