---
schema: foundry-doc-v1
type: topic
category: reference
slug: country-filter-chips
title: Selectores de Filtro por País
paired_with: country-filter-chips.md
state: authoritative
audience: vendor-public
bcsc_class: current-fact
language_protocol: DESIGN-COMPONENT
authored: 2026-04-30
---

# Selectores de Filtro por País (Country Filter Chips)

El componente "Country Filter Chip" es una primitiva de navegación especializada diseñada para conjuntos de datos geográficos multijurisdiccionales. Permite a los usuarios ejecutar cortes de datos globales o específicos por país a través de una interfaz de selección exclusiva, filtrando simultáneamente las características del mapa y recentrando la ventana de visualización en los límites nacionales de destino.

## Resumen Ejecutivo

Las superficies de mapas de Foundry utilizan los Selectores de Filtro por País para facilitar una segmentación geográfica rápida. Al proporcionar un grupo de radio horizontal de activadores específicos de la jurisdicción —incluyendo un estado "ALL" (TODO) por defecto— el componente permite a los usuarios navegar por conjuntos de datos globales complejos con una sola interacción. Cada selección activa una transición automática de la ventana de visualización (fly-to) a la extensión geográfica del país respectivo, garantizando que los datos relevantes se prioricen y enmarquen de inmediato.

## Directrices de Uso

### Escenarios de Implementación
- **Mapas de Inteligencia Global**: Sirve como el filtro principal para datos basados en la ubicación que abarcan varios países (p. ej., US, CA, MX, ES).
- **Paneles de Cartera**: Previsto para su uso en paneles específicos del cliente para segmentar activos por jurisdicción operativa.
- **Divulgación Regulatoria**: Destinado a superficies que requieran vistas jurisdiccionales específicas de la BCSC o la UE.

### Restricciones
El componente está optimizado para la selección exclusiva (radiogroup). No debe utilizarse para alternar capas de datos individuales o para cambiar entre modos de vista completamente diferentes, que son manejados por los componentes Checkbox (Casilla de verificación) y Content Switcher (Selector de contenido) respectivamente.

## Especificaciones Técnicas

### Anatomía y Composición
- **Identificador Visual**: Cada selector muestra un código de país ISO 3166-1 alpha-2, opcionalmente emparejado con un icono de bandera suplementario.
- **Retroalimentación de Estado**: Los estados seleccionados se comunican mediante una combinación de color de fondo, grosor de borde y atributos ARIA semánticos.
- **Contenedor**: Una fila horizontal que admite el desplazamiento por desbordamiento cuando el número de selectores jurisdiccionales supera los ocho.

### Modelo de Interacción
- **Lógica de Selección**: Al activar un selector se deseleccionan todos los demás. La selección activa un evento de filtro de datos y una animación de la ventana de visualización de 700ms con curva cubic-bezier.
- **Navegación por Teclado**: El grupo es accesible mediante Tab, con navegación mediante teclas de flecha que admite el movimiento del foco entre selectores individuales.
- **Optimización Táctil**: Cada selector mantiene un objetivo de pulsación mínimo de 44px para cumplir con las recomendaciones WCAG 2.2 AAA para interfaces táctiles.

## Accesibilidad y Cumplimiento
El componente cumple con los requisitos WCAG 2.2 AA para controles interactivos:
- **Roles Semánticos**: Utiliza `role="radiogroup"` y `role="radio"` con estados `aria-checked`.
- **Nombres Accesibles**: Todos los iconos son suplementarios; el código ISO representado proporciona el nombre accesible principal.
- **Contraste Visual**: Los estados seleccionados mantienen una relación de contraste mínima de 4.5:1 (AA) con planes de avanzar hacia 7:1 (AAA) en futuras iteraciones del sistema de diseño.

## Tokens de Diseño (DTCG)

| Token | Valor | Descripción |
| :--- | :--- | :--- |
| `ps.chip.height` | 36px | Altura estándar del selector |
| `ps.chip.border-radius` | 18px | Radio de píldora completo |
| `ps.chip.bg.selected` | brand-primary | Fondo de selección activa |
| `ps.chip.fg.selected` | text-on-brand | Color de texto de selección activa |

## Hoja de Ruta Estratégica
Las mejoras futuras prevén incluir:
- **Agrupación Geográfica**: Se está investigando si la agrupación continental (p. ej., "Américas", "Europa") proporciona una mejor usabilidad para conjuntos de datos que abarcan más de diez países.
- **Variante Multiselección**: Una variación planificada que utiliza `role="group"` y `aria-pressed` para permitir la composición de datos entre países.
