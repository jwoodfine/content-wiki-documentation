---
schema: foundry-doc-v1
title: "Disciplina de Archivos en la Raíz"
slug: root-files-discipline.es
category: reference
type: topic
quality: published
short_description: La convención que establece que todo repositorio mantiene un conjunto pequeño y enumerado de archivos de acompañamiento canónicos en su raíz — y nada más.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: root-files-discipline.md
---

La Disciplina de Archivos en la Raíz establece que todo repositorio del marco de ingeniería de PointSav mantiene un directorio raíz limpio. Limpio significa que una lista pequeña y explícitamente enumerada de archivos es permitida en la raíz, y cualquier otro archivo es un defecto que requiere reubicación. La convención organiza los archivos en seis niveles según el momento del ciclo de vida del repositorio en que se vuelven obligatorios.

## Los seis niveles

El **nivel 1** es siempre obligatorio desde el primer día: `README.md` como punto de entrada en inglés, `README.es.md` como resumen de adaptación estratégica en español y `LICENSE` con el texto completo de la licencia primaria del repositorio. Un repositorio sin estos tres archivos está estructuralmente incompleto.

El **nivel 2** es obligatorio cuando el trabajo está activo: `CLAUDE.md` como guía operativa, `AGENTS.md` como puntero neutro de proveedor para agentes de codificación de cualquier origen, y `NEXT.md` con los elementos abiertos en orden de prioridad. Estos tres archivos llegan juntos en el commit de activación del proyecto.

El **nivel 3** se requiere cuando ha ocurrido trabajo significativo: `CHANGELOG.md` con el historial de versiones en formato keep-a-changelog, una entrada por commit aceptado.

El **nivel 4** incluye archivos opcionales según el caso: `ARCHITECTURE.md`, `SECURITY.md`, `INVENTIONS.md`, `CONTRIBUTING.md`, `CITATION.cff` para repositorios que se espera sean citados externamente, y otros. Cada uno se añade cuando el alcance del repositorio lo justifica, no por defecto.

El **nivel 5** son archivos de herramientas por tipo de repositorio: `Cargo.toml` para proyectos Rust, `.gitignore` para todo directorio rastreado por Git, y similares.

El **nivel 6** está prohibido en la raíz: scripts (van dentro del proyecto que los usa), documentación orientada al usuario (va al wiki de documentación), materiales del sistema de diseño (van al repositorio de diseño) y archivos binarios grandes (se obtienen en tiempo de compilación, nunca se incluyen en el repositorio).

## Disciplina de licencias y postura bilingüe

El archivo `LICENSE` en cada repositorio se obtiene de un directorio centralizado de licencias en el repositorio de ingeniería de lanzamiento. Un mapa de asignaciones declara qué licencia aplica a qué repositorio; un script de propagación copia los textos apropiados. La postura bilingüe distingue entre material público — que lleva par en español — y documentación operativa interna — que es solo en inglés.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Con licencia [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*
