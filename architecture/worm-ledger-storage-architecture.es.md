---
schema: foundry-doc-v1
type: topic
slug: worm-ledger-storage-architecture
title: Arquitectura de Almacenamiento del Ledger WORM
audience: vendor-public
bcsc_class: current-fact
language: es
paired_with: worm-ledger-storage-architecture.md
---

# Arquitectura de Almacenamiento del Ledger WORM

La arquitectura de Foundry se basa en la inmutabilidad estructural, garantizando que los archivos de datos sean permanentes y legibles a largo plazo.

## El Motor de Almacenamiento por Teselas (Tiles)

Foundry utiliza el estándar **C2SP tlog-tiles**, dividiendo el historial de datos en archivos estáticos e inmutables:
- **Transparencia DARP:** Los datos se guardan en formato de texto plano (base64), legibles por cualquier sistema operativo futuro.
- **Integridad Criptográfica:** Cada dato se encadena en un "Árbol de Merkle", permitiendo demostrar que ningún registro ha sido alterado sin necesidad de leer todo el archivo.

## Dualidad de Ejecución

El mismo código está diseñado para funcionar en dos entornos:
1. **Hoy (Linux/BSD):** Como un proceso estándar con seguridad basada en permisos de archivos.
2. **Futuro (seL4):** Como un micro-kernel verificado matemáticamente, donde la seguridad es física y estructural.

## Cumplimiento Global

Este diseño cumple con las normativas SEC (EE. UU.) y eIDAS (UE), devolviendo la soberanía de los datos a la empresa y asegurando que la información sea accesible y válida legalmente durante décadas, independientemente de la evolución del software.


---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™ y Totebox Archive™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos titulares.*
