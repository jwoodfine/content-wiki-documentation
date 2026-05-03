---
schema: foundry-doc-v1
type: topic
category: reference
slug: zoom-tier-reveal-pattern
title: Patrón de Revelación por Niveles de Zoom
paired_with: zoom-tier-reveal-pattern.md
state: authoritative
audience: vendor-public
bcsc_class: current-fact
language_protocol: DESIGN-RESEARCH
authored: 2026-04-30
---

# Patrón de Revelación por Niveles de Zoom (Zoom-Tier Reveal Pattern)

El "Zoom-Tier Reveal Pattern" es una estrategia fundamental de visualización geográfica que preserva la semántica de los datos a través de diferentes escalas de aumento. Al transicionar entre representaciones de conglomerados (clusters) agregados y marcadores de características individuales en umbrales de zoom definidos, el patrón garantiza que las señales de densidad de alto nivel sigan siendo tan informativas como los detalles granulares de cada ancla.

## Resumen Ejecutivo

Las superficies GIS de Foundry emplean el Patrón de Revelación por Niveles de Zoom para resolver el conflicto entre la densidad de datos y la legibilidad. El agrupamiento (clustering) estándar de mapas normalmente colapsa múltiples puntos en un recuento numérico genérico, sacrificando los datos cualitativos por el rendimiento. Por el contrario, el Patrón de Revelación por Niveles de Zoom utiliza una banda de transición —actualmente establecida entre los niveles de zoom 8.0 y 8.5— para realizar un desvanecimiento cruzado (crossfade) entre los anillos de centroide de conglomerado agregados (que muestran la distribución por familia de marcas) y los marcadores de anclas individuales. Esto garantiza que la taxonomía comercial permanezca visible y procesable en cada escala.

## Estrategia de Implementación

### Calibración de Umbrales
El umbral de transición se calibra en función de tres factores principales:
1.  **Separación Espacial**: El nivel de zoom en el que las anclas individuales ocupan suficiente espacio en pantalla para ser visualmente distintas.
2.  **Prioridad Semántica**: El punto en el que una señal de densidad regional (p. ej., "este corredor está dominado por Ferretería") se vuelve menos valiosa que la identificación de activos específicos.
3.  **Lógica de Desvanecimiento**: Se utiliza un intervalo de zoom de 0.5 puntos (8.0 a 8.5) para interpolar la opacidad entre capas, evitando el "salto" brusco asociado con la alternancia de umbrales rígidos.

### Composición de Capas
- **Bajo Aumento (< 8.0)**: Se prevé que solo se representen los anillos de centroide de conglomerado. Estos anillos utilizan una geometría concéntrica o de gráfico de tarta para representar la mezcla de familias de marcas dentro de un conglomerado de coubicación.
- **Banda de Transición (8.0 - 8.5)**: Ambas capas se representan con interpolaciones de opacidad inversas, facilitando una entrega visual fluida.
- **Alto Aumento (> 8.5)**: Se representan los muestrarios y marcadores de anclas individuales, mientras que el centroide agregado se suprime por completo.

## Especificaciones Técnicas (Integración con MapLibre)

El patrón se implementa mediante expresiones de pintura declarativas dentro del motor MapLibre GL JS. Al vincular la opacidad de la capa al estado de zoom del mapa mediante interpolación lineal, el sistema mantiene un alto rendimiento sin necesidad de oyentes de eventos manuales.

```javascript
// Ejemplo: Opacidad interpolada para centroides de conglomerados
'circle-opacity': [
  'interpolate', ['linear'], ['zoom'],
  8.0, 1.0,  // Totalmente opaco por debajo del umbral
  8.5, 0.0   // Totalmente transparente por encima del umbral
]
```

## Accesibilidad y Cumplimiento
- **Sensibilidad al Movimiento**: Para los usuarios con `prefers-reduced-motion: reduce` activado, se prevé que el desvanecimiento cruzado de 500ms se colapse en un intercambio de capas instantáneo para minimizar los desencadenantes vestibulares.
- **Navegación por Teclado**: El orden de Tabulación se actualiza dinámicamente a medida que los niveles de zoom cruzan el umbral, garantizando que solo los marcadores visibles sean alcanzables por teclado.
- **Continuidad Semántica**: Los centroides de los conglomerados se tratan como entidades de datos de primera clase (`role="graphics-symbol"`), lo que garantiza que los lectores de pantalla anuncien la densidad agregada como un resumen significativo en lugar de un artefacto de optimización.

## Hoja de Ruta Estratégica
Las investigaciones futuras prevén investigar:
- **Revelación Multitier**: Un sistema planificado de tres niveles (Regional → Conglomerado → Individual) para entornos urbanos de ultra alta densidad.
- **Umbrales Adaptativos**: Desarrollo previsto de umbrales dinámicos que se ajusten en función de la densidad de datos local, garantizando una claridad visual constante tanto en conjuntos de datos rurales como metropolitanos.
- **Rutas de Clic para Zoom**: Se está investigando si al hacer clic en un centroide de conglomerado se debe volar exactamente al umbral de revelación o a una vista de detalle de mayor aumento predefinida (p. ej., zoom 13).
