---
schema: foundry-doc-v1
title: "tool-accounting — libro mayor de partida doble y estados financieros auditables"
slug: tool-accounting
category: applications
type: tool
content_type: topic
quality: complete
index_group: financial-and-construction-tools
status: active
audience: vendor-public
bcsc_class: forward-looking
language_protocol: TRANSLATE-ES
last_edited: 2026-09-01
editor: pointsav-engineering
paired_with: tool-accounting.md
short_description: "Un motor de contabilidad de partida doble, en archivos planos y de propiedad del titular, que produce estados financieros auditables a partir de diarios en texto plano; su motor central y su renderizador PDF/HTML están construidos y verificados contra datos históricos reales, por delante del resto de las herramientas de libro mayor de la plataforma."
cites: []
---

`tool-accounting` es un motor de contabilidad de partida doble construido para mantener
los libros de un grupo de entidades relacionadas como un registro en texto plano, de
propiedad del titular, en lugar de filas en una base de datos alojada. Registra cada
transacción en el diario. Pliega esos diarios en un libro mayor y un balance de
comprobación calculados. Y renderiza estados financieros auditables y su narrativa
correspondiente — sin requerir un servidor, una suscripción, ni un formato de archivo
propietario para volver a leer nada de ello más adelante.

El problema que resuelve es la durabilidad y la demostrabilidad al mismo tiempo. Busca
dejar un conjunto de libros que cualquier computadora pueda seguir leyendo dentro de veinte
años, que nada pueda sobrescribir silenciosamente. Un contador revisor debería poder
rastrear una cifra del estado financiero hasta el asiento que la produjo — sin tener que
confiar en la palabra de nadie sobre el camino intermedio.

---

## Compromiso de diseño: partida doble, calculada y nunca almacenada

Cada transacción se registra como dos efectos de igual magnitud y signo opuesto en dos
cuentas distintas — un pago reduce el efectivo y aumenta un gasto por el monto idéntico, en
un solo asiento. Como cada saldo de cuenta se construye a partir de muchos de estos efectos
pareados que siempre se cancelan entre sí, la suma de todos los saldos del libro mayor es
demostrablemente cero en todo momento. Ese hecho, verificado mecánicamente en el instante
en que se registra un asiento, detecta lo que un simple saldo corriente no puede: un
asiento desbalanceado, una referencia a una cuenta que no existe, un monto registrado solo
en un lado.

**Por qué importa:** un error en un libro de partida doble no puede esconderse como sí
puede hacerlo en un saldo corriente simple — los libros cuadran, o el motor rechaza el
asiento que los desequilibró. Eso es lo que permite confiar en un conjunto de libros que
nadie ha auditado todavía.

`tool-accounting` nunca almacena el libro mayor en sí. El saldo corriente de cada cuenta se
recalcula por completo a partir de los asientos de diario subyacentes cada vez que se
ejecuta un informe, y el resultado nunca se vuelve a escribir. Una segunda copia,
actualizada de forma incremental, es una segunda cosa que puede desviarse del diario del
que supuestamente se derivó. Un libro mayor sin existencia propia fuera de los asientos a
partir de los cuales se acaba de calcular no puede estar en desacuerdo con ellos.

```rust
pub struct Money {
    pub minor: i64,          // un conteo entero exacto de unidades menores — nunca un float
    pub currency: Currency,  // se registra explícitamente en cada monto
}
```

Los valores monetarios son enteros, nunca de punto flotante — un monto se analiza una sola
vez desde texto hacia un conteo exacto de unidades menores y permanece exacto a través de
cada cálculo. Un valor ingresado con más de dos decimales se rechaza directamente, en lugar
de redondearse, porque el ruido de punto flotante introducido aguas arriba no es un monto
real.

**Casos límite:** cada ejecución de informe toma una `run_date` explícita provista por
quien la invoca — nunca el reloj del sistema — de modo que el mismo registro, renderizado
de la misma manera dos veces, produce una salida idéntica byte a byte sin importar cuándo o
dónde se ejecute. Un período de reporte siempre es explícitamente disjunto (un solo
trimestre) o acumulado (año hasta la fecha); el motor nunca infiere cuál de los dos a
partir del contexto, y una etiqueta acumulada se rechaza directamente a nivel del asiento
de diario.

---

## El modelo de datos

El plan de cuentas de cada entidad es un único archivo plano, no una tabla que un operador
pueda extender silenciosamente escribiendo un código nuevo dentro de una transacción. Un
asiento que haga referencia a una cuenta que el plan de cuentas no contiene falla al
cargarse — un fallo de invariante, no una cuenta nueva creada como efecto secundario. Un
pequeño conjunto de otros archivos maestros mantiene la misma disciplina. Cada uno es la
única fuente de verdad para una categoría de hecho, referenciado por código en lugar de
volver a escribirse en el punto de uso. Entre ellos: un registro de entidades
(jurisdicción, moneda funcional, marco de reporte, qué períodos se entregan formalmente),
un registro de contrapartes, un registro de períodos, saldos de apertura, y una tabla de
tipos de cambio. Una tabla de membresía de consolidación completa el conjunto, mantenida
separada tanto del plan de cuentas como del registro de entidades.

**Por qué importa:** quien revisa el plan de cuentas ve las mismas preguntas abiertas que
ve el motor. Una cuenta cuya convención de signo aún no está decidida se excluye de todo
estado financiero calculado y se reporta por nombre — nunca se adivina.

Cada transacción registrada es una fila de un esquema fijo de diecisiete campos. Los
campos cubren entidad, cuenta, año fiscal, trimestre disjunto y fecha de la transacción;
contraparte (etiquetada como intercompañía o externa en el momento del registro, nunca
inferida después) y descripción; número de referencia y un subtotal antes de impuestos y
un monto de impuesto opcionales; y moneda, el monto en la moneda funcional, y una
referencia de factura. Existe exactamente un esquema de este tipo. El motor rechaza cargar
un archivo cuya estructura se haya desviado de él.

```rust
pub struct JournalLine {
    pub entity_code: String,
    pub account_code: String,
    pub fiscal_year: u16,
    pub period: JournalPeriod,        // Q1 | Q2 | Q3 | Q4 — siempre disjunto
    pub txn_date: String,
    pub counterparty_type: String,    // "intercompany" | "external"
    pub amount: Money,                // el monto en moneda funcional
    // ...
}
```

**Cómo funciona, en modo de archivos planos:** los archivos de diario existen como CSV
dentro de un repositorio git plano sin remotos — un directorio que `tool-accounting-core`
lee por completo una vez por cada ejecución de informe, nunca una vez por cuenta. El propio
nombre del archivo lleva la entidad, la cuenta, el año fiscal y el trimestre, duplicando
deliberadamente lo que ya está dentro del archivo, de modo que un pase de verificación
pueda cruzar la identidad declarada de un archivo contra sus propias filas.

---

## Consolidación y estructura multi-entidad

`tool-accounting` está construido para sostener más de una entidad a la vez: una entidad
de reporte principal, un socio administrador o entidad controladora equivalente excluida
de su propia consolidación, y una o más subsidiarias de propiedad total consolidadas dentro
del grupo. Cada nivel puede tener una obligación de reporte distinta, registrada por
entidad en lugar de asumida a nivel de toda la plataforma. Combinar los libros de entidades
relacionadas no es una simple suma. Una transacción intercompañía debe identificarse como
tal en el momento en que se registra. Una eliminación requiere que ambos lados de una
transacción cuadren exactamente en la misma cifra antes de eliminarse. Y cada asiento de
eliminación es en sí mismo un asiento de diario ordinario y revisable — nunca un ajuste de
hoja de cálculo invisible para quien no lo haya construido.

**Por qué importa:** el balance consolidado de un grupo no debería simplemente sumar lo
que una entidad le debe a otra y llamarlo deuda del grupo — eso duplica una obligación que,
vista desde afuera del grupo, no es ninguna obligación. El motor se niega a eliminar un par
que no cuadre, en lugar de disimular la diferencia.

El porcentaje de propiedad es un campo general en cada fila de membresía de consolidación
desde el inicio, incluso cuando hoy todos los miembros son de propiedad total. Así, la
lógica de patrimonio no necesita una reescritura estructural si alguna vez se agrega una
entidad de propiedad parcial.

---

## Postura de preparación para auditoría

El objetivo de diseño es un registro que un contador revisor pudiera razonablemente aceptar
como confiable sin tener que volver a realizarlo de forma independiente. Cuatro
propiedades cumplen ese objetivo: una salida reproducible a partir de las mismas entradas;
una población de asientos a prueba de manipulación una vez registrados; un saldo de
apertura re-derivado de forma independiente en lugar de solo afirmado; y un camino
mecánico desde cualquier cifra del estado financiero hasta los asientos que la
produjeron. **Esta es una postura de diseño, no una certificación de cumplimiento de
ningún tipo** — un diseño que hace una auditoría más eficiente de
realizar no es la misma afirmación que un diseño que ya ha pasado una.

**Por qué importa:** un propietario que nunca ha contratado a un auditor de todas formas
obtiene un registro sostenido con la misma disciplina que exigiría una auditoría. El
estándar no espera a que alguien revise el trabajo.

El motor se niega a renderizar cualquier cosa ante un fallo de invariante — un asiento
desbalanceado, una referencia a una cuenta nunca declarada, una discrepancia sin resolver
en el saldo de apertura — en lugar de continuar con una advertencia. La única excepción
gobernada es una partida de conciliación formalmente registrada, la cual está obligada a
cerrarse dentro de dos períodos de reporte o la ejecución falla por completo.

---

## Dónde vive el registro

`tool-accounting-core` funciona hoy contra un directorio plano de archivos CSV — un modo
real, en funcionamiento, y permanente en lugar de una etapa que la plataforma pretenda
retirar. Un segundo modo de almacenamiento está previsto pero aún no construido: agregar
esos mismos registros a través del registro de anexado con encadenamiento hash y
verificación de manipulación de [[service-fs]], dentro de un [[totebox-archive]]. Ese modo
permitiría a un contador revisor verificar no solo que el contenido de un asiento no ha
sido alterado, sino también que el registro en el que se encuentra solo se ha ido
anexando desde un punto de control previo que esa persona sostuvo. Se pretende que ambos
modos compartan
todas las capas por encima del propio trait de almacenamiento, de modo que cuál de los dos
use un propietario no cambiaría nada de la lógica del motor — solo dónde viven los bytes.

**Por qué importa:** nunca se exige a un propietario adoptar una plataforma alojada para
usar el libro mayor. El motor puede entregarse a un contador como una carpeta en una
laptop, y cada cifra de un estado financiero puede reproducirse a partir de ella en la
propia máquina de ese contador.

---

## Estado de construcción

`tool-accounting-core` reúne los tipos compartidos de dinero, período y línea de diario, el
analizador de CSV, y la lógica del plan de cuentas, el libro mayor y el balance de
comprobación. Está construido y ha sido verificado contra datos históricos anuales reales
en lugar de datos de prueba sintéticos, lo cual sacó a la luz y corrigió defectos reales de
entrada de datos en el proceso. `tool-typeset`, el renderizador de PDF y HTML sin
dependencias que este motor comparte con la herramienta hermana de construcción de la
plataforma, está construido y verificado de forma independiente extrayendo texto de un PDF
renderizado y comparándolo contra la estructura de origen. Juntos, ya han ejecutado el
canal completo de un año fiscal entero — diarios hacia un libro mayor calculado, un balance
de comprobación plegado a partir de él, estados financieros renderizados, y narrativa
renderizada. Esa corrida se introdujo y renderizó de extremo a extremo para una entidad de
reporte principal y su socio administrador, y un segundo año está actualmente en curso.

**Por qué importa:** a quien evalúa esta plataforma no se le pide confiar en el diseño por
fe. Los componentes que tocan cifras de dinero real ya han sido verificados contra un año
real de transacciones reales, no solo diseñados en papel. Eso sitúa a `tool-accounting`
más avanzado que cualquier herramienta comparable en el resto de la familia de
herramientas de libro mayor de la plataforma.

Lo que está registrado pero aún no activo: varias entidades subsidiarias de propiedad total
están registradas como miembros de consolidación, con la membresía y el porcentaje de
propiedad registrados y totalmente especificados. Pero el cálculo de la consolidación en
sí aún no está integrado, todavía no existen datos de diario para esas subsidiarias, y el
renderizado de estados financieros intermedios (trimestrales) está especificado pero aún
no construido. Los saldos de apertura están vacíos para todas las entidades. Las
ejecuciones actuales tratan un saldo de apertura como una partida abierta en lugar de
asumir una cifra, y la verificación dual contra el saldo de cierre del año anterior es un
diseño ya decidido, pero aún no ejercitado en la práctica. La terminal de
revisión contable prevista para confirmar asientos hacia el libro mayor está construida
como andamiaje y activa como superficie de complemento, pero todavía no está conectada a
datos reales del libro mayor — su vista actual renderiza cifras de marcador de posición.
Un componente de agregación entre archivos, previsto para una firma que administra los
libros de muchos propietarios a la vez, se menciona aquí bajo el nombre de trabajo
`app-orchestration-accounting`. **Este es solo un nombre y un alcance propuestos — no un
nombre ratificado en ninguna otra parte de la plataforma** — y todavía no existe nada bajo
ese nombre.

---

## Licenciamiento

`tool-accounting` está licenciado bajo AGPL-3.0-or-later. AGPL-3.0-or-later es una
licencia copyleft: el código fuente está disponible para todos, y cualquier versión
modificada — incluida una operada como servicio de red — debe publicarse bajo la misma
licencia si se distribuye o se pone a disposición a través de una red. Existe una
licencia PointSav-Commercial independiente como alternativa de pago para quien necesite
distribuir una versión modificada, u ofrecerla como servicio de red, sin esa obligación
de copyleft.

**Por qué importa:** un prestamista o el propio ingeniero de un propietario puede leer y
auditar el código fuente completo antes de decidir si confiar en él — el código no es una
caja negra detrás de un muro de pago.

---

## Véase también

- [[tool-construction]] — la herramienta hermana de libro mayor para desarrollo y
  construcción, construida sobre el mismo diseño de partida doble y que comparte el
  renderizador de este motor
- [[service-fs]] — el sustrato de almacenamiento de registro de anexado contra el que está
  diseñado el modo de archivo previsto
- [[totebox-archive]] — el archivo de propiedad del titular donde se prevé que vivan los
  registros de una entidad
- [[service-input]] — analiza y direcciona por contenido un documento de origen antes de
  que se convierta en un asiento de diario propuesto
