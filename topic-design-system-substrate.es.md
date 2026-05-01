---
schema: foundry-doc-v1
title: "El substrato del sistema de diseño"
slug: topic-design-system-substrate
lang: es
paired_with: topic-design-system-substrate.md
category: architecture
status: published
last_edited: 2026-04-28
editor: pointsav-engineering
bcsc_class: current-fact + forward-looking
cites:
  - mcp-spec
  - ni-51-102
  - osc-sn-51-721
---

## Visión estratégica

El substrato del sistema de diseño de PointSav es un motor autoalojado que el cliente posee y controla directamente. Su principio central es sencillo: el sistema de diseño de una organización debe residir en el repositorio Git de esa organización, firmado con su propia clave criptográfica, reproducible en cualquier herramienta. La dependencia de infraestructura de terceros no es un requisito técnico; es una decisión arquitectónica que el substrato invierte deliberadamente.

La instancia de referencia está disponible en `design.pointsav.com`. Cada cliente SMB que adopta el substrato opera su propia instancia en su propio dominio. Un único código base, una única forma de despliegue, dos contextos: la vitrina del proveedor y la instancia del cliente.

## Las tres inversiones estructurales

El mercado de herramientas de sistemas de diseño se ha concentrado históricamente en el segmento empresarial. El substrato responde a esto con tres inversiones estructurales:

**Primera inversión — propiedad del cliente.** Los tokens, los componentes y el historial de decisiones de diseño viven en el repositorio del cliente. El coste de migración cae hacia cero porque el estado canónico es siempre accesible para el cliente.

**Segunda inversión — razonamiento legible por máquina.** El directorio `research/` del substrato almacena la justificación de cada decisión de diseño como un archivo Markdown estructurado, con metadatos que los agentes de inteligencia artificial pueden consumir a través del protocolo MCP `[mcp-spec]`. Los sistemas de diseño convencionales publican únicamente los valores de los tokens; el substrato publica también el porqué, en el mismo nivel de accesibilidad para las herramientas.

**Tercera inversión — agnóstico respecto al editor.** Los tokens siguen el formato del W3C Design Tokens Community Group (DTCG), que es el estándar de interoperabilidad convergente para la industria en el horizonte 2026–2030. Figma, Penpot, Sketch y la autoría directa en JSON son todos caminos válidos. El substrato no favorece ningún editor en particular porque no tiene incentivo comercial para hacerlo.

## La capa de atestación

El historial del substrato se ancla mensualmente a Sigstore Rekor, produciendo un registro Merkle con raíz en el cliente. Cada trimestre, el operador del substrato emite un informe firmado —la Trustworthy System Attestation (TSA)— que cita los puntos de control del vault, la cadena `allowed_signers` del cliente y el registro WORM. Esta atestación cubre los artefactos de diseño del cliente: un alcance diferente e independiente de cualquier auditoría SOC 2 de terceros.

## El vocabulario de Carbon como base

El substrato importa el vocabulario de tokens primitivos de IBM Carbon como capa base. Esta elección responde a tres factores: la familiaridad del vocabulario entre practicantes de sistemas de diseño en sectores regulados (finanzas, salud, administración pública); el nivel de conformidad de accesibilidad que Carbon garantiza desde sus elecciones primitivas (WCAG 2.2 AAA); y la naturaleza permisiva de la convención de nomenclatura, que es un artefacto de documentación, no un activo de marca registrada.

El trabajo específico de marca de cada cliente ocurre en la capa semántica (`themes/<marca>/`), sin necesidad de aprender una taxonomía nueva.

## Horizonte planificado

El substrato está en producción como v0.0.1 desde el 28 de abril de 2026. El trabajo futuro planificado incluye la evaluación de una capa primitiva alternativa (Untitled UI, con licencia MIT) como segunda opción de base, y una modalidad de alojamiento gestionado para clientes SMB que prefieran no operar la infraestructura. Ambas son direcciones de producto previstas, sujetas a evaluación técnica y capacidad operativa; no representan compromisos de calendario.

*Esta sección contiene información prospectiva en los términos de `[ni-51-102]` y `[osc-sn-51-721]`. Los resultados reales pueden diferir de los objetivos descritos.*

## Para profundizar

La documentación técnica completa está disponible en inglés en el documento correspondiente (`topic-design-system-substrate.md`). Los runbooks operativos se encuentran en `vault-privategit-design/GUIDE-deploy-design-substrate.md`. La convención de arquitectura se documenta en `conventions/design-system-substrate.md` y la reclamación doctrinal de referencia es la #38 en `DOCTRINE.md`.

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.