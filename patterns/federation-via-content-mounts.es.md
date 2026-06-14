---
schema: foundry-doc-v1
title: "Federación mediante montajes de contenido"
slug: federation-via-content-mounts
short_description: "El patrón para combinar contenido editorial curado con montajes declarativos de repositorios especializados en una única superficie wiki — previsto para la Fase 6 del motor de conocimiento."
category: patterns
type: topic
content_type: topic
status: pre-build
bcsc_class: public-disclosure-safe
last_edited: 2026-06-01
editor: pointsav-engineering
paired_with: federation-via-content-mounts.md
---

# Federación mediante montajes de contenido

El patrón de federación de contenido combina dos modos de autoría complementarios en una única instancia wiki: artículos editoriales curados comprometidos directamente en el repositorio de conocimiento, y montajes declarativos que extraen contenido de repositorios especializados. Ambos modos comparten superficie de URL, cromo de navegación e índice de búsqueda, manteniendo sus repositorios fuente independientes. Este patrón está previsto para la Fase 6 de [[app-mediakit-knowledge]]; el modelo de repositorio único es la forma actualmente desplegada.

---

## El modelo híbrido

Una instancia wiki desplegada se configura mediante un manifiesto `knowledge.toml` en la raíz del directorio de contenido. El manifiesto declara cero o más montajes junto a cualquier artículo comprometido directamente en el repositorio. Ambas fuentes se renderizan en el mismo espacio de nombres de URL; los lectores no encuentran distinción visible entre un artículo editorial y un artículo montado.

Los compromisos directos son la opción correcta para el contenido de naturaleza editorial — artículos de referencia de la plataforma, notas del sistema de diseño, documentos de gobernanza — donde el repositorio de conocimiento es el hogar canónico y la edición fluye a través de la cadena de compromisos de staging estándar. Los montajes declarativos son la opción correcta para el contenido que se origina en un repositorio especializado — documentación por proyecto, registros de decisiones arquitectónicas, registros de cambios — donde el repositorio fuente es el hogar canónico y el wiki es una superficie de lectura sobre él.

---

## Cómo funcionan los montajes

Se prevé que una entrada de montaje en `knowledge.toml` especifique cuatro elementos: el repositorio fuente (URL remota o ruta local que el motor puede extraer), la ruta de montaje local (directorio bajo el cual se coloca el contenido extraído), el plano (esquema nombrado que valida y enruta los archivos del montaje), y la plantilla de URL de edición (patrón de URL que el motor usa para construir el enlace "editar esta página", enrutando a los editores de vuelta al repositorio fuente).

Se prevé que el motor extraiga el repositorio fuente al arrancar y en un intervalo de actualización configurado, escriba el contenido extraído en la ruta de montaje y lo procese de forma idéntica a los artículos comprometidos directamente.

---

## Planos

Un plano es un esquema nombrado que restringe qué contenido puede contener un montaje. Se prevé que dos planos sean integrados:

*`topic`.* El formato de artículo wiki estándar. Los archivos deben cumplir el esquema de frontmatter del contrato de contenido y las convenciones de cuerpo. Renderizado en `/:categoría/:slug` e incluido en el índice de artículos principal y la búsqueda.

*`guide`.* Documentos operacionales dirigidos a profesionales. Renderizados con un cromo diferenciado que enfatiza los pasos procedurales sobre las secciones de prosa. Excluidos del índice de artículos principal, pero descubribles mediante búsqueda y el [[guide-catalog|catálogo de guías]].

Se prevé que los operadores puedan registrar planos adicionales como complementos cuando la Fase 6 esté disponible. Los planos especializados candidatos incluyen `regional-market` (artículos de ubicación estructurados), `adr` (registros de decisiones arquitectónicas con esquema fijo de decisión/estado/contexto) y `changelog` (notas de versión ordenadas cronológicamente).

---

## Aislamiento por instancia

Se prevé que cada instancia wiki lea sólo los montajes declarados en su propio `knowledge.toml`. Dos instancias que extraigan del mismo repositorio pueden presentar conjuntos de artículos completamente diferentes según sus configuraciones de montaje. No existe un registro global de montajes — el aislamiento es una propiedad de configuración de la instancia, no un problema de coordinación.

Esta propiedad de aislamiento es lo que permite que un único repositorio de contenido canónico sirva a múltiples despliegues wiki distintos. El repositorio de contenido es la fuente de verdad; cada despliegue es una vista sobre él, configurada por su manifiesto de montaje.

---

## Procedencia y enrutamiento de edición

Se prevé que todo artículo renderizado desde un montaje declarativo lleve campos de procedencia en su frontmatter: `source_repo` (URL remota del repositorio fuente), `source_path` (ruta del archivo dentro del repositorio fuente) y `edit_url` (URL que el motor renderiza como enlace "editar esta página").

Se prevé que el campo `edit_url` enrute a los editores a la ruta de edición canónica en el repositorio fuente, en lugar de aceptar escrituras localmente. Esto mantiene intacta la inversión de la fuente de verdad en toda la superficie de contenido federada: el hogar canónico de un artículo montado es el repositorio fuente; la instancia wiki es una superficie de lectura sobre él, no un segundo almacén canónico.

---

## Relación con la inversión de la fuente de verdad

Este patrón está previsto para extender [[source-of-truth-inversion]] de una topología de repositorio único a una topología de múltiples repositorios. La invariante es la misma: git es canónico; el binario en ejecución es una vista. La extensión es que "git" puede ser uno de varios repositorios nombrados, cada uno el hogar canónico de su dominio, y la instancia wiki una vista sobre todos ellos simultáneamente.

---

## Véase también

- [[app-mediakit-knowledge]] — el motor que implementa este patrón
- [[source-of-truth-inversion]] — la decisión de diseño fundamental que este patrón extiende
- [[knowledge-wiki-leapfrog-architecture]] — la filosofía de arquitectura de IA y navegación más amplia
