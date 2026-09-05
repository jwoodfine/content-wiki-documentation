---
schema: foundry-doc-v1
title: "Cómo desplegar una instancia de conocimiento"
slug: deploy-knowledge-instance
short_description: "Despliega una instancia de app-mediakit-knowledge desde una ruta de contenido local: escribe una configuración knowledge.toml con [site] + [[mount]], compila el binario y arráncalo con el subcomando serve."
category: self-hosting
index_group: getting-the-platform-running
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Ingenieros (con acceso directo al terminal); operadores de cliente"
language: es
language_protocol: TRANSLATE-ES
last_edited: 2026-08-04
editor: pointsav-engineering
paired_with: deploy-knowledge-instance.md
---

## Requisitos previos

- El binario `app-mediakit-knowledge` compilado desde el monorepo (véase [[install-toolchain]])
- Uno o más clones de repositorios de contenido `media-knowledge-*` en el host de despliegue
- Un puerto de despliegue que no esté ocupado por otro servicio (por defecto `127.0.0.1:9090`)
- Una sesión de terminal en el host

## Propósito

Una instancia de conocimiento es un despliegue en ejecución de `app-mediakit-knowledge`, el motor que sirve las wikis de documentación y de proyectos de la plataforma. Desplegar una consiste en escribir un `knowledge.toml` que declare un `[site]` y al menos un `[[mount]]` de contenido, y después arrancar el binario contra ese archivo con el subcomando `serve`.

## Procedimiento

1. Localice o clone el repositorio de contenido que quiere servir:

   ```
   ls /ruta/a/media-knowledge-documentation/
   ```

   Si aún no está clonado:

   ```
   git clone git@github.com:pointsav/media-knowledge-documentation.git
   ```

2. Escriba el `knowledge.toml`:

   ```toml
   [site]
   title = "PointSav Documentation"
   brand = "pointsav"            # "pointsav" o "woodfine" — selecciona el conjunto de tokens
   bind = "127.0.0.1:9090"
   instance = "documentation"    # "documentation" | "projects" | "corporate"

   [[mount]]
   path = "/ruta/a/media-knowledge-documentation"
   role = "primary"              # el mount primario es editable; los demás son de solo lectura
   ```

   Todos los campos de `[site]` salvo `title` tienen valores por defecto (`brand` → `"pointsav"`, `bind` → `"127.0.0.1:9090"`, `state_dir` → `/var/lib/local-knowledge/state`) — declárelos explícitamente solo cuando necesiten diferir. `[[mount]]` es repetible; un segundo mount de solo lectura es la forma en que una sola instancia federa contenido de otro archivo (véase [[use-knowledge-mounts]]).

3. Compile el binario, si aún no dispone de uno:

   ```
   cd /ruta/a/pointsav-monorepo
   cargo build -p app-mediakit-knowledge --release
   ```

   El binario queda en `target/release/app-mediakit-knowledge`. Cópielo al host de despliegue si se trata de una máquina distinta.

4. Arranque la instancia:

   ```
   app-mediakit-knowledge serve --knowledge-toml knowledge.toml
   ```

   `--knowledge-toml` también puede suministrarse mediante la variable de entorno `WIKI_KNOWLEDGE_TOML`, que es la forma que suele emplear una unidad systemd. El subcomando hermano `check` (`app-mediakit-knowledge check --knowledge-toml knowledge.toml`) valida la configuración y el contenido sin arrancar ningún servidor — útil como control de CI antes de desplegar un cambio de configuración.

## Resultado esperado

La instancia se enlaza a la dirección de `[site].bind`, lee Markdown directamente desde cada ruta montada y sirve el wiki. Las ediciones de contenido en el repositorio aparecen en la siguiente petición — no existe ningún paso de compilación ni de reindexado entre una edición y su publicación.

## Verificación

Solicite la página de inicio:

```
curl -s http://127.0.0.1:9090/ | head -20
```

La respuesta debe contener HTML renderizado a partir del `index.md` del mount. Solicite una página de categoría para confirmar el enrutamiento:

```
curl -s http://127.0.0.1:9090/category/architecture | grep '<title>'
```

Si una página devuelve 404, confirme que el `path` de `[[mount]]` apunta a un directorio que contiene realmente la carpeta de categoría esperada, y que el subcomando `check` de `knowledge.toml` se ejecuta sin errores antes que nada.

## Reversión

Detenga el proceso (o ejecute `systemctl stop` sobre la unidad, si corre como tal). No se escribe estado fuera de `state_dir`; eliminar o revertir `knowledge.toml` y reiniciar devuelve la instancia a su configuración anterior. El repositorio de contenido no resulta alterado por el hecho de servirlo — revertir una edición de contenido defectuosa es una operación `git` normal en ese repositorio, no una reversión de despliegue.

## Próximos pasos

- [[use-knowledge-mounts]] — monte un segundo repositorio de contenido, de solo lectura, en esta instancia
- [[federate-archives-via-content-mounts]] — sirva contenido de múltiples archivos a través de una sola instancia
- [[self-host-a-deployment]] — la vía de despliegue de appliance más amplia dentro de la cual esta instancia puede ejecutarse

## Véase también

- [[app-mediakit-knowledge]] — la arquitectura del servidor wiki y el modelo de tres instancias
- [[use-knowledge-mounts]] — montar contenido de múltiples repositorios en una instancia
- [[install-toolchain]] — compilar el binario desde el código fuente del monorepo
- [[self-host-a-deployment]] — el procedimiento de despliegue más amplio del que este es un componente
- [[federate-archives-via-content-mounts]] — cómo servir contenido de múltiples archivos en una instancia
