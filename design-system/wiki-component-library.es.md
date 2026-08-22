---
schema: foundry-doc-v1
title: "Biblioteca de componentes del wiki"
slug: wiki-component-library
short_description: "El armazón compartido — encabezado, navegación móvil fuera de lienzo, barra lateral izquierda y pie de página — más las plantillas de página que envuelve, que juntas renderizan cada página de la plataforma de conocimiento de PointSav."
category: design-system
type: topic
content_type: topic
index_group: wiki-surface-design
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: wiki-component-library.md
---

El wiki de PointSav se construye a partir de un pequeño conjunto de elementos de armazón compartido — encabezado, navegación móvil fuera de lienzo, barra lateral izquierda y pie de página — que envuelven una de varias plantillas de página, todo compuesto en el motor [[app-mediakit-knowledge]]. Los nombres de clase siguen un catálogo `k-*` compartido en todas las plantillas, de modo que estilizar una superficie estiliza todas.

---

## Armazón compartido

### Encabezado

Un encabezado blanco fijo (`k-header`) con tres regiones: el logotipo y la marca del sitio a la izquierda, un cuadro de búsqueda centrado, y un grupo de controles a la derecha — un botón de alternancia de tema claro/oscuro y un botón de menú que abre el panel de navegación móvil.

### Navegación móvil fuera de lienzo

Un panel lateral izquierdo (`k-nav-drawer`), no una barra de pestañas inferior. El botón de menú del encabezado lo abre como un diálogo modal (`role="dialog"`, `aria-modal="true"`) con una superposición que oscurece el fondo. Dentro, una copia móvil del cuadro de búsqueda se sitúa sobre tres secciones de enlaces — Navegar, Recursos y Red PointSav — cada una renderizada como una lista etiquetada. Un botón de cierre y la tecla Escape lo descartan.

### Barra lateral izquierda

Una única barra lateral fija (`k-sidebar`) en escritorio, no una disposición dividida izquierda/derecha. Apila, en orden: un enlace "Página principal", una lista de categorías "Explorar por área", un enlace "Guías" (en los wikis que ofrecen contenido de tipo how-to) y — sólo en páginas con encabezados — una tabla de contenidos construida a partir de los H2/H3 de la página. La tabla de contenidos forma parte de esta misma barra lateral, no es un componente separado en la columna derecha.

### Pie de página

Un pie de página de todo el sitio (`k-footer`), no uno por artículo. Tres columnas de enlaces — Explorar, Este sitio, Red — seguidas de una fila base: lista de ciudades y copyright a la izquierda, una insignia "Desarrollado con" a la derecha. Las etiquetas de categoría y las listas de referencias no son elementos del pie; cuando un artículo tiene notas al pie, se renderizan en línea dentro del cuerpo del artículo, como parte del mismo proceso de contenido que produce el resto de la prosa.

---

## Plantillas de página

Cada plantilla se envuelve en el armazón compartido anterior y rellena la región de contenido.

**Artículo** (`k-article`). Una barra de dos pestañas (Artículo / Historial), una línea opcional de "última actualización" o de revisión en un momento dado, un aviso opcional de revisión histórica al ver un commit pasado, el título H1 y el cuerpo de prosa renderizado.

**Historial** (`k-history`). La lista de revisiones del artículo — una entrada por commit, cada una enlazando a la diferencia de esa revisión.

**Diferencia**. La vista de cambios línea por línea de una revisión concreta, alcanzada desde la pestaña Historial.

**Página principal** (`k-home`). La entradilla del sitio, un recuento total de artículos, una cuadrícula de tarjetas de categoría "Explorar por área" y — donde existen guías — una lista de "Guías how-to".

**Índice de categoría / resultados de búsqueda / listados especiales** (`k-catpage`). Una plantilla compartida para cuatro vistas de listado distintas — los artículos de una categoría, los resultados de búsqueda, el índice completo de registro y los cambios recientes — que sólo difieren en el encabezado y la lista de origen.

**404** (variante de `k-catpage`). Una página de mensaje mínima envuelta en el armazón; el wiki nunca sirve un error desnudo.

No existe ningún componente de diálogo modal, ninguna paginación numerada entre artículos ni ninguna insignia de grado de calidad (Destacado/Bueno/Esbozo, etc.) en el conjunto de plantillas actual — ninguno de los tres existe en el motor.

---

## Búsqueda

La búsqueda se renderiza en el servidor, no es una API que el cliente invoque por separado: el cuadro de búsqueda del encabezado envía a `/search?q=`, que se renderiza mediante la misma plantilla `k-catpage` que un listado de categoría, con un recuento de resultados y una tarjeta por coincidencia.

---

## Disciplina móvil

La disciplina de área táctil se aplica a todos los elementos interactivos — los controles del encabezado, los enlaces de la barra lateral, los activadores del panel y los enlaces de pestaña tienen cada uno un área táctil mínima de 44 px × 44 px (WCAG 2.2 SC 2.5.8).

---

## Dependencia de tokens

Cada componente toma sus colores, espaciado y tipografía de los tokens semánticos `k-*` definidos en [[design-system-substrate|la bóveda de tokens]] — véase [[wiki-dark-mode]] para los pares de tokens de modo claro/oscuro y [[wiki-typography-system]] para la pila tipográfica. Ningún componente introduce un valor de color o dimensión propio sin pasar por un token.

---

## Véase también

- [[wiki-dark-mode]] — el botón de alternancia de tema en el encabezado y los tokens semánticos que intercambia cada modo
- [[wiki-typography-system]] — la pila tipográfica Inter/Source Serif 4 con la que renderizan estas plantillas
- [[design-system-substrate]] — la bóveda de tokens de la que se nutre cada componente
- [[app-mediakit-knowledge]] — el motor wiki que renderiza este armazón y estas plantillas
- [[component-recipes-vs-raw-tokens|Recetas de componentes frente a tokens en bruto]] — el registro de componentes propio del sistema de diseño, distinto de este armazón de superficie wiki
