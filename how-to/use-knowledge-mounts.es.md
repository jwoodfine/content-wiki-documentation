---
schema: foundry-doc-v1
title: "Cómo usar los montajes de conocimiento declarativos"
slug: use-knowledge-mounts
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
language: es
language_protocol: TRANSLATE-ES
paired_with: use-knowledge-mounts.md
---

Los montajes de conocimiento permiten que una sola instancia wiki sirva contenido de múltiples repositorios fuente bajo un espacio de URL unificado. Un montaje se declara en `knowledge.toml` — la instancia lee la ruta fuente al inicio y hace que sus artículos estén disponibles en el prefijo de categoría configurado. Esta guía cubre la adición de un montaje de contenido secundario a una instancia existente.

Para la arquitectura de federación que los montajes habilitan, véase [[federate-archives-via-content-mounts]]. Para desplegar el servidor wiki en primer lugar, véase [[deploy-knowledge-instance]].

## Requisitos previos

- Una instancia de conocimiento en ejecución con una configuración `knowledge.toml` (véase [[deploy-knowledge-instance]])
- Un segundo repositorio de contenido `media-knowledge-*` clonado en el mismo host
- Acceso a terminal para reiniciar el servicio de conocimiento

## Paso 1: Identificar la ruta de contenido secundario

El repositorio de contenido secundario debe ser un clon `media-knowledge-*` en el mismo sistema de archivos que la instancia en ejecución. Anote su ruta absoluta:

```
ls /ruta/a/media-knowledge-projects/
```

Confirme que tiene un `index.md` válido y subdirectorios de categorías antes de añadir el montaje — el servidor wiki advertirá al inicio si la ruta del montaje está vacía o mal formada.

## Paso 2: Añadir el montaje a knowledge.toml

Abra `knowledge.toml` y añada una sección `[[mounts]]` después del bloque `[content]`:

```toml
[content]
primary_path = "/ruta/a/media-knowledge-documentation"
instance_name = "documentation"

[[mounts]]
path = "/ruta/a/media-knowledge-projects"
prefix = "projects"
label = "Projects"
```

`path` es la ruta absoluta del sistema de archivos al repositorio secundario. `prefix` es el prefijo de URL bajo el cual aparecerá el contenido montado (p.ej., los artículos montados se sirven en `/projects/<slug>`). `label` aparece en el encabezado de navegación para identificar la sección montada.

Se admiten múltiples montajes — añada secciones `[[mounts]]` adicionales para cada repositorio secundario.

## Paso 3: Reiniciar la instancia de conocimiento

La configuración de montaje se lee al inicio. Reinicie el servicio para que el nuevo montaje surta efecto:

```
sudo systemctl restart app-mediakit-knowledge
```

O si se ejecuta directamente:

```
# detenga el proceso en ejecución, luego:
app-mediakit-knowledge --config knowledge.toml
```

## Paso 4: Verificar que el montaje está sirviendo

Obtenga un artículo de la categoría montada:

```
curl -s http://127.0.0.1:9090/projects/<slug-de-media-knowledge-projects>/
```

Una respuesta exitosa devuelve el HTML del artículo renderizado. Si la respuesta es 404, verifique:

1. El `prefix` en `knowledge.toml` coincide con el segmento de ruta de URL que utilizó
2. El `path` apunta a un directorio con un `_index.md` en al menos un subdirectorio
3. El servicio se reinició correctamente (verifique `journalctl -u app-mediakit-knowledge`)

## Paso 5: Confirmar el aislamiento de wikilinks

Los wikilinks dentro del contenido montado se resuelven contra el espacio de nombres de slug propio del repositorio montado. Un `[[slug]]` en un artículo de projects NO se resolverá contra el slug de un artículo de documentation — cada montaje está aislado. Los enlaces entre montajes deben usar URLs completas.

Este aislamiento es por diseño: las tres instancias en vivo (documentation, projects, corporate) sirven dominios editoriales distintos; mezclar sus espacios de nombres de slug causaría conflictos de resolución.

## Puntos clave

- Los montajes extienden una instancia en ejecución con contenido de un segundo repositorio, servido bajo un prefijo de URL
- La configuración de montaje vive en `knowledge.toml` bajo `[[mounts]]`; se requiere un reinicio después de los cambios
- La resolución de wikilinks es por montaje — `[[slug]]` en una sección montada se resuelve solo contra los slugs de esa sección
- Se admiten múltiples montajes; añada un bloque `[[mounts]]` por repositorio adicional

## Véase también

- [[federate-archives-via-content-mounts]] — la arquitectura de federación que implementan los montajes declarativos
- [[deploy-knowledge-instance]] — desplegar el servidor wiki que los montajes extienden
- [[app-mediakit-knowledge]] — la arquitectura del servidor wiki incluyendo el pipeline de montaje y renderizado
- [[export-structured-data]] — exportar contenido de artículos de un repositorio montado a través de la API del wiki
