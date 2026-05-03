---
schema: foundry-doc-v1
type: guide
slug: fs-anchor-emitter
title: Guía de Configuración del Emisor de Anclaje (FS Anchor Emitter)
audience: vendor-public
bcsc_class: current-fact
language: es
paired_with: fs-anchor-emitter.md
---

# Guía de Configuración del Emisor de Anclaje (FS Anchor Emitter)

El emisor de anclaje es el componente encargado de generar "puntos de control" (checkpoints) firmados del ledger inmutable. Estos puntos de control son esenciales para demostrar la integridad de los datos ante auditorías externas.

## Requisitos de Configuración

El emisor requiere las siguientes variables de entorno:
- **FS_LEDGER_ROOT:** Ubicación de los datos del cliente.
- **FS_SIGNING_KEY:** Ruta a la clave privada del cliente (Ed25519).
- **FS_ANCHOR_INTERVAL:** Frecuencia de generación (se recomienda 1 hora).

## Funcionamiento

1. **Generación de Firma:** El emisor lee el estado actual del ledger y genera un archivo de texto con el tamaño del árbol y el hash raíz.
2. **Formato Estándar:** Utiliza el formato `signed-note` de C2SP, compatible con el ecosistema Sigstore Rekor.
3. **Prueba de Consistencia:** Se prevé que el sistema verifique que el nuevo estado sea una continuación válida del anterior antes de firmar, detectando cualquier intento de manipulación accidental o malintencionada.

## Anclaje Externo

Aunque los puntos de control se generan cada hora, su publicación en la red de transparencia Rekor está programada actualmente para realizarse de forma mensual, proporcionando una prueba de existencia externa e irrefutable de los datos de la empresa.


---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™ y Totebox Archive™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos titulares.*
