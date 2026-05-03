---
schema: foundry-doc-v1
type: topic
category: reference
slug: map-side-drawer
title: Panel Lateral de Mapa
paired_with: map-side-drawer.md
state: authoritative
audience: vendor-public
bcsc_class: current-fact
language_protocol: DESIGN-COMPONENT
authored: 2026-04-30
---

# Panel Lateral de Mapa (Map Side Drawer)

El "Map Side Drawer" es un patrón de superposición persistente diseñado para la inspección detallada de características sin perder el contexto geográfico. Sustituye a las ventanas emergentes (popups) transitorias por un panel de ancho fijo que se desliza desde el borde derecho, proporcionando un espacio dedicado para metadatos complejos, contexto de conglomerados y divulgaciones regulatorias.

## Resumen Ejecutivo

La interfaz GIS de Foundry utiliza el Panel Lateral de Mapa para centralizar los datos de atributos de las características seleccionadas del mapa. A diferencia de los subtítulos o ventanas emergentes tradicionales que oscurecen el lienzo del mapa, el panel mantiene una huella fija de 340px en el margen derecho, lo que permite que el mapa permanezca interactivo y visible. El componente está diseñado para el procesamiento rápido de datos, utilizando una cuadrícula de hechos estructurada y banners de divulgación opcionales para cumplir con los requisitos operativos y de transparencia regulatoria.

## Directrices de Uso

### Escenarios de Implementación
- **Detalles de Anclas Comerciales**: Sirve como la pantalla principal para metadatos comerciales, incluyendo dirección, códigos NAICS y fechas de apertura.
- **Contextualización de Conglomerados**: Proporciona datos agregados para los conglomerados de mapas seleccionados (p. ej., pertenencia a corredores, densidad de anclas).
- **Análisis de Edificios**: Previsto para su uso en integraciones BIM para mostrar detalles de la envolvente del edificio y la composición de la movilidad.

### Restricciones
El panel está destinado a la recuperación de información profunda. No debe utilizarse para mensajes de confirmación transitorios o alertas del sistema, que son atendidos por los componentes Toast o Snackbar.

## Especificaciones Técnicas

### Anatomía y Composición
- **Bloque de Encabezado**: Contiene el título de la característica y un distintivo de familia de marca para una identificación taxonómica rápida.
- **Cuadrícula de Hechos**: Utiliza una lista de definiciones (`<dl>`) para presentar pares clave-valor de metadatos.
- **Zona de Divulgación**: Un área dedicada en la parte superior o inferior para declaraciones prospectivas exigidas por la BCSC.

### Modelo de Interacción
- **Transición**: Se desliza desde el borde derecho durante 250ms utilizando una curva `cubic-bezier(0.16, 1, 0.3, 1)`.
- **Cierre**: Puede cerrarse mediante un botón de icono dedicado, la tecla ESC o haciendo clic en un área vacía del lienzo del mapa.
- **Modalidad**: Funciona como un punto de referencia complementario no modal (`aria-modal="false"`), permitiendo a los usuarios desplazar y hacer zoom en el mapa detrás del panel.

## Accesibilidad y Cumplimiento
El componente está diseñado para una compatibilidad total con el teclado y los lectores de pantalla:
- **Gestión del Foco**: Al abrirse, el foco queda atrapado dentro del panel para facilitar una navegación rápida por teclado. El cierre devuelve el foco al elemento del mapa previamente activo.
- **Roles Semánticos**: Utiliza `role="complementary"` con una `aria-label` descriptiva.
- **Control de Movimiento**: Respeta `prefers-reduced-motion`, colapsando la animación de deslizamiento en un desvanecimiento de opacidad instantáneo.

## Tokens de Diseño (DTCG)

| Token | Valor | Descripción |
| :--- | :--- | :--- |
| `ps.map-drawer.width` | 340px | Ancho fijo para superposiciones de mapa |
| `ps.map-drawer.bg` | surface-elevated | Fondo para superficies elevadas |
| `ps.map-drawer.transition.duration` | 250ms | Duración estándar de deslizamiento |
| `ps.map-drawer.shadow` | shadow-side-panel | Sombra interior en el borde principal |

## Hoja de Ruta Estratégica
Los desarrollos futuros prevén incluir:
- **Vista de Comparación**: Una variante planificada de panel dividido para admitir la comparación federada de conglomerados (Invención de Doctrina #9).
- **Ancho Adaptativo**: Se está investigando si se requiere una expansión a ancho completo para pantallas móviles preservando al mismo tiempo un contexto mínimo del mapa.
