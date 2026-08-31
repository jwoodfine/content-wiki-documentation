---
schema: foundry-doc-v1
title: "tool-construction — libro contable de costo, cronograma y calidad para construcción"
slug: tool-construction
category: applications
type: tool
content_type: topic
quality: complete
index_group: financial-and-construction-tools
status: active
audience: vendor-public
bcsc_class: forward-looking
language_protocol: PROSE-TOPIC
last_edited: 2026-08-30
editor: pointsav-engineering
paired_with: tool-construction.md
short_description: "Un libro contable de archivos planos, bajo control del propietario, para el costo, cronograma y control de calidad de la construcción, sobre la misma disciplina de partida doble que tool-accounting; con el andamiaje compilando pero sin lógica de canalización aún."
cites: []
---

`tool-construction` es un libro contable de archivos planos, bajo control del propietario, para el costo, el cronograma y el control de calidad de la construcción, construido sobre la misma disciplina de partida doble que el motor contable hermano, [[tool-accounting]]. Está diseñado para servir a tres audiencias a la vez: una referencia de implementación para los desarrolladores que construyen la plataforma (incluidos aquellos sin experiencia en construcción), una visión técnica para evaluar el negocio que respalda el software, y un documento de decisión para un contratista o propietario que evalúa su adopción.

**Lo que existe hoy.** `tool-construction-core` y `tool-construction-pro-01` son miembros reales del workspace de Cargo que compilan sin errores, pero son andamiajes vacíos — aún no se ha escrito la lógica de canalización. Un sitio de construcción piloto real está registrado, con sus documentos de origen citados por hash, pero no existe ninguna entrada contable. El mecanismo del libro contable en sí está completamente diseñado, incluidas dos revisiones de diseño adversariales independientes, pero nada de ese diseño se ha implementado en código todavía.

---

## El problema que está diseñado para resolver

El control de costos de construcción divide un proyecto en un **código de costo** — una estructura numerada de desglose del trabajo que identifica un tipo de trabajo en un proyecto, como el concreto colado en sitio o el montaje de acero estructural. Cada costo se divide además por **tipo de costo** — mano de obra, materiales, equipo y subcontrato — porque los cuatro se comportan de manera lo suficientemente distinta como para que combinarlos destruya la información que un sobrecosto revelaría.

Bajo el código de costo se encuentra el **paquete de trabajo**: una pieza definida de trabajo físico que lleva dos números cuya relación es el fundamento del diseño — una **cantidad** (obtenida al medir los planos) y un **factor unitario** (las horas de mano de obra para instalar una unidad de esa cantidad). La cantidad establece el presupuesto de mano de obra; la cantidad efectivamente instalada más adelante consume ese presupuesto. Las horas trabajadas nunca consumen nada por sí solas — son lo que se mide contra ese consumo.

**Por qué importa:** invertir esta dirección es uno de los errores reales más comunes en el costeo de obras, y es precisamente la falla que este diseño busca prevenir de forma estructural, no por convención.

---

## Gestión del valor ganado y costeo por reflujo

El gasto y el avance no son lo mismo — un proyecto que ha gastado el 60% de su presupuesto puede estar 30% o 80% completo. El diseño utiliza **Gestión del Valor Ganado** (Earned Value Management), registrando el Valor Planificado, el Valor Ganado y el Costo Real como tres números en la misma unidad, de modo que la eficiencia de costos y el cumplimiento del cronograma se conviertan en indicadores anticipados en lugar de algo visible solo después del hecho. El diseño protege específicamente contra una falla conocida: si el valor ganado se derivara de las horas gastadas en lugar de la cantidad instalada observada de forma independiente, la medición compararía una cantidad consigo misma y nunca podría reportar un problema — por eso la cantidad instalada reportada de forma independiente se trata como obligatoria, no opcional.

El consumo de materiales está diseñado alrededor del **costeo por reflujo** (backflush costing): en lugar de rastrear cada movimiento físico de material en obra, el sistema está diseñado para registrar lo que se produjo y calcular hacia atrás lo que debió consumirse, usando un factor conocido, dejando solo la diferencia contra un conteo físico periódico para investigar. El diseño especifica que esto debe basarse en la cantidad instalada, nunca en las horas trabajadas — basarlo en horas permitiría que una cuadrilla lenta parezca haber consumido más material del que realmente contiene un muro, confundiendo una señal de mano de obra con una señal de materiales.

**Por qué importa:** ambos mecanismos están diseñados para convertir el reporte diario de campo en una alerta temprana sobre problemas de costo y cronograma, meses antes de que un estado financiero mostraría lo mismo.

---

## Diseño del libro contable

El diseño especifica dos libros contables separados, denominados deliberadamente de forma distinta. El **libro de producción** está diseñado para contener cantidades físicas — horas, metros cúbicos, toneladas. El **libro de costos** está diseñado para contener dólares, alimentado únicamente por asientos reales de nómina y cuentas por pagar, nunca por convertir las cantidades del libro de producción mediante una tarifa. La obligación de un subcontratista a suma alzada es una función del contrato y el porcentaje certificado como completo, no de las horas trabajadas por su propia cuadrilla — dos libros están diseñados para mantener ese caso honesto, en lugar de forzar una cifra de dólares inventada o una aproximación basada en horas.

Los dos libros están diseñados como proyecciones nombradas de un solo diario, no como libros separados — un enfoque con precedente en producción (el propio Material Ledger de SAP terminó integrándose en un único Universal Journal). Dentro de ese diario único, el diseño especifica que distintos tipos de cantidad — horas y metros cúbicos, por ejemplo — nunca se suman entre sí; un asiento que se contabiliza en más de una unidad está diseñado para verificarse unidad por unidad, exigiendo que cada lado de cada unidad cuadre de forma independiente.

**Por qué importa:** el diseño busca permitir que un evento real del mundo, como el trabajo reportado en un día, se contabilice correctamente en varias unidades distintas a la vez en un solo asiento atómico, sin forzar nunca cantidades incompatibles a un solo número.

---

## Retención, el período de gravamen y los plazos estatutarios

Los contratos de construcción están sujetos a retención estatutaria (holdback) — un porcentaje definido de cada pago certificado que el propietario retiene, liberado una vez que expira un período de gravamen (lien period) durante el cual los proveedores impagos pueden registrar un reclamo contra el edificio, sin que se registre ningún reclamo. El diseño contempla tres consecuencias que esto genera: la retención se aplica sobre una solicitud de pago certificada en su totalidad, no solo sobre el trabajo subcontratado; distintos tipos de trabajo llevan distintos períodos de gravamen, por lo que las partes del mismo proyecto quedan liberables en fechas diferentes; y los plazos estatutarios relevantes corren en días hábiles, no en días calendario, lo que convierte un calendario correcto de días hábiles en un requisito legal del software, no en una conveniencia de programación.

---

## Topología del producto y el límite entre lo gratuito y lo pagado

`tool-construction` está diseñado como un componente dentro de una familia más amplia: el propio libro contable de construcción; el motor contable hermano, [[tool-accounting]], diseñado para recibir de este una alimentación unidireccional de costo en dólares; `tool-typeset`, un renderizador de documentos sin dependencias compartido con el motor contable; y el motor propuesto de [[tool-payroll]], diseñado para recibir de este libro contable una alimentación unidireccional de horas y clase de mano de obra como tarjetas de tiempo.

El sustrato de archivo y la terminal de la plataforma son gratuitos (Apache-2.0); la agregación entre archivos es el límite pagado que aplica en toda la plataforma. `tool-construction` está diseñado como una segunda superficie comercial separada sobre ese límite — lo que se vendería es la ingeniería de dominio en sí (el esquema de puntuación de calidad, las matemáticas de valor ganado, el mecanismo del libro contable), no un margen sobre una infraestructura que ya es gratuita.

Las reglas de distribución de la plataforma clasifican los componentes `tool-*` como herramientas internas del operador que, por defecto, no se distribuyen como producto independiente, con excepciones otorgadas de forma individual — `tool-wallet` es el único precedente existente. **Actualmente no existe ninguna excepción de distribución registrada para `tool-construction`.**

## Licenciamiento

`tool-construction` está licenciado bajo FSL-1.1-ALv2.

---

## Qué no está construido todavía

Nada de lo descrito arriba como "diseñado" tiene lógica de canalización escrita. Específicamente aún no construido: el motor del libro contable en sí (asientos, materiales, mano de obra, equipo, subcontratos, órdenes de cambio, retención); el adaptador de almacenamiento de archivo que permitiría a un archivo de construcción persistir los datos del libro contable a través del propio almacén de registros de la plataforma; un archivo dedicado al dominio de construcción (ninguno ha sido aprovisionado); el mecanismo de transferencia de acceso en la transición de venta; y las dos pantallas de terminal propuestas (una vista de tabla del libro contable y un panel de paquete de trabajo/calidad), ninguna de las cuales ha recibido un espacio de compilación en la terminal fija de doce teclas de función de la plataforma.

Entre las preguntas de diseño abiertas que permanecen genuinamente sin resolver están dónde se ejecuta el motor en el caso de múltiples archivos, si la puntuación de desempeño individual pertenece dentro de este sistema o permanece como un asunto separado, si las certificaciones de calidad necesitan firma criptográfica dado su posible peso legal en un reclamo por defectos, y qué desencadena y autoriza la transferencia de acceso en la transición de venta descrita arriba, y cómo se relaciona con un proceso real de cierre legal.

## Véase también

- [[tool-accounting]] — el motor contable hermano que recibe de este libro contable una alimentación unidireccional de costo
- [[tool-payroll]] — el motor de nómina propuesto que recibe de este libro contable una alimentación unidireccional de tarjetas de tiempo
