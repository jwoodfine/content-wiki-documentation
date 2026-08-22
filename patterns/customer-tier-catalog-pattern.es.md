---
schema: foundry-doc-v1
title: "Patrón de catálogo en el nivel cliente"
slug: customer-tier-catalog-pattern
aliases:
  - customer-tier-catalog-pattern
short_description: "Disciplina catálogo-instancia en el nivel cliente — definiciones de despliegue reutilizables en git; instancias específicas de cada copia fuera de los repositorios compartidos."
category: patterns
type: topic
content_type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: customer-tier-catalog-pattern.md
index_group: deployment-and-configuration
---

El nivel cliente separa las definiciones de despliegue de las instancias de despliegue. El catálogo registra qué es un despliegue: sus manuales operativos y su alcance. Las instancias numeradas registran dónde y cómo se ejecuta una copia concreta de ese despliegue. **Quien examina un despliegue en ejecución está viendo una instancia; la definición de la que se aprovisionó vive en otro lugar por completo**, y un cambio en una nunca modifica silenciosamente la otra.

## Catálogo e instancia son formas distintas

Una entrada de catálogo describe un despliegue sin codificar valores específicos del entorno. Es reutilizable: pueden ejecutarse simultáneamente múltiples instancias del mismo nombre de despliegue. El catálogo es aquello *de lo que* se aprovisiona una nueva instancia, no aquello *como lo que* se ejecuta.

Una instancia codifica los valores que hacen concreto al catálogo: la versión del servicio en ejecución, la configuración específica del entorno y cualquier estado local a esa copia. La instancia es lo que está ejecutándose realmente.

## Qué vive en el catálogo

Las entradas de catálogo viven en el repositorio de gestión de flota, un directorio por nombre de despliegue. En la práctica, una entrada de catálogo lleva un README bilingüe y uno o más manuales operativos propios de ese despliegue específico — por eso viven dentro del directorio de la entrada, no en otro lugar del repositorio.

## Qué vive en la instancia

Las instancias viven en un directorio local excluido del control de versiones, uno por copia numerada. Una instancia lleva un manifiesto con los campos que la distinguen de otras copias: la versión en ejecución, el número de instancia y el estado del ciclo de vida. **El manifiesto que realmente describe una copia en ejecución vive con esa copia, no en el catálogo compartido** — al verificar dos despliegues reales, ninguno lleva un archivo de manifiesto en su entrada de catálogo, solo en su instancia aprovisionada.

## Nombres de despliegue y la taxonomía de prefijos

| Prefijo | Alcance |
|---|---|
| `fleet-` | Servicios de flota distribuida multinodo |
| `route-` | Capas de enrutamiento y gestión de tráfico |
| `gateway-` | Servicios de puerta de enlace orientados al exterior |
| `cluster-` | Coordinación a nivel de clúster y servicios de archivo |
| `node-` | Servicios de nodo único en un rol nombrado |
| `media-` | Servicios de procesamiento de contenido orientados al cliente |
| `vault-` | Servicios de almacenamiento, libro mayor y criptografía |

## Ejemplo práctico: gateway-orchestration-gis

El despliegue de orquestación GIS demuestra el patrón directamente. Su entrada de catálogo lleva el par README y los manuales operativos para aprovisionamiento, reconstrucción del proceso de datos y adición de un país o cadena nueva. La instancia en ejecución lleva la configuración y el estado acumulado desde el aprovisionamiento; el sufijo numérico es el número de instancia.

## Aprovisionamiento y decomisionamiento

El aprovisionamiento comienza leyendo la entrada de catálogo. La sesión crea el directorio de instancia, escribe un manifiesto y aplica la configuración específica. Credenciales y vínculos DNS los proporciona el operador en el momento del aprovisionamiento; no viajan a través del control de versiones.

El decomisionamiento sigue un modelo de dos partes: la sesión propietaria desmantela el servicio ordenadamente; un paso separado de coordinación registra la finalización. El catálogo persiste — una instancia futura puede aprovisionarse desde la misma entrada sin ningún cambio en el repositorio.

## Véase también

- [[editorial-pipeline-three-stages]] — un ejemplo de proceso definido en catálogo que ejecuta una instancia aprovisionada
- [[language-protocol-substrate]] — el sustrato de familia de género que implementa un proceso editorial
- [[os-totebox]] — el entorno operativo en el que se ejecutan los despliegues de tipo clúster

## Procedencia

Versión en español elaborada por project-language, adaptación estratégica — no es una traducción literal del artículo canónico en inglés.
