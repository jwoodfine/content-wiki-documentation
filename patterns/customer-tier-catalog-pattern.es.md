---
schema: foundry-doc-v1
title: "El Patrón de Catálogo en el Nivel Cliente"
slug: customer-tier-catalog-pattern
category: patterns
type: topic
content_type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-06-10
editor: pointsav-engineering
paired_with: customer-tier-catalog-pattern.md
---

El nivel cliente separa las definiciones de despliegue de las instancias de despliegue. El catálogo registra qué es un despliegue: sus manuales operativos, artefactos requeridos y alcance. Las instancias numeradas registran dónde y cómo se ejecuta una copia concreta de ese despliegue. Las dos formas viven en rutas distintas, siguen reglas de seguimiento distintas y sirven propósitos distintos. Confundirlas es un error operativo recurrente en la gestión de flota; la convención de nomenclatura y la estructura de rutas hacen la distinción visible de un vistazo.

## Por Qué el Catálogo y la Instancia Son Formas Distintas

Una entrada de catálogo describe un despliegue sin codificar valores específicos del inquilino o del entorno. Es reutilizable: pueden ejecutarse simultáneamente múltiples instancias del mismo nombre de despliegue para distintos inquilinos o en momentos distintos para el mismo inquilino. El catálogo es aquello *de lo que* se aprovisiona una nueva instancia — no aquello *como lo que* se ejecuta.

Una instancia codifica los valores que hacen concreto al catálogo: el identificador del inquilino, la versión del servicio en ejecución, la configuración específica del entorno y cualquier estado en tiempo de ejecución local a esta copia. Los datos de instancia pueden incluir credenciales que no deben llegar a un repositorio de código compartido. La instancia es lo que está ejecutándose realmente.

## Qué Vive en el Catálogo

Las entradas de catálogo viven en `customer/woodfine-fleet-deployment/<nombre-del-despliegue>/` y se rastrean en el repositorio de gestión de flota. Una entrada de catálogo es agnóstica al inquilino.

Artefactos requeridos en una entrada de catálogo:

- `README.md` y `README.es.md` — descripción en lenguaje sencillo de lo que hace el despliegue
- `MANIFEST.md` — metadatos estructurados que cubren nombre del despliegue, versión fuente y estado del ciclo de vida
- Archivos `guide-*.md` — manuales operativos del despliegue; pertenecen dentro del directorio de la entrada de catálogo, no en la raíz del repositorio de flota

Los archivos GUIDE dentro de una entrada de catálogo son los complementos operativos de los artículos TOPIC que describen qué hace el servicio. Un GUIDE describe *cómo operar este despliegue* para quien lo ejecuta.

## Qué Vive en la Instancia

Las instancias viven en `~/Foundry/deployments/<nombre-del-despliegue>-N/` donde `N` es un entero secuencial basado en 1 que distingue instancias concurrentes o sucesivas del mismo nombre de despliegue. Esta ruta está excluida del control de versiones a nivel del espacio de trabajo: las instancias no aparecen en ningún repositorio.

Artefactos requeridos en una instancia:

- `MANIFEST.md` — creado desde la plantilla compartida de MANIFEST de despliegue; lleva los campos que distinguen esta instancia de las demás: inquilino, versión fuente, número de instancia y estado actual del ciclo de vida
- `README.md` y `README.es.md` — copiados o generados en el momento del aprovisionamiento

Una instancia puede acumular artefactos en tiempo de ejecución adicionales después del aprovisionamiento: archivos de registro, configuración local y detalles de conexión específicos del entorno. El límite de exclusión del control de versiones mantiene estos archivos locales por defecto.

## Nombres de Despliegue y la Taxonomía de Prefijos

Los nombres de despliegue siguen la taxonomía de prefijos de flota de la matriz de nomenclatura. Siete prefijos canónicos definen el alcance semántico de cada categoría de despliegue:

| Prefijo | Alcance |
|---|---|
| `fleet-` | Servicios de flota distribuida multinodo |
| `route-` | Capas de enrutamiento y gestión de tráfico |
| `gateway-` | Servicios de puerta de enlace orientados al exterior |
| `cluster-` | Coordinación a nivel de clúster y servicios de archivo |
| `node-` | Servicios de nodo único en un rol de nodo nombrado |
| `media-` | Servicios de procesamiento de contenido y conocimiento orientados al cliente |
| `vault-` | Servicios de almacenamiento, libro mayor y criptografía |

El prefijo hace legible el rol del despliegue sin consultar su MANIFEST. Un despliegue llamado `media-proofreader-woodfinegroup` es inmediatamente clasificable: es un servicio de procesamiento de contenido de nivel media, la variante del corrector, con alcance al inquilino `woodfinegroup`. El segmento de inquilino al final del nombre permite la expansión a múltiples instancias en el futuro — un segundo inquilino usaría un sufijo distinto en lugar de crear una colisión de nombres.

## Ejemplo Práctico: media-proofreader-woodfinegroup

El servicio de revisión para el inquilino `woodfinegroup` demuestra el patrón de catálogo/instancia de forma directa.

La entrada de catálogo en `customer/woodfine-fleet-deployment/media-proofreader-woodfinegroup/` contiene el par README que describe el servicio del proceso editorial, el MANIFEST de despliegue y los manuales operativos para la configuración inicial y la operación diaria. Esta entrada está bajo control de versiones y es visible para cualquier colaborador con acceso al repositorio de gestión de flota.

La instancia en `~/Foundry/deployments/media-proofreader-woodfinegroup-1/` contiene la configuración en ejecución: la versión del servicio fijada en el momento del aprovisionamiento, los detalles de vinculación específicos del inquilino y el estado en tiempo de ejecución acumulado desde el inicio. El sufijo `-1` es el número de instancia. Si el despliegue se reprovisiona desde cero o se crea una instancia paralela para pruebas, el siguiente número se incrementa.

El MANIFEST en la entrada de catálogo registra el nombre del despliegue y la versión fuente en el momento en que se creó la entrada. El MANIFEST en la instancia registra los mismos campos más el inquilino, el número de instancia y el estado actual del ciclo de vida.

## Aprovisionamiento y Decomisionamiento

El aprovisionamiento de una nueva instancia comienza leyendo la entrada de catálogo: el README y los archivos GUIDE describen el propósito del despliegue y los pasos para ponerlo en marcha. La sesión de aprovisionamiento crea el directorio `deployments/<nombre>-N/`, escribe un MANIFEST desde la plantilla y aplica cualquier configuración específica de la instancia. Las credenciales, claves de API externas y vínculos DNS los proporciona el operador en el momento del aprovisionamiento; no forman parte de la entrada de catálogo y no viajan a través del control de versiones.

El decomisionamiento sigue un modelo de dos partes. La sesión propietaria de la instancia realiza el desmantelamiento ordenado: detiene el servicio en ejecución, archiva el estado en tiempo de ejecución que valga la pena conservar y elimina el directorio `deployments/<nombre>-N/`. Un paso separado de coordinación del espacio de trabajo registra la finalización del desmantelamiento en el registro de cambios.

La entrada de catálogo persiste después del decomisionamiento. Una instancia futura del mismo nombre de despliegue puede aprovisionarse desde la misma entrada de catálogo sin ningún cambio en el repositorio de gestión de flota. El catálogo es la definición; la instancia es la realización transitoria de esa definición.

## Véase También

- [[editorial-pipeline-three-stages]] — el proceso en tres etapas que ejecuta la instancia del servicio de revisión
- [[language-protocol-substrate]] — el sustrato de familia de género que implementa el proceso
- [[os-totebox]] — el entorno operativo en el que se ejecutan los despliegues de tipo clúster
