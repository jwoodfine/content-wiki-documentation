---
schema: foundry-doc-v1
title: "Cómo Está Construido"
slug: architecture-index
short_description: "Arquitectura de plataforma transversal: el modelo de composición de tres anillos, límite de enrutamiento e inferencia de IA, sustrato de seguridad e identidad, principios de propiedad del cliente y el dominio de inteligencia de ubicación."
lang: es
category: architecture
type: topic
content_type: topic
quality: complete
index_type: thematic
index_scope: architecture
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-09-04
editor: pointsav-engineering
paired_with: _index.md
---

PointSav se compone de tres anillos concéntricos con dependencias estrictamente unidireccionales, una canalización de datos determinista que funciona completamente sin IA, y una disciplina de soberanía que permite a los clientes bifurcar toda la pila el primer día. Los artículos de arquitectura describen las decisiones estructurales que sustentan esas propiedades: por qué están diseñadas así, cómo se componen y qué invariantes deben mantenerse en cada despliegue.

El modelo de tres anillos es el marco de carga: el Anillo 1 gestiona la ingesta por inquilino, el Anillo 2 proporciona conocimiento y procesamiento determinista, y el Anillo 3 añade inferencia de IA opcional que nunca escribe en el registro autoritativo.

<!-- START-HERE-HIGHLIGHT: el motor lee este bloque para la tarjeta "empezar aquí"
     (reutiliza el componente cluster-card--start-here existente). No añadir más de una. -->

**Empiece aquí:** [[three-ring-architecture]] — el marco de carga que asume cada otro artículo de esta categoría: tres anillos concéntricos con dependencias estrictamente unidireccionales, IA estructuralmente opcional en todo momento.

<!-- END-START-HERE-HIGHLIGHT -->

## Estructura de la plataforma

Los artículos estructurales fundacionales — los patrones que componen cada despliegue PointSav.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: platform-structure -->
- [[three-ring-architecture]] — El patrón de composición duradero para la plataforma PointSav: tres anillos concéntricos con dependencias estrictamente unidireccionales, donde el anillo de IA es estructuralmente opcional y la canalización de datos determinista funciona completamente sin él.
- [[3-layer-stack]] — El Three-Layer Stack es el patrón de descomposición de infraestructura utilizado en todas las implementaciones de PointSav, separando la capacidad de cómputo puro, la ejecución de plataforma aislada y el acceso seguro del operador en tres capas distintas.
- [[three-layer-architecture]] — Flujo estrictamente unidireccional de los entregables de PointSav por tres capas: monorepo del proveedor, catálogo escaparate del cliente e instancias privadas en ejecución.
- [[six-tier-sovereignty-matrix]] — Seis prefijos fijos de directorio que organizan el monorepo de PointSav por propósito, haciendo el repositorio autodocumentado y reforzando la higiene de dependencias.
- [[foundry-doctrine-overview]] — El alcance planificado para la futura carta constitucional de PointSav — aún no ratificada ni redactada; descrita aquí solo en términos planificados/previstos.
- [[leapfrog-2030-architecture]] — Tesis de posicionamiento estructural que combina hardware, datos y pesos de adaptador propiedad del cliente con ingresos por transacción en lugar de suscripción.
- [[pointsav-overview]] — PointSav Digital Systems es un proveedor de tecnología que construye sistemas operativos soberanos y con capacidad de instalación local para gestión de registros y administración empresarial. Se encuentra dentro de una estructura de tres organizaciones establecida por Woodfine Capital Projects Inc.
- [[architecture]] — La consistencia criptográfica de la plataforma se apoya en un registro real encadenado por Merkle; la capacidad de arranque soberana — colapsar un despliegue en una sola imagen portátil — es un objetivo de diseño, aún no una función publicada.
- [[architecture-overview]] — Mapa de las principales superficies arquitectónicas de la plataforma PointSav: sustrato de cómputo, distribución de software, inteligencia GIS y el pipeline editorial.
- [[foundry-doctrine-architecture]] — El alcance planificado para una futura carta constitucional que se prevé codifique compromisos fundacionales y afirmaciones estructurales que rijan las decisiones de ingeniería de PointSav — aún no redactada ni ratificada.
- [[three-binary-architecture]] — Totebox Orchestration se entrega mediante tres entornos operativos binarios distintos — os-console, os-totebox y os-orchestration — cada uno con un rol, objetivo de despliegue y conjunto de aplicaciones diferenciados.
- [[app-orchestration-graph-federation]] — Cómo la plataforma PointSav federa los DataGraphs soberanos de cada archivo a través de una única puerta de enlace auditable, y las condiciones bajo las cuales esa puerta pasa a ser un servicio dedicado.
- [[software-distribution-substrate]] — Un sistema de tres componentes — servidor de versiones, tienda virtual y observador de pagos — que entrega binarios compilados contra pagos USDC en cadena, sin cuentas de cliente ni facturación por suscripción.
<!-- END AUTO-GENERATED -->

## Propiedad del cliente y despliegue

Los principios y mecanismos por los cuales los clientes son dueños plenos de su despliegue.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: customer-ownership-and-deployment -->
- [[customer-hostability]] — La capacidad de alojamiento del cliente es el compromiso arquitectónico de que cada artefacto de PointSav pueda ejecutarse en el hardware del cliente, contra las claves del cliente, con el libro mayor de auditoría del cliente — haciendo que la implementación autohospedada sea el patrón canónico, no un nivel.
- [[economic-model]] — La estructura comercial de dos niveles de PointSav: un nivel Community gratuito como embudo de adopción, y un nivel de Cliente PYME de pago orientado a pequeñas y medianas empresas reguladas que los modelos de facturación a hiperescala no pueden atender económicamente.
- [[direct-payment-settlement]] — El pago por transacciones del mercado está planificado para fluir directamente del comprador al inquilino-cliente; la participación de PointSav es una comisión por transacción en el momento de la liquidación, no una suscripción recurrente.
- [[totebox-orchestration-development]] — El entorno de desarrollo de PointSav está desplegado como una instancia de orquestación Totebox — el espacio de trabajo que construye la plataforma se ejecuta sobre la misma arquitectura que la plataforma entrega a los clientes.
- [[totebox-session]] — Una sesión Totebox es una sesión de colaborador asistida por IA abierta dentro de un único archivo Totebox — con alcance a los repositorios declarados del archivo, sin capacidad de escribir fuera de ellos, y es el punto de entrada estándar para todo trabajo de desarrollo en la orquestación Totebox.
- [[vertical-seed-packs-marketplace]] — PointSav tiene previsto distribuir paquetes de semilla curados específicos de la industria como taxonomías de inicio, con un mercado planificado que permite a los inquilinos contribuir mejoras.
- [[foundry-services-slice-model]] — Una reserva de memoria cgroup de systemd que protege los servicios de producción de ser desalojados por procesos pesados de compilación o investigación en el mismo host — aislamiento de un solo nodo sin Kubernetes.
- [[cargo-target-per-user-discipline]] — Particionado por usuario de la caché compartida de Cargo — CARGO_TARGET_DIR por desarrollador elimina carreras de bloqueo y errores de permisos entre usuarios.
- [[mailbox-atomicity]] — Escritura exclusiva con flock e idempotencia por msg-id en buzones de archivo plano — cómo las sesiones concurrentes serializan escrituras sin perder mensajes en silencio.
- [[multi-engine-session-coordination]] — Protocolo de bloqueos de sesión para motores de IA concurrentes en un mismo host — detección de bloqueos obsoletos por boot_id y protección del índice git compartido.
- [[os-products-distribution-model]] — os-network-admin se distribuye hoy en software.pointsav.com a $0 USDC (beta); el modelo de distribución de os-infrastructure (metal desnudo/VM en la nube) está previsto pero aún no catalogado. Ambos se entregan como artefactos firmados, licenciados y entregados en cadena.
<!-- END AUTO-GENERATED -->

## Inteligencia de ubicación y dominio

Decisiones arquitectónicas para el dominio de inteligencia de ubicación e inmuebles.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: location-intelligence-and-domain -->
- [[hardware-co-location-methodology]] — Un enfoque estructurado para clasificar candidatos de coubicación de hardware en dimensiones regulatorias, de red, de infraestructura y de costo, restringido primero por requisitos regulatorios antes de que ocurra cualquier otra optimización.
- [[flat-file-bim-leapfrog]] — El Sistema de Diseño de Edificios se construye sobre cinco restricciones — archivos planos, estándares abiertos, Rust y Tauri, funcionamiento sin conexión y licencia Apache 2.0. La propiedad anclada al activo, el uso en campo sin red, la ingesta de sensores y la convergencia del modelo con los registros de arrendamiento y financieros se derivan de la arquitectura, no se añaden encima.
- [[building-design-system]] — Una capa de coordinación planificada para el entorno construido: una biblioteca canónica y legible por máquina de especificaciones de elementos de construcción que las superficies de autoría BIM independientes consumen por referencia, de la misma manera que un sistema de diseño de software mantiene consistentes a equipos de producto independientes.
- [[asset-anchored-bim-vault]] — El registro digital autoritativo de un edificio, estructurado como archivos de texto plano y binario estandarizado en un directorio versionado con git, que califica como un Entorno de Datos Común conforme a la norma ISO 19650 y que viaja con la escritura de la propiedad.
<!-- END AUTO-GENERATED -->

Un artículo adicional planificado para el dominio de inteligencia de ubicación y BIM/inmuebles — que cubre la taxonomía regional de desarrollo — aún no está escrito.

## Véase también

- [Bloques de Construcción](/substrate/) — conceptos de mecanismo fundacionales: los sustratos compuesto, de aprendizaje, de citas y de divulgación
- [Patrones de Diseño](/patterns/) — patrones de diseño nombrados realizados en la plataforma
- [Gobernanza y Estándares](/governance/) — los registros de decisiones formales, la postura de licenciamiento y los requisitos de cumplimiento
- [Dónde Se Ejecuta](/infrastructure/) — topología de despliegue de flota, entorno en la nube e infraestructura física
