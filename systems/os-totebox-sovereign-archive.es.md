---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: os-totebox-sovereign-archive
title: "os-totebox: La Bóveda Soberana de Datos WORM"
short_description: "os-totebox está diseñado para convertirse en un sistema operativo de Tipo I sobre hardware físico, construido sobre el micronúcleo seL4 formalmente verificado — el estado final previsto, no el software que se ejecuta hoy."
audience: vendor-public
bcsc_class: forward-looking
language: es
language_protocol: PROSE-TOPIC
index_group: the-archive-layer
paired_with: os-totebox-sovereign-archive.md
category: systems
status: active
quality: complete
last_edited: 2026-08-24
---

**Estado (2026-08-06):** la imagen seL4 Microkit descrita en este artículo ha pasado de
planificada a verificada en vivo. Se ha confirmado un arranque real de la imagen, con
ciclos completos de inferencia confirmados y funcionando — el diseño de grafo de
capacidades y Dominios de Protección descrito a continuación es trabajo de ingeniería
real y actual, no simplemente trabajo previsto ni un diseño en papel. Este es un hito de
arranque verificado específicamente en la vía seL4; no describe todavía el despliegue
general de os-totebox, que sigue siendo el proceso convencional de Rust/tokio
(`service-content` + `service-slm`/Doorman ejecutándose como un único proceso
desplegable) descrito en el registro de ingeniería de la plataforma. `bcsc_class` se
mantiene como `forward-looking`: la pila de producción completa, la aplicación del grafo
de capacidades a escala y las garantías de persistencia que argumenta este artículo aún
no son reales — véanse las Limitaciones conocidas, a continuación, antes de tratar esto
como una bóveda soberana persistente ya desplegada. Cada otra afirmación en tiempo
presente de este artículo debe leerse como el diseño previsto, confirmado hoy solo en la
capa de arranque e inferencia descrita aquí. **Nota**: el resto del cuerpo de este
artículo en español aún no ha recibido el mismo ajuste de tiempo verbal sección por
sección que la versión en inglés — pendiente, no silenciosamente omitido.

## Limitaciones conocidas (2026-08-06)

Estas mismas limitaciones —almacenamiento aún no persistente, apagado ordenado roto, nada
que ancle o firme el registro todavía— son información determinante para quien evalúe el
diseño hoy. En lugar de repetirlas aquí, véase la sección propia de [[totebox-os]]
**"Una limitación conocida — persistencia de datos dentro del invitado seL4"** para la
versión canónica y de fuente única de este hecho.

Toda organización que depende de una plataforma de terceros para almacenar sus registros está asumiendo una apuesta implícita: que el proveedor de esa plataforma seguirá siendo solvente, accesible y libre de fallas de seguridad durante todo el tiempo que esos registros tengan relevancia. [[totebox-os]] está diseñado para los operadores que han decidido que esa apuesta es inaceptable.

## Qué está diseñado para ser os-totebox

El estado final previsto de os-totebox es un sistema operativo de Tipo I sobre hardware físico, lo que significa que se ejecutaría directamente sobre el hardware sin ningún sistema operativo de propósito general por debajo, sin terminal Linux, sin gestor de paquetes, sin proceso raíz y sin sistema de inicialización. El software previsto para ese hardware es una imagen seL4 Microkit: un [[sel4-microkernel-substrate|micronúcleo]] formalmente verificado con un conjunto de servicios compilados de forma estática y sin ninguna vía de modificación en tiempo de ejecución.

La característica definitoria de la plataforma es su modelo de almacenamiento. os-totebox opera como una [[worm-ledger-architecture|bóveda WORM]] — escritura única, lectura múltiple (Write Once, Read Many). Los registros escritos en el sistema no pueden ser alterados ni eliminados a través de ninguna vía de software. Esto no es una política aplicada por una lista de control de acceso ni por un indicador de permiso que un administrador pudiera anular; es una propiedad del grafo de capacidades que rige cada servicio de la máquina.

## Geometría de Capacidades en Hardware de Servidor

seL4 es un micronúcleo desarrollado y formalmente verificado por el Data61 de la CSIRO. La verificación demuestra matemáticamente que el modelo de control de acceso del núcleo se aplica sin excepción. En os-totebox, esta propiedad se extiende a la arquitectura de servicios.

Cada servicio en os-totebox se ejecuta dentro de un Dominio de Protección seL4 — un entorno de ejecución aislado que solo posee las capacidades que el diseño del sistema le otorga explícitamente. El DAG de capacidades (grafo acíclico dirigido) que define estas concesiones ha sido formalmente demostrado. No existe ningún camino en el grafo desde un servicio que procesa entradas externas hasta el servicio que posee la capacidad de almacenamiento.

Esto tiene consecuencias concretas en un escenario de falla. Si [[service-slm]] — el componente que gestiona la inferencia del modelo de lenguaje y, por tanto, el componente más directamente expuesto a entradas adversariales — quedara completamente comprometido, el código comprometido se encontraría acotado por su Dominio de Protección. No posee ninguna capacidad para alcanzar service-fs. No puede leer el dispositivo de bloques WORM. No puede escribir en él. El punto de apoyo del atacante queda geométricamente aislado del almacén de datos. Esta es la propiedad que la plataforma denomina [[capability-geometry|Geometría de Capacidades]].

## La Arquitectura de Anillos

os-totebox organiza sus servicios en dos [[three-ring-architecture|anillos concéntricos]] según su proximidad al almacenamiento.

**El Anillo 1** comprende los servicios que interactúan directamente con los datos duraderos y con la E/S externa: [[service-fs|service-fs]], service-input, service-extraction y service-egress. service-fs posee en exclusividad la capacidad sobre el dispositivo de bloques WORM — es el único Dominio de Protección de la máquina que puede realizar operaciones de almacenamiento. Ningún otro servicio puede acceder directamente al dispositivo de bloques, independientemente de su estado de ejecución.

**El Anillo 2** comprende los servicios que procesan, clasifican y razonan sobre los datos: service-content, service-people, service-email y service-slm. Estos servicios se comunican con el Anillo 1 a través de un protocolo de comunicación entre dominios definido y acotado. Pueden solicitar a service-fs que escriba un registro; no pueden poseer por sí mismos la capacidad para hacerlo.

Esta separación no es una preferencia arquitectónica que futuros desarrolladores puedan relajar. El grafo de capacidades se compila en la imagen seL4 en el momento de la construcción. Modificar la estructura de capacidades requiere reconstruir y volver a desplegar la imagen — un paso que produce un artefacto nuevo y auditable en lugar de un cambio silencioso en tiempo de ejecución.

## El Archivo de Datos Soberano

El modelo operativo que habilita os-totebox es aquel en el que el hardware del operador y el grafo de capacidades del operador constituyen el sistema completo. No existe ninguna dependencia de la nube en la ruta de almacenamiento. Los registros ingestados se escriben en un dispositivo físico bajo el control físico del operador y no pueden abandonar la máquina a través de ninguna vía de software que el DAG de capacidades no autorice.

Esto tiene implicaciones prácticas que van más allá de la seguridad. Una organización cuyos registros existen únicamente en su propio hardware no está sujeta a las políticas de residencia de datos de un proveedor, a la ventana de interrupciones de un proveedor de nube ni a un cambio en los términos de servicio de una plataforma. La pista de auditoría es local, el calendario de retención lo fija el operador y el dispositivo físico puede ser dado de baja según los procedimientos del propio operador.

Para los sectores en los que los registros tienen peso legal — libros de actas corporativas, expedientes de bienes inmuebles, libros de contabilidad financiera, correspondencia regulada — la inmutabilidad de una bóveda WORM no es simplemente una característica técnica. Es la evidencia de que un registro existió en un estado determinado en un momento determinado y que no ha sido alterado desde entonces.

## Superficie Operativa para Organizaciones Pequeñas y Medianas

La verificación formal de nivel empresarial y la inmutabilidad con raíz en el hardware han requerido históricamente equipos de infraestructura de seguridad dedicados para su despliegue y operación. os-totebox está diseñado para proporcionar esas propiedades sobre hardware de uso general con una superficie operativa que no presupone una organización especializada en seguridad.

La ausencia de una terminal no es un inconveniente; es una característica. Un sistema sin terminal no tiene superficie de ataque interactiva. Un sistema sin proceso raíz no tiene una vía de escalada de privilegios. Un sistema sin gestor de paquetes no puede actualizarse de maneras que introduzcan código no auditado. La imagen seL4 que se ejecuta en el hardware es el inventario de software completo y auditable de la máquina.

Una organización que despliega os-totebox no está confiando en la diligencia de un administrador para hacer cumplir las políticas de protección de datos. Está confiando en un grafo de capacidades formalmente demostrado. La distinción es la diferencia entre una política y una prueba.

## Relación con la Plataforma en Su Conjunto

os-totebox es uno de los tres sistemas operativos de hardware físico de propósito específico en la arquitectura de la plataforma. Opera junto con os-console, que proporciona la interfaz de operador nativa de teclado, y [[os-orchestration]], que gestiona el entorno de ejecución del [[totebox-archive|Archivo Totebox]]. Los tres sistemas no comparten ninguna ruta de código de núcleo y se comunican únicamente a través de canales de red definidos.

El patrón de despliegue previsto es hardware propiedad del operador con una única interfaz de red física. La bóveda WORM no es un servicio accesible desde internet público; es un nodo en un segmento de red privado cuyas rutas de entrada están controladas por la misma disciplina de capacidades que rige su almacenamiento.

**La imagen seL4 Microkit para os-totebox ha pasado de planificada a verificada en vivo: se ha confirmado un arranque real de la imagen, con ciclos completos de inferencia confirmados y funcionando.** Todo lo anterior describe el diseño final previsto; el hito de arranque e inferencia es un avance real en esa vía, pero las brechas de persistencia, apagado ordenado y anclaje del registro descritas en Limitaciones conocidas siguen abiertas — véase esa sección antes de tratar esto como una bóveda persistente lista para producción. El estado de implementación se registra en el registro de ingeniería de la plataforma — véase la propia descripción del crate `os-totebox` para más detalle sobre el despliegue actual (service-content + service-slm ejecutándose como un único proceso convencional, en el despliegue general).
