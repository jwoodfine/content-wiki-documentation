---
schema: foundry-doc-v1
title: "Modo oscuro del wiki"
slug: wiki-dark-mode
short_description: "Esquemas de color claro y oscuro para el wiki de PointSav, controlados por anulaciones de tokens semánticos sobre un atributo data-theme, con persistencia de tema mediante localStorage."
category: design-system
type: topic
content_type: topic
index_group: wiki-surface-design
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: TRANSLATE-ES
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: wiki-dark-mode.md
---

El [[app-mediakit-knowledge|wiki de PointSav]] admite esquemas de color claro y oscuro mediante [[design-system-substrate|tokens semánticos]] del sistema de diseño de la plataforma. El modo oscuro reduce la fatiga visual en entornos con poca luz y es preferido por una proporción significativa de lectores. Este artículo describe la implementación: cómo se establece el tema, cómo se conserva entre sesiones y cómo se alterna, junto con la paleta de colores completa para cada modo.

---

## Funcionamiento

El modo oscuro se controla mediante el atributo `data-theme="dark"` en el elemento `<html>`. El CSS del wiki usa este atributo como selector de anulación:

```css
/* Claro (predeterminado) — definido en :root */
:root {
  --k-surface: #ffffff;
  --k-ink: #202122;
  /* ... */
}

/* Oscuro — anula sólo los tokens semánticos */
:root[data-theme="dark"] {
  --k-surface: #101418;
  --k-ink: #e7e9ea;
  /* ... */
}
```

Sólo cambian los tokens semánticos (superficies, tinta, bordes, colores de estado). Los tokens primitivos — la paleta de colores base — permanecen sin cambios. Para agregar soporte de modo oscuro a un nuevo componente, basta con que el componente use tokens semánticos; no se necesitan selectores `[data-theme="dark"]` por componente.

---

## Inicialización

La preferencia de tema se almacena en `localStorage` bajo la clave `k-theme`. El script del chrome resuelve el tema inicial comprobando primero ese valor almacenado y recurriendo a la preferencia del sistema operativo (`prefers-color-scheme`) sólo cuando no se ha almacenado nada, y luego lo aplica estableciendo `data-theme` en la raíz del documento y actualizando el estado `aria-pressed` y la etiqueta del botón de alternancia. Se espera que quien integre este motor incluya además un fragmento equivalente en línea antes del renderizado, en `<head>`, para que el tema correcto se aplique antes del primer renderizado, en lugar de mostrar brevemente el tema incorrecto y corregirlo después.

Una elección explícita del usuario almacenada en `localStorage` prevalece sobre la preferencia del sistema operativo (`prefers-color-scheme`). Si no se ha almacenado ninguna elección, se respeta la preferencia del sistema.

En móvil, `prefers-color-scheme` es el disparador principal — la mayoría de lectores en móvil depende de la configuración del sistema operativo y nunca accede al botón de alternancia manual. El componente de alternancia es la capa de mejora progresiva para los lectores que desean anularla. La declaración `<meta name="color-scheme" content="light dark">` en el `<head>` evita que el navegador muestre un destello blanco antes de que el script en línea lea `localStorage`.

---

## Componente de alternancia

El control de tema (`.k-control--theme`) usa `aria-pressed` y actualiza `aria-label` para describir tanto la acción disponible como el estado actual — "Switch to dark theme (current: light)" y su inversa — en lugar de una etiqueta que sólo describa la acción. Al hacer clic, la alternancia establece `data-theme` en la raíz del documento y escribe el nuevo valor en `localStorage`.

---

## Paleta de colores

### Modo claro

| Token | Valor | Uso |
|---|---|---|
| `--k-surface` | #ffffff | Fondo de página |
| `--k-ink` | #202122 | Texto principal |
| `--k-ink-secondary` | (definido junto a `--k-ink`) | Texto secundario, metadatos |
| `--k-link` | (definido junto a `--k-ink`) | Hipervínculos |

### Modo oscuro

| Token | Valor | Uso |
|---|---|---|
| `--k-surface` | #101418 | Fondo de página |
| `--k-surface-sunken` | #171c22 | Aviso del sitio, pie de página |
| `--k-surface-raised` | #1b2027 | Cajón de navegación en móvil |
| `--k-ink` | #e7e9ea | Texto principal |
| `--k-ink-secondary` | #a6abb1 | Texto secundario |
| `--k-border` | #3a4149 | Bordes |
| `--k-link` | #7aa6f0 | Hipervínculos |
| `--k-link-hover` | #a3c1f5 | Estado de pasar el cursor sobre un hipervínculo |
| `--k-code-block-bg` | #2b303b | Fondo de bloque de código |

Los bloques de código permanecen oscuros en modo oscuro, con el resaltado de sintaxis cambiando a su propia paleta oscura en lugar de seguir los mismos tokens que el texto de prosa. Existen dos anulaciones específicas por instancia para los despliegues `documentation` y `projects`/`corporate`, que ajustan el color de acento mientras el resto de la paleta oscura permanece compartida.

### Alias de superficie del wiki

El CSS del wiki nombra sus superficies semánticas directamente, sin una capa
separada de alias abreviados — `--k-surface`, `--k-ink`, `--k-link` y el resto
son los nombres que usan los componentes. No existe una segunda capa de
nomenclatura `--color-*` sobre ellos.

---

## Véase también

- [[theming-via-semantic-tokens|Tematización mediante tokens semánticos]] — el contexto conceptual de este artículo: por qué la tematización es sustitución de tokens semánticos y no una hoja de estilos paralela, y cómo aparece el mismo patrón en Carbon, Material 3 y Radix
- [[wiki-component-library]] — los nueve componentes que consumen estas anulaciones de tokens del modo oscuro
- [[wiki-typography-system]] — la pila tipográfica que se combina con estos ajustes de color
- [[design-system-substrate]] — la bóveda de tokens donde se definen y versionan los valores de tokens semánticos
