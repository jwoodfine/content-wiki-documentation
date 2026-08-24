---
schema: foundry-doc-v1
title: "os-totebox — La bóveda soberana y host de servicios"
slug: totebox-os
category: systems
type: concept
content_type: topic
quality: complete
index_group: the-archive-layer
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-24
editor: pointsav-engineering
paired_with: totebox-os.md
short_description: "os-totebox es la capa de archivo de la familia PointSav — una bóveda aislada por entidad, que almacena registros como archivos planos inertes sin operación de borrado y los expone únicamente a través del Diodo bajo comando de os-console u os-orchestration. Su vía de producción aloja un invitado Linux bajo el micronúcleo seL4; existen otras formas de host para compatibilidad y desarrollo local."
cites: []
references:
  - id: 1
    text: "NIST. 'Directrices de Seguridad para Infraestructura de Almacenamiento.' SP 800-209, 2020."
    url: "https://doi.org/10.6028/NIST.SP.800-209"
---

`os-totebox` es la capa de archivo de la familia PointSav: una bóveda aislada por entidad. Almacena los registros, ejecuta los servicios que los procesan y no expone nada más. Una entidad es cualquier cosa que necesita su propio conjunto de libros — una persona, una corporación, una propiedad inmobiliaria, un proyecto, un hogar. Cada entidad tiene su propio `os-totebox`. Los Toteboxes no comparten archivos, no comparten usuarios y no pueden verse entre sí. Se comunican únicamente a través del [[diode-standard|Diodo]], y solo bajo comando de [[os-console|os-console]] u [[os-orchestration]]. Este artículo cubre los servicios internos, la disciplina WORM, la forma actual del host, una limitación de persistencia conocida, los niveles de cómputo y el diseño libremente transferible.

## Qué vive dentro

Cada `os-totebox` aloja un conjunto fijo de servicios:

| Servicio | Función |
|---|---|
| `service-fs` | Aplicador del ledger WORM; el único servicio que posee la capacidad de dispositivo de bloque que toca el disco sin procesar |
| `service-input` | Punto de entrada para ingesta, migración y calibración; las escrituras pasan por `service-fs` |
| `service-email` | Ingesta SMTP/IMAP; Maildir WORM; saneamiento de HTML y píxeles de rastreo |
| `service-people` | Libro mayor de identidades; la superficie F2; reclamaciones de entidad y el grafo Sovereign-ID |
| `service-content` | Lee cargas útiles, aplica el pipeline de síntesis editorial, genera resultados |
| `service-extraction` | Extracción de masa de entidades a través del archivo |
| `service-slm` | Modelo de lenguaje pequeño local; opera detrás del límite de auditoría Doorman |

Cada servicio de la tabla es una crate real y actualmente activa, no un marcador de posición. `service-fs` merece una advertencia específica: su propio servicio complementario de anclaje de integridad viene fallando desde el 2026-08-01, y la firma de checkpoints está deliberadamente sin configurar en esta línea base — el ledger está en ejecución, pero aún no completamente reforzado. Dos funciones que a veces se asumen como servicios separados de `os-totebox` — un archivo profundo de registros inmutables y un libro mayor financiero — no están respaldadas hoy por servicios dedicados. Lo más cercano que existe son vistas de interfaz sin identidad de servicio propia detrás.

## La disciplina WORM

`service-fs` escribe cargas útiles sin procesar directamente en almacenamiento de bloque de solo adición. No existe operación de borrado en el flujo de código. [^1] Un servicio comprometido no puede sobrescribir el historial porque el verbo no existe en la interfaz de almacenamiento. Esta es la capa de aplicación arquitectónica para la integridad de procesamiento y la [[worm-ledger-design|disciplina WORM]].

Cada registro institucional vive como un archivo plano inerte — Markdown, YAML o CSV — que no requiere ningún tiempo de ejecución propietario para leer décadas después. Un libro mayor `.yaml` o registro `.csv` puede ser leído por cualquier editor de texto, en cualquier hardware, en cualquier década. El costo de migración de datos tiende a cero: el operador siempre tiene la fuente en un formato que ningún software propietario puede bloquear. La [[worm-ledger-storage-architecture|arquitectura de almacenamiento WORM]] y la [[worm-ledger-architecture|arquitectura del ledger]] describen la implementación técnica.

## La forma del host

"`os-totebox`" nombra hoy tres cosas distintas, y distinguirlas importa para leer bien el resto de esta sección.

**La vía de producción es un invitado Linux aislado por seL4.** Un dominio de protección seL4 escrito a mano, sin dependencias externas — código real, de bajo nivel, en AArch64, no una simulación — ha arrancado, realizado IPC y conducido tráfico de red VirtIO genuino hasta alcanzar el servicio Doorman mediante un handshake TCP real. Por encima de ese hito de bajo nivel se ubica el diseño de hospedaje real: un VMM gestionado por Microkit (`libvmm`) arranca un invitado Linux ordinario, sin modificar, y el binario `os-totebox` se ejecuta dentro de él como el propio proceso init del invitado. La garantía de aislamiento la provee el límite de capacidades formalmente verificado de seL4 en la capa del hipervisor; los servicios dentro del invitado se ejecutan sin modificar. Un sistema de archivos raíz de invitado real y construido a propósito — Ubuntu 24.04 arm64 ("noble"), ensamblado mediante `debootstrap` — respalda esta vía; la base glibc es una elección deliberada, necesaria por la compatibilidad FFI que requiere el motor de grafo de conocimiento en C++ del que depende `service-content`. Esto produce una imagen de arranque real y completa (`loader.img`, de aproximadamente 113 MB) que ha sido verificada en vivo: un arranque genuino, seguido de un ciclo de inferencia de ida y vuelta completo a través del Doorman. La arquitectura objetivo completa es un mapa de capacidades de siete dominios — un `watchdog-pd` supervisor, y seis dominios de servicio que incluyen `service-fs-pd`, `network-pd`, `service-content-pd`, `service-people-pd`, `service-slm-pd` y `service-extraction-pd` — con un invariante aplicado en tiempo de compilación: solo `service-fs-pd` recibe jamás la capacidad de dispositivo de bloque. Todo otro dominio alcanza el almacenamiento durable únicamente a través de él.

**También existe una imagen NetBSD 10.1 como artefacto transicional**, no como el objetivo de producción. Es real y está construida — un pipeline genuino de herramientas cruzadas de NetBSD (`nbmakefs`, `nbinstallboot`) produce una imagen arrancable con un manifiesto de firma de binarios Veriexec — pero es un puente de compatibilidad en el camino hacia el invitado seL4 descrito arriba, no un destino paralelo.

**Un tercer significado, no relacionado, es el proceso único simple que hoy realmente ejecuta `os-totebox` localmente.** Su propio `main.rs` lanza `service-content` y el Doorman (`slm-doorman-server`) como dos hilos dentro de un proceso Linux ordinario — el enrutador y la lógica de negocio de cada servicio quedan intactos, este archivo solo los lanza juntos. Esto es lo que se despliega como la unidad systemd `local-totebox.service` en el entorno de desarrollo. Es una forma de empaquetado legítima y con intención de producción por derecho propio (el mismo patrón de un-binario-múltiples-roles que usan herramientas como Vault o Nomad), pero es algo distinto del invitado alojado por seL4 descrito arriba, y el nombre compartido es una fuente real de confusión que vale la pena nombrar con claridad.

## Una limitación conocida — persistencia de datos dentro del invitado seL4

El dispositivo de almacenamiento `virtio-blk` del invitado alojado por seL4 está conectado pero nunca es montado por la secuencia de inicio propia del invitado. En la práctica, esto significa que un reinicio de ese invitado hoy borra todos sus datos. Es una tensión directa con el propio planteamiento de "bóveda de datos soberana y persistente" de este artículo, y una limitación declarada aquí con claridad en lugar de dejarla implícita. Una brecha relacionada la agrava: la vía de apagado ordenado basada en QMP está documentada como no funcional, porque el invitado no declara ningún dispositivo ACPI o de botón de encendido para que QEMU lo señalice. De modo que un redespliegue hoy termina el invitado de forma abrupta, sin garantía de punto de control. Ninguna de las dos brechas afecta el propio ledger WORM de `service-fs`, que es un servicio separado a nivel de host (ver arriba); afectan los datos que el propio invitado alojado por seL4 acumula internamente. Ambas son elementos abiertos y conocidos, no defectos silenciados.

## Niveles de cómputo

`os-totebox` ajusta su comportamiento según el hardware disponible:

| Nivel | Perfil | Capacidad |
|---|---|---|
| Bóveda de Cero Cómputo | Nodo en la nube ~$7/mes, ≤1 GB RAM | Solo libro mayor WORM y enrutador criptográfico; delega el procesamiento pesado al Relé Yo-Yo |
| Relé Yo-Yo | Nodo en la nube elástico aprovisionado por el operador | Puente con estado hacia un nodo de cómputo temporal; ejecuta [[service-extraction|extracción]] en lote, luego se desmonta |
| Hierro Soberano | Estación de trabajo con ≥16 GB RAM o servidor bare-metal | Carga el [[service-slm|modelo de lenguaje pequeño]] local completo en RAM; sin egreso a la nube |

## Libremente transferible

Cada instancia de `os-totebox` está prevista para distribuirse como una única imagen de arranque firmada. El operador la toma y la mueve entre proveedores de nube, un servidor privado o hardware propio en sus instalaciones. No hay sistema operativo anfitrión subyacente que posea las claves. Esta portabilidad es un objetivo de diseño — la instancia en ejecución permanece como propiedad del operador en cualquier entorno — no una concesión de licencia distinta; `os-totebox` en sí tiene licencia FSL, una de las dos licencias separadas dentro de la familia de sistemas operativos (véase [[legal-and-ip-structure]]).

## Véase también

- [[os-family-overview]] — dónde encaja os-totebox en la familia de ocho SO
- [[os-console]] — el Libro Mayor de Comandos que se conecta a os-totebox y presenta su estado
- [[os-orchestration]] — el agregador de flota que consulta muchos Toteboxes a la vez
- [[diode-standard]] — el protocolo unidireccional a través del cual se comunica el Totebox
- [[sel4-microkernel-substrate]] — el núcleo que sustenta las garantías de aislamiento de os-totebox
- [[machine-based-auth]] — cómo el emparejamiento rige el acceso a un Totebox
- [[worm-ledger-design]] — la disciplina de almacenamiento de solo adición aplicada por os-totebox
