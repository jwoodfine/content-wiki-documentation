---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: os-totebox-service-pd-model
title: "Cómo los servicios service-* se convierten en dominios de protección seL4 en os-totebox"
short_description: "Explica cómo os-totebox asigna binarios de servicio Rust a dominios de protección seL4, cubriendo la pila de siete PDs, el modelo de confinamiento de capacidades, el orden de arranque y la vía de desarrollo de doble fondo."
audience: vendor-public
bcsc_class: current-fact
language: es
paired_with: os-totebox-service-pd-model.md
category: architecture
status: active
quality: complete
last_edited: 2026-06-23
---

# Cómo los servicios service-* se convierten en dominios de protección seL4 en os-totebox

os-totebox es el nivel de Bóveda de Datos WORM Soberana en la arquitectura de tres binarios. Se ejecuta como un sistema operativo de metal desnudo Tipo I sobre el micronúcleo seL4 — sin shell, sin proceso root, sin sistema init, sin gestor de paquetes. Cada servicio que maneja datos duraderos es un Dominio de Protección (PD) seL4: una unidad de aislamiento reforzada por hardware cuyo conjunto de capacidades queda fijo en el momento de la compilación y no puede ampliarse en tiempo de ejecución. Este artículo explica qué significa eso, por qué el diseño toma la forma que tiene y cómo dos herramientas planificadas — moonshot-sel4-vmm y moonshot-toolkit — convierten binarios de servicio Rust convencionales en un grafo de PD formalmente verificado.

## La cadena de herramientas que lo hace posible

Dos componentes están previstos para ensamblar la imagen de sistema de os-totebox (Fase H1, planificado):

**moonshot-sel4-vmm** es un crate Rust de aproximadamente 300 líneas que actúa como entorno de ejecución de PD. Proporciona la macro de punto de entrada `sel4_main!` que cada binario de servicio utiliza en lugar de `fn main()`, inicializa los canales IPC entre PDs en el arranque y registra el latido de cada PD con el watchdog. El crate tiene como objetivo la ABI de seL4 Microkit; no utiliza el crate externo rust-sel4. Esa dependencia externa fue evaluada y rechazada: el entorno de ejecución soberano es el único enlace Rust a seL4 en uso.

**moonshot-toolkit** es el constructor de imágenes de sistema (v0.3.1, 35 pruebas, Fase 1C completada). Lee una especificación de sistema en formato TOML — `examples/os-totebox.toml` — y genera un archivo `.system` que describe el grafo de PD completo: qué PDs existen, qué capacidades tiene cada uno, cómo están conectados los extremos IPC y qué regiones de memoria se asignan. El verificador de imágenes del toolkit comprueba, en tiempo de compilación, que la capacidad de dispositivo de bloque aparece exactamente una vez en la tabla de concesiones — en poder del PD service-fs y de ningún otro PD. Si esa afirmación falla, la compilación falla.

La especificación TOML es la declaración autoritativa única del grafo de PD. Un desarrollador que quiera entender qué servicio puede acceder a qué recurso lee `os-totebox.toml`, no un archivo de configuración en tiempo de ejecución ni un documento de política.

## Siete dominios de protección — por qué este número y no más

La pila de producción planificada (Fase H1+) ejecuta siete PDs. Cada PD corresponde directamente a un binario de servicio ya presente en el monorepo. Los valores de prioridad siguen la convención de seL4 Microkit: un número más alto significa que el planificador adelantará a un PD de menor prioridad para ejecutar este.

| PD | Crate | Prioridad | Cap. dispositivo de bloque |
|----|-------|-----------|---------------------------|
| watchdog-pd | system-security | 250 | No |
| service-fs PD | service-fs | 200 | Sí (única concesión) |
| network-pd | smoltcp VirtIO-net | 180 | No |
| service-content PD | service-content | 150 | No |
| service-people PD | service-people | 130 | No |
| service-slm PD | slm-doorman-server | 120 | No |
| service-extraction PD | service-extraction | 110 | No |

Siete es la pila segura mínimamente viable. Un número menor de PDs colapsaría los límites de aislamiento de los que depende el diseño: si service-slm y service-fs se ejecutaran en el mismo PD, la prueba formal de confinamiento no se sostendría, porque el PD combinado contendría tanto la superficie de inferencia como la capacidad del dispositivo de bloque. Un número mayor de PDs introduciría sobrecarga de IPC sin añadir un aislamiento más allá del que ya proporciona la división en siete.

La arquitectura no utiliza una malla de microservicios de propósito general. Cada PD tiene un rol específico, un conjunto de capacidades específico y una razón concreta para existir en su nivel de prioridad asignado.

## Secuencia de arranque — por qué este orden

La secuencia de arranque impone una cadena de dependencias estricta. watchdog-pd arranca primero porque debe poder adelantarse a cualquier otro PD en cualquier momento; si arrancara después de los servicios que monitoriza, existiría una ventana durante la cual un servicio fallido podría quedar sin detectar. El PD service-fs arranca segundo porque posee la capacidad del dispositivo de bloque — ningún servicio del Anillo 2 puede comenzar hasta que el ejecutor de WORM esté en buen estado. Cualquier intento de un servicio del Anillo 2 de escribir en almacenamiento duradero antes de que el PD service-fs esté listo sería rechazado en el límite IPC, no simplemente denegado por una comprobación de configuración.

Tras alcanzar un estado saludable el PD service-fs, arranca network-pd. Este posee la capacidad del dispositivo VirtIO-net y enruta todo el tráfico HTTP para los servicios del Anillo 2. Los servicios del Anillo 2 no pueden exponer una superficie HTTP hasta que network-pd esté activo, por lo que el orden es, de nuevo, estructural y no meramente orientativo.

Los cuatro servicios del Anillo 2 — service-content, service-people, service-slm y service-extraction — arrancan en orden de prioridad descendente. service-content (DataGraph, :9081) arranca antes que service-people porque este último depende del DataGraph para la resolución de entidades. service-slm (Doorman, :9080) arranca después de service-content porque Doorman utiliza el DataGraph para enrutar las solicitudes de inferencia. service-extraction (la canalización CORPUS) arranca en último lugar porque es un proceso en segundo plano que alimenta el DataGraph a lo largo del tiempo; no tiene ninguna dependencia crítica en cuanto a latencia que espere su señal de inicio.

El script de shell `os-totebox/scripts/start-stack.sh` implementa este orden para la vía de desarrollo (std/Linux, fondo de compatibilidad de la Fase H0). En la vía nativa seL4, el planificador de PD impone el mismo orden a nivel de capacidades — un PD no puede recibir una notificación de inicio de moonshot-sel4-vmm hasta que sus dependencias declaradas hayan enviado una señal de disponibilidad.

## Confinamiento de capacidades — qué cubre la prueba de seL4

La propiedad de seguridad crítica del diseño es geométrica: un PD service-slm comprometido no puede alcanzar el PD service-fs, independientemente del código que se ejecute dentro de service-slm. Esto no es una afirmación de política en tiempo de ejecución. El núcleo seL4 impone la seguridad de tipos de capacidades en cada invocación, y las pruebas Isabelle/HOL en vendor-sel4-kernel (BSD-2-Clause, seL4 Foundation, para AArch64 y RISC-V 64 a partir de Microkit 2.2.0, marzo de 2026) verifican formalmente que ninguna ruta de invocación elude este mecanismo.

La ruta de derivación es lo que importa. El PD service-slm no posee ninguna capacidad cuya cadena de derivación conduzca al extremo del dispositivo de bloque. network-pd enruta HTTP para service-slm pero no posee capacidad de dispositivo de bloque. service-extraction posee una capacidad de escritura circunscrita al canal del directorio de descarga del PD service-fs — no puede direccionar el dispositivo de bloque directamente. La única entidad del sistema que posee una capacidad de dispositivo de bloque es el PD service-fs, y esa capacidad se concede en `os-totebox.toml` y es verificada por moonshot-toolkit antes de ensamblar la imagen.

Una limitación es aplicable: la prueba de seL4 cubre el confinamiento de la ruta de invocación, pero no cubre los ataques por canal lateral a través de DRAM física compartida o líneas de caché compartidas. Un despliegue en hardware con zonas DMA físicas separadas por PD eliminaría ese riesgo residual. Esa configuración de hardware es un objetivo planificado para la Fase H2 y no forma parte del hito de arranque de desarrollo QEMU de la Fase H1.

## La vía de desarrollo de doble fondo

Dado que seL4 Microkit 2.2.0 tiene como objetivo únicamente AArch64 y RISC-V 64, el entorno de desarrollo x86_64 emplea una disposición paralela. La Fase H0 (completada) proporciona una imagen de referencia QCOW2 NetBSD precompilada que ejecuta los mismos servicios bajo un sistema operativo convencional. La Fase H1 (planificada) entrega el entorno de ejecución de PD seL4 en QEMU AArch64 (cortex-a53, VirtIO de bloque y red). Las dos vías no se fusionan: el fondo de compatibilidad NetBSD es un artefacto transitorio, y el fondo nativo seL4 es el objetivo de producción.

La decisión sobre el hardware AArch64 para el despliegue en metal desnudo de la Fase H2 — una instancia AArch64 en GCP o Firecracker x86_64 con KVM en hardware local — sigue siendo una decisión abierta que requiere dirección del administrador del sistema. Esa decisión condiciona el hito de la Fase H2, pero no el arranque de desarrollo QEMU de la Fase H1.

## Relación con la arquitectura de tres binarios

os-totebox es una de las superficies de un despliegue de tres binarios:

- **os-console** es la superficie de terminal de operador (TUI, cartuchos app-console-*). Transmite las solicitudes de inferencia a Doorman, pero no puede eludir los límites de capacidad de os-totebox.
- **os-totebox** es el nivel de persistencia de datos. Es la única superficie que posee capacidades de dispositivo de bloque WORM y firma los puntos de control del registro.
- **os-orchestration** es el nivel de agregación sin estado. Coordina la inferencia de GPU de Nivel B a través del agente Yo-Yo (:9180), pero nunca accede directamente al registro WORM.

La inferencia en os-totebox es exclusivamente de Nivel A — OLMo 7B local a través de Doorman (:9080). Los Niveles B (agente GPU) y C (API externa) se enrutan a través del crate app-orchestration-slm de os-orchestration. Este límite queda impuesto por el grafo de capacidades de PD: el PD service-slm en os-totebox posee una capacidad IPC únicamente hacia el motor OLMo local. No posee ninguna capacidad que alcance un extremo de red externo.

El registro WORM es el registro de auditoría autoritativo del sistema. Cada escritura que pasa por el PD service-fs es de solo anexado y con suma de comprobación. Ningún PD puede modificar una entrada existente del registro; el modelo de capacidades de seL4 lo hace estructuralmente imposible.

---

*Todo el lenguaje de la Fase H1 y posterior en este artículo describe funcionalidad planificada o prevista. La imagen de referencia NetBSD de la Fase H0 es el único artefacto desplegado en el momento de la redacción (2026-06-19).*
