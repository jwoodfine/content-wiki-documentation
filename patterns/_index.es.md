---
schema: foundry-doc-v1
title: "Patrones de Diseño"
slug: patterns-index
category: patterns
type: topic
content_type: topic
quality: complete
short_description: "La categoría de patrones recoge patrones de diseño nombrados realizados a través de la plataforma — inversión de la fuente de verdad, emparejamiento-como-permiso, runtime sin contenedores, enrutamiento sin ejecución, orden cliente-primero, disciplina de niveles de modelo, patrones de despliegue, el relevo de paso directo, la arquitectura de salto del wiki de conocimiento y la experiencia de inteligencia de ubicación — cada uno una forma recurrente aplicada en la capa editorial, de interfaz o de coordinación."
index_type: thematic
index_scope: patterns
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-09-04
editor: pointsav-engineering
paired_with: _index.md
---

La categoría **patrones** recoge patrones de diseño nombrados realizados a través de la plataforma. Un patrón en esta categoría es una forma recurrente — aplicada en la capa editorial, de interfaz o de coordinación — que resuelve un problema estructural de una manera que otras partes de la plataforma reutilizan. Los patrones se diferencian de los sustratos: un sustrato es un mecanismo portante del que depende la plataforma (y que se compone con el tiempo); un patrón es una decisión de diseño que puede aplicarse o no. Los patrones se diferencian de la arquitectura: un artículo de arquitectura describe cómo se compone un sistema específico; un patrón describe una forma que se repite en sistemas.

Los patrones de esta colección se sitúan sobre el [[compounding-substrate|sustrato compuesto]] y la [[three-ring-architecture|arquitectura de tres anillos]] — describen cómo la plataforma expresa esos fundamentos en formas recurrentes y nombradas.

<!-- START-HERE-HIGHLIGHT: el motor lee este bloque para la tarjeta "empezar aquí"
     (reutiliza el componente cluster-card--start-here existente). No añadir más de una. -->

**Empiece aquí:** lea primero [[source-of-truth-inversion|inversión de la fuente de verdad]] y [[pairing-as-permission|emparejamiento-como-permiso]] — son los patrones portantes sobre los que se construyen los demás.

<!-- END-START-HERE-HIGHLIGHT -->

## Patrones de soberanía e infraestructura

Los compromisos estructurales que definen qué es y qué no es un despliegue de PointSav.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: sovereignty-and-infrastructure-patterns -->
- [[source-of-truth-inversion|Inversión de la fuente de verdad]] — La inversión de origen de verdad designa una capa de almacenamiento como canónica (el registro autorizado, comprometido y firmado), una segunda como una vista derivada (reconstruida determinísticamente bajo demanda), y una tercera como efímera de sesión (estado colaborativo descartado hasta confirmación explícita).
- [[pairing-as-permission|Emparejamiento-como-permiso]] — El principio de control de acceso por Capacidades de Objeto — un emparejamiento criptográfico es el permiso, y su ausencia hace inexistente el camino — tal como se manifiesta en la admisión de nodos basada en máquinas de la plataforma.
- [[zero-container-runtime|Runtime sin contenedores]] — El compromiso estructural de que todo despliegue de PointSav se ejecuta como un binario Linux bajo systemd en una máquina virtual simple o hardware bare-metal, sin tiempo de ejecución de contenedores ni orquestador.
- [[zero-execution-routing|Enrutamiento sin ejecución]] — Las plantillas públicas de la página de inicio de la plataforma usan un patrón de casilla CSS nativa para el cambio de idioma y elementos interactivos, junto con una pequeña cantidad de JavaScript del lado del cliente para la integridad de página y analítica.
- [[customer-first-ordering|Orden cliente-primero]] — El principio de que un proveedor de software que construye algo que un cliente instalará debe construirlo en el mismo orden que el cliente lo instalará, en el mismo sustrato que el cliente usará.
- [[customer-hostability|Alojabilidad por el cliente]] — El compromiso arquitectónico de que cada artefacto se ejecute en el propio hardware del cliente, contra las propias claves del cliente, con el propio libro de auditoría del cliente.
- [[totebox-archives-as-the-asset|Los Archivos Totebox como el activo]] — Por qué un Archivo Totebox se diseña como una unidad de datos autónoma y libremente transferible, en lugar de un registro de base de datos propiedad de la plataforma que lo creó.
- [[city-code-as-composable-geometry|El código urbanístico como geometría componible]] — Un patrón de composición previa que codifica los requisitos normativos en las especificaciones de los elementos como restricciones geométricas y numéricas, en lugar de aplicarlos después del diseño, de modo que una configuración no conforme no llega a poder colocarse.
<!-- END AUTO-GENERATED -->

## Despliegue y configuración

Las configuraciones canónicas en las que se envía el sustrato y las disciplinas que mantienen los despliegues componibles.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: deployment-and-configuration -->
- [[deployment-patterns|Patrones de despliegue]] — Los patrones de despliegue describen las seis configuraciones canónicas en las que se despliega el sustrato PointSav — cada una basada en los mismos cinco primitivos y la misma superficie de SO, con el Plan de Cuentas y la superficie de cumplimiento adaptados por segmento.
- [[three-layer-architecture|Arquitectura de tres capas]] — Cómo los entregables PointSav se mueven a través de las capas SOFTWARE, SHOWCASE e INSTANCE con un flujo estricto unidireccional de proveedor a cliente.
- [[3-layer-stack|Pila de tres capas]] — La descomposición de infraestructura en tres capas: capacidad de cómputo bruta, ejecución de plataforma aislada y acceso seguro del operador.
- [[customer-tier-catalog-pattern|Patrón de catálogo en el nivel cliente]] — Disciplina catálogo-instancia en el nivel cliente — definiciones de despliegue reutilizables en git; instancias específicas de cada copia fuera de los repositorios compartidos.
<!-- END AUTO-GENERATED -->

## Colaboración y flujo de trabajo editorial

Patrones que gobiernan cómo múltiples sesiones, múltiples motores y múltiples humanos colaboran sin corromper el registro canónico.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: collaboration-and-editorial-workflow -->
- [[collab-via-passthrough-relay|Colaboración mediante relé de paso]] — Un diseño de edición colaborativa en tiempo real que no conservaba estado de documento en el servidor, reenviando actualizaciones CRDT directamente entre clientes — implementado en el motor wiki y luego retirado.
- [[model-tier-discipline|Disciplina de niveles de modelo]] — El Doorman enruta cada solicitud de inferencia a uno de tres niveles de cómputo — local, ráfaga en GPU, o API externa — según una indicación de complejidad y el estado presupuestario en vivo, no una elección directa del solicitante.
- [[multi-engine-session-coordination|Coordinación de sesiones multimotor]] — Cómo múltiples motores de IA coordinan sobre el mismo espacio de trabajo sin competir por el `.git/index` ni por el estado de sesión del otro.
- [[mailbox-atomicity|Atomicidad de buzón]] — La primitiva atómica de buzón que mantiene consistentes los traspasos entrada/salida entre sesiones bajo escrituras concurrentes.
<!-- END AUTO-GENERATED -->

## Interfaz y experiencia de usuario

Patrones que se repiten en el cromo orientado al operador — el wiki, la superficie de inteligencia de ubicación, la familia de escritorio.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: interface-and-user-experience -->
- [[knowledge-wiki-leapfrog-architecture|Arquitectura de salto del wiki de conocimiento]] — Estrategia de motor wiki que sirve Markdown plano desde git con interfaz al estilo Wikipedia, alcanzando paridad de memoria muscular antes de la capa de diferenciación.
- [[location-intelligence-ux|Experiencia de inteligencia de ubicación]] — Filosofía de interfaz Conclusion-First que renderiza conclusiones clasificadas en lugar de puntos de datos, destacando de inmediato los nodos comerciales defendibles.
- [[wikipedia-leapfrog-design|Diseño de salto sobre Wikipedia]] — Qué hereda el motor wiki de Wikipedia, qué añade más allá y qué significa el margen de salto del cinco por ciento.
- [[federation-via-content-mounts|Montajes de contenido y federación]] — El motor wiki renderiza artículos curados comprometidos directamente en su repositorio junto con contenido montado desde directorios locales separados, compartiendo una superficie de URL e índice de búsqueda.
- [[aec-interface-conventions|Convenciones de interfaz AEC]] — Las herramientas de autoría BIM de toda la industria comparten un vocabulario de interfaz común — una jerarquía espacial, un panel de propiedades de elementos, una vista 3D y vistas guardadas — porque se construyen sobre el mismo modelo de datos IFC subyacente. La capa de interfaz planificada del Sistema de Diseño de la Construcción reutiliza ese vocabulario en lugar de inventar uno nuevo, y está pensada para extenderlo a los flujos de trabajo de gestión de instalaciones.
<!-- END AUTO-GENERATED -->

## Véase también

- [Bloques de Construcción](/substrate/) — mecanismos fundamentales sobre los que se construyen los patrones
- [Cómo Está Construido](/architecture/) — arquitectura concreta de la plataforma
- [Aplicaciones](/applications/) — aplicaciones orientadas al operador que componen estos patrones
- [Sistemas Operativos](/systems/) — los sistemas operativos en los que se realizan los patrones
