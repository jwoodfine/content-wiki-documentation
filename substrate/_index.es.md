---
schema: foundry-doc-v1
title: "Sustrato"
slug: substrate-index.es
category: substrate
type: topic
quality: complete
short_description: "La categoría de sustrato recoge los conceptos fundacionales de mecanismo de la plataforma — el Sustrato Compuesto, el Sustrato de Aprendizaje, el Sustrato de Citación, el Sustrato de Divulgación, el Sustrato de Trayectoria, el Sustrato de Protocolo Lingüístico, y las disciplinas y primitivas que los componen — cada uno describiendo una propiedad estructural en la que la plataforma se apoya en lugar de un servicio o sistema específico."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-19
editor: pointsav-engineering
paired_with: _index.md
---

La categoría **sustrato** recoge los conceptos fundacionales de mecanismo de la plataforma. Cada sustrato nombra una propiedad estructural en la que la plataforma se apoya — no un servicio o sistema específico, sino un patrón que compone servicios, sistemas y contenido en un todo coherente.

La categoría responde a preguntas como: *¿qué hace que la plataforma mejore continuamente sin renunciar a la propiedad de los datos? ¿qué hace que las citaciones sean auditables por máquina? ¿qué hace que las divulgaciones cumplan estructuralmente? ¿qué hace que el trabajo del colaborador retroalimente el entrenamiento del modelo?* Los artículos aquí describen los mecanismos; las categorías de arquitectura, servicios y sistemas describen cómo se realizan en componentes concretos.

## Por dónde empezar

Lea primero [[compounding-substrate]] — es el patrón canónico que PointSav administra y el marco que hace legibles los demás sustratos. Después lea [[apprenticeship-substrate]], [[citation-substrate]] y [[disclosure-substrate]].

## Sustratos nombrados principales

Los nueve sustratos nombrados: cada uno designa una propiedad estructural de la que depende la plataforma.

- [[compounding-substrate]] — Cinco propiedades estructurales que convierten cada interacción operativa en un evento de entrenamiento que se compone en todos los despliegues de clientes.
- [[apprenticeship-substrate]] — Enruta el trabajo a través de un SLM local, captura veredictos firmados y utiliza los pares de preferencias resultantes como señal de preentrenamiento continuo.
- [[citation-substrate]] — Registro de citas YAML a nivel de plataforma con detección de desviaciones; hace que la procedencia sea auditable por máquina desde el instrumento regulatorio hasta la afirmación publicada.
- [[disclosure-substrate]] — Markdown versionado con cadenas de autoría firmadas y hashes criptográficos de contenido produce registros de divulgación continua estructuralmente conformes con BCSC.
- [[trajectory-substrate]] — Convierte el trabajo operativo — commits, sesiones, retroalimentación del operador — en tuplas de entrenamiento JSONL estructuradas para el preentrenamiento continuo.
- [[language-protocol-substrate]] — Cuatro familias de adaptadores y dieciocho plantillas de género que codifican el registro, la voz de marca y el público objetivo como andamiaje de indicaciones reutilizables.
- [[design-system-substrate]] — Motor de sistema de diseño auto-alojado que almacena tokens y componentes en el repositorio git propio del cliente; formato de token W3C DTCG; endpoint MCP legible por máquina.
- [[location-intelligence-substrate]] — Arquitectura GIS abierta de archivos planos: datos abiertos con licencia Apache, stack de renderizado alineado con Rust, análisis de co-ubicación minorista como primera superficie desplegada.
- [[brief-queue-substrate]] — Cola duradera respaldada por archivos que hace viable la computación Yo-Yo de apagado inactivo sin perder datos de captura del corpus de aprendizaje.

## El Doorman compuesto y la frontera de IA

- [[compounding-doorman]] — El servicio único que media cada llamada de cómputo externo: disciplina de saneamiento y rehidratación, registro de auditoría, señal de entrenamiento acumulada.
- [[mcp-substrate-protocol]] — Cada servicio de Ring 1 y Ring 2 expone una interfaz de servidor del Protocolo de Contexto de Modelo como su contrato externo principal.
- [[adapter-composition]] — La metáfora del sistema operativo para la IA en PointSav: Doorman como kernel, adaptadores como procesos, service-content como sistema de archivos.
- [[knowledge-graph-grounded-apprenticeship]] — El Doorman consulta el grafo de conocimiento del cliente antes de cada solicitud de inferencia; el grafo y el adaptador coevolucionan.
- [[single-boundary-compute-discipline]] — Cada solicitud de inferencia de IA se enruta exclusivamente a través del Doorman; la omisión está estructuralmente impedida a nivel de kernel.

## Pila de Modelo de Lenguaje Pequeño

- [[llm-substrate-decision]] — La justificación para OLMo 3: la única familia de modelos completamente abierta que satisface una postura de adquisición de empresa pública canadiense.
- [[four-tier-slm-substrate]] — Una ruta de soberanía gradual desde una puerta de enlace API ligera sin modelo local hasta un servicio especialista de dominio.
- [[yoyo-compute-substrate]] — El sustrato de cómputo de tres anillos que permite a service-slm activar y desactivar la capacidad de inferencia GPU mientras retiene el estado.
- [[yo-yo-lora-training-pipeline]] — La tubería nocturna de dos fases: extracción de entidades para el DataGraph empresarial (Fase 1) y entrenamiento del adaptador LoRA usando QLoRA en una GPU L4 (Fase 2).
- [[tui-corpus-producer]] — Cada interacción terminal con service-slm a través del TUI del operador es una contribución curada al corpus de entrenamiento del adaptador del cliente.
- [[nightly-datagraph-rebuild]] — El proceso programado que reconstruye el grafo de conocimiento de la plataforma desde fuentes canónicas de archivos planos cada noche.

## Primitivas criptográficas y de micronúcleo

- [[sel4-microkernel-substrate]] — El micronúcleo seL4 formalmente verificado como kernel L1 para todos los sistemas operativos de PointSav: aislamiento de memoria garantizado estructuralmente.
- [[merkle-proofs-as-substrate-primitive]] — Primitivas de prueba Merkle RFC 9162 como piso criptográfico del registro de capacidades de la plataforma.
- [[system-substrate-doctrine]] — La arquitectura a nivel de kernel: un registro de capacidades con raíz en el cliente que es el registro de auditoría.

## Soberanía y propiedad del cliente

- [[sovereign-ai-commons]] — El posicionamiento de mercado de PointSav como administrador de infraestructura de IA abierta y compartida para PYMEs reguladas.
- [[knowledge-commons]] — El modelo económico que separa lo que PointSav publica libremente de lo que vende.
- [[customer-owned-graph-ip]] — El grafo de conocimiento del cliente y los pesos del adaptador entrenado son propiedad intelectual del cliente, portátil y exportable.
- [[tier-zero-customer-side-sovereign-specialist]] — Un despliegue Totebox especialista soberano en el propio hardware del cliente sin dependencia de la nube y con un tamaño total de 1 GB.
- [[substrate-without-inference-base-case]] — El Archivo Totebox permanece completamente operativo y libremente transferible incluso sin un nivel de inferencia de IA disponible.
- [[substrate-native-compatibility]] — Compatibilidad estructural con las convenciones de los lectores de MediaWiki sin mimetismo de API.

## Mecánicas de plataforma

- [[code-for-machines-first]] — Cada contrato entre servicios, registro de auditoría, configuración y ontología es legible por máquina como superficie primaria.
- [[seed-taxonomy-as-smb-bootstrap]] — Cada despliegue de cliente aprovisiona una taxonomía semilla de cuatro partes como bootstrap del grafo de conocimiento.
- [[reverse-flow-substrate]] — La puerta de enlace Doorman y el registro de auditoría que aplican la disciplina de datos entrantes también aplicarán los flujos comerciales salientes — planificado, opt-in por cliente.

## Véase también

- [Architecture](/architecture/) — arquitectura transversal de la plataforma
- [Patterns](/patterns/) — patrones de diseño nombrados realizados sobre sustratos
