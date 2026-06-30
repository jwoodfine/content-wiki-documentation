---
schema: foundry-doc-v1
title: "os-totebox — La bóveda soberana y host de servicios"
slug: totebox-os
category: systems
type: concept
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: totebox-os.md
short_description: "os-totebox es la capa de archivo de la familia PointSav — una bóveda aislada a nivel de núcleo por entidad, que almacena registros como archivos planos inertes sin operación de borrado y los expone únicamente a través del Diodo bajo comando de os-console u os-orchestration."
cites: []
references:
  - id: 1
    text: "NIST. 'Directrices de Seguridad para Infraestructura de Almacenamiento.' SP 800-209, 2020."
    url: "https://doi.org/10.6028/NIST.SP.800-209"
  - id: 2
    text: "Madhavapeddy, A. et al. 'Unikernels: Library Operating Systems for the Cloud.' ACM ASPLOS, 2013."
    url: "https://dl.acm.org/doi/10.1145/2451116.2451167"
---

`os-totebox` es la capa de archivo de la familia PointSav: una bóveda aislada a nivel de núcleo por entidad. Almacena los registros, ejecuta los servicios que los procesan y no expone nada más. Una entidad es cualquier cosa que necesita su propio conjunto de libros — una persona, una corporación, una propiedad inmobiliaria, un proyecto, un hogar. Cada entidad tiene su propio `os-totebox`. Los Toteboxes no comparten archivos, no comparten usuarios y no pueden verse entre sí. Se comunican únicamente a través del [[diode-standard|Diodo]], y solo bajo comando de [[console-os|os-console]] u [[os-orchestration]]. Este artículo cubre los servicios internos, la disciplina WORM, la evolución de la forma del host, los niveles de cómputo y el diseño libremente transferible.

## Qué vive dentro

Cada `os-totebox` aloja un conjunto fijo de servicios:

| Servicio | Función |
|---|---|
| `service-email` | Ingesta SMTP/IMAP; Maildir WORM; saneamiento de HTML y píxeles de rastreo |
| `service-people` | Libro mayor de identidades; la superficie F2; reclamaciones de entidad y el grafo Sovereign-ID |
| `service-content` | Lee cargas útiles, aplica el pipeline de síntesis editorial, genera resultados |
| `service-extraction` | Extracción de masa de entidades a través del archivo |
| `service-slm` | Modelo de lenguaje pequeño local; opera detrás del límite de auditoría Doorman |
| `service-minutebook` | Archivo de registros profundos — PDFs inmutables, DOCX, XLSX, con sumas de verificación criptográficas |
| `service-bookkeeper` | Libro mayor financiero |
| `service-fs` (previsto) | Servicio de sistema de archivos unikernel — el único servicio que toca el disco sin procesar |
| `service-audit` (previsto) | Libro mayor de solo adición a nivel de micronúcleo |
| `service-resolution` (previsto) | Empaquetador de resolución de activos — el paracaídas auto-ejecutable ante fallo del proveedor |

## La disciplina WORM

`os-totebox` escribe cargas útiles sin procesar directamente en almacenamiento de bloque de solo adición. No existe operación de borrado en el flujo de código. [^1] Un servicio comprometido no puede sobrescribir el historial porque el verbo no existe en la interfaz de almacenamiento. Esta es la capa de aplicación arquitectónica para la integridad de procesamiento y la [[worm-ledger-design|disciplina WORM]].

Cada registro institucional vive como un archivo plano inerte — Markdown, YAML o CSV — que no requiere ningún tiempo de ejecución propietario para leer décadas después. Un libro mayor `.yaml` o registro `.csv` puede ser leído por cualquier editor de texto, en cualquier hardware, en cualquier década. El costo de migración de datos tiende a cero: el operador siempre tiene la fuente en un formato que ningún software propietario puede bloquear. La [[worm-ledger-storage-architecture|arquitectura de almacenamiento WORM]] y la [[worm-ledger-architecture|arquitectura del ledger]] describen la implementación técnica.

## La forma del host

`os-totebox` está diseñado para evolucionar a través de cuatro fases a medida que el sustrato seL4 madura:

| Fase | Forma | Caso de uso |
|---|---|---|
| 1 | Jaula LXC / FreeBSD | Desarrollo activo; itera rápidamente |
| 2 | Instancia FreeBSD reforzada | Primeros despliegues para clientes (previsto) |
| 3 | Monolito seL4 + Rust | Endurecimiento para producción (previsto) |
| 4 | Unikernel — binario único, ~15 MB, arranque <50 ms | Estado final (previsto) |

El objetivo unikernel es la meta de diseño. [^2] El estado final no tiene SSH, ni shell, ni Bash, ni intérprete Python — solo un binario compilado fusionado a los controladores de hardware. Un operador recompila el código fuente del proveedor en el monorepo y reinicia el nodo en la nube con la nueva imagen; no hay shell al que conectarse.

## Niveles de cómputo

`os-totebox` ajusta su comportamiento según el hardware disponible:

| Nivel | Perfil | Capacidad |
|---|---|---|
| Bóveda de Cero Cómputo | Nodo en la nube ~$7/mes, ≤1 GB RAM | Solo libro mayor WORM y enrutador criptográfico; delega el procesamiento pesado al Relé Yo-Yo |
| Relé Yo-Yo | Nodo en la nube elástico aprovisionado por el operador | Puente con estado hacia un nodo de cómputo temporal; ejecuta [[service-extraction|extracción]] en lote, luego se desmonta |
| Hierro Soberano | Estación de trabajo con ≥16 GB RAM o servidor bare-metal | Carga el [[service-slm|modelo de lenguaje pequeño]] local completo en RAM; sin egreso a la nube |

## Libremente transferible

Cada instancia de `os-totebox` está prevista para distribuirse como una única imagen de disco (`.img` o `.vmdk`). El operador la toma y la mueve entre proveedores de nube, un servidor privado o hardware propio en sus instalaciones. No hay sistema operativo anfitrión subyacente que posea las claves. Esta es la intención del Addendum Soberano en forma física: la instancia en ejecución permanece como propiedad del operador en cualquier entorno.

## Véase también

- [[os-family-overview]] — dónde encaja os-totebox en la familia de ocho SO
- [[console-os]] — el Libro Mayor de Comandos que se conecta a os-totebox y presenta su estado
- [[os-orchestration]] — el agregador de flota que consulta muchos Toteboxes a la vez
- [[diode-standard]] — el protocolo unidireccional a través del cual se comunica el Totebox
- [[sel4-microkernel-substrate]] — el núcleo que sustenta las garantías de aislamiento de os-totebox
- [[machine-based-auth]] — cómo el emparejamiento rige el acceso a un Totebox
- [[worm-ledger-design]] — la disciplina de almacenamiento de solo adición aplicada por os-totebox
