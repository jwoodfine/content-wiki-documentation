---
schema: foundry-doc-v1
title: "La Doctrina del Sustrato del Sistema"
slug: topic-system-substrate-doctrine.es
category: architecture
type: topic
quality: published
short_description: La arquitectura de nivel de kernel bajo cada servicio de PointSav — un registro de capacidades con raíz en el cliente, una estrategia de SO soberana de dos bases, y mecanismos para capacidades de tiempo limitado, verificación reproducible y recuperación universal.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites:
  - sec-17a-4-f
  - eidas-qualified-preservation
  - rfc-3161
  - opentimestamps
paired_with: topic-system-substrate-doctrine.md
---

La **Doctrina del Sustrato del Sistema** define la capa debajo de cada sistema operativo, servicio y aplicación de PointSav: el kernel, el modelo de capacidades, el registro de auditoría y la ceremonia de transferencia de propiedad que juntos constituyen un despliegue criptográficamente soberano.

Dos afirmaciones principales impulsan la arquitectura. El **Sustrato del Registro de Capacidades** (Doctrina #33): el estado de capacidades del sistema en ejecución ES el registro WORM de solo anexado; el kernel consulta el registro antes de honrar cualquier invocación; el despliegue se deriva del registro. El **Sustrato Soberano de Dos Bases** (Doctrina #34): los mismos binarios se ejecutan ya sea en un kernel formalmente verificado (seL4 hoy, con un futuro moonshot-kernel en Rust sin estándar) o en un kernel de compatibilidad de grado soberano (NetBSD con Veriexec y construcciones reproducibles sin conexión).

## La inversión del modelo de atestación

Los sistemas existentes anclan la atestación en las claves del proveedor: los proveedores de nube en sus propias raíces de confianza, los stacks nacionales de identidad digital en claves del estado, los enclaves seguros en claves del fabricante del chip. En cada caso, la prueba atestada es prueba de los controles del proveedor, no de los controles del cliente.

La composición de Foundry invierte esto: cada cadena de atestación termina en la clave de firma apex propia del cliente. La clave apex es sostenida por el cliente: en su TPM, en un HSM que él posee y opera, o como una semilla impresa en papel para recuperación con espacio de aire. Ningún servicio de Foundry, ningún proveedor, ningún fabricante de chips se interpone entre el cliente y la raíz del registro.

## El Registro de Capacidades

Cada invocación de capacidad mediada por el kernel emite una entrada firmada a un registro Merkle con raíz en el cliente. El despliegue ES el registro: arrancar es reproducir el registro desde el génesis; apagar es añadir una entrada de apagado; actualizar es añadir una entrada de actualización de versión; rotar claves es añadir una entrada de rotación. El estado del despliegue en cualquier momento es la aplicación determinista de todas las entradas del registro hasta ese momento.

## Tres mecanismos

**Mecanismo A — Capacidades de Tiempo Limitado.** Una capacidad lleva una marca de tiempo de vencimiento y una clave pública de testigo. El kernel se niega a honrar la capacidad pasado el vencimiento a menos que se presente un registro de testigo firmado cuyo hash aparezca en la raíz Merkle del registro de capacidades actual. Extender una capacidad requiere una nueva firma de testigo Y una aparición en el registro público.

**Mecanismo B — Verificación Reproducible en Hardware del Cliente.** Cada versión incluye archivos de teoremas Isabelle/HOL para la parte de seL4 formalmente verificada, trazas de propiedad de Rust para la capa del sistema, y un grafo de construcción reproducible anclado a un registro de transparencia público. La verificación de inspección rápida está prevista para completarse en menos de 60 minutos en un portátil de uso comercial.

**Mecanismo C — Recuperación Universal de Capacidades.** La identidad operativa completa del cliente se reconstruye desde una semilla impresa en papel más el estado del registro de transparencia público. La semilla cabe en una tarjeta índice de tamaño estándar. No se requiere portal del proveedor, vuelta al cloud ni HSM para la recuperación.

## Las dos bases

El sustrato opera sobre dos bases: una base nativa de máxima seguridad (seL4 en AArch64, con moonshot-kernel previsto en Rust sin estándar) y una base de compatibilidad de grado soberano (NetBSD con Veriexec, `build.sh` reproducible sin conexión, y rump kernels). Los mismos binarios `os-*` se ejecutan en cualquiera de las dos bases mediante un delgado shim.

NetBSD se elige específicamente por su transferibilidad BSD de 2 cláusulas, Veriexec (análogo al arranque de solo imágenes verificadas de seL4), reproducibilidad sin conexión de `build.sh`, rump kernels para el puente IT/OT, 57 puertos de hardware oficiales, y una fundación independiente sin entrelazamiento con hiperscalares.

## Véase también

- [[worm-ledger-architecture]] — el sustrato WORM primitivo que el Registro de Capacidades extiende
- [[compounding-doorman]] — el límite de inferencia que opera sobre el sustrato del sistema

## Referencias

1. Regla SEC 17a-4(f) — requisitos de preservación de registros electrónicos.
2. Reglamento eIDAS — firmas electrónicas cualificadas y servicios de confianza.
3. RFC 3161 — Protocolo de Sellado de Tiempo.
4. OpenTimestamps — sellado de tiempo anclado a Bitcoin.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Atribución 4.0 Internacional](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.