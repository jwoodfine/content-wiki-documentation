---
schema: foundry-doc-v1
title: "Seguridad y confianza"
slug: security-index
category: security
type: topic
content_type: topic
index_type: thematic
index_scope: security
quality: complete
short_description: "Cómo se protege la plataforma y cómo se verifican sus registros: identidad y permisos, verificación criptográfica, límites de aislamiento, cómo se maneja y se mantiene privada la información, y los controles de la cadena de suministro diseñados para mantener el código honesto."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-04
editor: pointsav-engineering
paired_with: _index.md
---

**La seguridad y la confianza** en esta plataforma descansan en una idea: cada componente posee
una credencial verificada y acotada que debe presentar para actuar — no una concesión heredada de
confianza. Esa disciplina se manifiesta en cinco áreas: quién es conocido por el sistema y qué se
le permite hacer, cómo un lector verifica de forma independiente que un registro no ha sido
alterado, qué contiene un compromiso una vez que ocurre, cómo se maneja y se mantiene privada la
información, y los controles que mantienen el código honesto desde la máquina de un colaborador
hasta producción.

La pregunta real de un lector de diligencia es *¿se puede confiar en esto?* La de un ingeniero
suele ser más específica — *¿cómo funciona realmente el control de acceso basado en
capacidades?* Ambas empiezan más abajo.

<!-- START-HERE-HIGHLIGHT: el motor lee este bloque para la tarjeta "empezar aquí"
     (reutiliza el componente cluster-card--start-here existente). No añadir más de una. -->
**Empezar aquí:** [[capability-based-security|Seguridad basada en capacidades]] — el modelo de
control de acceso que da nombre a toda la categoría: los componentes poseen tokens criptográficos
verificados en lugar de privilegio ambiental. Hoy existe una sola capa de software que lo
implementa; la aplicación a nivel de núcleo está planificada.
<!-- END-START-HERE-HIGHLIGHT -->

## Identidad y permisos {#group-count-5}

Quién es conocido por el sistema, cómo lo demuestra un dispositivo, y qué se le permite hacer.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: identity-and-permissions -->
- [[capability-based-security|Seguridad basada en capacidades]] — el modelo de control de acceso: los componentes poseen tokens criptográficos verificados en lugar de privilegio ambiental
- [[machine-based-auth|Autorización basada en máquina]] — emparejar hardware con hardware reemplaza las contraseñas; el emparejamiento mismo es el permiso
- [[personnel-permissions|Personal y permisos]] — cómo la identidad del colaborador y los cuatro niveles de permiso se expresan mediante emparejamientos, no roles de base de datos
- [[identity-ledger-schema-design|Diseño del esquema del libro de identidad]] — los tipos de registro Person/Anchor/Claim detrás de la resolución de identidad de Ring 1
- [[verification-surveyor|Supervisor de verificación]] — el punto de control humano que confirma una identidad extraída antes de confirmarla
<!-- END AUTO-GENERATED -->

## Verificación criptográfica {#group-count-2}

Cómo un lector comprueba de forma independiente que un registro no ha sido alterado.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: cryptographic-verification -->
- [[crypto-attestation|Atestación criptográfica de carga útil]] — hash SHA-256 del lado del cliente que permitiría a cualquier visitante verificar que el contenido publicado no cambió en tránsito; hoy es un patrón cosmético y sin conectar presente en algunas plantillas, no una capacidad que ninguna superficie publicada ofrezca realmente
- [[cryptographic-ledgers|Libros contables criptográficos]] — el patrón de almacenamiento de estado inmutable: entradas encadenadas por hash, checkpoints firmados, anclaje mensual en Sigstore Rekor
<!-- END AUTO-GENERATED -->

## Límites de aislamiento {#group-count-3}

Qué contiene un compromiso una vez que ocurre. Delgado en relación con el alcance propio de la
categoría — véanse los artículos de [[ppn-tenant-vm-isolation|aislamiento de inquilinos]] y
[[service-vm-tenant|VM de inquilino]] en [[infrastructure|Dónde se ejecuta]] para el caso
comercialmente relevante, que aún no está referenciado desde aquí.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: isolation-boundaries -->
- [[sel4-capability-topology|Topología de capacidades de seL4]] — por qué la seguridad en un sistema seL4 es la forma del grafo de capacidades, no una capa de política
- [[diode-standard|Estándar del diodo]] — el flujo unidireccional de comandos de autoridad a sujeto que elimina el movimiento lateral por diseño
- [[genesis-protocol|Protocolo génesis]] — la secuencia de arranque de flota que ejecuta un nodo en el primer arranque para alcanzar un estado seguro y reclamable
<!-- END AUTO-GENERATED -->

## Manejo de datos y privacidad {#group-count-1}

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: data-handling-and-privacy -->
- [[data-sovereignty-telemetry|Soberanía de datos y telemetría de estado cero]] — el único artículo de esta categoría sobre esta cláusula por ahora; la retención, eliminación y cifrado en reposo aún no tienen artículo propio
<!-- END AUTO-GENERATED -->

## Controles de la cadena de suministro {#group-count-2}

Mantener el código honesto desde la máquina de un colaborador hasta producción.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: supply-chain-controls -->
- [[five-stage-supply-chain|Cadena de suministro de cinco etapas]] — la ruta de promoción de colaborador a cliente, controlada por un script de promoción fuertemente resguardado y no por una solicitud de extracción (pull request), y el air-gap doble ciego entre colaborador y cliente
- [[pre-commit-defense-in-depth|Defensa en profundidad pre-commit]] — la puerta de solo ayudante, el análisis de patrones de secretos y la guarda de tamaño que se ejecutan en cada confirmación
<!-- END AUTO-GENERATED -->

## Lo que esto no es

Esta página no sustituye la lectura de los artículos enlazados — la anotación de una línea de
cada grupo orienta, no reemplaza las advertencias propias del mecanismo subyacente ni su propia
sección "qué no es esto". No es exhaustiva de todo hecho relevante para la seguridad en esta
wiki: los límites de aislamiento son especialmente delgados aquí porque el trabajo de
aislamiento de inquilinos comercialmente relevante vive en [[infrastructure|Dónde se ejecuta]],
no en esta categoría. No es una certificación de cumplimiento: varios artículos enlazados
describen mecanismos planificados, aún no construidos, con el matiz correspondiente en su propio
texto.

## Véase también

- [Arquitectura](/architecture/) — cómo está construida la plataforma
- [Gobernanza y estándares](/governance/) — qué se decidió y por qué es conforme
- [Dónde se ejecuta](/infrastructure/) — la infraestructura de almacenamiento y registro desplegada que protegen estos mecanismos
