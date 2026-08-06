---
schema: foundry-doc-v1
title: "Federar archivos mediante montajes de contenido"
slug: federate-archives-via-content-mounts
short_description: "Federa los artículos de una segunda instancia de conocimiento en una instancia en ejecución mediante una entrada [[mount]] en knowledge.toml — un espacio de nombres plano y combinado sin aislamiento, no un esquema de federación con prefijo de URL."
category: how-to
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Ingenieros (con acceso directo al terminal); operadores de cliente"
language: es
language_protocol: TRANSLATE-ES
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: federate-archives-via-content-mounts.md
---

## Requisitos previos

- Dos repositorios de contenido `media-knowledge-*` en el mismo sistema de archivos (o un montaje compartido como NFS)
- Acceso de lectura desde el usuario del proceso de la instancia primaria al directorio de contenido del repositorio secundario
- Acceso de escritura a `knowledge.toml` en la instancia primaria

## Propósito

Lea los artículos de una segunda instancia desde una instancia en ejecución sin copiar archivos — el mecanismo que `app-mediakit-knowledge` llama montaje de contenido. Esto es más limitado que una "federación" en el sentido aislado y con espacio de nombres propio que el término suele implicar: el contenido montado se une al mismo espacio de slugs plano que todo lo demás que la instancia ya sirve.

## Procedimiento

1. En el host que ejecuta el contenido secundario, confirme que el usuario del proceso de la instancia primaria puede leerlo:

   ```
   sudo -u <usuario-del-proceso-wiki> ls /srv/wiki/media-knowledge-projects
   ```

   Si la ruta está en un host remoto, móntela localmente primero. Una ruta ausente al iniciar hace que el montaje se omita, no que falle.

2. Declare el montaje en el `knowledge.toml` de la instancia primaria. Véase [[use-knowledge-mounts]] para los pasos mecánicos completos y el esquema real de `Mount` (`path`, `role`, `blueprint_set` — no existe ningún campo de prefijo de URL).

3. Reinicie la instancia primaria. Tanto la configuración como el contenido montado se leen una sola vez, al iniciar — los cambios en cualquiera de los dos requieren un reinicio para surtir efecto.

4. Acceda a un artículo del repositorio montado en el mismo patrón de ruta `/wiki/<slug>` que usa el primario para sus propios artículos — no hay ningún espacio de nombres ni prefijo separado al que navegar.

## Resultado esperado

La instancia primaria sirve tanto sus propios artículos como los del repositorio montado, indistinguiblemente, desde un único índice de contenido combinado.

## Verificación

Confirme que un artículo que sabe que existe solo en el repositorio montado se resuelve correctamente, y — de forma crítica — confirme que ningún repositorio tiene un artículo con un slug que el otro también use. Véase los pasos de verificación de [[use-knowledge-mounts]] para saber exactamente cómo comprobarlo.

> **Advertencia:** los wikilinks dentro de los artículos montados se resuelven en el mismo espacio de nombres combinado que todo lo demás, sin ninguna comprobación de existencia — un enlace `[[algun-slug]]` funciona si ese slug existe en cualquier lugar de todos los montajes, y produce un enlace muerto si no existe, sin importar qué repositorio lo contenía originalmente. No asuma que los enlaces internos de un artículo montado permanecen limitados a su propio repositorio de origen.

## Reversión

Elimine la entrada `[[mount]]` y reinicie. Véase [[use-knowledge-mounts]] para saber qué revisar si una colisión de slugs ya eclipsó un artículo antes de que lo notara.

## Próximos pasos

- [[use-knowledge-mounts]] — la mecánica completa paso a paso y el esquema real
- [[deploy-knowledge-instance]] — provisione la instancia que servirá el contenido federado

## Véase también

- [[app-mediakit-knowledge]] — el motor wiki que procesa las declaraciones de montaje
