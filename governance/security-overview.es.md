---
schema: foundry-doc-v1
title: "Resumen de seguridad"
slug: security-overview.es
short_description: "La postura de seguridad de la plataforma: aislamiento de hardware basado en capacidades, el estándar unidireccional Diode de flujo de comandos, el límite de inteligencia artificial Doorman, el registro de auditoría WORM, y cómo cada propiedad se ejecuta por arquitectura en lugar de controles de política que pueden configurarse incorrectamente."
lang: es
category: governance
type: topic
content_type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
editor: pointsav-engineering
cites: []
paired_with: security-overview.md
---

La plataforma PointSav aplica la seguridad a través de la arquitectura. Aislamiento basado en capacidades, flujo de comandos unidireccional, un libro WORM que hace estructuralmente imposible la modificación de registros, y un único límite de IA que registra cada llamada en el libro de auditoría por inquilino — estas propiedades se mantienen porque la arquitectura hace imposible su violación, no porque una política lo prohíba.

El servicio Portero centraliza todas las claves API externas y registra cada llamada de inferencia de IA. Ninguna solicitud de IA llega a un modelo externo sin pasar por este límite, y ninguna llamada al límite queda sin registrar. El registro no es opcional: es una propiedad estructural del Portero, no una configuración que un administrador pueda desactivar.

El estándar Diode impone una disciplina de flujo de comandos unidireccional en toda la flota. El tráfico fluye de autoridad a sujeto y nunca al revés. Un nodo que recibe un comando no puede iniciar un comando al nodo que lo envió. Los ataques de movimiento lateral requieren la lógica de enrutamiento que el Diode elimina.

Un responsable de seguridad puede verificar que la IA no ha tocado el registro autoritativo sin confiar en las afirmaciones del proveedor. La arquitectura de tres anillos proporciona la respuesta arquitectónicamente: los Anillos 1 y 2 no tienen ninguna importación, dependencia ni llamada en tiempo de ejecución que alcance el Anillo 3.

## Aislamiento de inquilinos

La plataforma aplica el aislamiento de inquilinos en tres capas:

**Aislamiento a nivel de kernel en el Anillo 1.** Los servicios de límite del Anillo 1 de cada inquilino se ejecutan como procesos separados con raíces de almacenamiento separadas. No existe ninguna ruta de código de los datos del Anillo 1 de un inquilino a los de otro. [[totebox-os|ToteboxOS]] aplica esto a nivel de kernel: la seguridad basada en capacidades significa que ningún componente puede acceder a los recursos de otro sin tener un token de capacidad criptográfico concedido explícitamente en el aprovisionamiento.

**Aislamiento de espacio de nombres en el Anillo 2.** Los servicios del Anillo 2 son multiinquilino mediante `moduleId`. El grafo de conocimiento y el índice de búsqueda de cada inquilino están aislados detrás de su espacio de nombres `moduleId` en cada ruta de lectura y escritura. Una consulta para el inquilino A no puede devolver registros del inquilino B.

**Aislamiento de IA de límite único en el Anillo 3.** [[service-slm]] es el único servicio del Anillo 3. Cada solicitud de IA pasa por el Portero, que sanea los datos de salida, enruta entre tres niveles de cómputo y escribe una fila de auditoría en el libro local del cliente antes de que se realice cualquier llamada externa.

## El límite del Portero

El Portero es el único punto por el que fluye toda la inferencia de IA. Aplica cinco propiedades:

**Ninguna clave vive fuera del Portero.** Las claves API para proveedores de IA externos se mantienen exclusivamente en el Portero. Ningún otro proceso de la plataforma tiene acceso a estas claves. Una brecha en cualquier servicio que no sea el Portero no puede exponer claves API externas.

**Cada llamada se registra antes de realizarse.** El Portero escribe una fila de auditoría en el libro local del cliente antes de enviar la llamada externa. Una llamada que falla en la capa de red sigue teniendo una entrada en el libro. La puerta de enlace del proveedor escribe una segunda fila de auditoría simultáneamente.

**Los datos de salida se sanean.** El Portero inspecciona cada carga útil de salida antes de que salga de la red del cliente. Los datos estructurados sujetos a las reglas de clasificación de datos de la plataforma se eliminan en este límite.

**La respuesta de entrada queda contenida.** La respuesta de un modelo externo vuelve al Portero y no se expone directamente a los servicios del Anillo 2 o del Anillo 1.

**El enrutamiento de nivel queda auditado.** El cliente puede ver en su libro local qué nivel de cómputo gestionó cada solicitud: local (Nivel A), ráfaga GPU (Nivel B) o API externa (Nivel C).

## El libro WORM

Cada servicio del Anillo 1 escribe en un libro de Solo Escritura y Múltiple Lectura. El libro no tiene operación de eliminación ni de sobreescritura — estas funciones no existen en el motor de almacenamiento. La modificación es estructuralmente imposible, no prohibida por política.

El libro está basado en tiles y encadenado por hash: cada tile contiene el hash del tile anterior. Cualquier modificación en cualquier tile rompe la cadena de hash y es detectable sin acceder a los sistemas propios de la plataforma. El servicio `[[fs-anchor-emitter]]` genera puntos de control firmados del libro a cadencia horaria y los prepara para su anclaje externo en el registro de transparencia público Sigstore Rekor mensualmente.

Esta estructura satisface la Regla SEC 17a-4(f), la preservación de registros electrónicos cualificados de eIDAS y SOC 2 — por garantía estructural, no por atestación de política que puede modificarse.

## El estándar Diode

El estándar Diode es la topología de seguridad de red fundamental de la flota PointSav. Los comandos fluyen de autoridad (os-orchestration, os-console) a sujeto (archivos Totebox, servicios) y nunca al revés.

Un archivo Totebox que recibe un comando de os-console no puede iniciar un comando de vuelta a os-console. La lógica de enrutamiento que permitiría esto no existe en la pila de comunicación. Esto elimina la superficie de ataque de movimiento lateral.

## Control de acceso basado en capacidades

La plataforma utiliza seguridad basada en capacidades en lugar de listas de control de acceso o control de acceso basado en roles. Un componente de software puede comunicarse con otro solo si tiene un token de capacidad criptográfico concedido explícitamente en el aprovisionamiento. No existe autoridad ambiente.

Un componente comprometido no puede escalar sus propios privilegios. Solo puede hacer lo que permite su conjunto de capacidades, y ese conjunto se fijó en el aprovisionamiento. [[machine-based-auth]] extiende este modelo a la autenticación del operador: el emparejamiento criptográfico entre el dispositivo de hardware del operador y el nodo de orquestación es el permiso.

## Véase también

- [[three-ring-architecture]] — el modelo de tres anillos y por qué la IA es estructuralmente opcional
- [[diode-standard]] — la disciplina de flujo de comandos unidireccional en detalle
- [[doorman-protocol]] — el servicio de límite de IA Portero y su lógica de enrutamiento
- [[capability-based-security]] — el modelo de aislamiento basado en capacidades en la capa del SO
- [[worm-ledger-design]] — la estructura del libro WORM y sus propiedades de cumplimiento
- [[architecture-decisions]] — las doce decisiones vinculantes, incluidas ADR-07, ADR-10 y ADR-19
- [[procurement-overview]] — términos de adquisición y estructura comercial para compradores regulados
