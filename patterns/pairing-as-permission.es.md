---
schema: foundry-doc-v1
title: "Emparejamiento como permiso"
slug: pairing-as-permission.es
category: patterns
type: topic
content_type: topic
quality: complete
short_description: "PairingAsPermission es el modelo de control de acceso por capacidades de objeto utilizado en la orquestación Totebox: un emparejamiento criptográfico entre dos nodos es el permiso, y la ausencia de emparejamiento hace estructuralmente imposible la conexión — no es acceso denegado, sino la inexistencia de un camino."
status: active
bcsc_class: no-disclosure-implication
last_edited: 2026-05-25
editor: pointsav-engineering
cites: []
references:
 - id: 1
 text: "Miller, M. S. et al. 'Capability Myths Demolished.' SRL2003-02, Johns Hopkins University, 2003."
 url: "https://srl.cs.jhu.edu/pubs/SRL2003-02.pdf"
 - id: 2
 text: "Google. 'Fuchsia Component Framework: Capabilities overview.' Fuchsia.dev, 2024."
 url: "https://fuchsia.dev/fuchsia-src/concepts/components/v2/capabilities"
 - id: 3
 text: "seL4 Project. 'seL4: Formally Verified Microkernel.' The seL4 Foundation, 2024."
 url: "https://sel4.systems/"
paired_with: pairing-as-permission.md
---

PairingAsPermission es el modelo de control de acceso utilizado en la [[totebox-orchestration|orquestación Totebox]]: un emparejamiento criptográfico entre dos nodos es el permiso, y la ausencia de emparejamiento hace estructuralmente imposible la conexión — no es acceso denegado, sino la inexistencia de un camino. No hay lista central de control de acceso, ni búsqueda de permisos en tiempo de solicitud, ni tabla de roles. El modelo es el patrón formalmente probado de Capacidades de Objeto, desplegado en producción en Fuchsia OS, seL4 y WireGuard. PairingAsPermission es canónico en el espacio de trabajo; los sinónimos RBAC, ACL y PermissionSystem se rechazan explícitamente.

Este artículo describe el principio, la topología en la orquestación Totebox, los riesgos de ingeniería y las implementaciones de referencia en producción.

## El principio fundamental

En la mayoría de los sistemas de control de acceso, llega una solicitud, el sistema busca si el solicitante tiene permiso y permite o rechaza la solicitud. La búsqueda requiere una autoridad central: una base de datos, un almacén de políticas de roles, una tabla de permisos.

PairingAsPermission elimina la búsqueda. Dos nodos se comunican solo si se ha establecido un emparejamiento criptográfico entre ellos. Si no existe emparejamiento, no existe conexión y no se realiza solicitud. La pregunta "¿tiene este nodo permiso para alcanzar a aquel nodo?" tiene una respuesta estructural: comprobar si existe un emparejamiento. Si no, no existe camino para preguntar en primer lugar.

Este es el modelo de Capacidades de Objeto — un patrón de seguridad formalmente probado descrito por primera vez por Mark S. Miller en *Capability Myths Demolished* (2003). [^1] El axioma central: **la conectividad genera conectividad.** El objeto A puede enviar un mensaje a B solo si A posee una referencia a B. La referencia es la capacidad. Sin la referencia, la conexión es estructuralmente imposible — no es acceso denegado, sino la inexistencia de un camino.

## La topología en la orquestación Totebox

La topología de la orquestación Totebox es:

- **Comando** (el concentrador os-orchestration) está emparejado con: cada archivo Totebox, ambos nodos os-mediakit y ambos nodos os-privategit. La lista de emparejamientos del Comando es el mapa topológico de hecho.
- **Las instancias de os-orchestration por proyecto** están emparejadas únicamente con sus propios archivos Totebox. Una orquestación de un proyecto no puede alcanzar la orquestación de otro proyecto — no existe emparejamiento.
- **La coordinación entre proyectos** fluye a través del Comando: una orquestación de proyecto envía un mensaje al Comando; el Comando, emparejado con ambos, recupera los datos o enruta la solicitud. No se crea ninguna conexión lateral directa entre orquestaciones por proyecto.

El mapa de permisos es el diagrama de arquitectura. No existe documento separado de control de acceso — la topología de emparejamientos en vivo es el registro autoritativo.

## Sin registro central

No existe registro central que documente quién está emparejado con quién. Es deliberado.

El estado de los emparejamientos está distribuido: existe entre los propios nodos. Cada nodo posee las claves públicas de sus pares emparejados. El Comando mantiene `pairings.yaml` — un registro de sus conexiones activas (punto final, clave pública, identificador de módulo, fecha de emparejamiento) — pero es el registro operativo del Comando, no una autoridad central. Si el Comando pierde su lista de emparejamientos, los emparejamientos pueden restablecerse porque cada par aún posee la clave pública del Comando y el Comando aún posee la clave pública de cada par. La verdad está distribuida.

Esto refleja el modelo de propiedad de Bitcoin: no hay banco central que registre quién posee qué monedas. El estado de propiedad es la cadena de bloques — distribuido, verificable, sin requerir autoridad. En PairingAsPermission, el estado del emparejamiento es la topología. Un nuevo archivo Totebox se declara mediante su `MANIFEST.md` (identidad de instancia más clave pública); el Comando lo añade a sus conexiones activas. La conexión es la autorización. Ninguna autoridad externa la aprueba ni la registra.

El diseño habilita un despliegue verdaderamente distribuido: un archivo Totebox puede residir en cualquier proveedor de nube, cualquier centro de datos o un nodo de cómputo mínimo. El Comando solo necesita el punto final del archivo y la clave pública para establecer un emparejamiento.

## Por qué es más fuerte que las tablas de roles

Los sistemas basados en roles y listas de acceso comparten una vulnerabilidad estructural: el **problema del adjunto confuso**. Un intermediario de confianza — un proceso con permisos elevados — puede ser engañado para realizar una acción en nombre de un solicitante de menor confianza. El intermediario usa sus propios permisos para hacer algo que el solicitante no podría hacer directamente. La vulnerabilidad es estructural; está presente en cualquier sistema donde la autoridad se busca en una tabla en tiempo de solicitud.

En el modelo de Capacidades de Objeto, esta vulnerabilidad es un invariante arquitectónico. Un titular no puede usar lo que nunca se le entregó como referencia. Una orquestación por proyecto no puede instruir al Comando para que actúe en su nombre en una operación entre proyectos a menos que la orquestación por proyecto ya posea la capacidad entre proyectos — que no posee. El Comando valida el alcance del solicitante en cada solicitud antes de actuar. La validación no es una capa de seguridad opcional; es la definición de lo que hace el Comando.

## Implementaciones en producción

No es un modelo teórico. Está desplegado a escala en sistemas de producción.

**Fuchsia OS** (Google) implementa PairingAsPermission a nivel del sistema operativo. Cada componente debe tener capacidades enrutadas explícitamente a él a través de la topología de componentes. Un componente que no ha recibido una ruta de capacidad es estructuralmente inalcanzable desde el recurso — no es acceso denegado, sino la inexistencia de un camino. Fuchsia se ejecuta en cada modelo de Google Nest Hub. [^2]

**El microkernel seL4** tiene una prueba formal verificada por máquina del confinamiento de capacidades: un proceso no puede acceder a un recurso para el que no se le ha otorgado explícitamente una capacidad. La prueba cubre la integridad (los datos no pueden modificarse sin autoridad) y el confinamiento de la autoridad (la autoridad no puede exceder lo delegado). seL4 es el estándar de referencia para los modelos de seguridad formalmente verificados. [^3]

**WireGuard** implementa el mismo patrón en la capa de red. La tabla `AllowedIPs` es la tabla de capacidades. Un nodo sin entrada para un destino no puede enviar paquetes hacia él. El control de acceso es estructural al enrutamiento, no una verificación en el momento de la transmisión.

## Tres riesgos de ingeniería y sus defensas

**Riesgo 1 — Adjunto confuso en el Comando (alto)**
Una orquestación por proyecto envía al Comando un mensaje pidiéndole que realice una operación entre proyectos. Si el Comando reenvía sin validar el alcance del solicitante, el solicitante ha ejecutado una capacidad que no posee, usando al Comando como adjunto.

Defensa: el Comando valida el alcance del solicitante en cada solicitud. La implementación planificada `app-orchestration-command` incluye esta verificación como la primera operación en el manejo de solicitudes. No es opcional.

**Riesgo 2 — El Comando como punto único de fallo de disponibilidad (medio)**
Si el Comando no está disponible, la coordinación entre archivos queda bloqueada.

Defensa: los archivos por proyecto operan plenamente sin el Comando — sirven recursos locales y encolan las solicitudes entre archivos para reintento. Sin fallo duro. La redundancia activo-pasivo del Comando es una adición planificada para una fase posterior.

**Riesgo 3 — Multitenencia en nodos físicos compartidos (medio)**
Cuando múltiples proyectos lógicos comparten un único nodo de archivo Totebox, el Comando posee capacidades de múltiples inquilinos. Si el Comando usa el token de capacidad incorrecto para una solicitud, los datos de un inquilino quedan accesibles bajo el alcance de otro inquilino.

Defensa: atenuación de capacidades mediante identificadores de módulo separados. El Comando posee tokens `X-Module-ID` distintos por inquilino. El archivo compartido aplica las particiones por identificador. La pasarela de control de acceso `service-slm` ya implementa este patrón — el Comando debe pasar el identificador de módulo correcto del archivo solicitante en cada llamada, nunca el suyo propio.

## Implementación

La implementación actual usa `system-mba-shim` — una capa transitoria detrás de la cual se ubica autenticación OAuth2 convencional. La interfaz `system-mba-shim` es el límite limpio: cuando el modelo criptográfico completo de PairingAsPermission (intercambio de claves entre pares basado en certificados) reemplace la capa OAuth2, no cambiará ningún código que llame. La interfaz permanece constante; la implementación detrás de ella se actualiza en su lugar.

Los Seis Contratos de Orquestación incluyen `pairing_attestation` como `SYS-CONTRACTS-01`, integrado en el núcleo del sistema operativo. No es configurable.

## El sistema confiable

PairingAsPermission es una capa del patrón del Sistema Confiable: la confiabilidad atestiguable de la arquitectura se compone con el tiempo. Cada evento de emparejamiento es una entrada en un libro mayor inmutable — la historia de quién estuvo conectado con qué es solo de adición. La Atestación del Sistema Confiable produce informes firmados trimestralmente que extienden la cadena de atestación. Los permisos del ápice se co-firman. La topología de emparejamientos en cualquier momento es auditable desde el `pairings.yaml` del Comando más los archivos `MANIFEST.md` distribuidos en posesión de cada par emparejado.

El emparejamiento es el permiso. La topología es la auditoría.

## Véase también

- [[totebox-orchestration-development]] — arquitectura de desarrollo de la orquestación Totebox que aplica este modelo
- [[doorman-protocol]] — el servicio Doorman que opera como pasarela en la topología de capacidades
- [[machine-based-auth]] — capa de autenticación basada en máquinas que opera junto al modelo de emparejamiento
- [[compounding-substrate]] — la arquitectura más amplia dentro de la cual este modelo de acceso se compone
- [[three-ring-architecture]] — el modelo de límite de anillos que PairingAsPermission aplica estructuralmente

