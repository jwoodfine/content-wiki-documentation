---
schema: foundry-doc-v1
title: "Compatibilidad nativa del sustrato — por qué se descartó el adaptador de Action API"
slug: substrate-native-compatibility
short_description: "Establece compatibilidad estructural con convenciones de lector e integrador de MediaWiki mientras rechaza deliberadamente la mimicría de API, manteniendo interfaces nativas de sustrato que reducen carga de mantenimiento y evitan obligaciones de divulgación ligadas a garantías de compatibilidad."
status: active
category: substrate
type: topic
content_type: topic
quality: complete
index_group: sovereignty-and-customer-ownership
last_edited: 2026-05-25
editor: pointsav-engineering
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
paired_with: substrate-native-compatibility.md
cites:
 - ni-51-102
 - np-51-201
---

El wiki de PointSav en `documentation.pointsav.com` ofrece compatibilidad estructural con las convenciones orientadas al lector de MediaWiki — patrones de URL, sintaxis de wikilinks, sintaxis de notas al pie — mientras rechaza deliberadamente replicar la superficie de API interna de MediaWiki, incluida una API de escritura. Cada interfaz que el sustrato no replica es una [[compliance-and-continuous-disclosure|obligación de cumplimiento]] que no asume.

El motor es de solo lectura desde la perspectiva de un visitante — no hay editor en el navegador, no hay API de escritura y no existe ninguna ruta de edición autenticada de ningún tipo. Un artículo se edita en su repositorio git de origen, mediante el flujo editorial normal que produce el commit, y el cambio aparece en el siguiente renderizado del wiki sin reiniciar el servicio. El historial de revisiones que ve un lector es ese mismo log de git, leído directamente en lugar de duplicado en una base de datos separada.

## Costo y beneficio de rechazar el adaptador

Esa decisión tiene un costo concreto y un beneficio concreto. El costo: los colaboradores que migran flujos de automatización compatibles con MediaWiki deben reimplementarlos contra nuevas interfaces. El beneficio: cada endpoint de la Action API que MediaWiki publica, retira o modifica habría generado un evento de mantenimiento; la plataforma no controla esa velocidad, y cada interfaz pública que expone la plataforma es una superficie de divulgación continua bajo la legislación de valores canadiense (el Instrumento Nacional 51-102 y la Política Nacional 51-201 de la CSA). Rechazar el adaptador significa que los compromisos de divulgación del wiki quedan acotados a lo que el sustrato realmente provee.

El resultado es un wiki con el alcance de ecosistema de lectores e integradores de un reemplazo de MediaWiki — resolviendo wikilinks, sirviendo `sitemap.xml`, aceptando marcado al estilo Wikipedia — y una superficie de mantenimiento que escala con la [[app-mediakit-knowledge|velocidad propia de la plataforma]], no con la de MediaWiki.

## La elección

El [[app-mediakit-knowledge|wiki de ingeniería]] de PointSav en `documentation.pointsav.com` es un wiki nativo del sustrato. Acepta una importación única de XML de MediaWiki, sirve URLs con la forma familiar `/wiki/{slug}` de MediaWiki, acepta la sintaxis de Wikipedia con `[[wikilink]]` y `[^nota]`, y se detiene ahí. No implementa la Action API de MediaWiki, no soporta plantillas de MediaWiki, no ejecuta un marco de bots compatible con pywikibot, y no proporciona una superficie de escritura que imite los endpoints REST de MediaWiki.

## Compatibilidad estructural frente a imitación de interfaces

La distinción arquitectónica central: cuando el sustrato sustituye el papel de una plataforma existente, replica la *compatibilidad estructural* — las superficies que un lector o integrador externo encuentra — sin replicar la *imitación de interfaces* — la forma de API que consumiría una integración de sistema interno. La distinción es fundamental.

El adaptador de la Action API de MediaWiki se definió durante la fase de diseño inicial del [[app-mediakit-knowledge|motor wiki]] en la versión 0.1.10 y se descartó en la versión 0.1.14, después de que se identificaran la carga de mantenimiento y el riesgo de [[disclosure-substrate|postura de divulgación]] que el adaptador habría introducido. Este artículo cubre esa justificación.

## El foso del ecosistema — lo que realmente compra la compatibilidad

El ecosistema de MediaWiki es real. Aproximadamente 1.500 extensiones, cientos de miles de plantillas, un marco de bots maduro (pywikibot), integración con Wikidata, la biblioteca de activos de Wikimedia Commons, y un profundo archivo de práctica operacional en Wikipedia, Wiktionary, Wikiquote y una larga cola de instalaciones autohospedadas. Un motor wiki que promete compatibilidad con MediaWiki hereda por referencia una porción de ese foso.

Pero el foso tiene dos partes, y las partes tienen costos distintos para participar en ellas.

### Convenciones de lector e integrador

La primera parte es la **compatibilidad estructural para lectores e integradores externos**: un lector que conoce el patrón de URL y el marcado de Wikipedia puede navegar el wiki sin reentrenamiento; un sistema externo que ingiere `sitemap.xml` o sigue wikilinks descubre el corpus sin adaptadores a medida. Esta parte es de bajo costo — `/wiki/{slug}`, `[[wikilink]]` y `[^1]` son convenciones que el sustrato adopta porque son útiles, no imitación.

### Imitación de interfaces y sus costos

La segunda parte es la **imitación de interfaces de sistemas internos**: extensiones que leen y escriben a través de la Action API, bots que se autentican contra el flujo de inicio de sesión de MediaWiki, plantillas que se expanden en el servidor usando el analizador de MediaWiki. Esta parte es de alto costo — cada endpoint de API imitado es una interfaz que debe mantenerse frente a la evolución de MediaWiki, endurecerse frente a las superficies de ataque conocidas de MediaWiki, y auditarse bajo cualquier postura de cumplimiento a la que se haya comprometido el sustrato.

### Cálculo de costos para rechazar el adaptador

La elección del sustrato es participar plenamente en la primera parte y rechazar deliberadamente la segunda. El cálculo de costos favorece el rechazo:

- Los efectos del ecosistema de lectores e integradores escalan mediante convenciones, que son estables durante una década. El sustrato adopta la convención una vez y se beneficia indefinidamente.
- Los efectos del ecosistema de extensiones de sistemas internos escalan mediante interfaces, que evolucionan con las versiones de MediaWiki. El sustrato heredaría una carga de mantenimiento que crece con la velocidad del ecosistema de MediaWiki, no con la del sustrato.
- Cada interfaz que el sustrato expone al público es una superficie de divulgación continua bajo la regulación de valores aplicable. Un adaptador de Action API comprometería al sustrato a fundamentar en divulgación el comportamiento de cada endpoint de la Action API, un objetivo móvil.

## Lo que se conservó

Se conservan cuatro superficies de compatibilidad del sustrato, todas en la categoría de bajo costo de provisión:

**La ruta de importación de volcado XML.** Una futura herramienta `import-mediawiki-xml` (planificada) consume volcados XML al estilo Special:Export y produce la forma de Markdown más frontmatter del wiki. La migración es de una sola vez por corpus; ninguna API de MediaWiki en vivo se ejecuta junto al sustrato después. Importar 30 artículos, 3.000 artículos o 30.000 artículos tiene la misma forma operacional — leer el volcado, escribir archivos Markdown, confirmar el commit. El patrón compone naturalmente con el control de versiones.

**Convenciones de URL.** `/wiki/{slug}` coincide con el esquema de URL de MediaWiki. Los sitios externos que enlazan a artículos mediante este patrón de URL siguen resolviendo sin errores 404. La ruta es una sola línea en el enrutador axum del motor wiki y no cuesta nada mantenerla. Adoptar la convención es una elección de bajo costo para el alcance del ecosistema.

**Sintaxis de wikilinks.** `[[slug]]` y `[[slug|texto de presentación]]` coinciden con el marcado de Wikipedia. Los colaboradores que conocen Wikipedia reconocen la forma. El motor indexa el árbol de contenido en un grafo de enlaces en memoria al iniciar, y el renderizador resuelve los wikilinks contra ese índice en tiempo de renderizado, emitiendo HTML con estilo de enlace-rojo para los destinos no resueltos.

**Sintaxis de notas al pie.** `[^1]` coincide con la extensión de notas al pie de CommonMark. La bibliografía resuelve las notas al pie contra la lista `references:` del frontmatter del artículo. La implementación se distribuye con `comrak` y no añade ninguna carga de mantenimiento específica del sustrato.

Estas cuatro superficies dan al wiki del sustrato el alcance de ecosistema de lectores e integradores que espera un despliegue que reemplaza a MediaWiki. Ninguna de ellas requiere ejecutar un analizador de MediaWiki, una API de MediaWiki ni un marco de extensiones de MediaWiki.

## Lo que se descartó

Tres superficies de la categoría de alto costo de provisión fueron rechazadas:

**El adaptador de la Action API de MediaWiki.** El adaptador se definió en la versión 0.1.10 del espacio de trabajo como una interfaz que habría replicado `?action=parse`, `?action=edit`, `?action=query`, `?action=login` y el resto de la superficie de la Action API contra el motor wiki del sustrato. En la versión 0.1.14 el adaptador se eliminó del alcance. El razonamiento:

- *El mantenimiento escala con la velocidad de MediaWiki.* Cada endpoint de la Action API que MediaWiki publica, retira o modifica genera un evento de mantenimiento del lado del adaptador. El sustrato no puede gobernar esa velocidad.
- *La auditoría de cumplimiento escala con la superficie de la API.* Cada interfaz que el sustrato expone al público debe fundamentarse en divulgación bajo los requisitos de divulgación continua aplicables. El adaptador de la Action API habría multiplicado la superficie de auditoría por un orden de magnitud sin un beneficio de ecosistema proporcional para la base de clientes real del sustrato.
- *Las interfaces nativas del sustrato cubren los casos de uso orientados al lector.* La superficie de rutas del wiki (`/wiki/{slug}`, JSON-LD, Atom, sitemap, `/search?q=`) cubre lo que habría servido la superficie orientada al lector del adaptador de la Action API, sin comprometer al sustrato con el contrato de API de Wikipedia. La superficie de escritura del adaptador (`?action=edit`, autenticación) no tiene ningún equivalente nativo del sustrato en absoluto — el motor es de solo lectura por HTTP; los artículos se editan en el repositorio git de origen, no a través del wiki.

**Plantillas y funciones de análisis de MediaWiki.** El renderizador del wiki es `comrak` (CommonMark) más extensiones específicas de PointSav para wikilinks, notas al pie, tabla de contenidos y anclas de sección. No es un analizador de MediaWiki. Las plantillas no se expanden en el servidor. La solución alternativa para el contenido que sería una plantilla en MediaWiki son fragmentos de Markdown, insertados por el colaborador en el momento de la edición; el sustrato acepta el costo de duplicación a cambio de un flujo de renderizado determinista que puede auditarse sin analizar un lenguaje de plantillas Turing-completo en tiempo de renderizado.

**El ecosistema de pywikibot.** La ruta de automatización del sustrato es el conjunto de herramientas existente de la plataforma — el flujo de trabajo de commits, la captura de corpus, el protocolo de sesión, la ingesta de borradores del pipeline editorial. Ninguna de ellas implementa la interfaz de pywikibot. Un colaborador que migra de pywikibot a las herramientas del sustrato reimplementa contra las nuevas interfaces; el sustrato acepta el costo de migración a cambio de mantener su ruta de automatización coherente con el modelo de sesión del resto del espacio de trabajo.

## El conjunto de superficies de API nativas del sustrato

La superficie orientada al lector del adaptador de la Action API, las interfaces nativas del sustrato la sirven de forma coherente — su superficie de escritura y autenticación no tiene ningún equivalente nativo del sustrato, por diseño:

| Necesidad de la Action API | Interfaz nativa del sustrato |
|---|---|
| `?action=parse` (renderizar Markdown a HTML) | `GET /wiki/{slug}` (HTML renderizado directamente) |
| `?action=query&list=allpages` (enumerar artículos) | `GET /sitemap.xml` (conforme a sitemaps.org), `GET /special/all-pages` |
| `?action=query&prop=revisions` (historial) | `GET /history/{slug}` (en vivo — lee el log de git directamente, renderiza el diff de cada revisión) |
| `?action=opensearch` / `?action=query&list=search` | `GET /search?q=` (búsqueda de texto completo con Tantivy) |
| `?format=json` (legible por máquina por artículo) | JSON-LD `<script type="application/ld+json">` en el `<head>` de cada artículo |
| Feeds RSS / Atom | `GET /feed.atom` |
| `?action=expandtemplates` | no provisto; el renderizador del sustrato no expande plantillas |
| `?action=edit` (escribir artículos) | no provisto por HTTP en absoluto — no hay API de escritura, no hay editor en el navegador y no hay ninguna ruta de edición autenticada; un artículo se edita en su repositorio git de origen y aparece en el siguiente renderizado |
| `?action=login` / autenticación | no aplicable — no hay nada contra qué autenticarse, ya que el motor no expone ninguna superficie de escritura |

Las interfaces componen con los demás invariantes del sustrato. El JSON-LD se genera a partir del frontmatter del artículo mediante la misma ruta de código que emite el HTML del artículo, de modo que los datos estructurados no pueden desviarse del contenido renderizado. El feed Atom comparte su fuente de datos con el sitemap y la página de índice; un cambio en el árbol de contenido actualiza los tres de forma atómica. El backend de búsqueda (Tantivy) lee el mismo árbol de contenido que el renderizador HTML; no se necesita ninguna ruta de escritura separada para mantener sincronizado el índice de búsqueda, porque el almacén de artículos es el sistema de archivos.

## El esquema de URL `verify://` (planificado)

Un futuro esquema de URL específico del sustrato — `verify://{citation-id}` — está *previsto* para resolver una referencia de cita hacia su fuente verificable a través de la ruta de verificación del sustrato, no a través del DNS público. El esquema está *planificado* para la Fase 7 del motor wiki; no está implementado a partir de v0.1.29.

La motivación: un `[citation-id]` en un artículo es una referencia estructurada que el sustrato puede resolver hacia una fuente autorizada a través del registro de citas. El registro asocia el ID con una tupla (título, URL, referencia de cláusula opcional), y una futura maquinaria de Verificabilidad de Información por Cita (IVC) está *prevista* para reforzar la resolución hasta una prueba de procedencia criptográficamente verificable. Esto es prospectivo. Aplica el lenguaje cauteloso conforme a [ni-51-102] y [np-51-201]. La base razonable es el sustrato de registro de citas ya operando en v0.1.29. El supuesto material es que la maquinaria IVC se ratifique antes de que comience la implementación de la Fase 7.

## La postura de divulgación como lente de compatibilidad

La razón más profunda por la que la postura nativa del sustrato prevalece es que las elecciones de superficie de compatibilidad del motor wiki son, en realidad, elecciones de divulgación continua encubiertas. Cada interfaz que el sustrato expone al público compromete al sustrato con una obligación de divulgación bajo los requisitos de divulgación continua aplicables. Lo que el sustrato no expone, no necesita divulgarlo.

Algunos casos concretos:

### Ejemplos de revisión, renderizado y ruta de edición

Un adaptador de Action API que devolviera `?action=query&prop=revisions` habría comprometido al sustrato con una representación de divulgación continua del historial de revisiones de cada artículo. El sustrato ya se compromete con esto a través de su historial de git (cada edición es un commit firmado, cada commit es una afirmación publicada). Pero una representación paralela de la Action API habría introducido un segundo registro canónico que necesita mantenerse sincronizado con el historial de git; cualquier divergencia es un fallo de divulgación. El sustrato rechaza el adaptador y mantiene git como canónico.

Un adaptador de Action API que devolviera `?action=parse` del lado del servidor habría comprometido al sustrato con un contrato de renderizado del lado del servidor independiente de la fuente en Markdown. Si el HTML renderizado se desvía de la fuente en Markdown, el sustrato tiene un conflicto de divulgación. El sustrato rechaza el adaptador y mantiene el HTML renderizado como una función determinista de la fuente en Markdown más la versión del renderizador.

Un adaptador de Action API que soportara `?action=edit` habría comprometido al sustrato con una ruta de escritura HTTP autenticada con una procedencia más débil que la superficie de edición real del sustrato — la autoría de commits de git, que la disciplina de commits del propio espacio de trabajo ya vincula a una identidad verificada. Una edición al estilo de la API de MediaWiki habría introducido una segunda ruta de escritura autenticada por token que no lleva la misma garantía de identidad. El sustrato rechaza el adaptador por completo en lugar de construir una ruta paralela — no hay ninguna API de escritura que asegurar, así que no hay nada contra qué autenticarse.

El patrón: cada interfaz que el sustrato no replica es una obligación que no asume.

## El patrón se generaliza

La sustitución de sustrato aplica más allá de MediaWiki. Varios casos de sustitución adicionales siguen el mismo patrón:

- **Plataformas de distribución de divulgación.** El registro de divulgación continua del sustrato (historial de git firmado en `documentation.pointsav.com`) es en sí mismo el canal de divulgación; no se requiere ninguna integración con una plataforma de distribución de divulgación de terceros.
- **Plataformas de CRM.** El registro de personas del sustrato es canónico. Ninguna imitación de API al estilo CRM está en alcance.
- **Plataformas de registros corporativos.** El libro de registros corporativos del sustrato es canónico. Ninguna imitación de API de plataforma empresarial.
- **SaaS de proveedores para almacenamiento de documentos.** El sustrato almacena documentos en árboles de Markdown bajo control de versiones; no se necesita ninguna integración SaaS para el almacenamiento.

El hilo común: el sustrato replica la compatibilidad estructural donde compensa y rechaza la imitación de interfaces donde los costos de mantenimiento y divulgación superarían el beneficio de ecosistema. Cada sustitución se analiza bajo la misma lente: qué obliga al sustrato la interfaz de la plataforma existente, y qué gana el sustrato a cambio.

## Véase también

- [[source-of-truth-inversion]] — la designación de capa de almacenamiento de la que depende este patrón (git como registro canónico)
- [[app-mediakit-knowledge]] — el motor wiki que este patrón gobierna
- [[disclosure-substrate]] — la postura de divulgación continua y los casos de sustitución más amplios
