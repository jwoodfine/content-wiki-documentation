---
schema: foundry-doc-v1
type: topic
slug: viewport-3d-accessibility
title: Accesibilidad del Visor 3D (3D Viewport)
audience: vendor-public
bcsc_class: current-fact
language: es
paired_with: viewport-3d-accessibility.md
---

# Accesibilidad del Visor 3D (3D Viewport)

El componente `bim-viewport-3d` es la capa principal de visualización de modelos. Aunque el contenido de un lienzo (canvas) 3D es gráfico por naturaleza, el visor de Foundry está diseñado para ser plenamente operativo mediante la sincronización con componentes de texto y el uso de atajos de teclado estándar.

## Sincronización de Selección

La interacción es bidireccional para garantizar la accesibilidad:
- Al seleccionar un elemento en el lienzo 3D, el nombre y las propiedades del objeto se anuncian y muestran en el `PropertiesPanel`.
- Al navegar por el `SpatialTree`, la cámara del visor se ajusta automáticamente para resaltar el elemento seleccionado.

## Control por Teclado Paritario

El visor implementa los atajos estándar de la industria AEC para permitir el control total sin ratón:
- **Teclas 1 al 6:** Cambiar la vista a los ejes ±X, ±Y, ±Z (Planta, Alzado, etc.).
- **Tecla F:** Ajustar la vista al elemento seleccionado (Fit).
- **Flechas:** Desplazar (Pan) o rotar (Orbit) la cámara.
- **Teclas + / -:** Zoom de acercamiento o alejamiento.
- **Tecla S:** Activar o desactivar el plano de sección.

## Postura Técnica

En el **Modo Console**, el visor puede mostrar miniaturas SVG de alta fidelidad en lugar de un entorno 3D completo. Esto optimiza el rendimiento y mantiene la integridad de la licencia EUPL-1.2 en superficies de consulta. En el **Modo Workplace**, se activa el motor 3D completo para tareas de coordinación y autoría.


---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™ y Totebox Archive™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos titulares.*
