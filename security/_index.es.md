---
schema: foundry-doc-v1
title: "Seguridad y confianza"
slug: security-index
category: security
type: topic
content_type: topic
quality: complete
short_description: "Cómo se protege la plataforma y cómo se verifican sus registros: identidad y permisos, verificación criptográfica, límites de aislamiento, cómo se maneja y se mantiene privada la información, y los controles de la cadena de suministro diseñados para mantener el código honesto."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-07-28
editor: pointsav-engineering
paired_with: _index.md
---

La categoría **seguridad** recoge cómo se protege la plataforma y cómo se verifican sus registros. Abarca la identidad y los permisos, la verificación criptográfica, los límites de aislamiento, cómo se maneja y se mantiene privada la información, y los controles de la cadena de suministro diseñados para mantener el código honesto desde el colaborador hasta producción.

Esta es la respuesta de la plataforma a la pregunta del lector de diligencia — *¿se puede confiar en esto?* — y la puerta de entrada para los ingenieros que buscan un mecanismo de seguridad específico: control de acceso basado en capacidades, autenticación basada en máquinas, atestación, registros criptográficos, y el arranque de establecimiento de confianza por el que pasa un dispositivo antes de unirse a un despliegue.

## Identidad y permisos

Quién es conocido por el sistema, cómo lo demuestra un dispositivo, y qué se le permite hacer.

- [[capability-based-security|Seguridad basada en capacidades]] — el modelo de control de acceso: los componentes poseen tokens criptográficos verificados en lugar de privilegio ambiental
- [[machine-based-auth|Autorización basada en máquina]] — emparejar hardware con hardware reemplaza las contraseñas; el emparejamiento mismo es el permiso
- [[personnel-permissions|Personal y permisos]] — cómo la identidad del colaborador y los cuatro niveles de permiso se expresan mediante emparejamientos, no roles de base de datos
- [[identity-ledger-schema-design|Diseño del esquema del libro de identidad]] — los tipos de registro Person/Anchor/Claim detrás de la resolución de identidad de Ring 1
- [[verification-surveyor|Supervisor de verificación]] — el punto de control humano que confirma una identidad extraída antes de confirmarla

## Verificación criptográfica

Cómo un lector comprueba de forma independiente que un registro no ha sido alterado.

- [[crypto-attestation|Atestación criptográfica de carga útil]] — hash SHA-256 del lado del cliente que permitiría a cualquier visitante verificar que el contenido publicado no cambió en tránsito; hoy es un patrón cosmético y sin conectar presente en algunas plantillas, no una capacidad que ninguna superficie publicada ofrezca realmente
- [[cryptographic-ledgers|Libros contables criptográficos]] — el patrón de almacenamiento de estado inmutable: entradas encadenadas por hash, checkpoints firmados, anclaje mensual en Sigstore Rekor

## Límites de aislamiento

Qué contiene un compromiso una vez que ocurre. Delgado en relación con el alcance propio de la categoría — véanse los artículos de [[ppn-tenant-vm-isolation|aislamiento de inquilinos]] y [[service-vm-tenant|VM de inquilino]] en [[infrastructure|Dónde se ejecuta]] para el caso comercialmente relevante, que aún no está referenciado desde aquí.

- [[sel4-capability-topology|Topología de capacidades de seL4]] — por qué la seguridad en un sistema seL4 es la forma del grafo de capacidades, no una capa de política
- [[diode-standard|Estándar del diodo]] — el flujo unidireccional de comandos de autoridad a sujeto que elimina el movimiento lateral por diseño
- [[genesis-protocol|Protocolo génesis]] — la secuencia de arranque de flota que ejecuta un nodo en el primer arranque para alcanzar un estado seguro y reclamable

## Manejo de datos y privacidad

- [[data-sovereignty-telemetry|Soberanía de datos y telemetría de estado cero]] — el único artículo de esta categoría sobre esta cláusula por ahora; la retención, eliminación y cifrado en reposo aún no tienen artículo propio

## Controles de la cadena de suministro

Mantener el código honesto desde la máquina de un colaborador hasta producción.

- [[five-stage-supply-chain|Cadena de suministro de cinco etapas]] — la ruta de promoción de colaborador a cliente, controlada por un script de promoción fuertemente resguardado y no por una solicitud de extracción (pull request), y el air-gap doble ciego entre colaborador y cliente
- [[pre-commit-defense-in-depth|Defensa en profundidad pre-commit]] — la puerta de solo ayudante, el análisis de patrones de secretos y la guarda de tamaño que se ejecutan en cada confirmación

## Véase también

- [Arquitectura](/architecture/) — cómo está construida la plataforma
- [Gobernanza y estándares](/governance/) — qué se decidió y por qué es conforme
- [Dónde se ejecuta](/infrastructure/) — la infraestructura de almacenamiento y registro desplegada que protegen estos mecanismos
