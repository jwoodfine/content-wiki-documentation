---
schema: foundry-doc-v1
title: "El Patrón Meta-Repositorio"
slug: topic-meta-repo-pattern.es
category: architecture
type: topic
quality: published
short_description: Un repositorio ligero que se sitúa sobre el código de los proyectos y proporciona a los agentes un contexto compartido sin acoplar los historiales de Git — el patrón estructural que organiza el espacio de trabajo Foundry.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: topic-meta-repo-pattern.md
---

Un **meta-repositorio** es un repositorio que se sitúa sobre el código de los proyectos, proporciona contexto compartido — reglas, doctrina, identidad, herramientas — a cada proyecto que contiene, y mantiene los historiales de los proyectos independientes. No se acoplan historiales de Git; cada proyecto conserva su propio directorio `.git/` y su propio ciclo de lanzamiento. El meta-repositorio permite flujos de trabajo coherentes con múltiples agentes al proporcionar a cada sesión el contexto que necesita para navegar muchos proyectos sin que ese contexto resida en ninguno de ellos.

El espacio de trabajo Foundry implementa este patrón. El directorio del espacio de trabajo es el meta-repositorio. Contiene la carta constitucional, la guía operativa, las convenciones compartidas, el registro de citas, el almacén de identidades, los scripts de herramientas compartidas y el manifiesto general de clones de proyectos.

## Tres capas

El espacio de trabajo Foundry tiene tres capas estructurales: el meta-repositorio del espacio de trabajo (nivel de espacio de trabajo), los repositorios de ingeniería de nivel superior cada uno con su propio `.git/` independiente (nivel de ingeniería), y los directorios de clúster bajo `clones/` que son en sí mismos sub-meta-repositorios que contienen uno o más sub-clones con sus propios `.git/` independientes (nivel de clúster).

## La única regla estricta

La restricción que hace funcionar el patrón es la carrera de `.git/index`: dos sesiones que escriben en el mismo `.git/index` pueden corromperse mutuamente. Dos sesiones en diferentes directorios `.git/` no compiten.

Por lo tanto: una sesión Master por meta-repositorio del espacio de trabajo, una sesión Root por repositorio de ingeniería, una sesión Task por directorio de clúster. Múltiples sesiones Task en diferentes clústeres son seguras porque los sub-clones de cada clúster tienen sus propios `.git/`.

## Roles de sesión y alcance

El patrón meta-repositorio se asigna directamente a los tres roles de sesión de Claude:

**Master** — opera en el meta-repositorio del espacio de trabajo. Escribe documentos de nivel de espacio de trabajo, crea nuevos directorios de clúster y mantiene el manifiesto de clones de proyectos.

**Root** — opera en la raíz de un repositorio de ingeniería. Escribe el CLAUDE.md de ese repositorio, el registro de proyectos y los archivos GUIDE. No opera a nivel del espacio de trabajo.

**Task** — opera en un directorio de clúster por proyecto. Escribe código de características en los sub-clones declarados del clúster, archivos por proyecto CLAUDE.md y NEXT.md, el buzón del clúster y confirmaciones en la rama de características del clúster.

El rol está determinado por el directorio en el que comienza una sesión. No se elige ni se reasigna a mitad de sesión.

## Manifiesto del clúster

Cada directorio de clúster lleva un manifiesto en `.claude/manifest.md` que declara el nombre del clúster, la rama, el estado, la lista de sub-clones con sus repositorios de origen, y la tétrada de cuatro patas requerida por la Doctrina: pierna del proveedor, pierna del cliente, pierna del despliegue y contribuciones de TOPIC al wiki.

## Véase también

- [[compounding-doorman]] — el límite de inferencia a través del cual enrutan las sesiones Task
- [[apprenticeship-substrate]] — cómo las confirmaciones de sesiones Task alimentan el corpus de entrenamiento
- [[topic-knowledge-commons]] — los artefactos del lado público que el meta-repositorio del espacio de trabajo publica

## Referencias

1. Patrón Meta-Repo — vocabulario de la industria 2026; precedente del meta-repo de Marte.
2. Guía de Espacio de Trabajo Multi-Agente Augment Code 2026.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Atribución 4.0 Internacional](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.