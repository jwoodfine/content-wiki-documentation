---
schema: foundry-doc-v1
title: "Arquitectura"
slug: _index.es
short_description: "Arquitectura de plataforma transversal: el modelo de composición de tres anillos, límite de enrutamiento e inferencia de IA, sustrato de seguridad e identidad, principios de propiedad del cliente y el dominio de inteligencia de ubicación."
lang: es
category: architecture
type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: _index.md
---

PointSav se compone de tres anillos concéntricos con dependencias estrictamente unidireccionales, una canalización de datos determinista que funciona completamente sin IA, y una disciplina de soberanía que permite a los clientes bifurcar toda la pila el primer día. Los artículos de arquitectura describen las decisiones estructurales que sustentan esas propiedades: por qué están diseñadas así, cómo se componen y qué invariantes deben mantenerse en cada despliegue.

El modelo de tres anillos es el marco de carga: el Anillo 1 gestiona la ingesta por inquilino, el Anillo 2 proporciona conocimiento y procesamiento determinista, y el Anillo 3 añade inferencia de IA opcional que nunca escribe en el registro autoritativo.

## Estructura de la plataforma

Los artículos estructurales fundacionales — los patrones que componen cada despliegue PointSav.

- [[three-ring-architecture]] — Tres anillos concéntricos con dependencias estrictamente unidireccionales; la IA es estructuralmente opcional; el flujo determinista funciona plenamente sin el Anillo 3.
- [[3-layer-stack]] — La descomposición de infraestructura en tres capas: capacidad de cómputo pura, ejecución de plataforma aislada y acceso seguro del operador.
- [[three-layer-architecture]] — Cómo los entregables de PointSav transitan por las capas SOFTWARE, SHOWCASE e INSTANCIA con un flujo estrictamente unidireccional del proveedor al cliente.
- [[six-tier-sovereignty-matrix]] — La taxonomía de seis prefijos del monorepo (app-, asset-, os-, service-, system-, moonshot-) que hace estructural la higiene de dependencias.
- [[foundry-doctrine-overview]] — Resumen público del estatuto constitucional de la plataforma: seis pilares, cincuenta y dos afirmaciones estructurales y el modelo económico que los sustenta.
- [[leapfrog-2030-architecture]] — La visión arquitectónica Leapfrog 2030: la física de infraestructura de la era hiperescaladora de 2030 y cómo la plataforma está posicionada para beneficiarse de ella.
- [[pointsav-overview]] — PointSav Digital Systems: qué construye la empresa, cómo está organizada y la estructura corporativa de tres entidades.

## Seguridad e identidad

Cómo la plataforma aplica el aislamiento, verifica la identidad y hace estructuralmente imposible el acceso no autorizado.

- [[diode-standard]] — La disciplina unidireccional de flujo de comandos; elimina el movimiento lateral al suprimir la lógica de enrutamiento que lo haría posible.
- [[capability-based-security]] — Cada componente de software posee un token criptográfico de capacidad para comunicarse con cualquier otro; sin autoridad ambiente.
- [[machine-based-auth]] — Autorización basada en hardware: el emparejamiento criptográfico reemplaza usuario y contraseña; el par es el permiso.
- [[crypto-attestation]] — Atestación de contenido en nodos de borde: el hash SHA-256 en el cliente permite a cualquier auditor verificar que una divulgación no ha sido alterada en tránsito.
- [[cryptographic-ledgers]] — Almacenamiento de estado inmutable por cadena de hash; cualquier alteración rompe una prueba criptográfica verificable en lugar de un control de política.
- [[personnel-permissions]] — Identidad de colaboradores en Totebox Orchestration: emparejamientos criptográficos de hardware, no control de acceso por roles almacenado en una base de datos.
- [[five-stage-supply-chain]] — El código pasa de colaborador a producción en cinco etapas, con una barrera de doble ciego que separa las credenciales de producción de los espacios de trabajo de los colaboradores.
- [[verification-surveyor]] — El componente humano en el bucle que presenta fragmentos de identidad extraídos a un operador antes del compromiso permanente en el libro verificado.

## Enrutamiento de IA y límite de inferencia

Cómo se clasifican, enrutan y contienen las solicitudes de IA para que nunca toquen el registro autoritativo.

- [[doorman-protocol]] — El Portero: el único límite de IA que sanea datos, enruta entre niveles de cómputo y centraliza todas las claves API; ninguna clave vive fuera de este límite.
- [[pointsav-llm]] — El modelo especialista de nivel proveedor planificado (Nivel 3 de la Escalera de Sustrato SLM de Cuatro Niveles); preentrenamiento continuado de OLMo 3 32B sobre el corpus de aprendizaje federado.
- [[slm-stack-architecture]] — El grafo completo de dependencias Rust y la arquitectura binaria de service-slm.
- [[sovereign-ai-routing]] — Las solicitudes de IA pasan por un paso de saneado local antes de llegar a cualquier modelo externo; los datos estructurados internos nunca viajan a servidores de terceros de forma identificable.
- [[zero-container-inference]] — Por qué la plataforma ejecuta la inferencia directamente en el binario del servicio en lugar de en un entorno de contenedor.
- [[decode-time-constraints]] — Restricciones estructurales aplicadas en cada paso de emisión de token; el vocabulario prohibido y las respuestas estructuralmente inválidas son matemáticamente imposibles de producir.

## Propiedad del cliente y despliegue

Los principios y mecanismos por los cuales los clientes son dueños plenos de su despliegue.

- [[customer-hostability]] — El compromiso arquitectónico de que cada artefacto se ejecuta sobre el hardware del cliente, contra sus propias claves, con su propio libro de auditoría.
- [[economic-model]] — La estructura comercial de dos niveles: un nivel Comunidad gratuito y un nivel Cliente PYME de pago dimensionado para empresas reguladas que los hiperescaladores no pueden atender económicamente.
- [[direct-payment-settlement]] — Los pagos de transacciones del mercado fluyen directamente del comprador al inquilino-cliente; la comisión de la plataforma se cobra en la liquidación.
- [[totebox-orchestration-development]] — El entorno de desarrollo es en sí mismo una instancia de Totebox Orchestration; el espacio de trabajo que construye la plataforma funciona sobre la misma arquitectura que entrega.
- [[totebox-session]] — Una Sesión Totebox: una sesión de colaboración asistida por IA, circunscrita a un solo archivo, incapaz de escribir fuera de él.
- [[vertical-seed-packs-marketplace]] — Taxonomías iniciales específicas del sector distribuidas como paquetes semilla; los inquilinos contribuyen con refinamientos a través de un mercado planificado.

## Inteligencia de ubicación y dominio

Decisiones arquitectónicas para el dominio de inteligencia de ubicación e inmuebles.

- [[co-location-methodology]] — La metodología de análisis espacial para clasificación de co-localización: cómo se miden y puntúan las concentraciones minoristas e institucionales.
- [[location-intelligence-strategy]] — El marco estratégico y arquitectónico para el sustrato de inteligencia de ubicación: SIG abierto de archivos planos, primero sin conexión, sin costes por usuario.
- [[flat-file-bim-leapfrog]] — Cómo el Modelado de Información de Edificios se gestiona como registros ISO 19650 de archivos planos en lugar de instancias de bases de datos alojadas.
- [[building-design-system-bim]] — Herramientas del sistema de diseño adaptadas para flujos de trabajo BIM e inmuebles.
- [[development-regions]] — Taxonomía regional para análisis de desarrollo y planificación en despliegues PointSav.

## Véase también

- [Sustrato](/substrate/) — conceptos de mecanismo fundacionales: los sustratos compuesto, de aprendizaje, de citas y de divulgación
- [Patrones](/patterns/) — patrones de diseño nombrados realizados en la plataforma
- [Gobernanza](/governance/) — los registros de decisiones formales, la postura de licenciamiento y los requisitos de cumplimiento
- [Infraestructura](/infrastructure/) — topología de despliegue de flota, entorno en la nube e infraestructura física
