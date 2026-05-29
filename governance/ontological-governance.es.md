---
schema: foundry-doc-v1
title: "Gobernanza ontológica"
slug: ontological-governance
short_description: "La gobernanza ontológica describe los cuatro registros de control auto-reparadores que rigen cómo service-content clasifica y acumula conocimiento, y el bucle de verificación humana que mantiene precisos los datos de identidad extraídos antes de ser comprometidos permanentemente."
category: governance
type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-19
editor: pointsav-engineering
paired_with: ontological-governance.md
cites: []
---

Los sistemas de clasificación automatizada derivan con el tiempo: las categorías se amplían o contraen, el vocabulario se fragmenta y los errores se acumulan más rápido de lo que pueden corregirse. La **gobernanza ontológica** evita esta deriva mediante dos mecanismos estructurales: cuatro libros contables de control con velocidad de actualización deliberadamente lenta que definen el vocabulario de clasificación, y un bucle de verificación humana que obliga a los fragmentos de identidad extraídos a pasar por revisión humana antes de que se escriban permanentemente en el libro contable verificado. Para un operador regulado, esto significa que el grafo de conocimiento de la plataforma permanece auditable y los registros de identidad se mantienen precisos sin curación manual continua.

## El problema de la deriva de clasificación

Sin gobernanza activa, los sistemas de clasificación automática derivan con el tiempo. Una categoría que inicialmente captura un conjunto de conceptos coherente se amplía o se contrae a medida que los datos llegan y los patrones cambian. La deriva acumulada socava la integridad de los datos institucionales de larga duración.

## Los cuatro libros contables de control

La gobernanza ontológica opera a través de cuatro libros contables CSV limitados en velocidad que definen el vocabulario de clasificación de [[service-content]]. Cada libro contable:

- Define las categorías y términos válidos para un dominio particular.
- Está limitado en velocidad para prevenir cambios de vocabulario masivos que invalidarían clasificaciones históricas.
- Es legible por humanos (CSV) y versionado en Git — la historia de cambios de clasificación es auditable.

## El bucle de verificación humana

La gobernanza ontológica también abarca el [[verification-surveyor|Verificador de Identidad]], que fuerza los fragmentos de identidad extraídos a través de la revisión humana antes de que se escriban permanentemente en el [[worm-ledger-design|libro contable verificado]]. Los dos mecanismos sirven al mismo objetivo: prevenir que los errores de clasificación acumulados socaven la integridad de los datos institucionales a largo plazo.

## Por qué importan las velocidades de actualización asimétricas para los operadores regulados

La estructura asimétrica del libro contable produce una propiedad que importa en contextos regulados: la base del grafo de conocimiento es lo suficientemente estable para ser auditada. Un evaluador de adquisiciones o un revisor de cumplimiento que lea datos extraídos hace dos años y datos extraídos la semana pasada los encontrará clasificados contra la misma taxonomía de Arquetipos y Plan de Cuentas — las categorías no han derivado. Solo la capa de Temas, que se actualiza con más frecuencia, refleja el enfoque operativo actual.

Para los propósitos de divulgación financiera, esto significa que el grafo de conocimiento de la plataforma no introduce variación espuria en el registro. La clasificación coherente a lo largo del tiempo no es un efecto secundario de la disciplina; es una propiedad estructural impuesta por el libro contable de velocidades de actualización. Un auditor que consulte "qué ha clasificado esta empresa como Cumplimiento en los últimos tres años" recibe una respuesta significativa porque los límites de las categorías no se han desplazado bajo los datos.

## Véase también

- [[verification-surveyor]] — el agente con humano en el bucle que verifica fragmentos de identidad antes de que entren al libro mayor
- [[archetypes-and-chart-of-accounts]] — los dos libros contables de actualización más lenta que definen la identidad de la empresa
- [[message-courier]] — el sustrato de enrutamiento que entrega comunicaciones entrantes al libro mayor
- [[moonshot-initiatives]] — programa de ingeniería para reemplazar dependencias en cuarentena de las que depende la gobernanza ontológica
- [[worm-ledger-design]] — el sustrato de almacenamiento de solo adición que hace autoritativo el libro mayor verificado
