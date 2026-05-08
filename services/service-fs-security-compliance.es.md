---
schema: foundry-doc-v1
title: "Postura de seguridad y cumplimiento de service-fs"
slug: service-fs-security-compliance.es
category: services
type: topic
quality: complete
short_description: "service-fs está diseñado para almacenamiento estructural Write-Once-Read-Many que satisface SEC Rule 17a-4(f), eIDAS y SOC 2 — la modificación de registros no se deniega en la capa de políticas; se deniega por el motor de almacenamiento mismo, y el anclaje externo a Sigstore Rekor proporciona una prueba de estado independiente de los propios sistemas de la plataforma."
status: active
audience: vendor-public
bcsc_class: current-fact
last_edited: 2026-05-08
editor: pointsav-engineering
paired_with: service-fs-security-compliance.md
---

`service-fs` está diseñado para almacenamiento estructural Write-Once-Read-Many que satisface los requisitos de SEC Rule 17a-4(f), eIDAS y SOC 2 — la modificación de registros no se deniega en la capa de políticas; se deniega por el motor de almacenamiento mismo, y el anclaje externo a Sigstore Rekor proporciona una prueba de estado independiente de los propios sistemas de la plataforma. La postura de cumplimiento se deriva de propiedades arquitectónicas, no de controles configurables: el motor de almacenamiento Rust físicamente carece de la capacidad de eliminar o modificar registros; cada entrada está vinculada criptográficamente a la siguiente; y cualquier intento de alterar el historial es detectable mediante pruebas de consistencia Merkle.

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

## Véase también

- [[service-fs-architecture]]
- [[capability-based-security]]
- [[machine-based-auth]]
- [[sel4-foundation]]
