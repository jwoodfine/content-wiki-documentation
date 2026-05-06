---
schema: foundry-doc-v1
type: topic
slug: properties-panel-accessibility
title: Accesibilidad del Panel de Propiedades
audience: vendor-public
bcsc_class: current-fact
language: es
paired_with: properties-panel-accessibility.md
## Véase también

- [[viewport-3d-accessibility]]
- [[spatial-tree-accessibility]]
- [[neurodiversity-typography-standards]]

---


El componente `bim-properties-panel` muestra los datos semánticos y de rendimiento de los elementos seleccionados. Su diseño está optimizado para presentar información técnica densa de manera clara y accesible para lectores de pantalla y usuarios de teclado.

## Estructura y Organización de Datos

- **Contenedor:** `<aside aria-label="Propiedades del elemento">`.
- **Secciones:** Cada conjunto de propiedades IFC (Pset o Qto) se organiza en un `<section>` con su propio encabezado `<h4>`.
- **Listas de Datos:** Se utilizan pares `<dt>` (término) y `<dd>` (valor) dentro de una lista de descripción `<dl>`.
- **Identificación:** La clase del elemento y su Identificador Global (GUID) se muestran de forma destacada para proporcionar contexto inmediato.

## Comportamiento según el Modo

El panel adapta su funcionalidad mediante la propiedad `data-mode`:
- **Modo Console:** Vista de solo lectura para consulta de datos.
- **Modo Workplace:** Los valores se transforman en controles editables (`<input>`, `<select>`), permitiendo la modificación de datos que se guardan en archivos "sidecar" YAML.

## Interacción de Teclado (Modo Workplace)

- **Tab / Shift-Tab:** Navegar entre los campos editables.
- **Enter:** Confirmar y guardar la edición.
- **Escape:** Cancelar y revertir al valor original.

## Recomendaciones de Implementación

Es obligatorio incluir una opción para "copiar al portapapeles" el GlobalID (GUID), ya que estos códigos de 22 caracteres son esenciales para las auditorías pero imposibles de transcribir manualmente.


---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™ y Totebox Archive™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos titulares.*
