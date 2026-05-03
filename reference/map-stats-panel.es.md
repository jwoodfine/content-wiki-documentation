---
schema: foundry-doc-v1
type: topic
category: reference
slug: map-stats-panel
title: Panel de Estadísticas de Mapa
paired_with: map-stats-panel.md
state: authoritative
audience: vendor-public
bcsc_class: current-fact
language_protocol: DESIGN-COMPONENT
authored: 2026-04-30
---

# Panel de Estadísticas de Mapa (Map Stats Panel)

El "Map Stats Panel" es un componente reactivo de visualización de datos que presenta estadísticas agregadas en tiempo real basadas en los filtros activos del mapa. Posicionado como una superposición flotante, proporciona a los usuarios visibilidad constante de los indicadores clave de rendimiento, como el recuento de anclas, la distribución jurisdiccional y las calificaciones de los conglomerados (clusters).

## Resumen Ejecutivo

Las superficies de mapas de Foundry utilizan el Panel de Estadísticas de Mapa para proporcionar un contexto cuantitativo inmediato a las visualizaciones geográficas. A medida que los usuarios manipulan los selectores de país o los filtros de familia de marcas, el panel se actualiza de forma reactiva para reflejar el subconjunto de datos actual. El componente está diseñado para una visibilidad persistente no intrusiva, normalmente anclado al margen superior derecho para evitar colisiones con los controles de navegación estándar del mapa.

## Directrices de Uso

### Escenarios de Implementación
- **Inteligencia de Ubicación**: Muestra recuentos agregados para corredores comerciales y anclas dentro de la ventana de visualización actual.
- **Paneles Ejecutivos**: Proporciona estadísticas de cartera de alto nivel (p. ej., calificación promedio del conglomerado) junto con las vistas de mapa.
- **Análisis Comparativo**: Previsto para su uso en la comparación federada de conglomerados para mostrar deltas agregados en paralelo.

### Restricciones
El panel es una pantalla de solo lectura. No debe utilizarse para activar filtros o navegación, que son manejados por los componentes de Selectores de Filtro por País y el Panel Lateral de Mapa.

## Especificaciones Técnicas

### Anatomía y Composición
- **Celdas de Datos**: Un diseño basado en cuadrícula (normalmente 2x2) que contiene valores numéricos de alto contraste y etiquetas semánticas compactas.
- **Contenedor**: Una tarjeta flotante con tokens de superficie elevados y esquinas redondeadas para distinguirla del fondo del mapa.
- **Densidad de la Cuadrícula**: Admite de 2 a 6 celdas estadísticas con ajustes adaptativos para diseños de varias columnas.

### Modelo de Interacción
- **Actualizaciones Reactivas**: Los valores se mantienen actualizados de forma asíncrona mediante anuncios `aria-live="polite"` cuando cambia el filtro de datos subyacente.
- **Posicionamiento**: Flota sobre el lienzo del mapa a un desplazamiento fijo (por defecto 16px) desde los bordes superior y derecho.
- **Retroalimentación Visual**: Se prevé que las transiciones entre valores utilicen un desvanecimiento de 200ms para evitar cambios bruscos de diseño durante el filtrado rápido.

## Accesibilidad y Cumplimiento
El componente está diseñado para cumplir con los estándares WCAG 2.2 AA:
- **Regiones Activas**: Implementa `aria-live="polite"` para garantizar que los usuarios de lectores de pantalla sean notificados de los cambios de datos sin interrupciones.
- **Emparejamiento Semántico**: Utiliza el marcado de lista de descripción (`<dt>` y `<dd>`) para mantener relaciones claras entre valor y etiqueta.
- **Unidades Accesibles**: Los valores numéricos utilizan atributos `aria-label` ocultos para proporcionar el contexto completo de la unidad (p. ej., "12 corredores" en lugar de solo "12").

## Tokens de Diseño (DTCG)

| Token | Valor | Descripción |
| :--- | :--- | :--- |
| `ps.map-stats.bg` | surface-elevated | Fondo para paneles flotantes |
| `ps.map-stats.value.font` | heading-04 | Tipografía para valores numéricos grandes |
| `ps.map-stats.label.font` | caption-01 | Tipografía para etiquetas compactas |
| `ps.map-stats.shadow` | shadow-floating | Señal de profundidad para superposiciones flotantes |

## Hoja de Ruta Estratégica
Las mejoras futuras prevén incluir:
- **Minigráficos (Sparklines)**: Soporte planificado para visualizaciones de datos compactas debajo de los valores numéricos para mostrar la distribución de calificaciones.
- **Auto-colapso Móvil**: Se está investigando el umbral de colapso óptimo para pantallas móviles para maximizar la visibilidad del mapa.
