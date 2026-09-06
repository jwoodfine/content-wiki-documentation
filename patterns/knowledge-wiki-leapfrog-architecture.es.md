---
schema: foundry-doc-v1
title: "Arquitectura Leapfrog del wiki de conocimiento"
slug: knowledge-wiki-leapfrog-architecture
short_description: "Estrategia de motor wiki que sirve Markdown plano desde git con interfaz al estilo Wikipedia, alcanzando paridad de memoria muscular antes de la capa de diferenciación."
category: patterns
type: topic
content_type: topic
quality: complete
index_group: interface-and-user-experience
status: active
language: es
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
last_edited: 2026-08-24
editor: pointsav-engineering
cites:
 - ni-51-102
 - np-51-201
paired_with: knowledge-wiki-leapfrog-architecture.md
---

[[app-mediakit-knowledge|`app-mediakit-knowledge`]] es el motor del wiki de conocimiento de PointSav: un binario Rust que sirve tres instancias wiki — `documentation.pointsav.com`, `projects.woodfinegroup.com` y `corporate.woodfinegroup.com` — desde archivos Markdown almacenados en repositorios git. El motor renderiza contenido con la interfaz visual de Wikipedia: tabla de contenidos adherente, resolución de wikilinks con señalización de enlaces rojos, páginas de categoría, historial de edición y búsqueda de texto completo. **Un lector que compare este wiki con Wikipedia función por función encontrará que la mayor parte de la experiencia de lectura ya coincide — las dos piezas claramente ausentes son el infobox y el navbox**, los dos elementos de mayor impacto en la memoria muscular visual de Wikipedia. Una hoja de ruta planificada de varios sprints prevé cerrar esa brecha antes de añadir una capa diferenciadora de Leapfrog 2030 que va más allá de lo que ofrece Wikipedia.

**Por qué importa:** un lector llega ya sabiendo cómo usar este wiki, porque los patrones de lectura y edición son los que dos décadas de uso de Wikipedia ya le enseñaron.

## Por qué Temas, no páginas

La interfaz al estilo Wikipedia del motor responde a un modelo de contenido concreto: un artículo es un **Tema** — una unidad autónoma con su propia tabla de contenidos — no una página dentro de un documento mayor, ni un hilo de correo. Adoptar un wiki responde a un patrón de fallo reconocible: distribuir conocimiento como un conjunto creciente de documentos independientes, cada uno actualizado por separado y reenviado a quien lo solicita, termina por colapsar bajo su propio volumen — cada destinatario acaba con una copia distinta y desactualizada, sin forma de saber cuál es la vigente.

Tres conceptos más antiguos de la ciencia bibliotecaria describen lo que un wiki organizado por Temas restituye. Una **biblioteca** ofrece servicios de información — alguien o algo que ayuda al lector a encontrar lo que necesita, no una carpeta de archivos. Una **enciclopedia** divide el conocimiento en temas en lugar de capítulos, cada uno localizable y enlazado de forma independiente. Un **repositorio** añade control de versiones y disciplina de acceso — el estado actual de un documento y su historial son ambos de primera clase, no solo el estado actual. Una plataforma que solo cumple uno de los tres queda incompleta: una biblioteca pura sin estructura de temas se dispersa; una enciclopedia pura sin disciplina de versiones pierde su historial; un repositorio puro sin estructura de temas es un servidor de archivos con mejor auditoría.

Por esto el objetivo base del motor es específicamente la memoria muscular de lectura y edición de Wikipedia, y no un sistema de gestión de contenido genérico: Wikipedia es el ejemplo existente más claro de una plataforma que es biblioteca, enciclopedia y repositorio a la vez, a una escala que prueba que el modelo funciona.

**Por qué importa:** un lector nunca tiene que preguntarse "¿es esta la versión vigente, y hay una copia mejor en otro lugar?" — cada Tema tiene exactamente un hogar, un historial y una sola respuesta a "qué dice esto ahora mismo."

## Por qué no se porta MediaWiki

MediaWiki es el software que ejecuta Wikipedia. Portarlo a Rust no serviría a los objetivos de la plataforma.

MediaWiki fue diseñado en 2003 para un stack PHP y MySQL. Su parser — el componente que convierte el formato wikitext en HTML — fue descrito por su autor original, Tim Starling, como "un gran montón de expresiones regulares." El proyecto Parsoid, el intento de MediaWiki de reemplazar ese parser con un convertidor bidireccional HTML↔wikitext, tardó diez años en desplegarse y todavía completaba su adopción en 2025.

El sistema de plantillas wikitext es el núcleo de la riqueza de contenido de MediaWiki — infoboxes, navboxes, plantillas de citas y plantillas de coordenadas geográficas están todas implementadas como páginas wiki en el espacio de nombres `Template:`, procesadas por un intérprete de expansión de macros recursivo que llama de vuelta a la base de datos durante el análisis. Este diseño acopla el parser a la base de datos, complica el caching y dificulta operar el sistema sin MySQL.

### Misma experiencia lectora, pila distinta

El objetivo arquitectónico de `app-mediakit-knowledge` no es replicar este diseño, sino lograr la misma experiencia lectora mediante una pila fundamentalmente diferente. El formato de contenido es Markdown con frontmatter YAML, no wikitext. El control de versiones es git, no una tabla de revisiones de MySQL. El backend de búsqueda es Tantivy — embebido, sin carga operativa — no un clúster respaldado por Elasticsearch. La transclusión de plantillas se reemplaza por seis tipos de bloque nativos que cubren aproximadamente el 95 por ciento de para qué se usan realmente las plantillas en Wikipedia.

**Por qué importa:** el lector obtiene la misma página familiar; el operador obtiene un sistema que se ejecuta como un solo binario, sin servidor de base de datos, sin runtime de PHP y sin un clúster de búsqueda separado que mantener vivo.

## Arquitectura de MediaWiki, entendida

El sistema de espacios de nombres de MediaWiki define 30 espacios de nombres en dos ejes: páginas de contenido (Article, User, File, Template, Category, Help, Module, Draft) emparejadas con páginas de discusión (Talk). Las páginas especiales forman una clase aparte de páginas generadas por software, sin equivalente de discusión.

El skin Vector 2022 divide cada página en: un encabezado adherente (logo, búsqueda, selector de idioma, herramientas personales), una barra lateral izquierda (menú de navegación y tabla de contenidos), un encabezado de artículo (pestañas de espacio de nombres, pestañas de vista, título, descripción corta, avisos), el cuerpo del artículo (infobox flotado a la derecha, texto, tablas, imágenes, superíndices de notas al pie), un apéndice (Véase también, Referencias, Enlaces externos), navboxes, tira de categorías y un pie de página (marca de tiempo de última edición, licencia, enlaces legales).

### La extensión Cite y la memoria muscular del lector

La extensión Cite gestiona las notas al pie: `<ref>texto de la cita</ref>` en el cuerpo del artículo inserta un superíndice numerado; `<references/>` al final de la sección renderiza la lista numerada. Reference Tooltips — un gadget de JavaScript — muestra el texto de la cita al pasar el cursor, sin que el lector tenga que desplazarse.

Estos elementos constituyen la memoria muscular que los lectores de Wikipedia han desarrollado a lo largo de dos décadas. Un wiki al que le falte el infobox, la tabla de contenidos adherente, los superíndices de notas al pie `[1][2][3]` o los navboxes no se siente como Wikipedia sin importar qué tan bueno sea su contenido.

**Por qué importa:** estos son los elementos concretos y nombrables que un lector verifica de forma inconsciente — cerrar exactamente esta lista, y no un vago "que se sienta más como Wikipedia," es lo que realmente cierra la brecha.

## Estado actual de las funciones

A partir de mayo de 2026, `app-mediakit-knowledge` implementa aproximadamente el 78 por ciento de la superficie completa de memoria muscular de Wikipedia. Los siguientes elementos están plenamente operativos:

- Wikilinks con distinción azul/rojo (los artículos existentes enlazan en azul; los faltantes, en rojo)
- Tabla de contenidos adherente y colapsable, patrón Vector 2022
- Pestañas Leer / Editar / Ver Historial y lápices de edición por sección
- Pestañas Artículo/Discusión (la pestaña Artículo funciona; la de Discusión es un stub funcional)
- Búsqueda de texto completo vía Tantivy BM25
- Historial de edición, blame y diff unificado vía git
- Editor CodeMirror 6 con autocompletado de citas y subrayado de reglas SAA
- Insignias de calidad (completo / núcleo / stub) y aviso de stub
- Páginas de categoría y tira de categorías al final del artículo
- Página de inicio con cuadrícula de categorías 3×3, artículo destacado y panel de datos leapfrog
- Sindicación Atom 1.0 y JSON Feed 1.1
- Vistas previas de página en tarjeta al pasar el cursor
- Autoenlazador de glosario con tooltips
- Autenticación y cola de revisión de ediciones (Fase 5)
- Remoto git de solo lectura (protocolo smart-HTTP)
- Servidor MCP (JSON-RPC 2.0) para integración de agentes
- Reindexación de búsqueda incremental basada en Notify (sin reinicio al cambiar archivos)
- Navegación móvil tipo hamburguesa

**Por qué importa:** un lector ya obtiene hoy búsqueda funcional, historial de edición funcional y navegación de categorías funcional — la brecha restante está nombrada y acotada abajo, no es una señal de que todo el motor esté sin terminar.

### Elementos faltantes, clasificados por impacto

Los siguientes elementos están en estado de stub o ausentes hoy, clasificados por impacto en la memoria muscular:

| Elemento faltante | Impacto | Notas |
|---|---|---|
| Infobox (resumen estructurado de columna derecha) | 9/10 | El elemento más reconocible de Wikipedia; ausente por completo |
| Navbox (plantilla de navegación inferior) | 8/10 | Crea agrupaciones de temas; ausente por completo |
| Renderizado CSS de citas `[1][2][3]` | 8/10 | Las notas al pie se analizan correctamente; el CSS no está estilizado |
| Tooltip de cita al pasar el cursor | 8/10 | El gadget de JavaScript aún no se ha escrito |
| Diff de dos columnas a nivel de palabra | 7/10 | Existe el diff unificado; falta el estilo de dos columnas de Wikipedia |
| Páginas de discusión | 7/10 | La pestaña se renderiza deshabilitada; no hay backend |
| Redirecciones | 6/10 | No hay procesamiento de frontmatter `redirect_to` |
| Páginas de desambiguación | 6/10 | No hay indicador de tipo de página ni interfaz |
| Special:RecentChanges | 6/10 | Los datos del log de git existen; falta la página HTML |
| Special:AllPages | 5/10 | Falta el endpoint de listado de artículos |
| Artículo `/random` | 5/10 | Ausente |
| Campo de resumen de edición | 5/10 | El mensaje de commit de git se rellena solo con autor y fecha |
| Listas de definición | 4/10 | Extensión de comrak deshabilitada; corrección de una línea |

**Por qué importa:** clasificar las brechas por impacto, en lugar de listarlas alfabéticamente, le dice al lector exactamente qué dos elementos — el infobox y el navbox — moverían más la aguja, en lugar de dejarlo adivinar cuál de trece elementos debería importarle.

## El enfoque de tipos de bloque nativos

En lugar de implementar un motor de expansión de macros wikitext, `app-mediakit-knowledge` está diseñado para usar seis tipos de bloque nativos como bloques de código cercados que el AST de comrak reconoce y convierte a HTML estructurado. Estos están previstos para cubrir la gran mayoría de para qué se usan realmente las plantillas en Wikipedia.

- **Infobox** — tabla resumen de columna derecha definida como bloque YAML cercado que el motor convierte en `<table class="infobox">`. Ningún motor de plantillas, ninguna expansión de macros, ningún intérprete de Lua.
- **Navbox** — un bloque similar previsto para renderizar una tabla horizontal colapsable al final del artículo, agrupando enlaces a artículos relacionados bajo un título compartido. JavaScript colapsa los navboxes cuando aparecen dos o más en la misma página, siguiendo el comportamiento `autocollapse` de Wikipedia.
- **Bloque de cita** — la sintaxis de cita en línea (`[^id]` con `[^id]: texto` al final del artículo) que la extensión de notas al pie de comrak ya analiza. El trabajo pendiente es el CSS de estilo superíndice `[1][2][3]` y un tooltip de JavaScript al pasar el cursor. El registro `citations.yaml` que usa el sistema de autocompletado del editor se extiende de forma natural al renderizado de citas.

El motor ya ejecuta comrak 0.52, que incorpora la extensión `block_directive` (sintaxis `:::infobox`, `:::navbox`), más limpia que los bloques de código cercados para contenido Markdown de varias líneas dentro del cuerpo del bloque. **La actualización de comrak fue la parte fácil; el código de renderizado de infobox y navbox que la usaría todavía no se ha escrito.** Tener la versión más reciente de comrak en su lugar elimina un requisito previo para construir estos tipos de bloque — no significa que ya estén construidos.

**Por qué importa:** no hay que construir ni operar ninguna base de datos de plantillas, intérprete de macros ni sandbox de Lua para que el infobox y el navbox aparezcan en pantalla — el trabajo restante es código de renderizado sobre un bloque YAML fácil de escribir para el autor, no un subsistema nuevo.

## La capa Leapfrog 2030

La memoria muscular de Wikipedia es el piso, no el techo. Una vez que `app-mediakit-knowledge` alcance la paridad completa con Wikipedia, se prevén tres primitivas planificadas de primera clase para distinguirlo de las alternativas existentes.

**Cinta de autoridad de citas** — indicador visual planificado del estado de verificación de las fuentes citadas, por artículo. Las citas resueltas contra `citations.yaml` están previstas para mostrar una cinta de color: verde para verificadas, ámbar para no verificadas, rojo para impugnadas. Wikipedia no tiene equivalente; todas las citas se tratan como igualmente fiables sin distinción de su estado de verificación real.

**Pie de trayectoria de investigación** — cada artículo declara cinco campos de frontmatter (método de investigación, profundidad, confianza, fecha, limitaciones) previstos para renderizarse como una sección plegable. Esto haría visible para el lector la procedencia de cada afirmación, apoyando las obligaciones de divulgación continua de NI 51-102 para emisores regulados. Wikipedia tiene archivos de página de discusión e historial de edición, pero ninguna procedencia de investigación estructurada a nivel de artículo.

**Editor con integración de IA** — el editor CodeMirror 6 incluye un acceso directo de tres teclas: Tab (completar la oración actual), Ctrl+K (preguntar sobre el contenido), Alt+J (insertar una cita). Estas funciones están planificadas para llamar a `app-orchestration-command` vía el proxy Doorman. Actualmente son endpoints 501 en espera de la operacionalización de service-slm. Una vez activadas, están previstas para ofrecer asistencia de autoría que las superficies de edición wiki tradicionales no ofrecen.

**Subrayado de cumplimiento BCSC** — el editor actualmente aplica siete reglas deterministas SAA mediante subrayados de color. El conjunto completo planificado incluye detección de declaraciones prospectivas, señalización de vocabulario prohibido, detección de tiempo presente indebido para la Sovereign Data Foundation, señalización de comparación competitiva y solicitudes de cita requerida. Esto se construye dentro de la propia superficie de edición, en lugar de aplicarse como una verificación de cumplimiento posterior a la publicación.

**Por qué importa:** estas tres primitivas son lo que la plataforma tiene previsto ofrecer que ningún wiki existente ofrece — la paridad con Wikipedia cierra la brecha con las expectativas de los lectores actuales, y esta capa está pensada para ser la razón de elegir esta plataforma sobre una alternativa igualmente parecida a Wikipedia.

## Diseño móvil primero y mejora progresiva

El wiki está diseñado con enfoque móvil primero: la maquetación, la navegación y la tabla de contenidos se renderizan de forma correcta y usable en una ventana de 375 px antes de cualquier mejora progresiva para pantallas más amplias. Los usuarios de escritorio reciben la maquetación completa de barra lateral más contenido como mejora; los usuarios de móvil reciben la experiencia completa de lectura y edición sin una alternativa reducida.

### Áreas táctiles y paridad móvil

La disciplina de área táctil sigue el Criterio de Éxito 2.5.8 de las WCAG 2.2: todos los elementos interactivos — entradas del índice, lápices de edición, enlaces de navegación, botones de alternancia — llevan un área táctil mínima de 44 px × 44 px. Las interacciones no dependen de estados hover; toda funcionalidad accesible por hover es igualmente accesible por toque. Se aplica relleno de zona segura (`env(safe-area-inset-*)`) al cromo del contorno para acomodar pantallas con muesca y dynamic island.

El objetivo de memoria muscular se extiende al móvil. Los patrones de navegación de la aplicación Wikipedia informan la maquetación móvil — volver arriba, deslizar entre categorías, búsqueda en barra inferior — no una "versión móvil" reducida que parezca un recurso de emergencia. Es el mismo principio leapfrog aplicado al factor de forma: alcanzar primero la paridad completa con Wikipedia móvil y luego añadir la capa diferenciadora.

**Por qué importa:** un lector en un teléfono obtiene la misma experiencia completa de lectura y edición que un lector frente a un escritorio — el móvil nunca es la opción degradada.

## Posicionamiento estructural

Las plataformas wiki existentes construidas sobre modelos de organización jerárquica — libros, capítulos, espacios, carpetas — rompen el grafo plano de hipervínculos que hace útil a Wikipedia. Un wiki jerárquico crea silos de conocimiento; un wiki plano con un DAG de categorías crea un patrimonio común de conocimiento.

Las plataformas que imponen organización jerárquica típicamente carecen de enlaces rojos (la señal de que falta una página y debería crearse), de enlaces entrantes, de navboxes y del marco completo de páginas especiales. Varias carecen por completo de páginas de discusión.

`app-mediakit-knowledge` está diseñado como un motor wiki de archivos planos, respaldado por git y nativo de Rust, orientado a la paridad completa de memoria muscular de Wikipedia para PYMEs reguladas que operan bajo obligaciones de divulgación continua.

**Por qué importa:** un wiki plano y enlazado por categorías mantiene cada artículo a un solo salto de sus vecinos — un lector nunca tiene que adivinar en qué carpeta o espacio se archivó un tema para encontrarlo.

## Véase también

- [[app-mediakit-knowledge]] — descripción de la aplicación, configuración de despliegue y hoja de ruta por fases
- [[leapfrog-2030-architecture]] — doctrina Leapfrog 2030 y ocho inventos del marco
- [[source-of-truth-inversion]] — el patrón de almacenamiento (git canónico, vista derivada) que implementa el motor wiki
- [[compounding-substrate]] — el patrón de compounding que implementa el pilar wiki
