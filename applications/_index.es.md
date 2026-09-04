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
last_edited: 2026-09-04
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
- [[app-mediakit-knowledge]] — Motor wiki Rust de binario único que sirve documentation.pointsav.com — una vista sobre un árbol Markdown donde los commits son canónicos y el binario es descartable.
- [[app-mediakit-marketing]] — app-mediakit-marketing es un servidor web en Rust que entrega sitios de marketing a partir de manifiestos de página tipados — la IA redacta vía MCP, un humano aprueba antes de que algo se publique. Sirve home.woodfinegroup.com y home.pointsav.com.
- [[knowledge-wiki-home-page-design|Diseño de la página de inicio del wiki]] — Cómo la página de inicio de documentation.pointsav.com hereda las convenciones estructurales de Wikipedia y las extiende para lectores técnicos y del ámbito financiero.
- [[wikipedia-leapfrog-design|Diseño de salto sobre Wikipedia]] — Qué hereda el motor wiki app-mediakit-knowledge de Wikipedia, qué añade más allá de él, y qué significa el 5% de margen leapfrog para lectores e ingenieros.
- [[documentation-pointsav-com-launch-2026-04-27|Lanzamiento de documentation.pointsav.com]] — El lanzamiento con TLS de documentation.pointsav.com en abril de 2026: pila de servicio, postura de marcador de posición, fundamento de divulgación y comandos de verificación.
- [[radical-proofreader-ui|Consola del corrector]] — Cartucho de contenido de terminal para la canalización service-proofreader — el operador envía texto, revisa los hallazgos y registra un veredicto binario aceptar/rechazar que alimenta el corpus de aprendizaje.
<!-- END AUTO-GENERATED -->

## Inteligencia de ubicación

El motor de análisis GIS, el artículo de plataforma que lo enmarca junto a la capa de renderizado y la intención de diseño de experiencia de usuario.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: location-intelligence-applications -->
- [[app-orchestration-gis]] — El pipeline de datos en Python que produce las clasificaciones de co-ubicación de Woodfine y el mapa interactivo — geometría de clústeres reconstruida en un ciclo nocturno a partir de los conjuntos de datos de origen, publicada como mosaicos de mapa estáticos.
- [[location-intelligence-platform|Plataforma de inteligencia de ubicación]] — Aplicación GIS de archivos planos propiedad del cliente para análisis de clústeres minoristas y selección de sitios, que une una canalización de puntuación nocturna con una capa de renderizado interactiva.
- [[location-intelligence-ux|Experiencia de inteligencia de ubicación]] — La filosofía de diseño Conclusión Primero: conclusiones de nivel ordenadas en lugar de puntos de datos individuales, para que los usuarios vean los nodos comerciales más defendibles a zoom nacional antes de profundizar en operadores individuales.
<!-- END AUTO-GENERATED -->

## Superficies de entrada y desarrollo

La puerta de entrada estructurada que admite archivos externos a un Totebox, y el workbench en navegador para trabajar con archivos sin una sesión de terminal.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: input-and-developer-surfaces -->
- [[app-console-input]] — app-console-input es la superficie F12 en os-console — una ruta, una confirmación y un envío, a través de los cuales los archivos externos sin procesar ingresan a un Totebox antes de sellarse en el libro mayor verificado.
- [[app-privategit-workbench|Workbench de PrivateGit]] — Editor de archivos en navegador incluido en os-privategit, con interfaz de tres columnas — árbol, visor y editor — para trabajar en el árbol del clúster sin terminal.
- [[app-console-keys|Chasis de la consola]] — app-console-keys es el chasis base siempre instalado de os-console. Proporciona el rasgo Cartridge que implementan todos los módulos de la consola, la barra de navegación de teclas de función, la barra de estado y el cliente de autorización basada en máquina.
- [[app-console-email|Cartucho de comunicaciones]] — app-console-email es el cartucho de comunicaciones F3 de os-console. Proporciona listado de bandeja de entrada, lectura de mensajes y redacción y envío, operando a través de service-email como el Diodo de Comunicaciones entre el operador y los corresponsales externos.
- [[app-console-slm|Consola de monitorización SLM]] — Cartucho de consola en terminal que muestra el estado en vivo de la infraestructura de inferencia — salud del modelo, la flota GPU de ráfaga, profundidad de cola y gasto diario — de solo lectura, sin controles propios.
<!-- END AUTO-GENERATED -->

## Aplicaciones de dominio

Superficies dedicadas a un dominio operativo específico — Modelado de Información de Edificios y flujos de trabajo de propiedad inmobiliaria.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: domain-applications -->
- [[bim-and-real-property-surfaces|Superficies BIM y propiedad inmobiliaria]] — Cómo PointSav trata el Modelado de Información de Construcción como un dominio operativo distinto — un sistema de diseño de nivel cliente separado, una ubicación real en el Plan de Cuentas y superficies de consola específicas de BIM aún en fase de investigación.
<!-- END AUTO-GENERATED -->

Artículos adicionales planificados para este dominio — herramientas del sistema de diseño para BIM, convenciones de interfaz AEC y la brecha entre las herramientas de autoría BIM y los flujos de trabajo del gestor inmobiliario — aún no están escritos.

## Herramientas financieras y de construcción

Una familia de herramientas de libro contable bajo control del propietario que comparten un mismo diseño de partida doble: contabilidad, control de costo/cronograma/calidad de construcción y nómina. Las tres ya tienen código real en funcionamiento — el motor de libro contable de tool-accounting, el motor de costo/cronograma/informes de tool-construction, y el primer informe de tool-payroll — aunque la profundidad de lo construido varía ampliamente entre las tres.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: financial-and-construction-tools -->
- [[financial-and-construction-tools-overview|financial-and-construction-tools-overview]] — Cómo se relacionan tool-accounting, tool-construction y tool-payroll como una sola familia de productos — un diseño compartido de partida doble, alimentaciones de datos unidireccionales entre ellos y un límite compartido de arquitectura gratuita/pagada.
- [[tool-accounting|tool-accounting]] — Un motor de contabilidad de partida doble, en archivos planos y de propiedad del titular, que produce estados financieros auditables a partir de diarios en texto plano; su motor central y su renderizador PDF/HTML están construidos, verificados contra datos históricos reales multi-entidad, y operados por una cadena de herramientas CLI real de binarios de estados, libro mayor, narrativa y línea de tiempo — solo CLI, sin superficie de consola todavía.
- [[tool-construction|tool-construction]] — Un libro contable de archivos planos, bajo control del propietario, para el costo, cronograma y control de calidad de la construcción, sobre la misma disciplina de partida doble que tool-accounting; el motor central ya funciona como CLI real, contabilizando los estimados de un piloto en vivo a través de las cuatro cadenas de tipo de costo — solo en etapa de estimación y sin superficie de consola todavía.
- [[tool-payroll|tool-payroll]] — Un motor de nómina y remesas estatutarias sensible a la jurisdicción cuyo primer informe real — un Registro de Nómina por división que agrega las horas laborales presupuestadas del piloto de construcción bajo una fila citada de reglas salariales de una sola jurisdicción — está construido y en funcionamiento; el cálculo bruto-a-neto, la frecuencia de pago y el cálculo de remesas siguen siendo solo diseño.
<!-- END AUTO-GENERATED -->

## Véase también

- [Servicios de la Plataforma](/services/) — la capa de servicios sobre la que construyen las aplicaciones
- [Sistemas Operativos](/systems/) — los sistemas operativos que alojan las aplicaciones
- [Cómo Está Construido](/architecture/) — el modelo de tres anillos y los principios de propiedad del cliente
- [Diseño y Marca](/design-system/) — el vocabulario de tokens y componentes que hereda el cromo de las aplicaciones
