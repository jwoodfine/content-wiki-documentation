---
schema: foundry-doc-v1
title: "tool-payroll — nómina y remesas estatutarias por jurisdicción"
slug: tool-payroll
category: applications
type: tool
content_type: topic
quality: complete
index_group: financial-and-construction-tools
status: active
audience: vendor-public
bcsc_class: forward-looking
language_protocol: TRANSLATE-ES
last_edited: 2026-09-04
editor: pointsav-engineering
paired_with: tool-payroll.md
short_description: "Motor de nómina y remesas estatutarias sensible a la jurisdicción cuyo primer informe real — un Registro de Nómina por división que agrega las horas laborales presupuestadas del piloto de construcción bajo una fila citada de reglas salariales de una sola jurisdicción — está construido y en funcionamiento; el cálculo bruto-a-neto, la frecuencia de pago y las remesas siguen siendo solo diseño."
cites: []
---

`tool-payroll` es un motor de nómina en su primera etapa real de construcción,
diseñado para gestionar el lado estatutario de pagarle a un trabajador: con qué
frecuencia se le paga, cuándo una fecha de pago calculada puede caer
legalmente, y cómo el hecho de pagar a alguien se relaciona con remitir las
deducciones estatutarias a la autoridad correcta. Es un producto hermano de
[[tool-accounting]], no una función de [[tool-construction]] — de dominio
transversal, no específico de construcción — y está pensado para recibir
tarjetas de horas de ambas herramientas como alimentaciones de una sola vía.

**Lo que existe hoy.** Existe un informe real, y solo uno. Un crate binario
piloto — creado junto a los propios crates piloto de la cadena de herramientas
de construcción, que es donde vive ahora el desarrollo del motor — lee las
horas laborales presupuestadas y los supuestos de cuadrilla que el piloto de
[[tool-construction]] ya mantiene, más la tabla de reglas salariales de una
sola jurisdicción y de una sola fila descrita abajo, los agrega en totales laborales por
división, y renderiza un Registro de Nómina (por División) como HTML y PDF a
través de `tool-typeset`, el mismo renderizador compartido que usan los
motores hermanos. Es un solo comando sin banderas ni argumentos, y sus pruebas
pasan. El límite es igual de real: la frecuencia de pago, el pago bruto y el
pago neto no se calculan en ninguna parte — el registro imprime una raya en
esas columnas en lugar de una cifra fabricada — y nunca se ha registrado una
tarjeta de horas ni una transacción de nómina. Todo lo demás que describe este
artículo sigue siendo diseño.

---

## El problema que está diseñado para resolver

Un trabajador de la construcción que espera cobrar al final del día o al
final de la semana, en lugar de en un ciclo quincenal estándar, es un
requisito operativo real. Atenderlo correctamente exige mantener separados
dos hechos que se confunden con facilidad: con qué frecuencia se paga a un
trabajador, y con qué frecuencia el empleador debe remitir a la autoridad
fiscal las deducciones estatutarias retenidas. Una plataforma que asumiera
en silencio que se trata del mismo reloj calcularía cheques de pago
correctos y presentaría remesas incorrectas, o al revés — exactamente el
modo de falla que este diseño busca evitar.

**Por qué importa:** un empleador que paga a diario a sus trabajadores de la
construcción no tiene, en la mayoría de los casos, que remitir a diario a la
autoridad fiscal — pero la plataforma sí tiene que conocer la diferencia, o
eventualmente confundirá una con la otra.

---

## El Registro de Nómina — el único informe real

La primera salida entregada del motor es un solo documento: el Registro de
Nómina (por División), una planilla de trabajo de labor presupuestada — no un
estado financiero presentado, y no una corrida de pago. El binario piloto lee
tres conjuntos de archivos planos: la propia tabla de correspondencia de
códigos de costo a divisiones del piloto de construcción y sus supuestos de
cuadrilla, sus datos reales de paquetes de trabajo, y la tabla de reglas
salariales de abajo. Une cada código de costo con su división de la industria
de la construcción, agrega las horas laborales presupuestadas y el tamaño de
cuadrilla por división, y renderiza el registro como HTML y PDF.

Vale la pena destacar dos propiedades. Primero, la agregación de horas refleja
deliberadamente, paso a paso, la lógica que el propio informe mensual de
estado del piloto de construcción usa para sus cifras de horas-hombre — los
mismos números subyacentes, calculados de la misma manera, de modo que los dos
documentos nunca puedan divergir en silencio. La lectura es por archivos a
propósito: no existe dependencia de código entre los dos crates piloto, solo
archivos, en línea con la disciplina de alimentación de una sola vía del
diseño. Segundo, las columnas de Frecuencia de Pago y Pago Bruto del registro
imprimen una raya en cada fila, y su propia nota de base de preparación dice
por qué: esos números no existen en ninguna parte — la frecuencia de pago aún
no tiene un lugar diseñado en los datos, y el cálculo bruto-a-neto está
explícitamente fuera de alcance — así que el registro declara el vacío en
lugar de mostrar una cifra plausible. La misma nota imprime los hechos de
jurisdicción que el motor resolvió de su tabla de reglas salariales: el límite
de pago salarial, la base de conteo de días, la autoridad de remesa y la
autoridad de compensación de trabajadores, con la propia cita de fuente de la
fila.

**Por qué importa:** lo primero que entregó este motor es su límite honesto.
Quien lee el registro obtiene horas reales y cifras reales de cuadrilla, una
declaración impresa de qué columnas aún no son reales, y las reglas citadas de
sincronización salarial que eventualmente las regirán — nunca una cifra de
pago inventada.

**Casos límite:** el tamaño de cuadrilla es opcional por división — una
división sin supuesto de cuadrilla también imprime una raya allí, nunca un
cero, porque una cuadrilla de cero sería en sí misma una afirmación.

---

## Alcance de jurisdicción — solo una, y explícitamente piloto

Cada cifra de sincronización salarial y remesa vive como una fila citada en
una tabla organizada por jurisdicción — `wage_payment_rules.csv`, ahora un
archivo real que el registro en funcionamiento carga — nunca como una regla
codificada de forma fija en el motor. Al momento de escribir esto, solo hay
**una fila de jurisdicción poblada y verificada**, que corresponde a la
provincia donde se encuentra el sitio piloto (no se nombra en contenido
público). Esto es explícitamente un alcance piloto, no
cobertura de plataforma. Toda otra jurisdicción es un vacío nombrado y sin
poblar. Se pretende que una entidad cuya jurisdicción carezca de fila sea un
vacío rechazado y visible, en lugar de recibir en silencio los valores
de la fila poblada por defecto.

```
wage_payment_rules.csv — real; una fila poblada y con fuente citada

jurisdiction_code,max_pay_period_days,max_days_to_pay_after_period_end,
day_counting,remitting_authority,comp_authority,source_ref,effective_from

[jurisdicción],31,10,calendar,CRA,WCB [jurisdicción],"estatuto de pago
salarial de la jurisdicción; calendario federal de tipos de remitente;
mecánica de primas de empleador de la junta de compensación de trabajadores",
```

Las citas viajan en el propio campo `source_ref` de la fila, de modo que la
regla y su fuente van juntas — quien revisa nunca tiene que confiar en que un
número en el motor coincide con una regla en otro lugar.

**Por qué importa:** se planea que agregar una segunda provincia, o una
jurisdicción fuera de Canadá, signifique agregar una fila citada a una
tabla — no tocar código del motor. Si ese plan se sostiene en la práctica
está por verse, ya que todavía no existe ninguna segunda fila de
jurisdicción.

---

## Dos relojes independientes: frecuencia de pago y frecuencia de remesa

La frecuencia de pago — con qué frecuencia se paga a un trabajador — está
diseñada para estar completamente desacoplada de la frecuencia de remesa
estatutaria, la distinción más consecuente de todo este diseño. Se pretende
que la frecuencia de pago sea configurable por el operador, por cuadrilla o
empleado: diaria, semanal, quincenal o semi-mensual, con el mes como límite
superior en la fila citada de la jurisdicción piloto, en lugar de una opción
distinta del
operador. La frecuencia de remesa, en cambio, es un hecho a nivel de
*empleador* fijado por la autoridad fiscal según el volumen de retención
histórico. La mayoría de los empleadores remite mensualmente sin importar
con qué frecuencia paguen a su personal. Solo a los empleadores de mayor
volumen se les exige remitir con más frecuencia a medida que ese volumen
aumenta.

La única excepción documentada: un empleador cuyo volumen de retención
histórico cruza un umbral alto y que paga a su personal más de dos veces al
mes puede estar obligado a remitir en cada día de pago. Por debajo de ese
umbral, pagar a diario o semanalmente a los trabajadores de la construcción
no se espera que, por sí solo, obligue a una remesa diaria o semanal.

**Por qué importa:** un empleador que paga a diario a trabajadores de la
construcción puede, en tamaños de nómina ordinarios, seguir remitiendo a la
autoridad fiscal en el calendario mensual habitual. La expectativa de pago
diario que exigen los trabajadores de la construcción a su empleador y la
obligación de remesa del empleador son dos preguntas distintas con dos
respuestas distintas.

---

## El límite de pago salarial

La regla citada de la jurisdicción piloto fija un límite máximo estricto:
una fecha de pago calculada para un periodo de pago dado no puede caer más
tarde del número de días que indique la jurisdicción después de que termine
el periodo. La fila citada de la jurisdicción piloto fija ese número en diez
días calendario consecutivos. El diseño pretende que el motor rechace, en
lugar de ajustar en silencio, cualquier configuración o entrada manual de
fecha de pago que violaría este límite una vez resuelto a partir de la fila
de jurisdicción de la entidad. Se pretende que una corrida de pago que
caería fuera de la ventana aparezca como un error nombrado y bloqueante, no
como una advertencia.

Hoy el límite es dato, no aplicación: el registro en funcionamiento resuelve
la fila de la jurisdicción piloto e imprime la cifra de diez días en sus
propias notas, pero todavía no se calcula ninguna fecha de pago en ninguna
parte, así que el comportamiento de rechazar-en-lugar-de-ajustar sigue
siendo diseño.

Las propias excepciones publicadas por la jurisdicción piloto para la
industria de la construcción son estrechas: cubren solo cómo puede
sincronizarse el pago de vacaciones y el pago de días festivos generales.
No cubren un periodo de
pago más corto o más largo, ni una regla de sincronización de pago distinta
para los trabajadores de la construcción o el trabajo por jornada en
general. Se diseña que los trabajadores de la construcción sigan el mismo
límite que cualquier otro empleado en esa fila — este hallazgo es
específico de la jurisdicción piloto y no se asume que se generalice a
ninguna otra jurisdicción.

**Por qué importa:** el derecho legal de un trabajador a cobrar dentro de
una ventana acotada después de realizar el trabajo no se flexibiliza para
los oficios de la construcción, al menos bajo la regla de la jurisdicción
piloto — el
diseño trata esto como una restricción estricta que aplica el motor, no
como una preferencia que pueda anular.

---

## Los días calendario y los días laborables nunca son el mismo reloj

El reloj de pago salarial de la jurisdicción piloto cuenta días calendario.
Un conjunto distinto de relojes, ya real y en operación dentro de
[[tool-construction]]
— que rigen la liberación de retenciones y la sincronización de pago
pronto entre partes contratantes — cuenta en cambio días *laborables*. Se
trata de regímenes legalmente distintos: uno rige los salarios que se le
deben a un empleado bajo la ley de normas de empleo; el otro rige los pagos
de avance entre partes contratantes bajo el derecho contractual. El propio
estatuto de pago pronto de la construcción establece directamente que sus
relojes no reducen ni alteran las obligaciones de pago salarial de un
empleador.

El diseño trata `day_counting` como su propio campo en la fila de
jurisdicción — `calendar` para el reloj salarial de la jurisdicción piloto —
en lugar de
una constante fija compartida con cualquier calendario de días laborables
que tool-construction ya mantiene para sus propios fines. Una regla que
tomara prestado en silencio el conteo de días de un reloj para el otro se
trataría como un defecto real de cumplimiento, no como una diferencia de
redondeo.

**Por qué importa:** dos plazos legales distintos pueden parecer el mismo
tipo de cuenta regresiva y no lo son — confundirlos es exactamente la clase
de error que este diseño está estructurado para hacer estructuralmente
difícil de cometer.

---

## Reporte de compensación de trabajadores — un tercer reloj, independiente

El reporte de ingresos evaluables para compensación de trabajadores y la
remesa de primas está diseñado como ortogonal a ambos relojes anteriores.
El requisito citado de la jurisdicción piloto es una estimación anual de
nómina más una
remesa periódica de primas — mensual, trimestral o anual, a elección del
empleador por debajo de un umbral de tamaño de nómina — a la junta
provincial de compensación de trabajadores. Ese calendario no sigue con qué
frecuencia, ni con qué rapidez, un empleador paga a sus trabajadores.

El diseño modela esto como un campo `comp_authority` por fila de
jurisdicción — la junta de la jurisdicción piloto es el único valor poblado
hoy; las juntas equivalentes de otras jurisdicciones son filas nombradas
pero sin poblar, y no se asume que compartan su mecánica específica.

**Por qué importa:** una plataforma de nómina puede acertar tanto en la
sincronización salarial como en la remesa fiscal y aun así reportar mal las
primas de compensación de trabajadores si asume que ese reloj depende de
alguno de los otros dos — el diseño lo mantiene separado a propósito.

---

## Lógica de calendario y días festivos

Un mecanismo concreto está dentro del alcance más allá de las reglas de
sincronización anteriores. Se pretende que una fecha de pago calculada que
caiga en fin de semana o día festivo estatutario se traslade al día hábil
anterior, práctica estándar de nómina en el mundo real. Eso requiere un
calendario de días festivos organizado por jurisdicción.

El diseño sigue un patrón ya establecido en otra parte de la plataforma. Se
prevé que un servicio de programación propuesto, aún no construido y
residente en el archivo, se convierta eventualmente en la fuente
compartida y canónica de calendario de días festivos entre
[[tool-construction]], `tool-payroll` y [[tool-accounting]]. Pero se
diseña que la propia tabla de calendario de días festivos de `tool-payroll`
funcione de forma autónoma en modo de archivo plano primero, sin
dependencia de compilación con ese servicio compartido. Ese punto de
convergencia se nombra como una intención futura, no construida ahora.

**Por qué importa:** el diseño está estructurado para que `tool-payroll`
pueda funcionar correctamente por sí solo, con una carpeta de archivos de
datos y ningún otro servicio en ejecución, y aun así poder conectarse más
adelante a un calendario compartido sin necesidad de rediseño.

---

## El límite de conectividad bancaria

Si `tool-payroll` — o cualquier elemento de la plataforma que lo rodea —
debería conectarse a un banco se responde de forma estrecha y deliberada.
El diseño propone un componente de ingesta acotado y de solo lectura
(nombre de trabajo `service-bank-feed`) en lugar de cualquier conexión
bancaria más amplia. Está modelado sobre un precedente real, ya en
operación en otra parte de la plataforma, para extraer datos de un sistema
externo nombrado. El nombre en sí es una elección deliberada: se consideró y se
rechazó un componente cuyo nombre pudiera leerse como la gestión de una
relación bancaria, en favor de uno cuyo nombre indica claramente que solo
extrae una alimentación de solo lectura.

| Propuesto para hacer | Explícitamente fuera de alcance |
|---|---|
| Extraer datos de transacciones de solo lectura de un banco o agregador externo nombrado, mediante una conexión estrecha y de propósito único | Alcanzar cualquier punto de red más allá de esa única integración — sin acceso general a internet |
| Analizar y normalizar la alimentación en un registro estructurado (fecha, monto, moneda, contraparte, referencia) — solo de forma determinista | Clasificar o interpretar el significado de una transacción — eso sigue siendo un paso humano o un paso de clasificación separado |
| Agregar el registro normalizado al libro mayor de solo-anexado de la plataforma | Editar o eliminar un registro existente del libro mayor |
| Exponer la alimentación cruda y sin clasificar para revisión humana | Reconciliar o cerrar automáticamente un periodo sin revisión humana |
| Mantener el alcance mínimo de credenciales necesario para una conexión de solo lectura | Iniciar un pago, transferencia bancaria o pago de facturas, o escribir cualquier cosa de vuelta al banco |

No existe hoy ninguna capacidad de escritura hacia un banco en ningún punto
del diseño actual. Si alguna vez se lleva adelante la iniciación de pagos,
la forma prevista es un archivo de instrucción de pago generado y entregado
a una parte con licencia separada — el propio banco del empleador o un
procesador de pagos con licencia. La entrega sigue un esquema de aprobación
de doble control; nunca es un movimiento de dinero realizado por
`tool-payroll` mismo. Esa forma se nombra como la dirección futura
correcta; explícitamente no está diseñada ni construida en esta etapa.

**Por qué importa:** la plataforma está diseñada de modo que nada en esta
tubería pueda mover dinero por sí solo — se planea que cada paso que mueve
dólares permanezca en manos de una parte con licencia separada, por diseño
y no por accidente.

---

## Relación con tool-accounting y tool-construction

`tool-payroll` está diseñado con dos fuentes de alimentación previstas que
llegan a un mismo destino. Las tarjetas de horas de cuadrilla de
[[tool-construction]] están planeadas como una alimentación. Se prevé que
[[tool-accounting]] mismo alimente directamente a `tool-payroll` para el
propio personal no relacionado con construcción de un operador. Se
pretende que el cálculo bruto-a-neto sea idéntico sin importar si el
empleador es un operador de construcción o cualquier otro tipo de negocio.
Ambas alimentaciones están diseñadas para llegar al libro mayor de
`tool-accounting` de la misma manera — como asientos ordinarios, de una
sola vía, por el mismo camino de revisión que cualquier otra transacción de
origen.

Un precursor de la primera alimentación ya es real, y es deliberadamente más
estrecho que la alimentación que nombra el diseño: el Registro de Nómina lee
las horas *presupuestadas* de los paquetes de trabajo del piloto de
construcción como archivos planos. Un presupuesto es una cifra de etapa de
estimación; una tarjeta de horas es un registro de datos reales, y todavía no
existe ninguna tarjeta de horas en ninguna parte del canal — el mismo límite
de etapa-de-estimación que el propio motor de construcción declara para su
libro mayor.

```
tool-construction (horas + clase laboral)   ──▶  tool-payroll   (alimentación 1)
tool-accounting (horas de personal propio)  ──▶  tool-payroll   (alimentación 2)
tool-payroll (dólares calculados)           ──▶  tool-accounting  (asientos ordinarios)
tool-payroll (dólares calculados)           ──▶  tool-construction  (libro de costos, una sola vía)
```

Se espera que un agregador de costos entre proyectos que ya existe para la
plataforma contable no necesite ninguna conexión directa con `tool-payroll`
en absoluto. Agrega el libro mayor contable ya asentado de cada entidad,
que ya contiene cualesquiera dólares de nómina que hayan llegado allí, sin
importar de qué alimentación provengan. Eso se desprende del diseño de una
sola vía, agnóstico a la fuente, en lugar de requerir una integración
separada.

Se planea que las pantallas de operador para aprobación de tarjetas de
horas y corridas de pago extiendan una superficie de terminal de
contabilidad ya existente en lugar de crear una nueva. El modelo de
terminal de la plataforma favorece extender una superficie compartida
sobre agregar una pantalla dedicada por herramienta. Esta extensión está
propuesta, aún no aprobada por quien es dueño de esa superficie.

**Por qué importa:** se pretende que una cuadrilla de construcción y el
propio personal de oficina de un despacho de abogados se paguen a través
del mismo motor idéntico — lo único que difiere es de qué herramienta
provienen las horas.

---

## Licenciamiento

`tool-payroll` está licenciado bajo AGPL-3.0-or-later. AGPL-3.0-or-later es una licencia
copyleft: el código fuente está disponible para todos, y cualquier versión modificada —
incluida una operada como servicio de red — debe publicarse bajo la misma licencia si se
distribuye o se pone a disposición a través de una red. Existe una licencia
PointSav-Commercial independiente como alternativa de pago para quien necesite distribuir
una versión modificada, u ofrecerla como servicio de red, sin esa obligación de copyleft.

---

## Resumen de estado

| Componente | Estado |
|---|---|
| Registro de Nómina (por División) — agregación de horas presupuestadas y cuadrilla por división, HTML + PDF | **Construido y en funcionamiento** — el primer informe real del motor; un solo comando sin banderas |
| Tabla de jurisdicción (`wage_payment_rules.csv`) | Real — una fila poblada y con fuente citada (jurisdicción no nombrada en contenido público), cargada por el informe en funcionamiento. Toda otra jurisdicción es un vacío nombrado y sin poblar |
| Clasificación y contrato de integración con `tool-construction` | Fijado como decisión de diseño; una lectura por archivos de las horas presupuestadas del piloto de construcción es real, pero la alimentación de tarjetas de horas en sí no está construida |
| Diseño de cadencia de pago y sincronización estatutaria (modelo de jurisdicción, los dos relojes, el límite de pago salarial, la distinción calendario/laborable, el reporte de compensación de trabajadores) | Diseñado y fijado; la aplicación no está construida — todavía no se calcula ninguna fecha de pago en ninguna parte |
| El cálculo bruto-a-neto mismo (tramos impositivos, fórmulas de deducción estatutaria) | Explícitamente diferido; no diseñado |
| El motor y los crates orientados al operador | Primer crate piloto creado y en funcionamiento, desarrollado junto a la cadena de herramientas de construcción; todavía no existe un crate de motor completo |
| `service-bank-feed` | Propuesto; propiedad aún no confirmada; aún no se ha enviado una propuesta formal |
| Generación de archivo de pago y aprobación de doble control | Nombrado como la forma futura prevista; no diseñado ni construido |
| Extensión de la terminal de contabilidad para aprobación de corridas de pago y tarjetas de horas | Propuesta; requiere el visto bueno de quien es dueño de esa superficie |

---

## Véase también

- [[tool-accounting]] — el producto hermano que `tool-payroll` está diseñado
  para extender; se prevé que ambos compartan el mismo motor bruto-a-neto sin
  importar qué herramienta le alimente las horas
- [[tool-construction]] — la herramienta cuyas tarjetas de horas de cuadrilla
  están diseñadas como una de las dos fuentes de alimentación previstas de
  `tool-payroll`, y cuyas horas presupuestadas del piloto ya lee el primer
  informe real
