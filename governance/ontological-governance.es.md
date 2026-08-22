---
schema: foundry-doc-v1
title: "Gobernanza ontológica"
slug: ontological-governance
short_description: "Cuatro libros contables de vocabulario de referencia mantenidos deliberadamente acotados, más un bucle de verificación humana que revisa los fragmentos de identidad extraídos antes de comprometerlos al libro contable verificado."
category: governance
type: topic
content_type: topic
quality: complete
index_group: platform-disciplines
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: ontological-governance.md
cites: []
---

Los sistemas de clasificación automatizada derivan con el tiempo: las categorías se amplían o contraen, el vocabulario se fragmenta y los errores se acumulan más rápido de lo que pueden corregirse. La **gobernanza ontológica** es la respuesta de esta plataforma: un pequeño conjunto de libros contables de vocabulario de referencia, mantenidos deliberadamente acotados, más un bucle de verificación humana que obliga a los fragmentos de identidad extraídos a pasar por revisión humana antes de que se escriban permanentemente en el libro contable verificado. Para un operador regulado, esto significa que los registros de identidad de la plataforma se mantienen precisos sin reclasificación automática continua.

## Los cuatro libros contables de vocabulario

[[service-content]] sirve cuatro libros contables CSV de referencia mediante un endpoint HTTP de configuración (`/v1/config/*`):

- **Arquetipos** — roles funcionales nombrados que una empresa puede ocupar (por ejemplo, "El Fiduciario", "El Guardián").
- **Plan de Cuentas** — la taxonomía de roles de personal de la empresa (por ejemplo, "Cumplimiento", "Soporte de TI").
- **Dominios** — glosarios bilingües que definen las tres macrocategorías temáticas de la plataforma: Corporativo (Finanzas), Proyectos (Bienes Raíces), Documentación (Tecnología).
- **Temas** — iniciativas activas nombradas (por ejemplo, "Expansión del Mandato de Co-ubicación").

Son vocabulario de referencia, no un clasificador automático — ningún código cruza el contenido entrante contra las palabras clave de los libros contables para asignar una categoría. El único consumidor confirmado es el [[verification-surveyor|Verificador de Identidad]], donde un operador etiqueta manualmente una entidad contra el vocabulario de Arquetipos/Plan de Cuentas durante la revisión humana. Mantener el vocabulario pequeño y revisado con poca frecuencia es una práctica editorial, no una propiedad limitada por código de los propios libros contables.

## El bucle de verificación humana

La gobernanza ontológica también abarca el [[verification-surveyor|Verificador de Identidad]], que fuerza los fragmentos de identidad extraídos a través de la revisión humana antes de que se escriban permanentemente en el [[worm-ledger-design|libro contable verificado]].

## Por qué importa un vocabulario estable para los operadores regulados

Un vocabulario pequeño y revisado con poca frecuencia produce una propiedad que importa en contextos regulados: la base del grafo de conocimiento permanece legible para auditoría. Un evaluador de adquisiciones o un revisor de cumplimiento que lea datos clasificados contra el vocabulario de Arquetipos y Plan de Cuentas con un año de diferencia encuentra los mismos nombres de categoría en uso — la taxonomía no se ha fragmentado bajo los datos.

## Véase también

- [[verification-surveyor]] — el agente con humano en el bucle que verifica fragmentos de identidad antes de que entren al libro mayor, y el único consumidor confirmado del vocabulario de Arquetipos/Plan de Cuentas
- [[archetypes-and-chart-of-accounts]] — los dos libros contables que definen la identidad de la empresa y la taxonomía de roles de personal
- [[worm-ledger-design]] — el almacenamiento de solo adición que hace autoritativo el libro mayor verificado
