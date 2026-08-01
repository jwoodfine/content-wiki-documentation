---
schema: foundry-doc-v1
title: "MCP y sistemas de diseño consumibles por agentes de IA"
slug: mcp-ai-agent-consumable-design-systems
short_description: "Explica por qué el Sistema de Diseño PointSav expone una superficie legible por máquinas — un punto de conexión Model Context Protocol alojado en la propia infraestructura, una API de búsqueda de tokens y una exportación de tokens DTCG — para que los agentes de codificación de IA consulten datos actuales de tokens y componentes desde el mismo registro que genera la documentación para lectores humanos, sin que ninguna consulta salga de la infraestructura del anfitrión."
category: design-system
type: topic
content_type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-01
editor: pointsav-engineering
paired_with: mcp-ai-agent-consumable-design-systems.md
cites: []
---

Un sistema de diseño es tan confiable como el código que se escribe sobre él.
Cuando ese código lo escribe un agente de codificación de IA, la imagen que
el agente tiene del sistema — qué tokens existen, a qué valores resuelven,
cuál es el marcado vigente de un componente — proviene normalmente de una
instantánea de entrenamiento o de un extracto pegado de la documentación.
Ambos quedan obsoletos en cuanto el sistema avanza. El Sistema de Diseño
PointSav aborda esto publicando una superficie legible por máquinas junto a
la superficie para lectores humanos: un punto de conexión Model Context
Protocol, una API de búsqueda de tokens y una exportación versionada de
tokens, todos respondidos desde el mismo registro que genera cada página de
la documentación. Un agente que pregunta a qué resuelve un token obtiene la
respuesta de hoy, con los mismos datos que está viendo un lector humano.

Como el servidor del sistema de diseño es autoalojable, esa superficie corre
en la infraestructura de la propia organización que lo adopta. Cada consulta
de un agente — una búsqueda puntual de un token o un barrido completo de
componentes — se responde localmente. Nada sobre el código, los prompts o el
uso de componentes de la organización se envía a un tercero.

## Qué es MCP

El Model Context Protocol (MCP) es un protocolo abierto para conectar
aplicaciones de modelos de lenguaje con herramientas y fuentes de datos
externas. Anthropic lo presentó en noviembre de 2024 y desde entonces ha
sido adoptado ampliamente en la industria, incluidos otros grandes
proveedores de IA. La especificación se publica abiertamente en
modelcontextprotocol.io; la revisión vigente al momento de escribir está
fechada 2025-11-25.

Técnicamente, MCP es un protocolo de mensajes JSON-RPC 2.0 entre tres
partes: un anfitrión (la aplicación de modelo de lenguaje — un agente de
codificación, un asistente de IDE), un cliente (el conector dentro de ese
anfitrión) y un servidor (el servicio que expone contexto y capacidades).
Los servidores ofrecen tres tipos de primitivas: herramientas que el modelo
puede invocar, recursos que puede leer y plantillas de prompts. La
especificación cita el Language Server Protocol como inspiración — del mismo
modo en que LSP permitió que cualquier editor hablara con cualquier cadena
de herramientas de lenguaje, MCP permite que cualquier agente hable con
cualquier proveedor de contexto sin una integración a medida por cada par.

Una propiedad adicional de la especificación importa para este artículo: su
sección de seguridad es explícita en que los anfitriones deben obtener el
consentimiento del usuario antes de exponer datos a los servidores y no
deben transmitir datos de recursos a otros destinos sin consentimiento. El
protocolo anticipa despliegues donde los datos detrás del servidor son
privados. Un servidor de sistema de diseño corriendo en el hardware propio
de una organización es exactamente ese caso.

## Sistemas de diseño como contexto para agentes — antecedentes

Servir contexto de sistemas de diseño a agentes de codificación mediante MCP
es un patrón establecido, no una invención de PointSav. Figma distribuye un
servidor MCP de Dev Mode que permite a agentes en herramientas como VS Code,
Cursor y Claude Code leer contexto de componentes, estilos y variables desde
archivos de Figma, y ha sostenido públicamente que los servidores MCP son el
mecanismo por el cual los sistemas de diseño se vuelven útiles para las
herramientas de IA. zeroheight ofrece una integración MCP que expone a los
agentes de codificación las guías de componentes, los tokens y las reglas de
uso de un equipo desde su plataforma de documentación alojada.

Lo que distingue la implementación de este sistema de diseño no es la idea
sino el modelo de despliegue y el recorrido de los datos. Las ofertas
anteriores son servicios alojados: el contexto del sistema de diseño vive
con un proveedor, y las consultas de los agentes transitan la
infraestructura de ese proveedor. Aquí, el servidor MCP viaja dentro del
mismo binario autoalojable que el propio sitio de documentación. No existe
una variante alojada de esta superficie — en infraestructura propia es la
única forma en que se ofrece — y no hay una segunda copia de los datos: el
punto de conexión lee el mismo registro desde el que se generan las páginas
del sitio.

## La superficie para máquinas, en concreto

El servidor del sistema de diseño expone tres puntos de entrada para
máquinas.

- **`POST /mcp`** — el punto de conexión MCP. Habla JSON-RPC 2.0 según la
  especificación y expone cuatro herramientas: `list_components` (todos los
  componentes que el registro conoce, filtrables por origen),
  `get_component_recipe` (el HTML, el CSS, la guía ARIA, los tokens
  consumidos y las variantes de un componente con nombre — la misma receta
  desde la que el sitio genera sus vistas previas en vivo), `get_token`
  (resuelve un token de diseño individual por su nombre de propiedad
  personalizada CSS o por su ruta DTCG) y `search_design_system` (búsqueda
  de texto completo sobre componentes, tokens y notas de investigación, para
  un agente que aún no conoce el nombre exacto de lo que necesita).
- **`GET /tokens/search`** — el mismo índice de tokens como consulta HTTP
  simple, para herramientas que prefieren una petición ordinaria a hablar
  MCP.
- **`GET /bundles/:name/download`** — paquetes de archivos versionados,
  incluida la exportación completa de tokens en formato Design Tokens
  Community Group (DTCG). Un agente o una cadena de compilación que solo
  necesita los valores de los tokens puede descargar este archivo
  directamente y no tocar nunca el punto de conexión MCP.

El principio de diseño que une a los tres es la fuente única. Los conteos de
tokens en las páginas de documentación, las vistas previas en vivo de los
componentes, las respuestas de las herramientas MCP y la exportación DTCG se
leen todos de un solo registro. Si el registro está mal, todo está mal de la
misma manera y al mismo tiempo — no existe una ruta de código exclusiva para
máquinas que pueda derivar mientras el sitio para humanos se ve bien, ni un
espejo cacheado de la documentación en el que un agente confíe después de
quedar obsoleto.

## Por qué la capa de tokens es la altitud correcta

Un agente que genera código de interfaz no necesita discreción sobre las
decisiones visuales; necesita un vocabulario pequeño y vigente de decisiones
válidas. Restringir la generación al vocabulario de tokens y componentes del
sistema de diseño — y dar al agente una vía en vivo para consultar ese
vocabulario — reduce lo que puede salir mal en el código generado al rango
que el sistema permite. El agente selecciona un token semántico en lugar de
inventar un valor hexadecimal, y reutiliza la receta de un componente en
lugar de aproximarla de memoria. Es el mismo argumento que justifica los
tokens de diseño para los equipos humanos, aplicado a un consumidor que lee
JSON con más fluidez de la que lee prosa.

## Licencias

Dos licencias distintas aplican al material que este artículo trata, y vale
la pena ser preciso con la distinción. Los datos de los tokens de diseño —
el JSON DTCG que consumen los agentes, los plugins y las cadenas de
compilación — se publican bajo Apache-2.0, la misma convención que usan los
grandes sistemas de diseño abiertos. El servidor que responde las consultas
MCP y de registro se publica bajo AGPL-3.0-or-later. Y este artículo mismo,
como parte del wiki de documentación, está licenciado CC BY 4.0 — una
licencia de contenido, distinta de las dos anteriores. Consumir los tokens
conlleva los términos de Apache-2.0; ejecutar el servidor conlleva los
términos de AGPL; reutilizar este texto conlleva los términos de atribución
de CC BY.

## Alcance y límites

Dicho con claridad: el conjunto de puntos de conexión descrito arriba —
`/mcp` con sus cuatro herramientas, `/tokens/search` y la ruta de descarga
de paquetes — está implementado en el código fuente del servidor del sistema
de diseño y es la superficie que expone una instancia autoalojada. La
documentación pública v3 de esa superficie, incluida la página Agents que la
presenta a lectores humanos, está bajo revisión del operador al momento de
escribir, y aquí se describe en términos de la capacidad del servidor, no de
una página publicada específica. No se afirma que la calidad del código de
los agentes mejore en una medida cuantificada; la arquitectura de registro
único es una decisión de diseño cuya justificación se da arriba, no un
resultado medido. Las comparaciones con ofertas alojadas son estructurales —
modelo de despliegue y recorrido de los datos — y se basan en la
documentación pública de esos proveedores al momento de escribir.

---

*Este artículo es material de contexto para lectores que encuentran por
primera vez la superficie de integración para máquinas del sistema de
diseño, previo a la guía operativa para conectar un agente específico a una
instancia autoalojada.*
