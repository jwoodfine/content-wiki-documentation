---
schema: foundry-doc-v1
type: topic
content_type: topic
index_group: brand-surface
slug: brand-typography
short_description: "Las superficies web de PointSav se renderizan en Inter, Source Serif 4 y Playfair Display, alojadas localmente en vez de depender de la pila de fuentes del sistema. Existe una matriz tipográfica OFL de impresión documentada por separado, sin canal de generación aún implementado."
title: Tipografía de marca y estándares de impresión
audience: vendor-public
bcsc_class: current-fact
language: es
paired_with: brand-typography.md
category: design-system
status: active
last_edited: 2026-08-22
editor: pointsav-engineering
---



La tipografía web y la de impresión se gobiernan por separado. La capa web —la wiki de documentación, la superficie de marketing— aloja localmente un conjunto fijo de fuentes en vez de recurrir a lo que ofrezca el sistema operativo del visitante, de modo que la misma página se lea de forma idéntica en cualquier dispositivo. La tipografía de impresión es una especificación aparte, actualmente aspiracional: una matriz de fuentes OFL documentada sin ninguna herramienta que la incorpore aún a un documento real.

## La capa web: fuentes alojadas localmente, no del sistema

`app-mediakit-knowledge`, el motor de la wiki, distribuye tres familias `.woff2` alojadas localmente — Inter para la interfaz y el cuerpo del texto, Source Serif 4 para lectura extensa y Playfair Display para encabezados destacados. Las tres se compilan como activos estáticos del motor y se sirven desde el mismo origen que la página; nada se obtiene de un CDN de fuentes ni de las fuentes instaladas en el sistema del visitante. Un visitante sin Inter instalada igual ve Inter.

## La matriz de impresión: documentada, aún no construida

Existe una especificación tipográfica aparte para salida impresa y en PDF —libros blancos, tablas financieras, divulgaciones formales—. Se construye sobre equivalentes con Licencia de Fuentes Abiertas SIL (OFL) de referencias propietarias:

| Token | Fuente activa | Referencia previa | Aplicación prevista |
| :--- | :--- | :--- | :--- |
| **serif_primary** | **Zilla Slab** | Caecilia LT Std | Marcas de confianza institucional (portadas de libros blancos). |
| **sans_condensed**| **Barlow Condensed** | Trade Gothic | Libros contables financieros y tablas de datos densas. |
| **sans_primary** | **Nunito Sans** | Avenir LT Std | Cuerpo de texto estándar y comunicaciones operativas. |

Estos nombres de fuente son tokens de diseño reales, definidos como cadenas de respaldo de propiedades CSS personalizadas en `templates/tokens.css` del monorepo. Ninguna herramienta de generación de PDF o compilación de documentos los consume actualmente — la matriz especifica qué debería usar un futuro canal de impresión, no un mecanismo activo que incorpore fuentes a PDFs en producción hoy.

## Resolución de Activos Digitales

El principio de licenciamiento de activos de la plataforma —todo activo embebido debe ser libremente distribuible— aplica tanto a las fuentes web ya distribuidas como a la matriz de impresión documentada. Todas las tipografías listadas son OFL, elegidas precisamente para que ninguna revisión de licencia bloquee a un futuro canal de impresión que las use.

## Véase también

- [[brand-family-swatch]]
- [[news-release-standards]]
