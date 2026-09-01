---
schema: foundry-doc-v1
title: "Aplicaciones"
slug: applications-index
short_description: "Aplicaciones internas y orientadas al usuario construidas sobre el sustrato de plataforma PointSav — el motor wiki, la superficie de marketing, el motor de análisis GIS, el workbench de desarrollo en navegador, la puerta de entrada de datos estructurados y los artículos de intención de diseño que enmarcan cómo se componen esas superficies."
lang: es
category: applications
type: topic
content_type: topic
quality: complete
index_type: thematic
index_scope: applications
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: _index.md
---

Las aplicaciones se sitúan por encima de la capa de servicios de tres anillos. Consumen datos deterministas y salida opcional de IA de los anillos y los presentan a través de una interfaz definida. Una aplicación no contiene datos canónicos — es una vista sobre la capa de servicios y puede ser reprovisada sin pérdida de datos apuntando una instancia nueva a los datos inmutables subyacentes. Los artículos de esta categoría cubren tanto las aplicaciones nombradas como el material de intención de diseño que explica cómo se compone cada superficie.

Cada aplicación aquí corresponde a un directorio `app-*` en el monorepo y hereda la separación de [[three-ring-architecture|arquitectura de tres anillos]]; ninguna contiene el registro autoritativo. Los artículos de cromo orientados al lector y de fundamentos de diseño se agrupan junto a los artículos de aplicación para que los operadores que evalúan una superficie puedan pasar del artículo de ingeniería a la intención de diseño sin salir de la categoría.

<!-- START-HERE-HIGHLIGHT: el motor lee este bloque para la tarjeta "empezar aquí"
     (reutiliza el componente cluster-card--start-here existente). No añadir más de una. -->

**Empiece aquí:** [[app-mediakit-knowledge]] — el motor wiki que renderiza la propia documentación que está leyendo ahora, y el ejemplo más claro del patrón central de esta categoría: una aplicación como vista desechable sobre datos canónicos confirmados en git.

<!-- END-START-HERE-HIGHLIGHT -->

## Conocimiento y editorial

El motor wiki, la superficie de marketing y los artículos de intención de diseño que describen su cromo orientado al lector.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: knowledge-and-editorial-applications -->
- [[app-mediakit-knowledge]] — Motor de wiki Rust de binario único que sirve documentation.pointsav.com — una vista sobre un árbol de markdown donde los commits de git son canónicos y el binario en ejecución es desechable.
- [[app-mediakit-marketing]] — Servidor web Rust que entrega sitios de aterrizaje de marketing desde manifiestos de página tipados — la IA redacta vía MCP, un humano aprueba antes de que algo se publique. Sirve home.woodfinegroup.com y home.pointsav.com.
- [[knowledge-wiki-home-page-design|Diseño de la página de inicio del wiki]] — Cómo la página de inicio de documentation.pointsav.com hereda las convenciones estructurales de Wikipedia y las extiende para lectores de ingeniería y de la comunidad financiera.
- [[wikipedia-leapfrog-design|Diseño de salto sobre Wikipedia]] — Qué hereda el motor wiki de Wikipedia, qué añade más allá y qué significa el margen de salto del cinco por ciento para lectores e ingenieros.
- [[documentation-pointsav-com-launch-2026-04-27|Lanzamiento de documentation.pointsav.com]] — El lanzamiento TLS de abril de 2026 de `documentation.pointsav.com`: pila de servicio, postura de marcador de posición, justificación de divulgación BCSC y comandos de verificación.
- [[radical-proofreader-ui|Consola del corrector]] — Cartucho de contenido de terminal para la canalización service-proofreader — el operador envía texto, revisa los hallazgos y registra un veredicto binario aceptar/rechazar que alimenta el corpus de aprendizaje.
<!-- END AUTO-GENERATED -->

## Inteligencia de ubicación

El motor de análisis GIS, el artículo de plataforma que lo enmarca junto a la capa de renderizado y la intención de diseño de experiencia de usuario.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: location-intelligence-applications -->
- [[app-orchestration-gis]] — La canalización de datos en Python que produce las clasificaciones de co-ubicación de Woodfine y el mapa interactivo — geometría de clústeres reconstruida en un horario nocturno a partir de conjuntos de datos fuente, publicada como mosaicos de mapa estáticos.
- [[location-intelligence-platform|Plataforma de inteligencia de ubicación]] — La plataforma completa de inteligencia de ubicación: una canalización nocturna app-orchestration-gis emparejada con una capa de renderizado interactiva; cada conjunto de datos, algoritmo y decisión de renderizado bajo el control del cliente.
- [[location-intelligence-ux|Experiencia de inteligencia de ubicación]] — La filosofía de diseño Conclusión Primero: conclusiones de nivel ordenadas en lugar de puntos de datos individuales, para que los usuarios vean los nodos comerciales más defendibles a zoom nacional antes de profundizar en operadores individuales.
<!-- END AUTO-GENERATED -->

## Superficies de entrada y desarrollo

La puerta de entrada estructurada que admite archivos externos a un Totebox, y el workbench en navegador para trabajar con archivos sin una sesión de terminal.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: input-and-developer-surfaces -->
- [[app-console-input]] — La superficie F12 en os-console: la puerta de entrada estructurada a través de la cual los archivos externos brutos entran en un Totebox antes de ser sellados en el libro verificado.
- [[app-privategit-workbench|Workbench de PrivateGit]] — Un editor de archivos de tres columnas basado en navegador incluido en os-privategit; para trabajar con archivos sin una sesión de terminal.
- [[app-console-keys|Chasis de la consola]] — El chasis base siempre instalado de os-console: define el rasgo Cartridge que implementa cada módulo de teclas de función, la barra de navegación F, la barra de estado y el cliente de autorización basada en máquina al que se conectan los demás cartuchos.
- [[app-console-email|Cartucho de comunicaciones]] — El cartucho de comunicaciones F3 de os-console: bandeja de entrada, lectura de mensajes y redacción y envío a través de la ruta de salida Diodo de Comunicaciones de service-email.
- [[app-console-slm|Consola de monitorización SLM]] — El cartucho de terminal F9 que muestra el estado en vivo de la infraestructura de inferencia de IA — salud del modelo, flota de nodos GPU, profundidad de cola y gasto diario — para el operador que gestiona un Totebox.
<!-- END AUTO-GENERATED -->

## Aplicaciones de dominio

Superficies dedicadas a un dominio operativo específico — Modelado de Información de Edificios y flujos de trabajo de propiedad inmobiliaria.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: domain-applications -->
- [[bim-and-real-property-surfaces|Superficies BIM y propiedad inmobiliaria]] — Cómo PointSav trata el Modelado de Información de Edificios como un dominio operativo distinto — un sistema de diseño de nivel cliente separado, una ubicación real en el Plan de Cuentas y superficies de consola específicas de BIM aún en fase de investigación.
<!-- END AUTO-GENERATED -->

Artículos adicionales planificados para este dominio — herramientas del sistema de diseño para BIM, convenciones de interfaz AEC y la brecha entre las herramientas de autoría BIM y los flujos de trabajo del gestor inmobiliario — aún no están escritos.

## Herramientas financieras y de construcción

Una familia de herramientas de libro contable bajo control del propietario que comparten un mismo diseño de partida doble: contabilidad, control de costo/cronograma/calidad de construcción y (propuesta) nómina. Dos de las tres ya tienen código real en funcionamiento — el motor de libro contable de tool-accounting y el motor de costo/cronograma/informes de tool-construction; tool-payroll permanece como un diseño propuesto sin código escrito.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: financial-and-construction-tools -->
- [[financial-and-construction-tools-overview|financial-and-construction-tools-overview]] — Cómo se relacionan las tres herramientas como una sola familia de productos: el diseño compartido de partida doble, las alimentaciones de datos unidireccionales entre ellas y el límite compartido de arquitectura gratuita/pagada.
- [[tool-accounting|tool-accounting]] — Un libro contable de partida doble, de archivos planos y bajo control del propietario, que produce estados financieros listos para auditoría; código real verificado contra datos históricos reales.
- [[tool-construction|tool-construction]] — Un libro contable de archivos planos, bajo control del propietario, para el costo, cronograma y control de calidad de la construcción; el motor central ya funciona como CLI real, produciendo informes de estimación de costes y cronograma para un piloto en vivo — solo en etapa de estimación, sin consola todavía.
- [[tool-payroll|tool-payroll]] — Un motor propuesto de nómina y remesas estatutarias, sensible a la jurisdicción; 100% de diseño hoy, sin código escrito.
<!-- END AUTO-GENERATED -->

## Véase también

- [Servicios](/services/) — la capa de servicios sobre la que construyen las aplicaciones
- [Sistemas](/systems/) — los sistemas operativos que alojan las aplicaciones
- [Arquitectura](/architecture/) — el modelo de tres anillos y los principios de propiedad del cliente
- [Sistema de diseño](/design-system/) — el vocabulario de tokens y componentes que hereda el cromo de las aplicaciones
