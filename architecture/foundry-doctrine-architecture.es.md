---
schema: foundry-doc-v1
title: "PointSav Platform — Visión arquitectónica"
slug: foundry-doctrine-architecture
short_description: "Carta constitucional que codifica seis compromisos fundacionales y cincuenta y cuatro afirmaciones estructurales que rigen cada decisión de ingeniería de PointSav."
category: architecture
index_group: platform-structure
type: topic
content_type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-07-31
editor: pointsav-engineering
paired_with: foundry-doctrine-architecture.md
---


La carta constitucional de la plataforma [[pointsav-overview|PointSav]] codifica los principios, compromisos y afirmaciones estructurales que rigen cada decisión de ingeniería, operaciones y editorial. La versión actual es v0.1.0 ALPHA, ratificada el 30 de abril de 2026. Véase [[foundry-doctrine-overview|la visión general de la doctrina]] para el encuadre introductorio.

## Los Seis Pilares

La plataforma se construye sobre seis compromisos fundamentales que tienen prioridad sobre cualquier decisión de diseño específica:

**Texto plano, archivo plano, código abierto.** Cada artefacto producido por el sustrato — grafos de conocimiento, libros de auditoría, documentación, configuración, datos de entrenamiento — es texto plano. Sin almacenes de solo binarios, sin formatos propietarios.

**La soberanía es estructural, no procesal.** Los datos y el cómputo del cliente permanecen dentro del límite del cliente por construcción. Las reglas de firewall, el confinamiento de tokens de portador y los libros de solo anexar WORM refuerzan la soberanía a nivel de infraestructura.

**El Anillo 3 es opcional.** El anillo de inferencia de IA es estructuralmente opcional. El sustrato determinista — grafo de conocimiento, búsqueda, ingestión, egreso — funciona completamente cuando la IA está desactivada o no disponible. La Inteligencia Opcional es una restricción de diseño, no una posición de marketing.

**Proveedor → Cliente → Despliegues es el único flujo.** El código fuente de ingeniería vive en los repositorios canónicos de `pointsav/*`. Los manuales de operación del cliente viven en `woodfine/*`. Las instancias de tiempo de ejecución están numeradas y son solo locales.

**Cada sesión entrena el modelo.** Cada sesión de colaborador que produce salida genera una tupla de entrenamiento que se acumula en el corpus de aprendizaje. El sustrato se perfecciona de forma monótona con el uso.

**El punto de control humano en F12 es obligatorio.** SYS-ADR-10 — el punto de control humano final antes de que cualquier estado se confirme en un libro de contabilidad verificado — nunca se omite.

## Las Cincuenta y Cuatro Afirmaciones de Salto

La doctrina enumera 54 afirmaciones estructurales numeradas que juntas constituyen el posicionamiento de la plataforma frente al software como servicio de hiperescaladores. Cada afirmación identifica una propiedad estructural del sustrato de la plataforma que la economía o arquitectura de los hiperescaladores no puede replicar sin cambiar el modelo de negocio subyacente.

Grupos representativos del conjunto completo de afirmaciones:

**Soberanía y propiedad de datos (afirmaciones #1–#11, #48, #54).** El grafo de conocimiento del cliente es [[customer-owned-graph-ip|propiedad intelectual del cliente]]. El [[worm-ledger-architecture|libro de contabilidad WORM]] por inquilino está enraizado en el cliente. Los formatos de exportación son abiertos desde el primer día.

**Sustrato de Compuesto (afirmación #18).** [[compounding-substrate|Cada unidad de trabajo]] — un commit, una sesión, un paso editorial, una ejecución de entrenamiento — aumenta la capacidad de la siguiente unidad. La curva de capacidad aumenta de forma monótona con el volumen de trabajo.

**Álgebra de composición de adaptadores (afirmación #22).** En el momento de inferencia, el [[doorman-protocol|Portero]] compone hasta tres [[adapter-composition|adaptadores]]: `base ⊕ inquilino ⊕ protocolo`. La inferencia resultante está sintonizada simultáneamente para la capacidad general del modelo base, el vocabulario de dominio del inquilino y los requisitos de género de la solicitud actual.

**Sustrato de Aprendizaje (afirmación #32).** El trabajo con forma de código y prosa se enruta a través del [[doorman-protocol|Portero]] como un resumen estructurado. El aprendiz (SLM local) produce un diff candidato con razonamiento citado. Una identidad sénior emite un veredicto firmado. La tupla aterriza en el [[apprenticeship-substrate|corpus de aprendizaje]].

**Sustrato de Libro de Capacidades (afirmación #33).** Cada invocación de capacidad mediada por el núcleo emite una entrada firmada a un [[merkle-proofs-as-substrate-primitive|registro de Merkle]] enraizado en el cliente. La transferencia de propiedad es una ceremonia de co-firma de ápice — sin migración de estado, sin interrupción del servicio. Véase [[capability-ledger-substrate|sustrato del libro de capacidades]].

**Sustrato Soberano de Dos Fondos (afirmación #34).** El diseño **prevé** que los binarios `os-*` se ejecuten en dos fondos de núcleo — [[sel4-microkernel-substrate|seL4]] (nativo, verificado formalmente) y NetBSD (compatibilidad, arranca en cualquier lugar) — mediante un shim de compatibilidad. El fondo de compatibilidad NetBSD y la capa de malla WireGuard operan hoy; el fondo nativo seL4 y el shim de binario compartido están planificados (Fase 3). Actualmente ningún servicio distribuye un único binario que se ejecute sin modificaciones en ambos fondos.

**Escalera de cuatro niveles de SLM (afirmación #40).** Los clientes avanzan por
[[four-tier-slm-substrate|cuatro posiciones de producto]] — Comunidad (puerta de enlace
API pura), Nivel 1 (especialista local de 7B), Nivel 2 ([[yoyo-compute-substrate|Yo-Yo]]
de 32B alojado por el proveedor), Nivel 3 (especialista PointSav-LLM con
preentrenamiento continuado especializado) — a medida que su corpus se acumula y su
apetito de cómputo crece. La escalera está diseñada para la ruptura: cada nivel es
portátil para el cliente; ningún nivel genera dependencia del proveedor.

**Sustrato de flujo inverso (afirmación #52).** La misma puerta de enlace
[[doorman-protocol|Doorman]] y el mismo libro de auditoría que imponen la disciplina de
entrada también imponen los flujos comerciales de salida —
[[reverse-flow-substrate|mercado de datos e intercambio publicitario]] — como
configuraciones opcionales, seleccionables por el inquilino. La configuración de
monetización es una decisión contractual, no una reconstrucción arquitectónica.

## Las Ocho Invenciones Transectoriales

Más allá de las afirmaciones estructurales, la doctrina se inspira en ocho invenciones de proceso tomadas de industrias establecidas: Pasaporte del Espacio de Trabajo (marítimo), NOTAM (aviación), Procedimiento de Retirada (farmacéutico), Conocimiento de Embarque (transporte marítimo), Operación con Período de Consolidación (banca), Modo Aprendiz (aviación/medicina), Ancla de Integridad (notarización), Convención Constitucional (IETF/enmienda constitucional).

## Estructura del espacio de trabajo

El espacio de trabajo es en sí mismo un despliegue del sustrato —
`vault-privategit-source-1`. Tres niveles fluyen en una sola dirección:

- `vendor/` — código fuente de ingeniería (`pointsav/*`) — rastreado en GitHub
- `customer/` — catálogo de manuales (`woodfine/*`) — rastreado en GitHub
- `deployments/` — instancias numeradas de tiempo de ejecución — solo locales,
  excluidas de git

Tres roles de sesión operan el espacio de trabajo: la sesión de mando (plano de
control del espacio de trabajo, una sola a la vez), la sesión de archivo (un plano por
repositorio de ingeniería, uno por repositorio) y la sesión de proyecto (por clúster de
proyecto, varias concurrentes). La restricción `.git/index` — una sola sesión por
índice — es la condición de carrera que determina esta estructura.

## Postura de Divulgación Continua

Cada artefacto escrito en el espacio de trabajo se trata como potencialmente revisable bajo las obligaciones de divulgación continua. Las declaraciones prospectivas sobre capacidad futura, cronograma o resultados del cliente llevan el encuadre "planificado"/"previsto"/"puede", una base razonable declarada y lenguaje cautelar.

## Véase también

- [[compounding-substrate]]
- [[three-ring-architecture]]
- [[single-boundary-compute-discipline]]
- [[system-substrate-doctrine]]
- [[slm-stack-architecture]]
- [[yoyo-compute-substrate]]
