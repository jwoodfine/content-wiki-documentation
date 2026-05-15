---
schema: foundry-doc-v1
title: "service-people — El Libro Mayor de Identidades"
slug: service-people
category: services
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: service-people.md
short_description: "service-people mantiene el libro mayor de identidades determinista del Totebox — la superficie F2 en os-console y la fuente de verdad sobre quién aparece en cualquier carga útil del Totebox, usando un modelo de datos Ancla-Reclamación-Enchufe que nunca sobrescribe el estado."
cites: []
references:
 - id: 1
 text: "Fowler, M. 'Event Sourcing.' martinfowler.com, 2005."
 url: "https://martinfowler.com/eaaDev/EventSourcing.html"
 - id: 2
 text: "Aho, A. V. & Corasick, M. J. 'Efficient String Matching: An Aid to Bibliographic Search.' Communications of the ACM, 18(6):333–340, 1975."
 url: "https://dl.acm.org/doi/10.1145/360825.360855"
---

`service-people` mantiene el libro mayor de identidades determinista del Totebox. Es la superficie F2 en `os-console` y la fuente de verdad sobre "quién" aparece en cualquier carga útil del Totebox. El modelo de datos se construye alrededor del patrón Ancla-Reclamación-Enchufe (ACS): la identidad nunca sobrescribe el estado, las reclamaciones se acumulan con el tiempo y el panorama actual de cualquier persona siempre puede recomputarse a partir del historial. Este artículo cubre el modelo de datos de tres entidades, el patrón ACS y la Red Infinita — el mecanismo mediante el cual las identidades entran al libro mayor desde cargas útiles en bruto sin intervención del operador.

## El modelo de datos de tres entidades

`service-people` organiza la identidad en tres tipos de entidades distintos:

| Entidad | Rol | Regla de almacenamiento |
|---|---|---|
| Objetivo (el Ancla) | Una persona u organización única, anclada por un identificador de alta fidelidad (hash de correo, hash de teléfono, URN de red profesional) | Mínimo — solo un Sovereign-ID estable y el ancla; los campos volátiles (cargo, empleador) no se almacenan aquí |
| Reclamación (la Observación) | Cada dato asociado a un Objetivo: `UUID_Objetivo | Atributo | Valor | Fuente | Marca_Tiempo` | Solo adición — las reclamaciones se acumulan con el tiempo; ninguna reclamación se elimina jamás |
| Enchufe Semántico (el Puente) | Una etiqueta de clasificación que mapea el Objetivo a una fila del Plan de Cuentas | Recomputado de forma determinista a partir de las reclamaciones más las anulaciones del operador |

Si el rol de un contacto de correo aparece listado de forma diferente en dos fuentes, ambas reclamaciones existen en el Totebox. La capa de consulta (`service-content` y `service-slm`) decide qué reclamación es la actual en el momento de la consulta. Esto previene la sobrescritura de datos y preserva la evolución completa de cada identidad.

## El modelo Ancla-Reclamación-Enchufe

El diseño de tres entidades, abreviado ACS, es el event sourcing aplicado a la identidad: nunca sobrescribir el estado; siempre añadir observaciones; recomputar el presente a partir del historial. [^1]

| Propiedad | Por qué importa |
|---|---|
| Las reclamaciones son inmutables | El registro de auditoría captura el historial completo de cómo el sistema llegó a conocer un hecho |
| Los enchufes son reproducibles | Cualquier enchufe del Plan de Cuentas puede regenerarse reproduciendo las reclamaciones |
| Los objetivos son estables | El Sovereign-ID nunca cambia; los atributos volátiles nunca provocan un rekeying |

## La Red Infinita

La identidad no entra en `service-people` solo mediante la entrada manual del operador. `service-extraction` ejecuta Aho-Corasick sobre cada carga útil entrante — cuerpo de correo, texto PDF, texto DOCX — y extrae cada nombre, dirección de correo, número de teléfono y organización que encuentra. [^2] Cada entidad extraída recibe un Sovereign-ID y entra al libro mayor en estado `Discovery`.

Con el tiempo, `service-slm` cruza las entidades descubiertas con los Vectores de Gravedad producidos por `service-content`. Si una entidad acumula gravedad — apareciendo en cargas útiles alineadas con Dominios, Arquetipos y Temas — se enchufa a una fila del Plan de Cuentas y se eleva a estado activo. Si nunca acumula gravedad (el remitente de un boletín promocional; una firma de un solo uso), sale del índice activo después de 30 días, permaneciendo en el registro WORM pero invisible para la búsqueda activa.

## El sustrato de archivos planos

El libro mayor es un directorio de archivos planos JSON en lugar de una base de datos relacional — portátil entre cambios de infraestructura, auditable con herramientas estándar del sistema de archivos y nativamente compatible con pipelines de entrenamiento de modelos locales que necesitan un esquema estable. No se requiere migración de base de datos cuando se añaden campos; los registros existentes permanecen válidos a medida que el esquema evoluciona.

## Véase también

- [[service-email]] — el servicio de ingesta de correo que alimenta registros del remitente a service-people a través de service-extraction
- [[service-content]] — el Motor de Gravedad que produce los Vectores de Gravedad que service-slm usa para enchufar entidades
- [[archetypes-and-chart-of-accounts]] — el Plan de Cuentas al que se mapean los Enchufes Semánticos
- [[totebox-os]] — el Totebox que aloja service-people y su almacenamiento WORM
