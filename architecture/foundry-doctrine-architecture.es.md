---
title: "Doctrina Foundry — Visión Arquitectónica"
slug: foundry-doctrine-architecture.es
category: architecture
status: stable
last_edited: 2026-04-30
editor: pointsav-engineering
quality: complete
---

La Doctrina Foundry es la carta constitucional de la plataforma PointSav. Codifica los principios, compromisos y afirmaciones estructurales que rigen cada decisión de ingeniería, operaciones y editorial en todo el espacio de trabajo. La versión actual es v0.1.0 ALPHA, ratificada el 30 de abril de 2026.

## Los Seis Pilares

Foundry se construye sobre seis compromisos fundamentales que tienen prioridad sobre cualquier decisión de diseño específica:

**Texto plano, archivo plano, código abierto.** Cada artefacto producido por el sustrato — grafos de conocimiento, libros de auditoría, documentación, configuración, datos de entrenamiento — es texto plano. Sin almacenes de solo binarios, sin formatos propietarios.

**La soberanía es estructural, no procesal.** Los datos y el cómputo del cliente permanecen dentro del límite del cliente por construcción. Las reglas de firewall, el confinamiento de tokens de portador y los libros de solo anexar WORM refuerzan la soberanía a nivel de infraestructura.

**El Anillo 3 es opcional.** El anillo de inferencia de IA es estructuralmente opcional. El sustrato determinista — grafo de conocimiento, búsqueda, ingestión, egreso — funciona completamente cuando la IA está desactivada o no disponible. La Inteligencia Opcional es una restricción de diseño, no una posición de marketing.

**Proveedor → Cliente → Despliegues es el único flujo.** El código fuente de ingeniería vive en los repositorios canónicos de `pointsav/*`. Los manuales de operación del cliente viven en `woodfine/*`. Las instancias de tiempo de ejecución están numeradas y son solo locales.

**Cada sesión entrena el modelo.** Cada sesión de Tarea, Root y Master que produce salida genera una tupla de entrenamiento que se acumula en el corpus de aprendizaje. El sustrato se perfecciona de forma monótona con el uso.

**El punto de control humano en F12 es obligatorio.** SYS-ADR-10 — el punto de control humano final antes de que cualquier estado se confirme en un libro de contabilidad verificado — nunca se omite.

## Las Cincuenta y Dos Afirmaciones de Salto

La doctrina enumera 54 afirmaciones estructurales numeradas que juntas constituyen el posicionamiento de Foundry frente al software como servicio de hiperescaladores. Cada afirmación identifica una propiedad estructural del sustrato Foundry que la economía o arquitectura de los hiperescaladores no puede replicar sin cambiar el modelo de negocio subyacente.

Grupos representativos del conjunto completo de afirmaciones:

**Soberanía y propiedad de datos (afirmaciones #1–#11, #48, #54).** El grafo de conocimiento del cliente es propiedad intelectual del cliente. El libro de contabilidad WORM por inquilino está enraizado en el cliente. Los formatos de exportación son abiertos desde el primer día.

**Sustrato de Compuesto (afirmación #18).** Cada unidad de trabajo — un commit, una sesión, un paso editorial, una ejecución de entrenamiento — aumenta la capacidad de la siguiente unidad. La curva de capacidad aumenta de forma monótona con el volumen de trabajo.

**Álgebra de composición de adaptadores (afirmación #22).** En el momento de inferencia, el Portero compone hasta tres adaptadores: `base ⊕ inquilino ⊕ protocolo`. La inferencia resultante está sintonizada simultáneamente para la capacidad general del modelo base, el vocabulario de dominio del inquilino y los requisitos de género de la solicitud actual.

**Sustrato de Aprendizaje (afirmación #32).** El trabajo con forma de código y prosa se enruta a través del Portero como un resumen estructurado. El aprendiz (SLM local) produce un diff candidato con razonamiento citado. Una identidad sénior emite un veredicto firmado. La tupla aterriza en el corpus de aprendizaje.

**Sustrato de Libro de Capacidades (afirmación #33).** Cada invocación de capacidad mediada por el núcleo emite una entrada firmada a un registro de Merkle enraizado en el cliente. La transferencia de propiedad es una ceremonia de co-firma de ápice — sin migración de estado, sin interrupción del servicio.

**Sustrato Soberano de Dos Fondos (afirmación #34).** La plataforma funciona en dos fondos de núcleo: seL4 (nativo, verificado formalmente) y NetBSD (compatibilidad, arranca en cualquier lugar). Los mismos binarios `os-*` se ejecutan en cualquiera de los dos fondos.

## Las Ocho Invenciones Transectoriales

Más allá de las afirmaciones estructurales, la doctrina se inspira en ocho invenciones de proceso tomadas de industrias establecidas: Pasaporte del Espacio de Trabajo (marítimo), NOTAM (aviación), Procedimiento de Retirada (farmacéutico), Conocimiento de Embarque (transporte marítimo), Operación con Período de Consolidación (banca), Modo Aprendiz (aviación/medicina), Ancla de Integridad (notarización), Convención Constitucional (IETF/enmienda constitucional).

## Postura de Divulgación Continua

Cada artefacto escrito en el espacio de trabajo se trata como potencialmente revisable bajo las obligaciones de divulgación continua. Las declaraciones prospectivas sobre capacidad futura, cronograma o resultados del cliente llevan el encuadre "planificado"/"previsto"/"puede", una base razonable declarada y lenguaje cautelar.

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ y Foundry™ son marcas no registradas de Woodfine Capital Projects Inc.
