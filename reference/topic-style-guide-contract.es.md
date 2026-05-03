---
schema: foundry-doc-v1
title: "Guía de estilo: Contrato"
slug: topic-style-guide-contract.es
category: reference
type: topic
quality: core
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: topic-style-guide-contract.md
---

Una plantilla de contrato en el sistema de protocolos de lenguaje
de Foundry pertenece a la familia LEGAL. Es la plantilla con
mayor restricción estructural del sistema: cinco secciones
requeridas en orden fijo, registro profesional-legal y
enrutamiento predeterminado al Nivel C.

## Cuándo usar esta plantilla

Se usa cuando se elabora o revisa un contrato para un inquilino
asociado a Foundry: un acuerdo de servicios, un acuerdo con
proveedores, un contrato de empleo u otro instrumento bilateral.

El parámetro `default_routing = "tier-c"` significa que el
Doorman envía el trabajo de contratos a un modelo de Nivel C
salvo que el operador haya habilitado explícitamente una ruta
diferente. La generación local en Nivel A o Nivel B está
permitida únicamente cuando el inquilino dispone de un corpus
jurídico suficiente y el operador ha confirmado la ruta.

## Estructura requerida

La plantilla exige cinco secciones en este orden:

1. **Parties** — nombres legales completos de todas las partes.
2. **Recitals** — contexto de fondo en forma "POR CUANTO"
   (WHEREAS).
3. **Definitions** — términos definidos, listados en orden
   alfabético y en mayúscula cuando se usan en el documento.
4. **Operative clauses** — cláusulas numeradas; una obligación
   por cláusula.
5. **Signature block** — firmas de ejecución con nombres, cargos
   y fechas.

## Aviso obligatorio

Todo borrador de contrato lleva el encabezado visible
**"DRAFT — for legal review"**. Eliminarlo antes de la revisión
legal formal es una violación de postura. Este documento nunca
sustituye el asesoramiento de un abogado.

## Véase también

- [[topic-style-guide-cla|Guía de estilo — Acuerdo de Licencia de Contribuidor]]
- [[topic-language-protocol-substrate|Substrato del Protocolo de Lenguaje]]
- [[topic-canadian-simple-copyright|Derechos de Autor Simplificados (Canadá)]]
