---
schema: foundry-doc-v1
title: "Usar montajes de conocimiento declarativos"
slug: use-knowledge-mounts
short_description: "Añade un repositorio de contenido secundario a una instancia de conocimiento en ejecución mediante una entrada [[mount]] en knowledge.toml — al mismo espacio de nombres de slugs plano que el primario, ya que no existe ningún aislamiento por prefijo de URL."
category: how-to
index_group: integration-data
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Ingenieros (con acceso directo al terminal); operadores de cliente"
language: es
language_protocol: TRANSLATE-ES
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: use-knowledge-mounts.md
---

## Requisitos previos

- Una instancia de conocimiento en ejecución con una configuración `knowledge.toml` (véase [[deploy-knowledge-instance]])
- Un segundo repositorio de contenido `media-knowledge-*` clonado en el mismo sistema de archivos
- Acceso de terminal para reiniciar el servicio de conocimiento

## Propósito

Añada un segundo repositorio de contenido a una instancia en ejecución para que sus artículos se indexen junto a los del primario — unos minutos para configurarlo. Lea la guía completa antes de confiar en esto en producción: el mecanismo real no tiene ningún aislamiento entre montajes, y ese es un riesgo genuino y actualmente sin mitigar si los dos repositorios comparten algún slug.

## Procedimiento

1. Anote la ruta absoluta al repositorio secundario:

   ```
   ls /ruta/a/media-knowledge-projects/
   ```

2. Añada una entrada `[[mount]]` a `knowledge.toml`. El esquema real tiene exactamente tres campos — `path`, `role` y `blueprint_set` — y no existe ningún campo `prefix` ni `label`:

   ```toml
   [[mount]]
   path = "/ruta/a/media-knowledge-projects"
   role = "primary"
   blueprint_set = ["TOPIC", "GUIDE"]
   ```

   `role` toma por defecto `"primary"` si se omite. El primer montaje con `role = "primary"` provee el chrome del sitio de la instancia (su `important-information.md`, `categories.yaml` y `redirects.yaml`) — eso es lo único que `role` afecta actualmente. `blueprint_set` se analiza pero actualmente no se aplica en ningún lugar del motor; no confíe en él para restringir qué tipos de artículo se sirven.

   > **Advertencia:** los artículos de cada montaje se indexan en un único espacio de nombres de slugs compartido y plano — no hay prefijo de URL, ni enrutamiento por montaje, ni ningún tipo de aislamiento. Si ambos repositorios contienen un artículo con el mismo slug, el que esté listado más tarde en `knowledge.toml` sobrescribe silenciosamente al anterior en el índice, sin ninguna advertencia al iniciar. Antes de añadir un montaje, revise usted mismo las colisiones de slugs entre los dos repositorios; el motor no las detectará por usted.

3. Reinicie el servicio de conocimiento. La configuración y el contenido se leen una sola vez al iniciar — no hay recarga en caliente:

   ```
   sudo systemctl restart app-mediakit-knowledge
   ```

## Resultado esperado

Los artículos del repositorio secundario se vuelven accesibles bajo el mismo patrón de ruta `/wiki/<slug>` que los propios artículos del primario — no bajo un prefijo separado.

## Verificación

Obtenga un artículo que sepa que existe solo en el repositorio secundario, usando su slug simple:

```
curl -s http://127.0.0.1:9090/wiki/<slug-del-repo-secundario>/
```

Una respuesta exitosa devuelve el artículo renderizado. Si obtiene el contenido del artículo *equivocado*, o contenido que no coincide con lo esperado, eso es una colisión de slugs — revise ambos repositorios en busca del mismo slug y renombre uno antes de continuar.

## Reversión

Elimine el bloque `[[mount]]` de `knowledge.toml` y reinicie el servicio. Si ya ocurrió una colisión, confirme qué artículo se sirvió realmente mientras tanto antes de asumir que la versión del primario quedó intacta — el propio contenido en disco de un artículo eclipsado nunca se modifica por esto, solo cuál sirvió la instancia en ejecución.

## Próximos pasos

- [[federate-archives-via-content-mounts]] — el concepto de federación más amplio que este mecanismo implementa
- [[deploy-knowledge-instance]] — desplegar el servidor wiki que los montajes extienden

## Véase también

- [[app-mediakit-knowledge]] — la arquitectura del servidor wiki, incluyendo el índice de contenido y el pipeline de renderizado
