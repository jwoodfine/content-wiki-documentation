---
schema: foundry-doc-v1
title: "archetypes-and-chart-of-accounts"
slug: archetypes-and-chart-of-accounts
category: services
type: concept
quality: complete
short_description: "El Plan de Cuentas y los once arquetipos son la taxonomía institucional de dos partes en el núcleo de service-people y service-content, que clasifica al personal y los documentos por posición estructural y función, sin depender de texto de título de trabajo variable."
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: archetypes-and-chart-of-accounts.md
references:
  - id: 1
    text: "Fundación IFRS, NIC 1 — Presentación de Estados Financieros, §54–76: Estado de Situación Financiera — requisitos de clasificación de partidas y subcuentas."
    url: "https://www.ifrs.org/issued-standards/list-of-standards/ias-1-presentation-of-financial-statements/"
  - id: 2
    text: "Organización Internacional del Trabajo, Clasificación Internacional Uniforme de Ocupaciones 2008 (CIUO-08): Marco Conceptual y Metodología. OIT, Ginebra, 2012."
    url: "https://www.ilo.org/public/english/bureau/stat/isco/docs/publication08.pdf"
---

El Plan de Cuentas y los once arquetipos son la taxonomía institucional de dos partes en el núcleo de [[service-people]] y [[service-content]]. Juntos permiten que la plataforma clasifique al personal y los documentos por posición estructural y función, sin depender de texto de título de trabajo variable. A diferencia de un registro de personal en texto libre, la taxonomía se basa en conectores: cada persona ocupa una posición fija en el Plan y hereda propiedades de una de las once clases de arquetipos inmutables. Al finalizar este artículo, el lector comprenderá la taxonomía de arquetipos, la jerarquía del Plan de Cuentas y el mecanismo de autocorrección que produce su intersección.

## Dos libros mayores, una institución

La taxonomía está construida sobre dos libros mayores interrelacionados. Uno define la anatomía estructural de la organización. El otro define la función de las personas dentro de ella.

| Libro mayor | Qué captura | Cómo cambia |
|---|---|---|
| Plan de Cuentas | Dónde residen la autoridad, el riesgo y la producción en la organización — una jerarquía de tres niveles: Perfil → Dominio → Subdominio [^1] | Ajustado deliberadamente por operadores; estable entre ajustes |
| Once Arquetipos | Cómo opera una persona y qué produce, independientemente de su título [^2] | Fijo permanentemente; las once categorías son exhaustivas |

El Plan de Cuentas es simultáneamente el libro mayor general y el espacio de nombres de la institución. Para un lector financiero, cada fila es un centro de costo o ingreso. Para un lector de ingeniería, cada fila es una ruta de espacio de nombres estable que previene documentos huérfanos. [[service-content]] consume la jerarquía del Plan cuando clasifica documentos entrantes en la puerta F12; [[service-people]] consume la capa de arquetipos cuando evalúa la alineación del personal.

Ningún libro mayor sustituye al otro. El Plan captura *dónde* en la organización pertenece un documento o decisión; el arquetipo captura *cómo* opera la persona que lo produce. Su intersección es el modelo operativo de comportamiento institucional de la plataforma.

## Los once arquetipos y sus claves de evaluación

Cada uno de los once arquetipos se corresponde con una función organizativa principal y una clave de evaluación legible por máquina. La clave es consumida por el motor de alineación de la plataforma cuando compara el comportamiento observado de una persona con su posición estructural.

| Arquetipo | Función principal | Clave de evaluación |
|---|---|---|
| El Ejecutivo | Autoridad y estrategia | `exec_integrity` |
| El Guardián | Riesgo y cumplimiento | `risk_variance` |
| El Fiduciario | Gestión fiscal | `asset_trust` |
| El Arquitecto | Sistemas estructurales | `vision_alignment` |
| El Ingeniero | Lógica y datos | `logic_efficiency` |
| El Artesano | Oficio y estética | `output_fidelity` |
| El Constructor | Construcción física | `build_durability` |
| El Catalizador | Crecimiento e impulso | `velocity_factor` |
| El Enviado | Influencia y diplomacia | `relation_equity` |
| El Administrador | Logística y soporte | `system_stability` |
| El Sabio | Teoría y conocimiento | `knowledge_depth` |

Los arquetipos funcionan como clases de objetos en el sentido del software: cada entidad en [[service-people]] hereda propiedades de una de las once clases base, y esa herencia determina qué funciones de la plataforma puede aplicar el sistema al registro de esa persona. Dos personas con títulos diferentes que comparten un arquetipo reciben el mismo tratamiento computacional; dos personas con el mismo título pero arquetipos diferentes, no.

Las claves de evaluación no son puntuaciones. Son etiquetas de dimensión — la plataforma rastrea la varianza de cada clave a lo largo del tiempo en lugar de su valor absoluto, lo que hace que el sistema sea robusto ante diferentes niveles base entre individuos.

## Cómo el Plan de Cuentas se ancla a los roles de arquetipos

Cada fila del Plan de Cuentas lleva un ancla de arquetipo principal: el rol funcional esperado para esa posición estructural. Una ilustración de un Plan institucional canónico de bienes raíces:

| Perfil | Dominio | Subdominio | Arquetipo ancla |
|---|---|---|---|
| Cumplimiento | Asesoría | Representación legal | El Guardián |
| Cumplimiento | Contabilidad | — | El Fiduciario |
| Bienes raíces | Arrendamiento de oficinas | — | El Catalizador |
| Bienes raíces | Inquilinos de oficinas | — | El Administrador |
| Construcción | Colaboradores | Consultores de fachada | El Ingeniero |
| Construcción | Colaboradores | Arquitectos paisajistas | El Artesano |
| Construcción | Oficios | — | El Constructor |
| Soporte de TI | Colaboradores | BIM | El Ingeniero |
| Soporte de TI | Colaboradores | Ciencia de datos | El Sabio |
| Personal | Junta directiva | — | El Ejecutivo |

El Plan abarca siete Perfiles de nivel superior en un despliegue típico: Cumplimiento, Bienes raíces, Construcción, Soporte de TI, Relaciones con inversores, Personal y Administración local. Los Perfiles específicos son configurables por el operador; el ejemplo de siete Perfiles representa un despliegue de referencia, no una restricción fija.

El arquetipo ancla se usa para establecer expectativas, no para restringir el acceso. Un Asesor de Cumplimiento anclado al Guardián puede asumir responsabilidades de Fiduciario si el operador lo asigna; el Plan captura el ancla principal, y el motor de alineación rastrea la divergencia respecto a ella.

## Cómo la plataforma detecta y señala la deriva organizacional

La propiedad más distintiva del diseño de doble libro mayor es que [[service-people]] y [[service-content]] usan la relación entre las dos tablas para detectar y señalar la deriva organizacional. El motor evalúa si el comportamiento observado de una persona coincide con su posición estructural.

| Escenario | Diagnóstico | Respuesta del sistema |
|---|---|---|
| Posición en el Plan coincide con la salida del arquetipo | Alineación saludable | Sin acción |
| Posición en el Plan coincide, salida del arquetipo se desvía | Fricción funcional | El sistema limita el enrutamiento de tareas no alineadas y redirige a tareas compatibles |
| Posición en el Plan no coincide, señal de arquetipo elevada | Descubrimiento de talento | El sistema señala un posible desajuste de rol y propone un ajuste del Plan al administrador |
| Ninguna dimensión coincide | Ruido sistémico | El sistema suspende el cálculo de métricas para evitar contaminar datos agregados; se activa una auditoría manual |

El mecanismo no toma acciones de personal autónomas. La plataforma no mueve, asciende ni da de baja a personas. Señala desajustes estructurales y propone ajustes; un operador toma cada decisión. El registro de auditoría en [[service-minutebook]] captura la propuesta, la decisión del operador y la marca de tiempo — el mismo patrón que la [[app-console-input|puerta de entrada F12]].

## Por qué la taxonomía basada en conectores supera los títulos en texto libre

Los sistemas convencionales de recursos humanos y gestión de relaciones almacenan los títulos como texto libre. Cuatro cadenas diferentes pueden describir un rol con bandas de antigüedad; la base de datos las trata como cuatro entidades completamente distintas, y su agregación requiere normalización manual. [^2]

El diseño del Plan de Cuentas y los arquetipos resuelve esto estructuralmente:

| Propiedad | Efecto |
|---|---|
| Conectores, no cadenas | Cada persona se asigna a un conector fijo de Perfil → Dominio → Subdominio; el texto del título es metadato complementario |
| Traducción semántica | Actualizar la definición de un rol requiere cambiar una fila en el Plan central, no cada registro de personal que lo referencia |
| Clasificación consciente del comportamiento | La capa de arquetipos rastrea lo que la persona produce, no lo que su título afirma que produce |

El identificador determinista asignado a un individuo por [[service-extraction]] — un identificador derivado de hash de contenido, estable ante cambios de nombre y título — permanece constante; la asignación del conector y la lectura del arquetipo evolucionan a medida que el operador los actualiza.

## Véase también

- [[service-people]] — el servicio que mantiene los registros de personal contra esta taxonomía
- [[service-content]] — el servicio que clasifica los documentos entrantes contra la jerarquía del Plan de Cuentas
- [[service-extraction]] — el motor de extracción que deriva identificadores de entidad de los documentos entrantes
- [[app-console-input]] — la puerta de entrada F12 donde los operadores confirman las decisiones de enrutamiento contra el Plan
