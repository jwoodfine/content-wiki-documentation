---
schema: foundry-doc-v1
content_type: topic
title: "Substrato del sistema de diseño"
slug: design-system-substrate
short_description: "El sustrato del sistema de diseño es un motor de sistema de diseño auto-alojado y propiedad del cliente que almacena tokens y componentes en el repositorio Git del cliente, los sirve a través de un extremo MCP legible por máquina, y utiliza el formato de token DTCG de W3C para permanecer agnóstico del editor."
lang: es
paired_with: design-system-substrate.md
category: substrate
index_group: core-named-substrates
status: active
last_edited: 2026-08-24
editor: pointsav-engineering
bcsc_class: public-disclosure-safe
cites:
 - mcp-spec
 - sigstore-rekor-v2
 - c2sp-tlog-tiles
 - ni-51-102
 - np-51-201
---


El substrato del sistema de diseño de PointSav es un motor de sistema de diseño autoalojado y propiedad del cliente. La vitrina del proveedor en `design.pointsav.com` es la instancia canónica. Cada cliente SMB que bifurca el substrato opera su propia instancia en su propio dominio — un único código base, una única forma de despliegue, dos contextos.

Los sistemas de diseño gestionados de escala empresarial colocan los tokens, los componentes y las decisiones de diseño dentro de la propia infraestructura del proveedor de la plataforma. Los archivos de tema del cliente viven en el almacenamiento del proveedor; la continuidad operativa del proveedor es una dependencia para cada build de UI. Las herramientas SaaS empresariales de este espacio tienen precios de entrada prohibitivos para clientes SMB.

El substrato invierte ese patrón en tres ejes estructurales: el sistema de diseño del cliente vive en el repositorio Git del cliente, firmado con la clave del cliente, reproducible en cualquier herramienta; la investigación de decisiones de diseño vive en la misma bóveda que los tokens y componentes, servida a través del mismo extremo del [[mcp-substrate-protocol|Protocolo de Contexto de Modelo]] `[mcp-spec]` que usan los agentes de IA; y los tokens se almacenan en el formato del W3C Design Tokens Community Group (DTCG), lo que mantiene al substrato agnóstico del editor por construcción.

## Arquitectura de bóveda inmutable

El contenido del substrato vive en un directorio de bóveda por inquilino:

```
<bóveda-del-inquilino>/
├── elements/    capas de tokens DTCG, anidadas por slug
├── components/  archivos de receta HTML+CSS+ARIA, anidados por slug
├── guidelines/  guía de uso y accesibilidad, anidada por slug
├── developing/  referencia orientada a ingeniería (plana)
├── designing/   referencia orientada a diseño (plana)
├── about/       documentación a nivel de substrato (plana)
├── research/    justificación de decisiones de diseño legible por IA (markdown, plana)
└── exports/     cachés derivadas (Figma, Tailwind, Style Dictionary)
```

La bóveda es la única capa canónica. Las exportaciones renderizadas — JSON de Variables de Figma, configuración de Tailwind, variables CSS, builds de Style Dictionary — son cachés derivadas, recomputables a partir de los directorios canónicos anteriores.

El motor del substrato es un servicio HTTP sin estado que lee la bóveda desde disco. El aislamiento por inquilino se logra ejecutando un proceso de motor por inquilino, cada uno apuntando a su propia bóveda. La persistencia por encima del sistema de archivos de la bóveda se realiza a través del [[worm-ledger-architecture|libro WORM]] del substrato. El historial de tokens y componentes se ancla mensualmente a Sigstore Rekor `[sigstore-rekor-v2]`, produciendo un registro Merkle con raíz en el cliente usando el formato C2SP tlog-tiles `[c2sp-tlog-tiles]`.

## Backplane de contexto legible por máquina

El directorio `research/` es el elemento estructuralmente más novedoso del substrato. Cada decisión de diseño vive como un archivo Markdown estructurado:

```
---
schema: foundry-design-research-v1
component_or_token: button-primary
decision_type: component-introduction
authored: 2026-04-28
authored_by: nombre-del-miembro-del-equipo-de-diseño O id-del-agente-ia
status: ratified
brand_voice_alignment: [confident, direct, professional]
accessibility_targets: [wcag-2-2-aa, focus-visible]
ai_consumption_hint: "Al generar un botón para una acción
 primaria, usa este componente. Cuando la acción sea
 destructiva, usa button-danger en su lugar."
---
```

El frontmatter es legible por máquina; el cuerpo es legible por humanos. Los agentes de IA consumen la investigación a través del [[mcp-substrate-protocol|extremo MCP]] `[mcp-spec]` del substrato en tiempo de decodificación. Los métodos incluyen `get_component_recipe`, `list_components`, `get_token`, `search_design_system` y `list_token_families`. Un agente de IA registra el substrato como servidor MCP y luego lo consulta durante la generación de UI para alinearse con la intención de marca de la SMB.

Los sistemas de diseño que publican solo valores de tokens y formas de componentes omiten la justificación detrás de esas elecciones. El substrato publica ambos, en el mismo nivel legible por máquina, servidos a través del mismo extremo.

## Estándar editorial agnóstico

El formato del W3C Design Tokens Community Group alcanzó su especificación estable 2025.10 en octubre de 2025. Figma envía importación y exportación nativas de DTCG; Penpot es nativo de DTCG desde Penpot 2.x; Style Dictionary, Specify y Tokens Studio consumen todos DTCG.

Del lado del consumidor:

- **Figma** — vía el plugin Tokens Studio o el sistema nativo de variables de Figma
- **Penpot** — importa DTCG de forma nativa; el emparejamiento substrato-Penpot es el flujo de trabajo de diseño totalmente de código abierto que la plataforma recomienda a los clientes SMB que prefieren un editor autoalojable
- **Sketch** — vía el plugin Tokens Studio para Sketch
- **Autoría manual** — los diseñadores editan JSON DTCG directamente; esta es también la vía más accesible para los agentes de IA

El cliente elige el editor; el substrato no requiere uno en particular.

## Componentes primitivos de referencia

El substrato importa el vocabulario de tokens primitivos de IBM Carbon como la capa base de cada nueva instancia. La nomenclatura de color sigue la convención de Carbon (`gray-10` hasta `gray-100`). La escala tipográfica sigue las familias productiva y expresiva de Carbon. El espaciado sigue la cuadrícula de 8px de Carbon. El anillo de foco sigue el estilo de Carbon conforme a WCAG 2.2 AAA.

El trabajo específico de marca ocurre en la capa semántica de tokens, no en la capa primitiva. Los clientes SMB extienden con anulaciones de marca sin necesidad de reaprender una nueva taxonomía de componentes.

Carbon se eligió por tres razones: superficie de familiaridad (amplia memoria muscular de diseño accesible entre los profesionales), piso de accesibilidad (conformidad WCAG 2.2 AAA integrada en las elecciones primitivas), y licenciamiento permisivo de la forma (los valores de los tokens de Carbon están públicamente documentados; IBM Plex tiene licencia permisiva; la convención de nomenclatura es un artefacto de documentación, no un activo de marca registrada).

Lo que no se importa de Carbon: temas específicos de IBM Cloud, implementaciones de componentes específicas de React, el logotipo de IBM y la marca "Carbon", micro-interacciones de componentes específicas de Carbon.

Un futuro hito planificado podría introducir una capa primitiva alternativa — Untitled UI (con licencia MIT) es candidata para una segunda capa primitiva en una versión posterior. Ese trabajo está previsto y sujeto a evaluación técnica; no se compromete ningún cronograma. Las declaraciones prospectivas sobre futuros hitos están sujetas a los factores de precaución descritos en `[ni-51-102]` y `[np-51-201]`.

## Procedimiento de bifurcación soberana

Un cliente SMB bifurca el proyecto clonando el repositorio fuente, compilando el motor del substrato (un binario nativo de Rust), inicializando una bóveda a partir de la plantilla canónica, editando la capa semántica de tokens de su marca, y ejecutando el script de arranque para configurar el servicio y TLS. El runbook operativo en `vault-privategit-design/GUIDE-deploy-design-substrate.md` cubre el procedimiento completo.

El cliente termina con un substrato de sistema de diseño totalmente autoalojado y de su propiedad. Sin dependencia de SaaS. Sin tiempo de ejecución de hiperescalador. Sus archivos de tema y cualquier entrada de investigación que redacten son su propio producto de trabajo, en su propio repositorio Git, firmados con su propia clave.

## Distinciones estructurales del substrato

**La propiedad de Git por inquilino** requiere una identidad de firma por inquilino (la cadena `allowed_signers` del cliente). Las plataformas alojadas en infraestructura compartida no pueden acomodar esto sin convertirse en un proveedor de alojamiento Git.

**El backplane de investigación legible por IA en forma propiedad del cliente** requiere alojamiento por cliente. Una plataforma puede publicar su propia investigación de diseño; no puede publicar la investigación del sistema de diseño de la SMB cliente, porque no aloja el sistema de diseño de esa SMB.

**Atestación con raíz en el cliente.** La [[capability-ledger-substrate|Atestación de Sistema Confiable]] trimestral del substrato combina el [[worm-ledger-architecture|libro WORM]], el anclaje a Sigstore Rekor `[sigstore-rekor-v2]` y los `allowed_signers` por inquilino. La atestación resultante cubre los datos de diseño del cliente — no los controles del proveedor de la plataforma.

**Agnosticismo de editor.** Las plataformas comerciales de sistemas de diseño tienen un incentivo para mantener al cliente dentro de su ecosistema de editor. El substrato no tiene tal incentivo — DTCG es el denominador común.

Las cuatro propiedades se refuerzan mutuamente. Eliminar cualquiera debilita a las demás.

## Modelos operativos excluidos

El substrato no es un reemplazo de Storybook. Storybook es un renderizador paralelo; el substrato posee su propio renderizado.

No es un competidor de los editores de diseño. Los editores de diseño (Figma, Penpot, Sketch) son las herramientas en las que trabajan los diseñadores; el substrato es el almacén canónico con el que esos editores interoperan vía DTCG.

No es una plataforma SaaS. Una opción de alojamiento gestionado para clientes SMB que prefieran no operar el servicio ellos mismos es una oferta futura planificada, sujeta a la capacidad del operador y la demanda del cliente; el código del substrato seguirá siendo autoalojable en todos los casos.

No es una elección de framework de JavaScript. Los componentes son recetas HTML+CSS+ARIA; el framework elegido por el cliente consume la receta.

No es un artefacto de contenedor. El substrato se distribuye como un binario nativo desplegado vía systemd.

## Véase también

- [[compounding-substrate]]
- [[substrate-native-compatibility]]
- [[customer-hostability]]
