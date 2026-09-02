---
schema: foundry-doc-v1
title: "Generar un paquete de estados financieros"
slug: generate-a-financial-statement-package
short_description: "Ejecuta el binario de estados para un ejercicio y un período concretos y produce un paquete consolidado en HTML y PDF, recalculado desde los CSV de asientos en cada ejecución — la herramienta se niega a representar antes que publicar una cifra que no cuadra."
category: how-to
index_group: financial-construction-tools
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Ingenieros (con las manos en el teclado); operadores del cliente"
last_edited: 2026-09-01
editor: pointsav-engineering
language: es
language_protocol: TRANSLATE-ES
paired_with: generate-a-financial-statement-package.md
---

## Requisitos previos

- Un conjunto de herramientas Rust funcional (véase [[install-toolchain]])
- Una copia de los tres crates de contabilidad — la biblioteca del motor, el crate binario de este despliegue y el renderizador compartido
- Acceso de lectura al repositorio de datos contables que el crate binario resuelve al arrancar
- Permiso de escritura sobre el directorio de salida, o `ACCOUNTING_OUTPUT_DIR` apuntando a un lugar donde pueda escribir

Esta tarea no requiere ningún servicio en ejecución. Los tres crates declaran cero dependencias de terceros, deliberadamente, de modo que una primera compilación construye el código propio y no descarga nada.

Hay un requisito que no puede satisfacerse por configuración, y conviene saberlo antes de la primera ejecución: **la ubicación del repositorio de datos de entrada está fijada en el binario como una ruta absoluta.** No existe `--data-dir`, ni argumento posicional, ni variable de entorno que la desplace. Una copia cuyo repositorio de datos esté en otro sitio falla en la primera lectura, nombrando un directorio que no es el suyo. Solo la ubicación de *salida* es redirigible.

## Propósito

Representar el paquete consolidado de estados financieros de una entidad — Estado de situación financiera, Estado de resultados (pérdidas), Estado de cambios en el patrimonio de los partícipes, Estado de flujos de efectivo y las Notas — en HTML y PDF, para un ejercicio y un período.

Nada del paquete se almacena entre ejecuciones. Cada cifra se recalcula desde los CSV de asientos cada vez: los asientos se pliegan en libros mayores por cuenta, los mayores en un balance de comprobación, el balance se consolida en el grupo y las líneas consolidadas las recoge la maqueta del estado. Un estado representado es una vista de los asientos tal como están en ese momento, no un informe guardado que pueda desviarse de ellos.

Para el diseño del libro mayor que hay debajo, véase [[tool-accounting]].

## Procedimiento

### 1. Trabajar desde el directorio del propio crate binario

```bash
cd <copia>/tool-accounting-pro-01
```

Estos crates no forman un espacio de trabajo de Cargo. Son tres paquetes hermanos unidos por dependencias de ruta, cada uno con su propio fichero de bloqueo — una decisión deliberada, ya que el crate que contiene datos financieros reales está pensado para entregarse a un revisor de forma aislada. No hay una raíz de espacio de trabajo desde la que ejecutar `cargo run -p`, que es justo lo primero que intentará quien llegue desde [[generate-a-construction-cost-estimate]] y no encontrará aquí.

### 2. Comprobar las entradas

La ejecución lee seis cosas: cuatro ficheros maestros en la raíz del repositorio de datos, un directorio de asientos y un registro de hechos.

| Entrada | Qué contiene |
|---|---|
| `accounts.csv` | El plan de cuentas, una fila por entidad y cuenta |
| `entities.csv` | El registro de entidades — denominación legal y los demás datos permanentes de cada una |
| `consolidation.csv` | Qué entidades consolidan en la entidad informante, y desde cuándo |
| `periods.csv` | Fecha de cierre y fecha de finalización por entidad, ejercicio y período |
| `journals/<año>/*.csv` | Todas las transacciones registradas de ese ejercicio |
| `register/<año>/events.csv` | El registro de hechos revelables del que se deriva la nota de hechos posteriores |

Tres de estos ficheros tienen esquemas que los lectores comparan por igualdad exacta contra sus propias constantes de encabezado — un fichero cuyas columnas se hayan desviado se rechaza imprimiendo tanto el encabezado hallado como el esperado, en lugar de analizarse a la buena de Dios.

`accounts.csv`, nueve columnas:

```
entity_code,account_code,ledger_account,statement,periods,sign,posting_tag,sourced,notes
```

`periods.csv`, seis columnas:

```
entity,fiscal_year,period,period_end_date,completion_date,lock_status
```

Cada fichero de asientos, diecisiete columnas:

```
entity_code,account_code,fiscal_year,period,txn_date,counterparty_type,counterparty_id,description,ref_no,ref_source,subtotal_cad,gst_number,gst_amount,currency_code,amount_foreign,amount_cad,invoice_number
```

Dos de estos campos se comportan de forma menos simple de lo que su nombre sugiere:

- **`sign`**, en el plan de cuentas, admite `+1`, `-1`, `TBD` o vacío. `TBD` y vacío no son valores predeterminados — significan que el criterio de signo de esa cuenta no está confirmado, y toda cuenta en ese estado queda excluida de todas las cifras calculadas del paquete y se nombra en el resumen de la ejecución. Un signo sin confirmar es una laguna visible, nunca una suposición.
- **`period`**, en una fila de asiento, es siempre un trimestre disjunto. El acumulado del ejercicio es una propiedad del *estado*, formada sumando trimestres en el momento del informe; nunca un valor que una fila de asiento pueda llevar.

Los ficheros de asientos se descubren por prefijo de nombre — `<entidad>_<cuenta>_<año>_<trimestre>_*.csv` — y el trimestre del nombre es lo que decide si un fichero entra en el ámbito del período representado. El nombre duplica a propósito lo que ya está dentro del fichero, para poder contrastar ambos.

### 3. Elegir ejercicio y período

```bash
cargo run --bin statements -- --year 2024 --period Q1
```

El juego completo de opciones es `--year YYYY`, `--period Q1|Q2|Q3|YE` y `-h`/`--help`. Cualquier otra cosa se rechaza por su nombre junto con la línea de uso. El argumento de período se recorta y se pasa a mayúsculas, de modo que `q1` funciona. El separador `--` es obligatorio: sin él, cargo consume las opciones.

Los cuatro períodos se representan. `YE` es el paquete anual, con una sola columna monetaria. `Q1` es un paquete intermedio condensado con dos — el trimestre corriente junto a un comparativo del año anterior. `Q2` y `Q3` son paquetes intermedios condensados cuyos estados de flujo llevan cuatro columnas monetarias: una ventana discreta de tres meses y el acumulado del ejercicio, cada uno junto a su comparativo. La ventana discreta es una segunda pasada completa de la misma cadena de cálculo, no una resta de una cifra acumulada, y se somete a los mismos controles descritos en Verificación.

**Indique ambas opciones de forma explícita.** Cada una tiene un valor predeterminado fijado en el código — el período recae en el paquete anual, y el ejercicio en aquel para el que se compiló originalmente este despliegue. Confiar en cualquiera de los dos es ejecutar un comando cuya salida depende de una constante que no se ve en la línea de comandos.

### 4. Leer el resumen en consola

A diferencia del binario hermano de informes de construcción, que deliberadamente no imprime importe alguno en el terminal, este sí imprime sus cifras principales. La intención es distinta: son los números que se comparan con el PDF representado para confirmar que se está mirando la ejecución que se acaba de hacer.

```
EXAMPLE-LP-01 consolidated (EXAMPLE-LP-01 + EXAMPLE-TC-01 + EXAMPLE-TC-02) — FY2024 Q1: 26 account(s) computed, 2 skipped (sign unconfirmed), 3 note-only
  BS: Cash 40,000  |  AP 12,500  |  Deficit (57,500)  |  Total equity (deficit) 27,500  |  Total liabilities and equity 40,000
  IS: Share-based comp 30,000  |  Professional 18,000  |  Advisory 9,000  |  Bank 500  |  Opex 57,500  |  Income (loss) (57,500)
  -> /tmp/statements-scratch/2024/EXAMPLE-LP-01_statements_Q1.html
  -> /tmp/statements-scratch/2024/EXAMPLE-LP-01_statements_Q1.pdf
```

Todas las cifras, códigos de entidad y rutas anteriores son inventados para esta guía. La *forma* es real: dólares enteros, separadores de millares, negativos entre paréntesis y una cifra nula como raya — la misma convención que usan los estados representados, de modo que terminal y página pueden compararse línea a línea sin aritmética mental.

Lea los dos últimos recuentos de la primera línea antes que nada. `skipped (sign unconfirmed)` es el número de cuentas excluidas de todas las cifras del paquete. Un recuento distinto de cero no invalida la ejecución — significa que el paquete está incompleto de forma consciente, y el propio documento lo revela.

## Resultado esperado

Dos ficheros en el directorio de salida, que la ejecución crea si no existe:

| Fichero | Qué es |
|---|---|
| `<código-de-entidad>_statements.html` / `.pdf` | El paquete anual |
| `<código-de-entidad>_statements_Q1.html` / `.pdf` | Un paquete intermedio, con el sufijo de su período |

El documento anual no lleva sufijo y todos los períodos intermedios sí. Esa asimetría no es un descuido — el documento anual se referencia por esa ruta exacta en otros sitios, y mantenerla estable era justamente el objetivo.

`ACCOUNTING_OUTPUT_DIR` redirige todo el árbol a otro lugar, añadiendo el ejercicio como subdirectorio. Úselo. La ubicación de salida predeterminada está dentro de un repositorio de datos compartido y versionado, y una pasada de representación hecha para mirar un PDF no debería ensuciar un artefacto ya confirmado ni competir con otro proceso que escriba las mismas dos rutas.

## Verificación

La mayor parte de la verificación la hace la propia ejecución, antes de escribir nada. Hay tres controles entre la población calculada y la página representada, y cada uno se niega en redondo en lugar de representar con una advertencia:

**La población debe cuadrar, o el descuadre debe ser atribuible.** Se suma la población calculada de partida doble; un residuo distinto de cero significa que no cuadra. Si no se excluyó ninguna cuenta por signo sin confirmar, ese residuo es un defecto aritmético sin nada a lo que atribuirlo, y la ejecución se niega. Si *sí* hubo cuentas excluidas — cada una nombrada — entonces el residuo es la consecuencia medida de una laguna ya revelada, y la ejecución continúa y lo revela en el propio estado de situación financiera. Negarse en ese segundo caso suprimiría precisamente el documento que hace visible la laguna.

**Toda línea calculada con saldo distinto de cero debe aparecer en la maqueta.** Cada epígrafe del estado declara qué líneas consolidadas consume. Cualquier línea con dinero real que ningún epígrafe reclame es huérfana, y la ejecución se niega, nombrándola con su saldo. Un estado que descarta una cifra en silencio es incorrecto, no simplemente incompleto.

**El estado de flujos de efectivo debe cuadrar con la línea de efectivo calculada.** La variación de efectivo derivada se compara con el saldo de efectivo calculado del propio período. Una discrepancia rechaza la representación e imprime ambas cifras.

De modo que un paquete que existe ya ha superado los tres. Lo que queda por su parte:

- **Compare el resumen de consola con la página representada.** Usan el mismo formato precisamente por eso; una discrepancia significa que está leyendo un PDF antiguo.
- **Lea los nombres de las cuentas omitidas.** Los imprime el paso de consolidación. Cada una es una cuestión abierta real en el plan de cuentas, no una limitación de la herramienta.
- **Busque `POPULATION DOES NOT BALANCE`** en la salida de consola. Solo aparece cuando se activa la rama de laguna revelada descrita arriba, y el mismo residuo aparece en el documento.
- **Abra el PDF.** Las columnas comparativas de un paquete intermedio imprimen `n/a`, nunca una raya — una raya en un estado presentado afirma que la línea es cero, y aquí el período comparativo no está medido, que no es lo mismo que ser cero. Si una columna comparativa muestra rayas, algo ha cambiado y esa distinción se ha perdido.

## Lo que esta tarea no hace

- **No audita, ni certifica, ni presenta nada.** Representa un documento. Si ese documento se presenta, se revisa o se utiliza queda enteramente fuera de este comando.
- **No calcula saldos de apertura.** Las posiciones de apertura aún no tienen origen, de modo que toda cifra del balance es actividad medida desde una apertura en cero. El documento representado lo indica en una nota visible justo después de la tabla del balance. El estado de resultados es solo de flujo y no lleva esa salvedad, porque no le aplica. Esto significa que el balance es una plantilla real con cifras provisionales — trátelo como tal.
- **No calcula el período comparativo.** Las columnas comparativas se representan porque los estados intermedios presentados las llevan, y todas sus celdas de cifra dicen `n/a`. La forma es real; el período que hay detrás no está medido.
- **No representa los estados de ninguna otra entidad.** Binarios hermanos del mismo crate representan el paquete individual del socio gestor y los de las filiales. Cada uno toma sus propios argumentos y es una tarea distinta.
- **No representa el informe de gestión.** Ese es otro binario.
- **No imprime un balance de comprobación ni el detalle del mayor.** De eso se encarga el binario predeterminado del crate, y conviene ejecutarlo cuando una cifra del estado resulte sorprendente.
- **No escribe asientos.** Frente al repositorio de datos, este comando es estrictamente de solo lectura. Sus únicas escrituras son los dos ficheros de salida.

## Casos límite

- **Un valor de `--period` no reconocido** se rechaza por su nombre, con la línea de uso y estado de salida 1. No se calcula nada.
- **`--year` sin valor o con un valor no numérico** falla igual. También cualquier argumento no reconocido — no hay argumentos posicionales a los que caer.
- **La falta de una fila en `periods.csv`** para la entidad, el ejercicio y el período solicitados es un error duro que nombra `periods.csv`. La ventana de hechos posteriores no puede clasificarse sin una fecha de cierre y una de finalización, y la ejecución no las adivinará. Es el fallo más habitual la primera vez que se representa un período nuevo.
- **Que no exista el registro de hechos del año siguiente no es un error.** La ventana de hechos posteriores se abre el día después del cierre, así que los hechos que la cumplen viven en el registro del año *siguiente*; la ejecución lo carga cuando existe y continúa sin él cuando no.
- **Un encabezado desviado** — en el plan de cuentas, en un fichero de asientos o en el registro de períodos — rechaza la ejecución e imprime el encabezado hallado junto al esperado. Repare el fichero en lugar de sortearlo.
- **Una fila con un número de campos incorrecto** no se omite con una advertencia. Aborta la ejecución, nombrando el fichero y el número de fila.
- **Un importe con más de dos decimales se rechaza, no se redondea.** La precisión por debajo del céntimo en un CSV es ruido de coma flotante procedente de algo aguas arriba, y el mensaje de error lo dice. Cuantifique en el origen.
- **Sumar dos monedas distintas se rechaza.** La conversión es una operación nombrada y con fuente citada en otro lugar; nunca ocurre de forma implícita dentro de una suma.
- **Los ficheros de salida se sobrescriben en el sitio.** Sin versionado, sin directorio con marca de tiempo, sin confirmación. Copie lo que necesite conservar, o apunte `ACCOUNTING_OUTPUT_DIR` a un lugar desechable.

## Reversión

No hay nada que deshacer en los datos de origen: la ejecución lee los ficheros maestros, los asientos y el registro, y nunca escribe en ellos. Sus únicas escrituras son los dos ficheros de salida. Bórrelos, o vuelva a ejecutar para reemplazarlos.

Si representó en la ubicación predeterminada y ensució un artefacto versionado, la corrección es la habitual para un fichero versionado — restáurelo desde el control de versiones y vuelva a ejecutar con `ACCOUNTING_OUTPUT_DIR` definido.

## Pasos siguientes

- [[generate-a-construction-cost-estimate]] — la tarea de informes del libro mayor de construcción hermano, que comparte el renderizador de esta herramienta
- [[generate-a-payroll-register]] — el registro de horas de mano de obra en el lado de construcción de la misma familia
- [[export-structured-data]] — llevar la salida representada o sus registros de origen a otro lugar

## Véase también

- [[tool-accounting]] — el diseño de partida doble, el modelo de datos y la postura de preparación para auditoría que estos estados representan
- [[tool-construction]] — el libro mayor hermano de desarrollo y construcción, construido sobre el mismo diseño
- [[financial-and-construction-tools-overview]] — dónde encaja esta herramienta entre las herramientas financieras y de construcción
