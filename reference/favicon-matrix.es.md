---
schema: foundry-doc-v1
type: topic
slug: favicon-matrix
title: Matriz de Favicon e Identidad de Pestañas
audience: vendor-public
bcsc_class: current-fact
language: es
paired_with: favicon-matrix.md
---

# Matriz de Favicon e Identidad de Pestañas

El sistema de Foundry utiliza URIs de datos SVG para la identificación de pestañas en el navegador, optimizando el rendimiento y la claridad visual.

## Lógica de Ingeniería

Al incrustar el SVG directamente en el encabezado HTML, logramos:
1. **Cero Peticiones HTTP:** Se elimina la necesidad de descargar archivos `.ico` externos.
2. **Escalado Infinito:** La naturaleza vectorial asegura nitidez total en pantallas de alta resolución.

## Identidad Visual

- **Proveedor (PointSav):** Cuadrado Azul Acero (`#869FB9`). Representa la infraestructura base.
- **Cliente (Woodfine):** Círculo Azul Woodfine (`#164679`). Representa la empresa operativa.

Este estándar garantiza una identidad de marca coherente y de carga instantánea en todas las aplicaciones de la plataforma.
