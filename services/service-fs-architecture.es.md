---
schema: foundry-doc-v1
type: topic
slug: service-fs-architecture
title: Arquitectura de Service-FS: El Núcleo WORM
audience: vendor-public
bcsc_class: current-fact
language: es
paired_with: service-fs-architecture.md
---

# Arquitectura de Service-FS: El Núcleo WORM

`service-fs` es el sustrato de almacenamiento inmutable (WORM) de Foundry, diseñado para ser la columna vertebral de persistencia para todos los servicios de la plataforma. Garantiza que cada registro sea permanente, auditable y soberano.

## Estructura de Cuatro Capas

- **Anclaje (L4):** Publicación mensual de pruebas de integridad en registros públicos externos.
- **Protocolo (L3):** Interfaz de comunicación que asegura que los datos de un cliente nunca se mezclen con otros.
- **Contrato API (L2):** Definiciones en Rust que aseguran la consistencia del sistema independientemente de la tecnología de disco.
- **Almacenamiento (L1):** El motor físico que guarda los datos en formato de texto estándar (ISO IFC compatible), asegurando su lectura dentro de un siglo.

## Entornos de Ejecución

El sistema es dual por diseño:
- **Actualidad:** Funciona como un servicio estándar en Linux (Daemon), ideal para servidores actuales.
- **Futuro:** Está preparado para ejecutarse como un micro-kernel verificado (seL4) en dispositivos físicos, proporcionando la máxima seguridad matemática posible hoy en día.

Esta arquitectura protege contra la obsolescencia tecnológica y el secuestro de datos, devolviendo el control total del archivo histórico al propietario del edificio o empresa.
