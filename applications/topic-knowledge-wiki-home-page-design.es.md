---
schema: foundry-topic-v1
status: published
last_edited: 2026-04-30
category: applications
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
language: es
companion: topic-knowledge-wiki-home-page-design.md
cites:
  - ni-51-102
  - osc-sn-51-721
---

El wiki de documentación de PointSav en documentation.pointsav.com es la superficie de lectura canónica para la arquitectura, los servicios, los sistemas operativos, la gobernanza, la infraestructura, las aplicaciones, la postura corporativa, el vocabulario de referencia y la ayuda para colaboradores de la plataforma. Su página de inicio se hereda estructuralmente de la Página principal de Wikipedia — el estándar de oro de las páginas de inicio de conocimiento general en internet público — y extiende esa herencia con primitivas que el modelo de gobernanza voluntaria de Wikipedia no ha podido implementar en la última década.

## Dos lectores, una página de inicio

La página de inicio sirve a dos audiencias simultáneamente: un lector de ingeniería (arquitecto, desarrollador, escritor técnico) que quiere profundidad, autoridad de fuente y estructura legible por máquina; y un lector de la comunidad financiera (analista, auditor, inversor, regulador) que quiere la postura del sustrato, el historial de divulgación y la estructura de la empresa expuestos en un registro autoritativo. Ambas audiencias llegan a la misma URL (`/`) y ven la misma composición. La página no bifurca por audiencia.

## Memoria muscular de Wikipedia — preservada verbatim

Diez ranuras estructurales componen la Página principal de Wikipedia en inglés. La página de inicio de PointSav preserva las primitivas de carga de la siguiente manera:

El **banner de bienvenida** abre con una sola oración y dos estadísticas — alcance y escala estructural — ambas derivadas en tiempo de renderizado, sin adjetivos de autodescripción. El **artículo destacado** preserva el invariante de formato de Wikipedia: título en negrita con enlace, paráfrasis del registro corporal del encabezado del artículo de 909–1.009 caracteres, cierre "→ Leer". **Explorar por categoría** expone las nueve categorías ratificadas — arquitectura, servicios, sistemas, aplicaciones, gobernanza, infraestructura, empresa, referencia, ayuda — en una cuadrícula 3×3, renderizando las nueve incluso cuando una categoría está vacía. **Adiciones recientes** expone los 5 artículos principales por fecha `last_edited` en orden descendente. El **pie de página** lleva aviso de licencia CC BY 4.0 y enlace a los repositorios GitHub, sin publicidad ni formularios de suscripción.

## El salto tecnológico — lo que extiende Wikipedia en la superficie de la página de inicio

Cinco primitivas extienden la composición de la página de inicio de Wikipedia. Tres son de primera clase; dos son de segunda clase.

**Estructura de ranura legible por máquina.** La página de inicio emite JSON-LD por ranura — el artículo destacado es una referencia `Article` tipada, las adiciones recientes son una `ItemList` de referencias `Article` tipadas. Los consumidores posteriores reciben estructura en lugar de prosa para inferir. Esto aborda el problema estructural que la Fundación Wikimedia nombró en sus OKRs de Producto y Tecnología 2025-2026: el 65% de las solicitudes más costosas de Wikipedia provienen de bots raspadores que recopilan datos de entrenamiento de IA, y la estructura proporcionada no coincide con la que los consumidores de IA necesitan.

**Cadencia de labor editorial como señal visible.** La página de inicio expone la cadencia de labor editorial visiblemente mediante la marca de tiempo "última actualización" en el banner de bienvenida, el artículo destacado rotatorio, y el feed de adiciones recientes.

**Editor como señal de acceso.** La página de inicio incluye un bloque "Otras áreas" con enlaces a repositorios GitHub y a artículos de incorporación de colaboradores. El camino del lector al colaborador es visible desde la página de inicio.

**Avance del rastro de investigación por sección (planificado).** Se *prevé* que la página de inicio exponga un pequeño widget agregado con el recuento de preguntas editoriales abiertas en el corpus. Esto requiere que la disciplina de rastro de investigación a nivel de artículo sea ampliamente adoptada primero.

**Punto de entrada al grafo de citas (planificado).** Se *planifica* implementar un punto de entrada al grafo de citas en la página de inicio, diferido hasta que el corpus alcance ≥200 artículos.

## Lo que la página de inicio deliberadamente no hace

La página de inicio no muestra publicidad, no recoge suscripciones a boletines informativos, no invoca copia de marketing, no bifurca por audiencia, y no presenta llamadas a la acción de "Comenzar" o "Obtener una demostración". Cada una de estas ausencias es parte de la carga. Una página de inicio que incluyera cualquiera de ellas estaría optimizada para la conversión o el compromiso, que es la estética de la documentación del marketing de productos SaaS — y esa estética señala al lector que está leyendo marketing en lugar de referencia.

## Véase también

- [[topic-article-shell-leapfrog]] — las primitivas de salto tecnológico de la capa de artículo
- [[topic-app-mediakit-knowledge]] — la arquitectura del motor
- [[topic-wiki-provider-landscape]] — la auditoría del panorama competitivo
- [[topic-wikipedia-leapfrog-design]] — el contrato de memoria muscular 95%/5%

## Procedencia

Redactado el 2026-04-30 por el cluster project-knowledge basándose en investigación paralela de sub-agentes. Refinado por project-language 2026-04-30. Las declaraciones prospectivas sobre iteraciones planificadas y competitividad en premios siguen la postura de divulgación continua [ni-51-102] y [osc-sn-51-721].

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
