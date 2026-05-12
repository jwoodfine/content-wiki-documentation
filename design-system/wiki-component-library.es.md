---
schema: foundry-doc-v1
title: "Biblioteca de Componentes del Wiki"
slug: wiki-component-library
language: es
category: design-system
type: topic
quality: core
status: active
bcsc_class: vendor-public
last_edited: 2026-05-07
editor: pointsav-engineering
paired_with: wiki-component-library.md
---

La biblioteca de componentes del wiki PointSav define nueve unidades de interfaz
reutilizables que juntas renderizan una página de artículo completa. Cada componente
aplica el patrón visual de Wikipedia —reconocible por millones de lectores— mientras
incorpora los estándares modernos de accesibilidad y el sistema de tokens PointSav.
Todos los componentes usan exclusivamente propiedades CSS personalizadas definidas en
`dist/tokens.css`; ningún componente introduce valores de color o dimensión directos.
La biblioteca fue especificada en una pasada de investigación de 24 agentes (2026-05-06).

## Los nueve componentes

**wiki-article-header** — Superficie superior del artículo. Renderiza: ruta de
navegación (breadcrumb), título H1 desde el frontmatter, distintivo de calidad opcional
y línea de autoría con fecha y enlace al historial.

**wiki-article-footer** — Superficie inferior. Tres secciones: enlaces de etiquetas de
categoría, lista numerada de referencias con retro-enlaces en el artículo, y enlace de
edición en GitHub para colaboradores.

**wiki-toc-sidebar** — Barra lateral derecha con los encabezados H2 y H3 del artículo,
en posición `sticky` en escritorio. En móvil colapsa a un `<details>`/`<summary>`
en línea. La sección activa se resalta mediante `IntersectionObserver` con `aria-current`.

**wiki-search-results** — Lista ordenada de resultados de búsqueda (motor Tantivy).
Muestra título del artículo y extracto de ~180 caracteres. Implementa `aria-live="polite"`
para anunciar actualizaciones a lectores de pantalla. Sin HTML en los extractos.

**wiki-modal-dialog** — Superposición con el elemento nativo `<dialog>` y `showModal()`.
Proporciona trampa de foco nativa. Se usa para lightboxes de imágenes, búsqueda y
confirmaciones. Se cierra con Escape o clic en el fondo.

**wiki-dark-mode-toggle** — Botón que establece `data-theme="dark"` en `<html>` y
persiste la preferencia en `localStorage`. Ver [[wiki-dark-mode]] para la paleta completa.

**wiki-badge-tag** — Chip de doble uso: distintivo de calidad del artículo (no
interactivo, con `aria-label`) y etiquetas de categoría (enlaces `<a>`).

**wiki-pagination** — Navegación anterior/siguiente dentro de una categoría. Cuadrícula
de tres columnas con atributos `rel="prev"` / `rel="next"` para SEO. Un componente de
paginación numérica para índices de categorías está previsto para una versión futura.

**wiki-drawer-mobile-nav** — Panel de navegación deslizante para pantallas compactas
(≤799px). Aplica el atributo `inert` al contenido principal al abrirse, confinando el
foco de teclado al panel. Soporte nativo en Chrome 102+, Firefox 112+, Safari 15.5+.

## Véase también

- [[wiki-dark-mode]]
- [[wiki-typography-system]]
- [[design-primitive-vocabulary]]
