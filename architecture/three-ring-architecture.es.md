---
schema: foundry-doc-v1
title: "Arquitectura de tres anillos"
slug: three-ring-architecture.es
short_description: "El patrón de composición duradero para la plataforma PointSav: tres anillos concéntricos con dependencias estrictamente unidireccionales, donde el anillo de IA es estructuralmente opcional y la canalización de datos determinista funciona completamente sin él."
category: architecture
type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-22
editor: pointsav-engineering
paired_with: three-ring-architecture.md
---

Antes de que una organización regulada compre una plataforma de IA, tiene que responder una pregunta: ¿puede la IA tocar silenciosamente el registro autoritativo? En la mayoría de las plataformas la respuesta es procedimental — una política, un parámetro de configuración. Un parámetro puede cambiarse, y una política vale solo lo que vale su cumplimiento.

PointSav responde la pregunta de forma arquitectónica. <!--claim id=three-rings confidence=structural cites=[]-->La Arquitectura de Tres Anillos organiza cada servicio en uno de tres anillos concéntricos con dependencias estrictas en una sola dirección; los dos anillos interiores — ingesta en el límite y procesamiento determinista — funcionan plenamente sin el anillo de IA exterior.<!--/claim-->

<!--claim id=ai-optional-by-construction confidence=structural cites=[]-->Los anillos 1 y 2 no contienen ningún import, dependencia ni llamada en tiempo de ejecución que llegue al anillo 3. Un despliegue puede excluir el anillo 3 por completo; donde se incluye, es un consumidor de solo lectura que produce propuestas, nunca escrituras en el registro.<!--/claim-->

Para un comprador regulado la verificación es estructural, no procedimental. Un despliegue sin el anillo 3 no tiene IA que auditar; uno con él mantiene el núcleo determinista como el único registro autoritativo. Este artículo cubre la disposición de los anillos, la taxonomía de servicios, el modelo de aislamiento multi-tenant y por qué la IA es opcional por construcción.

## Los tres anillos

**Anillo 1 — Ingesta en el límite.** Cada servicio de este anillo acepta datos sin procesar de una fuente externa — sistema de archivos, bandeja de correo, carga de documentos, proveedor de identidad — y los escribe en un registro duradero. No hay transformación ni clasificación en el anillo 1; solo almacenamiento. <!--claim id=ring1-mcp confidence=structural cites=[]-->Cada servicio del anillo 1 implementa una interfaz de servidor Model Context Protocol, y el anillo 2 le habla como cliente MCP. Un cliente que necesita una fuente de datos nueva añade otro servidor MCP sin modificar ningún servicio existente.<!--/claim--> Los datos de cada cliente residen en una instancia de servicio separada con su propio almacenamiento.

**Anillo 2 — Conocimiento y procesamiento.** Lee del anillo 1 y produce conocimiento estructurado: registros analizados, grafos de conocimiento, entidades clasificadas, índices de búsqueda. <!--claim id=ring2-deterministic confidence=structural cites=[]-->Todo el procesamiento del anillo 2 es determinista, y una decisión de arquitectura vinculante prohíbe que la IA escriba en el grafo de conocimiento o en los almacenes de registros estructurados. La salida del anillo 2 es reproducible: el mismo input del anillo 1 se reproduce al mismo resultado.<!--/claim--> Una auditoría que cuestione una clasificación puede reproducir el análisis determinista contra el registro inmutable del anillo 1 y obtener la misma respuesta. Los servicios del anillo 2 son multi-tenant por `moduleId`.

**Anillo 3 — Inteligencia opcional.** <!--claim id=ring3-read-only confidence=structural cites=[]-->El anillo 3 es un único consumidor de solo lectura del anillo 2. Nunca escribe en el grafo de conocimiento, el registro contable ni los almacenes estructurados; sus únicas salidas son propuestas — texto que el operador revisa, borradores que el operador aprueba. Cada salida aceptada entra en el registro a través de una ruta de escritura del anillo 2 con un humano en el punto de control.<!--/claim--> `service-slm` es el único servicio del anillo 3. Implementa el patrón Doorman: cada solicitud entra por un único límite que sanea los datos salientes, enruta entre los tres niveles de cómputo (local, ráfaga de GPU, API externa) y registra cada llamada en el libro mayor de auditoría del cliente. Ninguna clave de API existe fuera del límite del Doorman.

## Modelo de aislamiento multi-tenant

El aislamiento varía por anillo, por diseño deliberado: aislamiento duro por instancia de servicio en el anillo 1; aislamiento lógico por `moduleId` en el anillo 2; una única instancia de `service-slm` con carga de adaptador por `moduleId` en el anillo 3. En ningún nivel hay un camino de código desde los datos de un inquilino hasta los de otro.

## Por qué la IA es opcional por diseño

El patrón de tres anillos hace la IA opcional por construcción, no por configuración. Un despliegue que excluye el anillo 3 opera con menos procesos, menos superficie de ataque y cumple los requisitos de aislamiento de red que prohíben las llamadas a API externas. Para un despliegue que incluye el anillo 3, la restricción de solo lectura mantiene el núcleo determinista como el registro autoritativo.

La especificación técnica completa — taxonomía de servicios, invariantes direccionales y modelo de aislamiento detallado — está disponible en el artículo principal en inglés.

## Véase también

- [[compounding-substrate]] — las cinco propiedades estructurales que implementa la Arquitectura de Tres Anillos
- [[service-slm]] — el servicio Doorman del anillo 3
- [[compounding-doorman]] — el patrón operativo que implementa el Doorman y por qué se compone con el tiempo
- [[worm-ledger-architecture]] — el registro inmutable de solo adición del anillo 1
