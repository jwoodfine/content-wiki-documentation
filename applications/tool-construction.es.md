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
last_edited: 2026-09-03
editor: pointsav-engineering
paired_with: tool-construction.md
short_description: "Libro contable de archivos planos, bajo control del propietario, para costo, cronograma y control de calidad de construcción, sobre la misma disciplina de partida doble que tool-accounting; el motor central ya funciona como CLI real y contabiliza los estimados de un piloto en vivo por las cuatro cadenas de tipo de costo — solo etapa de estimación, sin consola todavía."
cites: []
---

`tool-construction` es un libro contable de archivos planos, bajo control del propietario, para el costo, el cronograma y el control de calidad de la construcción, construido sobre la misma disciplina de partida doble que el motor contable hermano, [[tool-accounting]]. Está diseñado para servir a tres audiencias a la vez: una referencia de implementación para los desarrolladores que construyen la plataforma (incluidos aquellos sin experiencia en construcción), una visión técnica para evaluar el negocio que respalda el software, y un documento de decisión para un contratista o propietario que evalúa su adopción.

**Lo que existe hoy.** El motor es real y está en funcionamiento. `tool-construction-core` implementa por completo el libro contable del lado de cantidades — asientos de diario con valor vectorial, unidades no fungibles y las cuatro cadenas de tipo de costo (mano de obra, materiales, equipo y subcontrato) — verificado con pruebas de valores de referencia que reproducen, número por número, los ejemplos resueltos de la propia arquitectura. Un crate binario piloto lo opera como una cadena de herramientas de línea de comandos con cinco binarios, que construyen un estimado de costos de abajo hacia arriba a partir de paquetes de trabajo, computan un cronograma de ruta crítica, contabilizan el estimado en el libro y generan reportes en HTML y PDF. Todo esto corre contra un piloto real: un proyecto de desarrollo en vivo cuyos paquetes de trabajo están contabilizados como bloqueos presupuestarios reales, con cero fallas en las identidades de balance de comprobación. Dos límites son igual de reales. La cadena de herramientas es exclusivamente CLI — no existe ninguna superficie de terminal o consola, y ninguna tiene asignado un espacio de compilación. Y opera solo en etapa de estimación: el libro contiene estimados y presupuestos reales, no datos efectivos, porque ninguna factura, pago o registro de nómina ha entrado todavía a la canalización.

---

## El problema que resuelve

El control de costos de construcción divide un proyecto en un **código de costo** — una estructura numerada de desglose del trabajo que identifica un tipo de trabajo en un proyecto, como el concreto colado en sitio o el montaje de acero estructural. Cada costo se divide además por **tipo de costo** — mano de obra, materiales, equipo y subcontrato — porque los cuatro se comportan de manera lo suficientemente distinta como para que combinarlos destruya la información que un sobrecosto revelaría.

Bajo el código de costo se encuentra el **paquete de trabajo**: una pieza definida de trabajo físico que lleva dos números cuya relación es el fundamento del diseño — una **cantidad** (obtenida al medir los planos) y un **factor unitario** (las horas de mano de obra para instalar una unidad de esa cantidad). La cantidad establece el presupuesto de mano de obra; la cantidad efectivamente instalada más adelante consume ese presupuesto. Las horas trabajadas nunca consumen nada por sí solas — son aquello contra lo que se mide el consumo.

**Por qué importa:** invertir esta dirección es uno de los errores reales más comunes en el costeo de obras, y es precisamente la falla que el motor previene de forma estructural, no por convención.

---

## Gestión del valor ganado y costeo por reflujo

El gasto y el avance no son lo mismo — un proyecto que ha gastado el 60% de su presupuesto puede estar 30% o 80% completo. El motor utiliza la **Gestión del Valor Ganado** (Earned Value Management), registrando el Valor Planificado, el Valor Ganado y el Costo Real como tres números en la misma unidad, de modo que la eficiencia de costos y el cumplimiento del cronograma se convierten en indicadores anticipados en lugar de algo visible solo después del hecho. El diseño protege específicamente contra una falla conocida: si el valor ganado se derivara de las horas gastadas en lugar de la cantidad instalada observada de forma independiente, la medición compararía una cantidad consigo misma y nunca podría reportar un problema — por eso la cantidad instalada reportada de forma independiente se trata como obligatoria, no opcional. Las identidades del valor ganado se exigen como pruebas unitarias de balance de comprobación sobre el propio pliegue del libro contable, no mediante una fórmula separada que pudiera desviarse de los asientos.

El consumo de materiales se construye alrededor del **costeo por reflujo** (backflush costing): en lugar de rastrear cada movimiento físico de material en obra, el sistema registra lo que se produjo y calcula hacia atrás lo que debió consumirse, usando un factor conocido, dejando solo la diferencia contra un conteo físico periódico para investigar. Esto se basa en la cantidad instalada, nunca en las horas trabajadas — basarlo en horas permitiría que una cuadrilla lenta parezca haber consumido más material del que realmente contiene un muro, confundiendo una señal de mano de obra con una señal de materiales.

**Por qué importa:** ambos mecanismos convierten el reporte diario de campo en una alerta temprana sobre problemas de costo y cronograma, meses antes de que un estado financiero mostraría lo mismo. En el piloto actual, esta maquinaria está construida y probada pero aún sin alimentar: no existe todavía una fuente independiente de cantidad instalada para el proyecto, así que las columnas de valor ganado no reportan nada en lugar de una conjetura derivada — véase la regla de reporte más abajo.

---

## Un solo diario, dos proyecciones

El motor mantiene dos libros contables, denominados deliberadamente de forma distinta. El **libro de producción** contiene cantidades físicas — horas, metros cúbicos, toneladas, fracciones de un calendario de valores. El **libro de costos** está diseñado para contener dólares, alimentado únicamente por asientos reales de nómina y cuentas por pagar, nunca por convertir las cantidades del libro de producción mediante una tarifa. La obligación de un subcontratista a suma alzada es una función del contrato y del porcentaje certificado como completo, no de las horas trabajadas por su propia cuadrilla — dos libros mantienen ese caso honesto, en lugar de forzar una cifra inventada en dólares o una aproximación basada en horas. El libro del lado de cantidades está implementado por completo; el libro del lado de dólares se difiere deliberadamente hasta que existan datos reales de cuentas por pagar y nómina que lo alimenten, en lugar de construirse contra cifras inventadas.

Los dos libros son proyecciones nombradas de un solo diario, no libros separados — un enfoque con precedente en producción (el propio Material Ledger de SAP terminó integrándose en un único Universal Journal). Dentro de ese diario único, distintos tipos de cantidad nunca se suman entre sí. El tipo de unidad convierte esto en una garantía verificada en compilación y en ejecución, no en una convención:

```rust
pub enum Unit {
    Labour(LabourClass),
    Material(MaterialSpec),
    Equipment(EquipmentSpec),
    Contract(ContractUnit),
}
```

Un asiento de diario tiene valor vectorial — un solo evento del mundo real, como el trabajo reportado en un día, se contabiliza en varias unidades a la vez en un único asiento atómico — y la verificación de cuadre corre componente por componente, exigiendo que los débitos y créditos de cada unidad cuadren de forma independiente. Sumar entre unidades se rechaza, no se desaconseja. El estado del libro nunca se almacena como un total acumulado: cada ejecución pliega el diario completo desde cero hacia los saldos de cuenta, de modo que las identidades del balance de comprobación se vuelven a demostrar desde los primeros asientos en cada corrida.

**Por qué importa:** el libro no puede mezclar silenciosamente horas con metros cúbicos, ni ninguna de las dos cosas con dólares, y cualquier corrupción del estado fallaría de forma ruidosa en el siguiente pliegue en lugar de acumularse en silencio.

---

## Las cuatro cadenas de tipo de costo

Cada tipo de costo lleva su propia cadena de cuentas y sus propias reglas de contabilización, porque cada uno falla de manera distinta. Las cadenas de mano de obra y materiales implementan la mecánica de bloqueo presupuestario y consumo descrita arriba, incluida la precondición de disparo que le da fuerza al libro: las cuentas presupuestarias rechazan de forma dura un consumo excedido hasta que una orden de cambio vuelve a comprometer fondos, mientras que las cuentas de almacén generan el asiento y lo marcan en lugar de bloquearlo — la distinción entre "este asiento sobregiraría una autorización" y "este asiento revela una variación que vale la pena investigar."

La cadena de **equipo** añade una dimensión de estado operativo a cada asiento — operado, ocioso, en espera, en transporte — siguiendo la práctica establecida del costeo de obra en la industria, no una taxonomía inventada. La pérdida por utilización y la variación de productividad se computan entonces como filtros puros sobre el mismo pliegue del libro, nunca como una fórmula derivada por separado, de modo que los dos componentes quedan estructuralmente garantizados a sumar con exactitud el residual de la cadena, sin necesitar una verificación de conciliación.

La cadena de **subcontratos** modela una línea del calendario de valores como una unidad de fracción de suma alzada y lleva la mecánica de certificación y retención a través del libro. También exige la única regla genuinamente distinta de todas las demás cadenas: el residual del subcontrato debe cerrar en **exactamente cero**. Mientras que la variación de cualquier otra cadena es un número computado que hay que explicar, el cierre de un subcontrato se rechaza ante cualquier residual distinto de cero hasta que se contabilice una cancelación explícitamente autorizada.

**Por qué importa:** una certificación de subcontrato reclamada en exceso, una máquina ociosa facturada como productiva, o trabajo que continúa más allá de un presupuesto de orden de cambio agotado, afloran como un asiento rechazado o marcado en el momento del registro — no como una anomalía que alguien podría notar en un reporte semanas después.

---

## De quién es el libro

Un libro de costos de obra solo tiene sentido desde un asiento en la mesa: la parte que realmente ejecuta el trabajo es la única que puede observar las horas de mano de obra, el consumo de materiales y los hechos de certificación. El motor lo hace explícito con un conjunto pequeño de roles de parte — ejecutor, propietario contratante, certificador, subcontratista, proveedor — con exactamente un ejecutor por despliegue, cuyos libros son los del sistema. La identidad de la parte se adjunta a un asiento solo cuando el significado del asiento depende genuinamente de quién lo afirmó (la cadena de certificación de subcontratos); los asientos de mano de obra, materiales y equipo son hechos sobre el trabajo, no sobre una relación, y no llevan parte alguna. Una prueba de regresión ejecuta el mismo ciclo de vida de subcontrato dos veces, una con nombres reales de las partes y otra con identificadores opacos, y verifica saldos idénticos — prueba mecánica de que la aritmética del libro es independiente de quiénes sean las partes.

En el piloto actual, el ejecutor es MCorp — el cliente de referencia de la plataforma, cuyo personal lleva a cabo el trabajo de construcción y opera el libro contable del piloto. El programa de desarrollo al que pertenece el proyecto es de Woodfine; el libro modela los registros de la parte ejecutora, no los del propietario.

**Por qué importa:** los mismos cinco roles describen igual de bien a un contratista general sin ninguna estructura de tenencia — la prueba concreta de que el motor es software genérico de dominio, no la herramienta interna de una empresa con los nombres borrados.

---

## Los reportes, y la regla de que un cero es una afirmación

La cadena de herramientas del piloto genera sus reportes — un estimado de costos, un cronograma de ruta crítica con línea de tiempo tipo Gantt, un listado de materiales y un reporte mensual de estado del proyecto — en HTML y PDF a través de `tool-typeset`, el renderizador de documentos sin dependencias compartido de la plataforma, desde una sola capa de cómputo por reporte. Cada PDF generado se verifica visualmente, no solo por el éxito de la compilación — una disciplina adoptada después de que compilaciones exitosas produjeran una línea de tiempo ilegible.

Vale la pena señalar dos características del sistema de reportes porque son poco comunes. Primero, el motor computa sus salidas de abajo hacia arriba a partir de las primitivas de los paquetes de trabajo — como lo haría el propio software de estimación y programación de un contratista — y luego las concilia contra los estimados profesionales preparados de forma independiente para el piloto y contra sus fechas de cronograma conocidas, que sirven como hoja de respuestas y no como datos que los reportes simplemente reformatean. Segundo, el reporte de estado se niega a fabricar. Donde no existe una medición real — un costo efectivo sin factura que lo respalde, un porcentaje de avance sin progreso observado, un conteo de incidentes sin registro de seguridad — el reporte imprime una raya, nunca un cero y nunca una proyección disfrazada de observación. Un cero en una columna de incidentes sería en sí mismo una afirmación de seguridad; un espacio en blanco es el estado honesto de los datos.

**Por qué importa:** un reporte de este motor es rastreable hasta un dato de entrada real o está visiblemente vacío — no existe un tercer estado, y esa propiedad la exige la capa de cómputo, no la diligencia de un revisor.

---

## Retención, el período de gravamen y los plazos estatutarios

Los contratos de construcción están sujetos a retención estatutaria (holdback) — un porcentaje definido de cada pago certificado que el propietario retiene, liberado una vez que expira, sin reclamos registrados, un período de gravamen durante el cual los proveedores impagos pueden registrar un reclamo contra el edificio. El diseño contempla tres consecuencias que esto genera: la retención se aplica sobre una solicitud de pago certificada en su totalidad, no solo sobre el trabajo subcontratado; distintos tipos de trabajo llevan distintos períodos de gravamen, por lo que las partes del mismo proyecto quedan liberables en fechas diferentes; y los plazos estatutarios relevantes corren en días hábiles, no en días calendario, lo que convierte un calendario correcto de días hábiles en un requisito legal del software, no en una conveniencia de programación. La mecánica de certificación y retención de la cadena de subcontratos está construida; el modelo de calendario de días hábiles y plazos estatutarios es la pieza más grande de esta sección aún sin implementar, y condiciona los reportes de ciclo de pagos que se apoyarían en él.

**Por qué importa:** una retención liberada un día antes, o un período de gravamen mal contado por siquiera un día hábil, es una falla real de cumplimiento bajo la ley de gravámenes, no un error de redondeo que el software pueda absorber en silencio — precisamente por eso el modelo de calendario se trata como un requisito legal y no como una comodidad de programación.

---

## Servicios de plataforma

Tres piezas del dominio del motor se construyeron deliberadamente como servicios independientes de la plataforma, y no como módulos internos, para que aplicaciones y reportes futuros puedan leer los mismos datos sin pasar por este motor: `service-materials`, el almacén canónico de paquetes de trabajo; `service-schedule`, el servicio de cómputo de ruta crítica; y `service-notify`, un vigilante agnóstico al dominio que se activa ante fechas límite y umbrales excedidos cuando quien lo llama reporta una observación. `tool-construction` los consume como un cliente HTTP ordinario — los paquetes de trabajo del piloto viven en `service-materials`, y el reporte de materiales se genera a partir de lo que el servicio devuelve, no del archivo que el motor cargó. Cada servicio lleva un diario de su estado y reconstruye su índice al reiniciar. Los tres corren localmente hoy; el cableado de supervisión de producción está diferido.

**Por qué importa:** los datos de costo, cronograma y alertas viven detrás de límites de servicio que cualquier aplicación futura puede leer, de modo que el motor CLI es un consumidor más de los datos de la plataforma, no su dueño.

---

## Topología del producto y el límite entre lo gratuito y lo pagado

`tool-construction` es un componente dentro de una familia más amplia: el propio libro contable de construcción; el motor contable hermano, [[tool-accounting]], diseñado para recibir de este una alimentación unidireccional de costo en dólares; `tool-typeset`, el renderizador de documentos compartido que hoy realiza el renderizado de producción de ambos motores; y el motor propuesto de [[tool-payroll]], diseñado para recibir de este libro una alimentación unidireccional de horas y clase de mano de obra como tarjetas de tiempo. Los crates hermanos con alcance de piloto para los motores de contabilidad y nómina ya están andamiados junto al piloto de construcción, pero las alimentaciones entre motores aún no están cableadas — las integraciones del lado de dólares y de nómina esperan los datos efectivos reales descritos arriba.

El sustrato de archivo y la terminal de la plataforma son gratuitos (Apache-2.0); la agregación entre archivos es el límite pagado que aplica en toda la plataforma. `tool-construction` está diseñado como una segunda superficie comercial separada sobre ese límite — lo que se vendería es la ingeniería de dominio en sí (el esquema de puntuación de calidad, las matemáticas de valor ganado, el mecanismo del libro contable), no un margen sobre una infraestructura que ya es gratuita.

Las reglas de distribución de la plataforma clasifican los componentes `tool-*` como herramientas internas del operador que, por defecto, no se distribuyen como producto independiente, con excepciones otorgadas de forma individual — `tool-wallet` es el único precedente existente. **Actualmente no existe ninguna excepción de distribución registrada para `tool-construction`.**

**Por qué importa:** el límite entre lo gratuito y lo pagado se sitúa en la ingeniería de dominio misma, no en la infraestructura subyacente — el mismo principio que mantiene gratuitos el sustrato de archivo y la terminal de la plataforma se aplica aquí también, un nivel más arriba.

## Licenciamiento

`tool-construction` está licenciado bajo AGPL-3.0-or-later. AGPL-3.0-or-later es una licencia copyleft: el código fuente está disponible para todos, y cualquier versión modificada — incluida una operada como servicio de red — debe publicarse bajo la misma licencia si se distribuye o se pone a disposición a través de una red. Existe una licencia PointSav-Commercial independiente como alternativa de pago para quien necesite distribuir una versión modificada, u ofrecerla como servicio de red, sin esa obligación de copyleft.

**Por qué importa:** un prestamista o el propio ingeniero de un propietario puede leer y auditar el código fuente completo antes de decidir si confiar en él — el código no es una caja negra detrás de un muro de pago.

---

## Qué no está construido todavía

Los límites enunciados al inicio merecen precisarse. Aún no construido: el libro de costos del lado de dólares (cuentas por pagar, asientos de nómina, dólares de retención) y con él cualquier reporte de costo efectivo — el piloto no tiene ninguna factura, pago o documento de nómina en su canalización, y el motor reporta esa ausencia en lugar de modelar a su alrededor; una fuente independiente de medición de cantidad instalada, que condiciona el reporte real de valor ganado; el modelo de calendario de días hábiles y plazos estatutarios; las alimentaciones unidireccionales hacia [[tool-accounting]] y [[tool-payroll]]; el adaptador de almacenamiento de archivo que persistiría los datos del libro a través del propio almacén de registros de la plataforma; el mecanismo de transferencia de acceso en la transición de venta; y cualquier superficie de consola o terminal — las dos pantallas propuestas (una vista de tabla del libro contable y un panel de paquete de trabajo/calidad) siguen sin espacio de compilación en la terminal fija de doce teclas de función de la plataforma, y la cadena de herramientas se opera enteramente desde la línea de comandos.

Entre las preguntas de diseño abiertas que permanecen genuinamente sin resolver están si las certificaciones de calidad necesitan firma criptográfica dado su posible peso legal en un reclamo por defectos, si la puntuación de desempeño individual pertenece dentro de este sistema o permanece como un asunto separado, y qué desencadena y autoriza la transferencia de acceso en la transición de venta, y cómo se relaciona con un proceso real de cierre legal.

**Por qué importa:** ninguno de estos vacíos está oculto dentro de una prueba que pasa o un valor de respaldo silencioso — cada uno se nombra aquí para que quien evalúe el motor sepa con precisión qué afirmaciones están demostradas hoy y cuáles siguen siendo una intención declarada.

## Véase también

- [[tool-accounting]] — el motor contable hermano diseñado para recibir de este libro contable una alimentación unidireccional de costo
- [[tool-payroll]] — el motor de nómina propuesto diseñado para recibir de este libro contable una alimentación unidireccional de tarjetas de tiempo
