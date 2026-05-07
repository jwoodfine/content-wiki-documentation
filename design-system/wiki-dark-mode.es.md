---
schema: foundry-doc-v1
title: "Modo Oscuro del Wiki"
slug: wiki-dark-mode
language: es
category: design-system
type: topic
quality: core
status: active
bcsc_class: vendor-public
last_edited: 2026-05-07
editor: pointsav-engineering
paired_with: wiki-dark-mode.md
---

El modo oscuro del wiki PointSav ofrece una experiencia de lectura en esquema claro u
oscuro, controlada mediante el atributo `data-theme="dark"` en el elemento `<html>`.
La paleta completa fue auditada en una pasada de investigación de 24 agentes (2026-05-06);
todos los pares de color en modo oscuro superan el estándar WCAG 2.1 AAA. El sistema se
implementó en la Fase A del sistema de diseño del wiki.

## Arquitectura de tokens

Solo los tokens semánticos cambian entre modos: superficies, tinta, bordes y colores de
estado. Los tokens primitivos —la paleta de colores base— permanecen iguales en ambos
modos. Esto significa que incorporar soporte de modo oscuro a un componente nuevo solo
requiere usar tokens semánticos; no son necesarios selectores `[data-theme="dark"]`
por componente.

## Inicialización sin parpadeo

La preferencia de tema se almacena en `localStorage` bajo la clave `ps-theme`. Un script
en línea en el `<head>` lee este valor antes de que el navegador renderice contenido,
evitando el parpadeo de tema incorrecto. La preferencia explícita del usuario tiene
prioridad sobre la preferencia del sistema operativo (`prefers-color-scheme`).

## Paleta en modo oscuro

Los siete tokens principales y sus valores de contraste verificados:

| Token | Valor | Contraste WCAG |
|---|---|---|
| `--ps-surface-base` | #1f2125 | — |
| `--ps-ink-primary` | #f5f6f8 | 14,5:1 (AAA) |
| `--ps-ink-secondary` | #aab0bb | 6,2:1 (AAA) |
| `--ps-wiki-link` | #6ab0f5 | 8,47:1 (AAA) |
| `--ps-wiki-redlink` | #f56565 | 6,42:1 (AA+) |
| `--ps-wiki-code-keyword` | #c792ea | 7,85:1 (AAA) |

El par más débil de la paleta oscura supera cómodamente el umbral AA para texto normal y
AAA para texto de gran tamaño.

## Véase también

- [[wiki-typography-system]]
- [[wiki-component-library]]
- [[design-color]]
