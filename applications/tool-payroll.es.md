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
language_protocol: PROSE-TOPIC
last_edited: 2026-08-30
editor: pointsav-engineering
paired_with: tool-payroll.md
short_description: "Un motor propuesto, sensible a la jurisdicción, para nómina bruto-a-neto y remesas estatutarias — actualmente 100% diseño, sin código escrito y sin crate creado."
cites: []
---

`tool-payroll` es un motor de dominio propuesto para calcular el pago
bruto-a-neto de un trabajador. Está diseñado para gestionar el lado
estatutario de pagarle: con qué frecuencia se paga a un trabajador, cuándo
una fecha de pago calculada puede caer legalmente, y cómo el hecho de pagar
a alguien se relaciona con remitir las deducciones estatutarias a la
autoridad correcta. Está planeado
como producto hermano de [[tool-accounting]], no como una función de
[[tool-construction]] — de dominio transversal, no específico de
construcción — y está pensado para recibir tarjetas de horas de ambas
herramientas como alimentaciones de una sola vía.

**Nada de lo descrito en este artículo está construido.** `tool-payroll` es
hoy 100% diseño: no se ha escrito código alguno, no se ha creado ningún
crate, y no se ha asignado ningún archivo para desarrollarlo. El trabajo de
diseño que sí existe — la capa de cadencia de pago y sincronización
estatutaria que cubre este artículo — está fijado como decisión de diseño,
no entregado como software.

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

## Alcance de jurisdicción — solo Alberta, y explícitamente piloto

Cada cifra de sincronización salarial y remesa en el diseño está planeada
como una fila citada en una tabla organizada por jurisdicción
(`wage_payment_rules.csv`, propuesta, aún no creada), nunca como una regla
codificada de forma fija en el motor. Al momento de escribir esto, solo hay
**una fila de jurisdicción poblada y verificada: Alberta**, porque el sitio
piloto previsto se encuentra allí. Esto es explícitamente un alcance piloto,
no cobertura de plataforma. Toda otra jurisdicción es un vacío nombrado y
sin poblar. Se pretende que una entidad cuya jurisdicción carezca de fila
sea un vacío rechazado y visible, en lugar de recibir en silencio los
valores de Alberta por defecto.

```
wage_payment_rules.csv                              [PROPUESTO — aún no creado]

jurisdiction_code                  estilo ISO-3166-2, ej. CA-AB     [clave primaria]
max_pay_period_days                periodo de pago máximo permitido, días
max_days_to_pay_after_period_end   el límite de pago salarial
day_counting                       calendar | working
remitting_authority                ej. CRA (federal, cualquier jurisdicción canadiense)
comp_authority                     ej. WCB Alberta
source_ref                         cita
effective_from                     fecha

# la única fila actualmente poblada y citada:
CA-AB,31,10,calendar,CRA,WCB Alberta,alberta.ca/payment-earnings,2026-01-01
```

**Por qué importa:** se planea que agregar una segunda provincia, o una
jurisdicción fuera de Canadá, signifique agregar una fila citada a una
tabla — no tocar código del motor. Si ese plan se sostiene en la práctica
está por verse, ya que aún no se ha diseñado ninguna segunda jurisdicción.

---

## Dos relojes independientes: frecuencia de pago y frecuencia de remesa

La frecuencia de pago — con qué frecuencia se paga a un trabajador — está
diseñada para estar completamente desacoplada de la frecuencia de remesa
estatutaria, la distinción más consecuente de todo este diseño. Se pretende
que la frecuencia de pago sea configurable por el operador, por cuadrilla o
empleado: diaria, semanal, quincenal o semi-mensual, con el mes como límite
superior en la fila citada de Alberta, en lugar de una opción distinta del
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

La regla citada de Alberta fija un límite máximo estricto: una fecha de
pago calculada para un periodo de pago dado no puede caer más tarde del
número de días que indique la jurisdicción después de que termine el
periodo. La fila citada de Alberta fija ese número en diez días calendario
consecutivos. El diseño pretende que el motor rechace, en lugar de ajustar
en silencio, cualquier configuración o entrada manual de fecha de pago que
violaría este límite una vez resuelto a partir de la fila de jurisdicción
de la entidad. Se pretende que una corrida de pago que caería fuera de la
ventana aparezca como un error nombrado y bloqueante, no como una
advertencia.

Las propias excepciones publicadas por Alberta para la industria de la
construcción son estrechas: cubren solo cómo puede sincronizarse el pago de
vacaciones y el pago de días festivos generales. No cubren un periodo de
pago más corto o más largo, ni una regla de sincronización de pago distinta
para los trabajadores de la construcción o el trabajo por jornada en
general. Se
diseña que los trabajadores de la construcción sigan el mismo límite que
cualquier otro empleado en la fila de Alberta — este hallazgo es específico
de Alberta y no se asume que se generalice a ninguna otra jurisdicción.

**Por qué importa:** el derecho legal de un trabajador a cobrar dentro de
una ventana acotada después de realizar el trabajo no se flexibiliza para
los oficios de la construcción, al menos bajo la regla de Alberta — el
diseño trata esto como una restricción estricta que aplica el motor, no
como una preferencia que pueda anular.

---

## Los días calendario y los días laborables nunca son el mismo reloj

El reloj de pago salarial de Alberta cuenta días calendario. Un conjunto
distinto de relojes, ya real y en operación dentro de [[tool-construction]]
— que rigen la liberación de retenciones y la sincronización de pago
pronto entre partes contratantes — cuenta en cambio días *laborables*. Se
trata de regímenes legalmente distintos: uno rige los salarios que se le
deben a un empleado bajo la ley de normas de empleo; el otro rige los pagos
de avance entre partes contratantes bajo el derecho contractual. El propio
estatuto de pago pronto de la construcción establece directamente que sus
relojes no reducen ni alteran las obligaciones de pago salarial de un
empleador.

El diseño trata `day_counting` como su propio campo en la fila de
jurisdicción — `calendar` para el reloj salarial de Alberta — en lugar de
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
El requisito citado de Alberta es una estimación anual de nómina más una
remesa periódica de primas — mensual, trimestral o anual, a elección del
empleador por debajo de un umbral de tamaño de nómina — a la junta
provincial de compensación de trabajadores. Ese calendario no sigue con qué
frecuencia, ni con qué rapidez, un empleador paga a sus trabajadores.

El diseño modela esto como un campo `comp_authority` por fila de
jurisdicción — la junta de Alberta es el único valor poblado hoy; las
juntas equivalentes de otras provincias son filas nombradas pero sin
poblar, y no se asume que compartan la mecánica específica de Alberta.

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

`tool-payroll` está licenciado bajo FSL-1.1-ALv2.

---

## Resumen de estado

| Componente | Estado |
|---|---|
| Clasificación y contrato de integración con `tool-construction` | Fijado como decisión de diseño |
| Diseño de cadencia de pago y sincronización estatutaria (modelo de jurisdicción, los dos relojes, el límite de pago salarial, la distinción calendario/laborable, el reporte de compensación de trabajadores) | Diseñado y fijado; no construido |
| Cobertura de jurisdicción | Una fila poblada y completamente citada (Alberta). Toda otra jurisdicción es un vacío nombrado y sin poblar |
| El cálculo bruto-a-neto mismo (tramos impositivos, fórmulas de deducción estatutaria) | Explícitamente diferido; no diseñado |
| El motor `tool-payroll` y los crates orientados al operador | No creados. Ningún archivo asignado para desarrollarlo |
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
  `tool-payroll`
