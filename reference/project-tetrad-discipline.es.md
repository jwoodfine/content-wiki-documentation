---
schema: foundry-doc-v1
title: "Disciplina de Tétrada de Proyecto"
slug: project-tetrad-discipline.es
category: reference
type: topic
quality: published
short_description: La regla estructural de cuatro patas que todo clúster de proyecto debe satisfacer — código fuente, manual operativo, instancia de despliegue y contribución al wiki de conocimiento.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: project-tetrad-discipline.md
---

La Disciplina de Tétrada de Proyecto establece que todo clúster de ingeniería activo debe mantener cuatro componentes estructurales en paralelo: código en el repositorio de proveedor, manuales operativos para el cliente, una instancia de despliegue funcional y una contribución al wiki público de documentación. Ningún hito puede ser ratificado si alguna de estas cuatro patas está silenciosamente ausente.

## Por qué cuatro patas

La Tríada anterior — que exigía código, manual y despliegue — garantizaba que cada clúster produjera software completo. La Tétrada extiende esa lógica al conocimiento público: sin una pata de wiki, las contribuciones de documentación son opcionales y el crecimiento del conocimiento colectivo es incidental en lugar de estructural. Cuando la pata de wiki es obligatoria, cada hito de ingeniería genera un artefacto de conocimiento que se publica, se refina editorialmente y alimenta el ciclo de entrenamiento continuo del sustrato.

## Las cuatro patas en resumen

La **pata de proveedor** contiene el código fuente agnóstico al inquilino, parametrizado por identificador de módulo. La **pata de cliente** contiene los manuales de operación en la carpeta de catálogo correspondiente al inquilino y la forma de despliegue. La **pata de despliegue** es una instancia numerada en el directorio de instancias de tiempo de ejecución, con su manifiesto declarando propósito, versión y estado. La **pata de wiki** es un camino de contribución a la wiki de documentación: los borradores se etapan en el directorio de salida del clúster, el portal editorial de project-language los refina y los entrega al repositorio wiki para su publicación.

## Declaración en el manifiesto y ratificación

Cada manifiesto de clúster declara un campo `tetrad:` con al menos una entrada por pata. Las patas que aún no están activas se declaran como `leg-pending` con un plan concreto. La sesión de nivel Master ratifica los hitos verificando que las cuatro patas estén declaradas y que al menos tres tengan contribuciones en el hito actual. Una pata silenciosamente omitida equivale a un fallo de ratificación.

## Legado de la Tríada

Los clústeres creados bajo la Tríada reciben una difusión de actualización en su buzón de entrada. La tarea consiste en renombrar el campo `triad:` a `tetrad:`, agregar la pata de wiki con temas planificados y confirmar los cambios. Los hitos anteriores ratificados bajo la Tríada permanecen válidos; la disciplina de Tétrada se aplica desde el compromiso de actualización en adelante.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Con licencia [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*
