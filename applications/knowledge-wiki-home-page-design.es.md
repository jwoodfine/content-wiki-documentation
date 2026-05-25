---
schema: foundry-doc-v1
title: "Página de inicio del wiki de conocimiento — intención de diseño"
slug: knowledge-wiki-home-page-design
short_description: "Cómo la página de inicio de documentation.pointsav.com hereda las convenciones estructurales de Wikipedia y las extiende para lectores técnicos y del ámbito financiero."
category: applications
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: knowledge-wiki-home-page-design.md
cites: [ni-51-102, osc-sn-51-721]
---

# Página de inicio del wiki de conocimiento — intención de diseño

El wiki de documentación de PointSav en documentation.pointsav.com es la superficie de lectura canónica para la arquitectura, los servicios, los sistemas operativos, la gobernanza, la infraestructura, las aplicaciones y el vocabulario de referencia de la plataforma. Su página de inicio hereda las convenciones estructurales de la Portada de Wikipedia — el estándar de referencia para páginas de inicio de conocimiento general — y extiende esa herencia con capacidades que el modelo de gobernanza de Wikipedia no ha podido incorporar.

Este artículo explica la intención de diseño: qué se preserva de Wikipedia, qué se añade más allá de ella, y qué encuentran los lectores técnicos y del ámbito financiero cuando llegan.

---

## Dos lectores, una sola página de inicio

La página de inicio sirve simultáneamente a dos tipos de audiencia.

Un lector técnico — un arquitecto, un desarrollador, un redactor técnico — busca profundidad, autoridad de fuente y estructura legible por máquinas. Un lector del ámbito financiero — un analista, un auditor, un inversor, un regulador — busca la postura de la plataforma, el historial de divulgación y la estructura corporativa, en el mismo registro autoritativo que un expediente regulatorio.

Ambas audiencias llegan a la misma URL (`/`), ven la misma composición y siguen los mismos enlaces hacia el corpus. La página de inicio no se bifurca por audiencia. Sirve a ambas al heredar el compromiso editorial más fundamental de Wikipedia: la ausencia de texto de marketing y la presencia de trabajo editorial. Las declaraciones sobre la plataforma son estructurales ("9 categorías", "N artículos", "actualizado por última vez AAAA-MM-DD"), no promocionales.

---

## Convenciones de Wikipedia preservadas

La Portada en inglés de Wikipedia se compone de diez espacios estructurales. La página de inicio de PointSav preserva los primitivos fundamentales.

**Banner de bienvenida.** Wikipedia abre con el alcance y la escala de la comunidad. La página de inicio de PointSav abre con el alcance ("La documentación de la plataforma de PointSav cubre la arquitectura, los servicios, los sistemas operativos y las convenciones de gobernanza del sustrato PointSav") y la escala estructural ("N artículos en 9 categorías, actualizado por última vez el AAAA-MM-DD").

**Artículo destacado.** El artículo destacado de hoy de Wikipedia impone un fragmento de entre 909 y 1.009 caracteres — por recuento de caracteres, no de palabras. La página de inicio de PointSav preserva ese invariante de formato: título enlazado en negrita, paráfrasis del párrafo de apertura del artículo en registro de cuerpo, cierre "→ Leer".

**Explorar por categoría.** La página de inicio de PointSav presenta las nueve categorías ratificadas — arquitectura, servicios, sistemas, aplicaciones, gobernanza, infraestructura, empresa, referencia, ayuda — en una cuadrícula de 3×3. La cuadrícula muestra las nueve categorías incluso cuando están vacías.

**Adiciones recientes.** Los cinco artículos más recientes por fecha `last_edited`, en orden descendente. La intención coincide con la sección "¿Sabías que...?" de Wikipedia: señalizar que el corpus se mantiene activamente.

**Pie de página.** Aviso de licencia CC BY 4.0 y enlaces a los repositorios de GitHub de referencia canónica. Sin publicidad, suscripciones ni afiliados.

---

## Extensiones más allá de Wikipedia

Cinco primitivos extienden la composición de la página de inicio de Wikipedia. Tres están disponibles en la iteración actual. Dos están previstos para iteraciones futuras.

**Estructura de espacios legible por máquinas.** La página de inicio emite JSON-LD por espacio — el espacio del artículo destacado como referencia `Article` tipada, el espacio de adiciones recientes como `ItemList`, la cuadrícula de categorías como colección `WebPageElement`. Los consumidores posteriores reciben estructura en lugar de prosa a interpretar.

**Cadencia de trabajo editorial como señal visible.** La página de inicio muestra la cadencia editorial a través de la marca de tiempo "última actualización" en el banner de bienvenida, el artículo destacado rotatorio y el feed de adiciones recientes.

**Señal de incorporación al rol de editor.** Un bloque "Otras áreas" enlaza a los repositorios de GitHub y a los artículos de sistema de diseño, gobernanza e incorporación de colaboradores. El camino de lector a colaborador es visible desde la página de inicio.

**Agregado de rastro de investigación por sección (previsto).** El wiki tiene previsto mostrar un widget agregado: "Preguntas editoriales abiertas en el corpus: N". Este widget está previsto para una iteración futura.

**Punto de entrada al grafo de citas (previsto).** Se tiene previsto incluir un punto de entrada al grafo de conocimiento del corpus — nodos tipados, aristas ponderadas y lagunas de enlaces rojos — cuando el corpus alcance la escala suficiente para que la navegación por el grafo resulte útil.

---

## Lo que la página de inicio omite deliberadamente

La página de inicio no muestra publicidad, no recoge suscripciones, no usa lenguaje de marketing, no se bifurca por audiencia, no muestra botones de redes sociales y no presenta llamadas a la acción. Las métricas de participación no se muestran en la superficie de la página de inicio.

---

## Véase también

- [[app-mediakit-knowledge]]
- [[wikipedia-leapfrog-design]]
- [[wiki-component-library]]
- [[language-protocol-substrate]]
