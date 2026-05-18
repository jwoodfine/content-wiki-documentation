---
schema: foundry-doc-v1
title: "Filosofía Editorial"
slug: editorial-philosophy
short_description: "Cada artículo es un recurso de aprendizaje que enseña comprensión en lugar de recuperar hechos, estructurado con párrafos de apertura enciclopédicos, vinculación interna y jerarquía de encabezados consistente adecuada tanto para lectores humanos como para máquinas."
category: reference
status: stable
bcsc_class: no-disclosure-implication
last_edited: 2026-05-08
editor: pointsav-engineering
language: es
paired_with: editorial-philosophy.md
---

Cada artículo de los wikis de PointSav es un recurso de aprendizaje, no una consulta de referencia. Un lector que termina un artículo debe comprender el tema, no solo haber recuperado un dato. Wikipedia es el modelo: estructurado, enlazado internamente, con la profundidad necesaria para construir comprensión genuina, y lo suficientemente consistente para que un lector que conoce Wikipedia reconozca el diseño de inmediato y sepa cómo navegar en él.

## El modelo Wikipedia

Wikipedia logra algo que la mayoría de la documentación no consigue: enseña. Un lector que llega buscando "estructura de propiedad de tenencia directa" o "service-slm" o "mandato de co-ubicación" se va con un modelo mental, no solo con una definición. Esto ocurre porque los artículos de Wikipedia se construyen en torno a la comprensión, no a la recuperación.

Tres decisiones estructurales producen este resultado:

**1. El párrafo inicial enciclopédico.** El primer párrafo contiene los hechos más importantes sobre el tema — en lenguaje llano, al nivel de abstracción adecuado para un lector general. No asume conocimiento previo. No comienza con una definición. Comienza con la consecuencia: por qué importa este tema, qué hace, qué gana el lector al comprenderlo.

**2. Enlazado interno que construye redes de comprensión.** Los artículos se enlazan entre sí mediante wikilinks `[[slug]]`. Un lector que sigue los enlaces construye progresivamente un conocimiento más profundo. Los enlaces rojos — enlaces a artículos que aún no existen — son características, no defectos. Muestran al lector dónde la enciclopedia está incompleta e invitan a contribuir.

**3. Estructura consistente.** Párrafo inicial → secciones del cuerpo → Véase también → Referencias. Esta estructura es la memoria muscular de Wikipedia. Un lector que la ha usado durante diez minutos la reconoce. El reconocimiento es en sí mismo una forma de confianza.

## La prueba enciclopédica

Cada artículo debe superar una prueba:

*¿Un lector que termina este artículo comprende el tema, o solo ha encontrado un dato?*

Un artículo de recuperación de datos responde "¿qué es X?". Un artículo enciclopédico responde "¿qué es X, por qué importa, cómo funciona y cómo se conecta con Y y Z?". El segundo artículo es un recurso de aprendizaje. El primero es una entrada de glosario.

## Contenido enriquecido por el DataGraph

Los wikis de PointSav están conectados a una base de datos de grafos de propiedades — el DataGraph — que acumula conocimiento sobre cada entidad de la plataforma: a qué se conecta cada entidad, a qué dominio pertenece, qué temas la atraviesan y qué dice el corpus de investigación sobre ella.

Una reescritura informada por el DataGraph añade ese conocimiento al artículo con dos entradas distintas:

| Entrada | Fuente | Lo que aporta |
|---|---|---|
| **Cómo escribir** | Corpus de investigación → tokens de lenguaje | Registro, estructura de oración, vocabulario, párrafo inicial con consecuencia primero |
| **Qué decir** | DataGraph — entidades, relaciones, dominios, temas | Contenido que el artículo fue escrito antes de que el DataGraph existiera para proporcionar |

Los tokens de lenguaje rigen el registro. El DataGraph rige el contenido. Un artículo con registro correcto pero contenido escaso no supera la prueba enciclopédica. Un artículo con contenido rico pero registro incorrecto no comunica. Ambas entradas son necesarias.

## El ciclo mensual de mejora

Los wikis de PointSav mejoran continuamente mediante una revisión mensual del contenido. Cada revisión se ejecuta contra un DataGraph actualizado — refinado por pasadas de inferencia de GPU bajo demanda que se ejecutan diariamente y pasadas de API externa que se ejecutan semanal o mensualmente a medida que se acumulan nuevos datos fuente.

El objetivo de cada artículo en cualquier revisión es "borrador 2 de 10" — suficientemente bueno para que la siguiente pasada automática produzca un borrador 3 claramente mejor. La perfección en un único pase desperdicia esfuerzo que sería mejor dedicar a establecer el marco que hace que cada pase posterior sea mejor.

## Véase también

- [[editorial-language-registers]] — los tres registros y las reglas de vocabulario que rigen cómo se escribe cada wiki
- [[style-guide-topic]] — estructura de artículos y convenciones del patrón Wikipedia
- [[style-guide-guide]] — estructura de guías operacionales
- [[glossary-documentation]] — definiciones canónicas de términos
