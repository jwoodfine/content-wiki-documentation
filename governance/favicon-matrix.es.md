---
schema: foundry-doc-v1
title: "Matriz de favicons e identidad de pestaña"
slug: favicon-matrix
category: governance
type: topic
content_type: topic
quality: complete
index_group: platform-disciplines
short_description: "El wiki sirve un único favicon SVG estático — un glifo de documento azul marino, enlazado desde un archivo estático, la misma marca en cada pestaña sin importar el inquilino."
status: active
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: favicon-matrix.md
---

El wiki sirve un único favicon: un glifo de documento azul marino (`#1a4480`) sobre un cuadrado redondeado, definido como un archivo SVG estático y enlazado desde el `<head>` de la página con un elemento `<link rel="icon">` estándar. Las pestañas de cada inquilino llevan la misma marca — no existe una variante de color o forma por inquilino, ni codificación de URI de datos insertada.

Este artículo describe el mecanismo tal como está construido.

## Puntos clave

- El favicon es un archivo estático (`static/favicon.svg`), servido por HTTP y referenciado por una etiqueta `<link rel="icon">` normal — no una URI de datos SVG insertada.
- `/favicon.ico`, la ruta que los navegadores solicitan por convención sin importar lo que declare el `<head>`, redirige al mismo archivo SVG estático.
- Una sola marca sirve a cada inquilino. No existe distinción proveedor/cliente, cuadrado/círculo, ni azul acero/azul Woodfine en la construcción actual.

## El mecanismo

La plantilla de página de `app-mediakit-knowledge` enlaza el icono en el `<head>`:

```html
<link rel="icon" type="image/svg+xml" href="/static/favicon.svg">
```

El servidor también registra una ruta `/favicon.ico` que redirige al mismo archivo, de modo que los navegadores y rastreadores que solicitan esa ruta exacta por convención (independientemente de lo que declare el `<head>`) igualmente resuelven al icono real en lugar de un 404.

## La marca

El icono es un único SVG sin parametrizar: una base cuadrada redondeada azul marino (`#1a4480`) con un glifo de documento blanco. No varía por inquilino, despliegue ni wiki — `documentation.pointsav.com`, `projects.woodfinegroup.com` y `corporate.woodfinegroup.com` sirven todos el archivo idéntico.

## Véase también

- [[design-system-substrate]] — el sustrato de sistema de diseño que define el lenguaje visual al que pertenecen estas marcas
- [[anti-homogenization-discipline]] — la disciplina editorial que preserva las voces de marca distintas junto a esta identidad visual
- [[disclosure-substrate]] — la arquitectura de comunicaciones salientes servida bajo la marca del cliente
