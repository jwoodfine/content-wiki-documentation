---
schema: foundry-doc-v1
title: "Búsqueda de texto completo"
slug: service-search
short_description: "service-search es un servicio de búsqueda de texto completo Ring 2 diseñado pero no construido — un README describe un índice invertido basado en Tantivy, pero aún no existe código fuente."
category: services
type: topic
content_type: topic
quality: complete
index_group: ring-2-knowledge-and-processing
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: service-search.md
cites: []
references:
  - id: 1
    text: "Tantivy. 'Tantivy — A Full-Text Search Engine Library in Rust.' docs.rs, 2024."
    url: "https://docs.rs/tantivy/"
---

`service-search` es un diseño, aún no una implementación. Su directorio en el monorepo solo
contiene un README que describe el servicio previsto — un índice de texto completo estático
y mapeado en memoria, construido con la biblioteca Rust Tantivy de
[[three-ring-architecture|Ring 2]] — y ningún código fuente. El objetivo de diseño, según lo
registrado, es una recuperación que responda consultas de texto completo en los documentos
de la plataforma sin un proceso de base de datos activo. El índice es un archivo, por lo que
puede copiarse y consultarse en cualquier máquina sin servidor que ejecutar.

## El diseño previsto

Un índice invertido mapea cada palabra de un corpus a los documentos que la contienen, el
mismo principio que el índice al final de un libro de referencia. Tantivy está construido
para indexación de alto rendimiento y búsqueda de baja latencia en hardware convencional.
[^1] El diseño registrado llama a que el índice se ubique en el Ring 2 de la arquitectura
por niveles de la plataforma — multi-inquilino, determinista, sin inferencia de IA en la
ruta de recuperación. Respondería consultas con referencias a documentos clasificados por
relevancia que otros servicios consumen para procesamiento posterior. No generaría ni
clasificaría contenido, solo lo localizaría.

## Lo que existe hoy

Nada más allá de la descripción. No hay configuración de compilación, ni directorio de
código fuente, ni servicio en ejecución. Nada en la plataforma depende actualmente de
`service-search` para recuperación; otros servicios realizan directamente cualquier
búsqueda de texto completo que necesitan.

## Véase también

- [[service-extraction]] — un servicio Ring 2 que alimentaría salida analizada a este índice si se construyera
- [[service-slm]] — la capa de inteligencia Ring 3 que consumiría los resultados de recuperación clasificados
- [[service-people]] — un libro de identidades cuyos registros formarían parte de un futuro corpus consultable
