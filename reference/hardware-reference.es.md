---
schema: foundry-doc-v1
title: "Referencia de Hardware"
slug: hardware-reference
category: reference
type: reference
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: hardware-reference.md
---

La referencia de hardware PointSav define los perfiles de dispositivos y las configuraciones de infraestructura contra las que se prueba y despliega el sustrato. Tres niveles cubren la estación de trabajo del desarrollador, el dispositivo de flota y el anfitrión de compilación heredado; tres patrones de infraestructura van desde instalaciones locales hasta metal desnudo arrendado y nube. La fragmentación de hardware es el principal enemigo de la estabilidad del sistema operativo; la lista de referencia es deliberadamente reducida, seleccionando por compatibilidad de controladores bajo una base FreeBSD o seL4 reforzada. Este artículo cubre la lista de dispositivos de referencia, los requisitos arquitectónicos de CPU, los patrones de despliegue de infraestructura y la restricción de nodo base de Nivel 1.

## Perfiles de hardware de referencia

[[os-workplace|os-workplace]] y [[console-os|os-console]] apuntan a un conjunto deliberado de dispositivos:

| Nivel | Dispositivo | Justificación |
|---|---|---|
| Insignia | Dell XPS 13 / 14 (Developer Edition) | Dell distribuye un perfil Linux oficial; los controladores de WiFi Intel y gráficos maduran rápidamente en FreeBSD |
| Flota | HP ProBook 400 series (445 / 450) | Chipsets WiFi de grado empresarial con compatibilidad BSD; adecuados para despliegues de clientes PyME más grandes |
| Anfitrión de compilación (legado) | iMac 12.1 (Sandy Bridge, 2011) | La máquina de compilación original hasta principios de 2026; posteriormente reemplazada para el trabajo de desarrollo de `service-content` |

El criterio de selección es la disponibilidad de controladores, no la preferencia de marca. Los portátiles de consumo con módulos WiFi propietarios que carecen de controladores compatibles con BSD quedan excluidos por esa sola razón.

## Requisitos arquitectónicos de CPU

Tres restricciones rigen qué hardware puede ejecutar el sustrato PointSav:

| Restricción | Requisito |
|---|---|
| Conjunto de instrucciones | x86_64 de generación Haswell o posterior |
| Extensión requerida | `fsgsbase` — utilizada por las rutas optimizadas del micronúcleo seL4 |
| Paginación de memoria | 1 GB de Huge Pages habilitado (flag de CPU `+pdpe1gb`) |

Las CPUs anteriores a Haswell — Nehalem y anteriores — carecen de `fsgsbase`. Intentar ejecutar el núcleo en hardware pre-Haswell provoca un `UserException` en la primera impresión del núcleo. La restricción es un requisito funcional, no una preferencia de rendimiento.

## Patrones de despliegue de infraestructura

[[infrastructure-os|os-infrastructure]] se despliega en tres patrones, cada uno con un perfil de confianza distinto:

| Patrón | Hardware | Perfil de confianza |
|---|---|---|
| En instalaciones propias | Servidor en la oficina del cliente (Dell PowerEdge T160 torre o R760 rack son configuraciones de referencia) | Máxima confianza — el operador es propietario del metal |
| Arrendado | Metal desnudo colocado en un centro de datos externo | Confianza híbrida — el proceso de arranque no puede verificarse físicamente |
| Nube | VMs de hiperproveedores (Google Cloud como base canónica) | Mínima confianza — usado para relay perimetral sin estado |

## Investigación de proveedores de metal desnudo — región de Vancouver

La investigación de archivo de 2026 evaluó el mercado de Vancouver, Columbia Británica, para opciones de metal desnudo más cercanas a la región de despliegue principal del cliente. La tabla registra los hallazgos de la investigación y no constituye una recomendación comercial:

| Proveedor | Ubicación física | Latencia a Vancouver | Características |
|---|---|---|---|
| Atal Networks | Vancouver, BC | <1–2 ms | Metal desnudo local verdadero con IPMI/KVM; no gestionado; interconexión directa con ISPs regionales |
| GTHost | Vancouver, BC | <1–2 ms | Aprovisionamiento de activación instantánea; orientado a la automatización |
| Vultr | Seattle, WA | ~3–10 ms | Metal desnudo con API; facturación por horas |
| OVHcloud | Montreal, QC | ~60–80 ms | Menor costo; alta latencia transcontinental |

Se prefiere una latencia inferior a 2 milisegundos para los Totebox de producción que sirven a operadores locales. El metal desnudo en la región de Seattle es aceptable para funciones perimetrales sin estado.

## El nodo base de Nivel 1

El objetivo de nube más probado es un único perfil canónico: Google Cloud `e2-micro` a aproximadamente siete dólares estadounidenses al mes. Este perfil ancla la base de Nivel 1 de la Matriz de Cómputo:

| Propiedad | Valor |
|---|---|
| Costo aproximado | ~$7 USD / mes (base 2026) |
| RAM | ≤1 GB |
| Virtualización de hardware | Deshabilitada por el proveedor — VMs anidadas no disponibles |
| Almacenamiento | Disco persistente |
| Función | [[worm-ledger-design|Libro mayor WORM]] + enrutador criptográfico; delega la inferencia SLM al relay |

La restricción arquitectónica es que un Totebox completo debe poder operar con este perfil. El sistema debe ser funcional para un operador que no puede aprovisionar recursos premium de hiperproveedores.

## Restricciones de virtualización de hardware

La base `e2-micro` deshabilita la virtualización de hardware, lo que impide ejecutar Micro-VMs en ese nivel. La respuesta arquitectónica es doble:

1. El sustrato utiliza unikernels verdaderos (Nanos, Unikraft) en lugar de Micro-VMs cuando el proveedor de nube prohíbe la virtualización anidada.
2. Los despliegues de nivel superior que requieren Micro-VMs se ejecutan en metal desnudo o instancias de nube con capacidad KVM.

## Véase también

- [[os-workplace]] — el sistema operativo de estación de trabajo que ejecuta los perfiles de dispositivos de referencia
- [[infrastructure-os]] — el sistema operativo de infraestructura que cubre los tres patrones de despliegue
- [[worm-ledger-design]] — el libro mayor WORM desplegado en el nodo base de Nivel 1
- [[sel4-microkernel-substrate]] — el micronúcleo seL4 que aplica las restricciones arquitectónicas de CPU
