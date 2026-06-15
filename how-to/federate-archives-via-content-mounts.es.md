---
schema: foundry-doc-v1
title: "Cómo federar archivos mediante montajes de contenido"
slug: federate-archives-via-content-mounts
category: how-to
content_type: how-to
type: how-to
status: stable
language_protocol: TRANSLATE-ES
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: federate-archives-via-content-mounts.md
---

Los montajes de contenido permiten que una instancia de conocimiento lea el contenido de artículos de la ruta local de una segunda instancia sin copiar archivos. La instancia lectora renderiza el contenido montado como si fuera nativo, con los wikilinks resolviéndose dentro de su gráfico de origen. Esta guía cubre la declaración de un montaje secundario en `knowledge.toml`, la verificación de que el montaje está activo y el acceso a artículos desde la fuente federada.

Para la arquitectura de federación, consulta [[federation-via-content-mounts]]. Para el motor de conocimiento que procesa las declaraciones de montaje, consulta [[app-mediakit-knowledge]].

## Antes de empezar

Necesitas:

- Dos instancias de `app-mediakit-knowledge` en ejecución en el mismo servidor
  o en servidores con un sistema de archivos compartido (NFS o equivalente)
- Acceso de lectura desde el usuario del proceso de la instancia principal al
  directorio de contenido de la instancia secundaria
- Acceso de escritura a `knowledge.toml` en la instancia principal

## Paso 1: Confirma la ruta de contenido de la instancia secundaria

En el servidor que ejecuta la instancia secundaria, localiza su directorio de
contenido. La ruta es el valor `content_root` en el `knowledge.toml` de la
instancia secundaria:

```shell
grep content_root /ruta/al/secundario/knowledge.toml
# ejemplo de salida: content_root = "/srv/wiki/media-knowledge-projects"
```

Confirma que el usuario del proceso de la instancia principal puede leer la
ruta:

```shell
sudo -u <usuario-del-proceso-wiki> ls /srv/wiki/media-knowledge-projects
```

Si la ruta está en un servidor remoto, móntala antes de continuar. El motor
lee las fuentes de montaje al iniciar; una ruta ausente en ese momento hace
que el montaje se omita con una advertencia en el registro.

## Paso 2: Declara el montaje en `knowledge.toml`

Abre el `knowledge.toml` de la instancia principal y agrega una entrada
`[[mount]]`:

```toml
[[mount]]
source = "/srv/wiki/media-knowledge-projects"
prefix = "projects"
```

`source` es la ruta absoluta al directorio de contenido secundario. `prefix`
es una cadena de espacio de nombres opcional que evita colisiones de slugs
cuando ambas instancias definen artículos con el mismo slug. Con
`prefix = "projects"`, un artículo con slug `topic-co-location-methodology`
en el archivo secundario se resuelve como `projects/topic-co-location-methodology`
en el primario.

Omite `prefix` solo cuando estés seguro de que ningún slug aparece en ambas
instancias.

## Paso 3: Reinicia el motor wiki

Aplica la configuración reiniciando el servicio:

```shell
sudo systemctl restart app-mediakit-knowledge
```

El motor lee `knowledge.toml` una vez al iniciar. Una entrada `[[mount]]`
agregada después del inicio inicial no tiene efecto hasta que el servicio
reinicie.

## Paso 4: Verifica que el montaje está activo

Comprueba el registro de inicio para la línea de confirmación del montaje:

```shell
journalctl -u app-mediakit-knowledge --since "1 minuto atrás" | grep -i mount
# esperado: Mounted secondary archive at prefix=projects (N articles)
```

Si la salida muestra `0 articles`, confirma que la ruta `source` es legible y
contiene archivos `.md` a la profundidad esperada. Si la ruta está ausente, el
registro muestra `Mount source not found — skipping` en lugar de un error al
iniciar.

## Paso 5: Accede a los artículos montados

Navega la instancia principal para confirmar que los artículos del archivo
secundario están disponibles. Con `prefix = "projects"` y un artículo
secundario con slug `topic-co-location-methodology`, la URL es:

```
https://<dominio-primario>/how-to/projects/topic-co-location-methodology
```

Los wikilinks dentro de los artículos montados se resuelven en el gráfico de
enlaces del archivo secundario, no del primario. Un enlace
`[[topic-regional-markets-system]]` dentro de un artículo montado se resuelve
en el gráfico secundario — los enlaces entre gráficos se renderizan como
enlaces rojos.

## Véase también

- [[federation-via-content-mounts]] — la arquitectura de federación declarativa y el modelo de montaje
- [[app-mediakit-knowledge]] — el motor wiki que procesa las declaraciones de montaje de `knowledge.toml`
- [[build-a-colocation-map]] — consume datos de inteligencia de ubicación expuestos a través de un montaje
- [[self-host-a-deployment]] — provisiona la instancia que servirá el contenido federado
