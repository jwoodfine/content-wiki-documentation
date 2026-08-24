---
schema: foundry-doc-v1
title: "Sustrato de citas"
slug: citation-substrate
lang: es
paired_with: citation-substrate.md
category: substrate
type: topic
content_type: topic
quality: complete
index_group: core-named-substrates
short_description: "Registro YAML de citas de ámbito de plataforma con detección de deriva que hace la procedencia auditable por máquina, del instrumento regulatorio a la afirmación publicada."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-24
editor: pointsav-engineering
cites:
 - ni-51-102
 - np-51-201
 - cff-spec
---

Cada artículo de esta documentación que realiza una afirmación basada en autoridades externas incluye una declaración `cites:` en su encabezado YAML con los instrumentos regulatorios, artículos académicos o especificaciones técnicas de los que depende. Esos identificadores se resuelven contra un registro YAML único de ámbito de plataforma. El resultado es un grafo de procedencia, no una bibliografía: una estructura que recorre desde una afirmación publicada hasta su fuente primaria, recorrible por una máquina o un revisor sin acceso a sistemas internos.

El registro contiene 159 entradas que cubren instrumentos regulatorios (NI 51-102, Regla SEC 17a-4(f), eIDAS), artículos académicos, especificaciones técnicas, documentos de proveedores y estándares abiertos. Cada referencia `[ni-51-102]` en un artículo publicado apunta a la misma entrada canónica del registro, con tipo, jurisdicción, URL estable y hash SHA-256 del contenido para detección de deriva.

Tres componentes trabajan en conjunto: un registro central con una entrada por identificador de cita; campos `cites:` en el encabezado por documento que hacen las dependencias legibles por máquina; y sintaxis `[id]` en línea en el cuerpo del texto que marca cada referencia con su identificador resoluble en el registro. Un proceso nocturno automatizado descarga cada URL registrada, verifica el hash del contenido y presenta cambios materiales o enlaces rotos para revisión humana antes de que se propaguen al contenido publicado.

Para compradores regulados, esto significa que cada afirmación sobre propiedades de cumplimiento — inmutabilidad de registros, pistas de auditoría de IA, residencia de datos — lleva una base declarada rastreable. Un responsable de cumplimiento que audite documentación sobre la Regla SEC 17a-4(f) puede seguir la cita hasta el instrumento regulatorio primario sin acceder a sistemas internos. Esto satisface el requisito de "base declarada" bajo `[ni-51-102]` y `[np-51-201]` para información prospectiva en [[disclosure-substrate|contenido público]].

## Componentes

**El registro** (`citations.yaml`). Un archivo YAML en formato CFF `[cff-spec]` con una entrada por identificador de cita. Cada entrada incluye el tipo, la jurisdicción (para instrumentos regulatorios), el título oficial, la URL estable, la fecha de última verificación, un hash de contenido para detectar cambios, la clase de evidencia, y los alias que puedan aparecer en prosa. El registro contiene 159 entradas.

**El encabezado por documento**. Un campo `cites:` en el YAML de cada artículo publicado y documento de especificación. Los identificadores declarados se resuelven contra el registro; las herramientas pueden validar que existan, generar automáticamente una sección de referencias, y construir un índice inverso de quién cita a quién.

**La sintaxis de referencia en línea**. En el cuerpo del texto, una cita aparece entre corchetes: `[ni-51-102]`. Las referencias a secciones específicas añaden la referencia: `[ni-51-102 §4A.2]`.

## Anillo y función

El Sustrato de Citas no tiene asignación de anillo — opera en la capa de documentación,
independiente de los tres anillos de servicio de la plataforma. Todo documento publicado
que haga una afirmación basada en autoridades externas debe llevar el `cites:`
correspondiente. El ciclo nocturno de higiene que vigila la salud del registro se
ejecuta como un trabajo de [[service-slm]] (Anillo 3); el registro en sí es un archivo
de la capa de documentación.

## Cómo funciona el registro

El esquema de cada entrada del registro hace explícita la procedencia en cada paso. Una
cita regulatoria como `[ni-51-102]` lleva `evidence_class: regulatory-primary` — una
señal filtrable por máquina que indica que esa entrada es autoridad primaria, no
comentario secundario. Un artículo académico lleva `evidence_class: technical-primary`
o `research-derived`, según sea una contribución original o una síntesis. Un documento
de proveedor lleva `evidence_class: cited-secondary`.

El campo `content_hash` es el mecanismo de autocuración. Cuando [[service-slm]] ejecuta
su ciclo nocturno de higiene, descarga cada URL, calcula un SHA-256 del contenido de la
página y lo compara con el hash almacenado. Una coincidencia actualiza la fecha
`last_verified`. Una discrepancia se marca como candidata a cambio material y se
presenta para revisión humana junto con el diff. Un error 404 se marca como enlace roto,
junto con resultados de búsqueda de posibles reemplazos.

La revisión nocturna automatizada aún no está construida; hasta que llegue, el mantenedor de la plataforma realiza una revisión manual mensual del registro.

Agregar una nueva cita sigue el principio de siembra: la entrada del registro y la
referencia en línea llegan en el mismo commit. Una referencia en línea huérfana — cuyo
identificador no se resuelve en el registro — es un defecto.

## Por qué importa esta disciplina

**Rastreabilidad regulatoria.** Conforme a `[ni-51-102]` y `[np-51-201]`, la información prospectiva en contenido público debe incluir lenguaje de precaución y una base declarada. El grafo de citas hace que esa base sea auditable por máquina: un revisor puede recorrer desde una afirmación pública hasta el instrumento regulatorio o artículo académico que la fundamenta.

**Prevención de divergencia.** Un corpus que crece a lo largo de sesiones, colaboradores y años puede producir documentos que citan la misma autoridad pero hacen afirmaciones contradictorias. El proceso de detección de divergencias del ciclo nocturno de higiene identifica exactamente estos pares y los presenta para revisión antes de que se propaguen al contenido publicado o a los datos de entrenamiento.

**Compuesto de conocimiento público.** Los repositorios de contenido wiki son la parte pública del [[compounding-substrate|Sustrato Compuesto]]. Las citas viajan con el contenido hacia cualquier exportación, espejo o corpus derivado, de acuerdo con el [[knowledge-commons|modelo de publicación en los comunes]]. Un lector o un consumidor de máquina puede seguir la cita hasta la fuente primaria sin necesidad de confiar en las afirmaciones propias de la plataforma.

## Estado y planificación

El sistema de citas actualmente requiere disciplina manual: la entrada del registro y la referencia en línea llegan en el mismo commit; el mantenedor de la plataforma revisa el registro mensualmente. Por `[ni-51-102]`, los siguientes elementos son infraestructura planificada:

- Un gancho post-commit que valida que cada nueva referencia `[id]` se resuelva en el registro.
- Generación automática de una sección de referencias al final de cada artículo, conectada a `app-mediakit-knowledge` como etapa del renderizador.
- Un índice inverso `cited_by:` reconstruido bajo demanda por el servicio [[service-slm]].
- Ciclos nocturnos de higiene cubriendo verificación de citas, detección de deriva, indexación inversa y sugerencias de citas — todo como sugerencias al mantenedor, no como correcciones automatizadas (ver [[nightly-datagraph-rebuild]]).

## Véase también

- [[compounding-substrate]]
- [[language-protocol-substrate]]
- [[disclosure-substrate]]
