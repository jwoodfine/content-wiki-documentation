---
title: "El patrón de catálogo de nivel cliente"
slug: customer-tier-catalog-pattern
category: architecture
last_edited: 2026-06-29
editor: pointsav-engineering
status: stable
---

El **patrón de catálogo de nivel cliente** es el principio estructural que separa lo que un
despliegue *es* de dónde y cómo *se ejecuta*. Una entrada de catálogo registra el propósito,
los artefactos requeridos y los libros de operaciones de una clase de despliegue. Una instancia
registra la máquina, el inquilino, la versión y el estado operativo actual de un despliegue
activo. Los dos registros se almacenan en ubicaciones separadas con reglas de visibilidad
distintas.

## Por qué el catálogo y la instancia tienen formas diferentes

Una entrada de catálogo es agnóstica al inquilino. No contiene credenciales, estado en
ejecución ni configuración específica de ningún cliente. Como la entrada de catálogo no cambia
cuando se provisiona una nueva instancia, puede almacenarse en un repositorio conectado a
GitHub y revisarse junto al software que despliega. Pueden existir múltiples instancias —
para distintos inquilinos, o para el mismo inquilino en versiones diferentes — simultáneamente
contra una única entrada de catálogo, cada una con su propio MANIFEST.md.

Una instancia codifica los datos que varían entre despliegues: la máquina en la que se
ejecuta, el inquilino al que sirve, la versión de origen con la que se provisionó y el estado
operativo actual. Las instancias pueden contener secretos o artefactos en ejecución que no
deben llegar a GitHub. Por ello son exclusivamente locales, numeradas e ignoradas por Git en
el nivel del espacio de trabajo. La convención de nombres hace legible la relación: la entrada
de catálogo `media-proofreader-woodfinegroup` produce instancias numeradas como
`media-proofreader-woodfinegroup-1`, `media-proofreader-woodfinegroup-2`, etcétera.

## Qué vive en el catálogo (agnóstico al inquilino)

El catálogo de nivel cliente reside en el repositorio `woodfine-fleet-deployment`, rastreado
en la organización GitHub `woodfine`. Cada nombre de despliegue tiene un subdirectorio en
`woodfine-fleet-deployment/<nombre>/`. Los artefactos requeridos dentro de ese subdirectorio son:

- `README.md` y `README.es.md` — descripción bilingüe de qué hace el despliegue y cómo se opera.
- `MANIFEST.md` usando la plantilla de manifiesto de despliegue — registra la identidad del
  despliegue, el repositorio de origen, las dependencias y las asignaciones de plataforma.
- Uno o más libros de operaciones `guide-*.md` que describen los pasos para provisionar,
  mantener y retirar una instancia.

El límite del subdirectorio es el límite del alcance. Los archivos de guía de un despliegue
pertenecen dentro de ese subdirectorio, no en la raíz de la flota, que permanece plana.

## Qué vive en la instancia (numerada, solo local)

Un directorio de instancia reside en el espacio de trabajo de despliegue local y es ignorado
por Git. El sufijo `N` es un entero que aumenta monótonamente y distingue despliegues
simultáneos o sucesivos de la misma entrada de catálogo. Los artefactos requeridos son
`MANIFEST.md` (completado a partir de la plantilla del catálogo), `README.md` y
`README.es.md`. El MANIFEST registra la versión específica de origen con la que se provisionó
la instancia, permitiendo un reaprovisionamiento reproducible cuando la instancia se
reconstruya o migre en el futuro.

La configuración por instancia — credenciales, puertos, nombres de host, estado en ejecución
— vive en el directorio de instancia o bajo rutas de sistema que el MANIFEST registra. Nada
de esto llega a Git.

## La convención de nomenclatura de nodo de flota de Nivel 3

Los nombres de despliegue siguen la taxonomía de prefijos de la Matriz de Nomenclatura. Siete
prefijos canónicos cubren el rango completo de tipos de despliegue:

- `fleet-` — clústeres multinodo con una capa de coordinación compartida
- `gateway-` — servicios de entrada de punto único con lógica de enrutamiento
- `cluster-` — grupos de servicios coubicados que comparten un límite de cómputo
- `node-` — instancias de servicios de proceso único
- `media-` — despliegues de procesamiento de contenido orientados al cliente
- `vault-` — servicios de almacenamiento y gestión de secretos
- `route-` — servicios de modelado de tráfico y proxy

El prefijo transmite la forma del despliegue sin necesidad de consultar el MANIFEST.

## Ejemplo ilustrativo — el despliegue del corrector

`media-proofreader-woodfinegroup` ilustra el patrón de forma concreta. La entrada de catálogo
en `woodfine-fleet-deployment/media-proofreader-woodfinegroup/` contiene la definición
operativa: par de README, plantilla de MANIFEST y el libro de operaciones de destilación. El
directorio de instancia de despliegue registra el nombre de la máquina, la versión en vigor y
las rutas de los binarios del servicio activo.

El sufijo `woodfinegroup` distingue este despliegue específico del inquilino de una futura
entrada `media-proofreader-pointsav` que ejecutaría el mismo software para la cuenta de
proveedor PointSav. La distinción de inquilinos a nivel de nombre — en lugar de mediante
banderas en tiempo de ejecución — mantiene el catálogo enumerable mediante inspección.

## Cómo se provisiona una instancia desde el catálogo

El aprovisionamiento es trabajo del operador. El ingeniero de aprovisionamiento lee los libros
de operaciones `guide-*.md` en la entrada del catálogo, crea el directorio de instancia,
completa `MANIFEST.md` a partir de la plantilla con valores específicos de la instancia
(máquina, inquilino, versión de origen, estado: aprovisionamiento) y copia o genera los
archivos de configuración por instancia. Se requiere intervención del operador en puntos de
corte definidos: credenciales, registros de facturación, registro DNS e emisión de
certificados.

## Desmantelamiento — desmontaje controlado por la sesión propietaria

El desmantelamiento sigue un modelo de dos partes. La sesión propietaria de la instancia
realiza el desmontaje controlado: detiene los servicios, archiva el estado en ejecución que
deba conservarse y elimina el directorio de instancia. La sesión de comando audita que el
desmontaje se completó y registra el resultado en el historial de cambios del espacio de
trabajo.

En ambos casos — desmantelamiento controlado o de emergencia — la entrada del catálogo
permanece intacta. Una ejecución de aprovisionamiento futura puede reconstruir una nueva
instancia numerada a partir de la misma entrada de catálogo.

## Véase también

- [[editorial-pipeline-three-stages]] — la canalización que ejecuta la instancia
  `media-proofreader-woodfinegroup`; artículo complementario
- [[language-protocol-substrate]] — el sustrato que implementa la canalización editorial;
  artículo complementario
