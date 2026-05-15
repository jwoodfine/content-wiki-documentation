---
schema: foundry-doc-v1
title: "Diseño del Libro de Registros WORM"
slug: worm-ledger-design.es
category: infrastructure
type: topic
quality: complete
short_description: "El sustrato de persistencia de escritura única y lectura múltiple (WORM) utilizado en los servicios Ring 1 de PointSav: un formato por bloques con encadenamiento criptográfico que satisface los requisitos de conservación de registros bajo regulación estadounidense, europea y SOC 2 por estructura, no por política."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
editor: pointsav-engineering
cites: []
references:
  - id: 1
    text: "C2SP. 'tlog-tiles: Tile-based logs specification.' C2SP.org, 2024."
    url: "https://c2sp.org/tlog-tiles"
  - id: 2
    text: "Sigstore Project. 'Rekor — Software Supply Chain Transparency Log.' Sigstore.dev, 2024."
    url: "https://rekor.sigstore.dev/"
  - id: 3
    text: "C2SP. 'signed-note: Signed checkpoint note format.' C2SP.org, 2024."
    url: "https://c2sp.org/signed-note"
  - id: 4
    text: "Laurie, B. et al. 'RFC 9162: Certificate Transparency Version 2.0.' IETF, 2021."
    url: "https://www.rfc-editor.org/rfc/rfc9162"
paired_with: worm-ledger-design.md
---


Los servicios del anillo 1 de la plataforma PointSav — la capa de ingesta de límites que gestiona registros del sistema de archivos, datos de personas, correo electrónico y entrada estructurada — requieren una persistencia que no pueda modificarse silenciosamente. Un registro escrito en un libro de registros del anillo 1 debe permanecer exactamente tal como fue escrito durante toda la vida del despliegue.

Este requisito no es exclusivo de PointSav. La regulación de conservación de registros para agentes bursátiles de EE. UU. bajo la Norma SEC 17a-4(f), los requisitos de conservación cualificada de la UE bajo el Reglamento de Ejecución (UE) 2025/1946 para eIDAS, y los Criterios de Servicios de Confianza SOC 2 especifican variantes del mismo requisito. El diseño del libro de registros WORM de la plataforma está estructurado para satisfacer los tres mediante el mismo mecanismo arquitectónico: la inmutabilidad la garantiza el sustrato de almacenamiento, no la política operativa.

## La pila de cuatro capas

**Capa 1 — Almacenamiento por bloques (tiles).** El formato en disco sigue la especificación C2SP tlog-tiles de forma literal [^1] — el mismo formato de bloques utilizado internamente por Trillian-Tessera y externamente por Sigstore Rekor v2. [^2] Esta alineación no es incidental: significa que cualquier herramienta del ecosistema de registros de transparencia puede verificar los bloques escritos por Foundry sin conversión de formato.

**Capa 2 — API del libro de registros WORM.** Un trait de Rust que expone las operaciones de apertura, adición, lectura, producción de punto de control firmado [^3] y verificación de pruebas de inclusión y consistencia. Implementaciones intercambiables: en memoria para pruebas, POSIX para producción.

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

## Véase también

- [[three-ring-architecture]] — el límite del anillo 1 donde opera el libro de registros WORM
- [[compounding-doorman]] — el servicio del anillo 3 cuyo libro de auditoría usa el mismo primitivo
- [[trajectory-substrate]] — el registro de señal de entrenamiento que utiliza el mismo formato de libro
