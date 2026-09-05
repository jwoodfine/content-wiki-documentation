---
schema: foundry-doc-v1
title: "Diseño de Interfaz de Usuario"
slug: user-interface-design
category: reference
type: topic
content_type: topic
quality: complete
status: active
audience: customer-woodfine
bcsc_class: current-fact
language_protocol: TRANSLATE-ES
last_edited: 2026-06-30
editor: woodfine-editorial
short_description: "Disciplina de diseño de interfaces entre humanos y máquinas orientada a maximizar usabilidad y experiencia de usuario, regida por los principios de la norma ISO 9241."
paired_with: user-interface-design.md
tags:
  - domain:documentation
  - source:jennifer-cluster
  - batch:iteration-2
source_refs:
  - d0b2cb64c72cd131b0df59af533bb8518674d08582dfc19a6b4df94231036804
thesis_alignment: "El diseño de interfaz de usuario es la disciplina que rige cómo los usuarios interactúan con las aplicaciones; comprender sus principios y normas es prerequisito para razonar sobre las superficies de las aplicaciones de consola, lugar de trabajo y de acceso público."
keynote: false
---

El diseño de interfaz de usuario, también llamado ingeniería de interfaz de usuario, es el diseño de interfaces para máquinas y aplicaciones de software con el objetivo principal de maximizar la usabilidad y la experiencia del usuario. En el contexto del software informático, el diseño de interfaz de usuario se centra en la arquitectura de la información — la organización y estructura de la información presentada al usuario — y la construcción de interfaces que comuniquen con claridad y permitan a los usuarios realizar tareas con la eficiencia apropiada y la mínima frustración.

El diseño de interfaz de usuario está involucrado en una amplia gama de proyectos, desde sistemas informáticos y cabinas de aeronaves hasta electrónica de consumo y paneles de control industrial. En todos los contextos, el objetivo es facilitar la realización de la tarea en cuestión sin atraer una atención innecesaria hacia la interfaz misma. Un diseño de IU eficaz combina el diseño gráfico, la tipografía y la arquitectura de la información al servicio de la usabilidad; equilibra la funcionalidad técnica con los elementos visuales e interactivos que hacen que el software sea accesible y comprensible para sus usuarios previstos.

## Relación con el diseño de experiencia de usuario

El diseño de interfaz de usuario se discute a menudo junto con el [[user-experience-design|diseño de experiencia de usuario]], pero las dos disciplinas son distintas. La distinción fue articulada por Don Norman y Jakob Nielsen: el diseño de IU se refiere a la superficie y el aspecto general de un diseño — los elementos visuales e interactivos que un usuario encuentra al usar un producto. El diseño de UX se refiere al proceso completo de creación de la experiencia del usuario — el rango completo de factores que afectan cómo un usuario percibe e interactúa con un producto, incluyendo pero no limitado a la interfaz visual. El diseño de IU es un componente del diseño de UX; el diseño de UX abarca el diseño de IU más la investigación de usuarios, la arquitectura de la información, la estrategia de contenido y el análisis posterior al despliegue.

## Tipos de interfaz de usuario

Tres tipos de interfaces principales están en uso generalizado en la informática contemporánea:

**Interfaces gráficas de usuario (GUI)** — aplicaciones de escritorio y web presentadas mediante metáforas visuales: ventanas, iconos, menús y punteros. El paradigma GUI, desarrollado en Xerox PARC y comercializado por Apple y Microsoft, es el modelo de interfaz dominante para la informática personal y el software empresarial.

**Interfaces de voz** — interfaces controladas mediante el habla, incluidos los asistentes personales inteligentes (Siri, Alexa, Google Assistant) y las aplicaciones controladas por voz. Las interfaces de voz enfrentan desafíos de diseño particulares: sin una pantalla visual, la interfaz debe comunicar el estado, las opciones y los errores solo mediante audio.

**Interfaces basadas en gestos** — interfaces controladas mediante movimiento físico, incluidas las interfaces de pantalla táctil, los paneles táctiles y las interfaces de gestos tridimensionales usadas en realidad virtual, realidad aumentada y entornos de juego interactivos.

## Proceso de diseño

Un proceso sistemático de diseño de IU sigue varias fases:

**Recopilación de requisitos de funcionalidad** — establecer lo que la interfaz debe permitir hacer al usuario, informado por la investigación de usuarios y el análisis de requisitos de negocio.

**Análisis de usuarios y tareas** — comprender quiénes son los usuarios, qué tareas necesitan realizar, en qué contextos trabajan y qué limitaciones (capacidad técnica, tiempo disponible, hardware) enfrentan.

**Arquitectura de la información** — organizar la estructura y jerarquía de la información para apoyar los objetivos del usuario. La arquitectura de la información determina el modelo de navegación, la agrupación de funciones relacionadas y el etiquetado de los elementos de la interfaz.

**Prototipado** — crear wireframes de baja fidelidad y prototipos interactivos que representen la estructura de la interfaz sin el detalle del diseño visual. Los prototipos se prueban con usuarios antes de realizar una inversión de desarrollo significativa.

### Inspección, pruebas y diseño visual

**Inspección de usabilidad** — revisión experta estructurada de la interfaz frente a criterios establecidos. Los métodos de inspección comunes incluyen el recorrido cognitivo (seguir el proceso de pensamiento del usuario paso a paso), la evaluación heurística (evaluar la interfaz frente a un conjunto de principios de usabilidad establecidos) y el recorrido pluralista (una revisión grupal estructurada que involucra a desarrolladores, usuarios y especialistas en usabilidad juntos).

**Pruebas de usabilidad** — observación de usuarios reales que intentan completar tareas definidas con la interfaz. El protocolo de pensar en voz alta, en el que los participantes narran sus pensamientos mientras usan la interfaz, es el método más utilizado.

**Diseño de GUI** — aplicar el diseño visual a la estructura de la interfaz, estableciendo la jerarquía visual, la paleta de colores, la tipografía y la iconografía que constituyen el aspecto y la sensación de la interfaz.

## Normas ISO 9241

La ISO 9241, la norma internacional para la ergonomía de la interacción persona-sistema, proporciona el principal marco internacional para los requisitos de diseño de IU.

**Siete principios de diálogo (ISO 9241, Parte 10/110)** abordan las cualidades dinámicas de una interfaz:

1. **Adecuación a la tarea** — la interfaz apoya al usuario en la realización de la tarea sin imponer una carga innecesaria.
2. **Autodescriptividad** — la interfaz proporciona retroalimentación y señales explicativas suficientes para que los usuarios comprendan su estado actual y las opciones disponibles sin documentación externa.
3. **Controlabilidad** — los usuarios pueden controlar el ritmo y la secuencia de la interacción.
4. **Conformidad con las expectativas del usuario** — la interfaz se comporta de manera consistente con lo que los usuarios esperan según su conocimiento previo y las señales que proporciona la interfaz.
5. **Tolerancia a errores** — a pesar de entradas o acciones erróneas, la interfaz permite al usuario recuperarse con el mínimo esfuerzo correctivo.
6. **Adecuación a la individualización** — la interfaz puede adaptarse a las habilidades, capacidades y preferencias de usuarios individuales.
7. **Adecuación para el aprendizaje** — la interfaz apoya a los usuarios en aprender a usarla.

### Partes de usabilidad, presentación y orientación

**Usabilidad (ISO 9241, Parte 11)** define la usabilidad como un producto de tres componentes: efectividad (los usuarios pueden lograr sus objetivos), eficiencia (los usuarios pueden lograr sus objetivos con el gasto apropiado de recursos) y satisfacción (los usuarios encuentran la interacción aceptable).

**Siete atributos de presentación (ISO 9241, Parte 12)** abordan las cualidades visuales estáticas de una interfaz:

1. **Claridad** — la información es distinguible y legible.
2. **Discriminabilidad** — la información mostrada puede diferenciarse de otra información.
3. **Concisión** — los usuarios no se ven sobrecargados con información extraña.
4. **Consistencia** — se aplica el mismo lenguaje de diseño en toda la interfaz.
5. **Detectabilidad** — la atención del usuario se dirige hacia la información requerida.
6. **Legibilidad** — los caracteres son fáciles de leer.
7. **Comprensibilidad** — el significado de la información mostrada es claro e inequívoco.

**Orientación al usuario (ISO 9241, Parte 13)** aborda cinco medios mediante los cuales una interfaz orienta a los usuarios: indicaciones, retroalimentación, información de estado, gestión de errores y ayuda en línea.

---

*citas: [[user-experience-design]], [[application-programming-interface]]*
