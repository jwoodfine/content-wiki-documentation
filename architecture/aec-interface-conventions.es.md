---
schema: foundry-doc-v1
title: "Convenciones de Interfaz AEC"
slug: aec-interface-conventions
short_description: "Las cuatro convenciones universales de interfaz — árbol espacial, panel de propiedades, visor 3D y navegador de vistas — que todas las herramientas de autoría BIM implementan, proporcionando vocabulario compartido para superficies de coordinación transversales consistentes."
language: es
category: architecture
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-17
editor: pointsav-engineering
cites: [ifc-4-3]
paired_with: aec-interface-conventions.md
---

Cada plataforma importante de autoría BIM incluye cuatro convenciones de interfaz que un arquitecto o ingeniero aprende una vez y aplica en todos los productos: un árbol de jerarquía para la estructura espacial, un panel de propiedades para los atributos de los elementos, un viewport 3D y un navegador de vistas guardadas. Estas convenciones existen porque el modelo de datos subyacente (la jerarquía de entidades IFC) es el mismo independientemente de la herramienta que lo autorice. Los componentes de interfaz universal del Sistema de Diseño de la Construcción están construidos sobre este vocabulario compartido.

## Las Cuatro Convenciones Universales

### Árbol espacial

Toda herramienta de autoría BIM muestra la estructura espacial de un edificio como un árbol jerárquico: Sitio contiene Edificio, Edificio contiene Planta, Planta contiene Espacio, Espacio contiene Elementos. Esto corresponde directamente a la jerarquía `IfcSpatialStructureElement` en IFC 4.3. El componente `SpatialTree` del Sistema de Diseño de la Construcción renderiza esta jerarquía con comportamiento consistente de expansión/colapso, propagación de selección al Viewport3D y visualización del GUID IFC al pasar el cursor.

### Panel de propiedades

Cuando se selecciona un elemento, un panel de propiedades muestra el nombre de la clase IFC del elemento, su identificador globalmente único (GUID IFC) y todos los valores de Conjunto de Propiedades adjuntos. El componente `PropertiesPanel` del Sistema de Diseño de la Construcción renderiza los mismos datos con una variante de prop de modo: el modo `view` muestra todos los valores Pset de forma plana; el modo `edit` muestra solo los valores que el rol actual está autorizado a modificar.

### Viewport 3D

La superficie de interfaz principal de toda herramienta BIM es un viewport 3D de perspectiva u ortográfico. Los controles de cámara (órbita, panorámica, zoom) usan controles de ratón estándar de la industria. El componente `Viewport3D` del Sistema de Diseño de la Construcción incorpora el visor xeokit-sdk o @thatopen/web-ifc con estos controles de cámara estándar.

### Navegador de vistas

El componente `ViewNavigator` del Sistema de Diseño de la Construcción renderiza las vistas guardadas como pestañas etiquetadas: `Planta L1`, `Sección A-A`, `Alzado Norte`. Al seleccionar una pestaña se carga el estado de la cámara y, opcionalmente, el filtro de planta IFC para esa vista.

## Diez Componentes de Interfaz Universal

El Sistema de Diseño de la Construcción define diez componentes de interfaz que aparecen en cada superficie — ya sea el cliente de campo, la consola de gestión de instalaciones o cualquier superficie futura que consuma el Sistema de Diseño de la Construcción.

| Componente | Función |
|---|---|
| `SpatialTree` | Navegación de jerarquía espacial (Sitio → Edificio → Planta → Espacio) |
| `PropertiesPanel` | Visualizador y editor de Psets IFC (variante de prop de modo) |
| `Viewport3D` | Viewport del modelo 3D (incorporación xeokit / @thatopen) |
| `ViewNavigator` | Vistas guardadas con nombre como pestañas etiquetadas |
| `IssueTracker` | Lista de temas BCF 3.0 con filtros de estado y asignado |
| `ElementSearch` | Búsqueda de GUID IFC o valor Pset en todo el modelo cargado |
| `ClashReview` | Lista de resultados de detección de colisiones con resaltado en el viewport |
| `HistoryTimeline` | Historial de confirmaciones Git renderizado como línea de tiempo de estados del modelo |
| `ExportPanel` | Exportación COBie, ejecución de validación IDS, descarga BCF ZIP |
| `StatusBar` | Progreso de carga del modelo, recuentos de validación, marca de tiempo de última sincronización |

## Por qué Importa el Vocabulario Compartido

Los equipos de proyectos BIM frecuentemente trabajan con múltiples herramientas de autoría en un solo proyecto. Los modelos del ingeniero estructural, del arquitecto y del ingeniero MEP exportan IFC-SPF. La coordinación ocurre en un visor común donde nadie está en su entorno de autoría nativo.

Un vocabulario de interfaz compartido significa que el visor de coordinación no introduce una nueva curva de aprendizaje además de las herramientas de autoría.

## Relación con el Sustrato del Sistema de Diseño

El Sistema de Diseño de la Construcción es una extensión semántica AEC de la línea base del Sistema de Diseño Carbon. Carbon proporciona los primitivos de interfaz de usuario fundamentales. El Sistema de Diseño de la Construcción agrega la capa semántica AEC encima: los diez componentes de interfaz universal y las ocho categorías de Objetos BIM primitivos.
