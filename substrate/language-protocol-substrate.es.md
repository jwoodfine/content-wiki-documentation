---
schema: foundry-doc-v1
title: "Sustrato de protocolo de lenguaje"
slug: language-protocol-substrate
lang: es
paired_with: language-protocol-substrate.md
category: substrate
type: topic
content_type: topic
quality: complete
index_group: core-named-substrates
short_description: "El mecanismo de enrutamiento que transporta el registro, tipo de documento y destino declarados de un borrador entre archivos — un campo de portada, una tabla de enrutamiento y una convención de buzón, no un sistema de adaptadores de IA."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-24
editor: pointsav-engineering
cites:
 - ni-51-102
 - np-51-201
---

Cada borrador que se mueve por la plataforma PointSav — un artículo de wiki, un README, una corrección legal, una traducción — declara de antemano su registro, tipo de documento y destino, en lugar de que estos se infieran después. Esa declaración es el sustrato de protocolo de lenguaje: un campo de portada, una tabla de enrutamiento y una convención de buzón, no un sistema de IA.

El sustrato tiene dos capas reales y separadas. La **capa de enrutamiento** es genuinamente operativa: cada borrador lleva un valor `language_protocol`, una tabla a nivel de espacio de trabajo mapea ese valor al archivo que lo posee, y un mensaje de buzón recoge el traspaso automáticamente. La **capa de registro y esquema** vive como datos, no como código — qué debe contener un documento PROSE o LEGAL, y qué palabras no puede usar. Archivos YAML en `pointsav-design-system` (un registro por wiki, una lista de vocabulario prohibido por wiki, un esquema por tipo de contenido) definen esas reglas; un script de linting las verifica antes de publicar. No existe una "taxonomía de adaptadores en cuatro familias" unificada, ningún adaptador LoRA compuesto por petición, ni un único crate de Rust que posea esquema, plantillas y validación juntos.

## Los cuatro valores de protocolo — reales, y cómo enrutan realmente

`PROSE-*`, `COMMS-*`, `LEGAL-*` y `TRANSLATE-*` son valores reales de `language_protocol`. Dos archivos gateway poseen el enrutamiento: `project-editorial` recibe PROSE/COMMS/LEGAL/TRANSLATE, `project-design` recibe DESIGN-*. Un borrador se marca con la portada `foundry-draft-v1` (protocolo, destino, campo de enrutamiento), y una convención de prefijo de mensaje de buzón lleva la intención de enrutamiento al archivo propietario automáticamente.

Lo que no es real: un sistema de IA que compone un modelo base con un adaptador de "voz de marca" y un adaptador por protocolo al momento de la inferencia. Tampoco existe un crate de Rust compartido que produzca "dieciocho plantillas de género" y "ocho términos prohibidos transversales." El contenido de registro y esquema que realmente gobierna cada protocolo son actualmente 3 esquemas de tipo de contenido (TOPIC, GUIDE, JOURNAL) y una lista de vocabulario prohibido por wiki — no una taxonomía única de dieciocho plantillas.

## Dónde vive realmente el contenido de registro y esquema

`pointsav-design-system/tokens/linguistic/` contiene un archivo de registro por wiki y una lista de vocabulario prohibido por wiki, cada término con su reemplazo aprobado en lenguaje llano. `pointsav-design-system/tokens/content-schema/` contiene el esquema de portada y estructura de cada tipo de contenido. `project-editorial` es el custodio de contenido de este subárbol de tokens; aplicar cambios pasa por la puerta de confirmación mecánica de `project-design`.

`editorial-lint.py` (de `project-editorial`) lee estos archivos de tokens directamente y verifica la estructura y el vocabulario de un borrador contra ellos antes de que pueda confirmarse. Es un script de linting que corre al momento de confirmar, no un adaptador de inferencia ni un servicio que otro componente invoca por petición.

## `service-proofreader` — un servicio real, desplegado por separado

`service-proofreader` es un servicio real de asistencia de escritura interactiva en ejecución (`local-proofreader.service`, puerto 9092) — pero no es un crate dentro de `pointsav-monorepo`, ni una pata de una división en cuatro servicios junto a `service-content`/`service-slm`. Es su propio despliegue, alcanzable desde la [[radical-proofreader-ui|consola de revisión]], y despacha su paso generativo a través del Doorman como cualquier otro llamador de inferencia. Si toda acción editorial en cualquier lugar de la plataforma produce, a través de él, una tupla de entrenamiento firmada con veredicto, como se afirmó previamente, no está confirmado — esa afirmación describía una integración más amplia que la verificada aquí.

## Multi-inquilino mediante espacio de nombres por moduleId

Una instancia de `service-content` por despliegue de plataforma, con `moduleId` particionando a los inquilinos dentro de ella. El despliegue aislado por inquilino es la ruta de escalamiento — cuando un cliente necesita gestión de claves por inquilino o un aislamiento más fuerte, levanta su propia instancia de plataforma en su propia infraestructura y obtiene ahí su propio `service-content`.

Este es el sentido de "el escalamiento de inquilino ocurre en la frontera del despliegue, no en la frontera de nomenclatura del servicio." El servicio permanece multi-inquilino; la topología del despliegue crece en aislamiento cuando se justifica.

## Fundamentación arquitectónica

El sustrato se apoya en tres mecanismos interconectados.

El esquema `foundry-draft-v1` es el sobre de portada que lleva cada artefacto de borrador. Requiere un campo de protocolo de lenguaje, un campo de destino y un campo de enrutamiento — las instrucciones legibles por máquina que el esquema aplica en el momento de la puesta en escena. Una tabla de enrutamiento a nivel de espacio de trabajo mapea cada valor de protocolo a un proyecto gateway y un destino; la tabla es la única fuente de verdad para ese mapeo, de modo que ningún archivo codifica de forma rígida la lógica de enrutamiento de los artefactos de otro archivo. Una convención de prefijo de mensaje de buzón lleva entonces la intención de enrutamiento entre archivos: un borrador puesto en escena genera un mensaje saliente que un relé recoge automáticamente, sin que se requiera ningún paso manual de traspaso.

El sustrato difiere de un sistema de gestión de contenido en dos sentidos. No almacena contenido — el contenido vive en git, en los directorios rastreados del archivo receptor. No posee la lógica de enrutamiento — cada proyecto gateway implementa su propio pipeline contra la forma del borrador entrante. El sustrato hace que el contenido sea enrutable por máquina entre archivos sin requerir que los archivos conozcan los detalles internos de los demás. También difiere de un protocolo de servidor de lenguaje: un protocolo de servidor de lenguaje define una sesión bidireccional en tiempo real, mientras que el sustrato no tiene estado de sesión — la declaración de protocolo en un borrador es un sello por artefacto, hecho una sola vez en el momento de la puesta en escena, que viaja con el artefacto a través de cada traspaso.

## Por qué la selección explícita de protocolo

La elección de diseño fundamental del sustrato es exigir que quien hace la solicitud declare un protocolo de lenguaje en cada solicitud editorial, en lugar de auto-detectar uno a partir de la entrada. Un estudio de 2023 de la Universidad de Cornell sobre la auto-detección de estilo de escritura encontró que inferir automáticamente el estilo a partir del texto de entrada estrecha el rango de voces que produce un modelo — el paso de detección homogeneiza la salida hacia la expectativa del modelo sobre el género, en lugar del registro propio del autor. La selección explícita evita esto: el operador declara el registro previsto en la frontera de la solicitud, y el pipeline aplica reglas específicas del género desde esa posición declarada. El operador ya sabe en qué registro está escribiendo; el sustrato refleja ese conocimiento de forma estructural en lugar de inferirlo.

## Auditoría del trabajo editorial realizado fuera del Doorman

Un clúster que realiza trabajo editorial localmente — sin enrutar la solicitud a través del Doorman — puede aun así enviar un registro de ello al registro de auditoría central con una única llamada. El evento lleva una etiqueta de tipo: `prose-edit` para trabajo editorial, además de `design-edit`, `graph-mutation`, `anchor-event` y `verdict-issued` para otras clases de trabajo que cubre el mismo endpoint. Esto mantiene el registro completo incluso cuando el trabajo ocurre fuera de la propia ruta de solicitud del Doorman — no genera, por sí mismo, una tupla de entrenamiento; solo el trabajo que realmente se enruta a través del pipeline de aprendizaje del Doorman lo hace.

Conforme al lenguaje de divulgación continua de `[ni-51-102]` y de acuerdo con los principios de información prospectiva de `[np-51-201]`: que cada acción editorial en toda la plataforma eventualmente produzca una tupla de entrenamiento firmada con veredicto para el adaptador propio de un cliente es un objetivo planificado, no un comportamiento actual confirmado.

## Véase también

- [[customer-hostability]]
- [[anti-homogenization-discipline]]
- [[apprenticeship-substrate]]
- [[citation-substrate]]
