---
schema: foundry-doc-v1
title: "Attestación criptográfica de cargas"
slug: crypto-attestation
short_description: "Mecanismo por el cual los nodos edge de PointSav demuestran la integridad del texto publicado mediante hash SHA-256 del lado del cliente, verificable por cualquier auditor."
category: security
type: topic
content_type: topic
quality: complete
status: archived
archived: 2026-08-03
archived_reason: "reemplazado por el piloto de autoría fresh-draft-first frente a los nuevos tokens de content-schema (schema-topic.yaml)"
superseded_by: crypto-attestation
audience: public
bcsc_class: forward-looking
language_protocol: PROSE-TOPIC
last_edited: 2026-07-30
editor: pointsav-engineering
paired_with: crypto-attestation.md
cites: []
language: es
---

**Corrección — reformulada como planificada/prevista (2026-07-30):** este artículo
describía originalmente una función de attestación en vivo. No existe tal código,
confirmado tanto en el motor del wiki como en una búsqueda posterior más amplia en la
flota de archivos (la única coincidencia de `crypto.subtle.digest` en todo el
monorepo es una función de integridad de guardado no relacionada, en una herramienta
de hojas de cálculo). El cuerpo se reformula a continuación como diseño
planificado/previsto, no como comportamiento actual.

La attestación criptográfica de cargas, una vez implementada, sería el mecanismo por el cual los nodos perimetrales de [[pointsav-overview|PointSav]] demostrarían dinámicamente la integridad de su contenido textual publicado a cualquier espectador. **No existe tal mecanismo hoy, ni en el motor del wiki ni en ningún otro lugar del monorepo.** Véase también [[cryptographic-ledgers|registros criptográficos]] y [[zero-execution-routing|enrutamiento de ejecución cero]].

## Cómo se prevé que funcione

El diseño prevé que los nodos perimetrales públicos calculen y muestren dinámicamente un hash SHA-256 de su contenido visible, de modo que cualquier auditor pudiera verificar independientemente que una divulgación no ha sido alterada. Nada de esto está implementado hoy.

## Postura de seguridad prevista

Una vez construida, la attestación sería de cero ejecución en el servidor para el cálculo del hash. El efecto previsto: un atacante intermediario que modificara el contenido en tránsito produciría una discrepancia de hash detectable.

## Aplicaciones previstas

- Divulgaciones regulatorias públicas en nodos perimetrales operados por [[pointsav-overview|PointSav]].
- Artículos del wiki de contenido donde la verificación de integridad importa a lectores institucionales.
- Cualquier superficie de contenido donde un lector necesite confirmar que está leyendo la versión publicada.

## Véase también

- [[worm-ledger-architecture]]
- [[cryptographic-ledgers]]
- [[machine-based-auth]]
- [[compounding-substrate]]
- [[sovereign-ai-routing]]
