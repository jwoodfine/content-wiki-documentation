---
schema: foundry-doc-v1
title: "El Sustrato de Citas"
slug: citation-substrate.es
lang: es
paired_with: citation-substrate.md
category: architecture
status: pre-build
last_edited: 2026-04-28
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
  - cff-spec
---

Cada cláusula doctrinal, convención y documento público del
espacio de trabajo Foundry declara sus dependencias de citas en
el encabezado YAML del archivo. Esos identificadores se resuelven
contra un registro central en `~/Foundry/citations.yaml`. El
resultado es un grafo de procedencia legible por máquina — no
solo una bibliografía — que conecta un instrumento regulatorio
con una cláusula doctrinal y con un artículo publicado, auditable
en cada paso.

## Qué es el Sustrato de Citas

El Sustrato de Citas es el mecanismo que une cada artefacto escrito
con las autoridades externas de las que depende. Tres componentes
trabajan en conjunto:

- **El registro** — un archivo YAML en formato CFF que contiene
  una entrada por identificador de cita. Cada entrada incluye el
  tipo, la jurisdicción (para instrumentos regulatorios), el título
  oficial, la URL estable, la fecha de la última verificación, un
  hash de contenido para detectar cambios, y la clase de evidencia.
  Al 27 de abril de 2026, el registro contiene 62 entradas.

- **El encabezado de cada documento** — un campo `cites:` en el
  YAML de cada cláusula doctrinal, convención y artículo. Los
  identificadores declarados se resuelven contra el registro;
  las herramientas pueden validar que existan, generar
  automáticamente una sección de referencias, y construir un
  índice inverso de quién cita a quién.

- **La sintaxis de referencia en línea** — en el cuerpo del
  texto, una cita aparece entre corchetes: `[ni-51-102]`. Las
  referencias a cláusulas específicas añaden la sección:
  `[ni-51-102 §4A.2]`.

## Por qué importa esta disciplina

La disciplina responde a tres necesidades concretas.

**Rastreabilidad regulatoria.** Conforme a `[ni-51-102]` y
`[osc-sn-51-721]`, la información prospectiva en contenido público
debe incluir lenguaje de precaución y una base declarada. El grafo
de citas hace que esa "base declarada" sea auditable por máquina:
un revisor puede recorrer desde una afirmación pública hasta la
cláusula doctrinal que la sostiene y hasta el instrumento
regulatorio o artículo académico que la fundamenta.

**Prevención de divergencia.** Un corpus que crece a lo largo de
sesiones, colaboradores y años puede producir documentos que citan
la misma autoridad pero hacen afirmaciones contradictorias. El
paso de detección de divergencias del ciclo nocturno de higiene
del SLM identifica exactamente estos pares y los presenta como
elementos de revisión, antes de que se propaguen a datos de
entrenamiento o a publicaciones.

**Compounding público.** Los repositorios de contenido wiki son
la parte pública del Sustrato Compuesto. Las citas viajan con el
contenido hacia cualquier exportación, espejo o corpus derivado.
Un lector o un consumidor de máquina no necesita confiar en las
afirmaciones propias de la plataforma — puede seguir la cita
hasta la fuente primaria.

## Lo que está previsto

El mecanismo completo — verificación automática de hashes de
contenido, generación de índice inverso, detección de divergencias
y sugerencias de citas — está previsto con la entrada en
funcionamiento de service-SLM. Hasta entonces, la disciplina
operativa es manual: la entrada del registro y la referencia en
línea llegan en el mismo commit; Master Claude revisa el registro
mensualmente.

## Véase también

- [El Sustrato Compuesto](topic-compounding-substrate.es.md)
- [El Sustrato del Protocolo de Lenguaje](topic-language-protocol-substrate.es.md)
- Convención de referencia: `~/Foundry/conventions/citation-substrate.md`
- Registro: `~/Foundry/citations.yaml`
