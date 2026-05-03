---
schema: foundry-doc-v1
type: topic
category: reference
slug: brand-family-swatch
title: Muestrario de Familias de Marcas
paired_with: brand-family-swatch.md
state: authoritative
audience: vendor-public
bcsc_class: current-fact
language_protocol: DESIGN-COMPONENT
authored: 2026-04-30
---

# Muestrario de Familias de Marcas (Brand-Family Swatch)

El "Brand-Family Swatch" es la primitiva taxonómica principal para la clasificación de anclas comerciales en el ecosistema GIS de Foundry. Codifica la taxonomía tripartita ratificada por el operador —Department (Departamental), Hardware (Ferretería) y Warehouse Club (Club de Compras)— manteniendo una arquitectura agnóstica de datos que admite extensiones impulsadas por el cliente mediante capas de datos soberanas.

## Resumen Ejecutivo

Los sistemas de información geográfica de Foundry utilizan el Muestrario de Familias de Marcas para estandarizar la representación visual de las anclas comerciales. Al combinar un identificador codificado por colores con una etiqueta semántica, el componente garantiza una densidad de datos accesible en superficies de mapas, filtros tabulares y paneles de detalles. La arquitectura está desacoplada intencionalmente de la taxonomía específica; resuelve los identificadores de familia a través de una configuración JSON en tiempo de ejecución, lo que permite a los operadores modificar o ampliar las categorías de clasificación sin cambios en el código.

## Directrices de Uso

### Escenarios de Implementación
- **Marcadores de Mapa**: Funciona como la base visual para los marcadores de anclas, utilizando puntos codificados por colores para señalar la afiliación familiar.
- **Filtrado de Datos**: Sirve como la primitiva interactiva dentro de las filas de filtro (normalmente emparejada con una casilla de verificación).
- **Superposiciones de Detalles**: Proporciona categorización de alto nivel dentro de los paneles laterales y distintivos de encabezado.
- **Análisis de Conglomerados**: Emplea una variante de anillo concéntrico para representar la distribución familiar dentro de los conglomerados (clusters) agregados del mapa.

### Restricciones
El componente está reservado para la clasificación taxonómica. No debe utilizarse para indicadores de estado binarios, mensajes transitorios del sistema o etiquetas no taxonómicas, que son atendidos por los componentes Tag (Etiqueta) y Status Indicator (Indicador de Estado).

## Especificaciones Técnicas

### Anatomía y Composición
- **Indicador**: Un punto circular de 12px (predeterminado) o 24px (marcador) que utiliza tokens de color específicos de la familia.
- **Etiqueta**: Un nombre de visualización resuelto por la taxonomía (por ejemplo, "Warehouse Club").
- **Capa de Accesibilidad**: Un `aria-label` que combina la semántica del punto y la etiqueta, garantizando que el indicador visual esté oculto para los lectores de pantalla para evitar anuncios redundantes.

### Modelo de Interacción
El muestrario es nativamente estático. La interactividad se hereda de su contenedor principal (por ejemplo, un botón de filtro o una función de mapa). En las superficies de mapas, el componente admite un comportamiento de revelación por zoom: se prevé que los anillos de centroide de conglomerado se representen en niveles de zoom inferiores a 8.5, transicionando a muestrarios individuales en aumentos mayores.

## Accesibilidad y Cumplimiento
El componente está diseñado para cumplir con los estándares WCAG 2.2 AA:
- **Señalización Redundante**: El color nunca es el único canal de información; las etiquetas proporcionan el significado semántico principal.
- **Soporte de Alto Contraste**: En entornos de modo de alto contraste de Windows o `forced-colors`, el punto vuelve a los colores del sistema para enlaces mientras la etiqueta mantiene la integridad del texto.
- **Contraste de Luminancia**: Los tokens de color de la familia están validados para una relación de contraste mínima de 3:1 frente a mapas base tanto claros como oscuros.

## Tokens de Diseño (DTCG)

| Token | Valor | Descripción |
| :--- | :--- | :--- |
| `ps.swatch.dot.size` | 12px | Tamaño de punto en línea predeterminado |
| `ps.swatch.dot.size.marker` | 24px | Tamaño de variante de marcador de mapa |
| `ps.brand-family.department.color` | `#0B5FFF` | Azul azur |
| `ps.brand-family.hardware.color` | `#FF6B00` | Naranja construcción |
| `ps.brand-family.warehouse-club.color` | `#00875A` | Verde almacén |

## Hoja de Ruta Estratégica
Se prevé que las futuras iteraciones incluyan:
- **Rellenos con Patrones**: Soporte planificado para patrones geométricos dentro del punto para mejorar la distinción para usuarios con deficiencias avanzadas de visión cromática.
- **Gráficos de Tarta Dinámicos**: Se está investigando la transición del anillo de centroide de conglomerado a un gráfico de dona dinámico cuando la densidad del conglomerado supere las 10 anclas.
