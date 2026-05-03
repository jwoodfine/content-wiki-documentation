---
schema: foundry-doc-v1
title: "Diseño del Libro de Registros WORM"
slug: worm-ledger-design.es
category: architecture
type: topic
quality: published
short_description: "El sustrato de persistencia de escritura única y lectura múltiple (WORM) utilizado en los servicios Ring 1 de PointSav: un formato por bloques con encadenamiento criptográfico que satisface los requisitos de conservación de registros bajo regulación estadounidense, europea y SOC 2 por estructura, no por política."
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: worm-ledger-design.md
---

Los servicios del anillo 1 de la plataforma PointSav — la capa de ingesta de límites que gestiona registros del sistema de archivos, datos de personas, correo electrónico y entrada estructurada — requieren una persistencia que no pueda modificarse silenciosamente. Un registro escrito en un libro de registros del anillo 1 debe permanecer exactamente tal como fue escrito durante toda la vida del despliegue.

Este requisito no es exclusivo de PointSav. La regulación de conservación de registros para agentes bursátiles de EE. UU. bajo la Norma SEC 17a-4(f), los requisitos de conservación cualificada de la UE bajo el Reglamento de Ejecución (UE) 2025/1946 para eIDAS, y los Criterios de Servicios de Confianza SOC 2 especifican variantes del mismo requisito. El diseño del libro de registros WORM de la plataforma está estructurado para satisfacer los tres mediante el mismo mecanismo arquitectónico: la inmutabilidad la garantiza el sustrato de almacenamiento, no la política operativa.

## La pila de cuatro capas

**Capa 1 — Almacenamiento por bloques (tiles).** El formato en disco sigue la especificación C2SP tlog-tiles de forma literal — el mismo formato de bloques utilizado internamente por Trillian-Tessera y externamente por Sigstore Rekor v2. Esta alineación no es incidental: significa que cualquier herramienta del ecosistema de registros de transparencia puede verificar los bloques escritos por Foundry sin conversión de formato.

**Capa 2 — API del libro de registros WORM.** Un trait de Rust que expone las operaciones de apertura, adición, lectura, producción de punto de control firmado y verificación de pruebas de inclusión y consistencia. Implementaciones intercambiables: en memoria para pruebas, POSIX para producción.

**Capa 3 — Protocolo de red.** Una capa de servicio HTTP que expone la API del libro de registros en red, con el protocolo MCP (estándar 2026 para servicios de herramientas de IA) superpuesto.

**Capa 4 — Anclaje externo.** Publicación mensual de los puntos de control de bloques en el registro de transparencia Sigstore Rekor v2. Un auditor externo puede confirmar la integridad de un registro sin involucrar al operador de la plataforma.

## Inmutabilidad estructural

La implementación POSIX sigue un patrón de escritura de cuatro pasos: escribir los bytes del bloque en un archivo temporal, sincronizar con fsync, renombrar atómicamente a la ruta canónica, y establecer los permisos en modo sólo lectura. La estructura de cadena de hash del formato significa que cualquier modificación de un bloque escrito altera la cadena — la modificación es detectable sin registro de auditoría adicional.

## Soberanía del cliente y anclaje dual

Los despliegues ToteboxOS del cliente operan sus propias instancias de libro de registros con sus propias claves de firma. El cliente es el sujeto de sus propios registros y posee la clave criptográfica que los atestigua. El espacio de trabajo del proveedor ancla independientemente los mismos puntos de control de bloques, proporcionando verificabilidad redundante: un auditor externo puede confirmar que un registro del cliente aparece tanto en el anclaje del cliente como en el del proveedor con el mismo hash criptográfico. El cliente puede excluir al proveedor del arreglo de anclaje en cualquier momento.

Esta propiedad estructural — soberanía de claves del cliente con redundancia opcional del proveedor — no está disponible en un servicio en la nube administrado, que es arquitectónicamente el custodio tanto de los datos como de la clave de firma.

## Mapeo de cumplimiento

La Norma SEC 17a-4(f) exige formato no reescribible con verificación de marca de tiempo y capacidad de verificación independiente de terceros. El formato de bloques satisface el primer requisito estructuralmente; los puntos de control firmados mensualmente aportan la marca de tiempo y la verificación de terceros mediante el registro público de transparencia.

La conservación cualificada bajo eIDAS exige preservación independiente de cambios tecnológicos futuros, integridad y autenticación del originador. La agilidad de algoritmo — el libro de registros lleva un campo de algoritmo de hash explícito en cada punto de control — aborda el primer requisito. El formato de bloques es una especificación abierta legible con herramientas estándar.

## Ver también

- [[three-ring-architecture]] — el límite del anillo 1 donde opera el libro de registros WORM
- [[compounding-doorman]] — el servicio del anillo 3 cuyo libro de auditoría usa el mismo primitivo

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*
