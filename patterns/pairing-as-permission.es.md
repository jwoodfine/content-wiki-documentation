---
schema: foundry-doc-v1
title: "Emparejamiento como permiso"
slug: pairing-as-permission
category: patterns
type: topic
content_type: topic
quality: complete
index_group: sovereignty-and-infrastructure-patterns
short_description: "El principio de control de acceso por Capacidades de Objeto — un emparejamiento criptográfico es el permiso, y su ausencia hace inexistente el camino — tal como se manifiesta en la admisión de nodos basada en máquinas de la plataforma."
status: active
bcsc_class: no-disclosure-implication
last_edited: 2026-08-22
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

El emparejamiento como permiso es el principio detrás de la [[machine-based-auth|admisión de nodos basada en máquinas]] de la plataforma. Un emparejamiento criptográfico entre dos nodos es el permiso; su ausencia hace estructuralmente imposible la conexión — no acceso denegado, sino la inexistencia de un camino para siquiera preguntar. No hay lista central de control de acceso consultada en tiempo de solicitud, ni búsqueda de roles en la ruta de conexión. **Un nodo que nunca completó la ceremonia de emparejamiento no puede ser instruido por nada, porque nada tiene forma de alcanzarlo.** Esa propiedad de seguridad se sostiene incluso si cualquier otra capa del sistema tiene un error. El modelo es el patrón formalmente probado de Capacidades de Objeto, desplegado en producción en Fuchsia OS, seL4 y WireGuard.

## El principio fundamental

En la mayoría de los sistemas de control de acceso, llega una solicitud, el sistema busca si el solicitante tiene permiso y permite o rechaza la solicitud. La búsqueda requiere una autoridad central.

El emparejamiento como permiso elimina la búsqueda. Dos nodos se comunican solo si ya se ha establecido un emparejamiento criptográfico entre ellos. Si no existe emparejamiento, no existe conexión y no se realiza solicitud. La pregunta "¿tiene este nodo permiso para alcanzar a aquel nodo?" tiene una respuesta estructural: comprobar si existe un emparejamiento.

Este es el modelo de Capacidades de Objeto — un patrón de seguridad formalmente probado descrito por Mark S. Miller en *Capability Myths Demolished* (2003).[^1] El axioma central: **la conectividad genera conectividad.** El objeto A puede enviar un mensaje a B solo si A posee una referencia a B. Sin la referencia, la conexión es estructuralmente imposible.

## Admisión de nodos mediante ceremonia de emparejamiento

La manifestación real de este principio en la plataforma es la admisión de nodos basada en máquinas. Un nodo nuevo completa una ceremonia de emparejamiento frente a un servicio de aprobación antes de poder unirse a la red — no se une primero para recibir permisos después. Hasta que esa ceremonia se completa y se aprueba, el nodo no tiene ningún camino hacia la red para solicitar nada.

Esta es una instancia concreta y más acotada del principio general, no su totalidad — la plataforma todavía no implementa control de acceso por capacidades en cada capa descrita por la literatura formal de Capacidades de Objeto. Lo que existe hoy es admisión de red condicionada por emparejamiento a nivel de nodo. La delegación de capacidades por recurso, en la extensión que implementan Fuchsia o seL4, es una dirección de diseño que este principio señala — no una afirmación sobre lo ya construido en todas partes.

## Por qué es más fuerte que las tablas de roles

Los sistemas basados en roles y listas de acceso comparten una vulnerabilidad estructural: el **problema del adjunto confuso**. Un intermediario de confianza puede ser engañado para realizar, en nombre de un solicitante de menor confianza, una acción que ese solicitante no podría hacer directamente. La vulnerabilidad está presente en cualquier sistema donde la autoridad se busca en una tabla en tiempo de solicitud, sin importar qué tan cuidadosamente se mantenga esa tabla.

En el modelo de Capacidades de Objeto, esta vulnerabilidad es un invariante arquitectónico, no un error del que hay que cuidarse. Un titular no puede usar lo que nunca se le entregó como referencia — no hay paso de búsqueda que un error pueda corromper.

## Implementaciones en producción

No es un modelo teórico. Está desplegado a escala en sistemas de producción ajenos a esta plataforma.

**Fuchsia OS** (Google) implementa control de acceso por capacidades a nivel del sistema operativo. Cada componente debe tener capacidades enrutadas explícitamente a través de la topología de componentes. Fuchsia se ejecuta en cada modelo de Google Nest Hub.[^2]

**El microkernel seL4** tiene una prueba formal verificada por máquina del confinamiento de capacidades: un proceso no puede acceder a un recurso para el que no se le otorgó explícitamente una capacidad. seL4 es el estándar de referencia para los modelos de seguridad formalmente verificados.[^3]

**WireGuard** implementa el mismo patrón en la capa de red. La tabla `AllowedIPs` es la tabla de capacidades — un nodo sin entrada para un destino no puede enviarle paquetes.

## Véase también

- [[machine-based-auth]] — el mecanismo real de ceremonia de emparejamiento que manifiesta este principio hoy
- [[personnel-permissions]] — el modelo de autorización por niveles de la plataforma para acceso de personal, distinto de este modelo de capacidades a nivel de nodo
- [[compounding-substrate]] — la arquitectura más amplia dentro de la cual opera este modelo de acceso
- [[three-ring-architecture]] — el modelo de límite de anillos que este principio refuerza a nivel de nodo
- [[pair-a-new-device]] — guía paso a paso: registrar un dispositivo mediante la ceremonia de emparejamiento

## Procedencia

Versión en español elaborada por project-language, adaptación estratégica — no es una traducción literal del artículo canónico en inglés.
