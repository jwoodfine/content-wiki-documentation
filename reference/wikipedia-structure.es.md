---
schema: foundry-doc-v1
title: "Estructura de Wikipedia — Referencia para Colaboradores"
slug: wikipedia-structure.es
category: reference
type: reference
quality: core
short_description: "Anatomía de artículos y estructura de la página principal de Wikipedia, con orientación de adaptación para colaboradores de documentation.pointsav.com."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
paired_with: wikipedia-structure.md
---

Wikipedia es la convención de documentación más interiorizada del mundo. Cualquier persona que haya utilizado Wikipedia durante un tiempo lleva un modelo inconsciente de dónde vive la información en una página: el resumen ejecutivo al inicio, el recuadro de datos a la derecha, las referencias al pie. `documentation.pointsav.com` adopta las mismas convenciones estructurales para que los lectores lleguen ya sabiendo cómo utilizarla.

## Por qué la memoria muscular del lector importa

Cuando un lector abre un artículo de PointSav y reconoce la misma estructura que en Wikipedia — párrafo de apertura conciso, tabla de contenidos, sección "Véase también" antes de las referencias — no necesita aprender cómo navegar la página. Ese reconocimiento inmediato reduce la fricción y genera confianza en el contenido.

Lo opuesto también es cierto: una wiki donde cada artículo tiene una estructura diferente obliga al lector a reaprender la navegación en cada visita. La consistencia no es un detalle estético; es un elemento funcional de la experiencia del lector.

## Los tres elementos clave

**Párrafo de apertura como resumen ejecutivo.** Wikipedia exige que el párrafo de apertura responda, en orden: ¿Qué es esto? ¿Por qué importa? ¿Cuándo y dónde aplica? El cuarenta por ciento de los lectores de Wikipedia lee únicamente ese primer párrafo. Los artículos de PointSav siguen la misma disciplina.

**Señales de calidad visibles.** Wikipedia usa insignias de calidad (Artículo Destacado, Artículo Bueno) que los lectores aprenden a reconocer como indicadores de confianza. PointSav usa tres niveles: Complete (verde), Core (azul) y Stub (amarillo), registrados en el campo `quality:` del encabezado de cada artículo.

**Navegación consistente.** Wikipedia entrena a los lectores para encontrar elementos en ubicaciones fijas: la barra lateral siempre a la izquierda, "Véase también" siempre antes de "Referencias", las categorías siempre al pie. PointSav adopta el mismo orden para que el conocimiento adquirido en un artículo aplique a todos.

## Cómo usar este artículo

La versión completa en inglés ([wikipedia-structure.md](wikipedia-structure.md)) describe los nueve paneles de la página principal de Wikipedia, los dieciséis elementos de la anatomía de un artículo, las tres plantillas de recuadro de datos para documentación de PointSav (endpoint de API, función, integración), y el sistema de calificación de calidad.

Los colaboradores que escriban o editen artículos deben consultar ese artículo como referencia de estilo. Los tres elementos esenciales para el trabajo cotidiano son: escribir el párrafo de apertura como si fuera el único texto que el lector verá; usar el campo `quality:` con honestidad desde el primer commit; y mantener el orden estándar de secciones (cuerpo → Véase también → Referencias).
