---
schema: foundry-doc-v1
title: "Biblioteca de componentes del wiki"
slug: wiki-component-library
short_description: "Nueve componentes reutilizables que componen una página completa de artículo wiki en la plataforma de conocimiento de PointSav."
category: design-system
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: wiki-component-library.md
---

# Biblioteca de componentes del wiki

La biblioteca de componentes del wiki de PointSav define nueve unidades de interfaz reutilizables que, en conjunto, renderizan una página completa de artículo wiki. Cada componente sigue las convenciones de disposición establecidas por Wikipedia, aplicando estándares de accesibilidad actuales y el sistema de tokens de PointSav.

---

## Visión general de la arquitectura

Una página de artículo wiki se compone mediante una pila de componentes:

```
┌─────────────────────────────────────────────────────┐
│  wiki-drawer-mobile-nav  (sólo dispositivos compactos)│
├─────────────────────────────────────────────────────┤
│  wiki-article-header  (miga de pan + H1 + insignia + metadatos)│
├──────────────────┬──────────────────────────────────┤
│                  │  wiki-toc-sidebar  (columna derecha)│
│  Cuerpo del      │  (sólo escritorio)               │
│  artículo        ├──────────────────────────────────┤
│  (prosa)         │  wiki-badge-tag (calidad/categoría)│
├──────────────────┴──────────────────────────────────┤
│  wiki-article-footer  (categorías + referencias + editar)│
├─────────────────────────────────────────────────────┤
│  wiki-pagination  (artículo anterior/siguiente)     │
└─────────────────────────────────────────────────────┘

Superposiciones (activadas por el usuario):
  wiki-modal-dialog     — visor de imágenes, búsqueda superpuesta
  wiki-dark-mode-toggle — cambio de tema persistente (encabezado del sitio)

Búsqueda:
  wiki-search-results   — lista de resultados (página propia o en modal)
```

---

## Componentes

### wiki-article-header

Superficie superior del artículo. Muestra cuatro elementos en secuencia: (1) miga de pan con la ruta de categoría del artículo, (2) el título H1 del artículo extraído del frontmatter, (3) una insignia de calidad opcional, y (4) una línea de autoría con la fecha de última edición y un enlace al historial.

Grados de calidad: Artículo destacado (dorado), Artículo bueno (verde), clase A (azul), clase B (azul claro), clase C (gris), Esbozo (gris claro). Los artículos sin clasificación omiten el espacio de la insignia.

**Token:** `--ps-wiki-text-h1` = 2,25 rem (36 px con base de 17 px).

---

### wiki-article-footer

Superficie inferior del artículo. Tres secciones: (1) enlaces de etiquetas de categoría, (2) una lista numerada de referencias usando `<ol id="ref-N">` con retroenlaces internos, y (3) un enlace "editar en GitHub" para colaboradores.

---

### wiki-toc-sidebar

Barra lateral derecha fija con los encabezados del artículo (H2 y H3). En escritorio (≥ 800 px) usa `position: sticky; top: 1rem`. En dispositivos compactos (≤ 799 px) se colapsa como un elemento interactivo `<details>` / `<summary>` por encima del cuerpo del artículo.

La sección activa se resalta mediante un `IntersectionObserver` de JavaScript que monitorea todos los anclajes de encabezado con atributo `[id]`. Cuando un encabezado entra en el área visible, su entrada en la tabla de contenidos recibe `aria-current="true"` y el estilo visual activo.

---

### wiki-search-results

Lista ordenada de resultados devueltos por el motor de búsqueda Tantivy. Cada resultado muestra el título del artículo como enlace y un fragmento de texto plano de aproximadamente 180 caracteres, truncado en límite de palabra. El componente incluye `aria-live="polite"` para que las tecnologías de asistencia anuncien actualizaciones en el número de resultados.

---

### wiki-modal-dialog

Superposición que usa el elemento nativo `<dialog>` con `showModal()`. El elemento dialog nativo proporciona un foco de teclado integrado: todo el contenido fuera del diálogo es inaccesible mediante teclado hasta que el diálogo se cierra. Se usa para visores de imágenes, búsqueda superpuesta y confirmaciones. Se cierra con Escape y al hacer clic en el fondo.

---

### wiki-dark-mode-toggle

Botón de alternancia que establece `data-theme="dark"` en `<html>` y persiste la preferencia en `localStorage` bajo la clave `ps-theme`. En cada carga de página, un script en línea lee este valor antes de que la hoja de estilos se renderice, evitando un destello del tema no deseado. Si no hay preferencia explícita, recurre a `prefers-color-scheme: dark`.

---

### wiki-badge-tag

Componente de doble función: (1) insignia de grado de calidad del artículo — un `<span>` no interactivo con `aria-label` que describe el grado completo — y (2) etiquetas de categoría como enlaces `<a>`. Se usa en el encabezado del artículo (insignia de calidad) y en el pie (etiquetas de categoría).

---

### wiki-pagination

Navegación de artículo anterior/siguiente dentro de una categoría. El componente es una cuadrícula de tres columnas: enlace al artículo anterior (izquierda), enlace al nombre de la categoría actual (centro), enlace al artículo siguiente (derecha). Cada enlace direccional incluye `rel="prev"` / `rel="next"` para SEO y un `aria-label` con el título completo del artículo adyacente.

---

### wiki-drawer-mobile-nav

Panel de navegación lateral que se desliza hacia dentro en dispositivos compactos (≤ 799 px). Un botón de menú hamburguesa abre el panel. Cuando está abierto, el atributo `inert` se aplica a la región de contenido principal y al encabezado, limitando el foco del teclado al interior del panel hasta que se cierre. Se cierra con Escape o al hacer clic en el fondo.

---

## Dependencia de tokens

Los nueve componentes usan exclusivamente el sistema de tokens de PointSav definido en `dist/tokens.css`. Ningún componente introduce valores brutos de color o dimensión. Las nuevas páginas y plantillas wiki incorporan componentes sin añadir nuevas variables CSS.

---

## Véase también

- [[wiki-dark-mode]]
- [[wiki-typography-system]]
- [[design-system-substrate]]
