---
schema: foundry-doc-v1
title: "Matriz de favicons e identidad de pestaña"
slug: favicon-matrix.es
category: governance
type: topic
content_type: topic
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

## Puntos clave

- Incluir el SVG como URI de datos en el elemento `<link rel="icon">` elimina la llamada de red para el archivo del icono. La identidad de la pestaña se establece antes de que se cargue cualquier otro recurso — no se emite ninguna solicitud HTTP adicional para el favicon.
- La geometría vectorial escala sin pixelación entre densidades de pantalla. La misma marca de unos pocos cientos de bytes es nítida en una pantalla de baja densidad y en un monitor externo de alta densidad. No se requieren variantes de activo con sufijo retina.
- Dos marcas están en uso: cuadrado azul acero (`#869FB9`) para propiedades servidas por PointSav (documentación, sistema de diseño, wikis del proveedor) y círculo azul Woodfine (`#164679`) para propiedades servidas por Woodfine (carteras de proyectos, divulgaciones corporativas, wikis del cliente). La asignación es inequívoca: cuadrado = proveedor, círculo = cliente.
- La distinción geométrica entre cuadrado y círculo se preserva independientemente del color. Un lector con visión cromática reducida puede identificar qué propiedad tiene abierta en cada pestaña sin depender exclusivamente de la diferencia de color.

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
| Cliente | Azul Woodfine (`#164679`) | Círculo | Propiedades servidas por Woodfine: carteras de proyectos, [[disclosure-substrate|divulgaciones corporativas]], wikis del lado del cliente. |

Un lector que tenga abiertos sitios del proveedor y del cliente en pestañas adyacentes del navegador puede identificar la fuente de cada pestaña sin leer el título. La distinción geométrica (cuadrado frente a círculo) se preserva cuando la visión del color está reducida.

## Véase también

- [[design-system-substrate]] — el sustrato de sistema de diseño que define el lenguaje visual al que pertenecen estas marcas
- [[anti-homogenization-discipline]] — la disciplina editorial que preserva las voces de marca distintas junto a esta identidad visual
- [[disclosure-substrate]] — la arquitectura de comunicaciones salientes servida bajo la marca del cliente
