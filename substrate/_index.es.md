---
schema: foundry-doc-v1
title: "Bloques de Construcción"
slug: substrate-index
category: substrate
type: topic
content_type: topic
quality: complete
short_description: "La categoría de sustrato recoge los conceptos fundacionales de mecanismo de la plataforma — el Sustrato Compuesto, el Sustrato de Aprendizaje, el Sustrato de Citación, el Sustrato de Divulgación, el Sustrato de Trayectoria, el Sustrato de Protocolo Lingüístico, y las disciplinas y primitivas que los componen — cada uno describiendo una propiedad estructural en la que la plataforma se apoya en lugar de un servicio o sistema específico."
index_type: thematic
index_scope: substrate
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-09-04
editor: pointsav-engineering
paired_with: _index.md
---

La categoría **sustrato** recoge los conceptos fundacionales de mecanismo de la plataforma. Cada sustrato nombra una propiedad estructural en la que la plataforma se apoya — no un servicio o sistema específico, sino un patrón que compone servicios, sistemas y contenido en un todo coherente.

La categoría responde a preguntas como: *¿qué hace que la plataforma mejore continuamente sin renunciar a la propiedad de los datos? ¿qué hace que las citaciones sean auditables por máquina? ¿qué hace que las divulgaciones cumplan estructuralmente? ¿qué hace que el trabajo del colaborador retroalimente el entrenamiento del modelo?* Los artículos aquí describen los mecanismos; las categorías de arquitectura, servicios y sistemas describen cómo se realizan en componentes concretos.

<!-- START-HERE-HIGHLIGHT: el motor lee este bloque para la tarjeta "empezar aquí"
     (reutiliza el componente cluster-card--start-here existente). No añadir más de una. -->

**Empiece aquí:** lea primero [[compounding-substrate]] — es el patrón canónico que PointSav administra y el marco que hace legibles los demás sustratos. Después lea [[apprenticeship-substrate]], [[citation-substrate]] y [[disclosure-substrate]].

<!-- END-START-HERE-HIGHLIGHT -->

## Sustratos nombrados principales

Los nueve sustratos nombrados: cada uno designa una propiedad estructural de la que depende la plataforma.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: core-named-substrates -->
- [[compounding-substrate]] — Patrón arquitectónico que une código de plataforma abierto, una capa de datos determinista sin IA y una capa de inteligencia opcional que genera señal de entrenamiento compuesta.
- [[apprenticeship-substrate]] — Mecanismo de plataforma que enruta el trabajo primero por un modelo de lenguaje pequeño local y captura veredictos sénior firmados como pares de preferencia de entrenamiento.
- [[citation-substrate]] — Registro YAML de citas de ámbito de plataforma con detección de deriva que hace la procedencia auditable por máquina, del instrumento regulatorio a la afirmación publicada.
- [[disclosure-substrate]] — Mecanismo que convierte una wiki Markdown con control de versiones en el registro principal de divulgación continua, con cadenas de autoría firmadas y hashes criptográficos.
- [[trajectory-substrate]] — El mecanismo de plataforma que convierte trabajo operativo — commits, sesiones, retroalimentación de operador — en tuplas de capacitación JSONL estructuradas, enrutándolas en un corpus de preentrenamiento continuado que mejora el modelo base OLMo a lo largo del tiempo.
- [[language-protocol-substrate]] — El mecanismo de enrutamiento que transporta el registro, tipo de documento y destino declarados de un borrador entre archivos — un campo de portada, una tabla de enrutamiento y una convención de buzón, no un sistema de adaptadores de IA.
- [[design-system-substrate]] — El sustrato del sistema de diseño es un motor de sistema de diseño auto-alojado y propiedad del cliente que almacena tokens y componentes en el repositorio Git del cliente, los sirve a través de un extremo MCP legible por máquina, y utiliza el formato de token DTCG de W3C para permanecer agnóstico del editor.
- [[location-intelligence-substrate]] — Una arquitectura de SIG plano y abierto que permite a los clientes poseer conjuntos de datos geográficos de extremo a extremo usando datos abiertos con licencia Apache y una pila de renderización alineada con Rust de código abierto, con análisis de coubicación de venta minorista como la primera superficie implementada.
- [[retail-co-location-tier-methodology]] — El sistema de condiciones de cuatro niveles (Regional/Distrital/Local/Marginal) que clasifica los clústeres de co-ubicación minorista — composición, rango de captación, respaldo cívico, no solapamiento.
- [[brief-queue-substrate]] — Una cola persistente respaldada en archivos que hace viable el apagado inactivo de Yo-Yo sin perder datos del corpus de aprendizaje — la capa de durabilidad del sustrato SLM de tres niveles.
- [[gis-as-bim-substrate|El SIG como sustrato del BIM]] — Qué ofrece el conjunto de datos de coubicación a una tubería de composición BIM: el manifiesto de agrupaciones y sus campos enlazables, la profundidad de resolución regional, las capas de contexto cívico y las garantías de estabilidad con las que puede contar un consumidor posterior.
- [[bim-object-specification|Especificación de Objeto BIM]] — La unidad de especificación reutilizable de elementos de construcción de la plataforma: un conjunto fijo de categorías primitivas ancladas a estándares abiertos (IFC, Uniclass, bSDD), cada una portando tres capas de información a la vez — qué es, qué exige su jurisdicción, y qué exige su clima.
<!-- END AUTO-GENERATED -->

## El Doorman compuesto y la frontera de IA

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: compounding-doorman-and-ai-boundary -->
- [[compounding-doorman]] — El patrón operativo en el corazón de sustratos de IA soberana: un único servicio que media cada llamada de cómputo externa, registra cada evento en un libro mayor de auditoría y acumula señal de capacitación que compone el sustrato a lo largo del tiempo.
- [[mcp-substrate-protocol]] — Cada servicio del Anillo 1 y Anillo 2 expone una interfaz de servidor MCP como su contrato externo primario, con el Portero actuando como la puerta de enlace MCP.
- [[adapter-composition]] — La metáfora del sistema operativo para la IA en PointSav — el Doorman como kernel, los adaptadores como procesos, service-content como sistema de archivos — y el álgebra que ensambla inteligencia por solicitud a partir de capas de adaptadores LoRA.
- [[knowledge-graph-grounded-apprenticeship]] — El Portero busca entidades coincidentes en el grafo de conocimiento por inquilino antes de despachar una solicitud, fundamentando la respuesta del modelo en hechos que el grafo ya contiene.
- [[single-boundary-compute-discipline]] — Todo el tráfico de inferencia de IA en un despliegue de la plataforma pasa exclusivamente por el Portero, con la omisión estructuralmente impedida a nivel de kernel.
<!-- END AUTO-GENERATED -->

## Pila de Modelo de Lenguaje Pequeño

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: small-language-model-stack -->
- [[llm-substrate-decision]] — La justificación para seleccionar OLMo 3 como sustrato de inferencia local y en GPU: la única familia de modelos completamente abierta — datos, código de entrenamiento y puntos de control incluidos — que permite el preentrenamiento continuo y satisface la postura de adquisición de una empresa pública canadiense.
- [[four-tier-slm-substrate]] — Un camino gradual hacia la soberanía en IA: cuatro niveles de despliegue para el cliente, desde una pasarela de API sin modelo local hasta un servicio de IA especializado entrenado sobre el corpus agregado del proveedor, donde cada nivel añade capacidad sin romper la garantía del nivel inferior.
- [[yoyo-compute-substrate]] — El substrato de cómputo de tres anillos que permite a service-slm activar y desactivar cómputo GPU mientras retiene estado, acumula habilidad y produce un ledger de auditoría de cada evento de inferencia.
- [[yo-yo-lora-training-pipeline]] — La tubería nocturna de dos fases en Yo-Yo #1: Fase 1 ejecuta extracción de entidad para el DataGraph empresarial; Fase 2 entrena un adaptador LoRA contra corpus de ingeniería y aprendizaje usando QLoRA en una única GPU L4.
- [[tui-corpus-producer]] — Cada interacción del operador con service-slm a través de la interfaz de terminal es una contribución curada al corpus de entrenamiento del adaptador por inquilino.
- [[nightly-datagraph-rebuild]] — El proceso programado que reconstruye el grafo de conocimiento de la plataforma cada noche. Existe un punto de control de aprobación humana para las entidades extraídas por IA, pero es opcional — un operador debe habilitarlo; por defecto, las escrituras automatizadas llegan al grafo sin revisión por elemento.
- [[ontological-datagraph]] — Grafo de conocimiento organizativo de personas, empresas, proyectos y relaciones — memoria semántica persistente para responder consultas de negocio sin releer documentos fuente.
- [[soft-slm-tiered-gateway]] — Una pasarela de inferencia por niveles que enruta las solicitudes de IA primero al modelo local, escalando a nodos GPU remotos y APIs externas solo cuando el nivel local no puede responder — minimizando la latencia, el coste y la exposición de datos mientras se mantiene la capacidad completa bajo demanda.
<!-- END AUTO-GENERATED -->

## Primitivas criptográficas y de micronúcleo

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: cryptographic-and-microkernel-primitives -->
- [[sel4-microkernel-substrate]] — Micronúcleo seL4 formalmente verificado, sustrato L1 compartido y planificado de PointSav — aún no es el núcleo en ejecución de cada miembro de la familia de SO tal como se distribuye hoy.
- [[merkle-proofs-as-substrate-primitive]] — Las pruebas de Merkle son el mecanismo criptográfico que permite al sustrato de la plataforma garantizar — a cualquier tercero, sin necesidad de confianza previa — que un registro específico forma parte de un registro de sólo-adición y que ese log no ha sido reescrito entre dos puntos de observación.
- [[capability-ledger-substrate]] — El Sustrato del Libro de Capacidades es el mecanismo por el cual cada decisión de control de acceso en un despliegue de plataforma se convierte en un evento criptográficamente auditable, anclado en un registro que controla el cliente.
- [[system-substrate-doctrine]] — La arquitectura de nivel de kernel bajo cada servicio de PointSav — un registro de capacidades con raíz en el cliente, una estrategia de SO soberana de dos bases, y mecanismos para capacidades de tiempo limitado, verificación reproducible y recuperación universal.
- [[capability-geometry]] — Geometría de Capacidades es el término de PointSav para la autorización basada en seL4, que reemplaza la política de control de acceso mutable por un DAG de capacidades aplicado formalmente por el kernel.
- [[moonshot-toolkit-build-orchestrator]] — Orquestador de construcción solo Rust para imágenes unikernel seL4 — de especificación TOML a manifiesto direccionado por contenido y elfloader AArch64, sin Python ni CMake.
- [[sel4-aarch64-qemu-substrate-target]] — Base de hardware de la plataforma unikernel — seL4 verificado formalmente sobre AArch64 con la máquina virt de QEMU para desarrollo, pruebas y CI.
- [[sel4-unikernel-substrate]] — os-console está previsto para ejecutarse como imagen unikernel seL4 Microkit en su forma de producción final, compilando el código de la aplicación directamente con un kernel formalmente verificado para eliminar la superficie de ataque de un SO de propósito general.
<!-- END AUTO-GENERATED -->

## Soberanía y propiedad del cliente

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: sovereignty-and-customer-ownership -->
- [[sovereign-ai-commons]] — El posicionamiento de PointSav como administrador de infraestructura de IA abierta y compartida para pequeñas y medianas empresas reguladas: cinco propiedades estructurales que los grandes proveedores de servicios en la nube no pueden ofrecer sin desmantelar sus propios modelos de facturación.
- [[knowledge-commons]] — El modelo económico que separa lo que PointSav publica libremente de lo que vende — artefactos de conocimiento bajo licencias abiertas, servicio de pago en el punto de agregación multi-Totebox.
- [[customer-owned-graph-ip]] — El grafo de conocimiento por inquilino y los pesos del adaptador entrenado son propiedad intelectual del cliente, portátiles y exportables sin aprobación del proveedor.
- [[tier-zero-customer-side-sovereign-specialist]] — El Nivel 0 Totebox es un despliegue especialista soberano que funciona en el propio hardware del cliente sin ninguna dependencia de nube requerida y sin conectividad a internet requerida.
- [[substrate-without-inference-base-case]] — El Archivo Totebox permanece completamente operativo y transferible libremente incluso cuando no hay ningún nivel de inferencia de IA disponible; el substrato determinístico es la base estructural.
- [[substrate-native-compatibility]] — Establece compatibilidad estructural con convenciones de lector e integrador de MediaWiki mientras rechaza deliberadamente la mimicría de API, manteniendo interfaces nativas de sustrato que reducen carga de mantenimiento y evitan obligaciones de divulgación ligadas a garantías de compatibilidad.
<!-- END AUTO-GENERATED -->

## Mecánicas de plataforma

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: platform-mechanics -->
- [[code-for-machines-first]] — Cada contrato entre servicios, registro de auditoría, configuración y ontología es legible por máquinas como superficie primaria; las interfaces para humanos son capas sobre APIs primero-para-máquinas.
- [[seed-taxonomy-as-smb-bootstrap]] — Cada despliegue de inquilino provisiona una taxonomía semilla de cuatro partes — Arquetipos, Plan de Cuentas, Dominios, Temas — como el arranque del grafo de conocimiento.
- [[reverse-flow-substrate]] — La puerta de enlace del Portero y el registro de auditoría que aplican la disciplina de datos de entrada están planificados para también aplicar flujos comerciales de salida — mercado de datos e intercambio de anuncios — ambos opt-in por inquilino.
<!-- END AUTO-GENERATED -->

## Véase también

- [Cómo Está Construido](/architecture/) — arquitectura transversal de la plataforma
- [Patrones de Diseño](/patterns/) — patrones de diseño nombrados realizados sobre sustratos
