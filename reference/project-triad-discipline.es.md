---
schema: foundry-doc-v1
title: "Disciplina de Tríada de Proyecto"
slug: project-triad-discipline.es
category: reference
type: topic
quality: published
short_description: La regla estructural predecesora de tres patas para clústeres de proyecto — código fuente, manual operativo e instancia de despliegue — actualmente reemplazada por la Disciplina de Tétrada.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: project-triad-discipline.md
---

La Disciplina de Tríada de Proyecto, introducida en la versión 0.0.4 de la Doctrina, exigía que todo clúster de proyecto activo mantuviera tres patas estructurales en paralelo: código en el repositorio de proveedor, manuales operativos para el cliente y una instancia de despliegue funcional. Esta convención ha sido reemplazada por la Disciplina de Tétrada de Proyecto a partir de la versión 0.0.10 de la Doctrina, que añade una cuarta pata obligatoria para las contribuciones al wiki de conocimiento. Este artículo documenta el fundamento de diseño de la Tríada, que permanece como base de la Tétrada.

## El problema que resolvía la Tríada

Sin una disciplina estructural, los proyectos de software derivan hacia tres modos de fallo predecibles: código que madura sin manuales operativos, manuales que maduran sin código funcional, y ambos maduran sin un tiempo de ejecución probado. La Tríada hacía que los tres modos fueran estructuralmente imposibles al exigir que cada clúster articulara dónde vive cada pata antes de poder recibir la ratificación de hito.

## Las tres patas

La **pata de proveedor** alberga el código fuente genérico y agnóstico al inquilino. La **pata de cliente** contiene los manuales de operación en la carpeta de catálogo correspondiente al inquilino del despliegue. La **pata de despliegue** es una instancia numerada en el directorio de instancias, con su manifiesto que declara inquilino, propósito, versión de origen y estado actual.

La disciplina se aplica a nivel de clúster a lo largo de su ciclo de vida, no a nivel de confirmación individual. Una confirmación que solo toque la pata de proveedor no es una violación; lo que importa es que las tres patas avancen en cada hito ratificado.

## Relación con la Tétrada

La Tríada se conserva aquí como referencia histórica. Todos los clústeres nuevos, y todos los existentes tras recibir la difusión de actualización a Tétrada, siguen la Disciplina de Tétrada de Proyecto. Las tres patas de la Tríada son idénticas dentro de la Tétrada; únicamente se añade la cuarta pata de wiki.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Con licencia [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*
