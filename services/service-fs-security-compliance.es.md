---
schema: foundry-doc-v1
type: topic
slug: service-fs-security-compliance
title: Seguridad y Cumplimiento de Service-FS
audience: vendor-public
bcsc_class: current-fact
language: es
paired_with: service-fs-security-compliance.md
---

# Seguridad y Cumplimiento de Service-FS

`service-fs` está diseñado para cumplir con los estándares internacionales más exigentes de almacenamiento inmutable y soberanía de datos. Nuestra arquitectura WORM asegura que los registros no puedan ser borrados ni modificados, cumpliendo con las normativas financieras y de confianza globales.

## Alineación Regulatoria

- **SEC Rule 17a-4 (EE. UU.):** Cumplimos con la ruta estricta de inmutabilidad física, superando las soluciones de nube tradicionales que permiten modificaciones ocultas.
- **eIDAS (UE):** Alineado con los estándares de preservación calificada para garantizar la validez legal de los documentos a largo plazo.
- **SOC 2:** El sistema está preparado para auditorías de integridad de procesamiento mediante firmas digitales y registros de auditoría inmutables.

## Seguridad Estructural

1. **Inmutabilidad por Diseño:** El código carece físicamente de funciones para borrar datos.
2. **Cadena de Merkle:** Cada dato está encadenado criptográficamente al anterior. Cualquier alteración es detectable al instante.
3. **Aislamiento de Clientes:** En su despliegue final (seL4), la separación entre clientes es matemática y física, no solo lógica.
4. **Lectura a 100 años:** Usamos formatos de texto abierto, permitiendo que cualquier arqueólogo digital del futuro pueda leer los datos sin necesidad de software propietario.

Esta postura protege a la empresa contra el secuestro de datos (ransomware), el error humano y la obsolescencia del proveedor de software.
