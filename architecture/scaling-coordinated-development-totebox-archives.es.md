---
schema: foundry-doc-v1
content_type: topic
title: "Escalar el desarrollo coordinado en múltiples Totebox Archives"
slug: scaling-coordinated-development-totebox-archives
short_description: "La topología de app-orchestration-command está diseñada para crecer. Este artículo describe los desafíos de coordinación a medida que aumenta el número de Totebox Archives, los mecanismos introducidos para abordarlos y la trayectoria prevista hacia el aislamiento de procesos por archivo."
category: architecture
type: reference
quality: complete
status: stable
audience: public
bcsc_class: public-disclosure-safe
language_protocol: TRANSLATE-ES
last_edited: 2026-06-23
editor: pointsav-engineering
paired_with: scaling-coordinated-development-totebox-archives.md
cites: []
---

La topología de `app-orchestration-command` está diseñada para crecer. Este artículo describe los desafíos de coordinación que aparecen a medida que aumenta el número de Totebox Archives, los mecanismos introducidos para abordarlos y la trayectoria prevista hacia el aislamiento de procesos por archivo.

## El desafío de coordinación

Cuando un número reducido de archivos comparte un coordinador central, la carga de trabajo del coordinador es manejable: un operador humano puede retransmitir mensajes entre archivos, revisar las solicitudes de publicación una a una y mantener la cola manualmente. A medida que el número de archivos supera los diez o veinte, emergen tres cuellos de botella:

1. **Serialización de la publicación.** Cada archivo que quiere que su código figure en el historial canónico debe esperar a que el coordinador ejecute la secuencia de publicación. Si el coordinador está ocupado con otro archivo —o simplemente no está en ejecución— la cola crece.
2. **Latencia de retransmisión de mensajes.** Los archivos se comunican mediante un sistema de mensajes basado en ficheros. Sin automatización, los mensajes permanecen en la cola de salida de un archivo hasta que el operador del coordinador los entrega manualmente al destino. Con 21 archivos, esto se convierte en una tarea manual recurrente.
3. **Carga cognitiva del operador.** El operador del coordinador debe hacer un seguimiento simultáneo del estado de todos los archivos: solicitudes de publicación pendientes, mensajes sin entregar, tareas bloqueadas y alertas operativas. A escala, esto no es sostenible.

## La ruta de publicación descentralizada

La primera mitigación es un modelo de elegibilidad por niveles. Los archivos que han demostrado madurez operativa —superando de forma consistente sus suites de compilación y pruebas, manteniendo historiales limpios y operando sin intervenciones frecuentes— pueden obtener un nivel de autoservicio más alto.

En el nivel de autoservicio más alto *(previsto/en desarrollo)*, un archivo puede iniciar la publicación canónica directamente, sin esperar a que actúe el operador del coordinador. El requisito previo es que la clave de administrador sea accesible desde el entorno del archivo. El coordinador valida el resultado a posteriori y registra el evento de publicación en el registro de auditoría.

Esto no elimina el papel del coordinador; delega la publicación rutinaria de bajo riesgo a los archivos que se han ganado esa confianza, reservando la atención del coordinador para decisiones de mayor importancia.

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

La instalación actual de `app-orchestration-command` opera 21 archivos en un entorno de usuario compartido en un único host `os-orchestration`. Es un prototipo funcional de la arquitectura objetivo.

La topología de producción prevista asigna cada archivo a una instancia `os-totebox` dedicada —un nodo de cómputo monofuncional que ejecuta los servicios del archivo, con su propio usuario operador, identidad de commit y límite de red. `app-orchestration-command` en `os-orchestration` sigue siendo el coordinador de publicación y la autoridad de auditoría; no desaparece, pero su papel pasa a ser de coordinación más que de ejecución.

Esta topología es objeto de trabajo arquitectónico en curso. La documentación actual sobre los modelos `os-orchestration` y `os-totebox` se mantiene de forma independiente; consulte los temas relacionados a continuación.

## Temas relacionados

- [[app-orchestration-command-publication-flow]] — el flujo de publicación y el modelo de elegibilidad
- [[app-orchestration-command-branch-model]] — aislamiento y filtrado
- *Arquitectura de os-orchestration* — mantenida en la serie TOPIC de project-data
- *Modelo de archivo os-totebox* — mantenida en la serie TOPIC de project-data

---

*Woodfine Capital Projects™, MCorp™, PointSav Digital Systems™, Totebox Orchestration™ y Totebox Archive™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos propietarios.*
