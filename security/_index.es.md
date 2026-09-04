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
last_edited: 2026-09-04
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
- [[capability-based-security|Seguridad basada en capacidades]] — La seguridad basada en capacidades entrega a cada componente un token infalsificable y acotado que debe presentar para actuar, en lugar del privilegio ambiental. Hoy la implementa una única capa de software; la aplicación a nivel de kernel está planificada.
- [[machine-based-auth|Autorización basada en máquina]] — El acceso se concede a la clave de un dispositivo, no a la contraseña de una persona. Una ceremonia de emparejamiento con código corto liga la huella de una clave SSH a un registro de usuario tras la aprobación del operador, sin almacenar ninguna contraseña en ningún sitio.
- [[personnel-permissions|Personal y permisos]] — Cuatro niveles de permisos, de P1 a P4, implementados como una enumeración tipada y servidos a través de un endpoint HTTP que lee un archivo de configuración del espacio de trabajo. Ese archivo no declara hoy ningún colaborador, de modo que el endpoint no resuelve nada para ningún usuario real.
- [[identity-ledger-schema-design|Diseño del esquema del libro de identidad]] — Tres tipos de registro — Person, Anchor y Claim — separan quién es conocido de cómo fue observado y de qué se afirmó sobre él. La identidad es un UUIDv5 de un correo en minúsculas, de modo que la misma entrada produce siempre el mismo identificador.
- [[verification-surveyor|Supervisor de verificación]] — Una herramienta de línea de comandos que exige a una persona confirmar cada identidad extraída contra evidencia externa antes de que ascienda de una cola a un registro verificado, con un tope de diez confirmaciones al día.
<!-- END AUTO-GENERATED -->

## Verificación criptográfica {#group-count-2}

Cómo un lector comprueba de forma independiente que un registro no ha sido alterado.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: cryptographic-verification -->
- [[crypto-attestation|Atestación criptográfica de carga útil]] — La atestación criptográfica permite a un lector recalcular el hash del contenido publicado y compararlo con un valor publicado. Existen prototipos cosméticos y sin conectar en unas pocas plantillas de publicación; el wiki de conocimiento no ofrece esta función.
- [[cryptographic-ledgers|Libros contables criptográficos]] — Un registro de solo anexado en el que el hash de cada entrada cubre a la anterior, cerrado con puntos de control firmados con Ed25519 y anclado mensualmente en un registro público de transparencia. Implementado como cadena lineal, con un archivo plano por inquilino.
<!-- END AUTO-GENERATED -->

## Límites de aislamiento {#group-count-3}

Qué contiene un compromiso una vez que ocurre. Delgado en relación con el alcance propio de la
categoría — véanse los artículos de [[ppn-tenant-vm-isolation|aislamiento de inquilinos]] y
[[service-vm-tenant|VM de inquilino]] en [Dónde se ejecuta](/category/infrastructure) para el caso
comercialmente relevante, que aún no está referenciado desde aquí.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: isolation-boundaries -->
- [[sel4-capability-topology|Topología de capacidades de seL4]] — En un sistema seL4 la política de seguridad es la forma del grafo de capacidades establecido en el arranque, no una capa de política en tiempo de ejecución. El trabajo propio son nueve binarios de prueba sobre hardware desnudo; ningún servicio de la plataforma se ejecuta sobre seL4.
- [[diode-standard|Estándar del diodo]] — El Estándar del Diodo es la regla de diseño según la cual los comandos y los datos circulan en una sola dirección, de la autoridad al sujeto. Varios mecanismos reales la cumplen; ningún componente la aplica como estándar con nombre propio.
- [[genesis-protocol|Protocolo génesis]] — El Genesis Protocol es la secuencia diseñada de arranque de flota para nodos os-infrastructure: enviarse sin configuración previa, arrancar en cualquier red y alcanzar un estado seguro y reclamable sin necesitar contacto con el plano de control.
<!-- END AUTO-GENERATED -->

## Manejo de datos y privacidad {#group-count-1}

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: data-handling-and-privacy -->
- [[data-sovereignty-telemetry|Soberanía de datos y telemetría de estado cero]] — La telemetría de estado cero es la postura prevista: medir el uso de un sitio sin conservar datos identificativos. La canalización que se ejecuta hoy escribe direcciones IP completas y sin enmascarar en un archivo de texto plano durante hasta un año; el enmascaramiento no está implementado.
<!-- END AUTO-GENERATED -->

## Controles de la cadena de suministro {#group-count-2}

Mantener el código honesto desde la máquina de un colaborador hasta producción.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: supply-chain-controls -->
- [[five-stage-supply-chain|Cadena de suministro de cinco etapas]] — El camino que va del commit de un colaborador al despliegue de un cliente atraviesa tres niveles de repositorio y dos organizaciones, controlado por un script de promoción fuertemente resguardado. No hay solicitud de extracción (pull request) ni revisión por un segundo interviniente.
- [[pre-commit-defense-in-depth|Defensa en profundidad pre-commit]] — Cuatro hooks de git independientes se ejecutan antes de que un commit quede registrado: una compuerta de solo-helper, un bloqueo por ruta de datos, un escaneo de secretos y tamaño sobre el contenido preparado, y una comprobación de identidad del autor. Toda elusión queda registrada.
<!-- END AUTO-GENERATED -->

## Lo que esto no es

Varios artículos enlazados aquí describen mecanismos planificados, aún no construidos, y
están matizados en su propio texto. Esta página es una orientación, no una certificación
de cumplimiento.

## Véase también

- [Cómo Está Construido](/architecture/) — cómo está construida la plataforma
- [Gobernanza y estándares](/governance/) — qué se decidió y por qué es conforme
- [Dónde se ejecuta](/infrastructure/) — la infraestructura de almacenamiento y registro desplegada que protegen estos mecanismos
