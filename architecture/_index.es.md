---
schema: foundry-doc-v1
title: "Arquitectura"
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
last_edited: 2026-08-06
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
- [[three-ring-architecture]] — Tres anillos concéntricos con dependencias estrictamente unidireccionales; la IA es estructuralmente opcional; el flujo determinista funciona plenamente sin el Anillo 3.
- [[3-layer-stack]] — La descomposición de infraestructura en tres capas: capacidad de cómputo pura, ejecución de plataforma aislada y acceso seguro del operador.
- [[three-layer-architecture]] — Cómo los entregables de PointSav transitan por las capas SOFTWARE, SHOWCASE e INSTANCIA con un flujo estrictamente unidireccional del proveedor al cliente.
- [[six-tier-sovereignty-matrix]] — La taxonomía de seis prefijos del monorepo (app-, asset-, os-, service-, system-, moonshot-) que hace estructural la higiene de dependencias.
- [[foundry-doctrine-overview]] — Resumen público del estatuto constitucional de la plataforma: seis pilares, cincuenta y cuatro afirmaciones estructurales y el modelo económico que los sustenta.
- [[leapfrog-2030-architecture]] — La visión arquitectónica Leapfrog 2030: la física de infraestructura de la era hiperescaladora de 2030 y cómo la plataforma está posicionada para beneficiarse de ella.
- [[pointsav-overview]] — PointSav Digital Systems: qué construye la empresa, cómo está organizada y la estructura corporativa de tres entidades.
- [[architecture]] — Las dos propiedades estructurales de la plataforma: consistencia criptográfica distribuida y capacidad de arranque soberano, mantenidas de forma simultánea entre la nube y bóvedas físicas desconectadas.
- [[architecture-overview]] — Un mapa de las principales superficies arquitectónicas de la plataforma: sustrato de cómputo, distribución de software, inteligencia GIS y el flujo editorial.
- [[foundry-doctrine-architecture]] — La carta constitucional en detalle: los seis pilares, las afirmaciones estructurales numeradas y las ocho invenciones de proceso adaptadas de otras industrias.
- [[three-binary-architecture]] — Los tres entornos operativos binarios — os-console, os-totebox, os-orchestration — cada uno con un rol, objetivo de despliegue y conjunto de aplicaciones propios.
<!-- END AUTO-GENERATED -->

## Seguridad e identidad

Cómo la plataforma aplica el aislamiento, verifica la identidad y hace estructuralmente imposible el acceso no autorizado.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: security-and-identity -->
- [[diode-standard]] — La disciplina unidireccional de flujo de comandos; elimina el movimiento lateral al suprimir la lógica de enrutamiento que lo haría posible.
- [[capability-based-security]] — Cada componente de software posee un token criptográfico de capacidad para comunicarse con cualquier otro; sin autoridad ambiente.
- [[machine-based-auth]] — Autorización basada en hardware: el emparejamiento criptográfico reemplaza usuario y contraseña; el par es el permiso.
- [[crypto-attestation]] — Atestación de contenido en nodos de borde: el hash SHA-256 en el cliente permite a cualquier auditor verificar que una divulgación no ha sido alterada en tránsito.
- [[cryptographic-ledgers]] — Almacenamiento de estado inmutable por cadena de hash; cualquier alteración rompe una prueba criptográfica verificable en lugar de un control de política.
- [[personnel-permissions]] — Identidad de colaboradores en Totebox Orchestration: emparejamientos criptográficos de hardware, no control de acceso por roles almacenado en una base de datos.
- [[five-stage-supply-chain]] — El código pasa de colaborador a producción en cinco etapas, con una barrera de doble ciego que separa las credenciales de producción de los espacios de trabajo de los colaboradores.
- [[verification-surveyor]] — El componente humano en el bucle que presenta fragmentos de identidad extraídos a un operador antes del compromiso permanente en el libro verificado.
<!-- END AUTO-GENERATED -->

## Enrutamiento de IA y límite de inferencia

Cómo se clasifican, enrutan y contienen las solicitudes de IA para que nunca toquen el registro autoritativo.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: ai-routing-and-inference-boundary -->
- [[doorman-protocol]] — El Portero: el único límite de IA que sanea datos, enruta entre niveles de cómputo y centraliza todas las claves API; ninguna clave vive fuera de este límite.
- [[pointsav-llm]] — El modelo especialista de nivel proveedor planificado (Nivel 3 de la Escalera de Sustrato SLM de Cuatro Niveles); preentrenamiento continuado de OLMo 3 32B sobre el corpus de aprendizaje federado.
- [[slm-stack-architecture]] — El grafo completo de dependencias Rust y la arquitectura binaria de service-slm.
- [[sovereign-ai-routing]] — Las solicitudes de IA pasan por un paso de saneado local antes de llegar a cualquier modelo externo; los datos estructurados internos nunca viajan a servidores de terceros de forma identificable.
- [[zero-container-inference]] — Por qué la plataforma ejecuta la inferencia directamente en el binario del servicio en lugar de en un entorno de contenedor.
- [[decode-time-constraints]] — Restricciones estructurales aplicadas en cada paso de emisión de token; el vocabulario prohibido y las respuestas estructuralmente inválidas son matemáticamente imposibles de producir.
<!-- END AUTO-GENERATED -->

## Propiedad del cliente y despliegue

Los principios y mecanismos por los cuales los clientes son dueños plenos de su despliegue.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: customer-ownership-and-deployment -->
- [[customer-hostability]] — El compromiso arquitectónico de que cada artefacto se ejecuta sobre el hardware del cliente, contra sus propias claves, con su propio libro de auditoría.
- [[economic-model]] — La estructura comercial de dos niveles: un nivel Comunidad gratuito y un nivel Cliente PYME de pago dimensionado para empresas reguladas que los hiperescaladores no pueden atender económicamente.
- [[direct-payment-settlement]] — Los pagos de transacciones del mercado fluyen directamente del comprador al inquilino-cliente; la comisión de la plataforma se cobra en la liquidación.
- [[totebox-orchestration-development]] — El entorno de desarrollo es en sí mismo una instancia de Totebox Orchestration; el espacio de trabajo que construye la plataforma funciona sobre la misma arquitectura que entrega.
- [[totebox-session]] — Una Sesión Totebox: una sesión de colaboración asistida por IA, circunscrita a un solo archivo, incapaz de escribir fuera de él.
- [[vertical-seed-packs-marketplace]] — Taxonomías iniciales específicas del sector distribuidas como paquetes semilla; los inquilinos contribuyen con refinamientos a través de un mercado planificado.
- [[foundry-services-slice-model]] — La partición cgroup de systemd que protege los servicios de producción frente a la carga de sesiones de compilación concurrentes en un mismo servidor Totebox compartido.
- [[cargo-target-per-user-discipline]] — Particionado de la caché de compilación por desarrollador que elimina las carreras de bloqueo entre usuarios en un servidor Totebox compartido.
- [[mailbox-atomicity]] — Escritura exclusiva con flock e idempotencia por msg-id en los buzones de archivo plano que usan las sesiones Totebox para comunicarse entre sí.
- [[multi-engine-session-coordination]] — Protocolo de bloqueos de sesión con detección de obsolescencia por boot_id que evita que motores de IA concurrentes toquen el mismo `.git/index`.
<!-- END AUTO-GENERATED -->

## Inteligencia de ubicación y dominio

Decisiones arquitectónicas para el dominio de inteligencia de ubicación e inmuebles.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: location-intelligence-and-domain -->
- [[hardware-co-location-methodology]] — La metodología para clasificar candidatos de co-ubicación en instalaciones de centros de datos de terceros: idoneidad jurisdiccional, tránsito de red, compatibilidad de infraestructura y costo, con los requisitos regulatorios primero. (No debe confundirse con la [[retail-co-location-tier-methodology|metodología de niveles de co-ubicación minorista]], un tema distinto que comparte el mismo término.)
- [[flat-file-bim-leapfrog]] — Las cinco restricciones arquitectónicas — almacenamiento en archivos planos, estándares abiertos, Rust y Tauri, funcionamiento sin conexión y licencia Apache 2.0 — sobre las que se construye el registro digital de un edificio, y las cinco capacidades que se derivan de ellas en lugar de añadirse encima.
- [[building-design-system]] — Una capa de coordinación planificada para el entorno construido: una biblioteca canónica y legible por máquina de especificaciones de elementos de construcción que las superficies de autoría BIM independientes consumen por referencia, de la misma manera que un sistema de diseño de software mantiene consistentes a equipos de producto independientes.
- [[asset-anchored-bim-vault]] — El registro digital autoritativo de un edificio, estructurado como archivos de texto plano y binario estandarizado en un directorio versionado con git, que califica como un Entorno de Datos Común conforme a ISO 19650 y que viaja con la escritura de la propiedad.
<!-- END AUTO-GENERATED -->

Un artículo adicional planificado para el dominio de inteligencia de ubicación y BIM/inmuebles — que cubre la taxonomía regional de desarrollo — aún no está escrito.

## Véase también

- [Sustrato](/substrate/) — conceptos de mecanismo fundacionales: los sustratos compuesto, de aprendizaje, de citas y de divulgación
- [Patrones](/patterns/) — patrones de diseño nombrados realizados en la plataforma
- [Gobernanza](/governance/) — los registros de decisiones formales, la postura de licenciamiento y los requisitos de cumplimiento
- [Infraestructura](/infrastructure/) — topología de despliegue de flota, entorno en la nube e infraestructura física
