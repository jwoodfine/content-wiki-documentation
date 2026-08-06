---
artifact: topic
schema: foundry-doc-v1
type: topic
content_type: topic
slug: scaling-coordinated-development-totebox-archives
aliases:
  - scaling-coordinated-development-sovereign-archives
title: "Escalar el desarrollo coordinado en múltiples Totebox Archives"
category: systems
index_group: the-archive-layer
short_description: "Cuellos de botella de coordinación más allá de veinte archivos — serialización de publicaciones, latencia de mensajes, carga del operador y aislamiento por proceso."
status: active
language_protocol: TOPIC
last_edited: 2026-08-03
editor: pointsav-engineering
---

El propio flujo de desarrollo multi-archivo del proveedor está diseñado para crecer. Este artículo describe los desafíos de coordinación que aparecen a medida que aumenta el número de [[totebox-archive|Totebox Archives]], los mecanismos introducidos para abordarlos y la trayectoria prevista hacia el aislamiento de procesos por archivo.

## El desafío de coordinación

Cuando un número reducido de archivos comparte un coordinador central, la carga de trabajo del coordinador es manejable: un operador humano puede retransmitir mensajes entre archivos, revisar las solicitudes de publicación una a una y mantener la cola manualmente. A medida que el número de archivos supera los diez o veinte, emergen tres cuellos de botella:

1. **Serialización de la publicación.** Cada archivo que quiere que su código figure en el historial canónico debe esperar a que el coordinador ejecute la secuencia de publicación. Si el coordinador está ocupado con otro archivo —o simplemente no está en ejecución— la cola crece.
2. **Latencia de retransmisión de mensajes.** Los archivos se comunican mediante un sistema de mensajes basado en ficheros. Sin automatización, los mensajes permanecen en la cola de salida de un archivo hasta que el operador del coordinador los entrega manualmente al destino. Con 21 archivos, esto se convierte en una tarea manual recurrente.
3. **Carga cognitiva del operador.** El operador del coordinador debe hacer un seguimiento simultáneo del estado de todos los archivos: solicitudes de publicación pendientes, mensajes sin entregar, tareas bloqueadas y alertas operativas. A escala, esto no es sostenible.

## La ruta de publicación descentralizada

La primera mitigación es un modelo de elegibilidad por niveles, ya real hoy para algunos archivos, no solo previsto. Los archivos que han demostrado madurez operativa —superando de forma consistente sus suites de compilación y pruebas, manteniendo historiales limpios y operando sin intervenciones frecuentes— pueden obtener un nivel de autoservicio: el archivo empuja su propia rama a sus espejos de preparación y añade un registro a un fichero de cola de promoción, que notifica a la bandeja de entrada de la sesión coordinadora en lugar de escribir directamente en el canónico. Véase [[five-stage-supply-chain]] para el mecanismo completo de esa ruta de promoción, incluidas las verificaciones que una solicitud de promoción debe superar en cualquier caso.

Esto no elimina el papel del coordinador; delega la publicación rutinaria de bajo riesgo a los archivos que se han ganado esa confianza, reservando la atención del coordinador para decisiones de mayor importancia. Los archivos sin elegibilidad de autoservicio envían una solicitud y esperan a que el coordinador ejecute la publicación en su nombre.

## El sustrato de mensajería

Los mensajes entre archivos se escriben en un formato de fichero estructurado y rastreado por git —uno por archivo, de adición al principio únicamente, con encabezados de esquema validado. Este formato es auditable, permite diferencias y es recuperable desde el historial git del archivo.

Un servicio de retransmisión *(previsto/en desarrollo)* automatizará la entrega de mensajes: con una cadencia regular, analizará la cola de mensajes salientes de cada archivo, leerá el destino declarado y escribirá cada mensaje en la cola de mensajes entrantes del archivo destino utilizando la ruta de escritura canónica. El paso de retransmisión manual del operador del coordinador será sustituido por un temporizador en segundo plano.

### Por qué no un intermediario de mensajes

Se evaluaron alternativas como NATS o RabbitMQ y se descartaron para este caso de uso:

- **Desajuste en la tasa de mensajes.** Los mensajes entre archivos llegan en horas y días, no en milisegundos. Un intermediario optimizado para mensajería de alta capacidad y baja latencia introduce complejidad de infraestructura que la tasa de mensajes real no justifica.
- **Duplicidad de fuente de verdad.** El formato de mensajes basado en ficheros ya está rastreado y versionado por git. Introducir un intermediario crearía un segundo registro autoritativo del estado de los mensajes, sin una regla clara sobre cuál respetar en caso de divergencia.
- **Superficie de dependencia.** Un intermediario es un servicio adicional de larga ejecución que debe instalarse, monitorizarse y mantenerse coherente con el registro git. El sistema basado en ficheros funciona sin ningún tiempo de ejecución externo.

El servicio de retransmisión añade automatización sin añadir un intermediario: lee y escribe el mismo formato de fichero que ya existe.

## Aislamiento por operador

El modelo actual ejecuta todos los Totebox Archives bajo un usuario del sistema compartido. Cada archivo puede leer y escribir los ficheros de cualquier otro archivo, limitado únicamente por los permisos de grupo del sistema de ficheros.

Una trayectoria prevista *(previsto/en desarrollo)* asigna cada Totebox Archive a un operador específico (usuario de Linux). Ese operador es el propietario del sistema de ficheros del archivo y el titular exclusivo de su identidad de commit. Los archivos cuyo propietario es un operador diferente no pueden escribir en los ficheros de estado del otro sin una escalada explícita. Esto refleja la topología de producción objetivo, en la que cada archivo se ejecuta como una instancia `os-totebox` dedicada con pleno aislamiento de procesos.

La transición del entorno de usuario compartido al aislamiento por operador es incremental. El primer paso consiste en aprovisionar material criptográfico para cada operador, de modo que pueda realizar commits desde su propia sesión de terminal. Los pasos siguientes asignan la propiedad del directorio del archivo y restringen el acceso al sistema de ficheros entre archivos.

## Trayectoria

La instalación actual opera 21 archivos en un entorno de usuario compartido en un único host. Es un prototipo funcional de la arquitectura objetivo — no, como implicaba una versión anterior de este artículo, un despliegue del producto `app-orchestration-command`. `app-orchestration-command` es real y sustancial en el canónico, pero su función real es el emparejamiento de archivos, la visibilidad de flota, los niveles de personal/permisos y el bróker de GPU (véase [[pairing-as-permission]] y [[personnel-permissions]]) — no desempeña ningún papel en la publicación canónica. La mecánica de coordinación y publicación que describe este artículo pertenece a las herramientas de promoción propias del proveedor, detalladas en [[five-stage-supply-chain]].

La topología de producción prevista asigna cada archivo a una instancia `os-totebox` dedicada —un nodo de cómputo monofuncional que ejecuta los servicios del archivo, con su propio usuario operador, identidad de commit y límite de red.

Esta topología es objeto de trabajo arquitectónico en curso. La documentación actual sobre los modelos `os-orchestration` y `os-totebox` se mantiene de forma independiente; consulte los temas relacionados a continuación.

## Temas relacionados

- [[five-stage-supply-chain]] — la canalización de publicación real: herramientas de promoción, elegibilidad de autoservicio y las verificaciones que un commit debe superar antes de alcanzar el canónico
- [[pairing-as-permission]] — el modelo de emparejamiento criptográfico que `app-orchestration-command` implementa realmente
- [[os-orchestration|arquitectura de os-orchestration]] — la plataforma anfitriona del coordinador
- [[os-totebox-sovereign-archive|modelo de archivo os-totebox]] — el sistema operativo por archivo al que apunta esta trayectoria
