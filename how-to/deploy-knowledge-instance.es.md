---
schema: foundry-doc-v1
title: "Cómo desplegar una instancia de conocimiento"
slug: deploy-knowledge-instance
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
language: es
language_protocol: TRANSLATE-ES
paired_with: deploy-knowledge-instance.md
---

Una instancia de conocimiento es un despliegue en ejecución de `app-mediakit-knowledge` — el servidor wiki que renderiza la documentación y los wikis de proyectos de la plataforma. Desplegar una instancia significa compilar el binario, escribir un archivo de configuración `knowledge.toml` que apunte a los repositorios de contenido e iniciar el servicio. Esta guía cubre el despliegue de un wiki de instancia única desde una ruta de contenido local.

Para el modelo de tres instancias (documentación, proyectos, corporativo), véase [[app-mediakit-knowledge]]. Para los montajes de contenido declarativos, véase [[use-knowledge-mounts]].

## Requisitos previos

- El binario `app-mediakit-knowledge` compilado desde el monorepo (véase [[install-toolchain]])
- Uno o más clones del repositorio de contenido `media-knowledge-*` en el host de despliegue
- Un puerto de despliegue (p.ej., 9090) que no esté ocupado por otro servicio
- Una sesión de terminal en el host

## Paso 1: Localizar el repositorio de contenido

El servidor wiki lee Markdown desde una ruta local. Identifique la ruta al repositorio de contenido que desea servir:

```
ls ~/Foundry/clones/project-editorial/media-knowledge-documentation/
```

El repositorio debe contener un `index.md` en la raíz y subdirectorios de categorías con páginas de aterrizaje `_index.md`. Si el contenido aún no ha sido clonado, clónelo primero:

```
git clone git@github.com:pointsav/media-knowledge-documentation.git
```

## Paso 2: Escribir el archivo de configuración

Cree `knowledge.toml` en el directorio de despliegue:

```toml
[server]
port = 9090
bind = "0.0.0.0"

[content]
primary_path = "/ruta/a/media-knowledge-documentation"
instance_name = "documentation"

[search]
enabled = true
index_path = "/var/lib/knowledge/search-index"

[auth]
enabled = false   # establezca true + configure MBA si se necesita la UI del editor
```

`primary_path` debe ser una ruta absoluta a un clon `media-knowledge-*`. `instance_name` aparece en el encabezado renderizado y en los mensajes de registro — use un valor corto y descriptivo.

## Paso 3: Compilar o localizar el binario

Si aún no ha compilado el binario, compílelo desde el monorepo:

```
cd ~/Foundry/clones/<su-archivo>/pointsav-monorepo
cargo build -p app-mediakit-knowledge --release
```

El binario aparece en `target/release/app-mediakit-knowledge`. Cópielo al host de despliegue si son máquinas diferentes.

## Paso 4: Iniciar la instancia

Ejecute el binario con el archivo de configuración:

```
app-mediakit-knowledge --config knowledge.toml
```

O inícielo como un servicio systemd usando la plantilla de archivo de unidad proporcionada (si está disponible en el despliegue). El servicio registra mensajes de inicio: lee la ruta de contenido, construye el índice de búsqueda y comienza a escuchar en el puerto configurado.

## Paso 5: Verificar que la instancia está sirviendo

Obtenga la página de inicio del wiki:

```
curl -s http://127.0.0.1:9090/ | head -20
```

La respuesta debe contener HTML para la página de inicio del wiki renderizada desde `index.md`. Obtenga una página de categoría para confirmar el enrutamiento de artículos:

```
curl -s http://127.0.0.1:9090/architecture/ | grep '<title>'
```

Si alguna página devuelve un 404, verifique que `primary_path` en `knowledge.toml` apunte a un directorio que contenga la carpeta de categoría esperada.

## Puntos clave

- El servidor wiki lee el contenido directamente desde la ruta de archivo local — los cambios en el repositorio de contenido aparecen inmediatamente sin reiniciar el servicio
- `instance_name` en la configuración es la etiqueta usada en los registros y el encabezado renderizado
- El índice de búsqueda se construye al inicio y vive en `index_path` — cambiar esta ruta requiere limpiar el directorio del índice antiguo
- Tres instancias separadas con tres rutas de contenido sirven los wikis de documentación, proyectos y corporativo de forma independiente

## Véase también

- [[app-mediakit-knowledge]] — la arquitectura del servidor wiki y el modelo de tres instancias
- [[use-knowledge-mounts]] — montar contenido de múltiples repositorios en una instancia
- [[install-toolchain]] — compilar el binario desde el código fuente del monorepo
- [[self-host-a-deployment]] — el procedimiento de despliegue más amplio del que este es un componente
- [[federate-archives-via-content-mounts]] — cómo servir contenido de múltiples archivos en una instancia
