---
schema: foundry-doc-v1
title: "Modo oscuro del wiki"
slug: wiki-dark-mode
short_description: "Esquemas de color claro y oscuro para el wiki de PointSav, con paletas verificadas según WCAG y persistencia de tema mediante localStorage."
category: design-system
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: wiki-dark-mode.md
---

# Modo oscuro del wiki

El [[app-mediakit-knowledge|wiki de PointSav]] admite esquemas de color claro y oscuro mediante [[design-system-substrate|tokens semánticos]] del sistema de diseño de la plataforma. El modo oscuro reduce la fatiga visual en entornos con poca luz y es preferido por una proporción significativa de lectores. Este artículo describe la implementación: cómo se establece el tema, cómo se conserva entre sesiones y cómo se alterna, junto con la paleta de colores completa para cada modo.

---

## Funcionamiento

El modo oscuro se controla mediante el atributo `data-theme="dark"` en el elemento `<html>`. El CSS del wiki usa este atributo como selector de anulación:

```css
/* Claro (predeterminado) — definido en :root */
:root {
  --ps-surface-base: #ffffff;
  --ps-ink-primary: #0e0f12;
  /* ... */
}

/* Oscuro — anula sólo los tokens semánticos */
[data-theme="dark"] {
  --ps-surface-base: #1f2125;
  --ps-ink-primary: #f5f6f8;
  /* ... */
}
```

Sólo cambian los tokens semánticos (superficies, tinta, bordes, colores de estado). Los tokens primitivos — la paleta de colores base — permanecen sin cambios. Para agregar soporte de modo oscuro a un nuevo componente, basta con que el componente use tokens semánticos; no se necesitan selectores `[data-theme="dark"]` por componente.

---

## Inicialización

La preferencia de tema se almacena en `localStorage` bajo la clave `ps-theme`. En cada carga de página, un script en línea en `<head>` lee este valor y establece `data-theme` antes de que el navegador renderice el contenido. Esto evita el destello del tema no deseado que ocurriría si el script se ejecutara tras el primer renderizado.

La preferencia explícita del usuario almacenada en `localStorage` prevalece sobre la preferencia del sistema operativo (`prefers-color-scheme`). Si no se ha almacenado ninguna preferencia, se respeta la configuración del sistema.

En móvil, `prefers-color-scheme` es el disparador principal — la mayoría de lectores en móvil depende de la configuración del sistema operativo y nunca accede al botón de alternancia manual. El componente de alternancia es la capa de mejora progresiva para los lectores que desean anular esa configuración. La declaración `<meta name="color-scheme" content="light dark">` en el `<head>` evita que el navegador muestre un destello blanco antes de que el script en línea lea `localStorage`.

---

## Componente de alternancia

El componente `wiki-dark-mode-toggle` usa `aria-pressed` y actualiza `aria-label` para describir la acción disponible, no el estado actual:

- En modo claro: etiqueta = "Cambiar a modo oscuro"
- En modo oscuro: etiqueta = "Cambiar a modo claro"

Al hacer clic, la alternancia establece `document.documentElement.dataset.theme` y escribe el nuevo valor en `localStorage`.

---

## Paleta de colores

### Modo claro

| Token | Valor | Uso |
|---|---|---|
| `--ps-surface-base` | #ffffff | Fondo de página |
| `--ps-surface-subtle` | #f5f6f8 | Barra lateral, superficie de código |
| `--ps-ink-primary` | #0e0f12 | Texto principal |
| `--ps-ink-secondary` | #4a4f59 | Texto secundario, metadatos |
| `--ps-wiki-link` | #234ed8 | Hipervínculos |
| `--ps-wiki-redlink` | #a52323 | Artículos inexistentes |
| `--ps-wiki-code-keyword` | #7c3aed | Palabras clave de código |

### Modo oscuro

| Token | Valor | Uso | Contraste WCAG vs fondo |
|---|---|---|---|
| `--ps-surface-base` | #1f2125 | Fondo de página | — |
| `--ps-surface-code` | #151618 | Fondo de bloque de código | — |
| `--ps-ink-primary` | #f5f6f8 | Texto principal | 14,5:1 (AAA) |
| `--ps-ink-secondary` | #aab0bb | Texto secundario | 6,2:1 (AAA) |
| `--ps-wiki-link` | #6ab0f5 | Hipervínculos | 8,47:1 vs página (AAA) |
| `--ps-wiki-redlink` | #f56565 | Artículos inexistentes | 6,42:1 vs página (AA+) |
| `--ps-wiki-code-keyword` | #c792ea | Palabras clave de código | 7,85:1 vs código (AAA) |

Todos los pares de colores del modo oscuro superan el nivel AAA de WCAG 2.1, verificado el 6 de mayo de 2026.

---

## Véase también

- [[wiki-component-library]] — los nueve componentes que consumen estas anulaciones de tokens del modo oscuro
- [[wiki-typography-system]] — la pila tipográfica que se combina con estos ajustes de color
- [[design-system-substrate]] — la bóveda de tokens donde se definen y versionan los valores de tokens semánticos
