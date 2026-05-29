---
schema: foundry-doc-v1
type: topic
category: design-system
slug: brand-family-swatch
short_description: "Las familias de color de marca asignadas a categorías de anclaje minoristas e institucionales en la superficie GIS de co-ubicación de la plataforma, proporcionando identificadores codificados por color consistentes para visualización de mapas y datos tabulares en modos de visualización accesible y estándar."
title: Muestrario de familias de marcas
paired_with: brand-family-swatch.md
state: authoritative
status: active
audience: vendor-public
bcsc_class: current-fact
language_protocol: DESIGN-COMPONENT
authored: 2026-04-30
last_edited: 2026-05-25
---

El muestrario de familias de marca es el componente de clasificación visual que la [[app-orchestration-gis|superficie GIS de la plataforma]] utiliza para identificar categorías de anclas comerciales — Departamental, Ferretería y Club de Compras — en mapas, filas de filtros y paneles de detalle, como parte de la [[location-intelligence-platform|plataforma de inteligencia de ubicación]]. Combina un punto codificado por color con una etiqueta semántica para que la membresía de categoría sea legible de un vistazo sin depender únicamente del color, apoyando la visualización de niveles de la [[co-location-methodology|metodología de co-ubicación]]. El componente está diseñado para ser agnóstico respecto a la taxonomía: los identificadores de familia se resuelven a través de una configuración en tiempo de ejecución, por lo que los operadores pueden ampliar o reclasificar categorías de anclas sin cambios en el código.

## Representación visual

La superficie GIS de la plataforma utiliza el muestrario de familias de marca para estandarizar la apariencia de las anclas comerciales en marcadores de mapa, filtros tabulares y paneles de detalle. Un identificador codificado por color combinado con una etiqueta semántica garantiza una densidad de datos accesible. El componente desacopla la presentación de la taxonomía subyacente, resolviendo los identificadores de familia a través de una configuración JSON en tiempo de ejecución.

## Directrices de uso

### Escenarios de implementación
- **Marcadores de Mapa**: Funciona como la base visual para los marcadores de anclas, utilizando puntos codificados por colores para señalar la afiliación familiar.
- **Filtrado de Datos**: Sirve como la primitiva interactiva dentro de las filas de filtro (normalmente emparejada con una casilla de verificación).
- **Superposiciones de Detalles**: Proporciona categorización de alto nivel dentro de los paneles laterales y distintivos de encabezado.
- **Análisis de Conglomerados**: Emplea una variante de anillo concéntrico para representar la distribución familiar dentro de los conglomerados (clusters) agregados del mapa.

### Restricciones
El componente está reservado para la clasificación taxonómica. No debe utilizarse para indicadores de estado binarios, mensajes transitorios del sistema o etiquetas no taxonómicas, que son atendidos por los componentes Tag (Etiqueta) y Status Indicator (Indicador de Estado).

## Especificaciones técnicas

### Anatomía y composición
- **Indicador**: Un punto circular de 12px (predeterminado) o 24px (marcador) que utiliza tokens de color específicos de la familia.
- **Etiqueta**: Un nombre de visualización resuelto por la taxonomía (por ejemplo, "Warehouse Club").
- **Capa de Accesibilidad**: Un `aria-label` que combina la semántica del punto y la etiqueta, garantizando que el indicador visual esté oculto para los lectores de pantalla para evitar anuncios redundantes.

### Modelo de interacción
El muestrario es nativamente estático. La interactividad se hereda de su contenedor principal (por ejemplo, un botón de filtro o una función de mapa). En las superficies de mapas, el componente admite un comportamiento de revelación por zoom: se prevé que los anillos de centroide de conglomerado se representen en niveles de zoom inferiores a 8.5, transicionando a muestrarios individuales en aumentos mayores.

## Accesibilidad y cumplimiento
El componente está diseñado para cumplir con los estándares WCAG 2.2 AA:
- **Señalización Redundante**: El color nunca es el único canal de información; las etiquetas proporcionan el significado semántico principal.
- **Soporte de Alto Contraste**: En entornos de modo de alto contraste de Windows o `forced-colors`, el punto vuelve a los colores del sistema para enlaces mientras la etiqueta mantiene la integridad del texto.
- **Contraste de Luminancia**: Los tokens de color de la familia están validados para una relación de contraste mínima de 3:1 frente a mapas base tanto claros como oscuros.

## Tokens de diseño (DTCG)

| Token | Valor | Descripción |
| :--- | :--- | :--- |
| `ps.swatch.dot.size` | 12px | Tamaño de punto en línea predeterminado |
| `ps.swatch.dot.size.marker` | 24px | Tamaño de variante de marcador de mapa |
| `ps.brand-family.department.color` | `#0B5FFF` | Azul azur |
| `ps.brand-family.hardware.color` | `#FF6B00` | Naranja construcción |
| `ps.brand-family.warehouse-club.color` | `#00875A` | Verde almacén |

## Extensiones previstas
Se prevé que las futuras iteraciones incluyan:
- **Rellenos con Patrones**: Soporte planificado para patrones geométricos dentro del punto para mejorar la distinción para usuarios con deficiencias avanzadas de visión cromática.
- **Gráficos de Tarta Dinámicos**: Se está investigando la transición del anillo de centroide de conglomerado a un gráfico de dona dinámico cuando la densidad del conglomerado supere las 10 anclas.

## Véase también

- [[brand-typography]] — los estándares de tipografía de impresión de la plataforma que complementan este sistema de identidad visual
- [[app-orchestration-gis]] — el motor analítico GIS que produce los datos de clúster que este componente visualiza
- [[location-intelligence-platform]] — la plataforma de inteligencia de ubicación que usa este componente en su superficie de mapa interactivo
- [[co-location-methodology]] — la metodología de co-ubicación cuyos rankings de niveles impulsan las asignaciones de color del muestrario
