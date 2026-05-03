---
schema: foundry-doc-v1
title: "El Patrón de Salto de Rana de Wikipedia"
slug: wikipedia-leapfrog-pattern.es
category: reference
type: topic
quality: published
short_description: Nueve patrones estructurales de Wikipedia y sus equivalentes aplicados por el sustrato — la transformación que reemplaza las normas editoriales voluntarias con aplicación en tiempo de generación, en tiempo de commit y en el bucle de entrenamiento.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: wikipedia-leapfrog-pattern.md
---

La autoridad editorial de Wikipedia descansa en veinte años de convenciones estructurales acumuladas: anatomía de artículos, notas de desambiguación, densidad de notas al pie, primitivas de navegación, plantillas de cuadros informativos, deliberación en páginas de discusión, grados de calidad, escritura en estilo de resumen y contribución atribuida. Estas convenciones se aplican mediante normas sociales voluntarias, patrullaje de bots, revisión editorial y gobernanza comunitaria. Son poderosas porque han sido iteradas durante décadas; también son frágiles porque su aplicación depende de atención voluntaria sostenida que es desigual en todo el corpus.

El wiki de documentación de PointSav toma su memoria muscular estructural de Wikipedia mientras reemplaza la aplicación voluntaria con aplicación por sustrato. Donde Wikipedia depende de la convergencia editorial a lo largo de meses, el sustrato de PointSav aplica estructuras equivalentes en el momento de la generación, en el momento del commit y a través de un bucle de entrenamiento continuo. Este artículo mapea nueve patrones estructurales de Wikipedia a sus equivalentes de sustrato e identifica la transformación de salto de rana que habilita cada uno.

## Los nueve saltos de rana

**Anatomía del artículo.** Wikipedia aplica la estructura de pirámide invertida a través de normas sociales voluntarias durante meses. El sustrato la aplica en tiempo de generación mediante plantillas de género por tipo de artículo.

**Desambiguación.** Wikipedia depende de la convergencia editorial para la consistencia terminológica. La consistencia de términos es una propiedad del sustrato aplicada en tiempo de generación mediante la gramática de vocabulario prohibido.

**Densidad de notas al pie.** La calidad de las citas en Wikipedia depende de la atención voluntaria. El sustrato solo puede referenciar entradas que existen en el registro verificado, y la resolución ocurre en cada borrador en tiempo de refinamiento.

**Navegación.** La navegación en Wikipedia requiere curación por artículo y gestión de redirecciones asistida por bots. El wiki de PointSav deriva la navegación de metadatos de front-matter legibles por máquina; la mayoría de los artefactos de navegación se calculan en lugar de ser creados por autores.

**Plantillas de tipo de artículo.** Las plantillas de cuadros informativos de Wikipedia se seleccionan y completan manualmente. La enumeración cerrada de tipos de artículos impulsa la selección de plantillas automáticamente en tiempo de refinamiento.

**Deliberación en páginas de discusión.** Las páginas de discusión de Wikipedia son no estructuradas, no consultables y no alimentan ningún modelo. El rastro de auditoría de PointSav es estructurado, firmado criptográficamente y alimenta el entrenamiento continuo.

**Grados de calidad.** Los grados de calidad de Wikipedia dependen de la nominación voluntaria. El estado de los artículos de PointSav es actualizado por criterios aplicados por el sustrato.

**Escritura en estilo de resumen.** La sincronización de resúmenes en Wikipedia es manual y periódica. La alineación de las páginas de contenido del mapa de categoría es una propiedad de la tubería, no un problema de programación.

**Atribución.** La atribución en Wikipedia es anónima abierta. La atribución en PointSav es estratificada por nivel, firmada criptográficamente y simultáneamente un registro de proveniencia de señal de entrenamiento.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Con licencia [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*
