---
schema: foundry-doc-v1
title: "Disciplina de archivos en la raíz"
slug: root-files-discipline
category: reference
index_group: editorial-and-publishing-standards
type: topic
content_type: topic
quality: complete
short_description: La convención según la cual todo repositorio y sub-clon de proyecto mantiene un conjunto pequeño y explícitamente enumerado de archivos de acompañamiento canónicos en su raíz — y nada más.
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-24
editor: pointsav-engineering
cites: []
language_protocol: TRANSLATE-ES
paired_with: root-files-discipline.md
---


La Disciplina de Archivos en la Raíz establece que todo repositorio del marco de ingeniería de PointSav mantiene un directorio raíz limpio. Limpio significa que una lista pequeña y explícitamente enumerada de archivos es permitida en la raíz, y cualquier otro archivo es un defecto que requiere reubicación. La convención organiza los archivos en seis niveles según el momento del ciclo de vida del repositorio en que se vuelven obligatorios. La disciplina interactúa directamente con el [[citation-substrate|sustrato de citas]] — todo repositorio esperando citas externas lleva un archivo `CITATION.cff` en la raíz.

## Los seis niveles

El **nivel 1** es siempre obligatorio desde el primer día: `README.md` como punto de entrada en inglés, `README.es.md` como resumen de adaptación estratégica en español y `LICENSE` con el texto completo de la licencia primaria del repositorio. Un repositorio sin estos tres archivos está estructuralmente incompleto.

El **nivel 2** es obligatorio cuando el trabajo está activo: `CLAUDE.md` como guía operativa, `AGENTS.md` como puntero neutro de proveedor para agentes de codificación de cualquier origen, y `NEXT.md` con los elementos abiertos en orden de prioridad. Estos tres archivos llegan juntos en el commit de activación del proyecto; escribir código de funcionalidad sin completarlos antes es un defecto de proceso.

La convención `AGENTS.md`, publicada en diciembre de 2025 y mantenida bajo la Linux Foundation, permite que agentes de codificación de cualquier proveedor descubran la guía operativa del proyecto a partir de un nombre de archivo estándar, sin necesitar conocer el nombre de archivo preferido de un proveedor concreto. El contenido sustantivo vive en `CLAUDE.md`; `AGENTS.md` es un puntero delgado.

El **nivel 3** se requiere cuando ha ocurrido trabajo significativo: `CHANGELOG.md` con el historial de versiones en formato keep-a-changelog, una entrada por commit aceptado. Se aplica la regla de versionado: un incremento de parche por commit aceptado, un incremento menor por hito de funcionalidad, un incremento mayor por cambio disruptivo.

El **nivel 4** incluye archivos opcionales según el caso: `ARCHITECTURE.md` para repositorios cuyo diseño justifica una visión general dedicada, `SECURITY.md` para el modelo de amenazas y la vía de divulgación, `INVENTIONS.md` para afirmaciones novedosas que surgen del repositorio, `CONTRIBUTING.md` para repositorios que esperan recibir contribuciones de nivel abierto, `CITATION.cff` para repositorios que se espera sean citados externamente, y varios otros. Cada uno es opcional; la decisión de añadirlo se toma cuando el alcance del repositorio lo justifica, no por defecto.

El **nivel 5** son archivos de herramientas por tipo de repositorio, según lo que el tipo de repositorio requiera: los repositorios de espacio de trabajo Rust llevan `Cargo.toml` y `Cargo.lock`; los proyectos Python llevan `pyproject.toml`; todo directorio rastreado lleva `.gitignore`. Se esperan en la raíz para sus respectivos tipos de repositorio, pero no son archivos de acompañamiento canónicos en el sentido doctrinal.

El **nivel 6** está prohibido en la raíz: los scripts pertenecen dentro del directorio del proyecto sobre el que operan, no en la raíz del repositorio. La documentación orientada al usuario pertenece al wiki de documentación. Los temas de arquitectura y las ADR pertenecen al wiki de documentación. El material del sistema de diseño pertenece al repositorio de diseño. Los binarios grandes se obtienen en tiempo de compilación y nunca se incluyen en el repositorio. Los archivos con sufijos de número de versión en su nombre — `_V2`, `_V3` y similares — representan violaciones de la edición-en-el-lugar y se trasladan al archivo canónico único correcto, con el historial preservado en Git.

## Disciplina de licencias

El archivo `LICENSE` de cada repositorio es el archivo de nivel 1 más consecuente. Determina lo que los consumidores posteriores pueden hacer con el contenido del repositorio. El marco mantiene un directorio de licencias en el repositorio `factory-release-engineering` como fuente única de verdad para todo texto de licencia usado en el marco. Las asignaciones de licencia se declaran en un mapa legible por máquina que indica qué licencia aplica a qué repositorio, a veces con anulaciones por ruta para monorepos de licencia mixta. Un script de propagación lee el mapa y copia el texto de licencia apropiado en el archivo `LICENSE` de cada repositorio de destino cuando se ejecuta la propagación de gobernanza.

Los archivos fuente llevan cabeceras de identificador de licencia SPDX usando el vocabulario de identificadores estandarizado, en lugar de incrustar el texto completo de la licencia en línea.

## Postura bilingüe

La regla bilingüe de la guía operativa a nivel de espacio de trabajo se aplica de manera uniforme. El material orientado al público es bilingüe: `README.md` con `README.es.md`, los archivos TOPIC del wiki de documentación, y la doctrina constitucional con su resumen en español. La documentación operativa interna — `CLAUDE.md`, `NEXT.md`, `CHANGELOG.md`, los manuales de operación — es solo en inglés. El criterio discriminante es si un lector nuevo fuera de los operadores de habla inglesa del marco podría encontrar el archivo; si es así, lleva un par en español.

## Por qué existe esta convención

La Disciplina de Archivos en la Raíz cumple tres propósitos estructurales. Hace que los repositorios sean inmediatamente navegables para contribuyentes que llegan con cualquier agente de codificación: tanto `AGENTS.md` como `CLAUDE.md` están presentes y apuntan en la misma dirección. Hace que los repositorios sean citables mediante `CITATION.cff` en todo repositorio que se espera sea citado externamente, dando soporte al sustrato de citas que trata la procedencia como una preocupación de primera clase. Y asegura que los límites de licencia sean inequívocos en la raíz de cada repositorio, lo cual es la condición previa para que el modelo de tres niveles de contribuyentes — núcleo, de pago y abiertos — pueda operar legalmente a escala.

Los archivos faltantes salen a la luz al inicio de sesión, cuando cualquier sesión en un repositorio observa que falta un archivo de nivel 1 o nivel 2 requerido. La sesión registra el defecto y continúa con la tarea real; no crea silenciosamente el archivo faltante ni ignora la ausencia.

## Véase también

- [[citation-substrate]] — el sustrato de citas de la plataforma que alimenta `CITATION.cff`
- [[disclosure-substrate]] — la capa de gobernanza que controla la propagación de licencias
- [[language-protocol-substrate]] — la especificación de postura bilingüe que gobierna los pares README

