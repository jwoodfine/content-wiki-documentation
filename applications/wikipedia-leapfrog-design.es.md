---
schema: foundry-doc-v1
title: "Diseño leapfrog de Wikipedia — memoria muscular y 5% de margen"
slug: wikipedia-leapfrog-design
short_description: "Qué hereda el motor wiki app-mediakit-knowledge de Wikipedia, qué añade más allá de él, y qué significa el 5% de margen leapfrog para lectores e ingenieros."
category: applications
type: topic
content_type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: wikipedia-leapfrog-design.md
cites: [ni-51-102, osc-sn-51-721]
---

# Diseño leapfrog de Wikipedia — memoria muscular y 5% de margen

El motor wiki [[app-mediakit-knowledge]] hereda el 95% de su interfaz de las convenciones de disposición establecidas por Wikipedia. El 5% restante es el margen leapfrog: añadidos que ningún lector de Wikipedia ha encontrado antes, implementados de forma aditiva para no perturbar la experiencia de lectura base. Este artículo explica por qué se tomó cada decisión de diseño y cómo se construye el contrato estructural con dos tipos de audiencia distintos.

---

## El contrato de memoria muscular

Wikipedia tiene aproximadamente dos mil millones de lectores mensuales. Esos lectores han desarrollado reflejos de navegación a lo largo de dos décadas de exposición a una interfaz específica: la ubicación de las pestañas, la estructura de las secciones de los artículos, el lenguaje visual de las notas al pie, la tabla de contenidos colapsable en el rail izquierdo. Estos reflejos no son fidelidad de marca; son programas motores.

Un nuevo sustrato de publicación de conocimiento se enfrenta a una elección estructural. Puede diferenciar su interfaz de Wikipedia, obligando a los lectores a aprender nuevos programas motores antes de poder trabajar con eficiencia. O puede adoptar la misma interfaz, aceptando una breve confusión inicial a cambio de cero fricción de incorporación.

El sustrato adopta el segundo camino, con una condición: la adopción es razonada, no imitativa. Una adopción razonada identifica el conjunto exacto de patrones que sostienen la memoria muscular y los mantiene inviolables.

### La distribución 95% / 5%

El 95% de la interfaz es el inventario de memoria muscular de Wikipedia, mantenido inviolable en todas las fases. El 5% es el margen leapfrog — añadidos que son aditivos, no sustitutivos, de modo que la experiencia de lectura base no se altera para los lectores que no prestan atención a los añadidos.

---

## Lo que se añade más allá de Wikipedia

Cinco añadidos se incorporan más allá del inventario de Wikipedia. Cada uno es aditivo: ningún patrón de memoria muscular existente se elimina ni altera.

**Insignias de citas.** Junto a cada referencia de cita en línea, la interfaz renderiza una pequeña insignia en la convención de pin CR de las C2PA Content Credentials. La insignia es gris neutro por defecto. En modo predeterminado, el estado positivo (verificado verde) sólo aparece cuando el lector activa explícitamente la configuración de densidad "mostrar todas las marcas verificadas". Las marcas de excepción (ámbar, rojo, azul) se muestran de forma prominente sin necesidad de activación.

**Banner de información prospectiva.** Los artículos cuyo frontmatter establece `forward_looking: true` muestran un banner de advertencia en la vista de lectura. El banner es la expresión en la superficie de lectura de los [[compliance-and-continuous-disclosure|requisitos de divulgación continua]] bajo [ni-51-102] y [osc-sn-51-721].

**Campo de clase de divulgación.** Los artículos llevan un campo `disclosure_class` en el frontmatter con tres valores: `narrative`, `financial`, `governance`. En la fase actual este campo es invisible para los lectores — aparece en los datos estructurados JSON-LD en el bloque `<head>` del artículo renderizado.

**Banda del encabezado IVC (marcador de posición).** Una franja horizontal debajo de la fila del título. En la fase actual esta banda muestra texto de marcador de posición indicando que la verificación aún no está disponible. Se prevé que una fase futura complete la banda con un resumen de verificación en tiempo real.

**Control de densidad para el lector.** Un control de preferencias con tres estados: Desactivado, Solo excepciones (predeterminado), Todos. La configuración se conserva entre sesiones.

---

## Divergencia deliberada de identidad visual

El sustrato adopta los patrones ergonómicos de Wikipedia — dónde están las pestañas, las tablas de contenidos y los encabezados — mientras diverge en todos los puntos donde la divergencia no tiene coste ergonómico.

El color, la tipografía, el logotipo y la marca son activos de marca, no elementos de navegación. Estos son los puntos de divergencia deliberada. La paleta de colores de PointSav se aplica a todos los elementos de la interfaz.

Un lector que llega a documentation.pointsav.com y ha pasado años leyendo Wikipedia navega de inmediato. No confunde el sitio con Wikipedia. La identidad visual es distinta; la identidad de navegación es familiar.

---

## Por qué ambas audiencias se sienten cómodas

Un lector del ámbito financiero llega a través de un enlace a un artículo específico. Ve un título, pestañas de artículo y discusión en la parte superior izquierda, pestañas de leer, editar y ver historial en la parte superior derecha. Nunca ha visitado este sitio antes; navega sin fricción porque ha navegado esta estructura miles de veces en Wikipedia.

Un lector de ingeniería tiene la misma experiencia de navegación y también nota el perfil JSON-LD `TechArticle` en el código fuente de la página, el slug de URL estable correspondiente a un archivo Markdown en un repositorio Git, y el endpoint `/feed.atom` anunciado en la cabecera de la página. Ambos lectores se sienten cómodos sin haber aprendido un nuevo paradigma.

---

## Véase también

- [[app-mediakit-knowledge]] — el motor wiki que implementa este diseño leapfrog
- [[knowledge-wiki-home-page-design]] — la intención de diseño de la página de inicio y las convenciones de Wikipedia aplicadas
- [[source-of-truth-inversion]] — el patrón canónico/vista/efímero que sustenta la postura editorial del motor
- [[substrate-native-compatibility]] — la justificación de la superficie API nativa del sustrato frente a un adaptador de MediaWiki
