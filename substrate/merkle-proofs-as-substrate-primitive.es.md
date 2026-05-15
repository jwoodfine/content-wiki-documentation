---
schema: foundry-doc-v1
title: "Pruebas de Merkle como Primitiva de Sustrato"
slug: merkle-proofs-as-substrate-primitive
category: substrate
status: stub
bcsc_class: no-disclosure-implication
last_edited: 2026-04-28
editor: pointsav-engineering
language: es
paired_with: merkle-proofs-as-substrate-primitive.md
cites:
  - rfc-9162
  - doctrine-claim-33
  - doctrine-claim-34
---

`system-core` incluye dos primitivas de prueba Merkle según RFC 9162 — pruebas de inclusión y pruebas de consistencia — como piso criptográfico del Sustrato del Libro de Capacidades (afirmación doctrinal #33). Junto con el formato de checkpoint firmado C2SP, validan la escritura en el libro y hacen auditable el estado de capacidades sin exigir buena conducta al consumidor.

## Qué son las pruebas de Merkle

Los árboles hash comprueban una secuencia de hojas: cada hoja se hash con un prefijo de separación de dominio 0x00; cada nodo interno hash dos hijos con prefijo 0x01 (RFC 9162 §2.1.1). El hash raíz compromete toda la secuencia. Los caminos de prueba son logarítmicos en el tamaño del árbol. La distinción importante: *comprometerse* con una secuencia (hash raíz) es distinto de *probar pertenencia o extensión* de esa secuencia (camino de prueba).

## Dos variantes: inclusión y consistencia

Las pruebas de inclusión (RFC 9162 §2.1.3) demuestran que una hoja determinada está presente en un árbol de tamaño dado. Las pruebas de consistencia (RFC 9162 §2.1.4) demuestran que un árbol de tamaño N+k es una extensión válida de uno de tamaño N. Las dos variantes responden preguntas distintas: "¿está esta hoja en el registro?" frente a "¿es este registro más reciente una continuación del anterior?" El mismo árbol hash soporta ambas.

## Pruebas de inclusión e `system-core`

La estructura `InclusionProof` y su método `verify` implementan el algoritmo de recorrido de árbol de RFC 9162 §2.1.3. Cobertura de pruebas: 11 tests incluyendo una cuadrícula de verificación completa para tamaños de árbol 1–8. Coste típico de verificación: 10–20 microsegundos.

## Pruebas de consistencia en `system-core`

La estructura `ConsistencyProof` y su método `verify` inicializan ambos acumuladores desde `hashes[0]` y rastrean contadores `fn`/`sn`. Nueve variantes de error distinguen fallos estructurales de criptográficos. Cobertura: 11 tests en `consistency_proof.rs`.

## Primitivas compuestas sobre `SignedCheckpoint`

`SignedCheckpoint::verify_inclusion_proof` y `verify_consistency_proof` encadenan tres pasos en una sola llamada: invariante de tamaño de árbol → verificación de firma → verificación de prueba sin procesar. Esta composición es la superficie de API orientada al núcleo.

## Por qué importa como primitiva de sustrato

El Sustrato del Libro de Capacidades (afirmación #33) exige un registro Merkle con raíz en el cliente para que el estado de capacidades sea auditable. El Sustrato de Dos Bases Soberanas (afirmación #34) exige que un despliegue como artefacto criptográfico sea heredable entre sustratos nativos (seL4) y compatibles (NetBSD). Las pruebas de inclusión y consistencia hacen posibles ambas propiedades sin exigir buena conducta al consumidor.

## Véase también

- capability-ledger-substrate — el libro que protegen las pruebas
- [[worm-ledger-architecture]] — Diseño del libro WORM que compone con la verificación de checkpoints
- [[disclosure-substrate]] — Cómo la cadena de auditoría satisface las obligaciones de divulgación

## Referencias

- **RFC 9162** — Certificate Transparency Version 2.0. IETF, 2021. https://datatracker.ietf.org/doc/html/rfc9162
- **Afirmación doctrinal #33** — El Sustrato del Libro de Capacidades. Foundry DOCTRINE.md v0.1.0.
- **Afirmación doctrinal #34** — El Sustrato de Dos Bases Soberanas. Foundry DOCTRINE.md v0.1.0.
