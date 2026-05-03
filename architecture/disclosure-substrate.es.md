---
schema: foundry-doc-v1
document_version: 0.1.0
title: "El Sustrato de Divulgación"
slug: disclosure-substrate.es
lang: es
paired_with: disclosure-substrate.md
category: architecture
status: pre-build
last_edited: 2026-04-28
editor: pointsav-engineering
audience: vendor-public
bcsc_class: disclosure-implication
language_protocol: PROSE-TOPIC
cites:
  - ni-51-102
  - osc-sn-51-721
  - bcsc-continuous-disclosure
  - sec-17a-4-f
  - eidas-qualified-preservation
  - ixbrl-esef
  - esap-eu-2027
  - opentimestamps
  - rfc-3161
  - sigstore-rekor-v2
  - cloud-act-us
---

La práctica convencional de relaciones con inversionistas divide la
divulgación en tres capas: documentación interna, un sitio de relaciones
con inversionistas administrado por un proveedor externo, y presentaciones
regulatorias periódicas en plataformas como SEDAR+ o EDGAR. Las tres capas
se escriben por separado, a menudo son inconsistentes entre sí y resultan
difíciles de auditar en conjunto.

El sustrato de divulgación invierte este patrón. La wiki de documentación
de PointSav —el mismo corpus que escriben los colaboradores internos— es
el registro de divulgación primario. No es una descripción de las
divulgaciones de la empresa: es la divulgación misma.

## Qué lo hace posible estructuralmente

Cada artículo del corpus Markdown (denominado TOPIC) lleva una cadena
criptográfica de autoría, un hash de contenido estable y, en fases
planificadas de implementación del motor wiki, marcas de tiempo ancladas
a registros externos (OpenTimestamps `[opentimestamps]` hacia la cadena
de bloques de Bitcoin; RFC 3161 `[rfc-3161]` con reconocimiento legal en
la UE y la mayoría de jurisdicciones de derecho consuetudinario). Cada
confirmación (*commit*) está firmada. Reguladores y analistas pueden leer
exactamente el mismo corpus que alimenta la presentación regulatoria.

Las afirmaciones sobre capacidades futuras en este artículo son
prospectivas (*forward-looking*) conforme a `[ni-51-102]` y
`[osc-sn-51-721]`. Los resultados reales dependen de la capacidad de
ingeniería, la priorización por parte del operador y los supuestos
materiales descritos en el artículo en inglés.

## Adaptadores por jurisdicción (planificados)

Se planea una capa de adaptadores enchufables para transformar el corpus
Markdown en el formato de presentación que exige cada superficie
regulatoria: SEDAR+ para emisores canadienses bajo `[ni-51-102]`, SEC
EDGAR para emisores en Estados Unidos, el mandato ESEF de la UE con
iXBRL `[ixbrl-esef]` (Fase 1 de ESAP prevista para julio de 2027
`[esap-eu-2027]`), y plataformas equivalentes en Japón, Corea e Israel.

Para jurisdicciones que exigen preservación electrónica cualificada —como
eIDAS `[eidas-qualified-preservation]` en la UE— los adaptadores están
diseñados para incluir la cadena de certificados del emisor y el token de
marca de tiempo RFC 3161 en el paquete de presentación. Cada adaptador
está planificado como un crate de Rust separado; las nuevas jurisdicciones
son aditivas y no modifican el núcleo del sustrato.

## Sustitución de sustrato aplicada a plataformas de divulgación

Conforme a la Reclamación Doctrinal #29 (Sustitución de Sustrato), la
wiki reemplaza la función de registro primario que convencionalmente ocupa
una plataforma de relaciones con inversionistas operada por un tercero.
La razón es estructural: la Ley CLOUD `[cloud-act-us]` de Estados Unidos
extiende la autoridad extraterritorial de acceso a datos sobre
proveedores de ese país, independientemente de dónde estén almacenados
los datos del cliente. Para un emisor en una jurisdicción donde la
soberanía del proveedor importa —RGPD europeo tras Schrems II, mandatos
de residencia de Salud Canadá, PDPL de Arabia Saudita— el sustrato ofrece
que el registro viva bajo la infraestructura propia del emisor, firmado
con su propia clave.

Los servicios que plataformas de relaciones con inversionistas
convencionales proveen y que el sustrato no replica —segmentación de
inversionistas, agregación de consenso del lado de la venta, analítica de
vigilancia— son componibles mediante adaptadores MCP del Anillo 1 a medida
que el sustrato madura. El sustrato reemplaza donde la sustitución es
limpia; compone donde no lo es.

## El principio fundamental

Nada en el sustrato declara *"cumplimos con NI 51-102"*. El cumplimiento
es el artefacto: el historial de confirmaciones firmadas, la trazabilidad
de citas en el frontmatter de cada artículo, los tokens de marca de tiempo
en cada MINOR del Doctrinario, las entradas de CHANGELOG aptas para
revisión legal. Un regulador o auditor que revise el corpus puede
reconstruir qué sabía Foundry, cuándo y cómo actuó al respecto, sin
instantáneas (*snapshots*) ni declaraciones de cumplimiento periódicas.

Para una descripción completa de la arquitectura técnica, los adaptadores
planificados y el diseño de fundamentación de IA, consulte el artículo en
inglés: [The Disclosure Substrate](topic-disclosure-substrate.md).

## Véase también

- [El Sustrato Compuesto](topic-compounding-substrate.es.md)
- [Compatibilidad nativa del sustrato](topic-substrate-native-compatibility.md)
- [Postura de derecho de autor simple canadiense](topic-canadian-simple-copyright.es.md)
- Convención operacional: `conventions/disclosure-substrate.md`
