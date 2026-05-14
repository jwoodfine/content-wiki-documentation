---
schema: foundry-doc-v1
title: "Página de inicio del wiki de documentación — intención de diseño"
slug: knowledge-wiki-home-page-design.es
category: applications
type: topic
quality: complete
short_description: "Intención de diseño de la página de inicio de documentation.pointsav.com: los primitivos estructurales de Wikipedia preservados íntegramente, las cinco adiciones de avance construidas sobre ellos, y lo que cada audiencia encuentra al llegar."
status: active
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
language: es
last_edited: 2026-05-14
editor: pointsav-engineering
paired_with: knowledge-wiki-home-page-design.md
cites:
  - ni-51-102
  - osc-sn-51-721
---

## Adaptación estratégica

El wiki de documentación de PointSav en `documentation.pointsav.com` es la superficie de lectura canónica para la arquitectura, los servicios, los sistemas operativos, la gobernanza, la infraestructura, las aplicaciones, el vocabulario de referencia y el sistema de diseño de la plataforma. Su página de inicio hereda estructuralmente la Página Principal de Wikipedia — el estándar de referencia para páginas de inicio de conocimiento general en la internet pública — y extiende esa herencia con primitivos que el modelo de gobernanza voluntaria de Wikipedia no ha podido implementar en la última década.

## Dos lectores, una página de inicio

La página de inicio sirve a dos audiencias simultáneamente: un lector de ingeniería — arquitecto, desarrollador, escritor técnico — que busca profundidad, autoridad de fuente y estructura legible por máquinas; y un lector de la comunidad financiera — analista, auditor, inversor, regulador — que busca la postura de la plataforma, el historial de divulgación y la estructura empresarial presentados con el mismo registro autoritativo de un documento regulatorio.

Ambas audiencias llegan a la misma URL (`/`), ven la misma composición y siguen los mismos enlaces azules hacia el corpus. La página de inicio no divide por audiencia. La composición sirve a ambas porque hereda el compromiso editorial más fundamental de Wikipedia: la ausencia de texto de marketing y la presencia de trabajo editorial. Las declaraciones sobre la plataforma son estructurales ("10 categorías", "N artículos", "última actualización AAAA-MM-DD"), no promocionales.

## Wikipedia como herencia estructural — preservada íntegramente

La página de inicio preserva los primitivos de carga de la Página Principal de Wikipedia:

**Banner de bienvenida — preservado.** PointSav abre con el equivalente de Wikipedia: alcance y escala estructural ("N artículos en 10 categorías, última actualización AAAA-MM-DD"), derivados en tiempo de renderizado, no redactados como texto de marketing. No aparecen adjetivos de autodescripción en el banner.

**Artículo destacado — preservado.** El blurb se aplica en 909–1.009 caracteres — recuento de caracteres, no de palabras — porque la restricción evita tanto el relleno como el truncamiento en la rotación. El artículo destacado rota según lo permite el trabajo editorial; la cadencia actual es semanal en lugar de diaria.

**Exploración por categoría — preservada estructuralmente.** Las diez categorías activas — arquitectura, sustrato, patrones, sistemas, servicios, aplicaciones, gobernanza, infraestructura, referencia, sistema de diseño — se muestran en la superficie de la página de inicio. La cuadrícula muestra las diez aunque una categoría tenga pocas entradas.

**Adiciones recientes — preservadas.** Los 5 artículos más recientes por fecha `last_edited` en orden descendente, señalando que el corpus está activamente mantenido.

**Pie de página — preservado.** Aviso de licencia CC BY 4.0, enlaces a los repositorios de fuente canónica, sin encuadre comercial.

## El avance — lo que extiende Wikipedia en la superficie de la página de inicio

Cinco primitivos extienden la composición de Wikipedia. Tres son de primera clase; dos son de segunda clase y están planificados para iteraciones futuras.

**Estructura de ranuras legible por máquinas.** La página de inicio emite JSON-LD por ranura — la ranura del artículo destacado es una referencia `Article` tipada, la ranura de adiciones recientes es una `ItemList` de referencias `Article` tipadas, la cuadrícula de categorías es una colección `WebPageElement` tipada. Los consumidores posteriores reciben estructura en lugar de prosa a inferir.

**Cadencia de trabajo editorial como señal visible.** La página de inicio muestra la cadencia del trabajo editorial a través de la marca de tiempo "última actualización" en el banner de bienvenida, el artículo destacado rotativo y el feed de adiciones recientes. Una futura iteración *planificada* puede clasificar por `content_reviewed_on` (revisión editorial sustantiva) en lugar de `last_edited` (recencia), sujeta a lenguaje cautelar conforme a [ni-51-102] y [osc-sn-51-721].

**Señal de incorporación lector-a-contribuidor.** Un bloque "Otras áreas" vincula a los repositorios de fuente y a los artículos de gobernanza y contribución. El camino del lector al contribuidor es visible desde la página de inicio y está a un clic de distancia.

**Avance de la pista de investigación por sección (planificado).** La superficie de inicio *tiene la intención* de mostrar un pequeño widget agregado: "Preguntas editoriales abiertas en el corpus: N". *Planificado* para una iteración futura.

**Punto de entrada al grafo de citas (planificado).** Un mini-mapa del grafo de citas *planificado* para cuando el corpus alcance el tamaño en que el recorrido del grafo justifique el costo editorial.

## Lo que esta página de inicio deliberadamente no hace

La página de inicio no muestra publicidad, no recopila suscripciones a boletines, no invoca texto de marketing, no se divide por audiencia, no muestra botones para compartir en redes sociales y no presenta llamadas a la acción de "Comenzar" o "Solicitar una demostración". Cada una de estas ausencias es fundamental. Una página de inicio que incluya cualquiera de ellas estaría optimizada para conversión o participación — la estética del marketing de producto SaaS — y esa estética, por muy bien ejecutada que esté, indica al lector que está leyendo marketing en lugar de referencia.

## Véase también

- [[wikipedia-leapfrog-design]] — el contrato de memoria muscular 95%/5% y la intención de diseño del chrome
- [[article-shell-leapfrog]] — los cinco primitivos de shell de artículo más allá de Wikipedia
- [[app-mediakit-knowledge]] — la arquitectura del motor wiki y la superficie de rutas
- [[wiki-provider-landscape]] — el panorama de proveedores de wiki y documentación evaluados frente a los primitivos estructurales de Wikipedia
