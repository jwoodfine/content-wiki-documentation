---
schema: foundry-doc-v1
title: "Matriz de favicons e identidad de pestaña"
slug: favicon-matrix.es
category: governance
type: topic
quality: complete
short_description: "La plataforma utiliza URIs de datos SVG insertados para los favicons de pestaña del navegador — eliminando una llamada de red, escalando sin pixelación en cualquier pantalla y asignando dos marcas distintas para que la entidad detrás de cada pestaña sea inequívoca a primera vista."
status: active
bcsc_class: no-disclosure-implication
last_edited: 2026-05-08
editor: pointsav-engineering
paired_with: favicon-matrix.md
---

La plataforma utiliza URIs de datos SVG insertados para los favicons de pestaña del navegador — eliminando una llamada de red para el archivo del icono, escalando sin pixelación en cualquier pantalla y asignando dos marcas distintas para que la entidad detrás de cada pestaña del navegador sea inequívoca a primera vista. Los sitios del proveedor llevan un cuadrado azul acero; los sitios del cliente llevan un círculo azul Woodfine. Las marcas se codifican directamente en el `<head>` de la página, de modo que la identidad de la pestaña se establece antes de que se cargue cualquier otro recurso.

Este artículo describe la justificación de ingeniería y la asignación de marcas por entidad.

## Justificación de ingeniería

Incluir el SVG insertado en el elemento `<link rel="icon">` como URI de datos codificado en URL ofrece dos propiedades prácticas:

- **Cero solicitudes HTTP.** No hay llamada de red para un archivo de icono. El favicon se analiza desde el `<head>` de la página y se renderiza de inmediato. La identidad de la pestaña se establece en el primer pintado.
- **Renderizado independiente de la resolución.** La geometría vectorial escala sin pixelación, por lo que el mismo icono es nítido en una pantalla portátil de baja densidad y en un monitor externo de alta densidad. No se requieren variantes de activo con sufijo retina.

El coste es un pequeño aumento de carga por página (unos cientos de bytes de SVG insertado). El beneficio — un primer pintado más rápido y una única ruta canónica de activo — vale la compensación.

## Asignación de marcas por entidad

Dos marcas están en uso en todas las páginas servidas por la plataforma:

| Marca | Color | Forma | Identifica |
|---|---|---|---|
| Proveedor | Azul acero (`#869FB9`) | Cuadrado | Propiedades servidas por PointSav: documentación, sistema de diseño, wikis del lado del proveedor. |
| Cliente | Azul Woodfine (`#164679`) | Círculo | Propiedades servidas por Woodfine: carteras de proyectos, divulgaciones corporativas, wikis del lado del cliente. |

Un lector que tenga abiertos sitios del proveedor y del cliente en pestañas adyacentes del navegador puede identificar la fuente de cada pestaña sin leer el título. La distinción geométrica (cuadrado frente a círculo) se preserva cuando la visión del color está reducida.

## Véase también

- [[design-system-substrate]]
- [[design-typography]]
- [[anti-homogenization-discipline]]
