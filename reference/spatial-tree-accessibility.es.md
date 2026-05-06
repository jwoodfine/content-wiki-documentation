---
schema: foundry-doc-v1
type: topic
slug: spatial-tree-accessibility
title: Accesibilidad del Árbol Espacial (Spatial Tree)
audience: vendor-public
bcsc_class: current-fact
language: es
paired_with: spatial-tree-accessibility.md
---


El componente `bim-spatial-tree` permite navegar por la jerarquía espacial de un edificio. Su diseño sigue las mejores prácticas de WAI-ARIA para asegurar que las estructuras arquitectónicas complejas sean accesibles para todos los usuarios.

## Estructura y Roles ARIA

El árbol utiliza un marcado semántico estricto:
- **Contenedor:** `<aside aria-label="Jerarquía espacial">`.
- **Raíz:** `<ul role="tree">`.
- **Nodos:** `<li role="treeitem">` con el atributo `aria-expanded` para indicar el estado de expansión.
- **Grupos de hijos:** `<ul role="group">` para niveles anidados.

Por convención de la industria AEC, las plantas del edificio están expandidas por defecto (`aria-expanded="true"`), mientras que los espacios individuales permanecen colapsados para evitar el exceso de información visual.

## Interacción de Teclado

El Árbol Espacial permite una navegación completa sin ratón:
- **Flechas Arriba/Abajo:** Navegar entre elementos visibles.
- **Flecha Derecha:** Expandir el nodo o ir al primer hijo.
- **Flecha Izquierda:** Colapsar el nodo o ir al padre.
- **Enter / Espacio:** Seleccionar el elemento enfocado.
- **Barra inclinada (/):** Mover el foco directamente al campo de búsqueda de espacios.

## Búsqueda y Filtrado

El componente incluye una entrada de búsqueda que filtra por el nombre de `IfcSpace`. Al encontrar coincidencias, el árbol expande automáticamente la ruta hacia el resultado y oculta las ramas que no coinciden, facilitando la localización rápida de activos dentro del modelo.


---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™ y Totebox Archive™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos titulares.*
